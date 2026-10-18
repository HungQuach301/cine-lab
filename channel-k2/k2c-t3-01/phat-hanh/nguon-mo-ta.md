# K2C-T3-01 "Why Gibraltar Was Besieged 14 Times": mô tả YouTube, bình luận ghim, danh mục nguồn (chờ chủ dự án duyệt ở G2)

> Phiên con G1b T3, 18/10/2026.
> - **Căn cứ:** lời khoá `script-v4.1-KHOA.md`; claims (`claims-vay-ham.json`, `tienky/claims.json`, `tuyen/claims-tuyen.json`, `g1/claims-g1.json`); `vay-ham/tai-san-vay-ham.json` và `licenses/`; RIGHTS.md (các dòng P1810*, P1810B*, P1810C*); `reports/v6/V6-BAO-CAO.md`, `RIGHTS-V6.md`, `KHUNG-NEO-V6.md`; `design/k2v/tl/layers.js` (chú thích); `tuyen/TUYEN-BAO-CAO.md`; `reports/P-1810c-BAO-CAO.md` §4; Kinh thánh §10.6, §11.3, §12.
> - **Mốc dữ kiện:** Facts as of 18 October 2026. Đọc lại C02 và C26 ngay trước khi đăng (TIEN-KY-VAY-HAM §7.3).
> - **Độ dài** (đếm bằng Python, ký tự Unicode):
>   - mô tả **4 423 ký tự** (4 479 byte UTF-8), dưới giới hạn 5 000;
>   - bình luận ghim **1 207**;
>   - trả lời sẵn 494 / 515 / 553 / 477;
>   - danh mục nguồn đầy đủ: 5 phần, đều ≤ 1 500 (đếm ở §5).
>   - Mô tả không chứa ký tự `<` `>`.
> - Danh mục nguồn **đầy đủ** (trang, mã lưu trữ, giấy phép) dài hơn 5 000 ký tự. Vì vậy mô tả chỉ giữ dạng rút gọn theo chương, và danh mục đầy đủ đăng thành **các trả lời dưới bình luận ghim** (§4). Tệp này là bản gốc.

## 1. Ghi chú cho người đăng (tiếng Việt)

1. **Khai báo AI.** Khi tải lên, vào mục **Attributes**, chọn **"AI use" = Yes** (P10C-2, đã duyệt).
2. **Kiểm lại trang chính sách mỗi lần đăng:** https://support.google.com/youtube/answer/14328491
   - Bản đọc 18/10/2026 (P-1810c §4) có SHA chữ `cdb2e190…`.
   - Nếu trang đổi, báo P trước khi đăng.
   - Trang viết YouTube **"may"** tự gắn nhãn khi tệp có C2PA, và nhãn đó "can not be adjusted". Vì vậy mô tả viết "YouTube may label…", không viết "YouTube labels…". Viết dứt khoát là nói quá trang chính sách.
3. **Đọc lại C02 (kiểm tra biên giới) và C26 (lịch bỏ phiếu Nghị viện châu Âu, 14/12/2026)** ngay trước khi đăng. Nếu đổi, sửa câu "The treaty is in force only provisionally." trong mô tả, và báo P vì lời 5i cũng phải đổi.
4. **Chương (timestamps):** chưa có, vì chưa dựng xong. Khi có bản cuối, thêm khối `0:00 Midnight at the Gate / … 1704: A Rock Changes Hands / … The Great Siege / … The Neutral Ground / … A Runway on the Isthmus / … The Gate` ngay sau đoạn mở. Khối này thêm khoảng 150 ký tự, vẫn dưới 5 000.
5. **Tư liệu hình chưa chốt.** Bảng shot chưa ghim ảnh cụ thể cho các shot "tranh Ken Burns" và "ảnh": 0f, 1b, 2e, 2h, 2l, 2p, 2r, 3e, 3g, 4a, 4h, 5g.
   - Khi dựng xong, mỗi ảnh/tranh **thực dùng** phải có một dòng trong trả lời "Images" (§4, phần 5), lấy từ danh mục chờ chọn ở §6. Tệp nào không lên hình thì xoá dòng đó.
   - Mô tả đã ghi chắc các tư liệu có trong bảng shot và V6: Drinkwater 1786, Faden 1783, Exact Plan 1705, AMS M981 1943, bản khắc pin nổi Rijksmuseum.
