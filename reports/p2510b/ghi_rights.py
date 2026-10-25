#!/usr/bin/env python3
"""P-2510b: sinh mục RIGHTS.md cho tài sản NC-T4 từ reports/nc-t4/{nhan-vat-anh,tu-lieu-1940,footage-2026}.json (đọc, không sửa).
In ra stdout; P nối vào cuối RIGHTS.md. Dùng: /opt/cine/bin/python -I reports/p2510b/ghi_rights.py >> RIGHTS.md"""
import hashlib, json, os
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
J = lambda p: json.load(open(os.path.join(R, p), encoding="utf-8"))
nv, tl, ft = J("reports/nc-t4/nhan-vat-anh.json"), J("reports/nc-t4/tu-lieu-1940.json"), J("reports/nc-t4/footage-2026.json")
sha = lambda p: hashlib.sha256(open(os.path.join(R, p), "rb").read()).hexdigest()
c = lambda x: str(x).replace("|", "/").replace("\n", " ")

DUYET_RIENG = {"wellcome-puwvaf8q-pepys": "**chờ chủ dự án duyệt riêng** (chân dung sau 1685; chú thích không gắn năm 1666)",
               "rijks-200221267-james2-loggan": "**chờ chủ dự án duyệt riêng** (năm khắc 1643–1692 chưa rõ; chú thích không ghi 1666)",
               "loc-2017696565-churchill-1943": "**chờ chủ dự án duyệt riêng** (ảnh 1943, 856×1024; câu Churchill đã bỏ — P4 — nên thẻ có thể không cần)"}
o = []
o.append("\n## T4 London — nghiên cứu NC-T4: chân dung, ảnh 1850–1930, tư liệu 1940, footage 2026 (P-2510b ghi 25/10/2026)")
o.append("Nguồn: `reports/nc-t4/NC-T4-BAO-CAO.md` §2–§5, §13; `reports/nc-t4/NHAN-VAT-ANH.md` + `nhan-vat-anh.json`; `reports/nc-t4/TU-LIEU-1940.md` + `tu-lieu-1940.json`; `reports/nc-t4/FOOTAGE-2026.md` + `footage-2026.json` (merge `k2c-t4-02-nc` @d2279bbb). "
         "Căn cứ dùng: chủ dự án 25/10/2026 09:15 \"Duyệt gói 50 % tiết kiệm + P1–P10 theo khuyến nghị\" (P6, P7). Trạng thái: **đã duyệt nhóm cho animatic v2 — bản cuối chốt danh sách lên hình**; tính vào trần T4 ≤ 20 % (Kinh thánh §19 (c) cập nhật 25/10 09:15). Ngày truy cập mọi nguồn: 2026-10-25.")
o.append("\n**Lưu ý bằng chứng (P-2510b phát hiện khi ghi sổ):** `NHAN-VAT-ANH.md` và cột `evidence` của `nhan-vat-anh.json` trỏ tới `channel-k2/k2c-t4-02/nc/licenses/<id>.json` (siêu dữ liệu nguyên văn của nơi giữ), nhưng **21 tệp JSON đó không có trong git** (nhánh `k2c-t4-02-nc` chỉ có `SHA256-NC.txt` + 2 trang Hooke; gốc `/var/tmp/nc-t4/` đã mất cùng container). "
         "Câu giấy phép nguyên văn, URL nguồn/API, SHA gốc nằm trong `reports/nc-t4/nhan-vat-anh.json` (trong git) — dùng làm bằng chứng tạm. **Trước bản cuối:** tải lại siêu dữ liệu bằng `scripts/k2ldn/nc/tai_nc.py` vào `nc/licenses/<id>.json` (đối chiếu SHA gốc ở `nc/licenses/SHA256-NC.txt`).")
o.append("\n### Chân dung + ảnh/bản vẽ 1850–1930 (21 tệp `channel-k2/k2c-t4-02/nc/anh/`, bản thu ≤ 2 400 px; gốc ngoài git — SHA gốc ở `nc/licenses/SHA256-NC.txt`, tái tạo bằng `scripts/k2ldn/nc/tai_nc.py`)")
o.append("| Mã | Tài sản | Loại | Nguồn/URL | Tác giả | Giấy phép (trích nguyên câu + link) | Được dùng: YouTube / bán phim / LHP | Ghi công | SHA-256 (gốc · bản thu trong git) | Ngày thêm |")
o.append("|---|---|---|---|---|---|---|---|---|---|")
for it in nv["items"]:
    i = it["id"]; loai = "Chân dung (thẻ ≤ 5 s; tham chiếu trang phục §15 (f) nới hẹp)" if it["nhom"] == "A" else "Ảnh/bản vẽ 1850–1930 (chồng góc khung / toàn khung có chuyển động máy, H3)"
    dung = DUYET_RIENG.get(i, "Có / Có / Có")
    ghi = f"\"{c(it['title'])}\" — {c(it['holder'])}"
    o.append(f"| T4-NC-{i} | {c(it['chu_de'])} ({c(it['date'])}); đề xuất: {c(it['de_xuat_dung'])}; rủi ro {c(it['rui_ro'])} | {loai} | {it['source_url']} | {c(it['creator']) if it['creator'] not in (None, 'None') else 'vô danh / không ghi'} | {c(it['licence'])}: \"{c(it['licence_quote_verbatim'])}\" — bằng chứng tạm `reports/nc-t4/nhan-vat-anh.json` (JSON nơi giữ: tải lại trước bản cuối) | {dung} | {ghi} | `{it['sha256'][:16]}…` · `{sha(it['file'])[:16]}…` | 2026-10-25 |")
