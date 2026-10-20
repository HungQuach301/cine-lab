#!/opt/cine/bin/python
"""ĐÓNG-GÓI-T3 · gọi `claude -p` (ghim model, thư mục tạm trống, không thấy repo) — mẫu channel-k2/k2c-t2-01/ai.py.
Khoá: ANTHROPIC_API_KEY lấy từ $CONSOLE_API_KEY trong môi trường tiến trình con; không in, không ghi.
Mốc theo dõi $3 (vượt thì ghi một dòng lợi ích rồi làm tiếp); chặn an toàn $10 → dừng.
Ghi nguyên văn trả lời vào <out>/<tag>.raw.txt (+ .json) và chi phí vào reports/dong-goi-t3-v2/cost.jsonl.
Ảnh: truyền đường dẫn tuyệt đối trong prompt + --allowedTools Read (người chấm chỉ đọc đúng các tệp được đưa)."""
import json, os, re, shutil, subprocess, tempfile
from pathlib import Path
HERE = Path(__file__).resolve().parent; LOG = HERE.parent / "cost.jsonl"
MOC, CHAN = 3.0, 10.0
def spent():
    return sum(json.loads(l)["usd"] for l in LOG.read_text().splitlines()) if LOG.exists() else 0.0
def ai(prompt, tag, model="claude-sonnet-5-5", out=None, images=None, save_raw=True):
    if spent() > CHAN: raise SystemExit(f"dừng: đã tiêu ${spent():.2f} > chặn an toàn ${CHAN}")
    env = dict(os.environ, ANTHROPIC_API_KEY=os.environ["CONSOLE_API_KEY"])
    with tempfile.TemporaryDirectory() as cwd:
        cmd = ["claude", "-p", "--model", model, "--output-format", "json"]
        if images:
            for i, p in enumerate(images):
                shutil.copy(p, Path(cwd) / f"img{i:02d}{Path(p).suffix}")
            prompt = prompt.replace("{IMAGES}", "\n".join(f"{Path(cwd) / f'img{i:02d}{Path(p).suffix}'}" for i, p in enumerate(images)))
            cmd += ["--allowedTools", "Read"]
        for _ in range(3):
            r = subprocess.run(cmd, input=prompt, capture_output=True, text=True, env=env, cwd=cwd, timeout=1800)
            try: d = json.loads(r.stdout)
            except Exception: continue
            u = d.get("usage", {})
            with open(LOG, "a") as f:
                f.write(json.dumps({"tag": tag, "model": model, "served": sorted(d.get("modelUsage", {})), "usd": d.get("total_cost_usd", 0),
                                    "in": u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0) + u.get("cache_read_input_tokens", 0), "out": u.get("output_tokens", 0)}) + "\n")
            res = d.get("result", "")
            if out and save_raw: Path(out).mkdir(parents=True, exist_ok=True); (Path(out) / f"{tag}.raw.txt").write_text(res)
            m = re.search(r"[\[{].*[\]}]", res, re.S)
            if m:
                try:
                    j = json.loads(m.group(0))
                    if out: (Path(out) / f"{tag}.json").write_text(json.dumps(j, indent=1, ensure_ascii=False))
                    return j
                except Exception: pass
    return None
