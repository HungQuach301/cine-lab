# P-2010 · Tra nguồn thảm thực vật 1779–83 (căn cứ cho NC-D5 "bụi trước 1900 = 0,45 × hiện nay")

## Nguồn và kiểm SHA
Tệp djvu gốc của T3b (`/var/tmp/cine-out/t3b/a2/`) không còn trong container. P-2010 tải lại đúng URL đã đăng ký trong `channel-k2/k2c-t3-01/vay-ham/claims-vay-ham.json` (`nguon_da_tai`) ngày 20/10/2026, UA "CineLab-research (+https://github.com/HungQuach301/cine-lab)". **SHA-256 khớp đăng ký 5/5**, nên đây đúng là các tệp T3b đã dùng. Tệp để ngoài git: `/var/tmp/cine-out/p2010/nguon/`.

| Nguồn | URL (archive.org djvu.txt) | SHA-256 đăng ký = tải lại |
|---|---|---|
| Drinkwater, *A History of the Late Siege of Gibraltar*, Dublin 1786 | historyoflatesie00driniala | `7576bb8fb645db341cbf981383d7d41efae91fce1c9991737e21be4d04565212` |
| Drinkwater, London 1785 (đối chiếu) | bim_eighteenth-century_a-history-of-the-late-si_drinkwater-john_1785 | `d55e8ebf…` (16 ký tự đầu khớp; bản đăng ký ghi thiếu đuôi) |
| Drinkwater 1905 | historysiegegibr00drin | `9a0c3c3e45f39e2fdbb46de1b92aef6d61d1d8b5100e170d4dcf60c86eb42709` |
| Spilsbury, *A Journal of the Siege of Gibraltar* (bản 1908) | ajournalsiegegi00spilgoog | `f6c2f3a940cde7ac88eb6745421b458f1f8c764c4a8affef42a784c54699dc1f` |
| Ancell, *A Circumstantial Journal…* 1784 | acircumstantial00ancegoog | `67d61d0aced585978cd08b34717ca985699b3dc7e32d01014f974d1fe488b526` |

Từ khoá đã quét (kể cả chữ s dài OCR "f"): brush, bushes/bufhes, shrub/fhrub, palmetto, fuel/fewel, fire-wood, verdure, herbage, barren, faggot, fascine/fafcine, garden, vegetable, green, underwood, thicket, heath, furze, "cut down", "wood for".

## Trích nguyên văn (OCR giữ nguyên chính tả, chỉ nối dòng)
Kiểm bằng máy: `reports/p2010/kiem_trich.py` — **22/22 đoạn trích khớp nguyên văn** tệp có SHA (chuẩn hoá khoảng trắng; "…" và " / " tách đoạn). Trang Drinkwater lấy từ đầu trang chạy trong OCR ("SIEGE OF GIBRALTAR. 49" / "50 HISTORY OF THE LATE"). Trang Spilsbury là số trang đứng riêng gần nhất trong OCR (bản 1908); năm theo trình tự nhật ký.

| # | Nguồn · trang · ngày | Dòng OCR | Trích | Nói gì về thực vật |
|---|---|---|---|---|
| 1 | Drinkwater 1786, tr. 49–50 (mô tả Rock trước vây) | 2860–2880 | "The appearance of the rock is barren and forbidding ; as few trees or (hrubs, excepting palmettos, are to be feen on the face of the hill: yet it is not entirely deilitute of vege- / tation ; wild herbs, of different kinds, fpring up in the interfaces of the rocks, when the periodical rains fet in … When they ceafe, and the powerful rays of the fun have wither- ed the little verdure that appeared on the hill, nothing offers to the eye but fharp uncouth rocks, and dried palmetto bufhes." | **Mặt núi trơ, rất ít cây/bụi, chủ yếu cọ lùn (palmetto)**; cỏ dại theo mùa mưa (9–10 → 4–5), mùa khô chỉ còn đá và bụi cọ khô; dê, cừu, bò gặm trên núi |
| 2 | Drinkwater 1786, tr. 50 | 2880–2884 | "The foil collected in the low ground , is however ex- tremely ricrl and fertile, producing variety of fruits and vegetables." | đất trũng thì màu mỡ, có vườn |
| 3 | Drinkwater 1786, tr. 50 | 2890–2896 | "The garrifon, before the blockade of 1779, was chiefly fupplied with roots and garden- fluff from the gardens on the neutral ground, which,, being on a flat, could almoft con- ffontly (even in fummer) be kept in a ftate of vegetation. The proprietors of thefc gar- dens were obliged totally to relinquifh them when the Spaniards erected their advanced works" | **eo đất (neutral ground): vườn rau xanh quanh năm trước 1779**, bị bỏ khi TBN dựng công sự tiền tiêu |
| 4 | Drinkwater 1786, tr. 79 (8/1779) | 4095–4097 | "Parties were likewife detached to colled fhrubs, &c. from the face of the hill, for fafcines" | quân đồn cắt bụi trên mặt núi làm bó cành |
| 5 | Drinkwater 1786, tr. 105 (12/1779) | 5112–5113 | "the party employed in cutting brufh-wood for fafcines" | cắt bụi tiếp tục |
| 6 | Drinkwater 1786, tr. 106 (1780) | 5143–5149 | "a vail quantity of wood, cork, &c. was floating under our walls … Fuel had long been a fcarce article : this fup- ply.was therefore confidered as a miraculous interference of Providence in our favour." | **củi khan hiếm** — Rock không tự cấp được củi |
| 7 | Drinkwater 1786, ≈ tr. 111 (OCR "m") (1/1780) | 5426–5427 | "a party employed behind the Rock in gathering fhrubs, &c. forfafcines" | cắt bụi cả ở mặt sau (đông) Rock |
| 8 | Drinkwater 1786, tr. 141 (6/1780) | 6520–6525 | "The hulls of the fire-fhips were foon after broke up and fold to the inhabitants for fewel, and proved a moft feafonable relief. Firing was become a more important article than before" | củi khan hiếm (đốt cả thân tàu lửa) |
| 9 | Drinkwater 1786, tr. 134 (1780) | 6241–6243 | "their camp they were bufy, collecting brufh- wood for fafcines" | phía TBN cũng cắt bụi làm bó cành |
| 10 | Spilsbury, ≈ tr. 2 (27/9/1779) | 757–758 | "She attends the boat that goes for thorns, &c., to the back of the Rock, to make fascines." | lấy cây gai ở mặt sau Rock |
| 11 | Spilsbury, ≈ tr. 10 (8/11/1779; dấu năm OCR gần nhất ghi "1778") | 982–983 | "The Governor seems desirous to have as many gardens made as possible." | thống đốc khuyến khích làm vườn trong đồn |
| 12 | Spilsbury, ≈ tr. 21 (1/10/1780) | 1590–1591 | "the Dons erected the first of the Mill Battery, and set fire to the huts and canes in the gardens" | vườn (có lau sậy) ngoài Land-port bị đốt |
| 13 | Spilsbury, ≈ tr. 26 (8/2/1781) | 1897–1898 | "Bread, flour and fuel are very scarce ; wood sells by the pound, The back of the Rock under the Signal House 1s scalping 3 to prevent desertion." | **củi bán theo cân**; mặt sau Rock dưới Signal House bị **"scalping"** (cạo trọc) để chống đào ngũ |
| 14 | Ancell 1784, tr. 40–41 (thư 29/3/1780) | 1782–1797 | "Our barren rock yields but little, but as neeeflity generally ftrikes out a reme- dy, many have begun to endeavour to con- vert the folid parts; of the rock into kitchen gardens, which fome have efFe&ed by raifing walls one height above another, and filling the enclofed with earth. … beholds the face of the dry and barren rock … in a ftatc of vegetation" | "**barren rock**"; vườn bậc thang đắp đất trên đá |
| 15 | Ancell 1784, tr. 67 (30/11/1780) | 3650–3652 | "to vifit the Common, at the foot of St. … Roque, to clear tfae ground of marquees, … tents, huts and fheds, and to let nothing re- main but the herbage for the cattle." | phía TBN (đồng cỏ chân San Roque) |

