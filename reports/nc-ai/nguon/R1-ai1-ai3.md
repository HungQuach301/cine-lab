# R1 — Công cụ AI mã nguồn mở chạy cục bộ (CPU) cho phim tài liệu lịch sử: OCR/HTR, vector hoá bản đồ, phục chế ảnh, độ sâu, chính sách công khai AI của YouTube

Ngày đọc mọi nguồn: **2026-10-18**. Phương pháp: tải trực tiếp file LICENSE / README / model card (raw) bằng `curl` qua proxy, PyPI JSON API, Zenodo API, arXiv; WebSearch/WebFetch cho bài báo. **Mọi trích dẫn giấy phép là nguyên văn** từ file đã tải ngày 2026-10-18. Khi một điều chưa kiểm được, ghi rõ "chưa kiểm".

Bối cảnh áp dụng: kênh YouTube có bật kiếm tiền + bán phim ⇒ **mục đích thương mại**. Quy tắc loại: trọng số (weights) hoặc mã có điều khoản NC / "research only" ⇒ **LOẠI**.

Ghi chú chung về CPU: container 4 lõi, 15 GB RAM, không GPU (đã kiểm `nproc`=4, `free -g`=15). **Chưa chạy đo tốc độ thật** trong phiên này; các cột "CPU ok?" là đánh giá theo kích thước mô hình và tài liệu chính thức, không phải số đo. Cần đo ở bước sau trước khi đưa vào quy trình.

Lưu ý về GitHub: `github.com/.../releases.atom` và `gh api` bị proxy chặn (HTTP 403, phiên chỉ gắn repo dự án) ⇒ **ngày release GitHub không đọc được**; phiên bản lấy từ PyPI (ngày upload thật) hoặc Hugging Face/Zenodo.

---

## A. OCR / HTR cho sách in, bản thảo thế kỷ 17–18 và bản đồ cổ

### Bảng A

| Công cụ | Phiên bản / ngày | Giấy phép mã | Giấy phép trọng số | Thương mại OK? | CPU ok? | URL đã đọc |
|---|---|---|---|---|---|---|
| Tesseract 5 | 5.5.3 (24/07/2026, theo Wikipedia — chưa xác nhận trên GitHub vì bị chặn); apt Ubuntu: 5.3.4-1build5; pip `tesserocr` 2.11.0 (2026-08-04, có wheel manylinux kèm libtesseract); `pytesseract` 0.3.13 (2024-08-16) | Apache-2.0 | tessdata_best: Apache-2.0 | **Có** | **Có** (thiết kế cho CPU) | raw.githubusercontent.com/tesseract-ocr/tesseract/main/LICENSE; raw.githubusercontent.com/tesseract-ocr/tessdata_best/main/README.md + LICENSE; pypi.org/pypi/tesserocr/json |
| kraken | 7.1.1 (PyPI 2026-09-04), Python 3.10–3.13 | Apache-2.0 | Theo từng mô hình; CATMuS-Print [Large/Small/Tiny], CATMuS Gothic Print, McCATMuS: **CC-BY-4.0** (Zenodo) | **Có** (ghi công CC-BY) | **Có** (kraken chạy CPU) | raw.githubusercontent.com/mittagessen/kraken/main/LICENSE; zenodo.org/api/records/10592716, 10599911, 13788177, 10602307, 10602357 |
| eScriptorium | (GitLab, chưa đọc release) | MIT (© 2018 Robin Tissot, PSL) | dùng mô hình kraken | **Có** | Có (web app Django + kraken; nặng về hạ tầng: Postgres, Redis, Docker) | gitlab.com/scripta/escriptorium/-/raw/develop/LICENSE |
| Calamari | `calamari-ocr` 2.3.1 (2024-11-12) | **GPL-3.0** | calamari_models: MIT (gồm `historical_french` 17–19c, `antiqua_historical`, `fraktur_historical`, `gt4histocr`) | Có (GPL chỉ ràng buộc khi phân phối phần mềm; đầu ra không bị ràng buộc) | Có (TF; nhẹ) | raw.githubusercontent.com/Calamari-OCR/calamari/master/LICENSE; .../calamari_models/master/README.md + LICENSE |
| docTR (Mindee) | `python-doctr` 1.1.0 (2026-08-21) | Apache-2.0 | (theo repo, Apache-2.0 — chưa kiểm từng checkpoint) | Có | Có (mô hình nhỏ) | raw.githubusercontent.com/mindee/doctr/main/LICENSE |
| Surya OCR (Datalab) | `surya-ocr` 0.22.1 (2026-07-20) | Apache-2.0 | **AI Pubs OpenRAIL-M (modified)** — giới hạn doanh thu > 5 triệu USD; **share-alike áp lên Output**; yêu cầu ghi công trên Output | Kỹ thuật: được nếu doanh thu < 5 tr USD, **nhưng có điều khoản share-alike lên Output + quyền "restrict remotely"** ⇒ **khuyên KHÔNG dùng** | Có điều kiện: bản hiện tại chạy VLM qua `llama.cpp` trên CPU (chậm, chưa đo) | raw.githubusercontent.com/datalab-to/surya/master/LICENSE, MODEL_LICENSE, README.md |
| TrOCR (Microsoft) | HF checkpoints (2021–22) | MIT (repo microsoft/unilm) | `trocr-base-handwritten`: MIT; `trocr-base-printed`, `trocr-large-handwritten`: **card không khai license** (repo gốc unilm MIT) | Có (handwritten-base rõ ràng); các card thiếu khai báo ⇒ rủi ro nhỏ | Có (~334M–558M tham số; chỉ nhận dạng dòng, cần bộ tách dòng) | huggingface.co/microsoft/trocr-base-printed, trocr-large-handwritten, trocr-base-handwritten (README raw); raw.githubusercontent.com/microsoft/unilm/master/LICENSE |
| PaddleOCR | `paddleocr` 3.7.0 (2026-06-11) | Apache-2.0 | (Apache-2.0 theo repo; chưa kiểm từng mô hình) | Có | Có (PP-OCR mobile dành cho CPU) | raw.githubusercontent.com/PaddlePaddle/PaddleOCR/main/LICENSE; pypi |
| olmOCR (AllenAI) | `olmocr` 0.4.27 (2026-03-12); mô hình olmOCR-2-7B-1025 | Apache-2.0 | Apache-2.0 (fine-tune từ Qwen2.5-VL-7B, cũng Apache-2.0) | Có | **Không thực tế** (7B, card hướng tới vLLM/GPU) | raw.githubusercontent.com/allenai/olmocr/main/LICENSE; huggingface.co/allenai/olmOCR-2-7B-1025 |
| GOT-OCR2.0 | HF `stepfun-ai/GOT-OCR2_0` | — | Apache-2.0 | Có | **Kém** (card chỉ hướng dẫn `device_map='cuda'`) | huggingface.co/stepfun-ai/GOT-OCR2_0 |
| Qwen2.5-VL | 3B / 7B / 32B / 72B | — | **3B: Qwen RESEARCH LICENSE (NC)** ⇒ LOẠI; 7B & 32B: Apache-2.0; 72B: "qwen" license (thương mại OK, >100 triệu MAU phải xin) | 7B/32B có; **3B KHÔNG** | 7B trên CPU rất chậm; 32B/72B không khả thi | huggingface.co/Qwen/Qwen2.5-VL-{3B,7B,32B,72B}-Instruct (README + LICENSE) |
| Qwen3-VL | 2B / 4B / 8B / 30B-A3B / 32B | — | **Apache-2.0** (tất cả các bản đã kiểm) | Có | 2B/4B khả thi trên CPU (chậm, chưa đo); 8B biên | huggingface.co/Qwen/Qwen3-VL-{2B,4B,8B,32B,30B-A3B}-Instruct |
| Florence-2 | base 0.23B / large 0.77B | — | MIT | Có | Có (nhỏ) | huggingface.co/microsoft/Florence-2-large (README + LICENSE), Florence-2-base |

