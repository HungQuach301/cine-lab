# Giấy phép chép nguyên văn — NC-BD (đọc 17/10/2026, ~14:20–14:35 UTC, bằng `curl` qua proxy)

Mỗi mục: URL · SHA-256 tệp trang đã tải (tệp thô ngoài git, `~/.cache/nc-bd/lic/`) · trích **nguyên văn** (tiếng gốc). Email trong trang gốc đã che bằng `[email đã che]`. Không phải tư vấn pháp lý.

## 1. OpenHistoricalMap (OHM)
- https://www.openhistoricalmap.org/copyright · SHA `883b6a2b679219107b0c4302a1074d39dfde0a636966ebdaa20261b9fec0a654`
> "Except where otherwise noted, OpenHistoricalMap data is dedicated to the public domain under a Creative Commons CC0 dedication. To the extent that what you use is in the public domain, you are free to copy, distribute, transmit, and adapt it for any purpose, without any restrictions. The OpenHistoricalMap database incorporates some individual map features under copyright. These features are available under an open license, such as Creative Commons Attribution (CC BY) or Creative Commons Attribution-ShareAlike (CC BY-SA), as noted in license=* tags on individual elements. To the extent that you use any significant portion of the database that is covered by a “share alike” license, you should respect the terms of this license in your own adapta[tion]…"
- https://wiki.openstreetmap.org/wiki/OpenHistoricalMap/Reuse · SHA `66c5441ef53f746d962e72419ec6831145cc248e22fe325fb55f86099f04e08e`
> "In general, OpenHistoricalMap data is in the public domain under a CC0 dedication. As a courtesy, please credit OpenHistoricalMap contributors where appropriate. Some individual features may have additional legal requirements around attribution."
- **Kiểm thật thẻ `license=*` trên đường thành phần** (Overpass, 17/10): quan hệ "Spain" 1704 (2860495): **201/298 đường `license=CC-BY-4.0`** (`source` = CNIG "LILIM" — đường địa giới hiện hành của IGN Tây Ban Nha); "Kingdom of France" 1697–1714 (2955283): **85/828 đường CC-BY-4.0**, 1 đường CC0; không thấy đường CC BY-SA trong 3 quan hệ đã kiểm.

## 2. historical-basemaps (aourednik) — GitHub @ `da7a4b735ecef70aebdc9c73e409d8a2500d50f3`
- LICENSE · SHA `8ceb4b9ee5adedde47b31e975c1d90c73ad27b6b165a1dcd80c7c545eb65b903`: **GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007**. Điều liên quan sản phẩm đầu ra (§2):
> "The output from running a covered work is covered by this License only if the output, given its content, constitutes a covered work."
- README · SHA `cbd9b99a5969785c532b901293ad77391223ea3223e1eb042e78a6704f01f76e`:
> "It is __work in progress__: verify the maps by comparison to other sources before using in academic work."
> "This project started as a collection of basemaps collected, adapted and converted from diverse sources, sometimes only available through the wayback machine. Among these sources, anonymous students from the "ThinkQuest Team C006628"."
> "__BORDERPRECISION__ : ordinal values 1 (approximate), 2 (moderately precise) and 3 (determined by international law)."

## 3. Cliopatria (Seshat Global History Databank)
- Zenodo API `https://zenodo.org/api/records/13363121/versions/latest` → bản ghi 23128623, **v0.2.1, 2026-10-03, `"license": {"id": "cc-by-4.0"}`** · SHA `95101d238b09863cad19f74fc017b09ca569a64634678674383cd10f4080bed5`
- README (GitHub `Seshat-Global-History-Databank/cliopatria`, tag v0.2.1 = `5f43337…`):
> "While we strive to reflect the most current historical knowledge, we acknowledge that these maps reflect only one version of the territory held by past polities. Border uncertainties, as well as differing opinions on the names, territorial changes, and durations of polities, are common challenges facing historians."
> "Please note that users and analysts of this map data are solely responsible for assessing its suitability for their specific purposes."
- Tệp đã tải: `cliopatria.geojson.zip` (nhánh main = v0.2.1) SHA `e10a4e429fca708788ff9e7572a95fce801fae55852d217cffabc1c59cd4eed4`, 46 005 176 byte.