6. **Câu minh bạch §10.6** nằm cuối mô tả, **chép nguyên văn** theo lệnh. Câu này **lệch với §12.1**: nó nói "on **marked** street frames", nhưng §12.1 (luật mới nhất, thắng khi trái) đã bỏ nhãn trên hình, nên không còn khung nào "marked". Đề xuất cho chủ dự án quyết:
   - **(A) Giữ nguyên văn §10.6.** Ưu: đúng chữ Kinh thánh. Nhược: người xem tìm "khung có đánh dấu" sẽ không thấy. Đây là sai sự thật nhỏ, rủi ro bị bình luận bắt lỗi.
   - **(B) Đổi một chữ: "on two street frames, surface detail is AI-assisted…".** Ưu: đúng với §12.1 và với phim. Nhược: lệch chữ §10.6, cần chủ dự án duyệt sửa Kinh thánh.
   - Đề xuất **(B)**. Bản nháp hiện để (A) vì lệnh yêu cầu nguyên văn.
7. **Ghi công bắt buộc (RIGHTS):**
   - "© OpenStreetMap contributors" (P1810-OSMN, ODbL);
   - "Cliopatria (Seshat Global History Databank), CC BY 4.0" (P1810-CLIO);
   - "OpenHistoricalMap contributors" + "CNIG/IGN (CC BY 4.0)" (P1810-OHM);
   - Dirección General del Catastro (điều khoản Catastro: "the D. G. of the Cadastre … is mentioned as author and owner");
   - Open Parliament Licence (P1810B-HANSARD).
   - Các dòng này đã có trong mô tả. **Lưu ý:** câu OPL "Contains Parliamentary information licensed under the Open Parliament Licence v3.0." là câu chuẩn của giấy phép. RIGHTS ghi **chưa đọc được nguyên văn** (parliament.uk 403), phải đối chiếu trước G2.
   - §12.1 bỏ dòng nguồn trên hình. P1810-CLIO và P1810-OSMN còn ghi "trên hình", nên **P cần sửa RIGHTS** cho khớp §12.1, hoặc giữ ghi công nhỏ trên bản đồ nếu giấy phép buộc. ODbL và CC BY chấp nhận ghi công ở nơi hợp lý; P kiểm nguyên văn trước khi bỏ.
8. **Sau khi đăng:** ghim bình luận §3. Đăng 5 phần danh mục (§4) làm trả lời của chính kênh dưới bình luận ghim, theo thứ tự. Lưu 4 câu trả lời sẵn (§3.2) để dán khi có câu hỏi tương ứng.

## 2. MÔ TẢ YouTube (dán nguyên khối, 4 423 ký tự)

