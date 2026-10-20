# K2C-T3-01 Gibraltar — mô tả YouTube v2, bình luận ghim v2, thẻ phương pháp v2 (ĐÓNG-GÓI-T3, 19/10/2026; chờ chủ dự án duyệt ở G2)

> **Thay cho** `nguon-mo-ta.md`, bản G1b ngày 18/10, theo lời v4.1. Tệp cũ giữ nguyên, không sửa.
>
> **Căn cứ**
> - Lời khoá **v4.2** (`loi-khoa.txt` `51d1c773…`, nhánh `origin/k2c-t3-kl42`). v4.2 chỉ khác v4.1 ở D11: dời ‹2o›/‹2p›, thêm câu nối. Vì vậy danh mục nguồn không đổi.
> - Kinh thánh §5, §10.6 (câu minh bạch **đã sửa**: "on two street frames"), §12.1 và §13.6 TL-4. TL-4 nói rằng số liệu và câu trích không lên hình, mà do lời + phụ đề CC + mô tả mang.
> - V7P §3: trại vây hãm số hoá từ Faden 1783.
>
> **Độ dài** (Python `len`):
> - Mô tả: **4 048** ký tự. Giới hạn YouTube là 5 000, và mô tả không chứa `<` hoặc `>`.
> - Bình luận ghim: **1 239**.
> - Trả lời (1) sửa: **492**.
> - Các trả lời (2)–(4) và danh mục nguồn 1/5–5/5 dùng nguyên văn `nguon-mo-ta.md` §3.2 và §4. Lý do: nguồn không đổi giữa v4.1 và v4.2.

## 1. Ghi chú cho người đăng
1. **Khai báo AI:** Attributes → **"AI use" = Yes** (P10C-2). Lý do: tệp ảnh sửa bằng AI mang **C2PA Content Credentials**, và trang chính sách (support.google.com/youtube/answer/14328491) viết YouTube **"may"** tự gắn nhãn. Mô tả vì thế giữ chữ "may label". Kiểm lại trang này mỗi lần đăng.
2. **Chương:** timestamp để `‹--:--›`, **điền sau khi dựng xong**. Chương đầu phải là `0:00`, có ≥ 3 chương, mỗi chương ≥ 10 giây. Tên chương lấy từ lời v4.2.
3. **Dòng 1 theo tiêu đề đã chốt** (Kinh thánh §5: câu hỏi tiêu đề + một sự thật):
   - Nếu chốt tiêu đề CHÍNH hoặc THỬ 2: giữ dòng 1 như bản dưới ("Fourteen sieges between 1309 and 1783…").
   - Nếu chốt THỬ 3 (nay theo khuôn §14.5 "Gibraltar: <lời hứa> | 3D Timelapse"; tên làm việc cũ đã bỏ 20/10 22:34): dòng 1 viết lại theo lời hứa đã chốt; bản cũ để tham khảo: *"Why was one small rock besieged fourteen times, between 1309 and 1783? Today you walk in from Spain across an airport runway."* Mô tả sẽ tăng thêm khoảng 40 ký tự, vẫn dưới 5 000.
4. **TL-4: số và câu trích chuyển từ hình sang mô tả.** Mọi thẻ `[TRÊN HÌNH]` của script v4.2 mang số hoặc câu trích nay nằm ở hai khối "QUOTED IN THE FILM" và "NUMBERS, AND WHO COUNTED":
   - Montero, Sayer, Gómez Nadal, Marquina Barrio;
   - số đạn Drinkwater;
   - số thương vong 13–14/9/1782;
   - Montero cả cuộc vây;
   - đường hầm 55 km;
   - lịch mới/cũ năm 1704.

   Bốn câu trích mô tả **chưa đưa vào**, vì mô tả sẽ vượt khoảng 4 800 ký tự: Montero «con cien hombres…», Montero «San Roque», Fernández Duro «50 navios», Conseil 1785. Các câu này **chuyển sang trả lời 6/6** dưới bình luận ghim (§4 dưới).
5. **Lỗi đã sửa so với bản cũ:** trả lời ghim (1) của `nguon-mo-ta.md` viết García Sanz "counts differently". Claim **S006** lại ghi bà dùng **cùng hệ đếm** với sử Anh (1704 là lần thứ mười một). Bản v2 sửa cho đúng claim.
6. **Phụ thuộc V7:** dòng "Siege camps…" và từ "3D timelapse" trong dòng 1 chỉ đúng khi bản dựng theo V7 (trại Faden, timelapse là xương sống). Nếu không duyệt V7, bỏ dòng "Siege camps…" và đổi "This 3D timelapse" thành "This history explainer".
7. **Đọc lại C02 và C26** ngay trước khi đăng (như bản cũ §1 điểm 3).

