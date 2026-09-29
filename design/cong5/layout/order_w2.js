// GÓI W2 — thứ tự + thời lượng shot cảnh 4–6: [id, giây, nguồn]. Chỉ W2 sửa. Đổi id đang được common.js tham chiếu (sự kiện) thì báo P.
export const ORDER_W2 = [
  ['s25', 3.0, 'new'],
  ['s26', 2.0, 'new'],
  ['s27', 3.0, 'new'],
  ['s28', 2.0, 'new'],
  ['s29', 3.0, 'new'],
  ['s30', 2.0, 'new'],
  ['s31', 3.0, 'new'],
  ['s32', 3.0, 'new'],
  ['s33', 5.0, 'new'],   // (a) chủ dự án sau Cổng 5: rút cảnh rộng tĩnh 7,0 → 5,0 s (tổng phim 140,5 s)
  ['s34', 2.0, 'new'],
  ['s35', 4.0, 'new'],
  ['s36', 2.0, 'new'],
  // Cổng 6 (PA1, chủ dự án): tách s37 (93,0–98,8) thành s37 MS nghiêng 90° "That's the last one, then." + nhịp cười buồn (93,0–96,4)
  // và s37b CU nghiêng 90° đẩy chậm "Goodnight, old street." + nhịp cười buồn (96,4–98,8). Giữ id 's37' cho phần đầu (DIALOGUE.L4 = T0.s37). Tổng 5,8 s không đổi.
  ['s37', 3.4, 'new'],
  ['s37b', 2.4, 'new'],
  ['s37w', 2.8, 'new'],
  // (c) Cổng 5 v2 (chủ dự án): câu "Just… keep a little dark for the ones who need it." BẮT ĐẦU trên hình Ida → s39 (Ida CU) trước s38 (Cas).
  // L4 = 93,0 s; lời "Just" từ L4 + 9,33 s = 102,33 (whisper: 9,68); "for" L4 + 12,08 = 105,08; hết câu L4 + 14,00 = 107,00.
  // s39 101,6–106,0 (cả đầu câu trên mặt Ida); cắt sang Cas ở 106,0 = giữa "…ones who need it" (sau "for"); s38 106,0–107,4. Tổng và mốc thoại không đổi.
  ['s39', 4.4, 'new'],
  ['s38', 1.4, 'new'],
  ['s40', 2.6, 'new'],
  ['s40w', 2.0, 'new'],
  ['s41', 1.5, 'new'],
  ['s42a', 2.0, 'new'],
  ['s42b', 2.0, 'new'],
  ['s42', 3.0, 'new'],
  ['s43', 4.0, 'new'],
  ['s44', 2.5, 'new'],
  ['s45', 2.0, 'new'],
  // (d) Cổng 5 v2 (chủ dự án): giờ trên hình CHỈ TIẾN. Bản trước s45c (quảng trường 10:00) → s46 (bỏ túi mở ở 9:53): AI mù đọc "thời gian chạy lùi".
  // Nay s45 (bà xem đồng hồ mình 9:53, rồi ngẩng về phía quảng trường) → s46 (vặn 9:53 → 10:00) → s45c (POV: quảng trường 10:00:00 — khớp giờ bà vừa nhận).
  ['s46', 3.0, 'new'],
  ['s45c', 1.5, 'new'],
  ['s47', 2.0, 'new'],
  ['s48', 5.0, 'new'],
];