## 4. CShapes 2.0 (ETH Zürich ICR)
- https://icr.ethz.ch/data/cshapes/ · SHA `771ea30af34a6176f2c8f43012df43d672e3b6bb7b3078787a4019a3d1c60de7`
> "CShapes 2.0 maps the borders and capitals of independent states and dependent territories from 1886 to 2019 and from 1816 for CShapes-Europe."
> "CShapes by Schvitz, Rüegger, Girardin, Cederman, Weidmann, Gleditsch is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License."

## 5. Euratlas (Euratlas-Nüssli, Thuỵ Sĩ)
- https://www.euratlas.net/infos_legales.html · SHA `bcfccecd9308aba0bda1f0857874b82f7e1b2ac08dad293321bfaa5c6c7ca22c`
> "Le titre, la conception, la forme des sites … mais aussi les commentaires, illustrations, cartes et images originales et leur organisation sont la propriété d'Euratlas-Nüssli, 1400 Yverdon-les-Bains, Suisse. Les visiteurs ne sont autorisés à copier électroniquement et à imprimer sur support papier ces éléments que dans la mesure où cela est spécifié dans le corps du site. Toute autre utilisation d'éléments des sites Euratlas, est interdite."
- Trang cửa hàng GIS (`shop.euratlas.com`, `www.euratlas.net/shop/`) **ngắt kết nối (curl 35/000)** từ container → **chưa đọc được điều khoản giấy phép GIS**. Thư viện Stanford/Duke ghi bộ GIS Euratlas chỉ cấp cho thành viên trường (WebSearch, chưa đọc trang gốc).

## 6. GeaCron
- https://www.geacron.com/home-en/ · SHA `32b66ccb10c54dcbb57183961ab65f02c260a319fd595ae2f44fa620605453c1`
> "Copyright © 2011 - geacron.com - All Rights Reserved"
- http://geacron.com/offer/ · SHA `a5ae58de70022af0dd62965b2c002eedf63389d4f50517caa5f1173e43a9461f`
> "Exclusive Sale Offer €450,000 … We are offering ownership of a valuable, proprietary database …"
- http://geacron.com/assets3/ · SHA `8cc6bcb1a3f07962684df4c3cc92ae119da9209c8bfa790b79450ee2dd0c2b29`
> "List of GeaCron Databases: 1. Vector historical countries maps by year 2. Vector historical routes by year …"
- Trang "Terms and Conditions" **lặp chuyển hướng 301 (curl 47)** → chưa đọc được.

## 7. Newberry Library — Atlas of Historical County Boundaries (Bắc Mỹ)
- https://digital.newberry.org/ahcb/download · SHA `d293384d3ef64ba82c7b2f06b77cafe345365ba9da536be32aff606848b06b65`
> "The data used in the _Atlas_ is readily available to download to be consulted, reviewed, and reused for any lawful purpose, commercial or non-commercial, without licensing or permission fees to the library. Please note that some files may contain the original, out-of-date copyright license; these can be ignored."
- Tệp `US_AtlasHCB_StateTerr_Gen01.zip` (SHA `db6f124d913bdda718fbf4153d5b1abe569cb9b60cb2a4d73b25afb5a258c457`) **vẫn kèm** `zCreativeCommonsLicense/CreativeCommonsDeed.htm` = "Creative Commons Attribution-NonCommercial-ShareAlike 2.5" (2006) — đúng loại "out-of-date copyright license" mà trang nói bỏ qua. Metadata: "a generalized version … based on a tolerance of .01 degrees", "from 1783 to 2000 … changes dated to the day".

