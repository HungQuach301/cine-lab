# V6 · KHUNG NEO (1782 hẻm + 1943 Commercial Square) — BÁO CÁO PHIÊN XƯỞNG CON

> Phiên xưởng con của V6, 18/10/2026. Làm trong worktree `agent-a277c00f732fc405d`; harness không cho đổi sang nhánh `ccr-0e3bf8dd-nst2mv`, nên mã `design/pt/**` được sao từ checkout chính sang worktree rồi sửa ở đó. **Không commit, không push.**
> Mọi số trong báo cáo là số đo thật của phiên. Tệp lớn để ngoài git ở `/var/tmp/v6kn/`, SHA ghi trong `k-lai/sha256-png-ngoai-git.json`.

## 0. Tóm tắt
1. **Người vẫn trông như đồ chơi: toy_like chưa đạt ≤ 4.** Ở vòng 2 (6 khung ngày, 3 người chấm × 6 = 18 phiếu), V6 sản xuất được **6,61**, PT4 được 6,83. V6 thắng **15 – 3** phiếu "tốt hơn". Craft 6,17 so với 5,72; chi tiết 6,17 so với 5,50; đúng thời kỳ 6,11 so với 5,06; ai_look 4,89 so với 5,22. Vòng 1 hai bản hoà 9 – 9, toy_like V6 7,17 so với PT4 6,94.
2. **Không truy cập được MPFB2.** Proxy trả 403 "GitHub access to this repository is not enabled" cho `makehumancommunity/mpfb2`, cả qua git, codeload lẫn `gh api`. Phiên không tìm đường vòng. Người được **tự dựng** bằng `design/pt/song/nguoi6.py`: thân, đầu và quần áo là SDF, chuyển thành lưới bằng marching cubes. Không dùng tài sản bên thứ ba.
   - Lưu ý: Kinh thánh §11.6 ghi "người: MakeHuman/MPFB". Đây là lệch kỹ thuật, chờ chủ dự án quyết (§11).
3. **Người khung neo (ngày, theo log mọi khung 540p):**
   - 1782: tối thiểu 22, trung bình 44,6, tối đa 58.
   - 1943: tối thiểu 26, trung bình 38,1, tối đa 48.
   - Khung tĩnh 1080p: 33 / 47 / 55 (1782) và 33 / 43 / 37 (1943) cho sáng / trưa / chiều.
   - Tất cả đạt Q-PT4-4 (trung bình 30–80, tối thiểu ≥ 15).
4. **Tấm C 1943 lần 3:** một lệnh OpenAI, **$0,0632**, C2PA có. Mặt nạ bảo vệ thêm mặt đất xa > 55 m (1,54 % khung), thay cho ghép `--dat-xa`. Kiểm dữ kiện HC4: **0 lỗi chắc, 0 nghi vấn**. W5, W6, W7 đều không còn.
5. **K-LAI (q_lai.py 1.15):**
   - Đạt: K-LAI-2 (nhãn 40 px), K-LAI-3, K-LAI-4 (≤ 0,001/255), K-LAI-5 (đêm 0,82× và 0,92×), K-LAI-6.
   - **TRƯỢT K-LAI-1** (100 % khung là AI): tất yếu với đoạn thử chỉ gồm khung neo, giống PT2.
   - **TRƯỢT K-LAI-B ở 2 khung đêm** (bão hoà trung vị 0,50 và 0,63, do khung gần đen). Các khung ngày đạt: 0,212–0,357.
   - O2 (q_thoi_dai): **ĐẠT**, 0 nghi vấn ở cả 6 khung ngày.
6. **Bản TỐT NHẤT** (người là lưới 3D trong cảnh, Cycles 256 spp + OIDN, rồi ghép LAI): **xong cho cả 2 khung trưa**.
   - Chấm mù bản tốt nhất so với bản sản xuất: **5 – 0, hoà 1**.
   - toy_like **5,83** (bản sản xuất 6,67); craft 6,00 so với 5,67; chi tiết 6,00 so với 5,17.
   - Dựng Cycles: 663 s/khung (1782) và 794 s/khung (1943); tính cả dựng người là 1 194 s và 1 405 s (§7).