Tranh/bản khắc PD trong repo (`channel-k2/k2c-t3-01/vay-ham/ref/`, 39/39 SHA khớp `tai-san-vay-ham.json`; bản xem trước ≈ 1600 px): hai bản khắc Drinkwater 1786 ("A View of the Grand Attack… Sept 13th 1782", SHA `7d261631…`; "A View from Gibraltar of the Spanish Batteries", SHA `863acf59…`) cho sườn Rock nét mảnh không ký hiệu cây/bụi, eo đất trống trừ ô vườn/ruộng rào; quạt vẽ Met 209515 (≈ 1782) tô sườn tây xanh rải cây nhưng địa hình tưởng tượng (độ tin thấp); Faden 1781 có ô vườn trên eo đất (nhãn đọc chưa chắc).

## Kết luận
- **Hướng: 1782 THƯA HƠN hiện nay** ở mặt núi. Căn cứ **bậc 2** (văn bản thời đó, ba người chứng độc lập: Drinkwater, Ancell, Spilsbury): mặt núi "barren", "few trees or shrubs, excepting palmettos"; trong vây còn bị cắt bụi làm bó cành (1779–80), cạo trọc mặt sau dưới Signal House (2/1781), củi khan hiếm tới mức bán theo cân. Bậc 4 (hai bản khắc Drinkwater) cùng hướng, nhưng cùng tác giả nên chưa đạt đối chiếu chéo độc lập.
- **Mùa:** mùa mưa (9–10 → 4–5) có cỏ dại xanh giữa khe đá; mùa khô chỉ đá + bụi cọ khô. Cuộc tấn công lớn 13/9/1782 rơi vào cuối mùa khô → sườn núi nâu/khô.
- **Eo đất:** vườn rau xanh quanh năm trước 1779 (bậc 2), bị bỏ khi TBN dựng công sự; vườn ngoài Land-port bị đốt 10/1780. Năm 1782 → đất trống/vườn hoang, không phải bụi rậm.
- **Con số 0,45:** nguồn cho HƯỚNG (thưa hơn) ở bậc 2 nhưng **không cho tỉ lệ**. Nguồn còn gợi ý mặt núi 1782 có thể thưa hơn 0,45 (gần trơ, chỉ cọ lùn), song không đo được. Mật độ "hiện nay" làm mốc so sánh cũng chưa có nguồn trong repo.
- **Đề xuất (chờ chủ dự án):** giữ hệ số **0,45 TẠM**, ghi căn cứ "**hướng: bậc 2** (Drinkwater 1786 tr. 49–50; Ancell 1784 tr. 40–41; Spilsbury 8/2/1781); **giá trị: bậc 5**". Thêm hai ràng buộc có nguồn cho phiên dựng: (a) loài bụi chủ đạo trên mặt núi là cọ lùn (palmetto), không phải cây gỗ; (b) mốc 9/1782 dùng tông khô (cỏ úa). Muốn nâng giá trị lên bậc 4 cần một tranh/bản khắc thời đó độc lập với Drinkwater nhìn rõ sườn tây, và ảnh gốc độ phân giải đầy đủ (ngoài git).
