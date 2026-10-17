"""T3 · gói TUYẾN · áp treatment-patch.json lên BẢN SAO vay-ham/treatment.json và chạy tự kiểm TRƯỚC/SAU — không ghi đè bản gốc.
Ba lượt (thư mục tạm ngoài repo, mỗi lượt chép tu_kiem.py + treatment.json vào đó vì tu_kiem.py đọc/ghi cạnh chính nó):
  (1) TRƯỚC: tu_kiem.py gốc trên bản sao treatment gốc.
  (2) SAU-gốc: tu_kiem.py gốc trên bản sao đã vá → gốc không biết loại 'bản đồ chiến lược' (assert) → ghi lỗi; chạy lại với SM* tạm coi là 'bản đồ lịch sử' để thấy tác động lên luật cũ.
  (3) SAU-strategic: tu_kiem.py gốc + vá tối thiểu (thêm loại 'bản đồ chiến lược' ngoài 3D; NC-H2 bỏ qua loại này theo B3; thêm khối luật strategic B3) → tuyen/tu_kiem_strategic.diff.
Kết quả: tuyen/tu-kiem-truoc-sau.json + in bảng.
Dùng: /opt/cine/bin/python -I channel-k2/k2c-t3-01/tuyen/ap_patch.py"""
import copy, difflib, hashlib, json, shutil, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
VH = HERE.parent / 'vay-ham'
PY = sys.executable

STRAT_BLOCK = '''
    # [TUYẾN] luật strategic B3 (đề xuất NC-BD §3.1): ≤ 15 % thời lượng, ≤ 8 s/lần, ≤ 2 lần/chương, không hai shot strategic liền nhau
    st = [s for s in shots if s["loai"] == "bản đồ chiến lược"]
    per_ch = Counter(s["ch"] for s in st)
    lien = [[a["id"], b["id"]] for a, b in zip(shots, shots[1:]) if a["loai"] == b["loai"] == "bản đồ chiến lược"]
    out["strategic"] = {"so_lan": len(st), "tong_s": sum(s["dur"] for s in st), "ty_le": round(sum(s["dur"] for s in st) / T, 4), "dai_nhat_s": max([s["dur"] for s in st] or [0]),
                        "moi_chuong": dict(per_ch), "lien_nhau": lien, "shot": [s["id"] for s in st],
                        "dat": (sum(s["dur"] for s in st) / T <= 0.15) and all(s["dur"] <= 8 for s in st) and all(v <= 2 for v in per_ch.values()) and not lien}
    chk("strategic tỷ trọng", out["strategic"]["ty_le"], 0.15)
    for s in st: chk(f"strategic {s['id']} giây", s["dur"], 8.0)
'''


def patched_tu_kiem(src):
    s = src
    s = s.replace('LOAI = ["3D phố", "3D vùng", "bản đồ lịch sử", "tranh Ken Burns", "ảnh", "footage", "thẻ số"]',
                  'LOAI = ["3D phố", "3D vùng", "bản đồ lịch sử", "tranh Ken Burns", "ảnh", "footage", "thẻ số", "bản đồ chiến lược"]  # [TUYẾN] loại mới B3')
    s = s.replace('glob = [s for s in shots if s.get("agl_max_km", 0) > 50]',
                  'glob = [s for s in shots if s.get("agl_max_km", 0) > 50 and s["loai"] != "bản đồ chiến lược"]  # [TUYẾN] B3: strategic không tính NC-H2')
    s = s.replace('    out["sat_nguong_5pct"] = near\n', STRAT_BLOCK + '    out["sat_nguong_5pct"] = near\n')
    s = s.replace('out["footage"]["dat"], not out["shot_khong_claim"]])', 'out["footage"]["dat"], not out["shot_khong_claim"], out["strategic"]["dat"]])')
    assert s.count('[TUYẾN]') == 3 and 'out["strategic"]["dat"]])' in s, 'vá tu_kiem không khớp bản gốc'
    return s


def apply(tr, patch):
    tr = copy.deepcopy(tr); shots = tr['shots']
    for op in patch['ops']:
        i = next(k for k, s in enumerate(shots) if s['id'] == op.get('ref', op.get('id')))
        if op['op'] == 'insert_before': shots.insert(i, copy.deepcopy(op['shot']))
        elif op['op'] == 'update': shots[i].update(copy.deepcopy(op['set']))
    return tr