```text
Why was one small rock besieged fourteen times? From the 1704 capture and the Great Siege of 1779–83 to a fence on the neutral ground, a runway across the only road to Spain and the 2026 UK–EU treaty, this history explainer tells Gibraltar's story from British and Spanish records side by side. Every date is sourced; where the two sides' numbers differ, we give both and say who counted.

Facts as of 18 October 2026. The treaty is in force only provisionally.

SOURCES (short form; pages and archive links in the replies to the pinned comment)
Hook & 1704 — Sayer, The History of Gibraltar (1862); Montero, Historia de Gibraltar y de su campo (1860); García Sanz, Historia de Gibraltar (2022); Gibraltar National Museum; Gibraltar Heritage Trust; Treaty of Utrecht (1713), Art. X, in Jenkinson, Collection of Treaties, vol. II (1785); Ortega Carcelén, Real Instituto Elcano (2013); Gómez Nadal, Almoraima 48 (2018); Escuadra Sánchez, Almoraima 34 (2007); Spain, Ministry of Foreign Affairs; UK Hansard (2015); Wikipedia, "List of sieges of Gibraltar".
Great Siege — Drinkwater, A History of the Siege of Gibraltar (1785; Dublin 1786; 1905 ed.); Spilsbury, A Journal of the Siege of Gibraltar (1908 ed.); Ancell, A Circumstantial Journal (1784); Conseil de guerre privé (1785, attrib. d'Arçon); Fernández Duro, Armada española VII (1901); Beatson, Naval and Military Memoirs V (1804); Clowes, The Royal Navy III (1898); Schomberg, Naval Chronology II (1802).
Neutral ground & runway — Gómez de Avellaneda, IECG (2022); Marquina Barrio, Revista de Estudios Internacionales (1981); HM Government of Gibraltar (HMGoG) press releases; Gibraltar Parliament (2018); UK Hansard (1940–43, 2015); FRUS 1940; Howe, Northwest Africa (US Army, 1957); Canadian Military Engineers Association; CIM Magazine (2018); Gingell, Between the Devil and the Deep Blue Sea (Gibraltar National Archives).
The gate — UK FCDO; UK–EU Agreement on Gibraltar (2026); HMGoG Statistics Office, Employment Survey 2025; HMGoG, 50 Years: Closure of the Border (2019); Sánchez Mantero, Historia Contemporánea 41 (2010); UK Hansard (1969); INE (Spain), Indicadores Urbanos 2025; European Parliament Legislative Train.
Maps, images & data — Drinkwater 1786 plates (Internet Archive, public domain); Faden 1783 (Yale, public domain); An Exact Plan of Gibraltar 1705 (Rijksmuseum, CC0); US Army Map Service M981, 1943 (public domain); floating-battery print 1783 (Rijksmuseum, CC0). © OpenStreetMap contributors (ODbL). Buildings, La Línea: Dirección General del Catastro. Cliopatria (Seshat Global History Databank), CC BY 4.0. OpenHistoricalMap contributors; CNIG/IGN, CC BY 4.0. Natural Earth. NOAA ETOPO 2022. Poly Haven (CC0). Contains Parliamentary information licensed under the Open Parliament Licence v3.0.

WHAT IS ESTIMATED
• 1782 town: blocks follow Drinkwater's 1786 plan. Inside the area it marks "THE RUINS OF GIBRALTAR", the ruined houses are our estimate; unmapped blocks are estimated infill.
• Building heights (two storeys in 1782; most 2026 heights) and church-tower heights: the maps give none.
• 1782 coastline: today's; we found no precise 1782 shoreline.
• Map borders: approximate (Cliopatria/Seshat; OpenHistoricalMap/IGN for 1704). Sea routes between sourced points: approximate.
• Troops and crowds: illustrative in number and layout (about 29,000 besiegers shown; sources give 33,000–40,000). Flag positions, boats, shot furnaces, regimental facing colours and civilian clothing: illustrative.

HOW AI WAS USED
• Two street frames (1782, 1943): one daytime plate each was AI-edited under a mask limited to walls, roofs and ground. Layout, landmarks, flags, people and light come from our sourced 3D render, laid back on top.
• King's Bastion: AI stone detail on the wall surface only.
• AI helped read 1782 diaries. Every extract was matched word-for-word to the source file and checked by a second model; numbers were checked against page images.
• AI created no facts: no position, building, flag, uniform, date or number.
• The AI-edited images carry C2PA Content Credentials, so YouTube may label this video as altered or synthetic; we also disclosed AI use at upload.

Narration: synthetic voice. Visuals: 3D reconstructions built from the cited sources and registers; on marked street frames, surface detail is AI-assisted — layout, landmarks and flags come from the sources. Historical images: public domain / CC0, credited.
```

### 2.1 Căn cứ từng mục "What is estimated" / "How AI was used" (kiểm trong repo)

