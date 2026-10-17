# Ghi công và giới hạn cho các mẫu GeoJSON trong thư mục này (NC-BD, 17/10/2026)

Mẫu chỉ để KIỂM (độ phủ, độ khớp, định dạng). Không phải tài sản đã khoá; chưa vào RIGHTS.md.

| Tệp | Nguồn | Giấy phép | Ghi công đề xuất khi dùng |
|---|---|---|---|
| `ohm-1704-tay-au.geojson`, `ohm-1782-tay-au.geojson`, `ohm-1941-tay-au.geojson` | OpenHistoricalMap (Overpass `overpass-api.openhistoricalmap.org`, 17/10/2026); quan hệ ghi ở `ohm_relation`; cắt bbox −10,5…4,5 / 35,5…52; đơn giản hoá 0,005° | Dữ liệu OHM CC0; **nhiều đường thành phần mang `license=CC-BY-4.0`** (nguồn CNIG/IGN Tây Ban Nha "LILIM", LSIB Bộ Ngoại giao Mỹ…) | "Borders: OpenHistoricalMap contributors (CC0); includes data © Instituto Geográfico Nacional (CNIG), CC BY 4.0" |
| `cliopatria-1704-tay-au.geojson`, `cliopatria-1782-tay-au.geojson`, `cliopatria-1941-tay-au.geojson` | Cliopatria v0.2.1, Seshat Global History Databank (Zenodo 23128623); cắt bbox, không đơn giản hoá | CC BY 4.0 | "Borders: Cliopatria v0.2.1 (Seshat Global History Databank), CC BY 4.0" |
| `newberry-us-1783-09-03.geojson`, `newberry-us-1803-05-01.geojson` | Newberry Library, Atlas of Historical County Boundaries — US Historical States and Territories (generalized .01°); đơn giản hoá thêm 0,01° | Trang Download: dùng lại mọi mục đích hợp pháp, thương mại hay không (tệp zip còn kèm CC BY-NC-SA 2.5 cũ — trang ghi bỏ qua) | "Atlas of Historical County Boundaries, The Newberry Library" |

historical-basemaps (GPL-3.0) **không** được chép vào repo; chỉ ghi SHA và số đo trong báo cáo.
