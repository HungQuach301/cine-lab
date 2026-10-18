# design/pt — phim trường khung neo (PT, 17/10/2026)

Máy cố định tầm mắt = phim trường: chỉ dựng những gì trong khung; nền tĩnh mỗi thời kỳ dựng Cycles **một lần** ở 5 lượt chiếu sáng,
lớp sống (người, khói, chim, cờ, đèn) ghép 2D theo phép chiếu của chính máy + lượt khoảng cách của cảnh. Báo cáo: `reports/pt/PT-BAO-CAO.md`.

```bash
# nền (A = vân CC0 Poly Haven ở $PT_TEXA; B = vân AI ở $PT_TEXB) — ghost SH ở $PT_GHOST (git show nhánh SH)
/opt/bpy/bin/python design/pt/scene/build_scene.py --epoch 1943 --tex A --passes d1,d2,d3,d4,n --res 1920x1080 --spp 40 --depth --out /var/tmp/pt/final/1943A
/opt/bpy/bin/python design/pt/scene/people.py --epoch 1943 --passes d1,d2,d3,d4,n --out /var/tmp/pt/spr1943
/opt/cine/bin/python design/pt/scene/live.py --tex A --out OUT --video 960x540          # + --stills 1920x1080 [--notext]
/opt/cine/bin/python -I design/pt/tools/measure.py OUT/*-notext.jpg                     # M1 (cổng 16/10) + M2 (FIND_EDGES)
/opt/cine/bin/python design/pt/tools/blind_pt.py set OUT && ... run && ... score         # chấm mù (Claude API, ghim)
/opt/cine/bin/python -I design/pt/tools/gen_tex_b.py OUTDIR reports/pt/ai/goi-api.jsonl  # nhánh B (OpenAI, khoá do proxy gắn)
```
- `pt_site.py`: toạ độ máy neo, đọc ghost (dời 1782 +6 m Đông — trong sai số nắn SH).
- `passes.json`: giờ mặt trời biểu kiến của 5 lượt.
- Không mô hình AI nào trong dây chuyền nhánh A; nhánh B chỉ thay 9 khe vân lát được (`SLOTS`).
