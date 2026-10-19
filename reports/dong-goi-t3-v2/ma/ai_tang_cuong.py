#!/opt/cine/bin/python
"""ĐÓNG-GÓI-T3 v2 việc 2 · [F] AI TĂNG CƯỜNG thumbnail từ khung gốc dựng bằng máy V7B: POST /v1/images/edits, gpt-image-2.5-sunburst-2026-09-08
(model sửa ảnh chính xác nhất theo tài liệu; cùng bản ghim với PT3). Khoá do proxy gắn cho api.openai.com — không đọc/in/ghi khoá; UA trung tính.
Chỉ tăng chi tiết bề mặt (đá, nước, lửa/khói, thân pin nổi, ánh đèn); bố cục/địa hình/số vật giữ nguyên (prompt + kiểm tay trên tờ so).
Ghi mỗi lệnh vào ai/goi-api.jsonl (prompt nguyên văn, model gửi/nhận, usage, $ theo bảng giá 18/10: ảnh vào $8/M, chữ vào $5/M, ảnh ra $30/M, C2PA).
Mốc theo dõi $6, chặn an toàn $10 (cộng mọi lệnh trong nhật ký). Dùng: ai_tang_cuong.py <ảnh gốc> <tên> <khoá prompt> <thư mục ra>"""
import base64, hashlib, json, os, sys, time, urllib.request, uuid
from pathlib import Path
from PIL import Image
HERE = Path(__file__).resolve().parent.parent; LOG = HERE / "ai" / "goi-api.jsonl"
UA = "CineLab-research (+https://github.com/HungQuach301/cine-lab)"; MODEL = "gpt-image-2.5-sunburst-2026-09-08"; MOC, CHAN = 6.0, 10.0
P_COMMON = ("This is a frame from our own 3D historical reconstruction (night of 13-14 September 1782 at Gibraltar). Enhance SURFACE DETAIL ONLY so it reads as a rich, "
            "cinematic, physically lit 3D render. Keep EXACTLY the same composition, camera, horizon line, silhouette of the Rock, coastline, every object's position, size and count. "
            "Do NOT add, remove, move or duplicate anything: no new ships, boats, buildings, lights, people, flags, text, letters, logos, watermark or signatures. "
            "No people anywhere. No modern objects. Keep the night colour palette (deep blue sky, dark sea) and the existing light sources only.")
PROMPTS = {
 "pin1782": P_COMMON + " Improve: the limestone rock face (fine natural cliff texture, ledges, scrub, subtle moonlit highlights) while keeping its outline; the sea surface (small waves, "
            "realistic reflections of the existing fires); the TEN existing floating batteries: keep them as low, flat-topped 18th-century wooden hulks with sloping wooden roofs, keep exactly ten, "
            "same positions — add wood planking detail and charring; the fires already burning on them: more detailed flames and embers and dark smoke rising from them, staying on the hulls; "
            "keep the small white flags as they are, small and not prominent. The fires must stay where they are and must not spread to the town or the Rock.",
 "pho2026": P_COMMON.replace("night of 13-14 September 1782 at Gibraltar", "night of October 2026 at Gibraltar") + " Improve: the limestone rock face texture; the sea surface and the reflections of "
            "the existing city lights; the existing buildings (keep their shapes and lit windows, add facade material detail). Do not add any new lights, buildings, ships or aircraft.",
}
def spent():
    return sum(json.loads(l).get("usd", 0) for l in LOG.read_text().splitlines()) if LOG.exists() else 0.0
def call(src, name, key, out, size="2560x1440"):
    if spent() > CHAN: raise SystemExit(f"dừng: OpenAI đã {spent():.2f} > chặn {CHAN}")
    out = Path(out); out.mkdir(parents=True, exist_ok=True); w, h = map(int, size.split("x"))
    inp = out / f"{name}-vao.png"; Image.open(src).convert("RGB").resize((w, h), Image.LANCZOS).save(inp)
    bnd = uuid.uuid4().hex; parts = []
    for k, v in {"model": MODEL, "prompt": PROMPTS[key], "size": size, "quality": "high", "n": "1", "output_format": "jpeg", "output_compression": "90", "stream": "true", "partial_images": "1"}.items():
        parts.append(f'--{bnd}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
    parts.append(f'--{bnd}\r\nContent-Disposition: form-data; name="image[]"; filename="{inp.name}"\r\nContent-Type: image/png\r\n\r\n'.encode() + inp.read_bytes() + b"\r\n")
    parts.append(f"--{bnd}--\r\n".encode()); body = b"".join(parts)
    rq = urllib.request.Request("https://api.openai.com/v1/images/edits", data=body, headers={"Content-Type": f"multipart/form-data; boundary={bnd}", "User-Agent": UA})
    t0 = time.time(); rec = {"anh": name, "khoa_prompt": key, "endpoint": "POST /v1/images/edits", "model_req": MODEL, "prompt": PROMPTS[key],
                             "params": {"size": size, "quality": "high", "n": 1, "output_format": "jpeg", "output_compression": 90, "stream": True, "partial_images": 1},
                             "input": {"file": inp.name, "sha256": hashlib.sha256(inp.read_bytes()).hexdigest(), "goc": str(src)}, "date_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    try:
        d = None; npart = 0
        with urllib.request.urlopen(rq, timeout=900) as r:   # SSE: image_edit.partial_image … image_edit.completed (như PT3)
            for line in r:
                line = line.decode().strip()
                if not line.startswith("data:"): continue
                ev = json.loads(line[5:].strip())
                if ev.get("type", "").endswith("partial_image"): npart += 1
                if ev.get("type", "").endswith("completed"): d = {"data": [{"b64_json": ev["b64_json"]}], "usage": ev.get("usage", {}), "model": ev.get("model", MODEL)}
        rec["http"] = 200; rec["partial_events"] = npart
        if d is None: raise RuntimeError("không có sự kiện completed")
    except urllib.error.HTTPError as e:
        rec["http"] = e.code; rec["loi"] = e.read().decode()[:600]; rec["usd"] = 0
        with open(LOG, "a") as f: f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        print("LỖI", e.code, rec["loi"][:300]); return None
    u = d.get("usage", {}); it = u.get("input_tokens_details", {}); img_in = it.get("image_tokens", 0); txt_in = it.get("text_tokens", 0); img_out = u.get("output_tokens", 0)
    rec["usage"] = u; rec["usd"] = round(img_in * 8e-6 + txt_in * 5e-6 + (img_out + 100 * rec.get("partial_events", 0)) * 30e-6, 4); rec["ghi_chu_gia"] = "usage sự kiện completed + 100 token ra/ảnh tạm (như PT3)"; rec["secs"] = round(time.time() - t0, 1)
    b = base64.b64decode(d["data"][0]["b64_json"]); fo = out / f"{name}-ai.jpg"; fo.write_bytes(b)
    rec.update(file=fo.name, sha256=hashlib.sha256(b).hexdigest(), bytes=len(b), model_resp=d.get("model", MODEL), size_resp=f"{Image.open(fo).size[0]}x{Image.open(fo).size[1]}",
               c2pa=(b"c2pa" in b), c2pa_segments=["APP11+jumb+c2pa"] if (b"jumb" in b and b"c2pa" in b) else [])
    with open(LOG, "a") as f: f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(name, rec["http"], rec["usd"], rec["secs"], "C2PA", rec["c2pa"], "luỹ kế $%.3f" % spent())
    if spent() > MOC: print("VƯỢT MỐC THEO DÕI $%.2f — lợi ích: xem báo cáo" % MOC)
    return fo
if __name__ == "__main__":
    call(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
