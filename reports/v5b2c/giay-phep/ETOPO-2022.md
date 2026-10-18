# ETOPO 2022 — giấy phép (đọc NGUYÊN VĂN từ trang NOAA NCEI, 18/10/2026, curl)

> Không phải tư vấn pháp lý. Chép nguyên văn khối chữ (đã bỏ thẻ HTML, gộp khoảng trắng). Tệp HTML gốc ngoài git (`/var/tmp/cine-out/bd/raw/`), SHA-256 dưới đây.

## 1. Trang metadata ISO của bộ dữ liệu
- URL: `https://www.ncei.noaa.gov/access/metadata/landing-page/bin/iso?id=gov.noaa.ngdc.mgg.dem:etopo_2022`
- SHA-256 trang tải về: `84bb47da4d9fc78f47a9ebfbb7fef621dd8f675b6f4d14574d6662c56fcf41db`

Nguyên văn (Use/Access/Other Constraints):

> Use Constraints Use liability: NOAA and NCEI cannot provide any warranty as to the accuracy, reliability, or completeness of furnished data. Users assume responsibility to determine the usability of these data. The user is responsible for the results of any application of this data for other than its intended purpose. Access Constraints Distribution liability: NOAA and NCEI make no warranty, expressed or implied, regarding these data, nor does the fact of distribution constitute such a warranty. NOAA and NCEI cannot assume liability for any damages caused by any errors or omissions in these data. If appropriate, NCEI can only certify that the data it distributes are an authentic copy of the records that were accepted for inclusion in the NCEI archives. Other Constraints Cite as:NOAA National Centers for Environmental Information. 2022: ETOPO 2022 15 Arc-Second Global Relief Model. NOAA National Centers for Environmental Information. https://doi.org/10.25921/fd45-gt74 . Accessed [date]. Other Constraints These data were produced by NOAA and are not subject to copyright protection in the United States. NOAA waives any potential copyright and related rights in these data worldwide through the Creative Commons Zero 1.0 Universal Public Domain Dedication (CC0-1.0). Other Constraints SPDX License: Creative Commons Zero v1.0 Universal (CC0-1.0)

Câu trích dẫn bộ dữ liệu (nguyên văn):

> Cite as:NOAA National Centers for Environmental Information. 2022: ETOPO 2022 15 Arc-Second Global Relief Model. NOAA National Centers for Environmental Information. https://doi.org/10.25921/fd45-gt74 . Accessed [date].

## 2. Trang sản phẩm ETOPO
- URL: `https://www.ncei.noaa.gov/products/etopo-global-relief-model`
- SHA-256: `152a527b102ef81cf0062534be91f11af6506452a7fccaa8be001081608f1f88`

> Versions Unrestricted Full global coverage, no copyright or security distribution restrictions Restricted Contains higher quality copyrighted data in areas where it was licensed, available, and necessary

## 3. Kết luận vận hành (phiên V5b-2c)
- **CC0-1.0 (SPDX), không bản quyền ở Mỹ, NOAA từ bỏ quyền toàn cầu** → dùng được cho video bán/kiếm tiền, không bắt buộc ghi công; vẫn ghi câu trích dẫn trong mô tả (lịch sự, truy vết). Bật `--dem etopo` cho nền tầm châu lục.
- Tệp đã tải (ngoài git, `/var/tmp/cine-out/bd/raw/`): `ETOPO_2022_v1_15s_N45W015_surface.tif` SHA-256 `4accf0190b62f20c2adc1bf29bd4ee98ddd1be885745276f2476b0d941e0d195`; `ETOPO_2022_v1_15s_N45E000_surface.tif` SHA-256 `86f7ba59e904807fee7e035ada1ad8e761fd89d658574e91efa9e0e727f8d5d0` (nguồn `https://www.ngdc.noaa.gov/mgg/global/relief/ETOPO2022/data/15s/15s_surface_elev_gtif/`).
- Đề xuất dòng RIGHTS (P ghi): `ETOPO 2022 15″ surface (NOAA NCEI, DOI 10.25921/fd45-gt74) · CC0-1.0 · nền địa hình bản đồ chiến lược · mọi tập`.

## Bổ sung: đủ 9 ô đã dùng (SM2 bbox −18…10°Đ, 30…47°B; SM3 bbox −24…12°Đ, 27…54°B)

Tên gốc `ETOPO_2022_v1_15s_<ô>_surface.tif` (lưu cục bộ là `etopo15s_<ô>.tif`), cùng thư mục nguồn như trên. SHA-256:

- `etopo15s_N30E000.tif` `2e661b1af6e235a6fba11c65897fc935ac0528f54975c7c6415ce97d95e7f8a1`
- `etopo15s_N30W015.tif` `7d364296c8bf1f212b31fe443080d24bd5f8a36e765a54679352e183678ec43d`
- `etopo15s_N30W030.tif` `f9058bc291fd5267e7849d11ae19e15743589ae6c29a7317c87347e96ba1efa5`
- `etopo15s_N45E000.tif` `86f7ba59e904807fee7e035ada1ad8e761fd89d658574e91efa9e0e727f8d5d0`
- `etopo15s_N45W015.tif` `4accf0190b62f20c2adc1bf29bd4ee98ddd1be885745276f2476b0d941e0d195`
- `etopo15s_N45W030.tif` `8f686f16b7440843c4c78e0d9cac7c341e14e1f568a148a22de9d1de40141eeb`
- `etopo15s_N60E000.tif` `d69dbf93dcf2f11fb008a57223da41092921ea2f81ef6eeb1807d50609586557`
- `etopo15s_N60W015.tif` `195d7c9235fe4ffe3eb6271a0b3d25ad4ebc2be17b33ee8e76ce8d67fa8f41dc`
- `etopo15s_N60W030.tif` `77bd9a4e2c0509a9cfaf157af4ed3e3f8e3940ddb395dcc157c5349e397241bc`
