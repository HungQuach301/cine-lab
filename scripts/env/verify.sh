#!/bin/bash
# CINE LAB — kiểm môi trường. Chạy đầu mỗi phiên mới: bash scripts/env/verify.sh
# In PASS/FAIL cho từng hạng mục; không sửa gì.
source /etc/profile.d/cine.sh 2>/dev/null
pass=0; fail=0
ok(){ echo "PASS  $1"; pass=$((pass+1)); }
ko(){ echo "FAIL  $1 — $2"; fail=$((fail+1)); }

echo "== Máy: $(nproc) vCPU, $(free -g | awk '/Mem/{print $2}') GB RAM, đĩa trống $(df -h / | awk 'NR==2{print $4}')"
grep -q "RESULT" /var/log/cine-setup.log 2>/dev/null && grep "RESULT" /var/log/cine-setup.log | tail -1

command -v ffmpeg >/dev/null && ok "ffmpeg $(ffmpeg -version | head -1 | cut -d' ' -f3)" || ko ffmpeg "chưa cài"
ffmpeg -hide_banner -filters 2>/dev/null | grep -q ebur128 && ok "ffmpeg ebur128 (đo LUFS)" || ko ebur128 "thiếu filter"
[ -x "$CINE_PY" ] && $CINE_PY -c "import faster_whisper, pyloudnorm, cv2, scenedetect, elevenlabs, librosa" 2>/dev/null \
  && ok "Python chính: faster-whisper, pyloudnorm, opencv, scenedetect, elevenlabs, librosa" || ko "Python chính" "thiếu gói trong /opt/cine"
[ -x "$CINE_BPY" ] && $CINE_BPY -c "import bpy; print(bpy.app.version_string)" >/tmp/bpyv 2>/dev/null \
  && ok "Blender bpy $(tail -1 /tmp/bpyv)" || ko "bpy" "chưa cài hoặc thiếu thư viện hệ thống"
ls /opt/pw-browsers 2>/dev/null | grep -q chromium && ok "Chromium (Playwright)" || ko "Chromium" "chưa tải — kiểm tên miền playwright"

# Mạng
code(){ curl -s -o /dev/null -w "%{http_code}" --max-time 20 "$1"; }
el_body=$(curl -s --max-time 20 -w "\n%{http_code}" https://api.elevenlabs.io/v1/models); c=$(tail -n1 <<<"$el_body")
[ "$c" = "200" ] && ok "ElevenLabs API (khoá được proxy gắn)" || { ko "ElevenLabs API" "HTTP $c — kiểm API credential (header xi-api-key, host api.elevenlabs.io)"; echo "      body: $(sed '$d' <<<"$el_body" | head -c 300)"; }
c=$(code https://huggingface.co/api/models/Systran/faster-whisper-small); [ "$c" = "200" ] && ok "Hugging Face" || ko "Hugging Face" "HTTP $c — thêm huggingface.co, *.huggingface.co, *.hf.co"
c=$(code https://pypi.org/simple/pip/); [ "$c" = "200" ] && ok "PyPI" || ko "PyPI" "HTTP $c"
c=$(code https://freesound.org/); [[ "$c" =~ ^(200|301|302)$ ]] && ok "Freesound" || ko "Freesound" "HTTP $c (tuỳ chọn)"

# Render thử 2 s bằng ffmpeg để chắc encoder chạy
ffmpeg -hide_banner -loglevel error -f lavfi -i testsrc2=size=1920x1080:rate=24 -t 2 -c:v libx264 -pix_fmt yuv420p -y /tmp/t.mp4 \
  && ok "ffmpeg encode H.264 1080p24" || ko "encode" "lỗi libx264"

echo "== Tổng: $pass PASS, $fail FAIL"
[ $fail -eq 0 ]
