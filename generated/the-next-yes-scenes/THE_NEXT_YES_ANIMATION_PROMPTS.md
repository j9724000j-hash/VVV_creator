# 🎬 THE NEXT YES — برومبتات التحريك الاحترافية | Animation Prompts v6.1.1
**جميع المشاهد 01-10 | 58 ثانية | 9:16 عمودي | MS-04 Warm Bittersweet**

> هذا الملف يجمع **برومبتات تحريك احترافية هايبر** لكل مشهد من المشاهد الـ 10 السابقة، مناسبة 100% للسكريبت والقصة الصوتية وتوقيت VN. كل برومبت مكتوب ليُستخدم مباشرة في أدوات تحريك الصور إلى فيديو: **Runway Gen-3 / Kling 2.0 / Luma Dream Machine / Hailuo / Pika 2.2** وكذلك كـ **تعليمات Keyframes دقيقة في VN Video Editor**.

**القاعدة الذهبية:** التحريك خفيف جداً ومحسوب — القصة هي البطلة، وليس المؤثرات. لا اهتزاز، لا زووم عدواني، لا تشويه للوجه أو الانعكاس.

**المجلد:** `generated/the-next-yes-scenes/` — نفس الصور الثابتة تُحرّك

---

## 📋 جدول سريع — الحركة لكل مشهد

| # | التوقيت | اسم الملف الثابت | حركة الكاميرا الأساسية | شدة الحركة |
|---|---------|------------------|------------------------|------------|
| 01 | 0:00 → 0:00.5 | `scene-01-visual-hook-try-again.png` | Push-in خفيف جداً 100%→102% | 2% فقط |
| 02 | 0:00.5 → 0:04 | `scene-02-verbal-hook-window-mug.png` | Push-in بطيء 100%→103% | 3% |
| 03 | 0:04 → 0:08 | `scene-03-context-bridge-empty-chair.png` | Pan جانبي من الكرسي للمرأة | لطيف |
| 04 | 0:08 → 0:18 | `scene-04-core-a-pain-phone-invitation.png` | Focus Shift وهمي + Push-in | متوسط-خفيف |
| 05 | 0:18 → 0:28 | `scene-05-core-b-inner-conflict-reflection.png` | Push-in 100%→103% مع انعكاس ثابت | 3% |
| 06 | 0:28 → 0:36 | `scene-06-core-c-unanswered-question.png` | Push-in 100%→104% ثم تجميد | 4% ثم Hold |
| 07 | 0:36 → 0:44 | `scene-07-emotional-payoff-cafe-coffee.png` | Dissolve دافئ + Push-in 100%→104% | 4% |
| 08 | 0:44 → 0:47 | `scene-08-like-share.png` | Static / حركة شبه معدومة | 0-1% |
| 09 | 0:47 → 0:54 | `scene-09-cta-again.png` | Static تماماً | 0% |
| 10 | 0:54 → 0:58 | `scene-10-loop-trigger-closing.png` | مطابق للمشهد 01 + تجميد للـ Loop | 2% |

---

## 🎥 البرومبتات الهايبر الاحترافية للتحريك — جاهزة للنسخ

### ① VISUAL HOOK | 0:00 → 0:00.5 | `scene-01`
**الهدف الدرامي:** التوتر الصامت — الإبهام متردد فوق الشاشة وانعكاس العين هو الـ pattern interrupt. أول إطار يجب أن يظهر فوراً بلا Fade In.

**VN Keyframes (الطريقة الأساسية):**
```
Scale: 100% → 102% خلال 0.5 ثانية
Position: ثابت
Easing: Linear
Transition IN: Hard Cut (لا Fade In)
```

