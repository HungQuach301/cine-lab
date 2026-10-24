#!/opt/cine/bin/python
"""GIONG-T4 · đưa bản thu GỐC ElevenLabs (tốn tiền, mp3 192 kb/s, mỗi phần < 5 MB) + alignment vào git ngay khi về:
channel-k2/k2c-t4-02/am-thanh/nguon/<tag>.mp3 + <tag>.align.json, SHA256SUMS. Master WAV/FLAC tái tạo bit-trùng từ các tệp này bằng gl_ghep.py + gl_xuat.py.
Nguồn: so-ai.jsonl (tag, tep) — mọi lệnh tts của phiên (thử phát âm, thu chương, thu lại)."""
import hashlib, json, shutil
from pathlib import Path
import sys; sys.path.insert(0, str(Path(__file__).resolve().parent)); import gl_lib as GL   # noqa: E402
D = GL.EP / 'am-thanh/nguon'; D.mkdir(parents=True, exist_ok=True)
for l in open(GL.LOG):
    r = json.loads(l); src = GL.OUT / 'raw' / r['tep']
    for ext in ('.mp3', '.align.json'):
        s = src.with_name(src.name.replace('.mp3', ext)); t = D / (r['tag'] + ext)
        assert s.stat().st_size < 5_000_000, s
        if not t.exists(): shutil.copy2(s, t)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
(D / 'SHA256SUMS').write_text('# GIONG-T4 · bản thu gốc G1 (ElevenLabs /with-timestamps, mp3_44100_192) + alignment; sổ: reports/giong-t4/so-ai.jsonl. Kiểm: grep -v "^#" SHA256SUMS | sha256sum -c\n'
                              + ''.join(f'{sha(p)}  {p.name}\n' for p in sorted(D.glob('*')) if p.name != 'SHA256SUMS'))
print(len(list(D.glob('*.mp3'))), 'mp3,', round(sum(p.stat().st_size for p in D.glob('*')) / 1e6, 2), 'MB')
