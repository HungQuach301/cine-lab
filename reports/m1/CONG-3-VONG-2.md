# CỔNG 3 — THIẾT KẾ · vòng 2 (nhân vật) · "Last Round"

Phiên P, 27/09/2026. Nhánh `claude/cine-lab-m1-cong3-v2`, tạo từ `main` sau khi merge vòng 1 và `checks/v1.3` (`lock.py --verify`: **KHỚP** `144b3cff…0294`).
Mọi số dưới đây là **đo thật, tuần tự trên máy rỗi**, 1920×1080, 8 mẫu (thiết lập sản xuất). Đây là **đề xuất của Claude, chưa duyệt**.

## 0. Tóm tắt
- Hai cách làm nhân vật, **cùng bối cảnh C, cùng ánh sáng, cùng máy quay** (P dựng sẵn 4 shot; mỗi cách chỉ thay module nhân vật, cùng API và khung xương).
- **Cả hai sửa được lỗi lớn nhất của vòng 1** ở mức "đọc được": Ida nay đọc là **"adult woman"** (vòng 1 là "đàn ông"); mặt có cấu trúc; tay có ngón; bóng chim có cánh.
- **C2 silhouette: 3D 85%, 2D 90%** (chấm chặt, tính ½ là sai: cả hai 80%). Chưa chắc qua mức 90%. Vẫn trượt: "hơ tay trên thang" (đọc thành "chăm đèn"), và chim bóng khi chỉ nhìn silhouette.
- **Luật máy trên shot chuyển động (96 khung): cả hai ĐẠT G3, G3b, N1, N2.** Lớp vẽ **không nhấp nháy đo được**.
- **Ngân sách ≤ 5 s/khung: vượt ở cận mặt (7,1–9,9 s) và shot đi bộ (6,8–7,4 s).** Phần lớn chi phí thuộc bộ cảnh chung (2 đèn khí có bóng + lớp vẽ), không phải nhân vật.
- **Cảnh 5 khung rộng: viền sáng đã thêm nhưng còn yếu**; người vẫn gần hoà vào bóng khi xem ở cỡ nhỏ.

## 1. Việc P đã làm
| Việc | File |
|---|---|
| Hợp nhất vòng 1 + checks v1.3 vào main; nhánh mới | — |
| Ghi quyết định Cổng 3 v1, đóng Cổng 1–2 | `AUTHORSHIP.md`, `reports/m1/DONG-CONG-1-2.md` |
| Luật thế giới v0.3 (5A nắp đèn lồng) | `bible/world-rules.md` |
| Hạ tầng: chu kỳ đi (sin, không tuyến tính), cột đèn khí, sào mồi, driver chuỗi khung, phơi sáng theo shot | `shared/anim.js`, `shared/props.js`, `shared/render_seq.js`, `shared/post.js` |
| 4 shot chung hướng C | `v2/shots.js` (a, b, walk), `v2/s5.js` (c: thêm dội ấm từ 2 vách bên để làm viền sáng; 5A), `v2/page.js` |
| Tư thế C2 mới (thắp đèn, cầm đèn lồng, hơ tay trên thang, đứng nhìn), dàn đạo cụ theo ngữ cảnh, khung tự canh | `model-sheet/*.json`, `model-sheet/sheet_page.js` |
| Hồ sơ nhân vật C1 | `bible/characters.md` |
| Đo nhấp nháy lớp vẽ | `v2/flicker.py` |
| **Sửa lỗi dấu `spread`** trong `shared/cast.js`: "xoè" ngón thực chất là khép. Agent 3D phát hiện; đây là nguyên nhân chính khiến cánh chim bóng vòng 1 thành que | `shared/cast.js` |
| Bài học vòng chờ tự khớp (`pgrep -f` khớp chính nó) | `reports/m1/BAI-HOC-VONG-CHO.md` |

## 2. Hai cách (2 subagent song song; P render chính thức tuần tự)
- **(1) 3D nâng cấp** (`v2/char3d/`): lưới điêu khắc liền; tay áo, chân, váy là ống uốn qua khớp; mặt có hốc mắt, gò má, nếp nhăn; ngón 3 đốt; khăn len, váy dài, búi xoắn; Cas có tai vểnh và tóc lộ gáy.
- **(2) Tranh 2D có khung xương** (`v2/char2d/`): tranh sinh bằng mã theo lớp bộ phận, gắn vào cùng khung xương, quay về máy quay. Đầu và thân vẽ lại theo góc nhìn (bước 4°/6°). Có normal map để đèn của cảnh chiếu lên. Thân 3D gốc làm vật đổ bóng vô hình, nên bóng đúng hình người.
- **Cả hai phóng to tay:** Cas 1,30× (đúng trần cho phép, **nằm trong vùng ±5%**), Ida 1,15×. 3D phóng búi 1,3×. 2D thêm nơ nhỏ trên băng mũ. **Tất cả chờ chủ dự án duyệt.**

## 3. Số đo
### Thời gian render (giây/khung, 1920×1080, 8 mẫu, tuần tự máy rỗi; ngân sách ≤ 5 s)
| Shot | 3D | 2D | Ghi chú |
|---|---|---|---|
| a · cận mặt Ida | **9,92** ✗ | **7,14** ✗ | Cận cảnh: bóng đèn khí 2048², DOF |
| b · Cas chim bóng | **5,13** ✗ (**trong ±5%**) | 4,40 ✓ | |
| c · cảnh 5 khung rộng | 4,12 ✓ | 3,77 ✓ | |
| walk (trung vị 96 khung) | **7,36** ✗ | **6,84** ✗ | Không lớp vẽ: 6,13 / 5,74 → lớp vẽ tốn khoảng 1,1–1,2 s |

