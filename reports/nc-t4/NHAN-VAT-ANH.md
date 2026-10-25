# NC-T4 — Chân dung nhân vật và ảnh City of London 1850–1950 (nghiên cứu, tải bản PD)

Ngày truy cập mọi mục: 25/10/2026. Phiên xưởng nghiên cứu: không sinh ảnh AI, không commit/push, không đọc `checks/`.
Bằng chứng từng mục: `channel-k2/k2c-t4-02/nc/licenses/<id>.json` (siêu dữ liệu NGUYÊN VĂN của nơi giữ trong `raw_metadata_verbatim`, cùng `source_url`, `api_url`, `accessed`, `licence_quote_verbatim`, SHA-256 và kích thước tệp gốc). Bản thu ≤ 2 400 px, JPEG q≈88 (≤ 5 MB) nằm trong `channel-k2/k2c-t4-02/nc/anh/<id>.jpg`. Tệp gốc nằm ngoài git ở `/var/tmp/nc-t4/goc/<id>/` (326 MB). SHA nằm trong `nc/licenses/SHA256-NC.txt` (21 ảnh + 2 trang bằng chứng Hooke).
Đã quét email trên mọi tệp json/html/txt: những gì lấy về đã được che bằng `[email-đã-che]`. Bản thu Pepys có một chuỗi nhị phân ngẫu nhiên khớp mẫu email, nên đã tái mã ở q87 để bước kiểm trước commit không chặn nhầm.
Công cụ tải (để tái tạo): `/tmp/claude-0/.../scratchpad/bin/tai_nc.py`. Đây là tệp tạm ngoài repo; phiên P quyết định có chép vào `scripts/k2ldn/` hay không.

> **Luật bible:** M-d **không được dựng** nhân vật lịch sử có tên. Vì vậy chân dung dưới đây chỉ dùng cho **thẻ nhân vật (≤ 5 s, ảnh tư liệu tĩnh, có ghi công)**. Khi dùng làm tham chiếu cho ảnh đầu Omni, chỉ được lấy **trang phục, tóc giả, cổ áo, chất liệu thời kỳ** cho người **vô danh**. Không lấy khuôn mặt, không làm "giống" người có tên.

## §1. Chân dung