| Câu trong mô tả | Căn cứ |
|---|---|
| Khối phố 1782 theo plan Drinkwater 1786 | `ghost/ghost-1782.geojson`: nguồn `ia-drinkwater1786-plan-batteries` (IA historyoflatesie00drin leaf 373), 22 khối + 13 toà, do_tin cao/vừa. Chú thích layers.js (V5b-2b) |
| Nhà đổ nát ước tính trong vùng "THE RUINS OF GIBRALTAR" | RIGHTS P1810C-DRINK373; V6 §1.5 P3 ("Ruins: estimated (plan 1786…)"); layers.js `RUINS_SRC`, chú thích V6 (P3) |
| Lấp khối ước tính | layers.js `INFILL_SRC: 'Grey-washed blocks: estimated infill'` (V5b-2c I2); Kinh thánh §11.4 |
| Chiều cao 2 tầng (1782) | ghost-1782 `so_tang_uoc: 2`, `cach_uoc_tang` ("bản đồ không ghi tầng … dùng cận dưới") |
| Chiều cao 2026 phần lớn ước | TIEN-KY-VAY-HAM §1 điểm 4: OSM chỉ 8 toà có số tầng trong phố cổ |
| Chiều cao tháp nhà thờ | V5B2D-BAO-CAO: "church tower height illustrative" (St Mary the Crowned, Convent) |
| Bờ biển 1782 là bờ hiện nay | V6 §1.5 V2D-4: "Giữ bờ hiện tại: không tìm được nguồn đường bờ 1782 đủ chính xác" |
| Ranh giới xấp xỉ | treatment.json `nhan_ranh`: "approx. borders c. 1704 — OpenHistoricalMap, IGN"; "c. 1782 / c. 1941 — Cliopatria (Seshat)" |
| Tuyến biển xấp xỉ | TUYEN-BAO-CAO §2: "Đoạn giữa hai điểm có claim luôn `approx: true`"; "Hải trình … là biểu trưng" |
| ≈ 29 000 quân, nguồn 33 000–40 000 | V5B2D-BAO-CAO (P1 và bảng nguồn: "~29,000 troops … illustrative"; S065). V6 §1.2: 28 716 người, 108 khối |
| Cờ, xuồng, lò nung đạn, màu nẹp: minh hoạ | V5B2D-BAO-CAO bảng nguồn ("vị trí minh hoạ"); RIGHTS-V6 quân phục ("màu viền … minh hoạ"); layers.js dòng 284 |
| Quần áo dân thường minh hoạ | RIGHTS-V6; KHUNG-NEO-V6 §2 |
| Hai khung phố có tấm AI, mặt nạ chỉ tường/mái/đất | Kinh thánh §11.3(a). KHUNG-NEO-V6: 1782 dùng tấm C PT2 lần 2; 1943 dùng tấm C V6 lần 3 (mặt nạ bảo vệ đất xa > 55 m, kiểm dữ kiện 0 lỗi). RIGHTS P1810-AI (phần PT2), P1810B-AI, P1810C-AI-V6 |
| King's Bastion vân AI chỉ mặt tường | RIGHTS P1810C-HC7; V6 §1.4 ("chỉ tường escarp") |
| AI đọc nguồn, kiểm nguyên văn, mô hình thứ hai, ảnh trang | NC-AI §7.1 (80/82 khớp nguyên khối, lượt 2 Claude Sonnet); `g1b/ai-doc-nguon.md` §2 (bảng gác đọc từ ảnh trang) |
| C2PA | RIGHTS P1810B-AI ("Có C2PA Content Credentials"); P-1810c §4 điểm 8 |
| Không sinh dữ kiện | Kinh thánh §12.2 ("không sinh dữ kiện (vị trí, công trình, cờ, quân phục, ngày, số)") |

**Không đưa vào mô tả, cần chủ dự án biết:**
- Khung neo 1782 hiện có ~47 người. Bảng gác 7/9/1782 chỉ đỡ được khoảng ≤ 1,5 lính trực / 100 m phố (`g1b/ai-doc-nguon.md` §2).
- Nếu giữ mật độ hiện tại, "What is estimated" phải thêm "street crowd density in 1782: illustrative", hoặc phải giảm người trong khung.

