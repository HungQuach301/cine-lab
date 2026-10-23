import json, sys
A = {r['q']: r for r in json.load(open(sys.argv[1]))['rows']}; B = {r['q']: r for r in json.load(open(sys.argv[2]))['rows']}
print('| Hàng | 1.17.2 | 1.17.3 | Lỗi 1.17.2 → 1.17.3 | Ghi |'); print('|---|---|---|---|---|')
for q in A:
    a, b = A[q], B.get(q, {})
    same = a['kq'] == b.get('kq') and len(a['loi']) == len(b.get('loi', [])) and a['val'] == b.get('val')
    if not same or '-v' in sys.argv:
        print(f"| {q} | {a['kq']} | {b.get('kq')} | {len(a['loi'])} → {len(b.get('loi', []))} | {'' if a['val'] == b.get('val') else 'giá trị đổi'} |")
print('hàng giống hệt:', sum(1 for q in A if A[q]['kq'] == B.get(q, {}).get('kq') and A[q]['val'] == B.get(q, {}).get('val') and len(A[q]['loi']) == len(B.get(q, {}).get('loi', []))), '/', len(A))
