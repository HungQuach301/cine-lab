# R2-ai2 — Giấy phép: ước lượng tư thế, kho mocap, sách điều lệnh cổ và bộ sưu tập bảo tàng

Ngày đọc: **2026-10-18** (mọi URL dưới đây đọc trong ngày này, trừ chỗ ghi "BỊ CHẶN" hoặc "nguồn thứ cấp").
Bối cảnh: kênh YouTube lịch sử có kiếm tiền và bán phim; đám đông người 3D (MakeHuman/MPFB CC0) trong Blender; container chỉ có CPU.
Quy tắc loại: mọi giấy phép **NC (phi thương mại)**, **SA/copyleft** hoặc **"chỉ nghiên cứu"** trên dữ liệu hay trọng số mô hình đều **BỊ LOẠI**.

Ký hiệu phân loại: **OK** = dùng thương mại được · **NC** = phi thương mại/chỉ nghiên cứu (LOẠI) · **SA** = chia sẻ tương tự/copyleft (LOẠI) · **KHÔNG RÕ** = chưa đủ bằng chứng, không dùng cho tới khi làm rõ.

Ghi chú phương pháp: trích dẫn tiếng Anh/Tây Ban Nha giữ nguyên văn. Các trích dẫn lấy bằng `curl` từ tệp LICENSE thô hoặc HTML gốc là nguyên văn chắc chắn. Một số trích dẫn lấy qua WebFetch (mô hình tóm tắt trả về câu trong ngoặc kép); những chỗ đó ghi "(qua WebFetch)" và nên đối chiếu lại một lần trước khi ghi vào `RIGHTS.md`.

---

## A. Ước lượng tư thế từ phim tư liệu

### A.1 Bảng tổng hợp

| Công cụ | Giấy phép mã | Trọng số / phụ thuộc | Ra 3D? Không cần SMPL? | CPU | Phân loại |
|---|---|---|---|---|---|
| **MediaPipe Pose (BlazePose GHUM 3D)** | Apache-2.0 | Model card: "LICENSED UNDER Apache License, Version 2.0" | Có: 33 điểm (x, y, z) + world landmarks; **không cần SMPL** (z "not metric but up to scale") | Có (Lite ~44 FPS CPU trên Pixel 3) | **OK** |
| **rtmlib** (RTMPose/RTMW/YOLOX qua ONNX) | Apache-2.0 | Trọng số tải từ `download.openmmlab.com`; trang rtmlib **không nêu giấy phép trọng số** | Chỉ 2D (cần bộ nâng 3D riêng) | Có (`device='cpu'`, `backend='onnxruntime'`) | Mã **OK**; trọng số **KHÔNG RÕ** (dữ liệu huấn luyện body7/HumanArt chưa kiểm) |
| **MMPose** | Apache-2.0 | như trên | 2D (có module 3D) | Có | Mã **OK**; trọng số **KHÔNG RÕ** |
| **ViTPose** | Apache-2.0 (tệp LICENSE là bản OpenMMLab) | Trọng số huấn luyện trên COCO/AIC… chưa kiểm | 2D | Chậm trên CPU | Mã **OK**; trọng số **KHÔNG RÕ** |
| **OpenPose** | Giấy phép riêng CMU, **phi thương mại** | — | 2D | Có | **NC — LOẠI** |
| **YOLO11-pose (Ultralytics)** | **AGPL-3.0** hoặc Enterprise trả phí | Trọng số cũng AGPL | 2D | Có | **SA/copyleft — LOẠI** (trừ khi mua Enterprise) |
| **4DHumans / HMR2.0** | MIT | **Bắt buộc SMPL** (NC) | 3D dạng SMPL | Rất chậm | **NC qua SMPL — LOẠI** |
| **WHAM** | MIT | **Bắt buộc SMPL/SMPLify** (NC); huấn luyện trên AMASS (NC) | 3D dạng SMPL | Không thực tế | **NC — LOẠI** |
| **TRAM** | MIT | **Bắt buộc SMPL/SMPLify**; khởi tạo từ HMR2b; dùng BEDLAM | 3D dạng SMPL | Không thực tế | **NC — LOẠI** |
| **GVHMR** | Giấy phép riêng ZJU: "educational, research and non-profit purposes only" | + SMPL | 3D dạng SMPL | Không | **NC — LOẠI** (hai lớp) |
| **SMPL / SMPL-X** (mô hình cơ thể) | MPI license | — | — | — | **NC — LOẠI** (thương mại phải mua qua Meshcapade) |
| **MotionBERT** (nâng 2D→3D, không SMPL) | Apache-2.0 | Trọng số huấn luyện trên **Human3.6M** (EULA "academic use only") | 3D 17 khớp H36M, **không cần SMPL** | Được (mô hình nhỏ) | Mã **OK**; trọng số **KHÔNG RÕ/nghiêng NC** — không dùng bản tải sẵn |

**Kết luận A:** Đường duy nhất sạch hoàn toàn và chạy CPU là **MediaPipe Pose Landmarker (BlazePose GHUM 3D, Apache-2.0)** → 33 điểm 3D world-landmark → retarget sang rig MPFB bằng ràng buộc IK/hướng xương trong Blender (không qua SMPL). RTMPose (rtmlib) cho 2D tốt hơn trên đám đông, nhưng cần làm rõ giấy phép trọng số trước khi dùng. Mọi lựa chọn dựa trên SMPL (4DHumans, WHAM, TRAM, GVHMR) đều bị loại vì SMPL là NC.

