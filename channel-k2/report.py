"""Gói kênh 2 — bảng tóm tắt hồ sơ cầu từ số liệu thô ($K2C_DATA). In markdown; chỉ số tự tính, không phải chỉ số YouTube.
Không in tên người bình luận (số liệu thô không lưu tên)."""
import json, os, statistics as st, sys
from pathlib import Path
DATA = Path(os.environ.get("K2C_DATA", Path.home() / ".cache/cine-channel-k2"))

def table(slug):
    d = json.loads((DATA / f"demand_{slug}.json").read_text())
    vs = sorted(d["videos"], key=lambda v: -v["views"])
    big = [v for v in vs if v["views"] >= 500_000]
    print(f"### {slug}: {d['title']}")
    print(f"- video dài duy nhất: {len(vs)}; ≥ 500 nghìn lượt: {len(big)} → Cầu-bền: {'CÓ' if big else 'KHÔNG'}")
    if big:
        print(f"- phút video ≥ 500 nghìn: {[v['min'] for v in big]} · trung vị {st.median(v['min'] for v in big):.1f}")
    rec = [v for v in vs if v["pub"] >= "2026-01-01"]
    print(f"- video đăng 2026 trong top: {len(rec)}; lượt xem cao nhất của nhóm này: {max([v['views'] for v in rec], default=0):,}")
    print(f"- bình luận: {d['n_comments']} (nhãn {d['label_cov']}/{d['n_comments']}); loại: {d['kinds']}; bỏ: {d['n_drop']}")
    print("| Lượt xem | Phút | Năm | Kênh | Tiêu đề |\n|---|---|---|---|---|")
    for v in vs:
        print(f"| {v['views']:,} | {v['min']} | {v['pub'][:4]} | {v['ch']} | {v['title']} |")
    print()

for s in (sys.argv[1:] or ["container", "jet-airliner", "card-networks"]):
    if (DATA / f"demand_{s}.json").exists(): table(s)
