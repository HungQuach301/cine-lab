# Giấy phép + tài liệu dùng trong PT2 (đọc 18/10/2026; chép nguyên văn)

## 1. OpenAI — hướng dẫn sinh/sửa ảnh (https://developers.openai.com/api/docs/guides/image-generation, HTTP 200, SHA-256 HTML `fba2a67a84435d32b57f6be4e6dade64237cd1333784b1c0bce9fa029d5fdd92`)
Model hiện hành: `GET /v1/models` (200) liệt kê `gpt-image-2.5-sunburst`, `gpt-image-2.5-flare` (+ bản ghim `-2026-09-08`), `gpt-image-2`, `gpt-image-1.5`… Tài liệu:
```text
The API lets you generate and edit images from text prompts using gpt-image-2.5-sunburst and gpt-image-2.5-flare. Choose Sunburst for workflows where editing precision matters most, and Flare for fast, high-quality everyday image generation. You can access image generation capabilities through two APIs:
```
Mặt nạ (lý do bắt buộc ghép lại lớp A — HC2):
```text
Edit an image using a mask
You can provide a mask to indicate which part of the image should be edited.
When using a mask with GPT Image, additional instructions are sent to the model to help guide the editing process accordingly.
Masking with GPT Image is entirely prompt-based. The model uses the mask as
guidance, but may not follow its exact shape with complete precision.
If you provide multiple input images, the mask will be applied to the first image.
Mask requirements
The image to edit and mask must be of the same format and size (less than 50MB in size).
The mask image must also contain an alpha channel. If you’re using an image editing tool to create the mask, make sure to save the mask with an alpha channel.
You can modify a black and white image programmatically to add an alpha channel.
```
Giá:
```text
Both GPT Image 2.5 models use the same token rates: $8 per million image input tokens, $2 per million cached image input tokens, $30 per million image output tokens, $5 per million text input tokens, and $1.25 per million cached text input tokens. See pricing.
```
Quy ước mặt nạ dùng: PNG RGBA cùng cỡ, cùng định dạng (PNG) với ảnh gửi; alpha 0 = được sửa, alpha 255 = giữ (theo ví dụ "use the mask itself to fill that alpha channel").
Điều khoản quyền đầu ra, C2PA, SynthID: như `reports/pt/giay-phep/openai.md` §3–§4 (không đổi). Chính sách công bố AI của YouTube: `reports/pt/giay-phep/youtube-disclosing-genai.txt`.

## 2. MakeHuman / MPFB2 — lưới người CC0 (đã có dòng RIGHTS W4-MPFB-A, -A2, -A3)
Repo `https://github.com/makehumancommunity/mpfb2.git` commit `3edf9df0551765be43563d047888cf7877eb89b4` (cùng commit RIGHTS). SHA khớp RIGHTS: `base.obj` 8e761e66…6fb4c,
`rig.default.json` 8b949de3…7be6797, `weights.default.json` 154b8667…24e89; `LICENSE.md` 5cefb606…ce04d; `LICENSE.ASSETS.md` f6089cba…6d2c.
Dùng: `3dobjs/base.obj` (gồm nhóm `helper-tights`, `helper-skirt` của chính lưới gốc), `targets/macrodetails/**` (universal male/female young, caucasian, height),
`rigs/standard/rig.default.json` + `weights.default.json`. **Không chạy mã addon MPFB** (bộ phân loại an toàn của phiên chặn chạy mã ngoài) — PT2 tự viết bộ nạp
(`design/pt/lai/mh_people.py`). Không dùng da/texture/quần áo MPFB; trang phục do PT2 tô vùng + khối cơ bản.
```text
C. The license for the bundled assets
-------------------------------------

The assets are defined as any data contributing to the output from MPFB.
This includes:

* The base mesh and proxies
* Targets and modifiers
* Textures
* Clothes (any MHCLO-based asset)
* Rigs, poses and expressions
* JSON data with mesh information

These assets have been released under CC0 1.0 Universal. In summary this means
that to the fullest extent possible, it is the intention of the MakeHuman 
team that anyone can do whatever they want with it.

For the full text of the legal statement regarding the assets, see
[LICENSE.ASSETS.md](LICENSE.ASSETS.md)

D. Concerning the output from MPFB
----------------------------------

It is the opinion of the MakeHuman team that no output from MPFB
contains any trace of program logic. That is, regardless of whether you use
the UI as such or if you call functions of MPFB via a script (such as 
an addon that extends MPFB), what you get is a combination of assets and your
own creative input. As the assets have been released under CC0, there is no
limitation on what you can do with this combined output.
```
→ Phạm vi PT2 nằm trong W4-MPFB-A/A3 (lưới gốc + targets + rig/weights), mở rộng mục đích sang **người đám đông khung neo** → đề nghị P ghi dòng mở rộng phạm vi (W4-MPFB-A5).

## 3. Vân vật liệu nền A
Không đổi so với PT: 9 vân Poly Haven CC0 (bảng `reports/pt/giay-phep/README.md`), tải lại 18/10, SHA-256 27/27 tệp khớp `polyhaven-files.json`.
