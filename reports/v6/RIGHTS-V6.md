# V6 — bổ sung RIGHTS (đề nghị phiên P chép vào `RIGHTS.md`; phiên xưởng không sửa RIGHTS.md gốc)

| Tài sản | Nguồn | Giấy phép | Phạm vi dùng trong V6 | SHA-256 (16) tệp gốc |
|---|---|---|---|---|
| Bản đồ "Plan of the Town and Fortifications of Gibraltar" trong J. Drinkwater, *A History of the Late Siege of Gibraltar* (London, 1786), tờ 373 | Internet Archive `historyoflatesie00drin` (jp2 tờ 0373) | Phạm vi công cộng (PD, in 1786) | Chỉ dùng làm **dữ kiện**: vùng chữ "THE RUINS OF GIBRALTAR" → đa giác vùng đổ nát 1782 (`design/k2v/tl/data/ruins-zone-1782.json`, khớp affine, sai số tối đa 0,02 m). Không đưa ảnh lên hình. | e3a2e3b0181f14f3 |
| Bản khắc pin nổi (floating batteries) 1782, Rijksmuseum RP-P-OB-19.249 | iiif.micr.io/saQvn | CC0 1.0 | Tham chiếu hình dạng pin nổi (mái nghiêng chống đạn, hai tầng pháo, cột buồm thấp) cho `ships6.js`; không đưa ảnh lên hình. | 3fb24fc6210b9c80 |
| Bản đồ pháp tuyến Poly Haven: painted_plaster_wall, old_stone_wall, stony_dirt_path (2k, `_nor`) | polyhaven.com (đã có từ PT4, `reports/pt/giay-phep/polyhaven-files.json`) | CC0 1.0 | Vi chi tiết bóng đổ trong lượt ánh sáng Cycles của bản TỐT NHẤT (tường vữa, đá công sự, đất). | 2d601a46ed5ce2af · 962f9ab9966a8c2b · 6e0ee32808d6ae09 |
| Vân chi tiết HC7 King's Bastion (`design/k2v/tl/data/hc7-kb-detail.jpg`) | Tách từ khối AI PT3 đã duyệt (Q-PT3-1; quy trình 5 điểm PT3 §9); D = I/Gσ(I), σ = 1 m | Theo §11.3 + Q-PT3-1 (chỉ bề mặt đá công sự) | Chỉ mặt tường escarp King's Bastion; khung có vân mang `ai_texture: true` + nhãn "Surface detail AI-assisted · layout, landmarks & flags from sources" ≥ 38 px dưới-trái suốt shot. | xem reports/v6/hc7/hc7-kb-nuong.json |

## Quân phục 1782 (vật mang dữ kiện — lớp (a) Q-PT4-3)
Bảng màu trong `design/k2v/tl/people.js` (UNIFORMS):
- **Bộ binh Anh**: áo đỏ, gi-lê/quần trắng ngà, ghệt đen, dây đeo trắng. Nguồn: Royal Warrant 1768; tranh J. S. Copley *The Siege and Relief of Gibraltar* (1783–91, PD).
- **Pháo binh Hoàng gia**: áo lam đậm viền đỏ. Nguồn: Royal Warrant 1768.
- **Bộ binh Tây Ban Nha**: áo trắng. Nguồn: Reglamento 1768; Clonard, *Historia orgánica…* (1851–62, bản khắc PD). Màu viền theo từng khối là **minh hoạ**.
- **Bộ binh Pháp**: áo trắng (Règlement 1779). Màu viền là **minh hoạ**.
- **Dân thường, phụ nữ, thuỷ thủ**: tông vải tự nhiên, **minh hoạ**.

Không sao chép thiết kế nhân vật, nhạc hay IP của phim tham chiếu. Không thêm nhạc hay SFX mới ở V6; đoạn thử dùng lại nhạc "Tyrant" đã có trong RIGHTS.md.