### Chữ s dài (ſ) — kiểm thật

- **Tesseract tessdata_best** (đo trực tiếp bằng cách tìm dòng unicharset `ſ` trong file `.traineddata`, 2026-10-18): `enm` (Middle English) **có** ſ; `deu_latf` (Fraktur) **có** ſ; `eng`, `lat`, `script/Latin` **không có** ſ ⇒ với `eng`, ſ sẽ bị đọc thành `f` hoặc `s`. (`frk` đã đổi tên thành `deu_latf`, file `frk` trả 404.)
- **kraken CATMuS-Print**: Zenodo ghi rõ quy tắc phiên âm giữ ſ (trích dưới).
- **Calamari `historical_french`**: dữ liệu in Pháp thế kỷ 17/18/19 (Gabay); có bản `*_ligs` tinh chỉnh với chữ ghép. Việc giữ ſ: chưa kiểm.
- Các VLM (Qwen, olmOCR, Florence, GOT): không có tài liệu nói về ſ; xu hướng **chuẩn hoá ngầm** (ſ→s) và **tự sửa chính tả cổ** ⇒ rủi ro bịa cao với văn bản lịch sử.

### Rủi ro bịa (hallucination)

- Thấp: Tesseract, kraken, Calamari, docTR, PaddleOCR (mô hình nhận dạng ký tự/CTC: sai thì ra ký tự rác, dễ thấy, không "viết hộ").
- Trung bình: TrOCR (decoder ngôn ngữ, có thể "đoán" từ phổ biến).
- Cao: VLM sinh văn bản (Qwen-VL, olmOCR, GOT, Florence-2, Surya bản VLM mới) — có thể hiện đại hoá chính tả, bỏ dòng, thêm chữ. Bắt buộc đối chiếu với ảnh gốc nếu trích dẫn trên màn hình.

### Trích dẫn nguyên văn (A)

**Tesseract** — https://raw.githubusercontent.com/tesseract-ocr/tesseract/main/LICENSE
> Apache License
> Version 2.0, January 2004

**tessdata_best** — https://raw.githubusercontent.com/tesseract-ocr/tessdata_best/main/README.md
> All data in the repository are licensed under the
> Apache-2.0 License, see file [LICENSE](LICENSE).

**kraken** — https://raw.githubusercontent.com/mittagessen/kraken/main/LICENSE
> Apache License
> Version 2.0, January 2004

**CATMuS-Print [Large]** — https://zenodo.org/api/records/10592716 (published 2024-01-30, license `cc-by-4.0`)
> CATMuS (Consistent Approach to Transcribing ManuScript) Print is a Kraken HTR model trained on data produced by several projects, dealing with different languages (French, Spanish, German, English, Corsican, Catalan, Latin, Italian…) and different centuries (from the first prints of the 16th c. to digital documents of the 21st century).
> Transcriptions follow graphematic principles and try to be as compatible as possible with guidelines previously published for French: no ligature (except those that still exist), no allographetic variants (except the long s), and preservation of the historical use of some letters (u/v, i/j). Abbreviations are not resolved.

Các bản khác (đều `cc-by-4.0`): CATMuS-Print [Small] 10602307, [Tiny] 10602357, CATMuS Gothic Print 10599911 (2024-01-31), McCATMuS 13788177 (2024-09-19, "handwritten, printed and typewritten documents from the 16th century to the 21st century").

**eScriptorium** — https://gitlab.com/scripta/escriptorium/-/raw/develop/LICENSE
> eScriptorium
> Copyright (C) 2018  Robin Tissot (PSL)
> Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"),
> to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
> and/or sell copies of the Software

**Calamari** — https://raw.githubusercontent.com/Calamari-OCR/calamari/master/LICENSE
> GNU GENERAL PUBLIC LICENSE
> Version 3, 29 June 2007