## 3. BÌNH LUẬN GHIM

### 3.1 Bình luận chính (1 207 ký tự)

```text
How this film was made — sources, estimates, AI

Main sources: Drinkwater's history of the siege and his 1786 plan of the town; the garrison diaries of Spilsbury and Ancell; Montero, Historia de Gibraltar (1860); Sayer, History of Gibraltar (1862); García Sanz, Historia de Gibraltar (2022); the Treaty of Utrecht (1713), Art. X; Marquina Barrio (1981) on the airstrip; UK Hansard; HM Government of Gibraltar; UK FCDO; INE (Spain). Every source, with pages and archive links, is in the replies below.

Estimated: the ruined 1782 houses inside the area Drinkwater's plan marks "The Ruins of Gibraltar"; building heights; the 1782 coastline (today's is shown); map borders and sea routes (approximate); the number and layout of troops and crowds (illustrative).

AI: on two street frames, walls, roofs and ground were AI-retouched under a mask; King's Bastion's wall carries AI stone detail. AI also helped read the 1782 diaries, and every quote was checked word-for-word against the original. AI added no facts. The narration is a synthetic voice. The AI images carry C2PA credentials, so YouTube may label the video.

Facts as of 18 October 2026. Spotted an error? Reply with your source and we'll check it.
```

### 3.2 Trả lời sẵn cho câu hỏi dự đoán (trung tính hai phía, theo claims)

**(1) "Fourteen sieges?"** (494 ký tự). Claims S001, S004, S006; `dem_so_lan_vay` trong `claims-vay-ham.json`.
- Con số 15 là từ Wikipedia dẫn Jackson 1987, **chưa xác minh bản gốc**. Vì vậy câu trả lời chỉ viết "some lists".
```text
Fourteen sieges? It depends on how you count. Sayer's History of Gibraltar (1862) and the Gibraltar National Museum count fourteen, from the Castilian capture of 1309 to the Great Siege of 1779–83; both 1333 sieges count, and the 1704 capture and the 1704–05 counter-siege count as two. A modern Spanish history (García Sanz, 2022) numbers the 1704 attack as the eleventh, because it counts differently. Some lists reach fifteen by adding the 1969–85 border closure; we kept to military sieges.
```

**(2) "Is this AI?"** (515 ký tự). Kinh thánh §11.3, §12.2; RIGHTS P1810B-AI, P1810C-HC7, P1810C-AI-V6.
```text
Is this AI? Partly, and we say where. The narration is a synthetic voice. The 3D scenes are our own reconstructions, built from period maps and records. On two street frames, the surface of walls, roofs and ground was retouched by AI under a mask; on King's Bastion, the stone texture of one wall is AI-made. AI also helped read old diaries, with every quote checked word-for-word. No video was AI-generated, and AI supplied no dates, numbers, positions, flags or uniforms. Those come from the sources listed above.
```

**(3) "Why both sides' numbers?"** (553 ký tự). Claims S069, S070, S071, S076, S077. Khớp lời 2n và 2r.
```text
Why both sides' numbers? Because the two sides counted different things. For the floating batteries on 13–14 September 1782, a British estimate and the Spanish historian Montero both put attackers' losses above 2,000 (the British figure includes prisoners); a French account of 1785 counts 185 hit by gunfire before the fires; the garrison's own return lists 16 killed. For the whole siege, Montero gives about 2,000 defenders and 6,000 besiegers lost from all causes; the garrison's records count at least 869 dead. We show who counted, and leave both.
```

**(4) "Is the isthmus Spanish?"** (477 ký tự). Claims S022, S030, S031, S035, C07. Khớp lời 1i và 5h.
```text
Is the isthmus Spanish? The two governments disagree, and the film doesn't take a side. The 1713 Treaty of Utrecht (Art. X) names the town, castle, port and forts, not the sandy isthmus. Spain's foreign ministry says the isthmus was never ceded and does not recognise the fence as a border. In 2015 the UK's Europe minister told Parliament that Britain regards Gibraltar as including the isthmus. The 2026 UK–EU agreement says it changes neither side's position on sovereignty.
```