| Người | Mục | Nơi giữ · số hiệu | Giấy phép (nguyên văn) | Bằng chứng | Tệp `nc/anh` | Rủi ro | Đề xuất dùng |
|---|---|---|---|---|---|---|---|
| **Charles II** (bản vẽ màu tốt hơn bản khắc Rijks đang giữ) | Samuel Cooper (1608–1672), tiểu hoạ chân dung vẽ từ người thật, màu nước trên giấy da | The Met 62.122.21 (objectID 435943) | `"isPublicDomain": true` (Met Open Access CC0) | `met-435943-charles2-cooper.json` | `met-435943-charles2-cooper.jpg` (gốc 2490×2958) | thấp | Thẻ Charles II (≤ 5 s). Mẫu cho trang phục cổ áo ren và tóc giả thập niên 1660 của người vô danh. Bản khắc `rijks-charles2` (đã giữ) để dự phòng. |
| **James, Duke of York (James II)** | David Loggan (1633–1692), *Portret van koning Jacobus II*, bản khắc | Rijksmuseum RP-P-1962-185 | linked-art: `https://creativecommons.org/publicdomain/mark/1.0/`, `https://creativecommons.org/publicdomain/zero/1.0/` | `rijks-200221267-james2-loggan.json` | `rijks-200221267-james2-loggan.jpg` (gốc 3872×6308) | thấp (Rijks ghi niên đại rộng 1643–1692; tiêu đề gọi "koning", nên có thể khắc sau 1685, muộn hơn năm 1666) | Thẻ "Duke of York" chỉ khi chú thích không ghi năm 1666 cho ảnh. Mẫu trang phục quý tộc. Dự phòng tuổi trẻ: Met 361554 (Hollar 1651, `isPublicDomain` true, **chưa tải**). |
| **Samuel Pepys** | *Samuel Pepys. Colour process print* (in màu cơ học, chụp lại tranh sơn dầu) | Wellcome Collection puwvaf8q / V0004604 (ref. 7777i) | `{"id": "pdm", "type": "License", "label": "Public Domain Mark", "url": "https://creativecommons.org/share-your-work/public-domain/pdm/"}` | `wellcome-puwvaf8q-pepys.json` | `wellcome-puwvaf8q-pepys.jpg` (gốc 2480×2944) | **vừa**: Wellcome ghi bản in "After a painting that exists in two versions…" (Ingamells, *later Stuart portraits 1685–1714*), tức Pepys **về già, sau 1685**, không phải Pepys 33 tuổi năm 1666; năm in không ghi | Thẻ Pepys chấp nhận được nếu chú thích không gắn với năm 1666. **Không có** bản Hayls 1666 sạch quyền: tranh ở NPG London (bị chặn và ảnh có điều khoản NC-ND); bản LoC 2005685252 "Reproduction of painting by John Hayls" có `Rights status not evaluated` nên không dùng. |
| **John Evelyn** | Robert Nanteuil, *John Evelyn. Line engraving … 1706, after himself* (Nanteuil vẽ Evelyn từ người thật ở Paris năm 1650) | Wellcome b6zd76cd / V0001805 | `{"id": "pdm", "type": "License", "label": "Public Domain Mark", …}` | `wellcome-b6zd76cd-evelyn-nanteuil.json` | `wellcome-b6zd76cd-evelyn-nanteuil.jpg` (gốc 2448×3370) | thấp | Thẻ Evelyn. Thay cho phương án RMG/Commons (rủi ro vừa) đã ghi ở RIGHTS-NHAP. |
| **Christopher Wren** | đã giữ: `nga-wren` (John Smith theo Kneller, NGA CC0) | NGA 2001.118.55 | (xem `licenses/nga-wren`) | đã có | — | thấp | Thẻ Wren. Không tải lại. |
| **Joseph Bazalgette** | *Portret van de ingenieur Joseph William Bazalgette*, ảnh chân dung c. 1862–1867, tác giả vô danh (trang album) | Rijksmuseum RP-F-F25409-Q | linked-art: `…/publicdomain/mark/1.0/`, `…/publicdomain/zero/1.0/` | `rijks-200348829-bazalgette.json` | `rijks-200348829-bazalgette.jpg` (gốc 2588×3569, cả trang album; phần ảnh chỉ ≈ 1/3 khung, cần cắt, còn khoảng 800–900 px) | thấp (tác giả vô danh, chụp trước 1956 hơn 70 năm nên PD ở Anh). Độ phân giải là điểm yếu. | Thẻ Bazalgette (khung nhỏ, có viền album). Ứng viên thay thế cùng nguồn: Rijks 200646243, 200648650, 200649268 (chưa tải). |
| **Winston Churchill** | *Winston Churchill*, ảnh ngồi bàn làm việc, 1943 Mar. | LoC FSA/OWI 2017696565 | `The contents of the Library of Congress Farm Security Administration/Office of War Information Black-and-White Negatives are in the public domain and are free to use and reuse.` | `loc-2017696565-churchill-1943.json` | `loc-2017696565-churchill-1943.jpg` (**chỉ 856×1024**: LoC chỉ có bản JPEG này, tệp TIFF 351×420) | **vừa**: năm 1943 chứ không phải 1940; ảnh có thể là ảnh chính thức Anh được OWI chép lại. Nếu vậy là Crown copyright, chụp trước 1957 nên đã hết hạn. Độ phân giải thấp. | Chỉ dùng thẻ nhỏ. Để có ảnh năm 1940 cần IWM (Crown, đã hết hạn) qua Commons, nhưng Commons bị 429 (xem §4). Dự phòng: LoC 2017696077 (1941, ghi chú "Image source: Official British photo", cùng câu quyền FSA/OWI; chưa tải). |

## §2. Người không có chân dung xác thực hoặc chưa tìm được bản sạch quyền → **chỉ thẻ chữ, không dựng mặt**