**برومبت تحريك AI (انسخه كما هو):**
```
Subtle cinematic push-in on a close-up of elegant mature woman's hands holding a smartphone, her thumb hovering millimeters above the dark screen with hesitation. Faint realistic reflection of her hazel eyes visible in the phone glass, physically accurate, no distortion. Cool dusk window light + warm practical lamp. Ultra slow dolly-in, 2% scale only, shallow depth of field, creamy bokeh, ARRI Alexa, 24fps. No camera shake, no face distortion, no extra fingers, no text, no logo. Keep hands and phone perfectly stable, only gentle forward motion. Loop-ready, photorealistic, 9:16 vertical.
```
**Negative Prompt:**
```
no shake, no warp, no face morph, no extra fingers, no text, no glitch, no fast zoom, no plastic skin
```
**SFX/BGM:** نوتة بيانو دافئة واحدة مع بداية الصورة (Pixabay)

---

### ② VERBAL HOOK | 0:00.5 → 0:04 | `scene-02`
**الهدف:** تأمل هادئ بجانب النافذة — الانتقال من التوتر للتفكير.

**VN Keyframes:**
```
Scale: 100% → 103% خلال 3.5 ثانية
Easing: Ease In Out (بطيء جداً)
Transition: Cut نظيف أو Dissolve 0.2s فقط إذا احتاج التسلسل
```

**برومبت تحريك AI:**
```
Slow intimate push-in on a 52-year-old woman sitting beside a large apartment window at blue hour dusk, holding a white ceramic mug with both hands, gazing at distant city lights bokeh outside. Cool blue evening light on one cheek, warm lamp glow on the other. Ultra slow cinematic dolly-in, almost imperceptible, 3% scale, shallow DOF, subtle background city lights twinkling softly, natural skin texture. Premium independent film look, restrained emotion, contemplative. No head movement, no camera shake, no morphing, 9:16 vertical, 24fps.
```
**Negative:** `no head turn, no eye blink exaggeration, no warp, no shake`

---

### ③ CONTEXT BRIDGE | 0:04 → 0:08 | `scene-03`
**الهدف:** الغياب بدون إظهار شريك سابق — الكرسي الفارغ في المقدمة.

**VN Keyframes:**
```
Scale: ثابت 100%
Position X: 0% → -3% (Pan لطيف من الكرسي نحو المرأة)
Duration: 4 ثوان
Easing: Ease In Out
Transition: Dissolve 0.25s من المشهد السابق
```

**برومبت تحريك AI:**
```
Gentle lateral tracking shot starting on a softly illuminated empty wooden armchair in foreground, then slowly revealing a composed 52-year-old woman standing in middle distance in a tasteful dim living room at dusk. Warm practical light on chair, cool shadows behind. Slow cinematic pan left-to-right, shallow depth of field, layered foreground/background, natural textures, bookcase softly blurred. No people appearing, no ghosting, no double exposure, photorealistic, 9:16 vertical, ARRI Alexa. Keep both chair and woman sharp enough, elegant slow motion.
```
**Negative:** `no person appearing in chair, no ghost, no warp, no fast pan`

---

### ④ CORE-A — PAIN DEVELOPMENT | 0:08 → 0:18 | `scene-04`
**الهدف:** 3 نبضات تصاعدية — الحذر → الدعوة → كادت ترفض. التركيز يتحول من الهاتف للعينين.

**VN Keyframes (حيلة بدون Rack Focus حقيقي):**
```
Beat 1 (0:08-0:11): Scale 100%→101% على الهاتف
Beat 2 (0:11-0:14): Cut إلى نفس الصورة ب Crop أقرب للعينين (يحاكي تغير التركيز)
Beat 3 (0:14-0:18): Hold 101% مع انخفاض BGM قليلاً
Transition: Hard Cut عند 0:08، ثم Cut نظيف بين النبضات
```

