# design/pt3 — vân nướng (HC7) + tấm chiếu (HC8) cho MÁY CHUYỂN ĐỘNG (PT3, 18/10/2026)

Bản sao có sửa từ `design/pt/` @7adb88f (không sửa `design/pt/`). Báo cáo: `reports/pt3/PT3-BAO-CAO.md`.

```bash
S=design/pt3/scene; T=design/pt3/tools; P=/opt/bpy/bin/python; Q="/opt/cine/bin/python -I"
# 1. chọn nhóm mặt cần vân (khung mẫu dọc cú máy)
$P $S/build_pt3.py --site street --mode probe --out RUN/probe_street --res 480x270 --step 12
$Q $T/select_groups.py RUN/probe_street street RUN/groups_street.json
# 2. dựng trực giao albedo + mặt nạ (mặt tường phẳng / mái-sàn) → ghép dải mỗi toà, chia khúc API
$P $S/build_pt3.py --site street --mode elev --groups RUN/groups_street.json --out RUN/elev_street   # (+ --mode top)
$Q $T/prep_ai.py street RUN/elev_street RUN/top_street RUN/groups_street.json AI_IN/street
# 3. sửa ảnh (OpenAI /v1/images/edits, khoá do proxy gắn) → sổ reports/pt3/ai/goi-api.jsonl
$Q $T/gen_ai.py AI_IN/street/chunks.json all --ref AI_IN/street/style_ref_street.png --try2
# 4. sàng tự động + rà mắt (HC4) → nướng atlas (kiểm trôi, nắn khung, đều sáng/neo màu σ 1 m, ghép cứng, hoà khúc)
$Q $T/kiem_van.py AI_IN/street reports/pt3/ai OUT.json
PT3_LOAI=reports/pt3/do/loai-ra-mat-street.json $Q $T/bake_hc7.py AI_IN/street reports/pt3/ai ATLAS/street reports/pt3/do/nuong-street.json
# 5. dựng cú máy A / HC7 (PNG + lượt pos/aux EXR)
PT3_KINDS=beauty,pos,aux $P $S/build_pt3.py --site street --tex A   --mode anim --out RUN/stA  --spp 16
PT3_KINDS=beauty,aux     $P $S/build_pt3.py --site street --tex HC7 --mode anim --atlas ATLAS/street --out RUN/stH7 --spp 16
# 6. HC8 (orbit): tấm C ở góc chính → sửa ảnh → chiếu ngược + hoà theo góc nhìn
$P $S/build_pt3.py --site kb --mode proj --res 1920x1080 --spp 32 --out RUN/projA ; $Q $T/hc8.py prep RUN/projA AI_IN/hc8 --thu2
$Q $T/hc8.py comp RUN/projA HC8C RUN/kbA RUN/kbH8 reports/pt3/do/hc8-cung-may.json
# 7. đo + video + chấm mù
$Q $T/do_pt3.py street RUN/stH7 RUN/stA RUN/stH7 reports/pt3/do/do-stH7.json ; $Q $T/video.py ra.mp4 log.jsonl HC7:RUN/stH7
$Q $T/blind_pt3.py set|run|score
```
- `scene/pt_site.py` (bản sao, đổi đường ghost), `scene/cams.py` (đường bay, vùng dựng, phép chiếu dùng chung), `data/osm-kings-bastion.json` (ODbL).
- Không mô hình AI nào trong dây chuyền dựng; AI chỉ ở bước 3 (ảnh vân) và HC8 (tấm C). Mọi khung có vân AI: `ai_texture: true` (log video) + dòng chữ trên hình.
