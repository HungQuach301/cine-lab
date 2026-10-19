#!/opt/cine/bin/python
"""ĐÓNG-GÓI-T3 việc 4b · xuất 8 thumbnail ứng viên tên trung tính T1…T8 (thứ tự xáo cố định, khoá ở thumbnail/khoa.json):
1280×720 PNG + 168×94 + 360×202 vào repo (thumbnail/xuat-dieu-phoi/); 3840×2160 ra ngoài git /var/tmp/cine-out/dong-goi-t3/ (SHA-256 trong khoa.json).
Kiểm đọc cỡ nhỏ: OCR cục bộ (RapidOCR) trên 168×94 (phóng ×4 để OCR nhìn được — mô phỏng mắt người trên điện thoại DPI cao) và 360×202."""
import hashlib, json, random, shutil, sys
from pathlib import Path
SRC = Path(sys.argv[1]); REP = Path(__file__).resolve().parent.parent / "thumbnail"; X = REP / "xuat-dieu-phoi"; X.mkdir(parents=True, exist_ok=True)
OUT4K = Path("/var/tmp/cine-out/dong-goi-t3"); OUT4K.mkdir(parents=True, exist_ok=True)
names = ["A1", "A2", "B1", "B2", "C1", "C2", "D1", "D2"]; T = [f"T{i}" for i in range(1, 9)]; random.Random(19102026).shuffle(T); key = dict(zip(names, T))
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
from rapidocr_onnxruntime import RapidOCR
from PIL import Image
ocr = RapidOCR(); rec = {}
for n, t in key.items():
    for sz in ("1280x720", "360x202", "168x94"): shutil.copy(SRC / f"{n}-{sz}.png", X / f"{t}-{sz}.png")
    shutil.copy(SRC / f"{n}-3840x2160.png", OUT4K / f"{t}-3840x2160.png")
    o = {}
    for sz, up in (("168x94", 4), ("360x202", 2)):
        im = Image.open(X / f"{t}-{sz}.png"); tmp = OUT4K / f"_ocr_{t}_{sz}.png"; im.resize((im.width * up, im.height * up), Image.BICUBIC).save(tmp)
        r, _ = ocr(str(tmp)); tmp.unlink(); o[sz] = [[txt, round(float(c), 2)] for _, txt, c in (r or [])]
    rec[t] = {"huong": n, "png_1280_sha256": sha(X / f"{t}-1280x720.png"), "png_1280_bytes": (X / f"{t}-1280x720.png").stat().st_size,
              "png_4k_ngoai_git": str(OUT4K / f"{t}-3840x2160.png"), "png_4k_sha256": sha(OUT4K / f"{t}-3840x2160.png"), "ocr_co_nho": o}
json.dump({"ghi": "Khoá T1…T8 ↔ hướng (A1…D2). KHÔNG đưa tệp này cho người chấm/điều phối trước khi chấm mù xong.", "khoa": rec}, open(REP / "khoa.json", "w"), indent=1, ensure_ascii=False)
for t in sorted(rec): print(t, rec[t]["huong"], rec[t]["png_1280_bytes"], rec[t]["ocr_co_nho"])
