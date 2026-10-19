# Giấy phép và điều khoản ElevenLabs cho casting giọng

**Tài liệu ElevenLabs đọc ngày 18/10/2026 — trích nguyên văn.**

Phương pháp: tải trực tiếp bản Markdown chính thức của tài liệu (`https://elevenlabs.io/docs/....md`, theo chỉ mục `https://elevenlabs.io/docs/llms.txt`) và trang pháp lý HTML (chuyển sang văn bản thô), rồi chép nguyên văn. Không gọi `api.elevenlabs.io`, không đọc khoá API. Mọi trích dẫn bên dưới là tiếng Anh nguyên văn; phần tiếng Việt là diễn giải của phiên nghiên cứu. Ngày truy cập của mọi URL: **2026-10-18**.

Lưu ý quan trọng ngay đầu: tài liệu hiện hành có **Eleven v4** (`eleven_v4`) làm mô hình chủ lực; Eleven v3 nay được gọi là "previous generation". Giọng **Default** sẽ **hết hạn 31/12/2026**.

---

## 1. Voice Design (text-to-voice)

### 1.1 Quy trình API: hai bước, design rồi create

URL: https://elevenlabs.io/docs/eleven-api/guides/how-to/voices/voice-design.md (2026-10-18)

> Designing a voice via a prompt has two steps:
>
> 1. Generate previews based on a prompt.
> 2. Select the best preview and use it to create a new voice.

URL: https://elevenlabs.io/docs/api-reference/text-to-voice/design.md (2026-10-18)

> POST https://api.elevenlabs.io/v1/text-to-voice/design

> Design a voice via a prompt. This method returns a list of voice previews. Each preview has a generated_voice_id and a sample of the voice as base64 encoded mp3 audio. To create a voice use the generated_voice_id of the preferred preview with the /v1/text-to-voice endpoint.

> - `model_id` (enum, optional, default: eleven_multilingual_ttv_v2) — Model to use for the voice generation. Possible values: eleven_multilingual_ttv_v2, eleven_ttv_v3.

> - `text` (string, optional, nullable) — Text to generate, text length has to be between 100 and 1000.

> - `seed` (integer, optional, nullable) — Random number that controls the voice generation. Same seed with same inputs produces same voice.

> - `guidance_scale` (double, optional, default: 5) — Controls how closely the AI follows the prompt. Lower numbers give the AI more freedom to be creative, while higher numbers force it to stick more to the prompt. High numbers can cause voice to sound artificial or robotic. We recommend to use longer, more detailed prompts at lower Guidance Scale.

> - `reference_audio_base64` (string, optional, nullable) — Reference audio to use for the voice generation. The audio should be base64 encoded. Only supported when using the eleven_ttv_v3 model.

URL: https://elevenlabs.io/docs/api-reference/text-to-voice/create.md (2026-10-18)

> POST https://api.elevenlabs.io/v1/text-to-voice

> Create a voice from previously generated voice preview. This endpoint should be called after you fetched a generated_voice_id using POST /v1/text-to-voice/design or POST /v1/text-to-voice/:voice_id/remix.

### 1.2 Mô hình và số preview

URL: https://elevenlabs.io/docs/overview/models.md (2026-10-18)

> | `eleven_ttv_v3`              | Human-like and expressive voice design model (Text to Voice)

> | `eleven_multilingual_ttv_v2` | State-of-the-art multilingual voice designer model (Text to Voice)

URL: https://elevenlabs.io/docs/overview/capabilities/voices.md (2026-10-18)

> Voice Design creates 3 voice previews. You just need to provide:
>
> * A **voice description** between 20 and 1000 characters.
> * Optional **text** to preview the voice, between 100 and 1000 characters.

> [Eleven v4](/docs/overview/capabilities/text-to-speech/eleven-v4) is the model to use. Voice Design voices work with it, though they may be less performative than with earlier models. Eleven v3 can also design voices that cover a wide emotional range.

URL: https://elevenlabs.io/docs/help-center/product/voices/voice-design/what-is-voice-design.md (2026-10-18)

> Voices created with Voice Design work with [Eleven v4](/docs/overview/capabilities/text-to-speech/eleven-v4), our latest model, and with earlier models including Eleven v3. They support audio tags. On Eleven v4 they may be less performative than on earlier models.

> **Note:** Voice Design is still experimental. Professional Voice Clones offer the
> highest quality and consistency. If you find a PVC that fits your needs, we recommend using it.

### 1.3 Chi phí

URL: https://elevenlabs.io/docs/eleven-creative/voices/voice-design.md (2026-10-18)

> When you hit generate, we'll generate three voice options for you. The only charge for using voice design is the number of credits to generate your preview text, which you are only charged once even though we are generating three samples for you. You can see the number of characters that will be deducted in the "Text to preview" text box.

> After generating, you'll have the option to select and save one of the generations, which will take up one of your voice slots.

URL: https://elevenlabs.io/docs/help-center/product/voices/voice-design/how-much-does-voice-design-cost.md (2026-10-18)

> Voice Design only consumes credits when you generate voices.
>
> Each time you click **Generate voice**, we create three voice options based on your prompt. You're charged based on the number of characters in your preview text.

Đơn giá credit/ký tự riêng cho `eleven_ttv_v3` so với `eleven_multilingual_ttv_v2`: **CHƯA XÁC MINH** (không trang nào nêu). Tài liệu cũng không nói rõ việc gọi `POST /v1/text-to-voice` (lưu giọng) có tốn credit hay không: **CHƯA XÁC MINH** (tài liệu chỉ nói "only charge ... is ... preview text").

