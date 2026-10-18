"""NC-AI · WER chép trang so đáp án tay. Chuẩn hoá 'nới': chữ thường, nối gạch nối cuối dòng, bỏ dấu câu, ſ→s VÀ f→s (OCR cũ đọc ſ thành f).
'Chặt': chỉ chữ thường + bỏ dấu câu (ſ phải giữ là ſ). Cửa sổ giả thuyết = đoạn giữa từ khớp đầu và cuối với đáp án (bỏ phần trang ngoài đáp án).
Dùng: python3 -I ai1_wer.py <dap_an> <gia_thuyet>..."""
import sys, re, difflib, json
def toks(s, loose):
    s = re.sub(r'-\s*\n\s*', '', s).lower(); s = re.sub(r"[^\wſ ]+", ' ', s)
    if loose: s = s.replace('ſ', 's').replace('f', 's')
    return s.split()
def ed(a, b):
    d = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        p, d[0] = d[0], i
        for j, y in enumerate(b, 1): p, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, p + (x != y))
    return d[-1]
gt = open(sys.argv[1]).read(); out = {}
for h in sys.argv[2:]:
    hy = open(h).read(); r = {}
    for loose in (True, False):
        G, H = toks(gt, loose), toks(hy, loose)
        m = [b for b in difflib.SequenceMatcher(None, G, H, autojunk=False).get_matching_blocks() if b.size]
        Hw = H[m[0].b: m[-1].b + m[-1].size] if m else H
        r['wer_noi' if loose else 'wer_chat'] = round(ed(G, Hw) / len(G), 3)
    r['so_tu_dap_an'] = len(toks(gt, True)); out[h] = r
print(json.dumps(out, ensure_ascii=False, indent=1))