**calamari_models** — https://raw.githubusercontent.com/Calamari-OCR/calamari_models/master/LICENSE: `MIT License`. README:
> *historical_french* used data from 17/18/19. century French printings collected by [Simon Gabay]
> The *ligs* versions used the same data as the standard *antiqua/fraktur_historical* models but were refined on an manually enriched subset (afair 100 lines per book) containing ligatures etc.

**docTR** — https://raw.githubusercontent.com/mindee/doctr/main/LICENSE
> Apache License
> Version 2.0, January 2004

**Surya** — https://raw.githubusercontent.com/datalab-to/surya/master/README.md
> The Surya code is licensed under Apache 2.0. The model weights use a modified AI Pubs Open Rail-M license (free for research, personal use, and startups under $5M funding/revenue). For broader commercial licensing of the model weights, visit our pricing page

https://raw.githubusercontent.com/datalab-to/surya/master/MODEL_LICENSE
> AI PUBS OPEN RAIL-M LICENSE (MODIFIED)
> Version 0.1, March 2, 2023 (Modified)

> 2. Commercial:
> (a) for any purpose if You (your employer, or the entity you are affiliated with) generated more than five million US Dollars ($5,000,000) in gross revenue in the prior year, except where Your Use is limited to personal use or research purposes;

> 7.  Attribution.  In connection with any Output, or use of Distribution of any Model or Derivatives of the Model, You agree to give appropriate credit and attribution to Licensor, provide a link to the original Model or Derivatives of the Model, provide a copy of this License, and identify any changes You have made to the Model or Derivatives of the Model (collectively, the “Attribution”).

> 8.  Share-a-Like.  As a condition to the license and authorizations herein, You agree to apply this License (to the exclusion of all others) to any and all copies of the Model, Derivatives of the Model, any changes or improvements to the Model or Derivatives of the Model, and to the Output and any derivatives, changes or improvements to or of the Output.

> 9. Updates and Runtime Restrictions. To the maximum extent permitted by law, Licensor reserves the right to restrict (remotely or otherwise) usage of the Model in violation of this License, update the Model through electronic means, or cause modification to the Output resulting from updates to the Model based.

(Nhận xét: giả định của bạn đúng — trọng số Surya bị giới hạn theo doanh thu. Ngoài ra điều 7 + 8 kéo nghĩa vụ ghi công và share-alike lên **Output**, không tương thích với phim bán.)

**TrOCR** — https://huggingface.co/microsoft/trocr-base-printed/raw/main/README.md: front-matter **không có trường `license`**; card ghi:
> Disclaimer: The team releasing TrOCR did not write a model card for this model so this model card has been written by the Hugging Face team.

`microsoft/trocr-base-handwritten`: `license: mit`. Repo gốc https://raw.githubusercontent.com/microsoft/unilm/master/LICENSE: `The MIT License (MIT)` / `Copyright (c) Microsoft Corporation`.

**PaddleOCR** — https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/main/LICENSE
> Apache License
> Version 2.0, January 2004

**olmOCR** — https://raw.githubusercontent.com/allenai/olmocr/main/LICENSE: `Apache License` `Version 2.0, January 2004`. Card https://huggingface.co/allenai/olmOCR-2-7B-1025/raw/main/README.md: `license: apache-2.0`, `base_model: - Qwen/Qwen2.5-VL-7B-Instruct`
> The toolkit comes with an efficient inference setup via VLLM that can handle millions of documents

**GOT-OCR2.0** — https://huggingface.co/stepfun-ai/GOT-OCR2_0/raw/main/README.md: `license: apache-2.0`
> Inference using Huggingface transformers on NVIDIA GPUs.

**Qwen2.5-VL-3B** — https://huggingface.co/Qwen/Qwen2.5-VL-3B-Instruct/raw/main/LICENSE
> Qwen RESEARCH LICENSE AGREEMENT
> i. "Non-Commercial" shall mean for research or evaluation purposes only.
> a. You are granted a non-exclusive, worldwide, non-transferable and royalty-free limited license under Alibaba Cloud's intellectual property or other rights owned by us embodied in the Materials to use, reproduce, distribute, copy, create derivative works of, and make modifications to the Materials FOR NON-COMMERCIAL PURPOSES ONLY.
> b. If you are commercially using the Materials, you shall request a license from us.

**Qwen2.5-VL-72B** — https://huggingface.co/Qwen/Qwen2.5-VL-72B-Instruct/raw/main/LICENSE
> If you are commercially using the Materials, and your product or service has more than 100 million monthly active users, you shall request a license from us.

**Qwen2.5-VL-7B / 32B; Qwen3-VL-2B / 4B / 8B / 30B-A3B / 32B** — card front-matter: `license: apache-2.0`.

