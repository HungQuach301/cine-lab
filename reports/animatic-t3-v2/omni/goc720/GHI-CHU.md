# Video gốc Omni 720p đã cứu (lệnh bổ sung của chủ dự án 22/10/2026)

Bản nén từ video gốc 1280×720 của 4 lượt Omni đã dùng trong master v2, để giữ lại khi container bị thu hồi. Mỗi tệp chứa đúng đoạn đã dùng trong phim, cộng 0,5 s đệm ở mỗi đầu nếu tệp gốc còn đủ. Thông số: 1280×720, 24 fps, không tiếng, x264 `-preset slow`, yuv420p, đã bỏ metadata. Mỗi tệp ≤ 4,9 MB, không phải chia đôi tệp nào.

Video gốc (`gemini-omni-1.1-flash`, image-to-video) dài 10,005 s, có C2PA `trainedAlgorithmicMedia` và SynthID. **Bản nén lại đã mất manifest C2PA** vì đã bỏ metadata khi mã hoá lại. Nguồn gốc AI tra theo SHA tệp gốc trong `reports/animatic-t3-v2/so-ai-gemini.jsonl`. Toàn bộ đoạn vẫn là **minh hoạ** (`minh_hoa: true`).

| Mã | Lượt | Tệp gốc dùng | SHA-256 tệp gốc (khớp sổ AI) | Đoạn dùng trong phim (s, theo tệp gốc) | Mốc cắt trong tệp gốc (s) | CRF | Tệp nén | Byte | SHA-256 tệp nén |
|---|---|---|---|---|---|---|---|---|---|
| M2 | M2-l3 | `/var/tmp/cine-out/omni-goc/M2-l3.mp4` | `d03dd5949de4d018fd4f9275568edc44690dcba4a65412c5d1130808d830fbe2` | 1,000–9,000 | 0,500–9,500 (9,000 s, 216 khung) | 19 | `M2.mp4` | 4 340 444 | `7fb41751db149e830fe573140100d7f7d2772381e94fc9545e2bbebe2226455f` |
| M3 | M3-l1 | `/var/tmp/cine-out/omni-goc/M3-l1.mp4` | `0ea8dd2d2590b8730b60c823accc451ce4a369d26d4d35475bb6547cba74f48c` | 0,000–8,000 | 0,000–8,500 (8,500 s, 204 khung; đầu tệp không có đệm) | 17 | `M3.mp4` | 4 793 892 | `3363670aed3fee81fb4fd6b58653d33066f10c284a995b46390630a863840d96` |
| M4 | M4-l1 | `/var/tmp/cine-out/omni-goc/M4-l1.mp4` | `7a72dac3bad46aa5cc83cdb6d1988e2b9fc4da6d1a62fa9931e872f56fe66070` | 2,000–8,417 | 1,500–8,917 (7,417 s, 178 khung) | 16 | `M4.mp4` | 3 035 576 | `cf129ac9c7adb565a698013db4c8f65efc212e4deaba91b4c5471fe7adb0f90d` |
| M5 | M5-l3 | `reports/animatic-t3-v2/omni/ra/M5-l3.mp4` (*) | `c683c4e9ac7d46a4484c0cbcad359bfc74972fd526f4aa3a92dc03c91e227b5b` | 0,000–6,000 | 0,000–6,500 (6,500 s, 156 khung; đầu tệp không có đệm) | 16 | `M5.mp4` | 3 772 224 | `91f17db5055afa8036755ba7021665caa30146efb42e322da00b35fdad6aff2e` |

(*) Trong `/var/tmp/cine-out/omni-goc/` không có `M5-l3.mp4` (thư mục này chỉ có các lượt tới M5-l1). Đã lấy tệp gốc trong `omni/ra/`, nằm ngoài git do `.gitignore`. SHA của tệp này **khớp** với sổ AI, nên đây chính là tệp gốc do API trả về. **Không tệp nào MẤT.**

Cách lấy mốc: đoạn dùng = [`bo_dau_clip_s`, `bo_dau_clip_s` + `doan_giay` × `toc_do`] theo `reports/animatic-t3-v2/do/minh-hoa-ghep.json` (cả 4 đoạn có `toc_do` = 1,0). Mốc cắt = đoạn dùng nới 0,5 s mỗi đầu, giới hạn trong [0; 10,005]. Cắt chính xác theo khung (`-ss` đặt sau `-i`). Kiểm toàn vẹn bằng `sha256sum -c SHA256SUMS`.