## 1. Hạ tầng (việc 1)
- **Ghost SH:** lấy bằng `git archive origin/claude/sh-ghost-gibraltar-t3-1gkftx` (đã fetch), đặt ở `/var/tmp/pt/ghost/`.
- **Poly Haven:** tải lại toàn bộ manifest, **SHA 42/42 khớp** `reports/pt/giay-phep/polyhaven-files.json` (9 vân dùng nằm trong số đó).
- **MPFB2:** bị chặn (xem §0.2).
- **OpenEXR:** đã có trong `/opt/cine`.
- **Thư viện cài thêm** (ngoài git, `/var/tmp/v6kn/pylib313`, pip): `scikit-image` 0.26 (BSD-3) cho marching cubes, `opencolorio` 2.6 (BSD-3) để áp đúng biến đổi hiển thị AgX của Blender. Kiểm OCIO so với PNG Blender: lệch < 0,3 % trên 8 mảng xám và màu (`design/pt/song/agx6.py`).
- **Nền A V6** (`PT6=1`, cờ mới trong `design/pt/scene/build_scene.py`; giữ nguyên chuỗi ngẫu nhiên của cảnh):
  - 1782A: 5 lượt + độ sâu + mã lớp + lượt nắng, 40 spp, 2 luồng, 275–290 s/lượt.
  - 1782old: nền PT2 cho tấm C PT2.
  - 1943A.
  - Ghép LAI bằng `compose4.py`: 1782 dùng `--nen-cu 1782old --xoa-lop 9510`; 1943 dùng `--ma-cua-A`. Vùng bảo vệ sai khác 0,0/255 ở mọi lượt.

## 2. Người (việc 2) — `nguoi6.py` + `mh_people6.py` + `live6.py`
- **(a) Quần áo là lưới riêng có độ dày.**
  - Mỗi lớp là vỏ giữa hai mặt lệch của thân, dày ≥ 13 mm. Mép gấu, vạt và ống lộ bề dày vải.
  - Nếp gợn quanh khuỷu, gối, eo, nách, háng, có xoắn nhẹ, cộng nhiễu vải thô.
  - Áo 1782 có vạt cắt chéo phía trước, xẻ sau, mép bẻ ngược lộ lót trắng; quần chẽn, ghệt đen tới gối, đai chéo; ống quần tách nhau dưới háng.
  - 1943: battledress (áo tới eo có cạp, 2 túi ngực, quần rộng có túi đùi, xà cạp, dây đeo mẫu 1937); khaki drill xắn tay; RN lam và RN trắng (cổ vuông, áo lót cổ chữ V, quần ống loe); RAF; thợ dân sự.
- **(b) Tỉ lệ và tay.** Đầu ≈ 1/7,5 chiều cao. Tay buông, giạng 6°, khuỷu chùng 12°. Khi đi tay đung đưa ±13° cạnh thân.
- **(c) Mũ là một lưới liền, có bề dày (Solidify).**
  - Tricorn: một vành tròn bẻ lên 3 phía quanh 3 cạnh tam giác, có viền ren trắng và nơ đen.
  - Các mũ khác: Brodie Mk II, mũ calô, mũ lính thuỷ, mũ vải lưỡi trai, mũ tròn 1782, mũ vải nữ.
- **(d) Ánh sáng.** Trời Nishita và mặt trời **dùng y hệt mã `set_pass` của nền** cho các lượt d1, d2 và d4.
  - Tách 2 nhóm sáng (light group "nắng" / "trời"). Ghép theo lượt nắng của nền; trong bóng nhà, hệ số ánh trời được hiệu chuẩn từ chính nền A: tỉ số chói cảnh đất bóng / đất nắng, chia cho tỉ số của thẻ xám 18 % trong tờ sprite.
  - Thêm hắt sáng ấm (1,12 / 1,0 / 0,8) và hệ số mặt đứng (1782: 0,68; 1943: 0,85). Sau đó áp AgX (OCIO) như nền.
