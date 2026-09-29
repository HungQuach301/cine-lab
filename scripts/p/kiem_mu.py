"""Phiên P — KIỂM MÙ bằng subagent (cách làm Cổng 5–6; cách chấm hiện hành: AUTHORSHIP "Cổng 6 — nhân vật", 29/09/2026).

QUY TRÌNH
 1. doi-chung <thư mục>: trích 2 khung đối chứng Sprite Fright (REF-SF-HC, CC BY 4.0, CHỈ hiệu chuẩn nội bộ, KHÔNG commit khung):
      mốc 104,5 s (Ellie, ngày) và 332 s (Victoria, đêm) → sf_104.5.png, sf_332.png (1920×804).
      Video: /var/tmp/hieuchuan/sprite-fright-804p.mp4; thiếu thì tải từ archive.org (RIGHTS.md REF-SF), kiểm SHA-256.
 2. chuan-bi <thư mục vòng> <nhãn>=<ảnh> ...: chép mỗi ảnh sang tên ngẫu nhiên 8 hex (giữ đuôi), ghi map.tsv (nhãn<TAB>tên mù),
      in câu lệnh giao cho từng subagent. Nhãn bắt đầu "doichung" = khung đối chứng.
      Nhãn có "hai-nguoi" dùng câu hỏi nhiều người; còn lại câu hỏi một người.
 3. Giao MỖI ảnh cho MỘT subagent MỚI (Agent, general-purpose, chạy nền), prompt NGUYÊN VĂN do bước 2 in ra. Không gợi ý gì thêm.
 4. nguyen-van <thư mục vòng> <ra.md> <tasks_dir> <agentId>=<tên mù> ...: lấy nguyên văn (lời SubagentHandback) từ
      <tasks_dir>/<agentId>.output của harness (vd. /tmp/claude-0/<dự án>/<phiên>/tasks). Đường dẫn tạm trong lời đáp nên rút về tên file.
 5. dem <nguyenvan.md>: đếm từ khoá bằng MÁY (không đếm tay), in từng câu trúng để người chấm xếp cột.
 6. Chấm (tay, theo AUTHORSHIP):
      - Mỗi câu trúng xếp cột HÌNH (mặt, đầu, thân, quần, áo, tay, vật liệu) hoặc TƯ THẾ (dáng, cứng đơ, như tượng).
        Câu nói cả hai → HÌNH. Chỉ tính câu chỉ vào NHÂN VẬT của ta (không tính đạo cụ, cảnh).
      - ĐẠT khi tỉ lệ khung có từ khoá cột HÌNH ≤ nhiễu nền đối chứng (2/20 = 10 % tới 29/09/2026) VÀ không có lời chê cùng
        một chỗ lặp ≥ 2 khung. Lời chê trúng chỗ thật vẫn phải sửa. Mỗi lần kiểm ≥ 6 khung (P đề xuất 10) + 2 đối chứng.
      - Cập nhật nhiễu nền: cộng số lượt đối chứng có từ khoá chỉ vào nhân vật / tổng lượt đối chứng.
"""
import hashlib, json, os, re, secrets, shutil, subprocess, sys, urllib.request

HOI_1 = "Trả lời bằng tiếng Việt, như một người xem bình thường: Người này bao nhiêu tuổi, giới tính gì, đang cảm thấy gì? Nêu thêm điều gì người xem có thể thấy lạ trong ảnh (nếu có)."
HOI_N = "Trả lời bằng tiếng Việt, như một người xem bình thường: Những người trong ảnh bao nhiêu tuổi, giới tính gì, đang cảm thấy gì? Nêu thêm điều gì người xem có thể thấy lạ trong ảnh (nếu có)."
MO = "Mở và xem đúng một file ảnh: {p} (dùng công cụ Read). Không mở, không tìm hay đọc bất kỳ file nào khác.\n\n"
TU_KHOA = r'búp bê|mặt nạ|con rối|ma-?nơ-?canh|ma nơ canh|tượng sáp|đồ chơi|lệch phong cách|không ăn nhập|khác phong cách|hai phong cách'
SF = '/var/tmp/hieuchuan/sprite-fright-804p.mp4'
SF_URL = 'https://archive.org/download/sprite-fright/Sprite%20Fright%20-%20Open%20Movie%20by%20Blender%20Studio-804p.mp4'
SF_SHA = '85af52d5f82976256d5f091aea4cf276a3d8599d14d36bae5d51e43a9acfd076'

def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()

def doi_chung(out):
    os.makedirs(out, exist_ok=True)
    if not os.path.exists(SF):
        os.makedirs(os.path.dirname(SF), exist_ok=True); urllib.request.urlretrieve(SF_URL, SF)
    if sha(SF) != SF_SHA: raise SystemExit('SHA video Sprite Fright không khớp RIGHTS.md REF-SF')
    for t in ('104.5', '332'):
        subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-ss', t, '-i', SF, '-frames:v', '1', f'{out}/sf_{t}.png'], check=True)
    print('đối chứng:', out + '/sf_104.5.png', out + '/sf_332.png')

def chuan_bi(rd, items):
    os.makedirs(rd, exist_ok=True); rd = os.path.abspath(rd)
    with open(rd + '/map.tsv', 'w') as m:
        for it in items:
            lab, src = it.split('=', 1); name = secrets.token_hex(4) + os.path.splitext(src)[1]
            shutil.copy(src, f'{rd}/{name}'); m.write(f'{lab}\t{name}\n')
            print(f'--- {lab} → {name}\n' + MO.format(p=f'{rd}/{name}') + (HOI_N if 'hai-nguoi' in lab else HOI_1) + '\n')

def nguyen_van(rd, out, tasks, pairs):
    mp = dict(l.rstrip('\n').split('\t')[::-1] for l in open(rd + '/map.tsv'))
    L = []
    for a in pairs:
        i, f = a.split('='); txt = None
        for line in open(os.path.join(tasks, i + '.output')):
            try: d = json.loads(line)
            except Exception: continue
            if d.get('type') == 'assistant':
                for c in d['message'].get('content', []):
                    if c.get('type') == 'tool_use' and 'andback' in c.get('name', ''): txt = c['input'].get('message')
        txt = (txt or '(không lấy được)').replace(os.path.abspath(rd) + '/', '')
        L.append(f"### {mp[f]} — file mù `{f}` — nguyên văn\n"); L.append('\n'.join('> ' + x if x else '>' for x in txt.strip().split('\n')) + '\n')
    open(out, 'w').write('\n'.join(L)); print('ghi', out)

def dem(md):
    t = open(md).read(); n = 0
    for s in re.split(r'^### ', t, flags=re.M)[1:]:
        name = s.split(' — ')[0]
        for line in s.split('\n'):
            for m in re.finditer(TU_KHOA, line, flags=re.I): n += 1; print(name, '|', m.group(0), '|', line.strip()[:300])
    print('tổng lượt trúng:', n)

if __name__ == '__main__':
    c = sys.argv[1] if len(sys.argv) > 1 else ''
    if c == 'doi-chung': doi_chung(sys.argv[2])
    elif c == 'chuan-bi': chuan_bi(sys.argv[2], sys.argv[3:])
    elif c == 'nguyen-van': nguyen_van(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5:])
    elif c == 'dem': dem(sys.argv[2])
    else: print(__doc__)
