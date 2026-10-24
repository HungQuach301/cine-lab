# P-2410b: ghi sổ 24/10/2026 — AUTHORSHIP, RIGHTS, COST-LEDGER (GIONG-T4, K-1.17.5), BAI-HOC-K2, QUYET-DINH-TREO.
# Chỉ NỐI CUỐI tệp (đọc/ghi newline=""), không sửa dòng cũ. Dòng COST-LEDGER P-2410b ghi riêng ở commit cuối (giờ máy đo thật).
import csv, io, re, glob, os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

def noi(p, text):
    s = open(p, encoding='utf-8', newline='').read()
    if not s.endswith('\n'): s += '\n'
    open(p, 'w', encoding='utf-8', newline='').write(s + text)

# ---------- AUTHORSHIP ----------
A = []
A.append('| 2026-10-24 | Kênh 2 T4 London — bổ sung giờ cho dòng "V1–V7 + K1174-D1…D6" (06:42; P-2410b ghi) | '
 'Theo lệnh P-2410b: tin nhắn "Duyệt V1–V7 và K1174-D1…D6 theo khuyến nghị" gửi lúc **24/10/2026 06:42** (Asia/Saigon). '
 'Dòng P-2410 ghi "giờ chính xác không có trong lệnh" giữ nguyên, không sửa; dòng này bổ sung giờ. Nội dung quyết định như dòng P-2410 | '
 '— (bổ sung hồ sơ) | — | Chủ dự án |')
A.append('| 2026-10-23 | Kênh 2 T4 London — Q1–Q7 trước animatic, nội dung đủ (21:45; P-2410b ghi bổ sung vì dòng P-2410 thiếu Q3–Q6) | '
 'Nguyên văn: "Duyệt Q1–Q7". Nội dung (theo lệnh P-2410b): **Q1** mức minh hoạ Omni T4 = 20–23 % (ngân sách Gemini lúc đó mốc $25, chặn $30; nay chặn $35 / mốc $30 theo 23:45); '
 '**Q2** bỏ trần cứng 20 % minh hoạ M-d → ngân sách Gemini mỗi tập + tổng khung AI ≤ 70 % + góc cao timelapse ≥ 60 %; '
 '**Q3** áp 8 điểm tiết kiệm Omni: (1) sinh đúng độ dài, (2) ảnh đầu hoàn thiện, (3) ảnh đầu + ảnh cuối, (4) thư viện lệnh / danh sách cấm, (5) trần 3 lượt + sổ giây, (6) nháp độ phân giải thấp, (7) kiểm 2 tầng — Gemini Flash trước, (8) sinh 720p rồi phóng 1080p tại chỗ; '
 '**Q4** lượt đo $2–3 đầu animatic rồi chốt số khoảnh khắc; **Q5** GPU quyết sau tờ chọn look, khuyến nghị bỏ GPU nếu đêm cách A đạt (sau đó L5 23:27 = bỏ GPU); '
 '**Q6** chủ dự án nạp Gemini trước animatic; **Q7** phiên K-1.17.4 chạy song song. Dòng P-2410 (chỉ Q1, Q2, Q7) giữ nguyên | '
 'Chủ dự án đặt mức minh hoạ AI, cách tiết kiệm và trình tự chốt chi phí trước animatic; tự nạp tài khoản Gemini | Điều phối: đề xuất Q1–Q7 | Chủ dự án |')