def run(script_src, tr):
    d = Path(tempfile.mkdtemp(prefix='tuyen-tk-'))
    (d / 'tu_kiem.py').write_text(script_src); (d / 'treatment.json').write_text(json.dumps(tr, ensure_ascii=False))
    r = subprocess.run([PY, '-I', str(d / 'tu_kiem.py')], capture_output=True, text=True)
    out = json.loads((d / 'tu-kiem.json').read_text()) if (d / 'tu-kiem.json').exists() else None
    shutil.rmtree(d)
    return r.returncode, (r.stderr.strip().splitlines() or [''])[-1], out


def main():
    src = (VH / 'tu_kiem.py').read_text(); tr0 = json.loads((VH / 'treatment.json').read_text())
    sha_goc = {'tu_kiem.py': hashlib.sha256(src.encode()).hexdigest(), 'treatment.json': hashlib.sha256((VH / 'treatment.json').read_bytes()).hexdigest()}
    patch = json.loads((HERE / 'treatment-patch.json').read_text())
    tr1 = apply(tr0, patch)
    rc0, msg0, k0 = run(src, tr0)
    rc1, msg1, k1 = run(src, tr1)
    tr1b = copy.deepcopy(tr1)
    for s in tr1b['shots']:
        if s['loai'] == 'bản đồ chiến lược': s['loai'] = 'bản đồ lịch sử'
    rc1b, msg1b, k1b = run(src, tr1b)
    src2 = patched_tu_kiem(src)
    (HERE / 'tu_kiem_strategic.diff').write_text(''.join(difflib.unified_diff(src.splitlines(True), src2.splitlines(True), 'vay-ham/tu_kiem.py', 'tu_kiem.py (+ vá TUYẾN)')))
    rc2, msg2, k2 = run(src2, tr1)
    assert sha_goc['treatment.json'] == hashlib.sha256((VH / 'treatment.json').read_bytes()).hexdigest(), 'bản gốc bị đổi!'
    ban_sao = {'so_shot': len(tr1['shots']), 'tong_s': sum(s['dur'] for s in tr1['shots']), 'sha256_ban_sao': hashlib.sha256(json.dumps(tr1, ensure_ascii=False, sort_keys=True).encode()).hexdigest()}
    out = {'sha256_goc': sha_goc, 'ban_sao_da_va': ban_sao,
           'truoc': {'rc': rc0, 'ket': msg0, 'tu_kiem': k0},
           'sau_goc': {'rc': rc1, 'ket': msg1, 'ghi_chu': 'tu_kiem.py gốc dừng ở assert loại cảnh — loại "bản đồ chiến lược" chưa có trong luật (chờ K/B3)'},
           'sau_goc_SM_coi_la_ban_do_lich_su': {'rc': rc1b, 'ket': msg1b, 'tu_kiem': k1b},
           'sau_strategic': {'rc': rc2, 'ket': msg2, 'tu_kiem': k2}}
    (HERE / 'tu-kiem-truoc-sau.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n')
    for name, k in (('TRƯỚC', k0), ('SAU (SM=bản đồ lịch sử)', k1b), ('SAU (strategic)', k2)):
        q = k['Q26b_K2']
        print(f"{name}: tổng {k['tong_s']} s, {k['so_shot']} shot | Q26b {q[0]['so_loai']}/{q[0]['ty_le_lon_nhat']} · {q[1]['so_loai']}/{q[1]['ty_le_lon_nhat']} | "
              f"NC-H2 {k['NC_H2']['so_lan']} lần {k['NC_H2']['giay']} | NC-H3 ≤60 {k['NC_H3']['le60km']} ≤3 {k['NC_H3']['le3km']} 3D/phim {k['NC_H3']['ty_le_3D_phim']} | "
              f"hồ sơ thật {k['ho_so_that']} | strategic {k.get('strategic')} | ±5% {k['sat_nguong_5pct']}")
    print('sau_goc:', rc1, msg1); print('rc:', rc0, rc1b, rc2)
    return 0


if __name__ == '__main__':
    sys.exit(main())