- **(e) Dáng và chuyển động.** 3 dáng thân cho lính chính, 1–2 dáng cho vai phụ. Có tư thế đi quay đầu 32° (cột `wl`; quay phải bằng lật gương hướng đối xứng); mỗi người đi 0–2 lần quay đầu, 0,6–1,5 s. Bỏ vệt phơi sáng (người "ma").
- **Tờ sprite:**
  - 1782 có 11 tờ: linh×3, linh2×2, phao_binh×2, thuy_thu, dan_nam, dan_nu, khieng.
  - 1943 có 10 tờ: linh×3, linh2×2, thuy_thu, thuy_thu_trang, raf, tho, khieng.
  - 8 hướng × 29 tư thế × 3 lượt; 120 px/m; 5 spp + OIDN; dựng theo cặp hàng để giới hạn RAM.
  - Đã giảm dáng phụ để kịp giờ: dự định 13 tờ/mốc.
- **Mật độ (Q-PT4-4).** Tuyến đi có điều kiện tránh vật trên đất (`vat_can` từ meta nền), `fill_min` 22 người, người gần máy nhất 14 m (sau chấm mù vòng 1).
- **1943 không có phụ nữ hay trẻ em.** Vai 1943 đều là nam (S114).

### Nguồn trang phục (vật mang dữ kiện) — chi tiết trong `ROLE_SRC` của `nguoi6.py`
| Mốc | Nguồn đối chiếu | Mức |
|---|---|---|
| 1782 bộ binh / pháo binh | Tranh PD trong TIEN-KY T3: phác thảo Copley (Met 60.44.17; Cleveland 1950.215), bản khắc Sharp theo Copley (LoC 96510788), Trumbull "Sortie" (Met 12828). Kiểu áo theo Royal Clothing Warrant 1768 nhưng chưa trích nguyên văn | **approx.**; màu nẹp trung đoàn là **illustrative** |
| 1782 thuỷ thủ, dân nam, dân nữ | không có nguồn riêng; S062 cho biết phần lớn dân đã rời phố nên tỉ lệ thấp | **illustrative** |
| 1943 battledress, KD, Brodie, mũ calô, RN, RAF | ảnh tra cứu Commons/IWM 1941/42 (chỉ tra cứu, `reports/pt4/nguon/KET-QUA.md`) | **approx.** |
| 1943 thợ dân sự nam | — | **illustrative** |

## 3. Vật nền phụ (việc 3, luật Q-PT4-3 sửa 12:55)
Bảng dưới gồm cả quyết định GIỮ / BỎ cho vật sẵn có của A.

| Mốc | Vật | Số | Quyết định | Lý do |
|---|---|---|---|---|
| 1943 | Chậu cây trên ban công (sẵn có của A) | 102 | **BỎ cả 102** | Đồ gia đình; dân thường đã sơ tán từ 1940 (S114). 102 chậu là "đồ gia đình đông đúc" nên trái hoàn cảnh |
| 1943 | Mái che vải cửa hàng (sẵn có) | 40 | **GIỮ 13, BỎ 27** | Cửa hàng phục vụ đồn trú là hợp lý. Chỉ giữ trên cửa hàng **mở**, thưa khoảng 1/2 (chọn theo vị trí) cho mật độ vừa phải. Bỏ mái trên cửa đóng. Không chữ |
| 1782 | Mái che vải cửa hàng (sẵn có) | 1 | **BỎ** | Phố bị bắn phá; dân bỏ đi từ 12/4/1781 (S062); kho bị cướp (S063). Vật này nằm ngoài khung nên không gây vá |
| 1782 | Thùng gỗ vỡ: ván bật, một đai sắt, ván rời trên đất (mới) | 2 | THÊM | S063: lính phá kho rượu 4/1781. Gỗ và sắt đúng thời kỳ |
| 1782 | Giỏ đan lật nghiêng (mới) | 1 | THÊM | Đồ chở đất/đá của tổ sửa tường; cói hoặc liễu |
| 1943 | Tường bao cát hình gối trước cửa ra vào (mới) | 5 | THÊM | Đặc trưng thị trấn đồn trú thời chiến; bao bố; không chữ |
| 1943 | Chồng hòm gỗ quân dụng không chữ (mới) | 1 | THÊM | Đồ quân dụng, gỗ sơn ô-liu hoặc để mộc |
| 1943 | Nhóm thùng phuy thép 40 gallon, sơn tối, không chữ (mới) | 2 | THÊM | Vật phổ biến thời chiến |
| Giữ như PT4 | 1782: thùng ×5, gạch vụn, dầm chống, đống đạn, đèn, pháo, cột cờ. 1943: thùng ×3, xe kéo (vật mang dữ kiện "xe", **illustrative**), đèn ×3, hầm, cột cờ, tàu | — | GIỮ | như PT4 |

