#!/opt/cine/bin/python
"""ĐÓNG-GÓI-T3 việc 3 · kịch bản 2 Short (dọc 9:16, ≤ 60 s): câu NGUYÊN VĂN lời khoá v4.2 (51d1c773…), mốc trong stem G1 của KL42
(origin/k2c-t3-kl42: reports/kl42/nhip-that.json → bd_stem/kt_stem từng câu). Ước thời lượng = tổng lời + khoảng nghỉ 0,45 s + đuôi 1,5 s.
Dùng: short_kb.py <loi-khoa v4.2> <cau-stem.json> <out.json>"""
import hashlib, json, sys
from pathlib import Path
LK, CS, OUT = Path(sys.argv[1]), json.load(open(sys.argv[2])), Path(sys.argv[3])
txt = LK.read_text(); assert hashlib.sha256(LK.read_bytes()).hexdigest().startswith("51d1c773"), "lời khoá không phải v4.2"
def find(s):
    for k, L in CS.items():
        for a, b, c in L:
            if c == s: return k, a, b
    raise SystemExit("không thấy câu trong stem: " + s)
SH = {
 "S1": {"ten": "Ten floating batteries", "khoanh_khac": "pin nổi cháy đêm 13→14/9/1782",
  "cau": [("The Rock sits at the western gate of the Mediterranean.", "S1c-kieu: Rock ban ngày 2026 từ vịnh (điểm B), dọc; bộ đếm 2026"),
          ("Historians on both sides count fourteen sieges of it, between 1309 and 1783.", "tua ngược 2026 → 1309 rồi 14 nhịp khói vây (đúng H2 bản V7), bộ đếm năm chạy"),
          ("The garrison turned to heat: cannonballs heated red-hot, so that whatever they hit caught fire.", "điểm C trên Line Wall: lò nung đạn (vật minh hoạ), 8/9/1782"),
          ("Their answer to red-hot shot: ten floating batteries, designed by the French engineer d'Arçon.", "S1b: 10 pin nổi tiến vào vịnh sáng 13/9/1782 (điểm B, máy thấp)"),
          ("A French account says he'd asked to test them against red-hot shot first.", "giữ cảnh pin nổi đang tiến; bộ đếm ngày-giờ"),
          ("It was refused.", "nhịp im 0,5 s trước câu kế"),
          ("The thirteenth of September 1782.", "bộ đếm 13 SEP 1782 10:25; khói pháo hai phía"),
          ("By the next afternoon, all ten batteries were lost.", "S1a: đêm 13→14/9, 10 pin nổi cháy thành hàng trước Rock (lửa ≤ 15 % khung, không người)"),
          ("The blockade never forced a surrender.", "trời sáng 14/9: hàng pin nổi tắt dần"),
          ("The last siege ended in 1783.", "tua nhanh 1783 → 2026, phố mọc lại (điểm B)"),
          ("The argument didn't.", "S1c: Rock + phố 2026; thẻ cuối không lời: 'Full film: Gibraltar' (liên kết video liên quan)")]},
 "S2": {"ten": "Walk in across a runway", "khoanh_khac": "người đi bộ băng qua đường băng",
  "cau": [("Midnight at the Gibraltar frontier.", "S2a: đêm 2026, máy dọc 45 m trên chỗ Winston Churchill Ave cắt đường băng; đèn mép đường băng"),
          ("To walk in from Spain, you cross an airport runway.", "người đi bộ (lớp sống, bậc 5) băng qua; bộ đếm 18 OCT 2026 23:52"),
          ("Since July 2026, this gate has had no routine checks.", "máy nâng chậm thấy cổng + hàng rào"),
          ("Why build an airfield on disputed ground?", "S2b: tua ngược về 1938 — eo đất cỏ, chưa có đường băng (đúng H3)"),
          ("In March 1939, Spain protested that the works stood on \"a usurped portion\" of its territory.", "giữ 1938→1939; công trường mọc ở đầu đông"),
          ("Late in 1939, Britain began a hard runway; in 1941, it was laid across the only road to Spain.", "mặt cứng mọc từ đông sang tây, cắt qua đường (1941), lấn vịnh (1943)"),
          ("People on foot still cross the runway.", "S2c: tua tới 2026 ban ngày, dòng người băng qua"),
          ("In October 2025, people living in Spain held more than four in ten of Gibraltar's jobs.", "máy nâng cao thấy La Línea ↔ Gibraltar hai bên cổng (không vẽ ranh)"),
          ("So why, today, is the fight over it about paperwork and payrolls?", "giữ toàn cảnh; thẻ cuối không lời: 'Full film: Gibraltar'")]}}
out = {"ghi": __doc__.splitlines()[0], "loi_khoa_sha256": hashlib.sha256(LK.read_bytes()).hexdigest(), "ban_thu": "KL42 G1 (Voice Design VDLncRBHDjLHBqLhQ1Qt, eleven_multilingual_v2, speed 1,03, seed 19102026) — master WAV ngoài git đã mất theo container; trong git chỉ có MP3 96 kb/s xem trên origin/k2c-t3-kl42: reports/kl42/nghe/T3-loi-G1-v42-xem-1-ch00-02.mp3 (0 → 392,9 s) và -xem-2-ch03-05.mp3 (392,9 → 733,5 s). Cần lấy từ origin/k2c-t3-kl42 (không có trên main).", "short": {}}
for k, S in SH.items():
    rows, tot = [], 0.0
    for s, hinh in S["cau"]:
        assert s in txt, "câu không có trong lời khoá: " + s
        sid, a, b = find(s); d = round(b - a, 3); tot += d
        rows.append({"cau": s, "shot_loi": sid, "bd_stem": a, "kt_stem": b, "dai_s": d, "tep_xem": "xem-1" if a < 392.9 else "xem-2", "bd_trong_tep": round(a if a < 392.9 else a - 392.9, 3), "hinh": hinh})
    est = round(tot + 0.45 * (len(rows) - 1) + 1.5, 2)
    out["short"][k] = {"ten": S["ten"], "khoanh_khac": S["khoanh_khac"], "so_cau": len(rows), "tong_loi_s": round(tot, 2), "uoc_thoi_luong_s": est, "dat_60s": est <= 60, "so_tu": sum(len(r["cau"].split()) for r in rows), "dong": rows}
OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False))
for k, v in out["short"].items(): print(k, v["so_cau"], v["tong_loi_s"], v["uoc_thoi_luong_s"], v["so_tu"])