## 2. MÔ TẢ YouTube v2 (dán nguyên khối)
```text
Fourteen sieges between 1309 and 1783, and today you walk in from Spain across an airport runway. This 3D timelapse tells Gibraltar's story from British and Spanish records side by side: every date sourced; where the two sides' numbers differ, we give both and say who counted.

Facts as of 18 October 2026. The UK–EU treaty is in force only provisionally.

CHAPTERS
‹--:--› Midnight at the Gate
‹--:--› 1704: A Rock Changes Hands
‹--:--› The Great Siege
‹--:--› The Neutral Ground
‹--:--› A Runway on the Isthmus
‹--:--› The Gate

QUOTED IN THE FILM (original, our translation)
• Montero (1860): «la preciosa llave del Mediterráneo», "the precious key of the Mediterranean"; Sayer (1862): "the key of the Mediterranean".
• Philip V's order, 8 Oct 1730 (Gómez Nadal, Almoraima 48): «bloquear definitivamente la correspondencia y paso a la plaza por tierra», "to block, once and for all, all contact with and passage to the town by land".
• Montero on the 1779 blockade: «privar a la plaza de los viveres que le llegaban de las costas de África», "depriving the town of the food that reached it from the coasts of Africa".
• Montero on 13 Sept 1782: «á las diez y veinte y cinco minutos de la mañana … rompieron á un tiempo el fuego», "at twenty-five past ten in the morning … opened fire all at once".
• Spain to its London ambassador, 4 Mar 1939 (Marquina Barrio, 1981): «una porción usurpada del territorio nacional», "a usurped portion of the national territory".

NUMBERS, AND WHO COUNTED
• 14 sieges, 1309–1783: Sayer (1862) and the Gibraltar National Museum; García Sanz (2022) uses the same numbering (1704 is the eleventh).
• 4 Aug 1704 is the new-calendar date; English histories give 24 July (old calendar).
• Rounds fired from April 1781 (Drinkwater): garrison 205,328; besiegers 258,387.
• 13–14 Sept 1782: over 2,000 attackers lost, prisoners included (a British estimate and Montero); 185 hit by gunfire before the fires (French account, 1785); 357 rescued (British return); garrison 16 killed (its own return).
• Whole siege: Montero, about 2,000 defenders and 6,000 besiegers lost from all causes; garrison return (Drinkwater), 333 killed or died of wounds and 536 died of sickness (scurvy deaths of 1779–80 not included).
• Tunnels: about 55 km (HM Government of Gibraltar, 2017; UK Hansard, 2015).

WHAT IS ESTIMATED
• 1782 town: blocks follow Drinkwater's 1786 plan; ruined houses inside "The Ruins of Gibraltar" and unmapped blocks are our estimate, as are the dates they fall.
• Siege camps: placed from Faden's 1783 plan (to about 250 m); tent numbers and the days they go up are estimates.
• Building and church-tower heights; the 1782 coastline (today's is shown); map borders and sea routes; street-lamp style.
• Troops, crowds, ships at anchor, flag positions, shot furnaces, uniform facings and civilian clothing: illustrative.

HOW AI WAS USED
• Two street frames (1782, 1943): walls, roofs and ground AI-retouched under a mask; layout, landmarks, flags, people and light come from our sourced 3D render. King's Bastion: AI stone detail on one wall.
• AI helped read the 1782 diaries; every extract was matched word for word to the source and checked by a second model.
• AI created no facts: no position, building, flag, uniform, date or number.
• The AI-edited images carry C2PA Content Credentials, so YouTube may label this video as altered or synthetic; we also disclosed AI use at upload.

Full sources, with pages and archive links, are in the replies to the pinned comment. © OpenStreetMap contributors (ODbL). Buildings, La Línea: Dirección General del Catastro. Cliopatria (Seshat Global History Databank), CC BY 4.0. OpenHistoricalMap contributors; CNIG/IGN, CC BY 4.0. Contains Parliamentary information licensed under the Open Parliament Licence v3.0.

Narration: synthetic voice. Visuals: 3D reconstructions built from the cited sources and registers; on two street frames, surface detail is AI-assisted — layout, landmarks and flags come from the sources. Historical images: public domain / CC0, credited.
```