- Vật mới mang mã vùng **9516**, thuộc vùng **BẢO VỆ**: điểm ảnh A, không qua AI.
- Lớp sống tránh đi xuyên vật (`vat_can`): 1782 có 15 vật, 1943 có 17.
- Chưa có nguồn riêng cho vật phụ: áp luật tầng (b).

## 4. Tấm C 1943 lần 3 (việc 4) — `gen_c6.py`, sổ `ai-c/goi-api.jsonl`
- Model `gpt-image-2.5-sunburst` (cả yêu cầu và phản hồi), `/v1/images/edits`, 2048×1152, chất lượng high.
- Mặt nạ: **41,29 % được sửa**; bảo vệ mặt đất > 55 m.
- Usage: 1 508 token ảnh vào + 493 token chữ vào + 1 522 token ra → **$0,06319**. C2PA `caBX` có. Ngày 2026-10-18T07:23:41Z. SHA tệp `f8e0dbfd…c550d`.
- Prompt ghi nguyên văn trong sổ. Đã thêm câu cấm tường, bậc, bó vỉa, lan can trên mặt đất, và câu "giữ bao cát, hòm, phuy".
- **Kiểm dữ kiện** (`kiem-du-kien.json`, bằng chứng `kiem/bang-chung-1943-lan3.jpg`): kiem_c.py cho 12 ứng viên, cộng 16 ô rà 200 % trên kết quả ghép thật.
  - 0 lỗi chắc.
  - W8: bóng nhà trên đất bị C vẽ lại mềm hơn — bề mặt / ánh sáng, giữ.
  - W9: viền A 3 px quanh bao cát — mép ghép, giữ.
- **So với `--dat-xa` của PT4:** mặt đất xa giờ là đá lát của C, không còn dải A mịn. Đó là lợi ích của việc sinh lại.
- 1782 dùng lại tấm C PT2 lần 2.

## 5. Bản sản xuất (việc 5) — `live6.py`
- **Khung 1080p, không chữ và có chữ:**
  - JPEG q90 ở `khung/` (8 khung LAI không chữ, 8 có chữ).
  - PNG ở `/var/tmp/v6kn/sx/`. Trưa: `1782-trua-LAI-notext.png` (SHA `8e59091583d3…`), `1943-trua-LAI-notext.png` (SHA `ed2e0c9f4a0f…`).
  - Nhãn phương pháp 40 px, góc dưới trái.
- **Video 540p mỗi khung neo:** `v6-LAI-960x540-1782.mp4` (0,69 MB) và `v6-LAI-960x540-1943.mp4` (0,65 MB). H.264, crf 25, 9 s.
- **s/khung (live, nền và sprite đã đệm):**
  - 1080p: khoảng 5,5–6 s/khung (4 khung trong 22–26 s); lần đầu dựng đệm sprite mất 60–140 s/mốc.
  - 540p: 0,38–0,44 s/khung (216 khung trong 82–95 s).
  - Nền A (Cycles 40 spp, 2 luồng): 275–292 s mỗi lượt.
  - Sprite: khoảng 40–80 s cho mỗi cặp hàng × lượt.

## 6. Số đo (`do/do-khung.json`) — đo theo cách của điều phối (640×360 INTER_AREA, cắt y 60–300)
Thứ tự trong mỗi ô: bão hoà / colorfulness / FIND_EDGES / tương phản.