A.append('| 2026-10-24 | Kênh 2 T4 London — lời khoá v2 + PHIẾU GIỌNG G-1…G-3 (08:31; P-2410b ghi) | '
 'Nguyên văn: "Duyệt G-1, G-2, G-3 theo khuyến nghị". **G-1 = (c) K1-C1, phim 730,1 s** (+1,4 % so 720 s): bỏ 7 câu nguyên trong dựng, cắt trên bản thu, 0 ký tự — L81 (tầm nhìn LVMF), L41 nửa sau (4 hạng nhà), L45 (thợ đo cắm mốc), L38 (bản in phương án Wren), L77 (614 500 người làm việc), L15 (câu thứ hai của Bludworth), L54 (câu khái quát); rút shot nối/lặng; thẻ Hooke dời sang H2-02 (`reports/giong-t4/GIAN-SHOT.md`). '
 '**G-2 = (a)** duyệt như bản khoá: các vế bỏ/làm mềm ở L53, L54, L61, L63, L71, L76, L77 (`reports/giong-t4/KIEM-LOI.md`). '
 '**G-3:** St Saviour\'s giữ bản thu gốc; Wenceslaus giữ cách G1 đọc; alias Evelyn "Eevlin" duyệt. '
 'Lời khoá v2 `channel-k2/k2c-t4-02/loi-khoa.txt` `645c0211…` (D3 giữ "burned to the ground twice"; 22 mục [cần kiểm]: 7 giữ, 12 sửa chữ, 2 bỏ vế, 1 viết lại an toàn) | '
 'Chủ dự án chọn độ dài phim và 7 câu bỏ, chấp nhận các vế bỏ/làm mềm, quyết cách đọc tên riêng (St Saviour\'s, Wenceslaus, Evelyn) | GIONG-T4: kiểm 22 mục với nguồn, đề xuất câu, thu G1, ASR + âm vị, phiếu G-1…G-3 | Chủ dự án |')
A.append('| 2026-10-24 | Kênh 2 T4 London — K1175-D1…D7 (tin nhắn ngay trước lệnh P-2410b; giờ chính xác không có trong lệnh; P-2410b ghi) | '
 'Nguyên văn: "Duyệt K1175-D1…D7 theo khuyến nghị và lưu master giọng T4 vào LFS". '
 '**D1** = A: phản chiếu chỉ lấy từ render 3D; lệnh AI không vẽ phản chiếu · **D2** = A: T9c thay T9b chiều nước→đất · '
 '**D3** = A: khớp màu cục bộ vòng bảo vệ, một độ lệch/vật, K kiểm (d) · **D4** = A: lớp sống ghép cộng hiệu, khai `song` · '
 '**D5** = A + D: phủ bề mặt nhà chỉ ở nhà ĐO ĐƯỢC (≥ 2 px/m và ≥ 40 điểm cạnh — chủ yếu khung trung/cận); toàn cảnh xa giữ render và nâng bằng 3D · '
 '**D6** = A: mặt nạ ID + tấm ghép + JSON kiểm của mọi tấm N2+/BMN vào git, nén ≤ 5 MB · **D7** = A: lời nhắc BMN v2 có năm bắt buộc + q_thoi_dai. '
 'Văn bản: Kinh thánh §13.6, §15 (a)(b)(c)(d)(j) (`0ab7a06b…`); PLAN.md quy ước D6; bộ kiểm 1.17.5 `c7630b4a…` vào main | '
 'Chủ dự án quyết cách dùng AI trên tấm nền và bề mặt nhà: chỉ phản chiếu thật, phủ bề mặt chỉ nhà đo được, toàn cảnh nâng bằng 3D | K-1.17.5: phiếu K1175-D1…D7 | Chủ dự án |')
A.append('| 2026-10-24 | Kênh 2 T4 London — lưu master giọng T4 vào LFS (cùng tin nhắn K1175; P-2410b ghi) | '
 'Nguyên văn: "… và lưu master giọng T4 vào LFS". Mẫu `channel-k2/k2c-t4-02/am-thanh/master/*.wav` và `*.flac` thêm vào `tools/lfs-allow.txt` + `.gitattributes`; '
 'master tái tạo bit-trùng bằng `scripts/k2ldn/giong/tai_tao.sh` (0 ký tự ElevenLabs): `T4-loi-G1-v2-14LUFS.wav` `b9cec46777a0…` (98 029 582 byte), `T4-loi-G1-v2-14LUFS.flac` `e5d49871807…` (59 258 364 byte); `git lfs push` 2/2 | '
 'Chủ dự án duyệt dùng hạn mức LFS cho master giọng T4 | GIONG-T4 §9 đề xuất mẫu LFS | Chủ dự án |')