## 4. DANH MỤC NGUỒN ĐẦY ĐỦ: 5 trả lời dưới bình luận ghim

Chỉ ghi nguồn có claim trong lời v4.1 (gồm nguồn đối chiếu hai phía) hoặc tư liệu đã chốt trên hình/làm dữ kiện dựng. "IA" = Internet Archive (archive.org/details/<ID>). "PD" = public domain.

**Phần 1/5: Hook & 1704**
```text
Sources 1/5 — Hook & 1704
• F. Sayer, The History of Gibraltar (1862), title page, pp. 99–114 — IA historyofgibralt00sayeuoft, PD
• F. M. Montero, Historia de Gibraltar y de su campo (Cádiz, 1860), pp. 263–264, 293, 323–324 — IA historiadegibra00montgoog, PD
• C. García Sanz, Historia de Gibraltar (Madrid: Catarata, 2022), chs. 1–3
• Gibraltar National Museum, "Brief History of Gibraltar" (web)
• Gibraltar Heritage Trust, The Great Siege — schools resource, ch. 1 (web)
• Wikipedia, "List of sieges of Gibraltar"
• Lord Mahon, History of the War of the Succession in Spain (1836) — IA historyofwarofsu00stan, PD
• C. Fernández Duro, Armada española, vol. VI — IA armadaespaolade00durogoog, PD
• W. L. Clowes, The Royal Navy, vol. II (1898) — IA royalnavyhistory02clowuoft, PD
• Treaty of Utrecht, 13 July 1713, Art. X, in C. Jenkinson, A Collection of All the Treaties, vol. II (1785) — IA bim_eighteenth-century_a-collection-of-all-the-_1785_2, PD
• M. Ortega Carcelén, Real Instituto Elcano, ARI 19/2013
• HM Government of Gibraltar, press release 500/2013
• Spain, Ministerio de Asuntos Exteriores, "Gibraltar" (web)
• UK Hansard, Westminster Hall, 14 Oct 2015, col. 129WH (D. Lidington)
• B. Gómez Nadal, Almoraima 48 (2018), pp. 259–272
• A. Escuadra Sánchez, Almoraima 34 (2007)
```

**Phần 2/5: The Great Siege**
```text
Sources 2/5 — The Great Siege (1779–83)
• J. Drinkwater, A History of the Siege of Gibraltar 1779–1783 (text of 1785; London: Murray, 1905), chs. III–VIII and appendix — IA historysiegegibr00drin, PD
• J. Drinkwater, A History of the Late Siege of Gibraltar (3rd ed., Dublin, 1786), p. 387 — IA historyoflatesie00driniala, PD
• J. Spilsbury, A Journal of the Siege of Gibraltar 1779–1783, ed. B. H. T. Frere (Gibraltar Garrison Library, 1908), pp. 67, 73–75 — IA ajournalsiegegi00spilgoog, PD
• S. Ancell, A Circumstantial Journal of the Long and Tedious Blockade and Siege of Gibraltar (1784) — IA acircumstantial00ancegoog, PD
• F. M. Montero, Historia de Gibraltar y de su campo (1860), pp. 337–373 — IA bub_gb_4_AqUai2tkIC, PD
• [attrib. J.-C.-É. Le Michaud d'Arçon], Conseil de guerre privé sur l'événement de Gibraltar en 1782 (1785), pp. 49–50, 201 — IA bub_gb_Lx5oLGPGvfgC, PD
• C. Fernández Duro, Armada española, vol. VII (1901) — IA bub_gb_G1y3VAtRHTIC, PD
• R. Beatson, Naval and Military Memoirs of Great Britain, vol. V (1804) — IA navalmilitarymem05beatuoft, PD
• W. L. Clowes, The Royal Navy, vol. III (1898) — IA royalnavyhistor03clow, PD
• I. Schomberg, Naval Chronology, vol. II (1802) — IA 10281675bsb, PD
```

