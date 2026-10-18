# Giấy phép công cụ phục chế (đọc NGUYÊN VĂN 2026-10-18 UTC; tệp đầy đủ cạnh tệp này)

- `swin2sr-x2-README.md` ← https://huggingface.co/caidas/swin2SR-classical-sr-x2-64/raw/main/README.md · SHA-256 9186aaf5bf94b0adb71532ad70368320e8134815fa026827c8f0e4920dc6886c
- `swin2sr-code-LICENSE` ← https://raw.githubusercontent.com/mv-lab/swin2sr/main/LICENSE · SHA-256 d66ccc11682c7458b19b376e1335e8665cbe412ff71f554bfec25f1791cddfa0
- `realesrgan-LICENSE` ← https://raw.githubusercontent.com/xinntao/Real-ESRGAN/master/LICENSE · SHA-256 4a699ec4863d96a91fc265948a0c90033f7e8735d515524dcf3444736406e0c2
- `transformers-LICENSE` ← https://raw.githubusercontent.com/huggingface/transformers/main/LICENSE · SHA-256 77fd4710def9ec3c0f6225800e0235f15a425abd4a8b03559127fcd782612049

Trích nguyên văn:
- Swin2SR ×2 (thẻ mô hình HF, phần đầu YAML): `license: apache-2.0` ; API HF `"license":"apache-2.0"`.
- Swin2SR mã (README mv-lab/swin2sr): "This project is released under the Apache 2.0 license."
- Real-ESRGAN mã (LICENSE): "BSD 3-Clause License / Copyright (c) 2021, Xintao Wang". Trọng số RealESRGAN_x2plus.pth phát hành trong bản v0.2.1 của cùng kho; README không nêu giấy phép riêng cho trọng số → áp giấy phép kho (BSD-3).
- transformers (Apache-2.0) chỉ dùng để chạy Swin2SR.

Trọng số đã tải (ngoài git, /var/tmp/g6w/w):
- RealESRGAN_x2plus.pth ← https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth · SHA-256 49fafd45f8fd7aa8d31ab2a22d14d91b536c34494a5cfe31eb5d89c2fa266abb · 67061725 byte
- swin2sr-x2-model.safetensors ← https://huggingface.co/caidas/swin2SR-classical-sr-x2-64/resolve/main/model.safetensors · SHA-256 a515955815ab6dba3a9331d8c75db13a5166a5ffbcebf1a95ab676a5656ac4fb · 48460660 byte

RỦI RO ghi nhận (không phải điều khoản NC/SA/ND của công cụ): README Swin2SR: "We use mainly the DIV2K Dataset and Flickr2K datasets for training". Điều khoản DIV2K/Flickr2K (dữ liệu huấn luyện) không thuộc giấy phép trọng số; chưa có án lệ coi trọng số là tác phẩm phái sinh của dữ liệu. Real-ESRGAN x2plus cũng huấn luyện trên DIV2K/Flickr2K/OST (theo bài báo arXiv 2107.10833). Chủ dự án quyết định có chấp nhận rủi ro này không.

LOẠI theo Kinh thánh §12.3 (không dùng, không tải): CodeFormer, SUPIR, GFPGAN, Depth Pro, Depth Anything V2 Base/Large.