noi('AUTHORSHIP.md', '\n'.join(A) + '\n')

# ---------- RIGHTS ----------
TEN = {
 'aim25-london-bridge': ('London Metropolitan Archives / AIM25 — London Bridge (Bridge House Estates)', 'LMA (AIM25)'),
 'bbc-stpauls-2010': ('BBC News Magazine (2010) — St Paul\'s trong Blitz 29/12/1940', 'BBC'),
 'brewers-hall-1940': ('Brewers\' Company — The destruction of Brewers\' Hall (1940)', 'Brewers\' Company'),
 'city-great-fire-walk': ('City of London — Great Fire walk (PDF)', 'City of London Corporation'),
 'city-kaoc-cluster': ('City of London — Draft Local Plan, KAOC land use, City Cluster (PDF)', 'City of London Corporation'),
 'city-key-facts': ('City of London — Our impact and key facts', 'City of London Corporation'),
 'city-who-we-are': ('City of London — Who we are', 'City of London Corporation'),
 'fig-cooper-2000': ('M. Cooper, bài FIG Working Week Prague 2000 (đo đạc London sau 1666)', 'M. Cooper (FIG)'),
 'gac-stpauls-watch': ('St Paul\'s Cathedral trên Google Arts & Culture — St Paul\'s Watch', 'St Paul\'s Cathedral'),
 'guildhall-many-lives': ('City of London — The many lives of Guildhall', 'City of London Corporation'),
 'innertemple-greatfire2016': ('Inner Temple Library — Great Fire 2016 (PDF)', 'Inner Temple Library'),
 'lm-blitz-letter': ('London Museum — New Year\'s Eve letter, Blitz London', 'London Museum'),
 'lm-great-fire': ('London Museum — Great Fire of London (London stories)', 'London Museum'),
 'loc-phoenix-2025': ('Library of Congress, blog Maps (12/2025) — Phoenix rising: urban planning after the Great Fire', 'Library of Congress'),
 'oxford-archer': ('University of Oxford, Faculty of History (I. Archer) — Facing catastrophe: the Great Fire of London', 'I. Archer (Oxford)'),
 'rmg-hooke': ('Royal Museums Greenwich — Robert Hooke rebuilding London after the Great Fire', 'Royal Museums Greenwich'),
 'royal-exchange-heritage': ('The Royal Exchange — Heritage', 'The Royal Exchange'),
 'spd-2012': ('City of London — Protected Views SPD (2012) (PDF)', 'City of London Corporation'),
 'stpauls-timeline': ('St Paul\'s Cathedral — Our timeline', 'St Paul\'s Cathedral'),
 'vm-plans-1666': ('Vetusta Monumenta (Univ. of Missouri) — vol. 2, plates 1–2: plans of London after 1666', 'Vetusta Monumenta / Univ. of Missouri'),
}
R = ['', '## T4 London — giọng (GIONG-T4) + bộ kiểm K-1.17.5 (P-2410b ghi 24/10/2026)', '',
 '### Nguồn dữ kiện kiểm lời (KIEM-LOI, 22 nguồn: 20 trang tải về + 2 văn bản đã có trong repo) — **chỉ dữ kiện, không chép văn bản vào phim**',
 'Bản chữ đã che email: `reports/giong-t4/nguon/<mã>.txt` (dòng đầu: URL, giờ đọc UTC, SHA-256 tệp gốc, cỡ); gốc HTML/PDF ngoài git, tái tạo bằng `scripts/k2ldn/giong/tai_nguon.py` (trang có thể đổi → so SHA). Trích dẫn trong `reports/giong-t4/KIEM-LOI.md` chỉ để kiểm, không vào phim.',
 '| Mã | Tài sản | Loại | Nguồn/URL | Tác giả | Giấy phép (trích nguyên câu + link) | Được dùng: YouTube / bán phim / LHP | Ghi công | SHA-256 | Ngày thêm |',
 '|---|---|---|---|---|---|---|---|---|---|']