**Phần 3/5: Neutral ground & runway**
```text
Sources 3/5 — The neutral ground & the runway
• C. Gómez de Avellaneda Sabio, "la Línea de Contravalación", Guías del patrimonio del Campo de Gibraltar 6 (IECG, 2022), pp. 60–61
• C. García Sanz, Historia de Gibraltar (2022), ch. 3 and n. 43
• A. Marquina Barrio, "La pista de aterrizaje de Gibraltar", Revista de Estudios Internacionales 2:2 (1981), pp. 307–314 (CEPC)
• HM Government of Gibraltar press releases 199/2018, 713/2013, 310/2017, 85/2015, 315/2019, 838/2022
• Gibraltar Parliament, motion on the Freedom of the City for RAF Gibraltar, 17 May 2018
• UK Hansard: Commons 8 Jan 2015; 19 Jun 1940; 20 Aug 1940; 13 Nov 1940; 3 Dec 1942; 3 Mar 1943 — Lords 11 Nov 1942
• Foreign Relations of the United States 1940, vol. II docs. 919–920; vol. III doc. 712
• G. F. Howe, Northwest Africa: Seizing the Initiative in the West (US Army Center of Military History, 1957), chs. IV, XI, XIII — PD
• Canadian Military Engineers Association, "Canadian Tunnellers Tackle Gibraltar" (web)
• C. Keating, "Hard rock mining on the Rock", CIM Magazine, 5 Nov 2018
• J. Gingell, Between the Devil and the Deep Blue Sea, 2nd ed. (Gibraltar National Archives)
```

**Phần 4/5: The gate (1969–2026)**
```text
Sources 4/5 — The gate (1969–2026)
• UK Hansard, Commons, 9 Jun 1969 (M. Stewart)
• HM Government of Gibraltar, 50 Years — Gibraltar: Closure of the Border 1969–2019, ch. 6
• R. Sánchez Mantero, Historia Contemporánea 41 (2010), p. 377; C. Langa Nuño, Historia Contemporánea 41 (2010); L. M. Manglano Tirado, Aportes 117 (2025)
• HM Government of Gibraltar, "Political development" (web); press releases 177/2023, 517/2026; Budget Address 536/2026
• HMGoG Statistics Office, Employment Survey 2025, Table 2.4
• UK FCDO press release (2026) and Explanatory Memorandum CP 1645
• Agreement between the UK and the EU in respect of Gibraltar (2026), Art. 2
• INE (Spain), Indicadores Urbanos 2025
• European Parliament, Legislative Train, 2026/0058(NLE)
Facts as of 18 October 2026.
```

**Phần 5/5: Maps, images, data**
```text
Sources 5/5 — Maps, images & data
• J. Drinkwater, plates in A History of the Late Siege of Gibraltar (London, 1786): plan of the batteries and town (1782 street blocks; "The Ruins of Gibraltar" area) — IA historyoflatesie00drin, Univ. of Pittsburgh copy, PD
• W. Faden, Plan of the bay, rock and town of Gibraltar (1783) — Yale University Library 2046612, PD
• An Exact Plan of the Town, Castle, Moles and Bay of Gibraltar (1705) — Rijksmuseum RP-P-OB-83.400, CC0
• US Army Map Service, Gibraltar city plan 1:10,000, M981 (1943) — Princeton University Library; US federal work, PD
• The Destruction of the Floating Batteries before Gibraltar (1783) — Rijksmuseum RP-P-OB-19.249, CC0 (shape reference)
• Building data: © OpenStreetMap contributors (ODbL); Dirección General del Catastro (La Línea)
• Borders: Cliopatria (Seshat Global History Databank), CC BY 4.0; OpenHistoricalMap contributors; CNIG/IGN, CC BY 4.0
• Natural Earth (PD); NOAA ETOPO 2022 (CC0); Poly Haven textures (CC0)
• Contains Parliamentary information licensed under the Open Parliament Licence v3.0.
```