| Khung | V6 sản xuất | PT4 |
|---|---|---|
| 1782 sáng | 0,212 / 33,0 / 34,6 / 0,253 | 0,212 / 33,7 / 34,3 / 0,252 |
| 1782 trưa | 0,224 / 32,5 / 35,2 / 0,253 | 0,227 / 33,0 / 34,5 / 0,256 |
| 1782 chiều | 0,231 / 25,5 / 20,3 / 0,266 | 0,220 / 22,1 / 19,2 / 0,268 |
| 1782 đêm | 0,502 / 30,6 / 5,9 / 0,056 | 0,502 / 30,5 / 5,8 / 0,056 |
| 1943 sáng | 0,325 / 48,5 / 31,1 / 0,261 | 0,286 / 44,8 / 32,4 / 0,267 |
| 1943 trưa | 0,314 / 40,7 / 31,0 / 0,261 | 0,278 / 38,7 / 31,9 / 0,271 |
| 1943 chiều | 0,357 / 42,0 / 25,0 / 0,275 | 0,329 / 42,6 / 25,8 / 0,274 |
| 1943 đêm | 0,502 / 19,9 / 3,3 / 0,033 | 0,502 / 19,8 / 3,3 / 0,034 |

- **Vùng bảo vệ LAI so với A** (PNG, q_lai K-LAI-4): ≤ 0,001/255 (< 1/255) ở cả 8 khung.
- **Người / khung:** xem §0.3.

## 7. Bản tốt nhất (việc 6) — `best6.py`
- Chạy lại chính `build_scene.py` (cùng mã, cùng hạt giống) ở lượt d2.
- 41–47 người là lưới 3D (`nguoi6`, ngân sách mặt cao `N6_FB_HI`, 79 k mặt/người), dùng bản sao liên kết. Vị trí, dáng và hướng lấy theo kế hoạch người của khung trưa sản xuất (`live6.py --plan`).
- Mã lớp 9560 thuộc vùng BẢO VỆ khi ghép LAI. Bóng người chuyển vào tấm C qua `--nen-cu`.
- Cycles **256 spp + OIDN**, 3 luồng.
- **Cách dựng:** chia 2 dải ngang (`BEST_BORDER`; mỗi lệnh dưới 29 phút, mỗi lần một tiến trình Blender). Ghép dải bằng `best_ghep6.py`, rồi `compose4` (`--nen-cu`), rồi `live6 --nonguoi`. Ở bước live, người 3D được xử lý màu vải giống sprite.
- Vùng bảo vệ của người **không nở**: bản đầu nở 3 px nên lộ viền đất A sáng quanh người. Đã sửa trong `lai_common.py`.
- **Số người trong cảnh:** 1782 có 47 người / 9 mẫu; 1943 có 43 người / 10 mẫu.
- **s/khung (Cycles 256 spp, 3 luồng):**
  - 1782: 389 + 274 = **663 s** dựng ảnh; cả hai lệnh (gồm dựng cảnh và người ~240 s mỗi dải) **1 194 s**.
  - 1943: 495 + 299 = **794 s**; cả hai lệnh **1 405 s**.
  - Lần thử đầu (bỏ vì kế hoạch người đổi ở vòng 2): 840 s.
- **Khung** (JPEG trong `khung/`, PNG ngoài git):
  - `1782-trua-TOTNHAT-notext.jpg`; PNG `/var/tmp/v6kn/tn/1782-trua-LAI-notext.png`, SHA `55539c447191…`.
  - `1943-trua-TOTNHAT-notext.jpg`; PNG `/var/tmp/v6kn/tn/1943-trua-LAI-notext.png`, SHA `a30c2521ef59…`.
- **Số đo** (bão hoà / colorfulness / FIND_EDGES / tương phản): 1782 0,220 / 32,0 / 35,4 / 0,259; 1943 0,314 / 40,5 / 31,6 / 0,263.
- **Chấm mù `tn-sx`** (`kiem-mu/v2/tn-sx`), bản tốt nhất / bản sản xuất:

| | craft | detail | period | ai_look | toy_like | Phiếu |
|---|---|---|---|---|---|---|
| Tốt nhất / sản xuất | 6,00 / 5,67 | 6,00 / 5,17 | 6,00 / 6,00 | 5,50 / 5,50 | **5,83** / 6,67 | **5 – 0, hoà 1** |

