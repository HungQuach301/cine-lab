#!/usr/bin/env python3
"""P-2110 · COST-LEDGER +3 dòng (ANIMATIC-T3, NC-N2P, P-2110); số lấy từ báo cáo; kiểm 20 cột mọi dòng. Đối số: giờ máy P-2110 (h)."""
import csv, io, os, sys
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')); P = os.path.join(R, 'COST-LEDGER.csv')
rows = list(csv.reader(open(P, encoding='utf-8', newline=''))); H = rows[0]; assert len(H) == 20 and all(len(r) == 20 for r in rows if r)
assert not any(r and r[0] in ('ANIMATIC-T3', 'NC-N2P', 'P-2110') for r in rows)
M = [dict(phien='ANIMATIC-T3', tap_hoac_moc='K2C-T3-01 animatic cả tập (43 shot + 2 thẻ, 761 s, cách A, LOOK-KHOA), bản xem 8 chương, xem câm AI', cong='animatic',
          ngay='2026-10-21', claude_api_usd='0.752', tran_api_usd='', model_ghim='claude-sonnet-5-5 (claude -p xem câm)', el_ky_tu_gui='0', el_ky_tu_bo_dem='0',
          gio_render='13.5', cham_chu_du_an='0', thoi_luong_s='761',
          nguon='reports/animatic-t3/ANIMATIC-BAO-CAO.md dòng 32, 66, 162–165 (nhánh ccr-d189108f-6mcz9k @41e0c8fd)',
          ghi_chu='Claude API $0,752 (§0 làm tròn $0,75; xem-cam/cost.jsonl, 6 lượt; mốc $10, dừng $30); OpenAI 0; RunPod 0; ElevenLabs 0; Gemini 0; YouTube 0; giờ máy ≈ 13,5 h đồng hồ (mốc 16 h; gồm khởi động lại container 01:17); ghi sổ bởi P-2110'),
     dict(phien='NC-N2P', tap_hoac_moc='Nghiên cứu + thử luật AI N2+ cho T4 London 1666: O1 ảnh tĩnh OpenAI, Omni Gemini, bộ kiểm N2+ có đáp án', cong='R&D',
          ngay='2026-10-21', claude_api_usd='6.946', tran_api_usd='', model_ghim='claude-sonnet-5-5; gpt-image-2.5-sunburst-2026-09-08; gpt-6.1-sol; gemini-omni-1.1-flash',
          el_ky_tu_gui='0', el_ky_tu_bo_dem='0', gio_render='3.5', cham_chu_du_an='0',
          nguon='reports/NC-N2P-BAO-CAO.md §0 dòng 18, §8 (nhánh nc-n2p @9cb001d1); sổ reports/nc-n2p/cost.jsonl, so-ai.jsonl, so-ai-gemini.jsonl',
          ghi_chu='Claude API $6,946 theo sổ cost.jsonl (49 lượt claude-sonnet-5-5); báo cáo §8 ghi thêm $1,422 q_thoi_dai.py (K, 39 khung) KHÔNG có dòng sổ — Claude tổng theo báo cáo $8,37 (vượt mốc $8); OpenAI $5,77 (ảnh $2,065 so-ai.jsonl + chữ/nhìn gpt-6.1-sol $3,708 cost.jsonl; vượt mốc $5); Gemini $9,92 (so-ai-gemini.jsonl 9 lượt × ≈ $1,10; mốc $12; số Google thực tính chưa đối chiếu); RunPod/Runway/ElevenLabs/YouTube 0; giờ máy CPU ≈ 3,5 h; ghi sổ bởi P-2110'),
     dict(phien='P-2110', tap_hoac_moc='Merge ANIMATIC-T3 + NC-N2P vào main, Kinh thánh §14.7 + §15 + §16, sổ, T3-loi-moc.json tái tạo, cập nhật main', cong='P',
          ngay='2026-10-21', claude_api_usd='0', tran_api_usd='0', model_ghim='không gọi API', el_ky_tu_gui='0', el_ky_tu_bo_dem='0', gio_render=sys.argv[1],
          cham_chu_du_an='0', thoi_luong_s='', nguon='reports/p2110/P2110-BAO-CAO.md',
          ghi_chu=f'Claude API 0; OpenAI 0; ElevenLabs 0 (không gọi); Gemini 0; YouTube 0; RunPod 0; GET gutenberg.org ×2 + distantreader.org ×1 (SHA khớp NC-N2P) + raw.githubusercontent.com TCP A63370.xml + texts.earlyprint.org + ai.google.dev/gemini-api/terms (đọc giấy phép); ghép lại moc giọng bằng reports/p2010b/ghep_lai.py (CPU) ×2; giờ máy ≈ {sys.argv[1].replace(".", ",")} h (mốc theo dõi 1,5 h); ghi sổ bởi P-2110')]
f = open(P, 'a', encoding='utf-8', newline=''); w = csv.writer(f, lineterminator='\n')
for m in M: w.writerow([m.get(k, '') for k in H])
f.close()
rows = list(csv.reader(open(P, encoding='utf-8', newline=''))); assert all(len(r) == 20 for r in rows if r); print(len(rows), 'dòng × 20 cột')