Thời gian dựng cảnh (một lần mỗi shot) không tính. Agent 2D đo nhân vật gốc (khối nguyên thuỷ) cùng lúc: cùng cỡ với 2D. Phần vượt ngân sách chủ yếu do **2 đèn điểm có bóng (6 lượt cube × 8 mẫu) + lớp vẽ**, không do nhân vật.

### Luật máy trên shot đi bộ (`checks/run.py --profile shot`, 96 khung, x264 30 Mbps; báo cáo: `v2/out/v2/<3d|2d>/check/`)
| | N1 | N2 luma ngoài dải | G3 banding | G3b |
|---|---|---|---|---|
| 3D | ĐẠT | ĐẠT 0,1347% | ĐẠT 0% | ĐẠT: σ 1,328; CV 0,055; max/min 1,00; tương quan khung kề 0,209 |
| 2D | ĐẠT | ĐẠT 0,1327% | ĐẠT 0% | ĐẠT: σ 1,318; CV 0,054; max/min 1,00; tương quan 0,207 |

Chỉ số trong ±5% quanh ngưỡng (theo máy): **không có**.

### Nhấp nháy lớp vẽ (máy tĩnh, 24 khung, so với cùng shot không lớp vẽ; `v2/out/v2/*/flicker.json`)
| | ΔL trung bình, điểm tĩnh (mã 8 bit) | Tỷ lệ điểm tĩnh đổi > 2 mã | ΔL cả khung |
|---|---|---|---|
| 3D có lớp vẽ / không | 0,272 / 0,245 | 0,18% / 0% | 1,071 / 1,079 |
| 2D có lớp vẽ / không | 0,269 / 0,245 | 0,15% / 0% | 1,068 / 1,076 |

Lớp vẽ chỉ thêm khoảng 0,025 mã trên điểm tĩnh, không nhìn thấy. Xem 4 khung liên tiếp quanh nhân vật: không thấy vệt nhiễu trôi. **Giới hạn:** Ida đi ngược sáng nên nhân vật gần như là silhouette. Shot này chưa thử được lớp vẽ trên **mặt** đang chuyển động (máy lia, cận cảnh). Cách 2D đổi tranh mỗi 4° góc nhìn: không thấy nhảy trong shot đi bộ, nhưng sẽ lộ khi đầu quay nhanh ở cận cảnh (agent 2D tự nêu).

### Silhouette C2 (kiểm mù: agent không biết dự án, xem 10 silhouette không nhãn, trộn thứ tự; `v2/out/v2/*/C2-silhouettes-*.png`, khoá `v2/out/v2/*/c2/blind-key.json`)
| | Hành động đúng | Chấm chặt | Giới tính / tuổi |
|---|---|---|---|
| Vòng 1 (nhân vật cũ, 2 lượt) | 85% | 80% | Ida đọc là "đàn ông", Cas là "bé gái búi tóc" |
| **3D** | **85%** | 80% | Ida **"adult woman"** ✓; Cas vẫn "búi tóc" |
| **2D** | **90%** (**trong ±5% quanh ngưỡng**) | 80% | Ida **"adult woman, long skirt"** ✓; Cas vẫn "búi tóc" |

Còn trượt ở cả hai: "hơ tay trên thang" (đọc là "chăm/thắp đèn": hành động gần đúng nghề, sai ý), và chim bóng khi chỉ có silhouette (3D: "giơ tay"; 2D: "đổ bóng hình quái vật trên tường"). Ở khung phim b, bóng chim đọc tốt hơn nhiều vì có tường và ánh sáng thật.

## 4. Tự chấm theo `checks/RUBRIC.md` (P tự chấm; không thay người chấm L2)
| Mã | 3D | 2D | Bằng chứng |
|---|---|---|---|
| **C1** Chiều sâu nhân vật | Chưa chấm được trên phim (trần 4) | như 3D | Hồ sơ `bible/characters.md` đủ 4 yếu tố + hành động lặp đầu–cuối (gõ đồng hồ → không gõ; chim bóng tan → chim lớn). C1 phải chấm từ phim (animatic, Cổng 4) |
| **C2** Silhouette | **2**: 85% (chặt 80%) | **3**: 90% sát ngưỡng (chặt 80%) | Mục 3 |
| **D2** Ngôn ngữ hình thống nhất | **3**: khối và ánh sáng hợp bối cảnh; da mặt mịn như sáp, lệch nét cọ của nền (khung a) | **3**: mặt đọc tốt nhưng nét mặt như nét mực minh hoạ, lệch chất sơn của nền (khung a); thân áo loang mượt kiểu CG | Khung a của hai cách |
| **G1** Ánh sáng có nguồn | **3**: nguồn đúng, nhưng mặt Ida gần cháy sáng và tay sáng hơn mặt (khung a) | **4**: mặt là vùng sáng nhất, có chi tiết; bóng chim là chủ thể khung b | Khung a, b |

### Nói thẳng: còn "ma-nơ-canh" ở đâu
- **3D:** da mặt mịn đều như búp bê sáp; miệng cận cảnh gần như "hé răng"; khuỷu và gối xẹp khi gập mạnh, phải lấp khối tròn; mu bàn tay trơn như găng cao su.
- **2D:** thân áo và tay áo là dải loang mượt, nếp vải nghèo; lớp tranh **không nhận bóng đổ** (tay không đổ bóng lên mặt); đổi tranh theo góc 4° có thể lộ khi đầu quay nhanh; váy che một phần đèn lồng ở thắt lưng (khung 45–47 của shot đi bộ).
- **Chung:** ở cảnh 5 khung rộng, nhân vật nhỏ (đầu khoảng 20 px), viền sáng từ vách bên mới làm người sáng hơn bóng một chút. Muốn tách rõ phải có shot gần hơn hoặc bố cục khác.