## 3. BÌNH LUẬN GHIM v2
```text
How this film was made — sources, estimates, AI

Main sources: Drinkwater's history of the siege and his 1786 plan of the town; Faden's 1783 plan of the bay; the garrison diaries of Spilsbury and Ancell; Montero, Historia de Gibraltar (1860); Sayer, History of Gibraltar (1862); García Sanz, Historia de Gibraltar (2022); the Treaty of Utrecht (1713), Art. X; Marquina Barrio (1981) on the airstrip; UK Hansard; HM Government of Gibraltar; UK FCDO; INE (Spain). Every source, with pages and archive links, is in the replies below.

Estimated: the ruined 1782 houses and the days they fall; the siege camps' tents (placed from Faden's plan); building heights; the 1782 coastline (today's is shown); map borders and sea routes; the number and layout of troops, crowds and ships (illustrative).

AI: on two street frames, walls, roofs and ground were AI-retouched under a mask; King's Bastion's wall carries AI stone detail. AI also helped read the 1782 diaries, and every quote was checked word for word against the original. AI added no facts. The narration is a synthetic voice. The AI images carry C2PA credentials, so YouTube may label the video.

Facts as of 18 October 2026. Spotted an error? Reply with your source and we'll check it.
```

### 3.1 Trả lời (1) — bản sửa (thay bản trong `nguon-mo-ta.md` §3.2)
```text
Fourteen sieges? It depends on how you count. Sayer's History of Gibraltar (1862) and the Gibraltar National Museum count fourteen, from the Castilian capture of 1309 to the Great Siege of 1779–83; both 1333 sieges count, and the 1704 capture and the 1704–05 counter-siege count as two. A modern Spanish history (García Sanz, 2022) uses the same numbering: it calls the 1704 attack the eleventh siege. Some lists reach fifteen by adding the 1969–85 border closure; we kept to military sieges.
```
Trả lời (2)–(4): giữ nguyên văn `nguon-mo-ta.md` §3.2.

## 4. Danh mục nguồn: 5 phần giữ nguyên `nguon-mo-ta.md` §4, thêm phần 6/6
- Phần 5/5 thêm một dòng: "• W. Faden, Plan of the bay, rock and town of Gibraltar (1783) — siege camps digitised from this plan — Yale University Library 2046612, PD". Dòng Faden đã có sẵn; chỉ thêm cụm "siege camps digitised from this plan".
```text
Sources 6/6 — Further quotes from the film's sources
• Montero (1860) on the 1704 garrison: «con cien hombres de guarnición … no había artilleros que las sirvieran», "a garrison of a hundred men … there were no gunners to serve them".
• Montero on 1704: «se habia acampado en las haciendas cercanas á la ermita de San Roque», "had camped on the farms near the hermitage of San Roque".
• Fernández Duro, Armada española VII (1901): «alegrando la vista los 50 navios que se juntaron en Algeciras», "the 50 ships of the line that gathered at Algeciras, a joy to see".
• Conseil de guerre privé (1785): «l'expérience que l'inventeur avoit demandée … à l'épreuve des boulets rouges», "the test the inventor had asked for … against red-hot shot".
• Montero on 1779: «Carlos III declaró la guerra á Inglaterra y se unió á Francia», "Charles III declared war on England and joined France".
• Gómez de Avellaneda (2022) on 1810: «con autorización española, fueran destruidos por los ingleses», "with Spanish authorisation, they were destroyed by the British" (Montero gives 1811).
• García Sanz (2022): «el progresivo avance de la frontera sobre la zona neutral», "the gradual advance of the frontier over the neutral zone"; on 1908: «como acto de cortesía», "as an act of courtesy".
• Marquina Barrio (1981): «no queda constancia de reclamaciones por el uso de la pista», "there is no record of complaints over the use of the strip".
```

## 5. Thẻ "How this film was made" (2 × ≈ 8 s) — `the-phuong-phap-v2.json`
| Thẻ | Dòng | Từ |
|---|---|---|
| 1/2 | Built from British and Spanish records and period maps. · Every source, with pages: description and pinned comment. · Estimated: 1782 ruins, camps, heights, coastline, borders. | 24 |
| 2/2 | Troops, crowds and ships: illustrative in number and layout. · AI retouched two street frames and read diaries; it added no facts. · Narration: synthetic voice. | 24 |

- **Sát ngưỡng (nêu tên theo luật cứng):** mỗi thẻ đúng 3,0 từ/giây ở 8 s, chạm trần 3 từ/giây.
- Nếu bản dựng cho được ≥ 9 s mỗi thẻ thì đạt dư.