### A.2 Trích dẫn nguyên văn

**MediaPipe BlazePose GHUM 3D — model card**
URL: https://storage.googleapis.com/mediapipe-assets/Model%20Card%20BlazePose%20GHUM%203D.pdf (PDF, trích bằng `pdftotext`)
> "LICENSED UNDER Apache License, Version 2.0"
> "Note, that Z is not metric but up to scale."
> "The model is not intended for human life-critical decisions. The primary intended application is entertainment."

**rtmlib** — https://github.com/Tau-J/rtmlib (README thô: https://raw.githubusercontent.com/Tau-J/rtmlib/main/README.md)
Trang ghi giấy phép "Apache-2.0". Ví dụ mã trong README: `device = 'cpu'  # cpu, cuda, mps` · `backend = 'onnxruntime'  # opencv, onnxruntime, openvino`. Mặc định tải các tệp như `rtmpose-m_simcc-body7_pt-body7_420e-256x192-e48f03d0_20230504.zip` và `yolox_m_8xb8-300e_humanart-c2c7a14a.zip` từ `download.openmmlab.com`. README **không có câu nào về giấy phép trọng số**.

**MMPose** — https://raw.githubusercontent.com/open-mmlab/mmpose/main/LICENSE
> "Copyright 2018-2020 Open-MMLab. All rights reserved.
>
>                                  Apache License
>                            Version 2.0, January 2004"

**ViTPose** — https://raw.githubusercontent.com/ViTAE-Transformer/ViTPose/main/LICENSE: cùng văn bản Apache 2.0 như trên ("Copyright 2018-2020 Open-MMLab. All rights reserved.").

**OpenPose** — https://raw.githubusercontent.com/CMU-Perceptual-Computing-Lab/openpose/master/LICENSE (qua WebFetch)
> "The Software may be used for your own noncommercial internal research purposes."
> "for noncommercial research purposes, without the right to sublicense"
> "You may not sell, rent, lease, sublicense, lend, time-share or transfer"

**Ultralytics** — https://www.ultralytics.com/license (qua WebFetch)
> "compliance means publicly releasing the complete corresponding source code for the entire derivative work"
> "including the larger application, modifications, scripts, configuration files, and, where applicable, model weights."
> "An Enterprise License is required if you want to use Ultralytics YOLO without open-sourcing your entire project."
> "All Ultralytics YOLO trained models fall under the AGPL-3.0 License by default."
Hệ quả: trang không nói về đầu ra (keypoint). AGPL là copyleft mạnh, cả trọng số cũng AGPL → theo quy tắc của dự án xếp **SA/copyleft — LOẠI**; nếu cần YOLO thì phải mua Enterprise.

**SMPL** — https://smpl.is.tue.mpg.de/modellicense.html (qua WebFetch)
> "To use the Software for the sole purpose of performing non-commercial scientific research"
> "Any other use, in particular any use for commercial purposes, is prohibited."
> "This includes, without limitation, incorporation in a commercial product, use in a commercial service"
> "production of other artefacts for commercial purposes"
> "The software/data is also available for commercial licensing through Meshcapade.com."
Hệ quả: một phim bán là "artefact for commercial purposes" → mọi pipeline cần tệp SMPL đều **NC**. (SMPL-X dùng cùng khung giấy phép MPI; không đọc riêng trang SMPL-X trong phiên này.)

**GVHMR** — https://raw.githubusercontent.com/zju3dv/GVHMR/main/LICENSE (curl, nguyên văn)
> "Permission to use, copy, modify and distribute this software and its
> documentation for educational, research and non-profit purposes only.
> Any modification based on this work must be open-source and prohibited
> for commercial use."
> "For commercial uses of this software, please send email to <email-đã-che>"

**WHAM** — https://raw.githubusercontent.com/yohanshin/WHAM/main/LICENSE: "MIT License / Copyright (c) 2023 Soyong Shin". README (https://raw.githubusercontent.com/yohanshin/WHAM/main/README.md):
> "To download SMPL body models (Neutral, Female, and Male), you need to register for [SMPL](https://smpl.is.tue.mpg.de/) and [SMPLify](https://smplify.is.tue.mpg.de/)."
> "WHAM training involves into two different stages; (1) 2D to SMPL lifting through AMASS dataset …"

**4D-Humans / HMR2.0** — https://raw.githubusercontent.com/shubham-goel/4D-Humans/main/LICENSE.md: "MIT License / Copyright (c) 2023 UC Regents, Shubham Goel". README:
> "Besides these files, you also need to download the *SMPL* model."

**TRAM** — https://raw.githubusercontent.com/yufu-wang/tram/main/LICENSE: "MIT License / Copyright (c) 2024 Yufu Wang". README:
> "Register at [SMPLify](https://smplify.is.tue.mpg.de) and [SMPL](https://smpl.is.tue.mpg.de), whose usernames and passwords will be used by our script to download the SMPL models. … Note that thirdparty models have their own licenses."