## 5. Đo độ dài

Đếm bằng `/opt/cine/bin/python` (`len(str)`, ký tự Unicode):

| Khối | Ký tự | Giới hạn |
|---|---|---|
| Mô tả | 4 423 (4 479 byte) | 5 000 (YouTube) |
| Bình luận ghim chính | 1 207 | 1 500 (lệnh) |
| Trả lời (1)–(4) | 494 / 515 / 553 / 477 | — |
| Danh mục phần 1–5 | 1 288 / 1 225 / 1 150 / 777 / 1 073 | ≤ 1 500 mỗi phần (tự đặt; giới hạn độ dài bình luận của YouTube chưa kiểm trong repo) |

Danh mục phần 1–5 (ký tự, đo lại sau khi ghi tệp): **1 288 / 1 225 / 1 150 / 777 / 1 073**. Không khối nào chứa `<` hoặc `>`.

## 6. Danh mục tư liệu hình CHỜ CHỌN (chỉ đưa vào phần 5/5 khi thực dùng trên hình)

Trích `vay-ham/tai-san-vay-ham.json` và `licenses/`. Mọi mục `commercial_ok: true`, trừ AMS M981 (bản quét Princeton có điều kiện, D8). Dòng ghi công soạn sẵn:

- "The Siege and Relief of Gibraltar", W. Sharp after J. S. Copley (1810) — Library of Congress 96510788, no known restrictions (chỉ nửa phải, TIEN-KY-VAY-HAM §2.1)
- J. S. Copley, Study for The Siege of Gibraltar (c. 1785–86) — Cleveland Museum of Art 1950.215, CC0
- J. S. Copley, studies for "The Siege of Gibraltar" — The Met 60.44.18 / 60.44.12 / 60.44.17, CC0
- Fan with the siege of Gibraltar (c. 1782) — The Met 24.80.3, CC0
- Beleg van Gibraltar, 1779–1782 — Rijksmuseum RP-P-1960-424, CC0
- J. Drinkwater, A View of the Grand Attack upon Gibraltar, 13 Sept 1782 (1786) — IA historyoflatesie00drin, PD
- J. Drinkwater, A View from Gibraltar of the Spanish Batteries (1786) — IA historyoflatesie00drin, PD
- Portrait of General George Eliott (1784) — Rijksmuseum RP-P-OB-53.323, CC0
- G. L. Hall, The King's Bastion (1844) / Part of the Bay of Gibraltar, the Spanish Lines (1844) — Yale Center for British Art B1975.4.490 / .491, CC0
- The neutral ground, from the Rock; The rock, from fort San Felipe; The Landport (c. 1860–70) — Rijksmuseum RP-F-2001-7-257-16 / -1 / -14, CC0
- F. Sayer, Plan of the Rock, Town and Territory of Gibraltar (1865) — IA historyofgibralt00saye, PD
- "Gibraltar. Neutral ground" (c. 1900–10) — Library of Congress 2025710366, no known restrictions (RIGHTS P1710-01)
- US Army Air Forces photographs, Gibraltar, 2 Oct 1943 — US National Archives 204918833 / 204918836 / 204918839, PD
- Visscher, Plan de la ville de Gibraltar (1706) — Library of Congress 2008621715; Homann Heirs (1733) — Rijksmuseum RP-P-2018-1131, CC0; Tirion (1759) — Rijksmuseum RP-P-2018-1774, CC0
- KHÔNG dùng làm Ken Burns: Emes, Scene before Gibraltar 14 Sept 1782 (tiêu điểm người chết đuối, TIEN-KY-VAY-HAM §2.1; Kinh thánh §10.6)
- Footage shot 2p ("then/now"): chưa có nguồn trong repo. Nếu dùng Pexels/Pixabay phải ghi vào `SOURCES-FOOTAGE.csv` (RIGHTS dòng 172).
