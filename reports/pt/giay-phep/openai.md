# OpenAI — giá, điều khoản quyền đầu ra, nguồn gốc nội dung (chép nguyên văn, phiên PT 17/10/2026)

Khoá API do proxy gắn cho api.openai.com; phiên không đọc/in/ghi khoá. `GET /v1/models` trả HTTP 200 (17/10/2026).

## 1. Bảng giá — https://developers.openai.com/api/docs/pricing (chuyển hướng từ platform.openai.com/docs/pricing), HTTP 200
SHA-256 HTML gốc: 71df235d640515eda4b1c34f16336397ac5407d9e9c1e81bd41bfdfdc107a028
```text
Image generation models
Prices per 1M tokens.
StandardBatch
 Standard
For image generation cost estimates, use the calculator in the image generation guide.
ModelModalityInputCached inputOutput
gpt-image-2.5-sunburstImage$8.00$2.00$30.00
Text$5.00$1.25-
gpt-image-2.5-flareImage$8.00$2.00$30.00
Text$5.00$1.25-
All models
Batch
For image generation cost estimates, use the calculator in the image generation guide.
ModelModalityInputCached inputOutput
gpt-image-2Image$4.00$1.00$15.00
Text$2.50$0.625-
gpt-image-2.5-sunburstImage$4.00$1.00$15.00
Text$2.50$0.625-
gpt-image-2.5-flareImage$4.00$1.00$15.00
Text$2.50$0.625-
All models
Transcription models
```

## 2. Hướng dẫn sinh ảnh — https://developers.openai.com/api/docs/guides/image-generation, HTTP 200
SHA-256 HTML gốc: a6a8b482515dea2a35702ae0e4abf9872d7ebf1dc9bbbf9197f0b2656557cd3d
```text
The API lets you generate and edit images from text prompts using gpt-image-2.5-sunburst and gpt-image-2.5-flare. Choose Sunburst for workflows where editing precision matters most, and Flare for fast, high-quality everyday image generation. You can access image generation capabilities through two APIs:
Image API
Size and quality options
gpt-image-2.5-sunburst and gpt-image-2.5-flare add xhigh and max quality settings. Both default to auto. Earlier GPT Image models support quality settings up to high.
Setting
Options
Recommended sizes
1024x1024 (square), 1536x1024 (landscape), 1024x1536 (portrait)
Quality
low, medium, high, xhigh, max, auto
Both models also support custom dimensions as WIDTHxHEIGHT strings, such as 1536x864. Width and height must be multiples of 16, the aspect ratio must be between 1:3 and 3:1, and neither edge may exceed 3840 pixels. The total pixel count must be between 655,360 and 8,294,400 (4K). Resolutions above 2560x1440 are experimental.
GPT Image 2.5 costs
Responses API requests include the mainline model’s token usage in addition to image generation costs.
Both GPT Image 2.5 models use the same token rates: $8 per million image input tokens, $2 per million cached image input tokens, $30 per million image output tokens, $5 per million text input tokens, and $1.25 per million cached text input tokens. See pricing.
Use the response’s usage to measure token consumption for your prompts, sizes, and quality settings. Equal token rates don’t mean equal cost per image: token consumption can differ by model and quality setting. For older-model pricing examples, see Earlier GPT Image models.
Cached input pricing
For GPT Image 2 and GPT Image 2.5, cached input pricing applies only to the image generation tool in the Responses API. It doesn’t apply to direct Images API requests, including /v1/images/edits.
Cached image generation inputs are reflected in billing, but their cached token counts aren’t included in the Responses API output. The response’s usage can’t verify these cache hits.
GPT Image 2.5 and GPT Image 2 output tokens
Select a model, quality, and size to estimate output tokens and image output cost.
For gpt-image-2.5-sunburst and gpt-image-2.5-flare, the quality options are low, medium, high, xhigh, and max.
For gpt-image-2, the options are low, medium, and high.
The models can use different token counts for the same quality setting and share the same price per image output token.
Use explicit quality and size values for this estimate; auto depends on the generated image.
ModelModelGPT Image 2.5 (Sunburst and Flare)
Quality
lowmediumhighxhighmax
WidthHeightOutput tokens
196
Estimated image output cost
$0.00588
Per image at 30 USD per million image output tokens. Excludes text and image input tokens and streaming partial images.
Partial images cost
```