for f in sorted(glob.glob('reports/giong-t4/nguon/*.txt')):
    ma = os.path.basename(f)[:-4]
    l1, l2 = open(f, encoding='utf-8').read().split('\n')[:2]
    url = l1.lstrip('# ').strip()
    m = re.search(r'đọc (\S+ \S+) UTC · SHA-256 gốc ([0-9a-f]{64})', l2); assert m, f
    ten, tg = TEN[ma]
    R.append(f'| T4-GL-{ma} | {ten} — dữ kiện kiểm lời T4 (đọc {m.group(1)} UTC) | Văn bản (dữ kiện) | {url} ; bản chữ `{f}` | {tg} | '
             'Bản quyền của nơi đăng (không giấy phép mở). Chỉ dùng **dữ kiện** (năm, số, sự kiện — không được bảo hộ); không chép câu chữ, không dùng hình của trang | '
             'Dữ kiện: Có / Có / Có; văn bản/hình: Không | danh sách nguồn trong mô tả YouTube (§15 (e)) | ' + m.group(2) + ' (tệp gốc) | 2026-10-24 |')
R += ['| T4-GL-PEPYS | Nhật ký Pepys 1666 — bậc 2; câu trích nguyên văn "a little ale-house on the Bankside" và "I am spent" trong lời | Văn bản (PD) | như **N2P-T4-1** (Gutenberg #4167) | Samuel Pepys | Phạm vi công cộng (như N2P-T4-1) | Có / Có / Có | như N2P-T4-1 | như N2P-T4-1 | 2026-10-24 |',
      '| T4-GL-EVELYN | Nhật ký Evelyn 1666 — bậc 2 (Wren trình Vua 11/9, Evelyn 13/9) | Văn bản (PD) | như **N2P-T4-2** (Gutenberg #42081) | John Evelyn | Phạm vi công cộng (như N2P-T4-2) | Có / Có / Có | như N2P-T4-2 | như N2P-T4-2 | 2026-10-24 |',
      '',
      '- **Giọng lời T4:** giọng G1 theo dòng **P1910-G1** — quyền **vẫn chờ thư Đ5** (ElevenLabs chưa trả lời): dùng cho animatic/nội bộ, **chưa dùng cho bản phát hành**. Bản thu: 13 mp3 gốc + alignment `channel-k2/k2c-t4-02/am-thanh/nguon/` (SHA256SUMS); master LFS `channel-k2/k2c-t4-02/am-thanh/master/T4-loi-G1-v2-14LUFS.wav` `b9cec46777a0…`, `.flac` `e5d49871807…`; sổ AI `reports/giong-t4/so-ai.jsonl` (13 lệnh). Không giọng mới.',
      '- **Mô hình âm vị** `facebook/wav2vec2-lv-60-espeak-cv-ft` (Hugging Face) và ASR faster-whisper: chỉ dùng để đo phát âm, không tạo nội dung phim.',
      '- **K-1.17.5 — 2 ảnh AI** `reports/k1175/ai/BMN-P1-l1-ai.jpg` (`7998435a6dc1…`), `BMN-TRUNG-l1-ai.jpg` (`948b57310e74…`): OpenAI `gpt-image-2.5-sunburst-2026-09-08` /v1/images/edits, đầu vào là render Blender của K (không tài sản ngoài); sổ `reports/k1175/so-ai.jsonl`. **Chỉ là khung đáp án kiểm, không vào phim** — không ghi dòng tài sản.',
      '- Không nhạc/SFX/font mới; không tài sản NC/ND.']
noi('RIGHTS.md', '\n'.join(R) + '\n')