o.append("\n- **Robert Hooke:** không có chân dung xác thực (Royal Society; bằng chứng `channel-k2/k2c-t4-02/nc/licenses/hooke-rs-trang.html`, `hooke-pbs-trang.html`) → chỉ thẻ chữ; không tài sản. Bludworth, Barbon, Godfrey Allen, Holden, Holford, Matthews: chưa có bản sạch quyền → thẻ chữ.")
o.append("- Ảnh NPG London: điều khoản CC BY-NC-ND → **không dùng** cho phim bán. Ảnh Keystone 1926–1931 (LoC \"Rights status not evaluated\") và LoC 91789510 (trường quyền rỗng): **không dùng**.")
o.append("\n### Tư liệu 1940 (ảnh MoI Crown — ứng viên, **chưa tải**; chú thích phải ghi đúng năm chụp)")
o.append("| Mã | Tài sản | Loại | Nguồn/URL | Tác giả | Giấy phép (trích nguyên câu + link) | Được dùng: YouTube / bán phim / LHP | Ghi công | SHA-256 | Ngày thêm |")
o.append("|---|---|---|---|---|---|---|---|---|---|")
for x in tl["candidates"]:
    if x["id"] in ("C01", "C02", "C03", "C04", "C05"):
        o.append(f"| T4-NC-1940-{x['id']} | {c(x['subject'])} — năm **{c(x['year'])}**; {c(x['recommend'])} | Ảnh (Crown, hết hạn) | {x['evidence_url']} (tải: {c(x['download_url'])}) | {c(x['author'])} | {c(x['status'])}; trích: {c(x['quote'])[:260]}… (CDPA 1988 Sch.1 para 41(2)(d); bằng chứng `reports/nc-t4/tu-lieu-1940.json`, `reports/nc-t4/nguon/web/commons-file-pages.txt`) | Có / Có / Có — bản Commons (không tải bản IWM theo hợp đồng phi thương mại) | {c(x['attribution'])[:200]} | (chưa tải — ghi SHA khi tải) | 2026-10-25 |")
o.append("\n### LOẠI (không dùng)")
o.append("| Mã | Tài sản | Lý do | Bằng chứng | Ngày |")
o.append("|---|---|---|---|---|")
for x in tl["candidates"]:
    if x["id"] in ("C12", "C13", "C14"):
        o.append(f"| T4-NC-LOAI-{x['id']} | {c(x['subject'])} — {c(x['author'])}, {c(x['year'])} | {c(x['status'])}. **LOẠI — không dùng ảnh, không dựng lại bố cục bằng AI** (P6) | {x['evidence_url']}; trích: {c(x['quote'])[:200]} | 2026-10-25 |")
