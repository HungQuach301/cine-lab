# K2C-T1-06 — SHOT LIST (ước) · script.md

> Tự đo của phiên P từ `shots.yaml` bằng `shotlist.py` (151,2 từ/phút, lặng 0.6 s/đoạn). **Không phải kết quả checks/**; checks 1.10.1 chạy trên đặc tả `episode.yaml` khi dựng.
> Tổng ước: **15.58 phút** (935 s), 90 shot.

## 1. Tỷ lệ theo loại shot
| type | giây | % | trần/luật |
|---|---|---|---|
| scene3d | 340.1 | 36.4 % |  |
| chart3d | 230.6 | 24.7 % |  |
| map | 167.7 | 17.9 % |  |
| card | 143.1 | 15.3 % | ≤ 25 % (Q26b `the`, Q34) |
| photo | 23.4 | 2.5 % | cộng vào ≤ 40 % |
| document | 9.1 | 1.0 % | cộng vào ≤ 40 %; ≤ 3 s/shot |
| footage | 20.6 | 2.2 % | cộng vào ≤ 40 %; ≤ 8 s/clip |
| **ảnh + tài liệu + footage** | 53.2 | **5.7 %** | ≤ 40 % (QUAN-TRI-RUI-RO §6.3, Q32/Q34d) |
| card liên tục dài nhất | 29.2 | — | ≤ 90 s |

## 2. Luật từng shot
- footage/ảnh > 8 s hoặc document > 3 s: **0** 
- document thiếu p.paper/p.date: **0**
- ảnh/footage/tài liệu thiếu nhãn năm/nguồn: **0**
- cùng (scene_id, camera_id) > 2 lần: **0** ; đúng 2 lần (bằng ngưỡng): không
- bối cảnh (scene3d theo bộ cảnh; `the` = card): the 15.3 % (liên tục ≤ 60 s), corner 14.1 % (liên tục ≤ 49 s), stairs 6.0 % (liên tục ≤ 23 s), street 4.3 % (liên tục ≤ 16 s), tiers 4.2 % (liên tục ≤ 39 s), bank 3.9 % (liên tục ≤ 28 s), lot 2.9 % (liên tục ≤ 16 s), ends 1.1 % (liên tục ≤ 10 s); nửa sau có 5 bộ cảnh 3D: bank, corner, ends, lot, street
- số neo hiện bằng chart3d/scene3d: **22/29 = 76 %** (≥ 60 %); số neo trên map: 6, photo: 1, card: 0, document: 0; mã claim không khớp `nums` của shot: 0
- địa danh không có shot map: **0** (11 địa danh)
- người thiếu photo/ly_do: **0** (3 người)

## 3. Bảng shot
| # | đoạn | bắt đầu | dài (s) | type | scene_id | camera_id | số (claim) | nội dung | nguồn / nhãn |
|---|---|---|---|---|---|---|---|---|---|
| s00a | 00 | 0:00.0 | 6.0 | scene3d | corner | wide_dusk |  | Toà góc phố chạng vạng, cửa sổ sáng; nhãn '1 in 13 homes' bám toà |  |
| s00b | 00 | 0:06.0 | 5.2 | chart3d | ch_hook | front | C01, C02 | Hai cột khác cơ sở, nhãn rõ |  |
| s00c | 00 | 0:11.1 | 3.2 | scene3d | corner | push_facade |  | Đẩy vào mặt tiền; tựa câu hỏi 'Why did America almost stop building them?' |  |
| s00d | 00 | 0:14.3 | 16.5 | scene3d | street | dolly_day |  | Lướt dãy phố; dòng 'Census ACS 2024 · NRC 2025 · our calculation' + 'Not financial advice' + 'Facts as of 12 Oct 2026' |  |
| s01a | 01 | 0:30.8 | 9.1 | scene3d | corner | section |  | Cắt lớp: cửa hàng, 3 tầng căn hộ, 1 cầu thang (nhãn bám vật thể) |  |
| s01b | 01 | 0:39.9 | 8.7 | scene3d | street | labels_row |  | Nhãn duplex · triplex · fourplex · 5–19 homes trên từng toà |  |
| s01c | 01 | 0:48.6 | 2.8 | photo | loc_det_fifthwood | kenburns |  | Ảnh lưu trữ góc phố thương mại có căn hộ tầng trên | LOC-DET-01 · Pittsburgh, c. 1900–1915 · Library of Congress |
| s01c2 | 01 | 0:51.4 | 7.1 | photo | loc_fsa_durham | kenburns | C03 | Ảnh lưu trữ cửa hàng góc phố 1940; thẻ nhỏ 'pre-1940: ~23% (our calculation, ACS 2024)' | LOC-FSA-01 · Durham, N.C., May 1940 · Library of Congress (FSA/OWI) |
| s01d | 01 | 0:58.5 | 18.7 | card | card_locks | intro |  | Thẻ 3 khoá (map · stairwell · bank) + 'costs, rates, rents' — 'OUR READ' |  |
| s01e | 01 | 1:17.2 | 6.6 | scene3d | corner | aerial_day |  | Toàn cảnh khu phố ban ngày |  |
| s02a | 02 | 1:23.7 | 1.6 | scene3d | tiers | top |  | Sa bàn từ trên, tựa 'LOCK 1 · THE MAP' |  |
| s02b | 02 | 1:25.3 | 6.3 | photo | p_hoover | kenburns |  | Chân dung (people) | CAN-TAI-HO:LOC-HOOVER · Herbert Hoover, c. 1921 · Library of Congress |
| s02c | 02 | 1:31.7 | 7.9 | chart3d | ch_zoning1921 | front | C05 | 48 thành phố (1921) — khối đếm 48 trên bản đồ Mỹ mờ |  |
| s02d | 02 | 1:39.6 | 2.4 | document | d_sszea | page | C06 | Trang bìa, ≤ 3 s | DOC-SSZEA · Standard State Zoning Enabling Act, 1926 · U.S. Dept. of Commerce |
| s02e | 02 | 1:42.0 | 6.7 | scene3d | tiers | districts_fill | C06 | Các khu tô màu lần lượt (minh hoạ) |  |
| s02g | 02 | 1:48.7 | 7.5 | map | usmap | m_euclid |  | Euclid, Ohio cạnh Cleveland (nhãn) — places |  |
| s02h | 02 | 1:56.3 | 16.7 | scene3d | tiers | oblique_tiers | C08 | U-1 → U-4 dựng lên lần lượt; toà góc phố đặt thử vào U-1..U-3: đỏ |  |
| s02i | 02 | 2:12.9 | 4.8 | photo | p_sutherland | kenburns |  | Chân dung (people) | CAN-TAI-HO:LOC-SUTHERLAND · Justice George Sutherland · Library of Congress |
| s02j | 02 | 2:17.7 | 2.0 | document | d_euclid | page394 | C10 | Trang 394, tô câu 'height and bulk' ≤ 3 s | DOC-EUCLID · Village of Euclid v. Ambler Realty Co., 272 U.S. 365 (1926) |
| s02k | 02 | 2:19.7 | 13.9 | scene3d | tiers | shadow_low | C10 | Toà căn hộ đổ bóng lên nhà nhỏ, xe đỗ; chú thích trích dẫn |  |
| s02l | 02 | 2:33.6 | 13.1 | scene3d | corner | shop_close | C10 | Toà góc phố 'in a different environment' — phố thương mại sáng; chú thích trích |  |
| s02m | 02 | 2:46.7 | 12.1 | card | card_quote | euclid_test | C11 | Thẻ trích 'fairly debatable → legislative judgment controls' + 'judges defer to local lawmakers' |  |
| s03a | 03 | 2:58.8 | 4.8 | footage | f_chicago_aerial | clip |  | Flycam khu dân cư nhà một hộ | PX-38879369 · Chicago-area homes · Pexels, 2025 (illustrative) |
| s03b | 03 | 3:03.5 | 7.1 | map | usmap | m_colorado |  | Colorado nổi lên, 334 khu vực pháp lý (lưới) |  |
| s03c | 03 | 3:10.7 | 17.1 | chart3d | ch_co | land | C12 | 59 % / 3 % trên khối đất 3D |  |
| s03d | 03 | 3:27.8 | 10.3 | scene3d | lot | plan | C14 | Ô đỗ xe lấp lô; nhãn '85% of residential land · most often 2 spaces/home' |  |
| s03e | 03 | 3:38.1 | 5.8 | scene3d | lot | iso |  | Toà co lại theo số ô đỗ (minh hoạ, không số) |  |
| s04a | 04 | 3:43.8 | 6.7 | scene3d | corner | stair_section |  | Cầu thang trong mặt cắt; tựa 'LOCK 2 · THE STAIRWELL'; hai lối thoát vẽ mũi tên |  |
| s04a2 | 04 | 3:50.6 | 4.8 | scene3d | stairs | model_code |  | Khối 'model code' đặt lên mặt cắt toà; nhãn 'International Building Code' |  |
| s04b | 04 | 3:55.3 | 2.4 | document | d_ibc | table | C15 | Bảng 'Fourth story… NP' ≤ 3 s (dựng lại chữ, không chụp trang) | DOC-IBC-SEA · Seattle Building Code 2021 (IBC 2021), Table 1006.3.4(1) |
| s04c | 04 | 3:57.7 | 18.7 | scene3d | stairs | elev_stack | C15 | Xếp tầng 1→3 với 1 cầu thang (xanh), tầng 4 'NP' (đỏ) |  |
| s04d | 04 | 4:16.4 | 9.9 | scene3d | street | tall_walkups |  | Toà 4–6 tầng trên lô hẹp được tô nhấn |  |
| s04e | 04 | 4:26.3 | 13.1 | scene3d | stairs | plan_compare | C16 | Mặt bằng 1 vs 2 cầu thang; phần cam ~7 % |  |
| s04f | 04 | 4:39.4 | 17.1 | chart3d | ch_pew | cost | C16 | +7 % sàn, +6–13 % chi phí; nhãn 'Pew + CBNA (advocates single-stair)' |  |
| s04g | 04 | 4:56.4 | 6.3 | map | usmap | m_wash |  | Washington state → Seattle (nhãn) |  |
| s04h | 04 | 5:02.8 | 4.4 | scene3d | stairs | floor_plate | C17 | Sàn nhỏ bị hai lõi thang chiếm; chú thích trích |  |
| s04i | 04 | 5:07.2 | 12.3 | map | usmap | m_seattle | C18 | Seattle: '1977 · up to 6 stories, ≤4 homes/floor (2021 code)' |  |
| s04k | 04 | 5:19.5 | 2.8 | scene3d | stairs | pressurized | C18 | Lõi thang kín, mũi tên áp suất; nhãn 'Seattle 2021: ≤6 stories · ≤4 homes/floor · pressurized stair' |  |
| s04l | 04 | 5:22.2 | 17.7 | chart3d | ch_terner | bar | C57 | +≈10 % chi phí theo luật thương mại cho ≥ 3 căn (California, Terner 2024) |  |
| s05a | 05 | 5:39.9 | 5.2 | footage | f_fire_escape | clip |  | Cầu thang thoát hiểm gạch, ≤ 6 s | PX-36624235 · Fire escape, U.S. city · Pexels, 2025 (illustrative) |
| s05b | 05 | 5:45.1 | 23.0 | card | card_positions | fire_side |  | Thẻ 3 tổ chức (IAFC 03/2024 · IAFF+Metro Chiefs 06/2024 · CAL FIRE) trích ngắn, nhãn 'FIRE SERVICE' |  |
| s05c | 05 | 6:08.1 | 13.1 | map | usmap | m_calif |  | California (nhãn); chú thích 'near-unanimous opposition… above three stories' |  |
| s05d | 05 | 6:21.2 | 25.4 | chart3d | ch_pew | records | C20, C21 | 4 440 toà NYC; tỷ lệ tử vong do cháy 'same'; 4 ca 2012–2024 — nhãn 'Pew + CBNA (advocates)' |  |
| s05e | 05 | 6:46.6 | 4.8 | map | usmap | m_minn |  | Minnesota (nhãn) + dòng 'WJE & Crux for MN DLI, Dec 2025' |  |
| s05f | 05 | 6:51.3 | 12.3 | scene3d | stairs | fire_logic | C24 | Sơ đồ 3 điều kiện trên mặt cắt: sprinkler hỏng + cửa căn hộ mở + cửa thang mở |  |
| s05g | 05 | 7:03.6 | 18.9 | chart3d | ch_icc | vote | C25 | 86–34; 'IBC 2027 not yet published (as of 12 Oct 2026)' |  |
| s06a | 06 | 7:22.5 | 5.2 | scene3d | bank | side |  | Hàng khối 1–2–3–4 | 5+; tựa 'LOCK 3 · THE BANK' |  |
| s06a2 | 06 | 7:27.6 | 6.7 | scene3d | bank | line_four | C26 | Vạch '4' sáng giữa khối 4 và khối 5; nhãn 'FHFA · single-family = 1–4' |  |
| s06b | 06 | 7:34.4 | 2.4 | document | d_cfr | text | C26 | Hai định nghĩa tô sáng ≤ 3 s | DOC-CFR1282 · 12 CFR §1282.1 (FHFA), eCFR |
| s06c | 06 | 7:36.8 | 11.5 | scene3d | bank | counter | C27, C28 | Quầy 'single-family' nhận khối 1–4 |  |
| s06d | 06 | 7:48.3 | 4.8 | scene3d | bank | fifth_block |  | Khối thứ 5 trượt sang quầy 'multifamily' |  |
| s06e | 06 | 7:53.0 | 18.3 | scene3d | corner | shop_section | C29, C30 | Tầng trệt cửa hàng sáng; nhãn Fannie '1 unit, owner runs business' · FHA '≤4 units, ≥51% residential' |  |
| s06f | 06 | 8:11.3 | 4.8 | scene3d | bank | mixed_reject |  | Toà có shop + 5 căn bị cả hai quầy trả lại (minh hoạ) |  |
| s06i | 06 | 8:16.1 | 10.1 | map | usmap | m_calif2 | C33 | California + chú thích 'completion guarantees · recourse to personal assets' (Terner 2024) |  |
| s07a | 07 | 8:26.2 | 7.1 | footage | f_crane | clip |  | Cẩu tháp, toà lớn đang xây, ≤ 7 s | PX-20568183 · Apartment construction · Pexels, 2024 (illustrative) |
| s07b | 07 | 8:33.3 | 14.7 | map | usmap | m_minn2 | C58 | Minneapolis (nhãn); chú thích trích 'have challenged the profitability…' — Minneapolis Fed, Oct 2026 |  |
| s07c | 07 | 8:48.0 | 11.1 | scene3d | lot | pencil | C59 | Toà mẫu nhỏ trên lô, bảng thu–chi đỏ: 'would not be built under recent market conditions' (Terner 2024, California) |  |
| s07d | 07 | 8:59.1 | 29.2 | card | card_locks | recap_matrix |  | Bảng 'khoá × loại nhà': map → all · stairwell → 4+ stories · bank → 5+ homes, many with a shop · + costs/rates/rents (người đọc mù 2/3 đề nghị) |  |
| s08a | 08 | 9:28.3 | 3.2 | scene3d | ends | wide_1972 |  | Sa bàn hai đầu năm 1972 |  |
| s08b | 08 | 9:31.5 | 13.1 | chart3d | ch_comp | timeline | C60 | Chuỗi 1968–2025; mốc 1986→1990, 2006→2010, 2025 |  |
| s08c | 08 | 9:44.6 | 6.0 | chart3d | ch_comp | when_not_why |  | Cùng chuỗi, dấu '?' trên các cú rơi — 'when, not why' |  |
| s08d | 08 | 9:50.5 | 13.5 | chart3d | ch_share | front | C36 | 5,9 % → 1,1 %, our calculation |  |
| s08e | 08 | 10:04.0 | 13.9 | chart3d | ch_size | small519 | C35 | 377k → 48k (our sum of two Census columns) |  |
| s08f | 08 | 10:17.9 | 10.7 | chart3d | ch_size | sf_share | C63 | 57 % → 68 % (our calculation) |  |
| s08g | 08 | 10:28.6 | 11.1 | chart3d | ch_size | big50 | C34 | 20 % → 57 % (CNH, series riêng) |  |
| s08h | 08 | 10:39.7 | 6.9 | scene3d | ends | wide_2025 |  | Sa bàn năm 2025: giữa thưa, hai đầu dày |  |
| s09a | 09 | 10:46.7 | 3.6 | footage | f_townhouse | clip |  | Townhouse đang xây, flycam ≤ 7 s | PX-33003293 · Chattanooga, Tenn. · Pexels, 2025 (illustrative) |
| s09b | 09 | 10:50.2 | 21.4 | card | card_claim_record | claims | C61 | Khung đôi COMMON CLAIM ↔ RECORD (BAI-HOC #92): bên trái 2 trích (supporters / others, House Bill Report 2023) |  |
| s09c | 09 | 11:11.7 | 10.3 | map | usmap | m_minn3 | C54 | Minneapolis; '2040 Plan · adopted 2019 · as of Oct 2026' |  |
| s09d | 09 | 11:22.0 | 16.7 | chart3d | ch_mpls | blocks | C39 | 317 vs 12 335; nhóm so sánh ≈ bằng |  |
| s09e | 09 | 11:38.7 | 11.5 | card | card_claim_record | record_mpls | C40 | Bên RECORD: 'stable rents, stalled development' + trích summary |  |
| s09f | 09 | 11:50.2 | 9.9 | map | usmap | m_calif3 |  | California: Los Angeles, San Diego (nhãn) |  |
| s09g | 09 | 12:00.1 | 7.5 | chart3d | ch_sb9 | bars | C41 | 211 vs 7 |  |
| s09h | 09 | 12:07.6 | 12.7 | map | usmap | m_chicago | C42 | Chicago; chú thích 'Freemark 2019: prices up, no measurable rise in permits (5 yrs)' — tên người, không ảnh |  |
| s09i | 09 | 12:20.3 | 14.7 | chart3d | ch_study | urban | C43 | +0,8 % (3–9 năm), 'mostly higher-rent units' |  |
| s09j | 09 | 12:35.0 | 15.9 | map | usmap | m_auckland | C44 | Khung chèn Auckland, NZ; '≈21,800 extra homes permitted · ≈4% of stock' |  |
| s09k | 09 | 12:50.9 | 27.2 | card | card_claim_record | verdict |  | Khung đôi kết: 'the record sits in between' — nhãn từng nghiên cứu |  |
| s10a | 10 | 13:18.1 | 4.8 | scene3d | street | dusk_new |  | Dãy phố chạng vạng, toà nhỏ mới (minh hoạ), dòng 'As of 12 Oct 2026' |  |
| s10b | 10 | 13:22.8 | 6.3 | map | usmap | m_nyc2 |  | NYC: 'City of Yes · approved Dec 5, 2024' |  |
| s10c | 10 | 13:29.2 | 20.2 | scene3d | corner | day_town_center | C45 | Toà góc 2–4 tầng nhà ở trên cửa hàng, ban ngày; chú thích 'functionally banned by zoning' — NYC DCP |  |
| s10d | 10 | 13:49.4 | 10.3 | map | usmap | m_oregon | C46 | Oregon: '≥25,000 people · duplex→fourplex, townhouses, cottage clusters' |  |
| s10e | 10 | 13:59.7 | 9.9 | map | usmap | m_wash2 | C47 | Washington: '2–6 homes per lot' |  |
| s10f | 10 | 14:09.7 | 9.1 | map | usmap | m_texas | C50 | Texas: '≤6 stories · ≤4 homes/floor · since Sep 2025' |  |
| s10g | 10 | 14:18.8 | 7.1 | map | usmap | m_colorado2 | C51 | Colorado: '≥100,000 people · 5 stories · by Dec 1, 2027' |  |
| s10h | 10 | 14:25.9 | 3.4 | scene3d | bank | line_still | C26 | Vạch '4' vẫn nguyên; 'As of Oct 2026' |  |
| s11a | 11 | 14:29.3 | 10.3 | scene3d | corner | blue_hour_end |  | Toà góc phố giờ xanh (góc khác móc, đóng vòng hình) |  |
| s11b | 11 | 14:39.6 | 2.4 | photo | px_bayridge | kenburns |  | Toà góc phố gạch, cửa hàng tầng trệt, Bay Ridge; Ken Burns ≤ 6 s | PXP-7180335 · Brooklyn, N.Y. · Pexels (recent photo) |
| s11c | 11 | 14:42.0 | 14.3 | chart3d | ch_stock | front | C53 | 11,1 triệu căn trong toà 2–4 căn; > 8/10 căn có người ở là thuê (our calculation, ACS 2024) |  |
| s11d | 11 | 14:56.3 | 22.6 | scene3d | corner | section_end |  | Mặt cắt toà góc: 3 lớp khoá hiện lần lượt (bản đồ dưới chân, cầu thang, vạch 4) + 'costs, rates, rents' |  |
| s11e | 11 | 15:18.9 | 15.7 | scene3d | corner | crane_up |  | Cẩu máy lên cao, phố tối dần; dòng 'Facts as of 12 Oct 2026' |  |

## 4. places / people / anchors
**places:** Euclid, Ohio / Cleveland → m_euclid; Colorado → m_colorado; Seattle → m_seattle; New York City → m_nyc2; California (Los Angeles, San Diego) → m_calif; Minnesota / Minneapolis → m_minn; Washington state → m_wash; Chicago → m_chicago; Auckland, New Zealand → m_auckland; Oregon → m_oregon; Texas → m_texas

**people:** Herbert Hoover (Secretary of Commerce, 1921) → photo `CAN-TAI-HO:LOC-HOOVER`; Justice George Sutherland → photo `CAN-TAI-HO:LOC-SUTHERLAND`; Yonah Freemark → ly_do: Người còn sống, không có ảnh có giấy phép đã kiểm; chỉ hiện tên + tên nghiên cứu (LUAT-NOI-DUNG-G §6)

**anchors:** 1 in 13 homes in 2–4-unit buildings (ACS 2024) (C01) → s00b [chart3d]; 1 in 100 new homes (NRC 2025) (C02) → s00b [chart3d]; ~23% built before 1940 (C03) → s01c2 [photo]; 48 cities with zoning (1921) (C05) → s02c [chart3d]; Colorado 59% / 3% (C12) → s03c [chart3d]; parking on 85%, 2 spaces/home (C14) → s03d [scene3d]; IBC: 3 stories, 4 homes/floor (C15) → s04c [scene3d]; 2nd stair: 7% floor, 6–13% cost (C16) → s04f [chart3d]; Seattle: 6 stories (since 1977) (C18) → s04i [map]; NYC 4,440 single-stair buildings (C20) → s05d [chart3d]; 4 deaths 2012–2024 (C21) → s05d [chart3d]; ICC vote 86–34 (C25) → s05g [chart3d]; 1–4 vs 5+ line (C26) → s06a2 [scene3d]; FHA ≥51% residential (C30) → s06e [scene3d]; ~10% commercial-code premium (CA) (C57) → s04l [chart3d]; 2–4 completions 86k→45k, 41k→9k, 16k (C60) → s08b [chart3d]; share 5.9% → 1.1% (C36) → s08d [chart3d]; 5–19 units 377k → 48k (C35) → s08e [chart3d]; 1-unit share 57% → 68% (C63) → s08f [chart3d]; 50+ units 20% → 57% (C34) → s08g [chart3d]; Minneapolis 317 / 12,335 (2%) (C39) → s09d [chart3d]; SB 9: 211 vs 7 (C41) → s09g [chart3d]; Urban +0.8% (C43) → s09i [chart3d]; Auckland ~21,800 (4%) (C44) → s09j [map]; Oregon ≥25,000 (C46) → s10d [map]; Washington 2–6 per lot (C47) → s10e [map]; Texas 6 stories (C50) → s10f [map]; Colorado 5 stories by 2027 (C51) → s10g [map]; 11 million homes, >8 in 10 rented (C53) → s11c [chart3d]
