#!/opt/cine/bin/python
"""ÂM THANH · mẫu giọng cho chủ dự án nghe (phiên Âm thanh, Mốc C, 15/10/2026). KHÔNG đổi giọng của T2.

  mau_giong.py <tệp_lời.txt> [--out /var/tmp/cine-out/am-thanh/mau-giong] [--dry]

Thu cùng một đoạn (móc 30 s của T2, lời v3.2 nguyên văn) bằng 3 cấu hình; cả 3 chuẩn về −16 LUFS (cùng độ to để so công bằng),
xuất mp3 192 kb/s NGOÀI git; in đường dẫn + SHA-256 + số ký tự gửi. Cache theo băm (cấu hình + chữ) → chạy lại không tốn ký tự.
"""
import hashlib, json, os, sys, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib

CFG = [dict(ten='A-eric-v2-hien-tai', id='cjVigY5qzO86Huf0OWal', model='eleven_multilingual_v2', ghi='Eric, eleven_multilingual_v2 — cấu hình T1/T2 hiện tại'),
       dict(ten='B-brian-v2', id='nPczCjzI2devNBz1zQrb', model='eleven_multilingual_v2', ghi='Brian (ElevenLabs: "Deep, Resonant and Comforting", Mỹ, trung niên, gợi ý cho narration) — đổi GIỌNG, giữ model'),
       dict(ten='C-eric-v4', id='cjVigY5qzO86Huf0OWal', model='eleven_v4', ghi='Eric, eleven_v4 — giữ giọng (liền mạch với T1), đổi MODEL')]
SET = dict(stability=0.5, similarity_boost=0.75, speed=1.0)


def main():
    if len(sys.argv) < 2: sys.exit(__doc__)
    text = open(sys.argv[1]).read().strip(); out = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else '/var/tmp/cine-out/am-thanh/mau-giong'
    os.makedirs(out, exist_ok=True); rows = []; sent = 0
    for c in CFG:
        key = hashlib.sha1(json.dumps([text, c['id'], c['model'], SET], sort_keys=True).encode()).hexdigest()[:10]; raw = os.path.join(out, f"{c['ten']}-{key}.raw.mp3")
        if not os.path.exists(raw):
            if '--dry' in sys.argv: print('sẽ gửi', len(text), 'ký tự', c['ten']); continue
            req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{c['id']}?output_format=mp3_44100_192", method='POST',
                                         data=json.dumps(dict(text=text, model_id=c['model'], voice_settings=SET)).encode(), headers={'Content-Type': 'application/json', 'Accept': 'audio/mpeg'})
            open(raw, 'wb').write(urllib.request.urlopen(req, timeout=300).read()); sent += len(text)
        if '--dry' in sys.argv: continue
        x = lib.dec(raw, 1); L = lib.integrated(x); fin = os.path.join(out, f"{c['ten']}.mp3")
        lib.write(fin, x * 10 ** ((-16.0 - L) / 20), 'libmp3lame', extra=('-b:a', '192k'))
        M = lib.ebur128(fin); rows.append(dict(cau_hinh=c['ten'], ghi=c['ghi'], voice_id=c['id'], model=c['model'], tep=fin, sha256=lib.sha256(fin), giay=round(len(x) / lib.SR, 2),
                                             I=M['I'], TP=M['TP'], LUFS_goc=round(L, 2)))
    if rows:
        json.dump(dict(loi=text, ky_tu_moi_ban=len(text), ky_tu_gui_lan_nay=sent, cai_dat=SET, ban=rows), open(os.path.join(out, 'mau-giong.json'), 'w'), ensure_ascii=False, indent=1)
        print(json.dumps(dict(ky_tu_gui_lan_nay=sent, ban=[{k: r[k] for k in ('cau_hinh', 'giay', 'I', 'sha256')} for r in rows]), ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
