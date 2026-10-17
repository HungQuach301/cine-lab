#!/bin/bash
# V5b-2a (GG1) · kiểm môi trường dựng llvmpipe cho mô-đun xương sống thời gian: Mesa 25.2.8 + LLVM 20 (gói hệ thống — nâng cấp image có thể đổi hình,
# GPU-RD §5.3) và chuỗi UNMASKED_RENDERER thật của Chromium headless với cờ của scripts/k2tl/render.js. Thoát 0 = ĐẠT, 1 = TRƯỢT.
# Đề xuất V5b-2b: gọi script này từ scripts/env/verify.sh và ghi phiên bản vào VERSIONS.yaml (nhóm k2tl) — xem reports/V5B2A-BAO-CAO.md §8.
#   bash scripts/k2tl/env_check.sh [--json <tệp>]
set -u
WANT_MESA="25.2.8"; WANT_LLVM="20"; rc=0; J=""
[ "${1:-}" = "--json" ] && J="${2:-}"
ver() { dpkg-query -W -f='${Version}' "$1" 2>/dev/null; }
MESA=$(ver mesa-libgallium); DRI=$(ver libgl1-mesa-dri); LLVM=$(ver "libllvm${WANT_LLVM}")
chk() { if [ "$2" = 1 ]; then echo "PASS  $1"; else echo "FAIL  $1"; rc=1; fi; }
chk "mesa-libgallium ${MESA:-thiếu} (cần ${WANT_MESA})" "$([[ "$MESA" == ${WANT_MESA}* ]] && echo 1)"
chk "libgl1-mesa-dri ${DRI:-thiếu} (cần ${WANT_MESA})" "$([[ "$DRI" == ${WANT_MESA}* ]] && echo 1)"
chk "libllvm${WANT_LLVM} ${LLVM:-thiếu}" "$([ -n "$LLVM" ] && echo 1)"
PROBE=$(node -e '
const { chromium } = require("/opt/pw/node_modules/playwright");
(async () => { const out = {};
  for (const [k, f] of Object.entries({ llvmpipe: ["--use-gl=angle", "--use-angle=gl-egl"], swiftshader: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader"] })) {
    const b = await chromium.launch({ args: [...f, "--ignore-gpu-blocklist"] }); const p = await b.newPage();
    out[k] = await p.evaluate(() => { const c = document.createElement("canvas").getContext("webgl2"); if (!c) return null; const e = c.getExtension("WEBGL_debug_renderer_info"); return e ? c.getParameter(e.UNMASKED_RENDERER_WEBGL) : c.getParameter(c.RENDERER); });
    await b.close(); }
  console.log(JSON.stringify(out)); })().catch((e) => { console.log(JSON.stringify({ error: String(e) })); });' 2>/dev/null)
RL=$(echo "$PROBE" | /opt/cine/bin/python -c 'import json,sys; print(json.load(sys.stdin).get("llvmpipe") or "")' 2>/dev/null)
RS=$(echo "$PROBE" | /opt/cine/bin/python -c 'import json,sys; print(json.load(sys.stdin).get("swiftshader") or "")' 2>/dev/null)
chk "WebGL2 llvmpipe: ${RL:-không có}" "$([[ "$RL" == *"llvmpipe (LLVM ${WANT_LLVM}."* ]] && echo 1)"
chk "WebGL2 swiftshader: ${RS:-không có}" "$([[ "$RS" == *SwiftShader* ]] && echo 1)"
if [ -n "$J" ]; then /opt/cine/bin/python - "$J" "$MESA" "$DRI" "$LLVM" "$RL" "$RS" "$rc" <<'PY'
import json, sys, platform, datetime
j, mesa, dri, llvm, rl, rs, rc = sys.argv[1:]
json.dump(dict(mesa_libgallium=mesa, libgl1_mesa_dri=dri, libllvm20=llvm, renderer_llvmpipe=rl, renderer_swiftshader=rs, kernel=platform.release(),
               dat=rc == "0", luc=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")), open(j, "w"), ensure_ascii=False, indent=1)
PY
fi
[ $rc = 0 ] && echo "env_check: ĐẠT" || echo "env_check: TRƯỢT"
exit $rc