### 1.4 Quyền sở hữu, chia sẻ, xoá giọng thiết kế

URL: https://elevenlabs.io/docs/help-center/product/voices/my-voices/who-has-access-to-my-voices.md (2026-10-18)

> Unless you explicitly share a voice, the voices you’ve created are **only accessible through your account.**

> Instant Voice Clones and voices created with [Voice Design](/docs/product-guides/voices/voice-design) can only be shared with members of your workspace. They cannot be shared outside your workspace or published to the Voice Library.

URL: https://elevenlabs.io/docs/help-center/product/voices/voice-library/can-i-share-an-ai-generated-voice-in-the-voice-library.md (2026-10-18)

> No. We only allow the sharing of professional cloned voices verified by a human. Instant Voice Clones, synthetic voices created using [Voice Design](/docs/product/voices/voice-lab/voice-design), AI-generated or AI-enhanced voices cannot be shared in the Voice Library.

URL: https://elevenlabs.io/docs/overview/capabilities/voices.md (2026-10-18)

> Voice Remixing works with any cloned voice you personally own (Instant Voice Cloning or Professional Voice Cloning) or voices created through Voice Design.

URL: https://elevenlabs.io/docs/help-center/product/voices/my-voices/how-do-i-delete-voices-from-my-voices.md (2026-10-18)

> Deleting a voice cannot be undone, and you will be asked to confirm the deletion.

Điều khoản (ToS non-EEA) — URL: https://elevenlabs.io/terms-of-use (2026-10-18; `https://elevenlabs.io/terms` chuyển hướng về đây), "Last Updated: 09 October 2026":

> (b) User Voice Models. Some of our Services allow you to create a voice model that can be used to generate Output in the form of synthetic audio sounding like your voice or a voice you are authorized to share with us (a "User Voice Model"). [...] You may request deletion of your User Voice Models created with your Input recordings through your account.

> (ii) For the avoidance of doubt, Output may be generated by, but does not include, ElevenLabs’ foundational and other artificial intelligence voice models (the “Voice Models”) or ElevenLabs’ foundational and other artificial intelligence or language learning models (“LLMs”) (Voice Models and LLMs, collectively, the “Models”). Except as expressly set forth herein, as between you and ElevenLabs, you retain all rights in and to your Output.

> (e) License to User Voice Models. To the extent you own or acquire any intellectual property rights in or to any User Voice Models, you hereby grant to ElevenLabs a license to use, reproduce, modify, adapt, publish, translate, create derivative works from, distribute, publicly or otherwise perform and display, and use the User Voice Models to provide the Services (including the trust and safety features therein) to you, to improve the Services, and to develop new services and products. Such license shall be:
> perpetual and irrevocable (which means this license cannot be withdrawn),
> nonexclusive (which means you can license your Input to others),
> [...]
> sub-licensable, through multiple tiers (which means we can make it available to others).

**Ý nghĩa cho dự án:** Voice Design = 1 lệnh `design` (3 preview, trả credit theo số ký tự preview text, 100–1000 ký tự, chỉ trả một lần) + 1 lệnh `create` (chiếm 1 voice slot). Giọng thiết kế chỉ tài khoản/workspace của mình dùng được và có thể xoá. **Quyền sở hữu pháp lý đối với "giọng thiết kế" (voice model) CHƯA XÁC MINH**: ToS chỉ nói rõ ta giữ quyền với *Output* (audio); định nghĩa "User Voice Model" nói về giọng của chính mình/giọng được uỷ quyền, không nhắc Voice Design; trang docs chỉ gián tiếp dùng chữ "own". Thêm rủi ro: Voice Design được gọi là **"still experimental"** — chưa thấy văn bản nào xếp nó vào "Beta Services" (xem mục 5.4), nhưng nên hỏi ElevenLabs (legal@) bằng văn bản trước khi dùng cho phim bán.

---

## 2. Voice Library (giọng cộng đồng)

### 2.1 Bản chất và điều kiện dùng

URL: https://elevenlabs.io/docs/eleven-creative/voices/voice-library.md (2026-10-18)

