"""SFX-T3 · cắt đoạn ứng viên từ tệp gốc → OGG Vorbis ≤ 2 MB trong reports/sfx-t3/ung-vien/ (48 kHz, giữ số kênh gốc),
chuẩn tuyến tính về −23 LUFS (đỉnh mẫu ≤ −1 dBFS: nếu vượt thì hạ chung, ghi lại), dốc 10 ms hai đầu. Không nén, không EQ.
  cat_ung_vien.py <spec.json> <thư mục gốc>   (spec: [{id, goc, ss, dai, ...meta}])  → ung-vien/<id>.ogg + cập nhật ung-vien/ung-vien.json"""
import json, os, sys, subprocess, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../scripts/audio'))
import lib
UV = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../ung-vien'))
def ff(*a): subprocess.run(['ffmpeg', '-v', 'error', '-nostdin', '-y', *a], check=True)
def main():
    spec = json.load(open(sys.argv[1])); src = sys.argv[2]; os.makedirs(UV, exist_ok=True)
    reg_p = os.path.join(UV, 'ung-vien.json'); reg = json.load(open(reg_p)) if os.path.exists(reg_p) else {}
    for s in spec:
        g = os.path.join(src, s['goc']); ch = int(json.loads(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'stream=channels', '-of', 'json', g], capture_output=True, text=True).stdout)['streams'][0]['channels'])
        ch = min(ch, 2); tmp = os.path.join(UV, s['id'] + '.tmp.wav')
        cut = (['-ss', str(s['ss'])] if s.get('ss') else []) + (['-t', str(s['dai'])] if s.get('dai') else [])
        ff(*cut, '-i', g, '-ac', str(ch), '-ar', '48000', '-c:a', 'pcm_f32le', tmp)
        x = lib.dec(tmp, ch, dtype=np.float64); n = len(x); r = min(int(0.01 * 48000), n // 4)
        env = np.ones(n); env[:r] = np.linspace(0, 1, r); env[n - r:] = np.linspace(1, 0, r); x = x * env[:, None]
        L = lib.integrated(np.repeat(x, 2, 1) if ch == 1 else x) if n > 0.4 * 48000 else float(20 * np.log10(np.sqrt((x ** 2).mean()) + 1e-12)) - 0.7
        gain = -23.0 - L; pk = 20 * np.log10(np.abs(x).max() + 1e-12) + gain; ha = 0.0
        if pk > -1.0: ha = pk + 1.0; gain -= ha
        y = (x * 10 ** (gain / 20)).astype(np.float32); lib.write(tmp, y, 'pcm_f32le')
        out = os.path.join(UV, s['id'] + '.ogg'); ff('-i', tmp, '-c:a', 'libvorbis', '-q:a', '6', out); os.remove(tmp)
        mb = os.path.getsize(out) / 1e6
        if mb > 2.0: raise SystemExit(f"{s['id']}: {mb:.2f} MB > 2 MB")
        rec = {k: v for k, v in s.items()}; rec.update(tep=f"reports/sfx-t3/ung-vien/{s['id']}.ogg", kenh=ch, dai_s=round(n / 48000, 2), chuan_db=round(gain, 2),
                                                    ha_vi_dinh_db=round(ha, 2), muc_sau_chuan='−23 LUFS (hoặc thấp hơn nếu bị trần đỉnh −1 dBFS)', mb=round(mb, 3), sha256_doan=lib.sha256(out))
        reg[s['id']] = rec; print(s['id'], rec['dai_s'], 's', rec['mb'], 'MB', 'gain', rec['chuan_db'], 'hạ đỉnh', ha, flush=True)
    json.dump(reg, open(reg_p, 'w'), ensure_ascii=False, indent=1)
main()