| Người | Kết luận | Nguồn / trích nguyên văn |
|---|---|---|
| **Robert Hooke** | Không có chân dung xác thực | Royal Society, blog "Hooke, Newton, and the 'missing' portrait" (Felicity Henderson, 03/12/2010): *"There are no known portraits of Robert Hooke - but is Isaac Newton to blame?"*; *"The inventory of Hooke's possessions after his death does not include a portrait."*; *"And if a portrait did exist, there is no evidence that it was given to the Royal Society."* Bằng chứng: `nc/licenses/hooke-rs-trang.html` (sha256 gốc 583dc325…). PBS NewsHour (27/07/2020): *"The absence of any contemporary portrait of Hooke stands out…"*; *"This blunder was made by historian Lisa Jardine when in 2004 she misidentified a portrait of 17th-century chemist Jan Baptist Van Helmont as being Hooke."* Bằng chứng: `nc/licenses/hooke-pbs-trang.html`. Bức "Portrait of a Mathematician" của Mary Beale chỉ là **giả thuyết** (PBS), **không dùng**. |
| **Thomas Bludworth** (Lord Mayor 1666) | Không tìm được chân dung trong Met, Rijksmuseum, Wellcome, LoC. Kiểm NPG London thì bị Cloudflare 403. **Chưa** chứng minh được là không tồn tại chân dung. | Tìm kiếm web không có nguồn nào nói về chân dung. Đề xuất chủ dự án tra tay NPG, Guildhall Art Gallery và Vintners' Company. Hiện tại → thẻ chữ. |
| **Nicholas Barbon** | Không tìm được (Wellcome "Barbon" chỉ ra kết quả nhiễu, Rijks và LoC không có) | Giữ giả định ban đầu: không có chân dung đáng tin → thẻ chữ. |
| **Godfrey Allen** (Surveyor of the Fabric, St Paul's 1931–56) | Không có mục nào trong LoC, Wellcome, Rijks, Met | Ảnh (nếu có) nhiều khả năng còn bản quyền hoặc do St Paul's giữ → thẻ chữ. |
| **Charles Holden** (mất 1960) | Không có ảnh PD trong các nguồn đã tra; ảnh chụp sau 1956 hoặc tác giả mất sau 1956 thì còn bản quyền | → thẻ chữ |
| **William Holford** (mất 1975) | Không có | → thẻ chữ |
| **Walter Matthews** (Dean of St Paul's) | Wikipedia có `pageimage: Walter_Matthews.jpg` nhưng **không xác minh được** vì Commons bị 429. LoC, Wellcome không có. | Chủ dự án tải tay trang Commons nếu muốn dùng; hiện tại → thẻ chữ. |

## §3. Ảnh 1850–1950 (và 1 bản vẽ kỹ thuật)

Luật Anh: PD khi tác giả mất trước 1956, hoặc tác giả vô danh và ảnh làm cách đây hơn 70 năm. Photochrom là ảnh chụp không rõ tên (Photoglob Zürich / Detroit Publishing Co.).

| # | Chủ đề | Năm | Người chụp (năm mất) | Nơi giữ · ID | Giấy phép (nguyên văn) | Gốc (px) | Tệp `nc/anh` | Phục vụ shot |
|---|---|---|---|---|---|---|---|---|
| 1 | London Bridge (cầu Rennie 1831), photochrom màu | c. 1890–1900 | vô danh (Detroit Publishing Co. / Photoglob) | LoC 2002696930 | `No known restrictions on publication.` | 3670×2727 (TIFF 30 MB) | `loc-2002696930-londonbridge-pc.jpg` | **H3-02** |
| 2 | London Bridge, có chữ quảng cáo Boehm's soap ở lề (cần cắt) | 1899–1901 | vô danh | Rijks RP-F-F00827-IB | `…/publicdomain/zero/1.0/` | 3279×2296 | `rijks-200355251-londonbridge-1900.jpg` | H3-02 (dự phòng, ảnh đen trắng) |
| 3 | Thames Embankment, photochrom | c. 1890–1900 | vô danh | LoC 2002696941 | `No known restrictions on publication.` | 3668×2738 | `loc-2002696941-embankment-pc.jpg` | **H3-03** (kè đã hoàn thành) |
| 4 | Victoria Embankment nhìn về Waterloo Bridge | 1851–1890 | vô danh | Rijks RP-F-F16350 | `…/publicdomain/mark/1.0/`, `…/zero/1.0/` | 6534×3958 | `rijks-200324875-embankment-waterloo.jpg` | H3-03 |
| 5 | *Construction drawings for the Thames Embankment* (Temple Steam Boat Pier), bản vẽ màu theo Bazalgette — **không phải ảnh** | 1865 | J. Bazalgette (1819–1891) | Wellcome uv3mugch / V0024386 | `{"id": "pdm", … "label": "Public Domain Mark" …}` | 3048×2386 | `wellcome-uv3mugch-embankment-1865.jpg` | H3-03 (lớp kỹ thuật: mặt cắt cống và kè) |
| 6 | St Paul's, mặt tây, photochrom | c. 1890–1900 | vô danh | LoC 2002696932 | `No known restrictions on publication.` | 2791×3659 | `loc-2002696932-stpauls-pc.jpg` | **H3-01** |
| 7 | St Paul's & Blackfriars Bridge (nhìn từ sông) | 188- | G.W. Wilson & Co. (G.W. Wilson mất 1893) | LoC 2004678933 | `No known restrictions on publication.` | **8773×6935** (TIFF 182 MB) | `loc-2004678933-stpauls-blackfriars-gww.jpg` | **H3-01** (mái vòm nhìn từ sông, độ phân giải tốt nhất) |
| 8 | Sông Thames với St Paul's | 1892 | vô danh | Rijks RP-F-F01852 | PDM + CC0 | 6226×3878 | `rijks-200323435-theems-stpauls-1892.jpg` | H3-01 / bến sông |
| 9 | Sông Thames với St Paul's (toàn cảnh mép sông) | 1855–1900 | vô danh | Rijks RP-F-F16351 | PDM + CC0 | 5314×4384 | `rijks-200324876-theems-stpauls.jpg` | H3-01, bến sông |
| 10 | St Paul's, ảnh lập thể (stereo) | 1850s–1910s | E. Ryder (không rõ năm mất) | The Met 1982.1182.938 | `"isPublicDomain": true` | 4000×1990 | `met-288279-stpauls-ryder.jpg` | H3-01 (dự phòng) |
| 11 | Cheapside, photochrom | c. 1890–1900 | vô danh | LoC 2002696937 | `No known restrictions on publication.` | 2727×3670 | `loc-2002696937-cheapside-pc.jpg` | phố City / H3-04 (trước) |
| 12 | Cheapside với St Mary-le-Bow | 1878–1890 | Francis Godolphin Osbourne Stuart (c.1843–1923) | Rijks RP-F-F01212-12-3 | PDM + CC0 | 2500×1782 | `rijks-200561138-cheapside-stuart.jpg` | phố City |
| 13 | Ludgate Hill, ảnh lập thể | 1892 | vô danh | Rijks RP-F-F07788 | PDM + CC0 | 4888×2306 | `rijks-200337941-ludgate-1892.jpg` | Ludgate → St Paul's |
| 14 | Fleet Street | 1895-08 | vô danh | Rijks RP-F-00-8439 | PDM + CC0 | 5544×4138 | `rijks-200632748-fleetstreet-1895.jpg` | Fleet St → St Paul's |
| 15 | Mansion House & Cheapside (bưu thiếp Valentine's Series) | 1902–ca. 1930 | vô danh (Valentine & Sons) | Rijks RP-F-00-15716 | `…/publicdomain/zero/1.0/` | 2592×1687 | `rijks-200794890-mansionhouse-cheapside.jpg` | **H3-04** (gần nhất với thập niên 1930 tìm được) |

**Khoảng trống:** (a) không có **ảnh** thi công Embankment thập niên 1860 có giấy phép rõ. Ảnh nổi tiếng của Henry Flather do Museum of London giữ, không thuộc open access; tạm dùng bản vẽ 1865 (#5). (b) Không có ảnh City **thập niên 1930** sạch quyền: các ảnh lập thể Keystone 1926–1931 ở LoC (2019639045, 2019639044, 2019637311) ghi `Rights status not evaluated` / `Publication may be restricted.` / "Copyrighted, Keystone View Company" nên **không dùng**. (c) Ảnh LoC 91789510 "Raid on London… Ludgate Hill" (1940, OEM/OWI) có trường quyền **rỗng**, nên chưa dùng; cần xác minh thêm.

## §4. Trang và nguồn bị chặn

| URL | Mã lỗi | Đề xuất |
|---|---|---|
| `https://www.npg.org.uk/…` (person-list Bludworth, person mp00406, trang giấy phép CC) | 403 Cloudflare ("Just a moment…"), cả qua WebFetch | Chủ dự án mở tay để: (1) chép câu giấy phép CC BY-NC-ND của NPG (ảnh NPG **không dùng được** cho phim bán vì NC-ND; câu nguyên văn **chưa lấy được**), (2) kiểm chân dung Bludworth và Barbon. |
| `https://commons.wikimedia.org/w/api.php` và `https://en.wikipedia.org/w/api.php` | 429 lặp lại (kể cả khi giãn 12 s mỗi lượt) | Chủ dự án tải tay: ảnh IWM Churchill 1940 (Crown, đã hết hạn), trang `File:Walter_Matthews.jpg`, bài Wikipedia về Bludworth, Barbon, Holden. Trang lỗi 429 có chứa email nên **không lưu**. |
| `https://tile.loc.gov/image-services/iiif/service:pnp:ppmsca:06800:06814u/full/pct:50/…` | 404 | Đã thay bằng TIFF gốc 182 MB (đã tải thành công). |
| Met `/public/collection/v1/search` | ngừng hoạt động từ 01/10/2026 (thông báo của API) | Đã dùng `/v1.1/search`. Script `scripts/k2ldn/tai_tu_lieu.py` không bị ảnh hưởng (chỉ gọi `/objects`). |
| Smithsonian Open Access (DEMO_KEY) | 200 nhưng không có kết quả liên quan | — |

## §5. Rủi ro

1. **Pepys:** bản Wellcome là Pepys **sau 1685**. Nếu thẻ đặt ở cảnh 1666, đó là sai lệch niên đại. Cần chủ dự án quyết: chấp nhận kèm chú thích không ghi năm, hoặc chỉ dùng thẻ chữ.
2. **Churchill:** ảnh năm 1943, chỉ 856×1024. Nguồn gốc có thể là ảnh chính thức Anh, đã hết Crown copyright, nhưng LoC không ghi rõ. Rủi ro vừa.
3. **James II:** chưa xác định năm khắc (Loggan, 1643–1692); có thể sau năm 1666.
4. **Bazalgette:** ảnh nhỏ trong trang album; nếu phóng to khi cắt sẽ lộ hạt. Nên cân nhắc 3 ảnh dự phòng cùng nguồn Rijks.
5. **Rijks:** câu giấy phép lấy ở cấp đối tượng (PDM cho đối tượng, CC0 cho siêu dữ liệu); có 2 mục có thêm câu ở cấp digital object. Một số ảnh chỉ có CC0 (#2, #15). Mức rủi ro: thấp.
6. **Photochrom** là ảnh in màu cơ học, màu đã chỉnh tay từ thời đó. Không được dùng làm dữ kiện màu thật (bậc tham chiếu không khí).
7. **Ảnh lập thể** (#10, #13) có 2 khung; cần cắt lấy 1 khung, độ phân giải thực còn khoảng một nửa.
8. **Luật M-d:** chân dung không được làm đầu vào để dựng mặt người có tên trong Omni hay bất kỳ công cụ nào. Chỉ dùng tham chiếu trang phục cho người vô danh.
9. Tổng dung lượng đã tải là 326 MB (≤ 1 GB); đĩa còn trống 16 GB.

## Việc đang chờ chủ dự án
- Duyệt dùng thẻ Pepys (sau 1685), Churchill (1943) và James (năm chưa rõ).
- Tải tay nguồn bị chặn (§4): câu giấy phép NPG; ảnh IWM Churchill 1940 qua Commons; ảnh Walter Matthews.
- Phiên P chép các dòng §1 và §3 vào `RIGHTS.md` sau khi duyệt.