> The [Voice Library](https://elevenlabs.io/app/voice-library) is a marketplace where our community can share Professional Voice Clones and earn rewards when others use them. Currently, only Professional Voice Clones can be shared. Instant Voice Clones and voices created with Voice Design are not shareable.

> Voice Library voices are not available via the API to free tier users.

URL: https://elevenlabs.io/docs/help-center/product/voices/voice-library/why-cant-i-use-some-voices-from-the-voice-library.md (2026-10-18)

> Some voices in the Voice Library are only available to users with a paid subscription. This is either because the voice’s owner has chosen to restrict usage, or the voice has a credit multiplier in place.

Voice Library Addendum — URL: https://elevenlabs.io/vla (2026-10-18), "Last Updated 6 March 2026". (Thử `https://elevenlabs.io/voice-library-terms` → **HTTP 404**; trang đúng là `/vla`, được docs dẫn tới.)

> The Voice Library Service makes available ElevenLabs Voice Models, provided by ElevenLabs, as well as User Voice Models, provided by ElevenLabs users, including you, through the Services. [...] We may charge fees for the access and use of these User Voice Models as set forth in this Addendum and through the Services.
>
> The rights in and to ElevenLabs Voice Models and User Voice Models, including those made available as part of the Voice Library Service, are set out in our Terms of Service.

> You may share User Voice Models you’ve generated on our platform through the Voice Library Service. If you chose to do so, you hereby authorize us to make available the User Voice Models for others to access and use through the Voice Library Service in accordance with the Terms of Service and this Voice Library Addendum (“Voice Library License”). For clarity, others may be able to generate Output with the User Voice Models you have shared in our Library.

### 2.2 Gỡ giọng và thời hạn báo trước (notice period) — nguyên văn

VLA (https://elevenlabs.io/vla, 2026-10-18):

> Notice Period: When you share your User Voice Model in the Voice Library, you will be asked to specify a “Notice Period.” You may choose to remove a User Voice Model you shared through the Voice Library Service at any time. However, (a) any Outputs generated using your User Voice Model prior to the end of the Notice Period will continue to exist and remain available for use thereafter, and (b) the User Voice Model will remain accessible for the duration of the Notice Period to users that added that User Voice Model to their account prior to removal of the User Voice Model from the Voice Library Service. For instance, if you select a Notice Period of 30 days, it means that the User Voice Model will be available for 30 days in other users’ accounts starting from the date on which you decide to remove the User Voice Model. This is to ensure that users who have added your User Voice Model to their account have enough time to migrate to a different User Voice Model. [...] Once you share your User Voice Model in the Voice Library, you will not be able to reduce your Notice Period, but you will be able to increase it.

> To the fullest extent permitted by applicable law, we reserve the right to review and remove any User Voice Model made available in the Voice Library in our sole discretion, and at any point in time, with or without notice to you, including as indicated in the Terms of Service.

URL: https://elevenlabs.io/docs/help-center/product/voices/voice-library/what-is-a-notice-period.md (2026-10-18)

> When a voice actor shares their voice to the Voice Library, they can set a notice period. If no notice period is set, their voice will be removed immediately if they decide to stop sharing it, and anyone who has saved the voice will immediately lose access.
>
> The minimum notice period is 30 days, and the maximum is 2 years. Voice owners receive increased financial rewards for selecting a longer notice period.

> For API users, you can see this when fetching the voice using the [Get Voice endpoint](/docs/api-reference/voices/get) by looking for `disable_at_unix` in the response. If the voice has not had its notice period active, this key will not exist or it will say `null`.

URL: https://elevenlabs.io/docs/eleven-creative/voices/voice-library.md (2026-10-18)

> You can use voices from the Voice Library directly without saving them to My Voices. When you use a voice, the notice period will be saved for your account, allowing you to continue using voices you've used previously during an active notice period, even if you haven't saved them to My Voices.

URL: https://elevenlabs.io/docs/help-center/product/voices/my-voices/how-do-i-delete-voices-from-my-voices.md (2026-10-18)

> If you remove a voice that has been removed from the Voice Library, you will not be able to save it to [My Voices](https://elevenlabs.io/app/voice-lab) again in the future.

### 2.3 Live Moderation, giọng có hệ số credit, payout

URL: https://elevenlabs.io/docs/help-center/product/voices/voice-library/what-is-live-moderation.md (2026-10-18)

> When users choose to share their Professional Voice Clone with the Voice Library, they can enable Live Moderation.  When this is enabled, we use tools to check whether requests to use that voice contain text that belongs to a number of prohibited categories.
>
> Please note that using a voice model with Live Moderation enabled may result in extra latency.

URL: https://elevenlabs.io/docs/help-center/product/voices/voice-library/what-are-custom-rates-and-credit-multipliers.md (2026-10-18)

> Some voices in the Voice Library have a credit multiplier in place. This is because the voice's owner set a custom rate for financial rewards when they shared their Professional Voice Clone with the Voice Library. Custom rates are a legacy feature that is no longer available for newly shared voices.

> The credit multiplier that applies for generating audio is based on the custom rate chosen by the voice owner as well as the subscription plan of the user of the voice.

URL: https://elevenlabs.io/docs/help-center/product/voices/voice-library/why-cant-i-use-some-voices-from-the-voice-library.md (2026-10-18)

> For example, if a voice has a 2x multiplier, generating audio will cost twice as many credits as a voice on the standard rate.

URL: https://elevenlabs.io/docs/help-center/product/monetization-business/payouts/what-are-voice-actor-payouts.md (2026-10-18)

> Voice Actor Payouts let you earn cash rewards when paid users generate audio with your Professional Voice Clone shared in the Voice Library. Earnings are calculated based on usage by paid users and exclude use by free users. Your default rate is determined by your selected notice period, and payouts are processed automatically through Stripe.

Cờ "not for commercial use" riêng trên từng giọng Library: **CHƯA XÁC MINH** — không tìm thấy trong tài liệu hiện hành; chỉ thấy hạn chế "paid subscription only"/"Exclude free users", Live Moderation và credit multiplier.

**Ý nghĩa cho dự án:** Audio đã render bằng giọng Library **vẫn dùng được vĩnh viễn** sau khi chủ gỡ ("continue to exist and remain available for use thereafter"). Nhưng nếu cần render lại (sửa thoại, phim đích 10–15 phút), ta chỉ có thời hạn báo trước 30 ngày–2 năm, hoặc **mất ngay** nếu giọng không đặt notice period; ElevenLabs cũng có thể gỡ "with or without notice". Nếu dùng giọng Library phải lọc giọng có notice period dài, không multiplier, theo dõi `disable_at_unix`, và lưu WAV gốc mọi dòng thoại.

---

## 3. Giọng Default/premade (Eric, Brian, George, Bill, Daniel…)

URL: https://elevenlabs.io/docs/help-center/product/voices/my-voices/what-are-default-voices.md (2026-10-18)

> Our Default voices are being replaced with new voices that you will be able to use forever. All our Default voices will expire on December 31, 2026, and they will no longer be accessible after this date. As part of this process, Default voices are only available for accounts that were created before March 2026.

> This table has suggested replacements for our Default voices. While we have aimed to provide similar voice types, this is not a strict 1-to-1 replacement, and tone and style may differ. We recommend testing the new voices to identify the best fit for your use case ahead of December 31, 2026.

Trích bảng thay thế (nguyên văn, bỏ link):

> | George | Eldrin - Crisp British Baritone |
> | Eric | Eddie - Helpful and Comforting |
> | Brian | Sawyer - Midnight Storyteller |
> | Daniel | Finley - Articulate Anchor |
> | Bill | Wyatt - Seasoned Mentor |

URL: https://elevenlabs.io/docs/overview/capabilities/voices.md (2026-10-18)

> Our Default voices are being replaced with new voices that you will be able to use in perpetuity.
> All our Default voices will expire on December 31, 2026, and they will no longer be accessible
> after this date.

URL: https://elevenlabs.io/docs/help-center/product/voices/my-voices/what-are-legacy-voices.md (2026-10-18)

> Legacy voices are former Default voices that do not meet our current quality standard. They have been fully deprecated and removed from all products.

> If you use the API, Legacy voice IDs will automatically route to their replacement voice IDs.

Điều khoản thương mại riêng cho giọng Default: **CHƯA XÁC MINH** (không có văn bản riêng). Văn bản gần nhất là VLA: "The rights in and to ElevenLabs Voice Models ... are set out in our Terms of Service" — tức áp dụng quy tắc chung mục 4 (gói trả phí = được dùng thương mại).

**Ý nghĩa cho dự án:** **Không chọn Eric/Brian/George/Bill/Daniel cho phim.** Chúng hết hạn 31/12/2026 (chưa đầy 2,5 tháng nữa) và chỉ tài khoản tạo trước 03/2026 thấy được; mọi lần render lại sau đó phải đổi giọng, phá tính liền mạch. Nếu thích chất giọng nào, nghe bản thay thế (Sawyer, Finley, Eldrin, Wyatt, Eddie) — bản thay thế "use forever / in perpetuity".

---

## 4. Sử dụng thương mại nói chung

ToS (https://elevenlabs.io/terms-of-use, 2026-10-18), mục 3(c):

> (i) if you access or use our Services free of charge (such a user, a “Free User”), you may only use the Services for non-commercial purposes; (ii) if you access or use our Services through a paid subscription plan (such a user, a “Paid User”), you may use the Services for commercial purposes, but in either case, your access and use of the Services and any Output must still comply with the Prohibited Use Policy.

ToS mục 4(c)(ii): xem trích ở 1.4 — "you retain all rights in and to your Output".

URL: https://elevenlabs.io/docs/help-center/legal/can-i-publish-the-content-i-generate-on-the-platform.md (2026-10-18)

> The free plan does **not** include a commercial license and cannot be used for any commercial purpose. If you publish content generated using our Services on a free plan or without being signed-in to your account, you must attribute it to ElevenLabs by including "elevenlabs.io" or "11.ai" in the title [...]

> All paid plans include a commercial license, provided you're not using Beta Services. As long as you hold the necessary intellectual property rights to your generated content, and it complies with applicable laws, our [Terms of Service](https://elevenlabs.io/terms) and [Prohibited Use Policy](https://elevenlabs.io/use-policy), you may use it commercially.

> * Content generated during a paid subscription can be used commercially, and indefinitely, subject to our [Service-Specific Terms](https://elevenlabs.io/service-specific-terms). Attribution requirement is subject to the agreement you have with ElevenLabs.
> * Content created outside of a paid subscription (before or after) cannot be used commercially and always requires attribution when shared non-commercially.
> * Under our [Beta Services Addendum](https://elevenlabs.io/bsa), content generated using Beta Services cannot be used for any commercial purpose or in any production environment.

Bảng giá — URL: https://elevenlabs.io/pricing (2026-10-18), gói Starter:

> Starter [...] Everything in free, plus
> Commercial License

(Giá hiển thị hôm nay có khuyến mãi "Until Oct 18"; không trích giá vì đổi theo ngày. Gói Pro ghi "44.1kHz PCM audio output via API".)

ElevenCreative Terms — URL: https://elevenlabs.io/creative-terms (2026-10-18), "Last updated: 09 October 2026". Lưu ý: điều khoản sau thuộc **Exhibit 4: Sound Effects** (không phải giọng nói):

> You may exercise those rights only in respect of Output combined with other material, and you may not sell, resell, license, sublicense, distribute, or otherwise commercially exploit Output, or any part of it, on a standalone basis, or make Output available as isolated audio files or samples, or as part of any sound, sample, effects, or music library or other collection of sounds.

Và **Exhibit 1: Dubbing**:

> Unless expressly authorized in an Order Form or other written agreement executed by ElevenLabs, you shall not use, or permit any third party to use, Dubbing v2 Output in connection with: (a) feature films; [...]

YouTube — URL: https://elevenlabs.io/docs/help-center/legal/audio-detector/will-watermarks-cause-my-content-to-be-flagged-downranked-or-demonetized-on-you-tube-or-other-platforms.md (2026-10-18)

> No other platforms can currently detect ElevenLabs watermarks. Our watermarking is focused on public AI transparency — giving people the ability to verify whether audio is AI-generated — and is not connected to other platforms’ monetization or content policies.

Văn bản nêu đích danh "bán phim" hay "YouTube monetization được phép": **CHƯA XÁC MINH** ở dạng nêu tên; được bao bởi giấy phép thương mại chung của gói trả phí.

**Ý nghĩa cho dự án:** Phải render **toàn bộ** thoại trong thời gian có gói trả phí (Starter trở lên); audio tạo trên gói Free — kể cả trước khi nâng cấp — không được dùng thương mại. Gói trả phí không bắt ghi công ElevenLabs. Nếu dùng SFX của ElevenLabs thì chỉ trong phim (không bán rời); không dùng Dubbing v2 cho phim khi chưa có hợp đồng.

---

## 5. Mô hình TTS hiện hành

### 5.1 Danh sách

URL: https://elevenlabs.io/docs/overview/models.md (2026-10-18)

> | `eleven_v4`                  | Our most emotionally rich, expressive speech synthesis model
> | `eleven_v4_turbo`            | Our most expressive, real-time speech synthesis model (\~100ms†)
> | `eleven_v3`                  | Human-like and expressive speech generation
> | `eleven_v3_conversational`   | Our most expressive, realtime speech synthesis model (\~280ms†)
> | `eleven_multilingual_v2`     | Our lifelike model with rich emotional expression
> | `eleven_flash_v2_5`          | Ultra-fast model optimized for real-time use (\~75ms†)
> | `eleven_flash_v2`            | Ultra-fast model optimized for real-time use (\~75ms†)

> The `eleven_turbo_v2_5` and `eleven_turbo_v2` models are functionally equivalent to the
> `eleven_flash_v2_5` and `eleven_flash_v2` models respectively, except the latency on the Flash
> models is lower on average. We recommend using the Flash models over Turbo models in all use
> cases.

> Eleven v3 is our previous generation speech synthesis model [...]

> Eleven Multilingual v2 is a previous generation emotionally-aware speech synthesis model.

### 5.2 Khuyến nghị cho tường thuật dài (long-form)

URL: https://elevenlabs.io/docs/overview/models.md (2026-10-18)

> Eleven v4 is our state of the art speech synthesis model, delivering our highest quality audio, expressiveness, and control over how voices are performed. Eleven v4 supports high-fidelity voice cloning with reliable speaker preservation across long text generations.

> * **Audiobook Production**: Perfect for long-form narration with complex emotional delivery.

> #### Eleven Multilingual v2
> Lifelike, consistent quality speech synthesis model
> [...]
> Most stable on long-form generations

> #### Content creation
>
> Use `eleven_v4` or `eleven_multilingual_v2`
>
> Ideal for professional content, audiobooks & video narration.

URL: https://elevenlabs.io/docs/eleven-api/choosing-the-right-model.md (2026-10-18)

> #### Content creation
>
> Use `eleven_v4`
>
> Ideal for professional content, audiobooks, and video narration.

URL: https://elevenlabs.io/docs/overview/capabilities/text-to-speech/eleven-v4.md (2026-10-18)

> Both variants use two voice settings: Stability and Similarity.

> Style and Speed sliders are not available in Eleven v4, and SSML is not supported.

> > Professional Voice Clone support for Eleven v4 is currently rolling out to everyone and should be
> > available within the next few days.

> We're still experimenting with Eleven v4 to understand how best to use it.

### 5.3 Giới hạn ký tự và chi phí

URL: https://elevenlabs.io/docs/overview/models.md (2026-10-18)

> | `eleven_v4`              | 10,000          | \~10 minutes               |
> | `eleven_v3`              | 5,000           | \~5 minutes                |
> | `eleven_flash_v2_5`      | 40,000          | \~40 minutes               |
> | `eleven_flash_v2`        | 30,000          | \~30 minutes               |
> | `eleven_multilingual_v2` | 10,000          | \~10 minutes               |

URL: https://elevenlabs.io/docs/help-center/technical/what-models-do-you-offer-and-what-is-the-difference-between-them.md (2026-10-18) — câu sau lặp nguyên văn cho Eleven v4, Multilingual v2, Flash v2.5, Flash v2, Turbo v2.5, Turbo v2:

> For UI generations, 1 character costs 1 credit, excluding credit multipliers. API generations are discounted - for details, see our [API Pricing.](https://elevenlabs.io/pricing)

URL: https://elevenlabs.io/docs/help-center/product/core-capabilities/text-to-speech/how-much-does-it-cost-to-generate-using-eleven-v3-alpha.md (2026-10-18)

> The cost of generating with Eleven v3 is 1 credit per character on the website. API generations are discounted - see [API pricing](https://elevenlabs.io/pricing/api) for details.

Bảng giá API — URL: https://elevenlabs.io/pricing/api (2026-10-18), trích văn bản trang:

> v4 [...] Text to Speech
> $0.08
> Price per 1K characters

> v4 Turbo [...] $0.04
> Price per 1K characters

> v3 [...] $0.08
> Price per 1K characters

> v3 Conversational [...] $0.04
> Price per 1K characters

> v2 Multilingual [...] $0.08
> Price per 1K characters [...]
> Lifelike, consistent quality for long-form audio

> Flash / Turbo [...] $0.04
> Price per 1K characters

Hệ số quy đổi "credit API per ký tự" theo từng model (ví dụ Flash = 0,5 credit/ký tự qua API): **CHƯA XÁC MINH** — docs chỉ ghi "API generations are discounted" và models.md ghi "Faster model, 50% lower price per character for API generations" cho Flash v2.5.

### 5.4 Trạng thái alpha/beta và Beta Services Addendum

Trong models.md và các trang help hiện hành **không** còn mô hình TTS nào gắn nhãn "alpha", "beta" hay "research preview" (slug URL của trang v3 vẫn chứa "alpha" nhưng nội dung đã bỏ nhãn). Voice Design được gọi là "still experimental" (xem 1.2).

Beta Services Addendum — URL: https://elevenlabs.io/bsa (2026-10-18), "Updated 13 November 2024":

> From time to time, ElevenLabs may make available services or functionality to you that are not generally made available to ElevenLabs customers and/or are designated as alpha, beta, pilot, preview, or similar designation (“Beta Services”).

> You agree not to (and agree not to permit any third party to): (a) use the Beta Services for any commercial purposes or in any production environment;

**Ý nghĩa cho dự án:** Mô hình nên chọn cho phim là **`eleven_v4`** (docs khuyến nghị cho audiobook/narration, 10.000 ký tự/lệnh, $0,08/1K ký tự API, 1 credit/ký tự UI); `eleven_multilingual_v2` là phương án dự phòng "most stable on long-form", cùng giá. v4 không có Style/Speed, không SSML (không `<break>`), và chính ElevenLabs nói "still experimenting" — cần thử thật trước khi khoá. Rủi ro "experimental" của Voice Design so với định nghĩa "or similar designation" trong BSA: **CHƯA XÁC MINH**, nên xin xác nhận bằng văn bản.

---

## 6. Từ điển phát âm (pronunciation dictionaries)

### 6.1 Mô hình nào hỗ trợ PHONEME, mô hình nào chỉ ALIAS

URL: https://elevenlabs.io/docs/eleven-api/guides/how-to/text-to-speech/pronunciation-dictionaries.md (2026-10-18)

> ElevenLabs supports both [IPA](https://en.wikipedia.org/wiki/International_Phonetic_Alphabet) and [CMU](https://en.wikipedia.org/wiki/CMU_Pronouncing_Dictionary) alphabets.

> Pronunciation dictionary phoneme tags only work with eleven_v4, eleven_flash_v2 and eleven_v3 models.
>
> Other models skip dictionary phoneme tags and use the default pronunciation. For other models, use
> alias tags instead to substitute spellings or phrases that produce the pronunciation you need.
>
> If you want to use IPA and CMU pronunciations in languages other than English, you will have to
> switch to the eleven_v4 model.

URL: https://elevenlabs.io/docs/eleven-agents/customization/voice/pronunciation-dictionary.md (2026-10-18) — cùng câu, kết thúc khác:

> If you want to use IPA and CMU pronunciations in languages other than English, you will have to
> switch to the eleven_v3 or eleven_v4 models.

URL: https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices.md (2026-10-18)

> This can be useful if you're generating using Multilingual v2, which doesn't support phoneme tags.

> Unlike older models that require XML-style phoneme tags, Eleven v4 understands IPA symbols when they are wrapped in forward slashes in your text:

> IPA pronunciation is more consistent than in previous models, but results can still vary by voice and phrase. We recommend testing important pronunciations with your chosen voice before relying on them in production.

> Phoneme tags are only compatible with the `eleven_flash_v2` [model](/docs/overview/models).

(Câu trên nằm trong mục "Phoneme tags for v2 models", tức nói về thẻ SSML inline của nhóm v2.)

**Mâu thuẫn trong tài liệu (cần nêu):**

URL: https://elevenlabs.io/docs/help-center/product/studio/studio/how-do-i-use-the-pronunciations-editor-in-studio.md (2026-10-18)

> Phoneme tags are only compatible with Eleven Flash v2.

URL: https://elevenlabs.io/docs/help-center/product/core-capabilities/text-to-speech/how-can-i-force-a-certain-pronunciation-of-a-word-or-name.md (2026-10-18)

> On Flash v2 and Turbo v2, you can force a certain pronunciation with SSML phoneme tags. We support both IPA and CMU.

URL: https://elevenlabs.io/docs/help-center/technical/do-pauses-and-ssml-phoneme-tags-work-with-the-api.md (2026-10-18)

> Please note that phonemes are available only for English language models and are currently not supported for other languages.

### 6.2 Cách gắn và giới hạn

URL: https://elevenlabs.io/docs/api-reference/text-to-speech/convert.md (2026-10-18)

> - `pronunciation_dictionary_locators` (list of PronunciationDictionaryVersionLocatorRequestModel, optional, nullable) — A list of pronunciation dictionary locators (id, version_id) to be applied to the text. They will be applied in order. You may have up to 3 locators per request

URL: https://elevenlabs.io/docs/api-reference/pronunciation-dictionaries/create-from-rules.md (2026-10-18)

> POST https://api.elevenlabs.io/v1/pronunciation-dictionaries/add-from-rules

> Rule can be either: an alias rule: \{'string\_to\_replace': 'a', 'type': 'alias', 'alias': 'b', } or a phoneme rule: \{'string\_to\_replace': 'a', 'type': 'phoneme', 'phoneme': 'b', 'alphabet': 'ipa' }

URL: https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices.md (2026-10-18)

> Please note that searches are case sensitive. When checking for a replacement word in a pronunciation dictionary, the dictionary is checked from start to end and only the very first replacement is used.

> Phoneme tags only work for individual words. If you have a name with a first and last name that you want to be pronounced a certain way, you will need to create a phoneme tag for each word.

Giới hạn số rule/kích thước file từ điển: **CHƯA XÁC MINH** (tài liệu hiện hành không nêu; con số 1,5 MB chỉ thấy trong bài blog cũ qua kết quả tìm kiếm, không tải và không xác nhận).

**Ý nghĩa cho dự án:** Theo trang API/Agents (mới nhất, cụ thể nhất), rule **phoneme (IPA/CMU)** chạy trên `eleven_v4`, `eleven_v3`, `eleven_flash_v2`; `eleven_multilingual_v2` **chỉ dùng alias** (bỏ qua phoneme). Tối đa **3 dictionary/lệnh**, khớp phân biệt hoa thường, phoneme chỉ cho từng từ. Vì các trang help/Studio cũ còn ghi "chỉ Flash v2", phải **chạy thử thật** từng tên riêng trên `eleven_v4` trước khi khoá.

---

## 7. Tính độc quyền (một giọng nhiều kênh dùng)

VLA (https://elevenlabs.io/vla, 2026-10-18):

> For clarity, others may be able to generate Output with the User Voice Models you have shared in our Library.

URL: https://elevenlabs.io/docs/help-center/product/voices/voice-library/what-is-the-voice-library.md (2026-10-18)

> The [Voice Library](https://elevenlabs.io/app/voice-library) is a marketplace where our community can share Professional Voice Clones and earn rewards when others use them.

URL: https://elevenlabs.io/docs/help-center/product/voices/my-voices/who-has-access-to-my-voices.md (2026-10-18)

> Unless you explicitly share a voice, the voices you’ve created are **only accessible through your account.**

URL: https://elevenlabs.io/docs/api-reference/text-to-voice/design.md (2026-10-18)

> Same seed with same inputs produces same voice.

ToS 4(e) (https://elevenlabs.io/terms-of-use, 2026-10-18): giấy phép cấp cho ElevenLabs với User Voice Models là "nonexclusive" và "sub-licensable, through multiple tiers (which means we can make it available to others)" (trích đầy đủ ở 1.4); ToS 4(d) có câu:

> Notwithstanding the foregoing, we will not commercialize your voice on a standalone basis without your permission to do so.

Không tìm thấy văn bản nào nói giọng Library/Default/thiết kế là **độc quyền** (exclusive) cho người dùng: **CHƯA XÁC MINH** (về tính độc quyền pháp lý của giọng thiết kế).

**Ý nghĩa cho dự án:** Giọng Library và Default **không độc quyền** — bất kỳ kênh nào cũng dùng được, nên khán giả có thể đã nghe giọng đó ở nơi khác (ảnh hưởng nhận diện thương hiệu phim). Giọng Voice Design chỉ nằm trong tài khoản/workspace của ta và không đưa lên Library được, nên **trên thực tế** là riêng; nhưng không có cam kết độc quyền pháp lý, và người khác dùng cùng prompt + seed có thể ra giọng giống. Ghi prompt, seed, `generated_voice_id` vào `RIGHTS.md`/`AUTHORSHIP.md`.

---

## Phụ lục: các URL đã tải (2026-10-18)

Mọi lần tải qua `curl -L` (HTTPS proxy của môi trường), trừ hai lượt WebSearch có ghi chú.

| # | URL | HTTP |
|---|---|---|
| 1 | https://elevenlabs.io/docs/llms.txt | 200 |
| 2 | https://elevenlabs.io/docs/llms-full.txt | 200 (trả về cùng nội dung chỉ mục, 220.224 byte — không phải toàn văn) |
| 3 | https://elevenlabs.io/terms-of-use | 200 |
| 4 | https://elevenlabs.io/terms | 200 (chuyển hướng → /terms-of-use) |
| 5 | https://elevenlabs.io/voice-library-terms | **404** — thay bằng /vla |
| 6 | https://elevenlabs.io/vla | 200 |
| 7 | https://elevenlabs.io/bsa | 200 |
| 8 | https://elevenlabs.io/service-specific-terms | 200 |
| 9 | https://elevenlabs.io/creative-terms | 200 |
| 10 | https://elevenlabs.io/elevenapi-terms | 200 |
| 11 | https://elevenlabs.io/use-policy | 200 (tải, không trích) |
| 12 | https://elevenlabs.io/pricing | 200 |
| 13 | https://elevenlabs.io/pricing/api | 200 |
| 14 | https://elevenlabs.io/docs/overview/models (HTML) | 200 |
| 15 | https://elevenlabs.io/docs/overview/models.md | 200 |
| 16 | https://elevenlabs.io/docs/eleven-creative/voices/voice-library.md | 200 |
| 17 | https://elevenlabs.io/docs/eleven-creative/voices/voice-design.md | 200 |
| 18 | https://elevenlabs.io/docs/eleven-api/guides/how-to/voices/voice-design.md | 200 |
| 19 | https://elevenlabs.io/docs/eleven-api/guides/how-to/text-to-speech/pronunciation-dictionaries.md | 200 |
| 20 | https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices.md | 200 |
| 21 | https://elevenlabs.io/docs/overview/capabilities/text-to-speech/eleven-v4.md | 200 |
| 22 | https://elevenlabs.io/docs/overview/capabilities/voices.md | 200 |
| 23 | https://elevenlabs.io/docs/eleven-api/choosing-the-right-model.md | 200 |
| 24 | https://elevenlabs.io/docs/eleven-agents/customization/voice/pronunciation-dictionary.md | 200 |
| 25 | https://elevenlabs.io/docs/api-reference/text-to-voice/design.md | 200 |
| 26 | https://elevenlabs.io/docs/api-reference/text-to-voice/create.md | 200 |
| 27 | https://elevenlabs.io/docs/api-reference/text-to-speech/convert.md | 200 |
| 28 | https://elevenlabs.io/docs/api-reference/pronunciation-dictionaries/create-from-rules.md | 200 |
| 29 | https://elevenlabs.io/docs/api-reference/pronunciation-dictionaries/create-from-file.md | 200 |
| 30 | https://elevenlabs.io/docs/help-center/product/voices/my-voices/what-are-default-voices.md | 200 |
| 31 | https://elevenlabs.io/docs/help-center/product/voices/my-voices/what-are-legacy-voices.md | 200 |
| 32 | https://elevenlabs.io/docs/help-center/product/voices/my-voices/how-do-i-access-eleven-labs-default-voices.md | 200 |
| 33 | https://elevenlabs.io/docs/help-center/product/voices/my-voices/who-has-access-to-my-voices.md | 200 |
| 34 | https://elevenlabs.io/docs/help-center/product/voices/my-voices/how-do-i-share-a-voice.md | 200 |
| 35 | https://elevenlabs.io/docs/help-center/product/voices/my-voices/how-do-i-delete-voices-from-my-voices.md | 200 |
| 36 | https://elevenlabs.io/docs/help-center/product/voices/voice-design/how-much-does-voice-design-cost.md | 200 |
| 37 | https://elevenlabs.io/docs/help-center/product/voices/voice-design/what-is-voice-design.md | 200 |
| 38 | https://elevenlabs.io/docs/help-center/product/voices/voice-design/what-kind-of-voices-can-i-create-using-voice-design.md | 200 |
| 39 | https://elevenlabs.io/docs/help-center/product/voices/voice-library/can-i-share-an-ai-generated-voice-in-the-voice-library.md | 200 |
| 40 | https://elevenlabs.io/docs/help-center/product/voices/voice-library/how-are-voices-updated-changed.md | 200 |
| 41 | https://elevenlabs.io/docs/help-center/product/voices/voice-library/how-do-i-delete-a-voice-ive-shared-with-the-voice-library.md | 200 |
| 42 | https://elevenlabs.io/docs/help-center/product/voices/voice-library/what-are-custom-rates-and-credit-multipliers.md | 200 |
| 43 | https://elevenlabs.io/docs/help-center/product/voices/voice-library/what-is-live-moderation.md | 200 |
| 44 | https://elevenlabs.io/docs/help-center/product/voices/voice-library/what-is-a-notice-period.md | 200 |
| 45 | https://elevenlabs.io/docs/help-center/product/voices/voice-library/what-is-the-voice-library.md | 200 |
| 46 | https://elevenlabs.io/docs/help-center/product/voices/voice-library/why-cant-i-use-some-voices-from-the-voice-library.md | 200 |
| 47 | https://elevenlabs.io/docs/help-center/product/core-capabilities/text-to-speech/how-can-i-force-a-certain-pronunciation-of-a-word-or-name.md | 200 |
| 48 | https://elevenlabs.io/docs/help-center/product/core-capabilities/text-to-speech/how-much-does-it-cost-to-generate-using-eleven-v3-alpha.md | 200 |
| 49 | https://elevenlabs.io/docs/help-center/product/core-capabilities/text-to-speech/what-is-eleven-v4.md | 200 |
| 50 | https://elevenlabs.io/docs/help-center/product/core-capabilities/text-to-speech/what-is-eleven-v3-alpha.md | 200 |
| 51 | https://elevenlabs.io/docs/help-center/product/core-capabilities/text-to-speech/whats-the-maximum-amount-of-characters-and-text-i-can-generate.md | 200 (trang này còn thiếu v4/v3 trong danh sách giới hạn API — đã dùng models.md) |
| 52 | https://elevenlabs.io/docs/help-center/product/core-capabilities/text-to-speech/can-i-use-the-same-cloned-designed-voice-across-languages.md | 200 |
| 53 | https://elevenlabs.io/docs/help-center/technical/do-pauses-and-ssml-phoneme-tags-work-with-the-api.md | 200 |
| 54 | https://elevenlabs.io/docs/help-center/technical/how-much-does-it-cost-to-use-the-api.md | 200 |
| 55 | https://elevenlabs.io/docs/help-center/technical/what-models-do-you-offer-and-what-is-the-difference-between-them.md | 200 |
| 56 | https://elevenlabs.io/docs/help-center/legal/can-i-publish-the-content-i-generate-on-the-platform.md | 200 |
| 57 | https://elevenlabs.io/docs/help-center/legal/audio-detector/will-watermarks-cause-my-content-to-be-flagged-downranked-or-demonetized-on-you-tube-or-other-platforms.md | 200 |
| 58 | https://elevenlabs.io/docs/help-center/account/general/where-can-i-find-out-more-about-the-pricing-plans.md | 200 |
| 59 | https://elevenlabs.io/docs/help-center/product/monetization-business/payouts/what-are-voice-actor-payouts.md | 200 |
| 60 | https://elevenlabs.io/docs/help-center/product/studio/studio/how-do-i-use-the-pronunciations-editor-in-studio.md | 200 |
| — | WebSearch ×3 (Voice Design ownership; giới hạn từ điển; quyền thương mại giọng Default) | chỉ dùng để dò; không trích từ kết quả tìm kiếm |

Không truy cập `help.elevenlabs.io` (trung tâm trợ giúp hiện nằm trong `elevenlabs.io/docs/help-center/`).