**MotionBERT** — https://raw.githubusercontent.com/Walter0807/MotionBERT/main/LICENSE: Apache License 2.0. README: "The model uses 17 body keypoints ([H36M format]…)"; bảng tải "3D Pose (H36M-SH, scratch)", "3D Pose (H36M-SH, ft)".
**Human3.6M EULA** — http://vision.imar.ro/human3.6m/eula.php (qua WebFetch)
> "Licenses free of charge are limited to academic use only."
> "for commercial licensing, please contact us at the following email address"
Hệ quả: EULA không nói trực tiếp về mô hình đã huấn luyện → trọng số MotionBERT **KHÔNG RÕ, nghiêng NC**; không dùng.

---

## B. Kho dữ liệu motion capture (đi, đứng, mang vác)

### B.1 Bảng tổng hợp

| Kho | Giấy phép | Phân loại | Ghi chú cho dự án |
|---|---|---|---|
| **CMU Graphics Lab Mocap** | Điều khoản riêng trên trang | **OK** (cấm bán lại dữ liệu thô) | ~2.600 clip, nhiều đi/đứng/mang vác; BVH đã chuyển đổi có sẵn |
| **Bandai Namco Research Motion Dataset 1 & 2** | **CC BY-NC 4.0** | **NC — LOẠI** | Phần script Blender là MIT, dữ liệu thì NC |
| **100STYLE** | **CC BY 4.0** | **OK** (ghi công) | 100 phong cách đi; rất hợp cho đám đông |
| **LaFAN1 (Ubisoft)** | **CC BY-NC-ND 4.0** | **NC + ND — LOẠI** | |
| **AMASS** | MPI, "non-commercial scientific research…" | **NC — LOẠI** | |
| **HumanML3D** | Mã MIT; dữ liệu tái tạo từ **AMASS** + HumanAct12 | **NC — LOẠI** (kế thừa AMASS) | |
| **Mixamo (Adobe)** | Điều khoản Adobe | **OK, cần xác minh** (trang gốc BỊ CHẶN 403) | Theo nguồn thứ cấp: dùng miễn phí bản quyền trong phim; cấm phân phối tệp thô |
| **SFU Motion Capture Database** | Điều khoản riêng | **NC — LOẠI** | |
| **KIT Whole-Body Motion Database** | Không đọc được (trang chạy JS) | **KHÔNG RÕ, nghiêng NC** | Nguồn thứ cấp nói chỉ nghiên cứu phi thương mại |
| **Motorica Dance Dataset** | Điều khoản riêng, "Non-commercial use" | **NC — LOẠI** | |
| **Quaternius Universal Animation Library** | **CC0** | **OK** | rig "universal humanoid", có .blend; không có clip "carry" ghi rõ |
| **OpenGameArt** | Theo từng tác phẩm (CC0 / CC-BY / CC-BY-SA / GPL) | **Theo từng tác phẩm**; chỉ lấy CC0/CC-BY; **CC-BY-SA và GPL bị LOẠI** | |
| **Rokoko free library (150 động tác)** | Không đọc được văn bản giấy phép gốc | **KHÔNG RÕ** (nguồn thứ cấp nói được dùng thương mại) | Phải đọc EULA trong Rokoko Studio trước khi dùng |

### B.2 Trích dẫn nguyên văn