**Florence-2** — https://huggingface.co/microsoft/Florence-2-large/raw/main/README.md: `license: mit`; LICENSE: `MIT License` `Copyright (c) Microsoft Corporation.`
> | Florence-2-base[[HF]](https://huggingface.co/microsoft/Florence-2-base) | 0.23B | Pretrained model with FLD-5B
> | Florence-2-large[[HF]](https://huggingface.co/microsoft/Florence-2-large) | 0.77B  | Pretrained model with FLD-5B

### Đề xuất A
1. **kraken + CATMuS-Print (Large) [CC-BY-4.0]** cho sách in thế kỷ 16–18: giữ ſ theo quy tắc, chạy CPU, rủi ro bịa thấp. Ghi công CC-BY vào `RIGHTS.md`. Nếu cần GUI chỉnh tay: eScriptorium (MIT) nhưng nặng hạ tầng.
2. **Tesseract 5 + `enm`/`deu_latf` (Apache-2.0)** làm phương án nền/đối chiếu (cài dễ: apt 5.3.4 hoặc `pip install tesserocr`). Tránh `eng`/`lat` khi cần giữ ſ.
- Loại: Surya (trọng số OpenRAIL-M sửa đổi, share-alike lên Output), Qwen2.5-VL-3B (NC). VLM Apache (Qwen3-VL-2B/4B) chỉ dùng làm trợ lý đọc/phân loại, không làm nguồn trích dẫn nguyên văn.

---

## B. Vector hoá dấu chân công trình từ bản đồ cổ đã scan

### Bảng B

| Công cụ | Phiên bản / ngày | Giấy phép mã | Giấy phép trọng số | Thương mại OK? | CPU ok? | URL đã đọc |
|---|---|---|---|---|---|---|
| SAM (v1) | `segment-anything` 1.0 (PyPI 2023-04-06) | Apache-2.0 | Apache-2.0 ("The model is licensed under…") | **Có** | Có với ViT-B (chậm vài giây–chục giây/ảnh, chưa đo) | raw.githubusercontent.com/facebookresearch/segment-anything/main/LICENSE + README.md |
| SAM 2 | `sam2` 1.1.0 (PyPI 2024-12-21) | Apache-2.0 | **Apache-2.0** (checkpoints) | **Có** | Có với bản tiny/small (chưa đo) | raw.githubusercontent.com/facebookresearch/sam2/main/LICENSE + README.md |
| SAM 3 / 3.1 | README: SAM 3.1 checkpoints trên HF; LICENSE "Last Updated: November 19, 2025" | **SAM License** (Meta, tuỳ chỉnh) | **SAM License**; checkpoint HF **gated** (HF trả 401 khi đọc card không đăng nhập) | Có vẻ cho phép (không có điều khoản NC), nhưng có hạn chế Trade Controls/quân sự và nghĩa vụ phân phối kèm giấy phép; cần xin quyền truy cập | Không rõ (mô hình lớn, chưa kiểm) | raw.githubusercontent.com/facebookresearch/sam3/main/LICENSE + README.md; huggingface.co/facebook/sam3 (401) |
| MapReader (Alan Turing Inst.) | `mapreader` 1.8.3 (PyPI 2026-09-13) | MIT | (mô hình người dùng tự fine-tune) | Có | Có (phân loại patch) | raw.githubusercontent.com/maps-as-data/MapReader/main/LICENSE + README.md |
| QGIS (Georeferencer) | (chưa đọc release) | GPL-2.0 (COPYING) | — | Có; GPL chỉ ràng buộc phân phối phần mềm, **không** ràng buộc bản đồ/vector xuất ra | Có | raw.githubusercontent.com/qgis/QGIS/master/COPYING |
| GDAL | `gdal` 3.13.3 (PyPI 2026-08-18) | MIT/X (tổng thể; file LICENSE.TXT liệt kê thêm thành phần) | — | Có | Có | raw.githubusercontent.com/OSGeo/gdal/master/LICENSE.TXT |
| MapSAM / MapSAM2 (ETH Zürich, nghiên cứu) | arXiv 2411.06971; 2510.27547 | Chưa công bố URL/giấy phép mã ("will release") | — | Chưa xác định | — | arxiv.org/html/2510.27547v1 |

Lưu ý: MapReader **không** vector hoá polygon; nó phân loại patch (ví dụ "có nhà / không có nhà") và text spotting. Để ra polygon công trình cần: georeference (QGIS) → phân đoạn (SAM/SAM2 có prompt hoặc U-Net tự huấn luyện) → `gdal_polygonize` / đơn giản hoá → kiểm tay.

### Số đo độ chính xác đã công bố (IoU trên bản đồ cổ)

- **MapSAM2** (arXiv 2510.27547, https://arxiv.org/html/2510.27547v1), bảng 1, IoU **10-shot** trên tập "Building Block" (ICDAR 2021 — bản đồ Paris cổ): U-Net 60.0; PerSAM 16.0; Few-Shot SAM 15.5; SAMed 70.3; MapSAM 71.1; **MapSAM2 75.8**. ⇒ SAM "nguyên bản/không fine-tune" (PerSAM, Few-Shot SAM) chỉ ~15–16 IoU — **SAM zero-shot không đủ** trên bản đồ cổ.
- Cùng bài, chuỗi thời gian công trình bản đồ Siegfried (Thuỵ Sĩ), chỉ báo **P/R/F1** (không phải IoU): MapSAM2 F1 83.9 (huấn luyện đầy đủ 2.105 video), 70.6 (10-shot); Mask2Former-VIS F1 89.5 (đầy đủ) nhưng 34.8 (10-shot).
- **arXiv 2508.03564** ("A Scalable Machine Learning Pipeline for Building Footprint Detection in Historical Maps", bản đồ OSI Ireland 25 inch / 6 inch): abstract không nêu IoU (chỉ "high performance").
- Xydas et al. VISAPP 2022 (DOI 10.5220/0010839700003124) và Zhao et al. IJGI 2022 (DOI 10.3390/ijgi11110572): chỉ thấy qua kết quả tìm kiếm; **chưa đọc số IoU**.

### Trích dẫn nguyên văn (B)

**SAM v1** — https://raw.githubusercontent.com/facebookresearch/segment-anything/main/README.md
> ## License
> The model is licensed under the [Apache 2.0 license](LICENSE).

**SAM 2** — https://raw.githubusercontent.com/facebookresearch/sam2/main/README.md
> The SAM 2 model checkpoints, SAM 2 demo code (front-end and back-end), and SAM 2 training code are licensed under [Apache 2.0](./LICENSE), however the [Inter Font](https://github.com/rsms/inter?tab=OFL-1.1-1-ov-file) and [Noto Color Emoji](https://github.com/googlefonts/noto-emoji) used in the SAM 2 demo code are made available under the [SIL Open Font License, version 1.1]

**SAM 3** — https://raw.githubusercontent.com/facebookresearch/sam3/main/LICENSE
> SAM License
> Last Updated: November 19, 2025

> “SAM Materials” means, collectively, Documentation and the models, software and algorithms, including machine-learning model code, trained model weights, inference-enabling code, training-enabling code, fine-tuning enabling code, and other elements of the foregoing distributed by Meta and made available under this Agreement.

> a. Grant of Rights. You are granted a non-exclusive, worldwide, non-transferable and royalty-free limited license under Meta’s intellectual property or other rights owned by Meta embodied in the SAM Materials to use, reproduce, distribute, copy, create derivative works of, and make modifications to the SAM Materials.

> v. You are not the target of Trade Controls and your use of SAM Materials must comply with Trade Controls. You agree not to use, or permit others to use, SAM Materials for any activities subject to the International Traffic in Arms Regulations (ITAR) or end uses prohibited by Trade Controls, including those related to military or warfare purposes, nuclear industries or applications, espionage, or the development or use of guns or illegal weapons.

README:
> ⚠️ Before using SAM 3, please request access to the checkpoints on the SAM 3
> Hugging Face [repo](https://huggingface.co/facebook/sam3).

**MapReader** — https://raw.githubusercontent.com/maps-as-data/MapReader/main/LICENSE
> MIT License
> Copyright (c) 2022 The Alan Turing Institute, British Library Board, Queen Mary University of London,
> University of Exeter, University of East Anglia and University of Cambridge

README:
> - Classification pipeline: This pipeline enables users to fine-tune a classification model and predict the labels of patches created from a parent image.
> - Text spotting pipeline: This pipeline enables users to detect and recognize text in map images.

**QGIS** — https://raw.githubusercontent.com/qgis/QGIS/master/COPYING
> GNU GENERAL PUBLIC LICENSE
> Version 2, June 1991

**GDAL** — https://raw.githubusercontent.com/OSGeo/gdal/master/LICENSE.TXT
> GDAL/OGR Licensing
> This file attempts to include all licenses that apply within the GDAL/OGR
> source tree, in particular any that are supposed to be exposed to the end user
> for credit requirements for instance.

### Đề xuất B
1. **QGIS Georeferencer + GDAL** cho nắn chỉnh và polygon hoá; **SAM 2 (Apache-2.0, cả checkpoint)** dùng có prompt (điểm/khung do người đặt) để tách từng khối nhà, sau đó người kiểm tay. Không dựa vào SAM zero-shot tự động (IoU ~15–16 theo MapSAM2).
2. Nếu cần tự động hoá quy mô lớn: **U-Net tự huấn luyện** hoặc MapReader (MIT) để sàng lọc patch, rồi SAM 2 tinh chỉnh. Chờ mã MapSAM/MapSAM2 công bố giấy phép trước khi dùng.
- SAM 3: không NC nhưng giấy phép tuỳ chỉnh + gated; chỉ cân nhắc nếu SAM 2 không đủ, và cần chủ dự án duyệt điều khoản.

---

## C. Phục chế / phóng to ảnh khắc và ảnh lưu trữ; độ sâu cho parallax 2.5D

### Bảng C1 — Phục chế, phóng to, tô màu

| Công cụ | Phiên bản / ngày | Giấy phép mã | Giấy phép trọng số | Thương mại OK? | CPU ok? | URL đã đọc |
|---|---|---|---|---|---|---|
| Real-ESRGAN | `realesrgan` 0.3.0 (PyPI 2022-09-20) | BSD-3-Clause | Không có giấy phép riêng (phát hành trong GitHub Releases của repo BSD-3) | **Có** | Có (x4plus ~ chậm, chưa đo; có tile) | raw.githubusercontent.com/xinntao/Real-ESRGAN/master/LICENSE + README.md + docs/model_zoo.md |
| SwinIR | (repo) | Apache-2.0 | Không có giấy phép riêng (theo repo) | Có (rủi ro nhỏ: huấn luyện trên DIV2K/Flickr2K — dữ liệu học thuật) | Chậm hơn Real-ESRGAN | raw.githubusercontent.com/JingyunLiang/SwinIR/main/LICENSE |
| HAT | (repo) | Apache-2.0 | Không có giấy phép riêng | Có (cùng lưu ý dữ liệu) | Chậm (transformer lớn) | raw.githubusercontent.com/XPixelGroup/HAT/main/LICENSE |
| GFPGAN | `gfpgan` 1.3.8 (2022-09-16) | Apache-2.0 **trừ thành phần bên thứ ba**; thành phần StyleGAN2 kèm **NVIDIA License "non-commercially"** | Không ghi riêng | **Rủi ro — coi như KHÔNG** (điều 3.3 NVIDIA trong chính file LICENSE) | Có | raw.githubusercontent.com/TencentARC/GFPGAN/master/LICENSE |
| CodeFormer | (repo); PyPI `codeformer` 0.0.11 ghi "MIT" là **bản đóng gói bên thứ ba**, không phải giấy phép gốc | **S-Lab License 1.0 — NC** | NC | **KHÔNG — LOẠI** | — | raw.githubusercontent.com/sczhou/CodeFormer/master/LICENSE |
| SUPIR | (repo) | **SUPIR Software License — NC** | **NC** | **KHÔNG — LOẠI** | Không (SDXL + LLaVA, ≥12 GB VRAM) | raw.githubusercontent.com/Fanghua-Yu/SUPIR/master/LICENSE + README.md |
| DeOldify | `deoldify` 0.0.1 (2023-06-05) | MIT | **MIT** (README: "trained by ourselves and are released under the MIT license") | Có | Có (chậm, chưa đo) | raw.githubusercontent.com/jantic/DeOldify/master/LICENSE + README.md |
| BOPBTL (Microsoft) | (repo) | MIT | (theo repo MIT; chưa kiểm riêng phần mô hình mặt) | Có | Chậm, có thể chạy CPU | raw.githubusercontent.com/microsoft/Bringing-Old-Photos-Back-to-Life/master/LICENSE |
| NAFNet | (repo) | MIT | theo repo | Có | Có (nhẹ; khử nhiễu/khử mờ) | raw.githubusercontent.com/megvii-research/NAFNet/main/LICENSE |
| Restormer | (repo) | MIT | theo repo | Có | Chậm (ảnh lớn cần tile) | raw.githubusercontent.com/swz30/Restormer/main/LICENSE.md |
| waifu2x | (repo) | MIT | theo repo | Có | Có (thiết kế cho tranh vẽ/anime; hợp nét khắc đơn giản) | raw.githubusercontent.com/nagadomi/waifu2x/master/LICENSE |

### Bảng C2 — Ước lượng độ sâu

| Công cụ | Phiên bản / ngày | Giấy phép mã | Giấy phép trọng số | Thương mại OK? | CPU ok? | URL đã đọc |
|---|---|---|---|---|---|---|
| Depth Anything V2 | Small / Base / Large / Giant | Apache-2.0 (Small) | **Small: Apache-2.0; Base/Large/Giant: CC-BY-NC-4.0** (đã xác nhận cả README GitHub và HF card) | **Chỉ Small** | Small (~25M) có | raw.githubusercontent.com/DepthAnything/Depth-Anything-V2/main/README.md; huggingface.co/depth-anything/Depth-Anything-V2-{Small,Base,Large} |
| Depth Anything 3 (ByteDance Seed) | `depth-anything-3` 0.1.1 (PyPI 2026-03-04); checkpoint `-1.1` | Apache-2.0 | **DA3-SMALL, DA3-BASE, DA3METRIC-LARGE, DA3MONO-LARGE: Apache-2.0**; **DA3-LARGE, DA3-GIANT(-1.1), DA3NESTED-GIANT-LARGE(-1.1): CC BY-NC 4.0**. ⚠️ Mâu thuẫn: HF card `DA3-LARGE-1.1` ghi `apache-2.0` nhưng bảng README GitHub ghi CC BY-NC 4.0 ⇒ coi là NC | Có cho Small/Base/Mono-Large/Metric-Large | Small/Base có; Mono-Large (0.35B) chậm nhưng khả thi (chưa đo) | raw.githubusercontent.com/ByteDance-Seed/Depth-Anything-3/main/README.md + LICENSE; HF cards DA3-BASE, DA3MONO-LARGE, DA3METRIC-LARGE, DA3-LARGE, DA3-LARGE-1.1, DA3-GIANT-1.1, DA3NESTED-GIANT-LARGE-1.1 |
| Depth Pro (Apple) | không có trên PyPI | Apple sample-code license (permissive) | **Apple Machine Learning Research Model license — "exclusively for Research Purposes"** (README: weights theo cùng file LICENSE; HF: `license: apple-amlr`) | **KHÔNG — LOẠI** | — | raw.githubusercontent.com/apple/ml-depth-pro/main/LICENSE + README.md; huggingface.co/apple/DepthPro (README + LICENSE) |
| MiDaS | (repo) | MIT | theo repo | Có | Có (bản small rất nhanh) | raw.githubusercontent.com/isl-org/MiDaS/master/LICENSE |
| Marigold | `prs-eth/marigold-depth-v1-1` | Apache-2.0 | **CreativeML Open RAIL++-M** (fine-tune từ stable-diffusion-2) — không NC, có danh sách hạn chế sử dụng | Có (có điều khoản sử dụng hạn chế) | **Kém** (diffusion, nhiều bước) | raw.githubusercontent.com/prs-eth/Marigold/main/LICENSE.txt; huggingface.co/prs-eth/marigold-depth-v1-1 |
| ZoeDepth | (repo) | MIT | theo repo | Có | Có | raw.githubusercontent.com/isl-org/ZoeDepth/main/LICENSE |

Rủi ro bịa (C): Real-ESRGAN/SwinIR/HAT/waifu2x: **bịa chi tiết** (vân, nét, chữ) khi phóng ≥ 4×; với ảnh khắc nên phóng ≤ 2× và so với gốc. GFPGAN/CodeFormer/SUPIR: **bịa khuôn mặt** — rủi ro cao về tính xác thực lịch sử (đằng nào cũng loại vì NC). DeOldify: màu là **đoán**, không phải dữ liệu lịch sử ⇒ phải ghi chú trên phim. Độ sâu: sai quan hệ trước/sau ở ảnh khắc (không có bóng thật) ⇒ cần chỉnh tay mặt nạ.

### Trích dẫn nguyên văn (C)

**Real-ESRGAN** — https://raw.githubusercontent.com/xinntao/Real-ESRGAN/master/LICENSE
> BSD 3-Clause License
> Copyright (c) 2021, Xintao Wang

**SwinIR**, **HAT** — LICENSE: `Apache License` `Version 2.0, January 2004`.

**GFPGAN** — https://raw.githubusercontent.com/TencentARC/GFPGAN/master/LICENSE
> GFPGAN is licensed under the Apache License Version 2.0 except for the third-party components listed below.

> StyleGAN2
> The codes are modified from the repository stylegan2-pytorch. Many thanks to the author - Kim Seonghyeon 😊 for translating from the official TensorFlow codes to PyTorch ones. Here is the license of stylegan2-pytorch.
> The official repository is https://github.com/NVlabs/stylegan2, and here is the NVIDIA license.

> 3.3 Use Limitation. The Work and any derivative works thereof only
> may be used or intended for use non-commercially. The Work or
> derivative works thereof may be used or intended for use by Nvidia
> or its affiliates commercially or non-commercially. As used herein,
> "non-commercially" means for research or evaluation purposes only.

**CodeFormer** — https://raw.githubusercontent.com/sczhou/CodeFormer/master/LICENSE (xác nhận NC)
> S-Lab License 1.0
> Copyright 2022 S-Lab
> Redistribution and use for non-commercial purpose in source and
> binary forms, with or without modification, are permitted provided
> that the following conditions are met:

> In the event that redistribution and/or use for commercial purpose in
> source or binary forms, with or without modification is required,
> please contact the contributor(s) of the work.

**SUPIR** — https://raw.githubusercontent.com/Fanghua-Yu/SUPIR/master/LICENSE
> SUPIR Software License Agreement
> Copyright (c) 2024 by SupPixel Pty Ltd. All rights reserved.

> a. The Licensor retains all ownership and commercial usage rights in the Licensed Software, including its neural network(s), regardless of the open-source availability of portions of the Licensed Software's source code. Under the open-source license, anyone may freely use, copy, modify, and distribute the source code of the Licensed Software for non-commercial purposes only. Similarly, the proprietary neural network weights, biases, and architecture may only be used for non-commercial purposes.

README:
> The SUPIR ("Software") is made available for use, reproduction, and distribution strictly for non-commercial purposes.

**DeOldify** — https://raw.githubusercontent.com/jantic/DeOldify/master/README.md
> All code in this repository is under the MIT license as specified by the LICENSE
> file.
> The model weights listed in this readme under the "Pretrained Weights" section
> are trained by ourselves and are released under the MIT license.

**BOPBTL** — LICENSE: `MIT License` `Copyright (c) Microsoft Corporation.`
**NAFNet** — `MIT License` `Copyright (c) 2022 megvii-model`
**Restormer** — `MIT License` `Copyright (c) 2022 Syed Waqas Zamir and contributors`
**waifu2x** — `The MIT License` `Copyright (C) 2015 nagadomi`

**Depth Anything V2** — https://raw.githubusercontent.com/DepthAnything/Depth-Anything-V2/main/README.md (xác nhận giả định của bạn)
> Depth-Anything-V2-Small model is under the Apache-2.0 license. Depth-Anything-V2-Base/Large/Giant models are under the CC-BY-NC-4.0 license.

HF cards: Small `license: apache-2.0`; Base `license: cc-by-nc-4.0`; Large `license: cc-by-nc-4.0`.

**Depth Anything 3** — https://raw.githubusercontent.com/ByteDance-Seed/Depth-Anything-3/main/README.md (bảng mô hình, cột License)
> | [DA3-GIANT-1.1](https://huggingface.co/depth-anything/DA3-GIANT-1.1) | 1.15B | … | CC BY-NC 4.0 |
> | [DA3-LARGE-1.1](https://huggingface.co/depth-anything/DA3-LARGE-1.1) | 0.35B | … | CC BY-NC 4.0 |
> | [DA3-BASE](https://huggingface.co/depth-anything/DA3-BASE) | 0.12B | … | Apache 2.0 |
> | [DA3-SMALL](https://huggingface.co/depth-anything/DA3-SMALL) | 0.08B | … | Apache 2.0 |
> | [DA3METRIC-LARGE](https://huggingface.co/depth-anything/DA3METRIC-LARGE) | 0.35B | … | Apache 2.0 |
> | [DA3MONO-LARGE](https://huggingface.co/depth-anything/DA3MONO-LARGE) | 0.35B | … | Apache 2.0 |

(Rút gọn bằng "…" các cột tính năng; cột License giữ nguyên.) HF card DA3MONO-LARGE: `license: apache-2.0`, `| **License** | Apache 2.0 |`.

**Depth Pro** — https://raw.githubusercontent.com/apple/ml-depth-pro/main/README.md
> This sample code is released under the [LICENSE](LICENSE) terms.
> The model weights are released under the [LICENSE](LICENSE) terms.

https://huggingface.co/apple/DepthPro/raw/main/LICENSE (`license: apple-amlr`)
> Disclaimer: IMPORTANT: This Apple Machine Learning Research Model is
> specifically developed and released by Apple Inc. ("Apple") for the sole purpose
> of scientific research of artificial intelligence and machine-learning
> technology.

> limited license, to use, copy, modify, distribute, and create Model
> Derivatives (defined below) of the Apple Machine Learning Research Model
> exclusively for Research Purposes. You agree that any Model Derivatives You
> may create or that may be created for You will be limited to Research Purposes
> as well. “Research Purposes” means non-commercial scientific research and
> academic development activities, such as experimentation, analysis, testing
> conducted by You with the sole intent to advance scientific knowledge and
> research. “Research Purposes” does not include any commercial exploitation,
> product development or use in any commercial product or service.

(Ghi chú: file LICENSE trên GitHub ml-depth-pro hiện là giấy phép mẫu mã Apple dạng permissive — "Apple grants you a personal, non-exclusive license … to use, reproduce, modify and redistribute the Apple Software" — nhưng giấy phép trên HF cho **trọng số** là research-only. Áp dụng điều chặt hơn ⇒ LOẠI.)

**MiDaS** — `MIT License` `Copyright (c) 2019 Intel ISL (Intel Intelligent Systems Lab)`
**ZoeDepth** — `MIT License` `Copyright (c) 2022 Intelligent Systems Lab Org`

**Marigold** — LICENSE.txt: `Apache License` `Version 2.0, January 2004`; HF card https://huggingface.co/prs-eth/marigold-depth-v1-1/raw/main/README.md:
> - **License:** [CreativeML Open RAIL++-M License](https://huggingface.co/stabilityai/stable-diffusion-2/blob/main/LICENSE-MODEL).
> The model is fine-tuned from the `stable-diffusion-2` [model](https://huggingface.co/stabilityai/stable-diffusion-2) as

### Đề xuất C
1. **Phục chế/phóng to:** **Real-ESRGAN (BSD-3)** cho ảnh lưu trữ, phóng ≤ 2× (kiểm trực quan với gốc); với ảnh khắc nét mảnh cân nhắc waifu2x (MIT) hoặc chỉ khử nhiễu bằng NAFNet (MIT). Tô màu (nếu thật cần): DeOldify (MIT cả trọng số) kèm ghi chú "colorized" trên phim.
2. **Độ sâu 2.5D:** **Depth Anything 3 — DA3MONO-LARGE (Apache-2.0)**, dự phòng nhẹ **Depth Anything V2 Small** hoặc DA3-SMALL (Apache-2.0); MiDaS (MIT) làm phương án nhanh. Chỉnh tay mặt nạ trước khi dựng parallax.
- LOẠI: CodeFormer (S-Lab NC), SUPIR (NC), Depth Pro (research only), DA2 Base/Large/Giant và DA3 Large/Giant/Nested (CC-BY-NC). GFPGAN: rủi ro do thành phần NVIDIA NC ⇒ không dùng.

---

## D. YouTube — công khai nội dung bị thay đổi / tổng hợp (Altered or synthetic content)

URL: https://support.google.com/youtube/answer/14328491?hl=en (HTTP 200, đọc 2026-10-18). Tiêu đề trang hiện tại: **"Disclosing use of GenAI content"**.

Trích nguyên văn các phần liên quan:

> We require creators to disclose AI-generated or altered content that seems realistic. Creators can make this disclosure during the upload process.
> Creators must disclose GenAI content that:
> - Makes a real person appear to say or do something they didn’t do.
> - Alters footage of a real event or place.
> - Generates a realistic scene that didn’t actually occur.
> - Creates music that’s the main focus of the video.

> Realistic AI content and meaningful changes require disclosure, while non-realistic or minor edits don’t. Keep in mind, this isn’t a complete list.

> Creators don’t need to disclose non-realistic content that’s made with AI, or edits to realistic content that are minor. Minor edits are ones that are primarily aesthetic, and don't alter the content in a way that could mislead the viewer about what actually happened.

Danh sách "không cần công khai" (trích đúng các mục liên quan):
> - Color adjustment or lighting filters
> - Special effects filters, like adding background blur or vintage effects
> - Production assistance, like using generative AI tools to create or improve a video outline, script, thumbnail, title, or infographic
> - Video sharpening, upscaling or repair and voice or audio repair
> - Using an AI-generated or altered animation of a missile in a fully animated video
> - AI generating or extending a backdrop to simulate a moving car

Danh sách "cần công khai" (trích các mục liên quan):
> - AI generated music
> - AI generated extra footage of a real place, like a video of a surfer in Maui for a promotional travel video
> - Showing a realistic depiction of a tornado or other weather events moving toward a real city that didn’t actually happen

Về nhãn và kiếm tiền:
> Labels may appear in the expanded description for non-music AI-generated audio or AI content that is non-photorealistic or animated.
> Note: Disclosing AI content alone won’t limit a video’s audience or impact its eligibility to earn money.

> YouTube may automatically apply an AI label on the video player or in the expanded description for:
> - Content made using YouTube's GenAI tools
> - Content that contains C2PA metadata
> - Content that our internal systems detect is Al generated or altered

> Creators who consistently choose not to disclose this information may be subject to manual application of a label, or penalties from YouTube, including removal of content or suspension from the YouTube Partner Program.

**Nhận định:**
- **Upscaling / phục chế**: trang ghi rõ "Video sharpening, upscaling or repair" thuộc nhóm **không cần công khai** (chỉnh sửa nhỏ).
- **"Làm ảnh tĩnh chuyển động" / parallax độ sâu từ ảnh thật**: trang **không có ví dụ nào nói trực tiếp** (đã tìm toàn văn trang; không có cụm "still image", "photo", "animate", "parallax", "depth"). Áp dụng tiêu chí chung: parallax 2.5D thuần thị giác không đổi sự kiện ⇒ gần "minor/aesthetic"; nhưng nếu AI **sinh thêm** người/vật/chuyển động không có trong ảnh (ví dụ người trong ảnh cử động, khói bay do AI vẽ) mà trông thật ⇒ rơi vào "Alters footage of a real event or place" / "Generates a realistic scene that didn’t actually occur" ⇒ **nên công khai**. Đây là suy luận, không phải câu chữ của YouTube.
- Tái dựng 3D phong cách hoá (không photoreal) ⇒ thuộc "non-realistic", không bắt buộc công khai; nhãn nếu có sẽ ở phần mô tả, không ở trình phát.
- Lưu ý C2PA: nếu công cụ ghi metadata C2PA, YouTube có thể tự gắn nhãn và **không thể gỡ**.

---

## Thống kê nguồn

- **URL đọc thành công: ~120** (57/58 file trong lô tải chính; 22 truy vấn PyPI JSON; 8 HF card DA3/Depth Pro; 7 HF card Qwen/Florence/olmOCR/TrOCR + 3 LICENSE; 6 Zenodo API + 1 tìm kiếm Zenodo; arXiv 2508.03564; MapSAM2 qua WebFetch; README SAM v1, MapReader, ml-depth-pro, tessdoc, calamari_models ×2, Real-ESRGAN model_zoo; 5 file tessdata_best `.traineddata` để kiểm ſ; trang YouTube).
- **Bị chặn / lỗi:**
  - `huggingface.co/facebook/sam3` README: **HTTP 401** (repo gated).
  - `github.com/<repo>/releases.atom` ×10 và `gh api repos/...` ×17: **HTTP 403** (proxy: phiên chỉ gắn repo dự án) ⇒ không đọc được ngày release GitHub.
  - `raw.githubusercontent.com/tesseract-ocr/langdata_lstm/main/script/Latin.unicharset`: **404**; `tessdata_best/frk.traineddata`: **404** (đã đổi tên thành `deu_latf`).
  - PyPI `depth-pro`, `marigold-depth`: **404** (không phát hành trên PyPI).
- Không ghi gì vào `/home/user/cine-lab`.

## Việc còn mở (cần đo/kiểm thêm)
1. Đo thật thời gian/trang trên CPU 4 lõi: Tesseract `enm`, kraken CATMuS-Print Large, Real-ESRGAN x2, DA3MONO-LARGE, SAM 2 tiny.
2. Ngày release GitHub (Tesseract 5.5.3 mới chỉ có nguồn Wikipedia).
3. Số IoU của Xydas 2022 và Zhao 2022 (chưa đọc toàn văn).
4. Quy ước ſ của Calamari `historical_french`.
5. Chủ dự án duyệt: dùng CC-BY (CATMuS) ⇒ ghi công trong credits và `RIGHTS.md`.
