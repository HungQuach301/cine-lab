# Dữ liệu Natural Earth trong checks/ll/data (phiên K, 1.14.0, 17/10/2026)

Natural Earth là **public domain** (https://www.naturalearthdata.com/about/terms-of-use/). Không cần ghi công; ghi để truy nguồn.
Không có bản đã commit ở `design/k2v/data/` (chỉ có countries-110m/50m, states-10m, places), nên K tải từ kho chính thức trên GitHub
(`nvkelso/natural-earth-vector`, nhánh master, thư mục `geojson/`) ngày 17/10/2026 và đóng gói bằng `ne_build.py` (lượng tử 1e-5°).

| Tệp gốc | SHA-256 tệp gốc | Tệp đóng gói | Dùng cho |
|---|---|---|---|
| `ne_10m_admin_0_disputed_areas.geojson` (99 feature; Gibraltar 7 đỉnh, mép bắc 36,141°) | `9cafef8b7dfb6b164dc58f218f981f4ace9f716f6c03795d4c62d1ac9f3d50f5` | `ne10m-disputed.npz` | BD-5, K-R3 |
| `ne_10m_land.geojson` (11 feature, 446 175 điểm) | `1ac90796408bc6ad6911d69448485d3c4dbf2190370080368a09976e1c9f7416` | `ne10m-land.npz` | BD-6 |

SHA của tệp đóng gói nằm trong `checks/LOCK`. Đóng gói lại: `/opt/cine/bin/python checks/ll/data/ne_build.py <disputed.geojson> <land.geojson> checks/ll/data`
(zip của numpy ghi thời gian → SHA tệp .npz đổi mỗi lần đóng gói; nội dung toạ độ không đổi).