**CMU** — http://mocap.cs.cmu.edu/ (curl, nguyên văn)
> "This dataset of motions is free for all uses."
> "This data is free for use in research projects."
> "You may include this data in commercially-sold products, but you may not resell this data directly, even in converted form."
(Trang FAQ http://mocap.cs.cmu.edu/faqs.php và info http://mocap.cs.cmu.edu/info.php không thêm hạn chế.) Trang cũng đề nghị ghi câu cảm ơn "The data used in this project was obtained from mocap.cs.cmu.edu…" → nên đưa vào credits.

**Bandai Namco** — https://raw.githubusercontent.com/BandaiNamcoResearchInc/Bandai-Namco-Research-Motiondataset/master/README.md và `dataset/Bandai-Namco-Research-Motiondataset-1/LICENSE`
> "- Bandai-Namco-Research-Motiondataset-1: [CC BY-NC 4.0](dataset/Bandai-Namco-Research-Motiondataset-1/LICENSE)
> - Bandai-Namco-Research-Motiondataset-2: [CC BY-NC 4.0](dataset/Bandai-Namco-Research-Motiondataset-2/LICENSE)
> - Motion visualization on Blender: [MIT](utils/blender/LICENSE)"
Tệp LICENSE mở đầu: "Attribution-NonCommercial 4.0 International".

**100STYLE** — https://www.ianxmason.com/100style/ (curl, nguyên văn)
> "For creative or commercial work please credit in an appropriate way."
> "This work is licensed under a Creative Commons Attribution 4.0 International License."
(liên kết tới creativecommons.org/licenses/by/4.0)

**LaFAN1** — https://raw.githubusercontent.com/ubisoft/ubisoft-laforge-animation-dataset/master/license.txt và README
> "This dataset can be used under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International Public License (see license.txt)."

**AMASS** — https://amass.is.tue.mpg.de/license.html (curl, nguyên văn)
> "License for non-commercial scientific research purposes"
> "To use the Dataset for the sole purpose of performing non-commercial scientific research, non-commercial education, or non-commercial artistic projects;"
> "This includes, without limitation, incorporation in a commercial product, use in a commercial service, or production of other artefacts for commercial purposes."
> "This license also prohibits the use of the Dataset to train methods/algorithms/neural networks/etc. for commercial use of any kind."

**HumanML3D** — https://raw.githubusercontent.com/EricGuo5513/HumanML3D/main/README.md
> "HumanML3D is a 3D human motion-language dataset that originates from a combination of [HumanAct12](…) and [Amass](…) dataset."
> "Due to the distribution policy of AMASS dataset, we are not allowed to distribute the data directly."
(Tệp LICENSE là "MIT License / Copyright (c) 2022 Chuan Guo" — chỉ áp cho mã.)

**SFU** — http://mocap.cs.sfu.ca/ (curl, nguyên văn)
> "This dataset of motions is free for research purposes."
> "The data cannot be used for commercial products or resale, unfortunately."

**Motorica Dance** — https://raw.githubusercontent.com/simonalexanderson/MotoricaDanceDataset/main/LICENSE.txt
> "The motion in this database is (c) copyright Motorica AB, with all rights reserved."
> "The Motorica Dance Dataset is free to use for research purposes by academic institutes, companies, and individuals. Use for commercial purposes is not permitted without prior written consent. This includes, without limitation, incorporation in a commercial product, use in a commercial service, or training machine-learning algorithms for commercial purposes."

**KIT** — https://motion-database.humanoids.kit.edu/ trả về trang JS, không trích được điều khoản. Nguồn thứ cấp (WebSearch, bài arXiv 2411.00128) nói các bộ dữ liệu này "allow usage of their data for non-commercial scientific research". → **KHÔNG RÕ, nghiêng NC**.

**Quaternius Universal Animation Library** — https://quaternius.com/packs/universalanimationlibrary.html (qua WebFetch)
> "Free to use in personal, educational and commercial projects. (CC0 License)"
> "Locomotion in 8 directions, jog, sprint, push, crawling, swimming, sitting, death animations and more."

**OpenGameArt FAQ** — https://opengameart.org/content/faq (qua WebFetch)
> CC0: "This license is the creative commons team's equivalent of public domain."
> CC-BY-SA: "These licenses are extensions of the CC-BY licenses." (sản phẩm phái sinh phải dùng cùng giấy phép → LOẠI)
> "Some artists have multiple licenses listed"

**Mixamo** — https://helpx.adobe.com/creative-cloud/faq/mixamo-faq.html và bản /ca/: **BỊ CHẶN (403)**. Tóm tắt trang này qua WebSearch (nguồn thứ cấp, không phải nguyên văn đã đọc): các nhân vật và hoạt cảnh dùng được "royalty free for personal, commercial, and non-profit projects", gồm cả "creating films". Bài Adobe Community (2022) nói không được phân phối tệp nhân vật/hoạt cảnh thô. **Cần chủ dự án mở trang bằng trình duyệt và lưu bản PDF điều khoản trước khi dùng.**

**Rokoko** — không đọc được văn bản gốc. Tin năm 2020 (cgchannel.com, awn.com) nói 150 động tác miễn phí được dùng thương mại. → **KHÔNG RÕ**.

---

## C. Sách điều lệnh quân sự (phạm vi công cộng) đã số hoá

Tác phẩm gốc (1635–1780) đều **thuộc phạm vi công cộng** do quá hạn. Rủi ro chỉ nằm ở **điều khoản của bản số hoá**. Luận cứ pháp lý về ảnh chụp tác phẩm 2D thuộc PD (mục D) áp dụng cho các bản quét.

### C.1 Bảng tổng hợp

| Nhóm | Tác phẩm | Bản số hoá (URL) | Điều khoản bản số hoá | Hình khắc tư thế? |
|---|---|---|---|---|
| (i) Anh TK18 | *The Manual Exercise, As Ordered By His Majesty, In The Year 1764* (bản in 1776) | https://archive.org/details/the-manual-exercise-as-ordered-by-his-majesty-in-the-year-1764 | **CC0** (licenseurl: creativecommons.org/publicdomain/zero/1.0/) | Chưa kiểm (chủ yếu là văn bản khẩu lệnh) |
| | *New manual exercise as performed by His Majesty's dragoons, foot-guards, foot, artillery, marines…* 1758 | https://archive.org/details/bim_eighteenth-century_new-manual-exercise-as-p_great-britain-army_1758 | Không ghi rights (bản quét vi phim) | Chưa kiểm |
| | *The manual exercise, with explanations, as ordered by His Majesty* 1770 | https://archive.org/details/bim_eighteenth-century_the-manual-exercise-wit_great-britain-army_1770 | Không ghi rights | Chưa kiểm |
| | Humphrey Bland, *A Treatise of Military Discipline* 1727 | https://archive.org/details/bim_eighteenth-century_a-treatise-of-military-d_bland-humphrey_1727 | Không ghi rights | Có bản đồ đội hình (theo thư mục học; chưa kiểm trong phiên) |
| | Bland, các bản 1734, 1743, 1746 | …`_bland-humphrey_1734`, `_1743`, `_1746` (cùng tiền tố như trên) | Không ghi rights | Chưa kiểm |
| | *Rules and Regulations for the Formations, Field-Exercise…* (Dundas) | https://archive.org/details/rulesandregulat00fawcgoog (1794, NOT_IN_COPYRIGHT); https://archive.org/details/cihm_40650 (1793) | Google/CIHM; PD | **Lưu ý: là 1792, sau Gibraltar (1779–83) → không dùng làm chuẩn cho 1779–83** |
| | Bản gần thời Gibraltar: *[Regulations. 1780]. Standing orders, regulations, exercise, evolutions…* | https://archive.org/details/bim_eighteenth-century_regulations-1780-sta_great-britain-army-lig_1780 | Không ghi rights | Chưa kiểm |
| | John Muller, *A Treatise of Artillery* 1768 và 1780 | https://archive.org/details/bim_eighteenth-century_a-treatise-of-artillery_muller-john_1780 ; …`_muller-john_1768` | Không ghi rights | Có bảng khắc (tựa ghi kích cỡ súng; chưa kiểm hình người thao tác) |
| (ii) Tây Ban Nha TK18 | *Ordenanzas de S.M. para el régimen, disciplina, subordinación y servicio de sus exércitos* 1768 | https://archive.org/details/bub_gb_JQ7gfF99ZlIC (U. Michigan, **Public Domain Mark**); https://archive.org/details/bub_gb_8dUCh4xp-F8C (**tomo segundo**, PDM); https://archive.org/details/ordenanzasdesmp00spaigoog , …01spaigoog (NOT_IN_COPYRIGHT) | **PDM 1.0** / NOT_IN_COPYRIGHT | Tomo II chứa phần "manejo del arma"; chưa kiểm hình |
| | *Ordenanzas … tomo segundo que contiene la formacion, manejo de arma, y evoluciones … en la Infanteria* 1762 | https://archive.org/details/A303417 (Biblioteca de la Universidad de Sevilla) | **Public Domain Mark 1.0** | **Có — "XVI h. de grab. pleg."** (16 tờ khắc gấp) — nguồn tốt nhất cho thao tác súng Tây Ban Nha thời Gibraltar |
| | *Libro de figuras … del manejo del arma* (Madrid 1762) | Chỉ thấy bản ghi vật lý (americanrevolutioninstitute.org), chưa thấy bản số hoá | — | Có (toàn bộ là hình) |
| | Biblioteca Virtual de Defensa | https://bibliotecavirtual.defensa.gob.es/BVMDefensa/en/catalogo_imagenes/grupo.do?path=51564 (*Reglamento para el ejercicio y maniobras de la Infantería*, không rõ năm — bản trên archive.org là 1808, quá muộn) | Chưa đọc điều khoản BVD | — |
| (iii) Anh TK17 | Henry Hexham, *The Principles of the Art Militarie* 1637 (+ phần 2 1638/39, phần 3 1640) | https://archive.org/details/bim_early-english-books-1475-1640_the-principles-of-the-ar_hexham-henry_1637 | Không ghi rights (vi phim) | Có hình tư thế (theo thư mục học; chưa kiểm trong phiên) |
| | William Barriffe, *Military Discipline: or, the Young Artillery Man* 1635 (và 1639, 1643, 1647, 1661) | Ảnh: https://archive.org/details/bim_early-english-books-1475-1640_military-discipline-or-_barriffe-william_1635 ; …1641-1700_militarie-discipline_barriffe-william_1661. **Văn bản EEBO-TCP CC0:** http://hdl.handle.net/20.500.14106/A04919 | Văn bản TCP: **CC0** (đã xác minh) | Tựa: "the postures both of musket and pike" |
| | Richard Elton, *The Compleat Body of the Art Military* 1650 (và 1659, 1668) | https://archive.org/details/bim_early-english-books-1641-1700_the-compleat-body-of-the_elton-richard_1650 | Không ghi rights | Có (theo thư mục học; chưa kiểm) |
| | *The Military discipline wherein is martially showne the order for driling the musket and pike: set forth in postures…* 1642 | Văn bản EEBO-TCP: http://hdl.handle.net/20.500.14106/A50851 | **CC0** cho văn bản; **ảnh trang KHÔNG thuộc CC0** | Là sách hình tư thế |
| | Gerat Barry, *A Discourse of Military Discipline* (1634) | http://hdl.handle.net/20.500.14106/A05146 | CC0 (văn bản) | "additional title page, engraved" |
| | Huấn luyện dân quân 1660s–70s | Không tìm thấy qua archive.org trong phiên này | — | — |

### C.2 Trích dẫn nguyên văn

**EEBO-TCP Phase I — bản ghi Oxford Text Archive/LLDS cho Barriffe 1635 (A04919)**
URL: https://llds.ling-phil.ox.ac.uk/llds/xmlui/handle/20.500.14106/A04919?show=full (curl, nguyên văn)
> "This keyboarded and encoded edition of the work described above is co-owned by the institutions providing financial support to the Early English Books Online Text Creation Partnership. This Phase I text is available for reuse, according to the terms of Creative Commons 0 1.0 Universal. The text can be copied, modified, distributed and performed, even for commercial purposes, all without asking permission."

**Bản ghi A50851 (1642)** — https://llds.ling-phil.ox.ac.uk/llds/xmlui/handle/20.500.14106/A50851?show=full
> "To the extent possible under law, the Text Creation Partnership has waived all copyright and related or neighboring rights to this keyboarded and encoded edition of the work described above, according to the terms of the CC0 1.0 Public Domain Dedication Creative Commons 0 1.0 Universal. This waiver does not extend to any page images or other supplementary files associated with this work, which may be protected by copyright or other license restrictions."

→ **Xác minh: EEBO-TCP Phase I là CC0 cho văn bản chép tay; CC0 KHÔNG bao gồm ảnh trang** (ảnh EEBO thuộc ProQuest). Hình khắc tư thế phải lấy từ bản quét khác (archive.org, thư viện), không lấy từ EEBO. Trang FAQ của TCP (https://textcreationpartnership.org/faq/ → https://www.textpartnership.net/faq/) **404**; trang Bodleian https://ota.bodleian.ox.ac.uk/repository/xmlui/handle/20.500.12024/5 **quá thời gian**. Nguồn thứ cấp (WebSearch) cho biết Phase I phát hành ngày 1/1/2015.

**archive.org — siêu dữ liệu (API https://archive.org/metadata/<id>, đọc 2026-10-18)**
- `the-manual-exercise-as-ordered-by-his-majesty-in-the-year-1764`: `licenseurl : https://creativecommons.org/publicdomain/zero/1.0/`; mô tả: "This is the manual used by the British army during American war for independence and by the American colonial militia and Continental army early in the war".
- `A303417`: `licenseurl : https://creativecommons.org/publicdomain/mark/1.0/`; `contributor : Biblioteca de la Universidad de Sevilla`; định dạng: "[2], 248 p., XVI h. de grab. pleg. ; 12º".
- `bub_gb_JQ7gfF99ZlIC`, `bub_gb_8dUCh4xp-F8C`: `licenseurl : http://creativecommons.org/publicdomain/mark/1.0/`.
- `ordenanzasdesmp01spaigoog`: `possible-copyright-status : NOT_IN_COPYRIGHT`; "Book digitized by Google from the library of the University of Michigan".
- Các mục `bim_*` (vi phim ECCO/EEBO, nhóm `bim_microfilm`): **không có trường rights/licenseurl**. Đánh giá: bản quét cơ học tác phẩm PD → theo luận cứ ở mục D (Mỹ: Bridgeman v. Corel; Anh: THJ v Sheridan 2023) không phát sinh quyền mới; tuy vậy ghi **"PD, điều khoản bản số hoá không ghi"** trong RIGHTS.md.

**Biblioteca Nacional de España / Biblioteca Digital Hispánica** — trang điều kiện tái sử dụng https://www.bne.es/es/servicios/reproduccion-documentos/condiciones-reutilizacion **BỊ CHẶN (403)**; đã đọc PDF https://www.bne.es/sites/default/files/repositorio-archivos/procedimiento_normas_reproduccion.pdf (curl + pdftotext, nguyên văn):
> "Las imágenes en dominio público que se encuentren en el sitio web bne.es/ y accesibles en los catálogos digitales de la BNE (Biblioteca Digital Hispánica y Hemeroteca Digital) están bajo una licencia de Reconocimiento 4.0 Internacional de Creative Commons o equivalente."
→ BDH: **CC BY 4.0 — OK, phải ghi "Biblioteca Nacional de España"**. Trong phiên này chưa tìm được bản BDH cụ thể của sách điều lệnh 1760–1780; dùng bản archive.org ở trên.

---

## D. Bộ sưu tập bảo tàng mở (tham chiếu trang phục/quân phục)

### D.1 Bảng phân loại

| Tổ chức | Điều khoản | Phân loại | Ghi chú |
|---|---|---|---|
| **Smithsonian Open Access** | CC0 cho mục gắn nhãn CC0 | **CC0** (chỉ mục gắn CC0) | Trang si.edu BỊ CHẶN 403; trích qua WebSearch |
| **Rijksmuseum** | PD hoặc CC0 trên phần lớn dữ liệu | **CC0 / PD** | Đã đọc trực tiếp |
| **The Met Open Access** | CC0 cho tác phẩm gắn biểu tượng CC0 | **CC0** (theo từng mục) | Trang chính sách 429; đã đọc README chính thức trên GitHub |
| **Royal Collection Trust** | Thương mại phải xin phép bằng văn bản | **BỊ HẠN CHẾ** | rct.uk 403; trích qua WebSearch |
| **National Army Museum (UK)** | CC BY-NC-ND hoặc NAM Non-Commercial Licence; thương mại qua Bridgeman/Mary Evans | **BỊ HẠN CHẾ (NC/ND)** | Đã đọc trực tiếp |
| **Anne S.K. Brown Military Collection (Brown)** | Nhãn quyền theo từng mục: "No Copyright - United States" (bản khắc TK18) hoặc "In Copyright" | **PD tại Mỹ, theo từng mục**; ngoài Mỹ chưa rõ | Đã đọc API BDR |
| **Victoria and Albert Museum** | Miễn phí chỉ phi thương mại; "Fees will apply for any commercial use" | **BỊ HẠN CHẾ** | Đã đọc trực tiếp |
| **London Museum (trước là Museum of London)** | Điều khoản cấm AI và cấm dùng thương mại dữ liệu cào | **BỊ HẠN CHẾ** | museumoflondon.org.uk chuyển sang londonmuseum.org.uk |
| **Europeana** | Theo từng mục (PDM, CC0, CC BY, In Copyright, NoC-NC…) | **Theo từng mục** | pro.europeana.eu 403; trích qua WebSearch |
| **Museo del Ejército / CER.es** | Không tìm thấy điều khoản | **KHÔNG RÕ → coi là hạn chế** | |
| **Wikimedia Commons (PD-Art)** | Ảnh trung thực của tác phẩm 2D thuộc PD là PD tại Mỹ; Anh: không phát sinh quyền mới (THJ v Sheridan 2023) | **PD, không hạn chế** cho tranh/bản khắc 2D; **không áp cho ảnh vật thể 3D** (quân phục, hiện vật) | Đã đọc trực tiếp |

### D.2 Trích dẫn nguyên văn

**Rijksmuseum** — https://data.rijksmuseum.nl/policy (chuyển hướng từ https://www.rijksmuseum.nl/en/research/conduct-research/data/policy; curl, nguyên văn)
> "According to our policy, much of the information and data on the Rijksmuseum's collection website and through our open data services can be freely used, including for commercial purposes, without needing to request permission."
> "For much of the information and data on the collection website, you will find a Public Domain or Creative Commons Zero (CC0) Public Domain Dedication under the copyright notice, meaning you can use the material freely This means that the material is either free of copyright, or the Rijksmuseum has waived its rights."

**The Met** — https://raw.githubusercontent.com/metmuseum/openaccess/master/README.md (curl, nguyên văn). Trang https://www.metmuseum.org/policies/image-resources trả **429**.
> "The Metropolitan Museum of Art provides select datasets of information on more than 470,000 artworks in its Collection for unrestricted commercial and noncommercial use. To the extent possible under law, The Metropolitan Museum of Art has waived all copyright and related or neighboring rights to this dataset using [Creative Commons Zero](https://creativecommons.org/publicdomain/zero/1.0/)."
> "Images are not included and are not part of the dataset. Companion artworks listed in the dataset covered by the policy are identified in the [Collection section](http://www.metmuseum.org/art/collection) of the Museum's website with the Creative Commons Zero (CC0) icon."

**Smithsonian** — https://www.si.edu/openaccess/faq, https://www.si.edu/openaccess, https://dashboard.si.edu/openaccess/faq: **BỊ CHẶN (403)**. Câu do WebSearch trả về từ FAQ si.edu (nguồn thứ cấp, cần đối chiếu):
> "Yes, you may use Smithsonian Open Access assets designated as CC0 for commercial purposes without any attribution, permission, or fee paid to the Smithsonian."
> "If the item is not designated CC0, you must still obtain prior written permission from the Smithsonian for commercial use."
> "… a third party may claim rights in the content such as trademark, privacy, or publicity rights."

**Royal Collection Trust** — https://www.rct.uk/about/website-terms-and-conditions và https://rct.uk/copyright: **BỊ CHẶN (403)**. Câu do WebSearch trả về từ rct.uk/copyright (nguồn thứ cấp):
> "Any commercial use of the images on this website is subject to written permission from Royal Collection Trust and the applicable Licence Terms and Conditions displayed on this site."

**National Army Museum** — https://nam.ac.uk/copyright (curl, nguyên văn)
> "We support and encourage public access by providing on our Online Collection low-resolution images of works for re-use under a non-commercial licence, where possible."
> "Material identified as copyright of the National Army Museum (© National Army Museum) may be reproduced free of charge under a Creative Commons Attribution Non-Commercial No Derivatives Licence (CC BY-NC-ND) where indicated."
> "The National Army Museum provides high-resolution images for commercial and other uses through the services of third parties, Bridgeman Images and the Mary Evans Picture Library ."

**Anne S.K. Brown (Brown Digital Repository)** — API https://repository.library.brown.edu/api/search/ và https://repository.library.brown.edu/api/items/bdr:233074/ (curl)
- Bản khắc TK18, ví dụ `bdr:230029` "Grenadier drummer and infantry officer" (1775), `bdr:242688` "Grenadier company and infantry musicians" (1760), `bdr:230027` (1775): `mods_access_condition_rights_text_tsim: ['No Copyright - United States']`.
- Catalogue triển lãm 1991 `bdr:233074`: `['In Copyright']`, `http://rightsstatements.org/vocab/InC/1.0/`.
Ghi chú: "No Copyright – United States" là nhãn RightsStatements.org, không phải giấy phép; tác phẩm gốc TK18 hiển nhiên PD; ảnh chụp phẳng → luận cứ PD-Art bên dưới.

**V&A** — https://www.vam.ac.uk/info/va-websites-terms-conditions (curl, nguyên văn)
> "'V&A Owned Content' in which the V&A owns copyright (or related rights) may be used free of charge for non-commercial purposes."
> "Fees will apply for any commercial use of Content, which includes but is not limited to the following: Content for use in publications with a print run of over 4,000 copies Content for broadcast, commercial website and digital use …"
> "For any commercial use, please contact our Image Licensing Team: <email-đã-che>"

**London Museum** — https://www.londonmuseum.org.uk/terms-of-use/ (curl, nguyên văn; https://www.museumoflondon.org.uk/terms-and-conditions chỉ còn trang khung)
> "Museum images, video and audio content: are strictly prohibited from being used externally for AI-based data scraping, data mining, or any form of automated algorithmic training."
> "Image licensees may not modify, adapt, or otherwise alter any licensed image in a way that generates AI-based derivative works or that contributes to an AI-generated work."
→ Rất quan trọng với pipeline dùng AI: **không dùng ảnh London Museum làm đầu vào**, kể cả cho hiện vật 1666.

**Europeana** — https://www.europeana.eu/en/rights và https://pro.europeana.eu/page/available-rights-statements: **BỊ CHẶN (403)**. Theo nguồn thứ cấp, Europeana dùng nhãn theo từng mục (PDM, CC0, CC BY, CC BY-SA, CC BY-NC…, "No Copyright – Non Commercial Use Only", "In Copyright") → chỉ lọc **PDM / CC0 / CC BY**.

**Museo del Ejército / CER.es** — WebSearch không tìm ra điều khoản tái sử dụng. → **KHÔNG RÕ**; phải hỏi bảo tàng.

**Wikimedia Commons — PD-Art** — https://commons.wikimedia.org/wiki/Commons:Reuse_of_PD-Art_photographs (curl, nguyên văn)
> "Wikimedia Commons explicitly permits the hosting of photographs that carefully reproduce a two-dimensional public domain work; such photographs are in the public domain in the United States, where this site is based"
> "Despite some intervening claims to contrary, a November 2023 Appeal Court judgement (THJ v Sheridan, 2023) clarified that, in the UK, no new copyright is created in making a photographic reproduction of a public domain artwork, and that this has been the case since 2009."
> "Note that there is also no issue regarding raw unenhanced scans or photocopies of PD illustrations in an old book. These are always OK, as purely mechanical copying has never been capable of creating a new copyright."

---

## E. Khuyến nghị

1. **Ước lượng tư thế:** chỉ dùng **MediaPipe Pose Landmarker (BlazePose GHUM 3D, Apache-2.0)** chạy CPU → 33 điểm 3D → retarget sang rig MPFB bằng script Blender riêng (copy rotation/IK theo hướng xương), **không qua SMPL**. Ưu: sạch giấy phép, chạy CPU, có z. Nhược: z chỉ đúng tương đối ("up to scale"), mỗi lần một người, tư liệu cũ mờ dễ rung. Rủi ro: cần làm mượt và khoá chân. Nếu cần 2D đám đông tốt hơn: rtmlib/RTMPose **chỉ sau khi** làm rõ giấy phép trọng số (body7, HumanArt) với OpenMMLab. **Loại:** OpenPose, Ultralytics YOLO (AGPL), SMPL/SMPL-X và mọi thứ cần SMPL (4DHumans, WHAM, TRAM, GVHMR), trọng số MotionBERT tải sẵn (Human3.6M).
2. **Mocap:** nền chính là **CMU** (đi, đứng, mang vác; được dùng trong sản phẩm bán, cấm bán lại dữ liệu) và **100STYLE (CC BY 4.0, ghi công)** để đám đông đi đa dạng; bổ sung **Quaternius UAL (CC0)**. Mixamo và Rokoko chỉ dùng sau khi chủ dự án lưu bản điều khoản gốc. **Loại:** Bandai Namco, LaFAN1, AMASS, HumanML3D, SFU, Motorica, KIT (chưa rõ), OpenGameArt CC-BY-SA/GPL.
3. **Điều lệnh:** Gibraltar phía Anh: Manual Exercise 1764 (bản archive.org gắn CC0) + Bland + Muller (pháo binh); **không dùng Dundas 1792** làm chuẩn cho 1779–83. Phía Tây Ban Nha: **Ordenanzas 1762 tomo II (A303417, PDM, 16 tờ khắc thao tác súng)** và Ordenanzas 1768 (PDM). London 1666: Barriffe, Hexham, Elton; văn bản EEBO-TCP là CC0 nhưng **ảnh trang EEBO thì không** → lấy hình từ bản quét archive.org.
4. **Trang phục:** ưu tiên **Rijksmuseum, The Met, Smithsonian (chỉ mục CC0)**, **Anne S.K. Brown (mục "No Copyright – United States", tranh khắc 2D)**, Wikimedia Commons PD-Art (chỉ tác phẩm 2D). **Không dùng** RCT, NAM, V&A, London Museum (cấm cả dùng cho AI), Museo del Ejército khi chưa có giấy phép.
5. Mỗi tài sản đã chọn phải vào `RIGHTS.md` với URL + ngày đọc ở trên; đối chiếu lại các trích dẫn "(qua WebFetch)" hoặc "nguồn thứ cấp" bằng trình duyệt trước khi khoá.

**Việc đang chờ chủ dự án:** (a) mở và lưu điều khoản Mixamo, Smithsonian, RCT, Europeana (các trang này chặn máy); (b) quyết định có hỏi OpenMMLab về giấy phép trọng số RTMPose hay không; (c) duyệt danh sách nguồn mocap CMU + 100STYLE + Quaternius.

## F. URL bị chặn / không đọc được
helpx.adobe.com Mixamo FAQ (403, cả bản /ca/) · si.edu/openaccess, /faq, dashboard.si.edu (403) · metmuseum.org/policies/image-resources (429) · rct.uk (403) · europeana.eu/en/rights, pro.europeana.eu (403) · bne.es condiciones-reutilizacion (403; đã dùng PDF thay) · textcreationpartnership.org/faq → textpartnership.net/faq (404) · ota.bodleian.ox.ac.uk (quá thời gian; đã dùng llds.ling-phil.ox.ac.uk thay) · motion-database.humanoids.kit.edu (trang JS) · nam.ac.uk/terms-conditions (404; đã dùng /copyright) · GitHub API (403 với phiên; đã dùng raw.githubusercontent.com).