o.append("| T4-NC-LOAI-C06 | Ảnh ghép St Paul's + vệt khói máy bay (IWM HU 54557) | ảnh dựng (composite) — không dùng làm tư liệu thật | `reports/nc-t4/tu-lieu-1940.json` | 2026-10-25 |")
o.append("| T4-NC-LOAI-PHIM1940 | *London Can Take It!* (1940; C15–C18) và *Christmas Under Fire* (1941; C19) | Chủ dự án P6 = (a): **không dùng phim 1940 trong T4** (bản IA SD, nhãn PD tự gán; lời bình Reynolds còn nghi vấn; bản HD trả phí) | `reports/nc-t4/TU-LIEU-1940.md` §3.2–§3.3 | 2026-10-25 |")
o.append("| T4-NC-LOAI-BYSA | Footage Commons CC BY-SA: C4, C5, C6, C7, C9 | share-alike → phim phải mang BY-SA, không DRM; Kinh thánh §19 (c) cập nhật 25/10 09:15 (5) chỉ cho phép giấy phép không share-alike | `reports/nc-t4/FOOTAGE-2026.md` §2; `reports/nc-t4/nguon/web/footage-cc-by-sa-4-legalcode.txt` | 2026-10-25 |")
o.append("\n### Footage London 2026 — ứng viên cho **1 clip đêm H5-07a (≈ 6 s)** (P7 = (a) cho H5-07a + (b) tham chiếu cho phần còn lại); **chưa chọn, chưa tải, chưa lên hình**")
o.append("| Mã | Tài sản | Loại | Nguồn/URL | Tác giả | Giấy phép (trích nguyên câu + link) | Được dùng: YouTube / bán phim / LHP | Ghi công | SHA-256 | Ngày thêm |")
o.append("|---|---|---|---|---|---|---|---|---|---|")
PX = "trích qua WebFetch (mô hình tóm tắt, ≤ 125 ký tự/đoạn): \"download, use, copy, modify or adapt the Content for commercial or non-commercial purposes\"; \"You cannot sell or distribute the Content … on a Standalone basis.\" (https://www.pexels.com/license/, https://www.pexels.com/terms-of-service/) — **CHƯA ĐỐI CHIẾU BẢN GỐC** (curl 403); bằng chứng tạm `reports/nc-t4/nguon/web/footage-licence-webfetch.txt`"
PB = "trích qua WebFetch: \"Use Content for free\"; \"Modify or adapt Content into new works\"; \"You cannot sell or distribute Content … on a Standalone basis.\" (https://pixabay.com/service/license-summary/) — **CHƯA ĐỐI CHIẾU BẢN GỐC** (curl 403); bằng chứng tạm `reports/nc-t4/nguon/web/footage-licence-webfetch.txt`"
cho = "Chờ: chủ dự án lưu PDF trang giấy phép vào `licenses/` + xem khung clip trước khi dùng"
for x in ft["pixabay"]:
    if x["id"] == "X1":
        o.append(f"| T4-NC-FT-X1 | Pixabay {x['id']} — {x['res']}, {x['fps']} fps, {x['date']}; {c(x['note'])} — **ứng viên chính H5-07a** | Footage (người quay, không AI) | {x['url']} | {x['author']} | Pixabay Content License — {PB} | {cho} | không bắt buộc; ghi \"{x['author']} / Pixabay\" | (chưa tải) | 2026-10-25 |")
for x in ft["pexels"]:
    if x["id"] in ("P3", "P4"):
        o.append(f"| T4-NC-FT-{x['id']} | Pexels {x['id']} — {x['res']}, {x['fps']} fps, {x['dur']}, {x['date']}; {c(x.get('note',''))} — dự phòng H5-07a | Footage | {x['url']} | {x['author']} | Pexels License — {PX} | {cho} | không bắt buộc; ghi \"{x['author']} / Pexels\" | (chưa tải) | 2026-10-25 |")
for x in ft["commons"]:
    if x["id"] in ("C3", "C1"):
        note = "giấy phép đã được bot xác nhận (\"License reviewed by YouTubeReviewBot\"); chỉ vài giây dùng được" if x["id"] == "C3" else "\"License review needed (video)\"; skyline 2016 thiếu 22 Bishopsgate → **không dùng làm \"2026\"**; chỉ tham chiếu"
        o.append(f"| T4-NC-FT-{x['id']} | Commons {x['id']} — {c(x['title'])}, {c(x['resolution'])}, {x['duration_s']} s; {note} | Footage | {x['url']} | {c(x['author'])} | {x['LicenseShortName']} — \"{x['UsageTerms']}\" (https://creativecommons.org/licenses/by/3.0/) | {'Có / Có / Có (CC BY, ghi công) — ' + cho if x['id']=='C3' else 'Không (chỉ tham chiếu)'} | \"{c(x['author'])}, CC BY 3.0, via Wikimedia Commons\" | (chưa tải) | 2026-10-25 |")
o.append("\n- Footage phần còn lại (H5-04, H5-05a, H5-05b, H5-06, H5-08): **chỉ tham chiếu bố cục/ánh sáng** (P7 (b)) — gồm Pexels P1, P2, P5–P7, Commons C2, C8, C10, Pixabay X2, X3; không chèn vào phim, không cần dòng tài sản. Báo giá Getty/Storyblocks: **không mua**.")
o.append("- Văn bản nguồn dữ kiện điểm nhấn (chỉ dữ kiện, không chép văn bản vào phim): *Parentalia* (1750, archive.org gri_33125011157357, PD) `reports/nc-t4/nguon/web/dn-parentalia-1750.txt`; City of London *Protected Views SPD* 2012 (dữ kiện) `dn-col-spd-2012.txt`; St Paul's \"Our timeline\" + \"St Paul's Watch\", themonument.org.uk, All Souls Wren drawings, London Museum 435888/99769/102498, BHO *Old and New London* (1878), City of London Barbican history — `reports/nc-t4/nguon/web/dn-*.txt`. Pepys/Evelyn như **N2P-T4-1/-2**. Lưu ý: St Paul's \"Our timeline\" ghi sai ngày cháy (\"September 3rd 1666\") — không dùng câu đó.")
o.append("- Lời mới P5 (868 ký tự, N0a…N6) do dự án viết; câu trích Pepys/Evelyn từ văn bản PD. Thu bằng giọng G1 — quyền phát hành vẫn chờ Đ5.")
o.append("- Không nhạc/SFX/font mới; không tài sản NC/ND được nhận vào phim.")
print("\n".join(o))
