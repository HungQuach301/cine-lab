# design/pt/lai — khung neo LAI "A + C có kiểm soát" (PT2, 18/10/2026)

Quy trình HC1–HC6 (chủ dự án duyệt 18/10). Báo cáo: `reports/pt2/PT2-BAO-CAO.md`. Nền A + sprite + tấm C nằm ngoài git ở `/var/tmp/pt2/`.

```bash
export PT_GHOST=/var/tmp/pt/ghost PT_TEXA=/var/tmp/pt/texA      # ghost SH (git show) + vân Poly Haven CC0 (SHA trong reports/pt/giay-phep)
# 1) nền A (Cycles) + lượt độ sâu + lượt mã lớp + lượt nắng — máy chọn bằng PT_CAM (pt = Commercial Square 1943; k1782 = hẻm K09/K10 1782)
PT_CAM=k1782 /opt/bpy/bin/python design/pt/scene/build_scene.py --epoch 1782 --tex A --passes d1,d2,d3,d4,n --res 1920x1080 --spp 40 \
    --depth --clspass --sunvis d1,d2,d3,d4 --out /var/tmp/pt2/bg/1782A
# 2) người MakeHuman/MPFB (chỉ đọc dữ liệu CC0 — không chạy mã addon): 8 hướng × (đứng + 8 pha đi) × 5 lượt
/opt/bpy/bin/python design/pt/lai/mh_people.py -- --epoch 1782 --head 268.7 --roles linh,linh2,phao_binh,dan_nam,dan_nu,thuy_thu --out /var/tmp/pt2/spr1782
# 3) tấm C (một tấm/khung neo × mốc, chỉ ban ngày d2, mặt nạ từ lượt mã lớp) — OpenAI /v1/images/edits, khoá do proxy gắn
/opt/cine/bin/python -I design/pt/lai/gen_c2.py /var/tmp/pt2/bg /var/tmp/pt2/c reports/pt2/ai-c/goi-api.jsonl 1782 [--lan 2]
# 4) HC4 rà: tờ 200 % + ứng viên 400 % → reports/pt2/kiem-du-kien.json (phiên rà, KHÔNG chấm mù)
/opt/cine/bin/python -I design/pt/lai/kiem_c.py /var/tmp/pt2/bg/1782A /var/tmp/pt2/bg/1782L/d2.png /var/tmp/pt2/kiem1782
# 5) ghép HC2 + chiếu sáng theo lượt → nền LAI (vùng bảo vệ = đúng giá trị 16 bit của A); --xoa-lop = vật bị loại ở HC4
/opt/cine/bin/python -I design/pt/lai/compose_c2.py /var/tmp/pt2/bg/1782A /var/tmp/pt2/c/1782-d2-lan2.png /var/tmp/pt2/bg/1782L --xoa-lop 9510
# 6) lớp sống trên cùng + nhãn → video/khung (LAI và A-thuần cùng hạt giống); đo; chấm mù
/opt/cine/bin/python -I design/pt/lai/live2.py --ban LAI --out OUT --video 960x540      # và --ban A; --stills 1920x1080 --notext
/opt/cine/bin/python -I design/pt/lai/measure2.py OUT reports/pt2/do/do-khung.json
/opt/cine/bin/python design/pt/lai/blind_lai.py set OUT && ... run && ... score
```
- `lai_common.py`: giải mã lượt mã lớp (`cls = mã vùng × 64 + mã vật liệu`), mặt nạ được sửa (tường/mái/đất/đồ vật nền) và vùng bảo vệ.
- Vùng bảo vệ: trời, đồi/chân trời, biển, tàu, Line Wall, cột cờ, pháo, đạn pháo, đèn, chốt gác, hầm, xe tải; trên toà: kính, lòng cửa, cửa chớp, cửa,
  ban công, biển hiệu trơn, phần ĐỔ NÁT. Cờ, người, khói = lớp sống vẽ sau (không qua AI).
