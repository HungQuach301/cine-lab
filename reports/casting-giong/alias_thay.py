#!/opt/cine/bin/python
"""CASTING-GIỌNG · thử alias thay thế cho các mục SAI ở mọi giọng (lỗi alias chung, không phải lỗi giọng).
Giả thuyết: âm tiết VIẾT HOA trong alias ("EL-ee-ut", "LEE-neh-ah", "TEH") bị vài giọng đọc thành chữ cái/viết tắt;
"fayt" bị đọc thành "fight". Alias thay: chữ thường, chính tả tiếng Anh quen. KHÔNG sửa từ điển khoá (channel-k2/) — chỉ đề xuất.
alias_thay.py <ma> … → $CG_OUT/alias-<ma>.json"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import cg_lib as L, kiem_lib as K
THAY = [('Eliott', 'Elliot'), ('fait accompli', 'fet ah-kom-plee'), ('Cádiz', 'kah-deeth'), ('Montero', 'mon-tair-oh'),
        ('La Línea', 'la lee-nay-ah'), ("d'Arçon", 'dar-sohn'), ('Algeciras', 'al-heh-see-rahs')]
CHU = 'General Elliot held the Rock. It was a fet ah-kom-plee. A port called kah-deeth. The historian mon-tair-oh. The town of la lee-nay-ah. The engineer dar-sohn. The bay of al-heh-see-rahs.'
for ma in sys.argv[1:]:
    vid = json.load(open(f'{L.OUT}/{ma}.json'))['voice_id']; p, n = L.tts(vid, CHU, tag=f'{ma}:alias-thay'); R = dict(ma=ma, chu=CHU, ky_tu=n, nghe={})
    for name, beam in K.NGHE:
        txt, _ = K.transcribe(p, name, beam); R['nghe'][name] = dict(asr=txt, dung=[g for g, a in THAY if K.name_ok(g, txt, a) >= 0.75])
    R['dung'] = sorted(set(R['nghe']['medium.en']['dung']) | set(R['nghe']['small.en']['dung']))
    json.dump(R, open(f'{L.OUT}/alias-{ma}.json', 'w'), ensure_ascii=False, indent=1); print(ma, len(R['dung']), '/', len(THAY), R['nghe']['medium.en']['asr'], flush=True)