**برومبت تحريك AI (مقسم لثلاثة أجزاء، استخدم نفس الصورة):**
```
Beat 1: Extreme close-up of mature woman's hands holding smartphone, thumb hovering above reply area, cautious uncertainty on face, warm light on hands, cool dusk background, very slow push-in 1%, shallow DOF, photorealistic.

Beat 2: Add subtle simulated rack focus from phone screen to woman's hazel eyes, maintain 5 natural fingers, blank dark screen no text, creamy bokeh shift, no warp, no morph.

Beat 3: Hold on eyes with restrained hesitation, almost saying no, quiet tension, ultra slow motion, no exaggerated emotion, 9:16 vertical, 24fps.
```
**إضافة في VN:** طبقة نص منفصلة للرسالة `Would you like to get dinner this Friday?` تظهر 1.5-2 ثانية عند 00:11 مع صوت Notification ناعم (Mixkit - soft notification). لا تُولّد النص داخل الصورة.

**Negative:** `no text on screen, no app UI, no finger warp, no face morph`

---

### ⑤ CORE-B — INNER CONFLICT | 0:18 → 0:28 | `scene-05`
**الهدف:** التناقض: الرغبة في التواصل مقابل تذكر التكلفة. الانعكاس يجب أن يبقى مطابقاً تماماً.

**VN Keyframes:**
```
Scale: 100% → 103% خلال 10 ثوان
Position: ثابت
Reflection: لا تحرك الانعكاس رقمياً أبداً — يجب أن يبقى مطابقاً للوجه الحقيقي
```

**برومبت تحريك AI:**
```
Slow cinematic push-in on a mature woman standing beside a large apartment window at dusk, smartphone resting loosely in one hand, looking at her physically accurate reflection in the glass. Reflection perfectly aligned with real face, no duplication, no distortion, city lights bokeh outside with soft twinkle. Warm lamp on one side of face, cool window light on other, split lighting. Quiet resilience, internal conflict through subtle gaze, no tears, no head movement. Ultra slow dolly-in 3%, shallow DOF, ARRI Alexa, photorealistic, 9:16 vertical. Keep reflection locked to face, no supernatural effects.
```
**تحذير:** لا تستخدم أي تأثير Broken Glass أو Lens Flare أو تشويه رقمي للانعكاس.

**Negative:** `no reflection warp, no duplicate face, no broken glass, no lens flare, no tears`

---

### ⑥ CORE-C — THE UNANSWERED QUESTION | 0:28 → 0:36 | `scene-06`
**الهدف:** المفصلة النفسية — السؤال `What if protecting my heart means never giving it a chance?` ثم صمت محسوب 0.3-0.5 ثانية.

**VN Keyframes:**
```
Scale: 100% → 104% خلال 6 ثوان ثم HOLD ثابت لآخر 2 ثانية أثناء الصمت
BGM: خفض إلى 12-15% قبل السؤال مباشرة
Transition: Cut نظيف إلى تأطير أقرب
```

**برومبت تحريك AI:**
```
Intimate close portrait of same 52-year-old woman sitting beside apartment window at dusk, smartphone resting in hands on lap, shoulders just beginning to relax, expression of thoughtful realization, subtle softening around hazel eyes, not smiling yet. Warm lamp balancing cool evening window light, bittersweet glow. Ultra slow push-in 4% then freeze and hold perfectly still for 2 seconds, shallow DOF, natural skin texture, premium film look. No camera movement during final hold, no face morph, no smile morph, 9:16 vertical, 24fps. Leave negative space beside face for text.
```
**النص في VN:** 
```
WHAT IF PROTECTING MY HEART...
...KEEPS IT CLOSED?
```
يظهر بـ Fade In بطيء 0.2s ويبقى ثابتاً أثناء الصمت. لا تُحرك الكاميرا أثناء بقاء السؤال على الشاشة.

**Negative:** `no smile animation, no head nod, no warp, no shake during hold`

---

### ⑦ EMOTIONAL PAYOFF | 0:36 → 0:44 | `scene-07`
**الهدف:** القرار المتواضع — قهوة واحدة بحدود، وليس وعداً بنهاية سعيدة. أول انتقال Dissolve واضح في الفيديو.