# ---------- COST-LEDGER ----------
hdr = next(csv.reader(open('COST-LEDGER.csv', encoding='utf-8', newline='')))
g = next(csv.reader(io.StringIO('GIONG-T4,"K2C-T4-02 M2: khoá lời v2 (22 mục [cần kiểm]), phát âm, thu G1 cả tập, ASR, master, giãn shot",xưởng,2026-10-24,,,,,0,2,không gọi API,11362,4998,1.2,,0,680.76,,reports/giong-t4/GIONG-T4-BAO-CAO.md §8,"ElevenLabs 11 362 gửi / bộ đếm +4 998 (0,440); Claude API $0; OpenAI/Gemini/RunPod/YouTube 0"')))
assert len(g) == len(hdr) == 20, (len(g), len(hdr))
g[18] += ' (nhánh claude/k2c-t4-02-giong-a24udn @5e5e02ce); sổ AI reports/giong-t4/so-ai.jsonl'
g[19] += '; giờ máy ≈ 1,2 h (mốc 3 h); dòng theo đề xuất GIONG-T4 §9; chủ dự án duyệt G-1…G-3 24/10 08:31; ghi sổ bởi P-2410b'
k = ['K-1.17.5', 'Luật 1.17.5: N2P-3 nước→đất = T9c, N2P-1 (e) lớp sống, (d) vòng khớp màu cục bộ, BE-MAT-NHA (phủ bề mặt nhà); LOCK 1.17.4 08486eb2 → 1.17.5 c7630b4a',
     'K', '2026-10-24', '', '', '', '', '0.497', '3',
     'claude-sonnet-5-5 (nhìn, O2); gpt-6.1-sol (nhìn); gpt-image-2.5-sunburst-2026-09-08 (edits)', '0', '0', '2.9', '', '1', '', '',
     'reports/k1175/K1175-BAO-CAO.md §11, §13 (nhánh checks-1-17-5 @1dc8be60); sổ AI reports/k1175/so-ai.jsonl',
     'OpenAI $0,343 = 2 ảnh edits $0,151 + nhìn gpt-6.1-sol $0,192 (mốc $2); Claude API $0,497 = nhìn claude-sonnet-5-5 $0,259 + q_thoi_dai (O2) $0,239 (mốc $3); Gemini/ElevenLabs/RunPod/YouTube 0; tổng ≈ $0,84; giờ máy ≈ 2,9 h (mốc 5 h); tải LFS master T3 1,79 GB; selftest k1175 52/52; chủ dự án duyệt K1175-D1…D7 24/10; ghi sổ bởi P-2410b']
assert len(k) == 20
b = io.StringIO(); w = csv.writer(b, lineterminator='\n'); w.writerow(g); w.writerow(k)
noi('COST-LEDGER.csv', b.getvalue())

