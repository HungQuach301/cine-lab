# NC-T4: Footage London miễn phí cho H5 (truy cập 25/10/2026)

Phạm vi: chỉ nghiên cứu. Không tải file video, không mua, không commit. Bản thô lưu ở `reports/nc-t4/nguon/web/footage-*.txt|json`. Dữ liệu máy đọc nằm ở `reports/nc-t4/footage-2026.json`.

**Mức độ chắc chắn:**
- Với Commons, tôi đã xem khung hình tĩnh (thumbnail `seek=` của Wikimedia, không tải video) của 6 file nên góc máy đã kiểm. Giấy phép lấy từ `extmetadata` của API, nguyên văn.
- Với Pexels, Pixabay, Getty và Storyblocks, tôi chỉ đọc metadata qua WebFetch, chưa xem khung hình. Góc máy chỉ suy từ tiêu đề và mô tả.
- Các câu trích từ trang giấy phép Pexels/Pixabay đi qua công cụ tóm tắt (mỗi đoạn trích tối đa 125 ký tự), **chưa đối chiếu với HTML gốc** vì curl bị 403.

## §1. Wikimedia Commons

Cách tìm: chạy 24 truy vấn `filetype:video` (St Paul's, City of London, Millennium Bridge, Leadenhall, Bankside, Monument, Barbican, Embankment, Fleet Street, drone/aerial/timelapse…). Ngoài ra liệt kê `Category:Videos from London` (125 mục). Bốn category nêu trong đề bài đều trả **0 thành viên**: "Videos of the City of London", "Videos of St Paul's Cathedral", "Videos of the River Thames in London", "Time-lapse videos of London".

**Kết luận chung:** Commons không có clip CC0/PD nào mới về City hay St Paul's. Ứng viên tốt nhất là các bản nhập từ YouTube theo CC BY 3.0, và một số clip BY-SA 4.0 của Acabashi quay năm 2025–2026.

| ID | File (trang Commons) | LicenseShortName / UsageTerms (nguyên văn) | Tác giả | Ngày | Độ phân giải, thời lượng | Góc máy (đã xem khung hình?) | Khớp H5 | Rủi ro |
|---|---|---|---|---|---|---|---|---|
| C1 | [Timelapse from Waterloo Bridge, London](https://commons.wikimedia.org/wiki/File:Timelapse_from_Waterloo_Bridge,_London.webm) | CC BY 3.0 / "Creative Commons Attribution 3.0" | nabs | Mô tả: "The view facing East, April 2016" | 3240×2160 (3:2), 23,7 s, không tiếng | Từ cầu Waterloo nhìn về phía đông. Mái vòm St Paul's bên trái, cụm tháp City (Walkie-Talkie, Leadenhall, Tower 42) ở giữa, chuyển từ hoàng hôn sang đêm (**đã xem 3 khung**) | H5-05a (góc thay thế), H5-07a/b | Nằm trong category "License review needed (video)", tức chưa ai xác nhận nguồn YouTube. Skyline năm 2016 thiếu 22 Bishopsgate. Không quay từ Bankside. Phải crop sang 16:9 |
| C2 | [Aerial footage of London … River Thames](https://commons.wikimedia.org/wiki/File:Aerial_footage_of_London,_United_Kingdom_featuring_London_Tower,_Downtown_London,_London_Bridge,_River_Thames.webm) | CC BY 3.0 / "Creative Commons Attribution 3.0" | the Dronalist | 2022-12-31 | 3840×2160, 8 phút 36 s | Drone. Ở khoảng giây 270: bay trên rìa đông City nhìn về tây, thấy Walkie-Talkie và mái vòm St Paul's ở xa. Ở giây 90/390: Tower Bridge với cụm tháp và The Shard (**đã xem 8 khung**) | H5-06; H5-04 (góc thay thế) | "License review needed (video)". Chưa kiểm được giấy phép bay drone trên City. Nắng đông thấp |
| C3 | [London Timelapse 4K](https://commons.wikimedia.org/wiki/File:London_Timelapse_4K.webm) | CC BY 3.0 / "Creative Commons Attribution 3.0" | manish ramrakhani | 2019-01-05 (quay từ cuối tháng 10/2018) | 3840×2160, 2 phút 21 s | Dựng ghép nhiều cảnh. Giây ~60: cụm tháp City về đêm nhìn qua sông từ bờ nam gần Tower Bridge. Giây ~80: mặt tây St Paul's có cây thông Noel. Mở đầu bằng title card (**đã xem 7 khung**) | H5-07 (góc đông), H5-06 (một phần) | "License reviewed by YouTubeReviewBot" (giấy phép đã được bot xác nhận). Chỉ dùng được vài giây. Chưa kiểm có nhạc hay không |
| C4 | [Mercuria tour boat … Bankside … video](https://commons.wikimedia.org/wiki/File:Mercuria_tour_boat_River_Thames_Bankside_Southwark_Bridge_Cannon_Street_Railway_Bridge_London_England_video.webm) | CC BY-SA 4.0 / "Creative Commons Attribution-Share Alike 4.0" | Acabashi | 2025-09-22 | 1920×1080, 81 s | Từ Bankside ngang mặt nước nhìn sang bờ bắc: cầu Southwark, tàu, cầu Cannon Street (**đã xem 2 khung**) | B-roll Bankside/sông, chèn vào H5-08 | BY-SA (xem §2). Thương hiệu trên tàu. Chỉ 1080p |
| C5 | [Will the last one to leave the City of London… 2009](https://commons.wikimedia.org/wiki/File:Will_the_last_one_to_leave_the_City_of_London_please_switch_off_the_lights_2009.webm) | CC BY-SA 2.0 / "Creative Commons Attribution-Share Alike 2.0" | Lars Plougmann | 2009-03-11 | 1920×1080, 16 s | Cụm tháp đông về đêm (Tower 42, Gherkin) (**đã xem**) | H5-07, chỉ dùng như tư liệu lịch sử | Skyline cũ: chưa có Leadenhall và 22 Bishopsgate. BY-SA |
| C6 | [Liverpool Street Station Bishopsgate … Heron Tower](https://commons.wikimedia.org/wiki/File:Liverpool_Street_Station_Bishopsgate_Hamilton_Hall_Heron_Tower_City_of_London_England.webm) | CC BY-SA 4.0 / "Creative Commons Attribution-Share Alike 4.0" | Acabashi | 2025-09-21 | 1080p, 32 s | Ngang mặt phố Bishopsgate (chưa xem khung) | B-roll mặt phố cho H5-04 | BY-SA. Người qua đường nhận diện được |
| C7 | [2026 London Marathon Upper Thames Street from Blackfriars Bridge…](https://commons.wikimedia.org/wiki/File:2026_London_Marathon_Upper_Thames_Street_from_Blackfriars_Bridge_and_Queenhithe.webm) | CC BY-SA 4.0 / "Creative Commons Attribution-Share Alike 4.0" | Acabashi | 2026-04-26 | 1080p, 119 s | Cuộc chạy marathon (chưa xem khung) | Không khớp trực tiếp | Đám đông. BY-SA |
| C8 | [THE SHARD, London, UK 4K](https://commons.wikimedia.org/wiki/File:THE_SHARD,_London,_UK_4K.webm) | CC BY 3.0 / "Creative Commons Attribution 3.0" | Kauko Helavuo | 2015-06-28 | 1920×1080, 12 phút 19 s | Từ trong The View from The Shard, nhìn qua kính về phía bắc xuống City (**đã xem**) | H5-04 (cũ) | Watermark "© Kauko Helavuo" in cứng vào hình. Phản chiếu kính. Quay năm 2015 |
| C9 | [Hungerford Bridge, London, lighting at night 2022-01-07](https://commons.wikimedia.org/wiki/File:Hungerford_Bridge,_London,_lighting_at_night_2022-01-07.webm) | CC BY-SA 4.0 / "Creative Commons Attribution-Share Alike 4.0" | The wub | 2022-01-07 | 1080p, 12 s | Cầu Hungerford chiếu sáng đêm (Illuminated River), cạnh Victoria Embankment | B-roll đêm bổ trợ | BY-SA. Bản thân hệ đèn có thể là một tác phẩm riêng (chưa kiểm) |
| C10 | [London City Tour , England](https://commons.wikimedia.org/wiki/File:London_City_Tour_,_England.webm) | CC BY 3.0 / "Creative Commons Attribution 3.0" | Le Monde en Vidéo | Quay 24–25/06/2015 | 3840×2160, 25 phút 41 s | Tour xe buýt và du thuyền (chưa xem khung) | Chưa rõ | "License review needed (video)". Quay năm 2015 |

Đã loại: "Practising Decents With A View Of London" (hướng BT Tower, không phải City); "Carol Williams visits St Pauls Cathedral" (là St Paul's ở San Diego); các file "Kin/WP25" (quảng cáo Wikipedia); "Google Timelapse" (ảnh vệ tinh).

## §2. Rủi ro CC BY-SA khi dùng trong phim phái sinh

Trích nguyên văn từ legal code BY-SA 4.0 (`footage-cc-by-sa-4-legalcode.txt`), Section 1:
> "Adapted Material means material subject to Copyright and Similar Rights that is derived from or based upon the Licensed Material and in which the Licensed Material is translated, altered, arranged, transformed, or otherwise modified in a manner requiring permission under the Copyright and Similar Rights held by the Licensor. For purposes of this Public License, where the Licensed Material is a musical work, performance, or sound recording, Adapted Material is always produced where the Licensed Material is synched in timed relation with a moving image."

Section 3(b), ShareAlike:
> "In addition to the conditions in Section 3(a), if You Share Adapted Material You produce, the following conditions also apply. The Adapter's License You apply must be a Creative Commons license with the same License Elements, this version or later, or a BY-SA Compatible License."
> "You may not offer or impose any additional or different terms or conditions on, or apply any Effective Technological Measures to, Adapted Material that restrict exercise of the rights granted under the Adapter's License You apply."

Bản BY-SA 3.0 (`footage-cc-by-sa-3-legalcode.txt`) định nghĩa "Adaptation" là gồm cả "cinematographic adaptations", và:
> "except that a work that constitutes a Collection will not be considered an Adaptation for the purpose of this License."

"Collection" chỉ áp dụng khi tác phẩm được đưa vào "in its entirety in unmodified form along with one or more other contributions, each constituting separate and independent works in themselves".

FAQ của CC (`footage-cc-faq.txt`), mục "When is my use considered an adaptation?":
> "Whether a modification of licensed material is considered an adaptation for the purpose of CC licenses depends primarily on the applicable copyright law."
> "Under CC licenses, synching music in timed relation with a moving image is always considered an adaptation, whether or not it would be considered so under applicable law."

Mục về trích đoạn:
> "Incorporating an unaltered excerpt from an ND-licensed work into a larger work only creates an adaptation if the larger work can be said to be built upon and derived from the work from which the excerpt was taken. Generally, no derivative work is made of the original from which the excerpt was taken when the excerpt is used to illuminate an idea or provide an example in another larger work."

Mục về collection:
> "When you include CC-licensed content in a collection, you still must adhere to the license conditions governing your use of the material incorporated."

**Diễn giải.** Đây là nhận định nghiên cứu, không phải ý kiến pháp lý:
1. Quy tắc "đặt khớp thời gian với hình động thì luôn là bản phỏng tác" chỉ áp dụng cho **nhạc, bản ghi âm và buổi biểu diễn**. Văn bản không nói cắt một clip **video** vào phim thì mặc nhiên là phỏng tác. Việc đó do luật bản quyền nơi áp dụng quyết định.
2. Trên thực tế, phim của ta sẽ **cắt, crop sang 16:9, chỉnh màu, đổi tốc độ** clip. Như vậy clip bị "altered … transformed", gần như chắc chắn thành Adapted Material, và không còn là "unmodified form" để được coi là Collection theo bản 3.0.
3. Nếu clip là Adapted Material thì giấy phép của **phần đóng góp phỏng tác** phải là BY-SA, và không được áp DRM hay điều khoản hạn chế. Phần này có thể bị hiểu là cả bộ phim hoặc ít nhất đoạn chứa clip. Điều này **xung đột với việc bán phim kèm DRM hoặc điều khoản thương mại độc quyền**, và với YouTube (YouTube không cho chọn giấy phép BY-SA; Content ID có thể áp hạn chế).
4. **Đề xuất:** không dùng clip BY-SA trong bản phát hành bán. Ưu tiên CC BY và giấy phép Pexels/Pixabay (không share-alike). Nếu bắt buộc phải dùng BY-SA thì cần ý kiến luật sư, hoặc xin tác giả (ví dụ Acabashi) một giấy phép riêng.
5. Với clip CC BY 3.0, phải ghi công đầy đủ (tác giả, tiêu đề, URL, giấy phép, ghi chú đã chỉnh sửa) trong credits và trong `RIGHTS.md`. Các file mang nhãn "License review needed (video)" (C1, C2, C10) phải **tự kiểm trang YouTube gốc** xem có thực sự là CC BY không trước khi dùng.

## §3. Pexels và Pixabay: giấy phép và ứng viên

Bản thô ở `footage-licence-webfetch.txt`. curl trả **403** cho cả hai site. WebFetch đọc được, nhưng các trích dẫn dưới đây do công cụ trả về, **chưa đối chiếu với HTML gốc**.

**Pexels** ([license](https://www.pexels.com/license/) và [terms-of-service](https://www.pexels.com/terms-of-service/), Section 5):
- "All photos and videos on Pexels are free to use."
- "we grant you an irrevocable, worldwide, perpetual (or as long as allowed by law), non-exclusive and royalty-free right"
- "download, use, copy, modify or adapt the Content for commercial or non-commercial purposes"
- "Don't sell unaltered copies of a photo or video"
- "You cannot sell or distribute the Content (either in digital or physical form) on a Standalone basis."
- "by suggesting that any depicted person, brand, organization or other third party endorses or is affiliated with you"
- "We do not warrant that any consents or licenses have been obtained in relation to any Content,"
- "Responsibility for determining whether permissions are needed always rests solely and exclusively with you."

**Pixabay** ([license-summary](https://pixabay.com/service/license-summary/) và [terms](https://pixabay.com/service/terms/), Section 5):
- "Use Content for free"
- "Use Content without having to attribute the author"
- "Modify or adapt Content into new works"
- "You cannot sell or distribute Content (either in digital or physical form) on a Standalone basis."
- "If Content depicts any trademarks, logos or brands (whether two- or three-dimensional),"
- "you cannot use that Content for commercial purposes in relation to goods and services"
- "certain Content (including CC0 Content) may be subject to additional intellectual property rights"
- "We do not warrant that any consents or licenses have been obtained in relation to any Content,"

**Đánh giá:** cả hai giấy phép cho phép đưa clip vào một phim thương mại đã được biên tập. Phim không phải là bán clip "Standalone". Không yêu cầu share-alike hay ghi công, nhưng nên ghi công. Rủi ro còn lại là **không có bảo đảm về người và nhãn hiệu xuất hiện trong hình**, và không có cam kết bồi thường (indemnity).

**Chủ dự án nên tự mở 3 trang giấy phép trên trình duyệt và lưu bản PDF** để có văn bản nguyên văn đầy đủ.

Ứng viên (chưa xem khung hình; chi tiết trong `footage-stock-candidates.txt`):

| ID | URL | Tác giả | Ngày | Độ phân giải, fps, thời lượng | Góc máy (theo mô tả) | Khớp H5 |
|---|---|---|---|---|---|---|
| P1 | [Walking across Millennium Bridge to St Paul's](https://www.pexels.com/video/walking-across-millennium-bridge-to-st-paul-s-37601950/) | Florian Delée | 15/05/2026 | 3840×2160, 25 fps, 0:13 | Đi bộ trên cầu Millennium, nhìn về St Paul's | **H5-05a** (nếu máy đủ ổn định) |
| P2 | [London Skyline Time-Lapse](https://www.pexels.com/video/london-skyline-time-lapse-11328858/) | Tom Shearwood | 28/02/2022 | 3840×2160, 60 fps, 0:13 | Timelapse skyline từ ngày sang đêm | H5-07 (cần xem có City không) |
| P3 | [Downtown London at Night](https://www.pexels.com/video/downtown-london-at-night-5844901/) | George Morina | 10/11/2020 | 3840×2160, 29,97 fps, 0:21 | Đèn skyline phản chiếu trên sông Thames | H5-07 |
| P4 | [Time Lapse Video of City of London](https://www.pexels.com/video/time-lapse-video-of-city-of-london-6789136/) | JustAlex Himself | 11/02/2021 | 1920×1080, 23,98 fps, 0:08 | Từ hoàng hôn sang đêm | H5-07 |
| P5 | [St Paul's Cathedral Dome](https://www.pexels.com/video/st-paul-s-cathedral-dome-6138314/) | Sam Jae | 09/12/2020 | 3840×2160, 23,98 fps, 0:08 | Cận cảnh mái vòm | Cảnh chèn mái vòm |
| P6 | [London Skyline at Sunset: Shard and Walkie-Talkie](https://www.pexels.com/video/london-skyline-at-sunset-iconic-shard-and-walkie-talkie-34313773/) | Steven Duque | 15/10/2025 | 3840×2160, **24 fps**, 0:14 | Skyline lúc hoàng hôn | H5-04 hoặc H5-07 |
| P7 | [Nighttime View of London Skyline](https://www.pexels.com/video/nighttime-view-of-london-skyline-35330810/) | Dominik Gryzbon | 22/12/2025 | 1920×1080, 24 fps, 0:09 | Có một phụ nữ trên cầu trong khung hình | H5-07 (rủi ro người nhận diện được) |
| X1 | [River, London, South Bank, St Pauls](https://pixabay.com/videos/river-london-south-bank-st-pauls-176408/) | Whitechappel79 | 17/08/2023 | 1920×1080, 23 fps | Tag: South Bank, St Pauls, Night | **H5-07a/b** |
| X2 | [London, City, UK](https://pixabay.com/videos/london-city-uk-summer-warm-clouds-286089/) | Whitechappel79 | 16/06/2025 | 3840×2160, 24 fps | Không nêu địa danh | Chưa rõ |
| X3 | [Buildings, Skyscrapers, London (night)](https://pixabay.com/videos/buildings-skyscrapers-london-night-287389/) | TungArt7 | 24/06/2025 | 3840×2160, 50 fps | Tag có cả "Bangkok", mâu thuẫn | Cần kiểm địa điểm |

Đã loại vì quay dọc 9:16: Pexels 29300143, 29300146, 32278000, 32215140, 34270993, 34466636, 39835784.

## §4. Báo giá stock trả phí (CHỈ BÁO GIÁ, KHÔNG MUA)

| Nhà cung cấp | Clip | Loại giấy phép | Giá hiển thị | Độ phân giải | Khớp |
|---|---|---|---|---|---|
| Getty | [1441204329: Time lapse of St Paul's Cathedral…](https://www.gettyimages.com/detail/video/time-lapse-of-st-pauls-cathedral-with-tourist-and-people-stock-footage/1441204329) | Royalty-free, "No release required" | Không hiển thị ("Join today to view pricing…") | 3840×2160 ProRes 422 HQ, 30p, 7 s | Cảnh chèn mái vòm, mặt phố |
| Getty | [1405484119: London Skyline over the River Thames at dusk (drone)](https://www.gettyimages.com/detail/video/the-london-skyline-over-the-river-thames-at-dusk-from-a-stock-footage/1405484119) | Royalty-free | Không hiển thị | 3840×2160 ProRes 422 HQ, 30p, 44 s | H5-07 hoặc H5-08 |
| Getty | [1492315874: commuters … St Paul's at twilight](https://www.gettyimages.com/detail/video/footage-time-lapse-of-crowded-commuter-people-walking-in-stock-footage/1492315874) | Royalty-free | Không hiển thị | 4K, 30p, 7 s | Có thể dùng cho H5-05b (mặt phố) |
| Storyblocks | [SBV-354225492: London Skyline At Night](https://www.storyblocks.com/video/stock/london-skyline-at-night-354225492) | Thuê bao | "Sign Up to Download". Bảng giá: Individual $21–30/tháng, Small Business $40/tháng (trả theo năm); Business: "Get a Quote" | 4K ProRes/HEVC, 9 s | H5-07 |

Phạm vi giấy phép:
- **Getty EULA** cho phép "Any and all media" và "Unlimited". Đại lý phân phối được phép "use content in any production or distribution process related to your final project". Văn bản **không nói rõ** về việc bán phim thành phẩm, và trang không nêu bậc "enhanced". Cần hỏi Getty bằng văn bản.
- **Storyblocks:** chỉ gói Business ghi "broadcast, TV, streaming / OTT, and feature films", có indemnity US$1 triệu và "Perpetual use … after your subscription ends" = Yes. Gói Individual chỉ cho YouTube "1x channel", indemnity US$20k, và trang có câu mâu thuẫn về quyền vĩnh viễn. Phim bán thương mại nên cần gói Business, nên phải xin báo giá.
- Getty đều xuất 30p. Phim chạy 24 fps nên phải chuyển nhịp; timelapse ít bị ảnh hưởng.

## §5. Trang bị chặn hoặc lỗi

| URL | Mã / hiện tượng | Đề xuất |
|---|---|---|
| https://www.pexels.com/license/ | curl 403 (WebFetch đọc được nhưng chỉ trích ngắn) | Chủ dự án mở tay và lưu PDF |
| https://pixabay.com/service/license-summary/ | curl 403 | Như trên |
| https://pixabay.com/service/terms/ | curl 403 | Như trên |
| https://www.pond5.com/search?kw=st-pauls-cathedral-millennium-bridge&media=footage | WebFetch 403 | Mở tay nếu cần báo giá |
| https://stock.adobe.com/search/video?k=st+pauls+cathedral+millennium+bridge | WebFetch 403 | Mở tay |
| https://www.shutterstock.com/video/search/st-pauls-cathedral-millennium-bridge | WebFetch trả trang rỗng | Mở tay |
| commons.wikimedia.org/w/api.php | Body "You are making too many requests to the API." (rate limit) | Đã chờ và thử lại có backoff, không vượt rào; đủ 24 truy vấn |
| thumb.wikimedia.org (seek) | 429, 2/28 lần | Bỏ qua 2 khung đó |

## §6. Đề xuất theo shot H5

| Shot | Ứng viên miễn phí tốt nhất | Đánh giá |
|---|---|---|
| H5-04: nhìn từ cao ở Bankside, cụm tháp đông | Không có clip khớp. Tạm dùng C2 (CC BY 3.0, drone 2022, nhìn từ phía đông) hoặc P6 (chưa xem khung) | **Thiếu.** Cần tự dựng, hoặc báo giá stock cho góc Tate Modern / One Blackfriars |
| H5-05a: tầm nhìn được bảo vệ từ bờ nam / cầu Millennium | **P1** (Pexels, 4K, 2026). C1 là góc tương tự từ cầu Waterloo (2016) | P1 phải xem có rung tay không. C1 phải kiểm nguồn YouTube |
| H5-05b: từ Fleet Street nhìn đông, Leadenhall sau mái vòm | **Không tìm thấy** clip miễn phí nào | Thiếu; Getty 1492315874 có thể gần nhưng chưa xác minh góc |
| H5-06: mái vòm giữa cụm tháp nhìn từ phía đông | **C2** (khoảng giây 270) | Mái vòm nhỏ ở xa, cần crop từ 4K |
| H5-07a/b: đêm từ Bankside, đèn City quanh mái vòm | **X1** (Pixabay, tag South Bank / St Pauls / Night), **C1** (hoàng hôn sang đêm, cầu Waterloo), P3, P4 | Phải xem khung X1 trước. C1 là skyline 2016 |
| H5-08: kéo lùi cuối, mái vòm / sông / Bankside | Không có. C4 (BY-SA) chỉ dùng được làm cảnh chèn mặt sông | **Thiếu** |

**Kết luận:** footage miễn phí phủ được tốt nhất H5-05a, H5-06 và H5-07. Ba shot H5-04, H5-05b và H5-08 **không có** nguồn miễn phí đạt chuẩn.

Phim của ta là hoạt hình phong cách hoá, nên footage thật phù hợp nhất ở vai trò **tham chiếu bố cục và ánh sáng** hơn là chèn thẳng vào phim. Việc chèn hay chỉ tham chiếu là quyết định sáng tạo của chủ dự án.

## Việc đang chờ chủ dự án
1. Mở tay và lưu PDF 3 trang giấy phép Pexels/Pixabay; quyết định có cho dùng giấy phép Pexels/Pixabay không.
2. Duyệt nguyên tắc **không dùng BY-SA** trong bản bán.
3. Xem trực tiếp P1, X1, C1, C2 (góc máy, rung, người trong hình) trước khi ghi vào `RIGHTS.md`.
4. Kiểm trang YouTube gốc của C1 và C2 (cả hai mang nhãn "License review needed").
5. Quyết định có xin báo giá Getty hoặc Storyblocks Business cho các shot H5-04, H5-05b, H5-08 không.
