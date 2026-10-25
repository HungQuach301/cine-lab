# Hiệu chuẩn bộ dò mặt YuNet (NHAN-VAT-TEN) — đáp án bằng mắt (K-1.17.7, 25/10/2026)

Mô hình: `checks/models/face_detection_yunet_2023mar.onnx` (SHA `8f2383e4…`, MIT), `cv2.FaceDetectorYN` (OpenCV 5.0, CPU), ngưỡng NMS 0,3.
Dữ liệu: 23 clip M-d animatic T4 v1 (`channel-k2/k2c-t4-02/animatic/omni/clip/<omni/chon>.mp4`, 640×360, 120–192 khung).

## 1. Độ chính xác theo điểm (hộp ≥ 4 % chiều cao khung, mỗi 6 khung — 347 hộp, `crops.json`; tờ `crop-*.jpg` xếp theo điểm giảm dần)
| Điểm ≥ | Số hộp | Hộp > 1/8 khung | Hộp sai (không phải mặt) — soi bằng mắt |
|---|---|---|---|
| 0,85 | 73 | 0 | 0 |
| 0,80 | 121 | 0 | 0 |
| **0,75 (chọn)** | **160** | **0** | **0** (mặt nhìn thẳng/nghiêng, kể cả mặt tối dưới mũ) |
| 0,70 | 184 | 1 | 1 (lửa, 0,73, cao 0,13 khung — H1-10) |
| 0,60 | 232 | 8 | ≥ 5 (lửa/khói/mái cháy 0,63–0,73, cao 0,13–0,19) |
| 0,50 | 347 | 23 | nhiều (khói H4-04b 0,52–0,58 cao 0,52–0,64; lửa H1-02 0,51–0,57 cao 0,30–0,35) |
→ ngưỡng tính **0,75**; 0,60–0,75 có hộp > 1/8 chỉ ra **(w)** cho người soi (`max.jpg`: các hộp lớn nhất ở 0,5–0,73 đều là lửa/khói, trừ mặt nghiêng lính cứu hoả H4-04b 0,61–0,69 cao ≈ 0,12).

## 2. Độ nhạy (bắt/sót) — 8 khung đáp án u = 0,55 (`gt-55-*.jpg`), mặt THẤY ĐƯỢC (không quay lưng) cao ≥ 3,5 % khung
| Clip | Mặt thấy được | Bắt ở ≥ 0,75 | Sót (điểm YuNet) |
|---|---|---|---|
| H2-03c (toà án) | 5 | 5 (0,76–0,86) | 0 |
| H2-03a (đo đất) | 2 | 1 (0,86) | 1 (0,61 — mặt nhỏ ≈ 4 %) |
| H1-10 (xe chạy nạn) | 2 | 0 | 2 (0,54–0,56, ≈ 4 %) |
| H1-17b (trại Moorfields) | 1 | 1 (0,85) | 0 |
| H1-12 (thuyền đêm) | 2 | 1 (0,79) | 1 (0,54) |
| H4-04b (lính cứu hoả, mũ sắt, nghiêng) | 3 | 0 | 3 (0,61 / không bắt) — mặt nghiêng cao ≈ 0,08–0,12 |
| H3-04b (phố 1935) | 0 (quay lưng) | — | — |
| H2-13 (thuyền 1711) | 3 | 0 | 3 (0,51–0,54, ≈ 4 %) |
| **Tổng** | **18** | **8 (44 %)** | **10** — mặt ≤ 6 % khung hoặc nghiêng đội mũ sắt |

## 3. Mặt cận (trên trần 1/8)
- Không clip M-d T4 v1 nào có mặt thật > 1/8 khung (soi tay 69 khung k25/k55/k90 + `max.jpg`); YuNet ≥ 0,75 cũng 0 khung > 1/8 → **0 TRƯỢT oan** trên 23 clip.
- Ca có mặt cận thật (fixture selftest, khung H2-03c-l1 cắt + phóng 640×360): mặt thẩm phán cao **0,236** khung → YuNet **0,89** (bắt); khung rộng hơn: 4 mặt 0,078–0,093 → 0,87–0,89 (ĐẠT, < 1/8).
- Giới hạn: mặt nghiêng đội mũ (H4-04b) điểm 0,61–0,69 — nếu cận > 1/8 sẽ chỉ ra (w), không TRƯỢT → người soi tờ khung (KIEM-2-MUC bắt buộc day_du cho đoạn có nhân vật có tên).