# ---------- BAI-HOC-K2 ----------
B = ['', '## K51–K58 · Giọng T4 và bộ kiểm 1.17.5 (P-2410b ghi 24/10/2026)',
 '| # | Bài học | Số đo | Nguyên nhân | Luật hiện hành |', '|---|---|---|---|---|',
 '| K51 | Giọng TTS có thể rút gọn câu trích nguyên văn | GIONG-T4 §4: G1 đọc "I am spent" (Pepys) thành "I\'m spent" — ASR 2 cách và âm vị cùng bắt; thu lại 1 câu (11 ký tự), khớp mức +3,42 dB | TTS chuẩn hoá theo văn nói | **Kiểm cấp từ mọi câu trích nguyên văn** (ASR 2 cách + âm vị), không chỉ mục tên/số; sai thì thu lại riêng câu đó (GIONG-T4 §9 (a)) |',
 '| K52 | Nhận dạng âm vị là "tai thứ hai" tốt cho tên riêng | GIONG-T4 §3: 48 tên × 3 lượt; ASR viết đúng chính tả "Evelyn" dù G1 đọc 3 âm tiết → âm vị bắt, alias "Eevlin"; St Saviour\'s âm vị đúng dù ASR viết "Xavier\'s" (không thu lại oan) | ASR chữ tự sửa về chính tả và thiên về từ phổ biến | **Tên riêng: nghe bằng ASR + mô hình âm vị** (`facebook/wav2vec2-lv-60-espeak-cv-ft`, venv riêng, chỉ đo); lỗi chỉ ở ASR thì không thu lại (GIONG-T4 §9 (b)) |',
 '| K53 | Độ dài lời phải tính cả ngừng giữa đoạn và shot không lời | GIONG-T4 §2, G-1: lời theo shot 632,8 s (87,9 % của 720 s) nhưng bảng v1 có 138 s shot không lời → phim ≥ 782 s (+8,6 %); chủ dự án chọn K1-C1 730,1 s (bỏ 7 câu) | ước độ dài chỉ theo số từ lời | **Khi đặt số từ lời: thời lượng = lời + ngừng giữa đoạn + shot không lời + lặng có chủ ý**; kiểm trên bảng shot trước khi khoá lời (GIONG-T4 §9 (c)) |',
 '| K54 | **"pkill -f khớp chính shell" — lặp lần 3** | K-1.17.5 §13 (1) (lặp lần 3 theo K-1.17.5: LL #24/#41, K-1.17.4); cùng ngày GIONG-T4 sự cố 2 cũng gặp; trước đó LL #112, K46 | chuỗi tìm nằm trong dòng lệnh của chính shell gọi | **Chỉ dừng theo PGID ghi ra tệp khi khởi chạy; cấm `pkill -f` / `pgrep -f` theo chuỗi.** Đã lặp ≥ 3 lần dù có luật chữ → đề xuất chặn bằng công cụ (phiên Nền tảng), xem P2410B-BAO-CAO §8 |',
 '| K55 | Cất `checks/` bằng stash khi selftest đang chạy nền có thể làm hỏng lượt đó | K-1.17.5 §13 (2); lặp K47 | module nạp lười đọc tệp giữa lượt chạy | **Đẩy WIP khi không có lượt chạy, hoặc chạy từ worktree/bản sao riêng** (K47) |',
 '| K56 | Mặt nạ / tấm ghép để ở `/var/tmp` làm phiên K không tái hiện được số kiểm | K-1.17.5 §1: look2 24 tấm — không tái hiện số `tam-nen.json`; lặp kiểu LL #109, #117, K49 | tệp kiểm sống cùng container | **PLAN.md quy ước D6** (K1175-D6 = A): mặt nạ ID + tấm ghép + JSON kiểm của mọi tấm N2+/BMN vào git ≤ 5 MB nén |',
 '| K57 | Mặt nạ phải đúng độ phân giải khung | K-1.17.5 §2: mặt nạ thu 960×540 rồi phóng lệch bờ 1 px → ca âm Blender ô-liu trượt | thu/phóng mặt nạ làm lệch biên | **`mat_na` đúng độ phân giải khung, không thu/phóng** (Kinh thánh §13.6) |',
 '| K58 | Blender `world_to_camera_view` trả toạ độ cũ nếu chưa cập nhật cảnh | K-1.17.5 §13 (5) | ma trận máy chưa tính lại sau khi đặt máy | **Gọi `bpy.context.view_layer.update()` sau mỗi lần đặt/đổi máy, trước khi chiếu điểm** |']
noi('channel-k2/BAI-HOC-K2.md', '\n'.join(B) + '\n')