**VN Keyframes:**
```
Transition IN: Dissolve 0.25-0.3s من المشهد البارد للدافئ (الوحيد الواضح في الفيديو)
Scale: 100% → 104% خلال 6 ثوان ثم Hold لآخر 1.5-2 ثانية للسؤال الختامي
Warm Light Leak (اختياري): Screen Blend 10-15% للحظة قصيرة فقط
```

**برومبت تحريك AI:**
```
Warm cinematic reveal of same mature woman sitting at small round wooden table in quiet sunlit neighborhood café during late morning, two plain white ceramic coffee cups with subtle steam on table, soft natural daylight through large windows, warm wood tones, blurred café background with gentle bokeh. Across table only soft blurred shoulder/arm of another adult, no identifiable face. Woman with cautiously hopeful restrained half-smile, self-possessed posture, looking toward unseen person. Slow dolly-in 4% then hold, shallow DOF, delicate background bokeh, no hands touching, no kiss, photorealistic, 9:16 vertical, warm bittersweet color, ARRI Alexa.
```
**النص المتسلسل في VN:**
1. `ONE COFFEE.` (تظهر أولاً)
2. `NOT A PROMISE. A POSSIBILITY.`
3. `Would you give love another chance?` (تبقى 1.5-2 ثانية)

**BGM:** ارتفاع تدريجي إلى 22-28% ثم خفض قبل السؤال الأخير

**Negative:** `no kiss, no hand touch, no face morph, no extra people, no menu text`

---

### ⑧ LIKE + SHARE | 0:44 → 0:47 | `scene-08`
**الهدف:** دعوة مشاركة لطيفة — القصة انتهت، لا تسرق الأضواء.

**VN Keyframes:**
```
Scale: ثابت 100% أو Push-in شبه معدوم 100%→101%
Text: Fade In بطيء فقط
Transition: Hard Cut من السؤال الختامي
```

**برومبت تحريك AI:**
```
Static hold on the same quiet café scene, same mature woman with coffee cups, extremely subtle almost imperceptible slow motion, warm natural light, shallow DOF, no camera movement, no subject movement. Minimal Like icon may appear as small static overlay in corner, no bounce animation, no stickers. Hold calm and stable, 9:16 vertical, photorealistic. No new character, no new scene, reuse existing café still.
```
**ملاحظة:** لا تنشئ مشهداً جديداً — أعد استخدام صورة المشهد 07 مع Hold ثابت. أيقونة Like اختيارية وصغيرة جداً (<1 ثانية).

---

### ⑨ CTA | 0:47 → 0:54 | `scene-09`
**الهدف:** التعليق بـ AGAIN — دعوة كتابية لأن لا يوجد رابط خارجي.

**VN Keyframes:**
```
Scale: ثابت 100% تماماً — لا زووم، لا Pan، لا اهتزاز
Text: COMMENT "AGAIN" ↓ يظهر بـ Fade In، الكلمة AGAIN بلون #E8A020 ومقاس 64-72pt مع خلفية داكنة إذا لزم للتباين
```