## 3. Điều khoản quyền sở hữu đầu ra — OpenAI Services Agreement (PDF)
URL: https://cdn.openai.com/osa/openai-services-agreement.pdf · HTTP 200 · SHA-256 PDF: b93f17c5be5a4deadca42026195d361353619f49756ab74a7b356877cf7ab341 · trang HTML openai.com/policies/services-agreement trả 403 (Cloudflare) cho phiên. Chữ trích bằng pdftotext, không sửa:
```text
                                                  OpenAI Services Agreement
This OpenAI Services Agreement (“Agreement”) is entered as of the Effective Date between the organization agreeing to these
terms (“Customer”) and the OpenAI Contracting Party defined below (“OpenAI”). In this Agreement, OpenAI and Customer
are each referred to as a “Party” and collectively as the “Parties.” Capitalized terms not defined in the Agreement have the
meanings provided in the Order Form. Customer represents it is lawfully able to enter into this Agreement and, if it is entering
into the Agreement for an entity, that it has legal authority to bind that entity. By clicking “I agree,” accepting the Order Form,
or using the Services, Customer agrees to this Agreement.
4. Customer Content.
    4.1. Generally. Customer and Customer’s End Users may provide Input and receive Output. As between Customer and
         OpenAI, to the extent permitted by applicable law, Customer: (a) retains all ownership rights in Input; and (b) owns
         all Output. OpenAI hereby assigns to Customer all OpenAI’s right, title, and interest, if any, in and to Output.
    4.2. OpenAI Obligations. OpenAI will only use Customer Content as necessary to provide Customer with the Services,
         comply with applicable law, enforce the OpenAI Policies, and prevent abuse. OpenAI will not use Customer Content
         to develop or improve the Services, unless Customer explicitly agrees to such use.
    4.3. Customer Obligations. Customer is responsible for all Input and represents and warrants that it has all rights,
         licenses, and permissions required to provide Input to the Services. Customer is solely responsible for all use of the
         Outputs and for evaluating the accuracy and appropriateness of Output for Customer’s use case.
    4.4. Similarity of Output. Due to the nature of OpenAI’s Services and artificial intelligence generally, Output may not be
         unique, and other users may receive similar content from OpenAI’s services. Responses that are requested by and
         generated for other users are not considered Customer’s Output.
2:This OpenAI Services Agreement (“Agreement”) is entered as of the Effective Date between the organization agreeing to these
355:               will be effective on the date OpenAI posts the updated Agreement or OpenAI Policy. Customer’s continued use
387:      Administrators are Authorized Purchasers. Authorized Purchasers may be periodically updated by Customer in the
403:     “Effective Date” means the date this Agreement is entered into by the Parties, either by acceptance online, by signing an
433:      OpenAI Policies applicable to Customer are those in effect on the most recent effective date between either the
```

## 4. Nguồn gốc nội dung (C2PA, SynthID) — https://developers.openai.com/api/docs/guides/content-provenance, HTTP 200
SHA-256 HTML gốc: 88b4aeaf1734754fb8c6d8b34844c0da472b5d83017989d9954da9def33234c9
```text
 Use the Content Provenance API to check whether an image or audio file contains
supported OpenAI provenance signals. Send a file to
POST /v1/content_provenance_checks to receive the completed verification
results in the same response. Use these signals in content review,
fact-checking, labeling, and trust and safety workflows.
To check a file in your browser, use the web tool at
openai.com/verify.
For request parameters and response schemas, see the
Content provenance API reference.
To check text, apply for access.
Text verification is currently available only to approved organizations including
AI research and academic institutions. OpenAI reviews each application on a
case-by-case basis.
A not_detected result means the tool didn’t find supported signals in the
uploaded file. Content may still have been generated by OpenAI if its metadata
was stripped or shows evidence of tampering, its watermark was degraded, it
came from a legacy generation model, or it was created before provenance
signals were available. The tool doesn’t currently detect content generated by
another company’s AI model, so a not_detected result doesn’t rule that out
either.
What content provenance checks
Content provenance checks supported files for the following signals:
Signal
Applies to
What it checks
C2PA Content Credentials
Images
Signed metadata with issuer and AI-use details
SynthID
Images and audio
A watermark embedded directly in supported media
C2PA metadata provides more context about a file’s origin. Editing, converting,
or sharing a file can remove its metadata. A SynthID watermark is part of the
image or audio itself and may survive some transformations.
The API checks for supported OpenAI signals. It isn’t a general-purpose AI
detector and doesn’t identify content generated by every AI system. Visible
watermarks and labels are separate from the provenance signals checked by the
```