## 8. IPUMS NHGIS (Mỹ, so sánh)
- https://www.nhgis.org/ipums-nhgis-terms-use · SHA `986d576519c091fd6cb5be00d7f39cc75961dbce0ba578260b9613673db02e62`
> "Redistribution: You will not redistribute the data without permission … Contact us for permission for any other redistribution; we will consider requests for free and commercial redistribution."

## 9. Natural Earth (nền bờ biển/đất, hiện đại)
- https://www.naturalearthdata.com/about/terms-of-use/ · SHA `f4ff5d616b442260e2f1b0f1e23a821bcbd159a4343cbb3b67dbc59bfc754fcf`
> "All versions of Natural Earth raster + vector map data found on this website are in the public domain. You may use the maps in any manner, including modifying the content and design, electronic dissemination, and offset printing."

## 10. David Rumsey Map Collection (ảnh bản đồ cổ)
- https://www.davidrumsey.com/about · SHA `8f0c19e32b18389b89d9005c2c9d5be5f23952b70bc585668c2c9e664340f6e5`
> "Images from this web site and database may be reproduced or transmitted, but not for commercial use. Permitted non-commercial use is any work or publication, either in print or digital media. Please give image credit to "David Rumsey Map Collection, David Rumsey Map Center, Stanford Libraries" Commercial use is selling reproductions of our images. For commercial use or commercial republication, contact [email đã che] This work is licensed under a Creative Commons License. By downloading any images from this site, you agree to the terms of that license."
- Liên kết "Creative Commons License" trong trang trỏ tới `creativecommons.org/licenses/by-nc-sa/3.0/` (đọc từ HTML cùng SHA) → **CC BY-NC-SA 3.0**.

## 11. Rijksmuseum (ảnh bản đồ/tranh)
- https://www.rijksmuseum.nl/en/research/conduct-research/data/policy · SHA `27de5b323dade1f1288647f936e7f1611e236488661f3676f118e1b273a47f41`
> "For much of the information and data on the collection website, you will find a Public Domain or Creative Commons Zero (CC0) Public Domain Dedication under the copyright notice, meaning you can use the material freely … In some cases, copyright does apply. If so, a Creative Commons BY 4.0 (CC BY 4.0) licence is indicated."

## 12. Library of Congress
- Trang quyền của bộ sưu tập bản đồ trả **403** từ container (đúng ghi chú QUAN-TRI-RUI-RO §6.6: trang item loc.gov chặn máy). Luật hiện hành của repo (§6.7): kiểm "Rights Advisory" từng item ("No known restrictions" / tác phẩm chính phủ Mỹ / xuất bản trước 1931); chủ dự án đối chiếu trang LoC trước phát hành.

## 13. Creative Commons BY-SA 4.0 (để xét share-alike cho video)
- https://creativecommons.org/licenses/by-sa/4.0/legalcode.en · SHA `47c0a954c88d793bdefe92fb007ae3c038fb3807f1a27083433d01aa7542c0d8`
> "Adapted Material means material subject to Copyright and Similar Rights that is derived from or based upon the Licensed Material and in which the Licensed Material is translated, altered, arranged, transformed, or otherwise modified in a manner requiring permission under the Copyright and Similar Rights held by the Licensor. For purposes of this Public License, where the Licensed Material is a musical work, performance, or sound recording, Adapted Material is always produced where the Licensed Material is synched in timed relation with a moving image."

## 14. Atlas Pi (mới, liệt kê trong README historical-basemaps)
- https://atlaspi.it/ · SHA `611ec8fb4cd93ded9df294b97500dda62fd5c6d5506b8a22d201b5be99c73ae9`
> "Open source Core $0 /month Full REST API access MCP server included Self-host from GitHub Apache-2.0 licensed"
- Trang chỉ nêu giấy phép **mã** (Apache-2.0); **không nêu giấy phép dữ liệu ranh giới** → chưa dùng được cho đến khi đọc giấy phép dữ liệu.