**برومبت تحريك AI:**
```
Completely static freeze frame of the same café table with two white coffee cups and woman's hands/calm posture, no movement at all, stable hold, natural café lighting, photorealistic, 9:16 vertical. No browser mockup, no fake URL button, no new visual, keep emotional continuity with same character visible. Freeze frame stable for CTA text overlay.
```
**النص:**
```
【 COMMENT "AGAIN" ↓ 】
Pinned comment: What feels hardest?
```
الكلمة المفتاحية AGAIN هي الأقوى بصرياً (ذهبي #E8A020).

---

### ⑩ LOOP TRIGGER | 0:54 → 0:58 | `scene-10`
**الهدف:** العودة للبداية — نفس جملة الافتتاح تُعاد حرفياً، والصورة الأخيرة تطابق الأولى تماماً لحلقة سلسة.

**VN Keyframes:**
```
Scale & Crop: مطابق تماماً للمشهد 01 (100%→102%)
Position: مطابق تماماً للهاتف وموضع اليد
Color Grade: نفس MS-04 تماماً، لا تدفئة إضافية
BGM: قطع عند 00:57.7 قبل الحل الموسيقي — يبقى معلقاً
No outro, no logo, no fade out — قطع مباشر للـ Loop
```

**برومبت تحريك AI:**
```
Exact same intimate close-up of elegant mature woman's hands holding smartphone with thumb hovering above dark screen, faint realistic eye reflection in glass, identical to opening shot, same 85mm close-up, same cool dusk + warm lamp lighting, same camel cardigan and navy blouse. Ultra slow push-in 2% matching opening, no new motion, identical composition, scale, color and phone position to enable seamless loop. No new headline, opening headline TRY AGAIN? absent or fading before loop point, only verbatim subtitles remain. Photorealistic, 9:16 vertical, no extra effects, loop-ready.
```
**الصوت:** نفس تسجيل الجملة الأولى تماماً: `At fifty-two, she wasn't afraid of being alone.` — نفس النبرة والطاقة.

**Negative:** `no fade out, no black frame, no logo, no new shot, no color change`

---

## 🛠️ دليل التطبيق في VN Video Editor (موبايل فقط)

### إعداد المشروع
- Canvas: 9:16 عمودي، 1080×1920، 30fps، H.264 MP4
- استيراد الصور الـ 7 الفريدة + 3 إعادات الاستخدام بالترتيب الزمني أعلاه
- ضع الصورة الافتتاحية عند 00:00 وابدأ التعليق الصوتي على أول إطار

### طبقات VN
1. **Layer 1 — Base visuals:** الصور الثابتة المتحركة بـ Keyframes (لا فراغات)
2. **Layer 2 — Audio:** تعليق صوتي + BGM بيانو + SFX إشعار واحد فقط
3. **Layer 3 — Overlays:** رسالة الدعوة كطبقة نص منفصلة + حبيبات فيلم اختيارية 10-15% Overlay
4. **Layer 4 — Text:** ترجمات حرفية + عناوين داعمة قصيرة + CTA

### خطوات التحريك في VN
1. لكل صورة: اضغط على الكليب → Keyframe → Scale/Position
2. استخدم القيم المذكورة أعلاه (100%→102% إلخ) — لا تتجاوز 4%
3. Easing: Linear أو Ease In Out — لا تستخدم Bounce/Elastic
4. الانتقالات: Hard Cut أساساً + Dissolve 0.2-0.3s فقط عند الضرورة العاطفية
5. أضف رسالة `Would you like to get dinner this Friday?` كعنصر نص منفصل عند 00:11 (38-44pt)
6. طبق نفس LUT/Preset على جميع الكليبات (Warm Vintage Free 60% إذا استخدمت)

### نصائح ذهبية
- لا تضخم الحركة — الشورت العاطفي يحتاج سكون، لا أكشن
- لا تشوه الانعكاس رقمياً أبداً
- حافظ على نفس درجة حرارة اللون لكل المشاهد
- جمد الحركة أثناء السؤال المحوري (المشهد 06) وأثناء CTA (09)

---

## 📦 الملفات الجاهزة

- الصور الثابتة: `generated/the-next-yes-scenes/*.png` (7 فريدة + 3 إعادة)
- ZIP المضغوط: `generated/the-next-yes-scenes.zip` (24 MB)
- البرومبتات الثابتة: `THE_NEXT_YES_HYPER_PROMPTS_EDITION.md`
- هذا الملف: `THE_NEXT_YES_ANIMATION_PROMPTS.md`

> كل البرومبتات أعلاه جاهزة للنسخ واللصق مباشرة في Runway/Kling/Luma أو كتعليمات Keyframes في VN. استخدمها كما هي دون تعديل لتحافظ على الاستمرارية.

---
*تم إنشاؤه كبرومبتات تحريك هايبر احترافية مطابقة 100% لسكريبت THE NEXT YES v6.1.1 — حركة محسوبة، سينمائية، ومحترمة للمشاهد.*