## 8. K-LAI (việc 7) — `episode-lai.yaml`, `k-lai/`
- **Đầu vào đã ghi:**
  - Log khung gộp có `shot` (`k-lai/log-khung.jsonl`, 432 khung).
  - Log chữ có `box` (`k-lai/log-chu.json`).
  - Sổ AI gộp (`k-lai/goi-api-gop.jsonl`): 5 lệnh của 2 khung neo × mốc qua PT2, PT4 và V6, có cờ `dung`.
  - `bao_ve`: 8 cặp PNG LAI/A cùng chỉnh màu, kèm `bao_ve-*.png` và `bat_buoc-*.png` lấy từ lượt mã lớp (trời, Line Wall, tàu, đồi, biển, cột cờ, đèn, pháo, kính và lòng cửa). Phần nằm ngoài mặt nạ: 0,0 %.
  - Cặp đêm.
  - Thư mục khung LAI (`/var/tmp/v6kn/klai`).
  - `duyet.yaml` rỗng.
  - Khối `o2:`.
- **Kết quả q_lai.py** (`k-lai/q_lai-ket-qua.txt`):

| Mã | Kết quả |
|---|---|
| K-LAI-1 | TRƯỢT: 100 % là khung AI. Đây là đoạn thử chỉ gồm khung neo. Ngưỡng 20 % chỉ có nghĩa trên một tập phim |
| K-LAI-2 | ĐẠT: 432/432 khung có nhãn, 40 px |
| K-LAI-3 | ĐẠT: 2 tấm dùng, 0 lỗi, 0 nghi vấn |
| K-LAI-4 | ĐẠT: ≤ 0,001/255 |
| K-LAI-5 | ĐẠT: 5 lệnh thành công, 2 tấm dùng; 1943 có 3 lệnh, đúng ngưỡng 1+2. Đêm 0,82× và 0,92× |
| K-LAI-6 | ĐẠT: 5 lệnh, $0,3139 cộng dồn PT2+PT4+V6, C2PA 5/5 |
| K-LAI-B | TRƯỢT 2 khung đêm (0,502 và 0,627); ngày 0,212–0,357 |

- **O2 q_thoi_dai** (`k-lai/o2v2-*/ket-qua.json`, khung vòng 2): 6 khung ngày, **0 nghi vấn**, $0,251.
  - Ghi chú độ tin < 0,5 ở 1782: "cờ giống mẫu 1801". **Sai.** Cờ do mã vẽ theo đúng mẫu 1707 (PT2 đã kiểm). Máy soi lặp lại lỗi người chấm PT4.
  - Ghi chú ở 1943: "thuyền buồm kiểu galleon". Đây là thuyền đánh cá có sẵn từ PT.
  - Vòng 1 (`o2-*`) cũng 0 nghi vấn, $0,240.
- **Chưa làm:** chưa rà riêng người trên mọi khung có vật phụ; O2 mới phủ 6 khung ngày.

## 9. Chấm mù (việc 8) — `kiem-mu/v1`, `kiem-mu/v2` (`blind6.py`)
Giao thức như blind4: sonnet-5-5, chỉ Read, 3 vai `blind_v2`, hạt giống 20261018. Không dùng khung đối thủ.

| Vòng | | craft | detail | period | ai_look | toy_like | Phiếu |
|---|---|---|---|---|---|---|---|
| v1 (người ≥ 10 m, bão hoà 0,74) | V6 / PT4 | 5,72 / 5,78 | 5,78 / 5,28 | 5,67 / 5,28 | 5,11 / 5,22 | **7,17** / 6,94 | 9 – 9 |
| v2 (người ≥ 14 m, bão hoà 0,66) | V6 / PT4 | **6,17** / 5,72 | **6,17** / 5,50 | **6,11** / 5,06 | **4,89** / 5,22 | **6,61** / 6,83 | **15 – 3** |
| v2 1943 | V6 / PT4 | 6,11 / 5,78 | 6,11 / 5,33 | 6,44 / 5,22 | 4,56 / 5,22 | 6,22 / 6,67 | — |

- **Góp ý lặp lại:** "mannequin / clay-coloured / doll-like"; cần chất liệu vải và da thật, tư thế đa dạng, bóng tiếp đất, ít người gần máy hơn, và motion blur hoặc độ sâu trường ảnh.
- 1943 chiều PT4 vẫn thắng nhờ sương làm khuất người (toy_like 4).
- Một phiếu 1782 chiều chê "mũ như shako": tricorn nhìn ngược sáng.