# ---------- QUYET-DINH-TREO ----------
Q = ['', '## E. Cập nhật 24/10/2026 sau K-1.17.5 và GIONG-T4 (P-2410b ghi)', '',
 '**Đã quyết** (nguyên văn + giờ ở `AUTHORSHIP.md`; văn bản ở Kinh thánh `docs/BIBLE-KENH2.md` `0ab7a06b…`):', '',
 '| # | Quyết định | Khi nào | Áp ở |', '|---|---|---|---|',
 '| G-1 | (c) K1-C1 — phim 730,1 s; bỏ 7 câu trong dựng (0 ký tự), rút shot nối/lặng | 24/10 08:31 ("Duyệt G-1, G-2, G-3 theo khuyến nghị") | animatic T4 (`reports/giong-t4/GIAN-SHOT.md`) |',
 '| G-2 | (a) duyệt các vế bỏ/làm mềm như bản khoá | 24/10 08:31 | lời khoá v2 `loi-khoa.txt` |',
 '| G-3 | St Saviour\'s giữ bản gốc; Wenceslaus giữ; alias Evelyn "Eevlin" | 24/10 08:31 | master giọng T4 (không thu lại) |',
 '| K1175-D1 (K1175-a) | A — phản chiếu chỉ từ render 3D; lệnh AI không vẽ phản chiếu | 24/10 ("Duyệt K1175-D1…D7 theo khuyến nghị …") | Kinh thánh §15 (b) |',
 '| K1175-D2 (K1175-b) | A — T9c thay T9b chiều nước→đất | 24/10 | Kinh thánh §15 (c) (iii); RULES-LL 1.17.5 |',
 '| K1175-D3 (K1175-d) | A — khớp màu cục bộ vòng bảo vệ, một độ lệch/vật, K kiểm (d) | 24/10 | Kinh thánh §15 (a) |',
 '| K1175-D4 (K1175-c) | A — lớp sống cộng hiệu, khai `song` | 24/10 | Kinh thánh §15 (b), §13.6 |',
 '| K1175-D5 (K1175-e) | A + D — phủ bề mặt nhà chỉ ở nhà đo được (≥ 2 px/m, ≥ 40 điểm cạnh); toàn cảnh xa giữ render, nâng bằng 3D | 24/10 | Kinh thánh §15 (j) (vẫn ĐANG THỬ) |',
 '| K1175-D6 | A — mặt nạ ID + tấm ghép + JSON kiểm vào git ≤ 5 MB nén | 24/10 | PLAN.md quy ước D6 |',
 '| K1175-D7 | A — lời nhắc BMN v2 năm bắt buộc + q_thoi_dai | 24/10 | Kinh thánh §15 (j) |',
 '| LFS | lưu master giọng T4 vào LFS | 24/10 (cùng tin nhắn) | `tools/lfs-allow.txt`, `.gitattributes`; master `b9cec467…` / `e5d49871…` |',
 '| (giờ) | tin "Duyệt V1–V7 và K1174-D1…D6" lúc 24/10 06:42 | lệnh P-2410b | AUTHORSHIP dòng bổ sung |', '',
 '**Còn treo:**', '',
 '| # | Nội dung | Căn cứ | Chặn gì |', '|---|---|---|---|',
 '| THU-B-T4 | Vòng thử phương án B (phủ bề mặt nhà) qua BE-MAT-NHA + cổng (c), rồi chủ dự án duyệt — điều kiện (2)(3) của Kinh thánh §15 (j) | K1175-D5 = A + D | áp B ở bản cuối T4 |',
 '| LOOK-T9c | Phiên LOOK đo lại 24 tấm look2 bằng T9c (mặt nạ của họ; lưu mặt nạ + tấm ghép theo D6); đo lại M1-rong-oai-l3h với khớp màu cục bộ | K1175 §12 D2, D3; §14 mục 3 | dùng lại tấm look2 / M4-rong |',
 '| BIEN-CO-V | Hiệu chuẩn lại BIEN-CO-V trên animatic T4 (log máy thật) | K1174-D2 | G2 T4 |',
 '| V1-1666 | Mở tấm nền cho cảnh 1666 ban ngày sau khi luật đo đã có (V1 hiện giữ: chỉ 2026 ban ngày) | Kinh thánh §15 (d) cập nhật 24/10 | tấm nền 1666 |',
 '| Đ5 | Quyền giọng G1 cho bản phát hành (chờ thư ElevenLabs) | RIGHTS P1910-G1 | phát hành T4 |']
noi('reports/k1173/QUYET-DINH-TREO.md', '\n'.join(Q) + '\n')
print('xong')
