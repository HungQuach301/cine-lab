#!/opt/cine/bin/python
"""ĐÓNG-GÓI-T3 v2 việc 7 · xuất V1…V8 + mốc vòng 1 (A2 = T2, B1 = T5) tên trung tính X01…X10 (xáo cố định) — 1280×720 PNG + 168×94 + 360×202 vào repo;
4K ra ngoài git /var/tmp/cine-out/dong-goi-t3-v2/ (SHA ở khoa.json). OCR cục bộ (RapidOCR) ở 168×94 (phóng ×4) và 360×202 (×2)."""
import hashlib, json, random, shutil, sys
from pathlib import Path
from PIL import Image
V2, V1D = Path(sys.argv[1]), Path(sys.argv[2])   # ra của ghep_v2 · xuat-dieu-phoi vòng 1
REP = Path(__file__).resolve().parent.parent / "thumbnail"; X = REP / "xuat-dieu-phoi"; X.mkdir(parents=True, exist_ok=True)
O4 = Path("/var/tmp/cine-out/dong-goi-t3-v2"); O4.mkdir(parents=True, exist_ok=True)
src = {f"V{i}": (V2, f"V{i}") for i in range(1, 9)} | {"A2-v1": (V1D, "T2"), "B1-v1": (V1D, "T5")}
names = list(src); lab = [f"X{i:02d}" for i in range(1, len(names) + 1)]; random.Random(20261019).shuffle(lab); key = dict(zip(names, lab))
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
from rapidocr_onnxruntime import RapidOCR
ocr = RapidOCR(); rec = {}
for n, x in key.items():
    d, s = src[n]
    for sz in ("1280x720", "360x202", "168x94"): shutil.copy(d / f"{s}-{sz}.png", X / f"{x}-{sz}.png")
    f4 = (d / f"{s}-3840x2160.png") if (d / f"{s}-3840x2160.png").exists() else Path("/var/tmp/cine-out/dong-goi-t3") / f"{s}-3840x2160.png"
    shutil.copy(f4, O4 / f"{x}-3840x2160.png"); o = {}
    for sz, up in (("168x94", 4), ("360x202", 2)):
        im = Image.open(X / f"{x}-{sz}.png"); t = O4 / f"_o_{x}.png"; im.resize((im.width * up, im.height * up), Image.BICUBIC).save(t); r, _ = ocr(str(t)); t.unlink()
        o[sz] = [[txt, round(float(c), 2)] for _, txt, c in (r or [])]
    rec[x] = {"ung_vien": n, "png_1280_sha256": sha(X / f"{x}-1280x720.png"), "png_1280_bytes": (X / f"{x}-1280x720.png").stat().st_size,
              "png_4k_ngoai_git": str(O4 / f"{x}-3840x2160.png"), "png_4k_sha256": sha(O4 / f"{x}-3840x2160.png"), "ocr_co_nho": o}
json.dump({"ghi": "Khoá X01…X10 ↔ ứng viên. KHÔNG đưa cho người chấm/điều phối trước khi chấm xong.", "khoa": rec}, open(REP / "khoa.json", "w"), indent=1, ensure_ascii=False)
for x in sorted(rec): print(x, rec[x]["ung_vien"], rec[x]["png_1280_bytes"], rec[x]["ocr_co_nho"]["168x94"])
