# design/pt/song — khung neo LAI "có sự sống" (PT4, 18/10/2026)

Kế thừa `design/pt/lai/` (PT2). Báo cáo: `reports/pt4/PT4-BAO-CAO.md`. Nền, sprite, tấm C nằm ngoài git ở `/var/tmp/pt4/`.

```bash
export PT_GHOST=/var/tmp/pt/ghost PT_TEXA=/var/tmp/pt/texA PT4=1      # PT4=1: lòng nhà đổ nát, tàu 1943, hầm dựng lại (vùng BẢO VỆ)
# 1) nền A (như PT2) — chạy lệnh dài với thời hạn > 30 phút
PT_CAM=k1782 /opt/bpy/bin/python design/pt/scene/build_scene.py --epoch 1782 --tex A --passes d1,d2,d3,d4,n --res 1920x1080 --spp 40 \
    --depth --clspass --sunvis d1,d2,d3,d4 --out /var/tmp/pt4/bg/1782A
PT_CAM=pt PT2_NO_SANDBAG=1 /opt/bpy/bin/python design/pt/scene/build_scene.py --epoch 1943 ... --out /var/tmp/pt4/bg/1943A
# 1782 dùng lại tấm C PT2 → cần nền CŨ (không PT4) lượt d2 + mã lớp:
PT4= PT_CAM=k1782 /opt/bpy/bin/python design/pt/scene/build_scene.py --epoch 1782 --tex A --passes d2 --res 1920x1080 --spp 40 --depth --clspass --out /var/tmp/pt4/bg/1782old
# 2) người: 13 tờ/mốc (6 vai × 2 dáng + cặp khiêng), 8 hướng × 21 tư thế × lượt d1,d2,d4 (ghi meta sau mỗi dáng; chạy lại thì giữ EXR đã có)
/opt/bpy/bin/python design/pt/song/mh_people4.py -- --epoch 1782 --head 268.7 --roles linh,linh2,phao_binh,dan_nam,dan_nu,thuy_thu,khieng --out /var/tmp/pt4/spr1782
/opt/bpy/bin/python design/pt/song/mh_people4.py -- --epoch 1943 --head 281.0 --roles linh,linh2,thuy_thu,thuy_thu_trang,raf,tho,khieng --out /var/tmp/pt4/spr1943
# 3) tấm C 1943 lần 2 (mặt nạ chặn kiến trúc; trần OpenAI $2)
/opt/cine/bin/python -I design/pt/song/gen_c4.py /var/tmp/pt4/bg/1943A /var/tmp/pt4/c reports/pt4/ai-c/goi-api.jsonl 1943 --lan 2
# 4) ghép (HC2) — HC4 quyết các cờ: --ma-cua-A (W6), --dat-xa 62 (W7); 1782: --nen-cu + --xoa-lop 9510; --sac-A = biến thể sắc độ A
/opt/cine/bin/python -I design/pt/song/compose4.py /var/tmp/pt4/bg/1943A /var/tmp/pt4/c/1943-d2-lan2.png /var/tmp/pt4/bg/1943L --ma-cua-A --dat-xa 62
/opt/cine/bin/python -I design/pt/song/compose4.py /var/tmp/pt4/bg/1782A reports/pt2/ai-c/1782-d2-lan2.png /var/tmp/pt4/bg/1782L --nen-cu /var/tmp/pt4/bg/1782old --xoa-lop 9510
# 5) lớp sống + không khí + màu LAI riêng → khung/video; đo; chấm mù PT4 vs PT2
/opt/cine/bin/python -I design/pt/song/live4.py --ban LAI --out OUT --stills 1920x1080 --notext     # --ban A (màu chung), --grade lai (kiểm HC2), --video 960x540
/opt/cine/bin/python -I design/pt/song/measure4.py ra.json nhan=anh.png ... [--bv bao_ve.png LAI.png A.png]
/opt/cine/bin/python design/pt/song/blind4.py set OUT && ... run && ... score      # PT4_VONG=kiem-mu-v2: vòng 2, 6 khung ngày
```
- Rà dữ kiện tấm C: `design/pt/lai/kiem_c.py` (PT2) trên nền LAI d2 đã ghép.
- RAM: sprite nạp float16 không đệm (13 tờ × 3 lượt × 2 mốc ≈ 5,4 GB); tờ sprite không SUBSURF (168 người/tờ).