## 10. Chi phí, giờ máy, chỉ số ±5 %
- **OpenAI: $0,0632** (1 lệnh).
- **Claude: $2,948**, chi tiết:
  - Chấm mù v1: $1,068.
  - Chấm mù v2 bộ pt4-sx: $1,039.
  - Chấm mù bộ tn-sx: $0,350.
  - O2 vòng 1: $0,240.
  - O2 vòng 2: $0,251.
  - Vượt mốc phần phiên con khoảng $2 thêm ~$0,95. Lý do: chạy đủ vòng 2 và bộ tốt nhất / sản xuất để có số toy_like đầy đủ.
- **Giờ máy** (`log/gio-may.tsv`): khoảng 7,2 h tiến trình, cộng bản tốt nhất ≈ 0,8 h, tổng ≈ 8 h. Gồm:
  - Nền A: 3 350 s.
  - Sprite: khoảng 20 500 s tiến trình, gồm cả các lượt bỏ: dừng vì OOM 2 lần, đổi vật liệu vải, đổi cách dựng theo hàng, dừng theo yêu cầu RAM của phiên chính.
  - Ghép, C và kiểm: khoảng 60 s.
  - Live: khoảng 1 100 s.
- **OOM:** lần OOM thứ 2 (2 tờ sprite chạy song song, ~7 GB mỗi tờ) đã **giết một tiến trình chromium của phiên chính**. Đã sửa: dựng theo cặp hàng (~3,6 GB) và từ đó chỉ chạy một tiến trình Blender.
- **Chỉ số trong ±5 % quanh ngưỡng:**
  - K-LAI-5: 1943 có 3 lệnh sinh thành công = ngưỡng 1+2 (0 %).
  - Nhãn 40 px so với ngưỡng 38 px (+5,3 %, sát biên).
  - Bão hoà 1943 chiều 0,357 so với 0,40: −11 %, không nằm trong ±5 %.
  - Không chỉ số nào khác.

## 11. Việc chờ chủ dự án
1. **Người tự dựng thay MPFB** (Kinh thánh §11.6): chấp nhận, hoặc mở quyền GitHub `makehumancommunity/mpfb2` cho phiên sau (`add_repo`). Mã `mh_people6.py` hiện chỉ dùng thân tự dựng.
2. **toy_like vẫn 6,6** (mục tiêu ≤ 4). Hướng tiếp theo ước khoảng 1 phiên:
   - vân vải và da (bản đồ vân thật thay màu trơn);
   - bóng tiếp đất từ lượt sprite (shadow catcher);
   - motion blur khi đi và độ sâu trường ảnh;
   - giảm người ở 14–20 m;
   - nhiều dáng và tư thế hơn.
3. **Danh sách vật phụ §3**: duyệt các quyết định giữ 13 / bỏ 27 mái che, bỏ 102 chậu cây (1943) và bỏ mái che 1782.
4. **K-LAI-B đêm**: luật nên loại khung gần đen, hoặc chủ dự án chấp nhận ngoại lệ. K-LAI-1 chỉ áp cho tập phim.
5. **Đĩa:** theo yêu cầu phiên chính đã xoá tờ sprite EXR và đệm npz (≈ 9 GB), cùng mọi bản thử. Muốn dựng lại video hoặc khung sản xuất phải dựng lại sprite: `run/spr.sh`, khoảng 2–2,5 h, mỗi lần một tiến trình. Còn giữ:
   - nền A, LAI và bản tốt nhất (`/var/tmp/v6kn/bg`, `/var/tmp/v6kn/best`);
   - khung PNG (`sx`, `sxA`, `tn`, `klai`);
   - ảnh và bản ghi O2 / chấm mù (`/var/tmp/v6kn/ngoai-anh`).
6. **RIGHTS** (P ghi): người tự dựng (mã Cine Lab, không tài sản ngoài); công cụ `scikit-image`, `opencolorio` (BSD-3, chỉ chạy, không vào phim); ảnh C 1943 lần 3 ở diện "chỉ nghiên cứu" như lần 2.
