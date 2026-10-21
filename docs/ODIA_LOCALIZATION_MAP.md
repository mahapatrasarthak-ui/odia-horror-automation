# Odia Localization Map

## Purpose

This document defines how the Hindi folk-horror automation becomes an Odia-first production system.

The goal is not only to translate words. Every episode should feel like it was written, voiced, designed, and packaged for an Odia-speaking audience while keeping the reliable production engine intact.

The map covers language, Odisha settings, characters, folklore sensitivity, audio, visuals, title cards, publishing metadata, and quality checks.

## Current implementation status

The first localization layer is implemented on the odia-adaptation branch:

- Central locale profile in scripting/pipeline/localization.py, with Odia as the fork default and Hindi preserved as an explicit option.
- Odia routing for idea, story, character, background, animation, and publishing templates.
- Locale-aware generator metadata, narrator direction, character voice fallback, dialogue labels, title-card kicker, and title font.
- Locale-aware general CLI, Windows launcher, parser compatibility, and production editor dialogue lookup.
- Python smoke tests for Odia routing, Hindi compatibility, and a complete 12-scene fake generation.

Still pending is a live provider test: generate one narrator scene and one speaking-character scene, verify the actual Odia voice and Odia glyph font, then expand to the full 12-scene run.

## 1. Localization profile

| Field | First Odia target | Why it matters |
|---|---|---|
| Language name | Odia | Used by prompts, narration, metadata, and review |
| Language code | or-IN (candidate) | Provider support must be tested before production |
| Script | Odia script | Spoken lines and on-screen text should render in Odia glyphs |
| Region | Odisha, India | Gives settings and cultural details a consistent home |
| Culture mode | Odisha-localized; episode setting remains configurable | Coastal, western, southern, urban, and rural episodes should not look identical |
| Story type | Folk horror / supernatural suspense | Keeps the channel identity while allowing original stories |
| Visual style | Flat, semi-realistic 2D Indian animation | Preserve the existing visual language unless an episode deliberately changes it |
| Frame | 16:9 | Keep the current video and thumbnail layout |
| Quick-run structure | 12 scenes initially | Retain the production contract while we localize; optimize later using evidence |
| Clip duration | Natural duration selected by the video model | Do not assume that a Hindi line and an Odia line take the same time |

The profile should eventually live in one central configuration object. Prompts and code should read from that object instead of repeating Hindi assumptions.

## 2. What changes and what stays

### Must change for Odia

- Story instructions and spoken language.
- Hook and idea-generation instructions.
- Character names, identities, clothing, appearance, behavior, and speech style.
- Background and animation prompts, including Odisha-specific place and material details.
- Narrator direction, pronunciation, rhythm, emotion, and voice selection.
- Dialogue timing and pronunciation review.
- Title-card wording, font support, line wrapping, and thumbnail text.
- Video title, description, tags, language settings, and other publishing metadata.
- Cultural and folklore review rules.
- Any hidden fallback text that says Hindi, Devanagari, North Indian, or a Hindi accent.

### Can stay while we learn

- JSON status fields and scene numbering.
- Asset naming and speaker ownership rules.
- Browser automation, download, retry, and recovery logic.
- FFmpeg assembly, audio mixing, loudness checks, and final MP4 creation.
- 16:9 output, natural Flow clip duration, review/approval checkpoints, and API-key loading.
- The initial 12-scene production contract.

This separation is important: localization changes the creative inputs and validation, while the dependable mechanical engine can continue to do its job.

## 3. Repository change map

| File or area | Role | Odia work |
|---|---|---|
| scripting/prompts/odia/3- STORY.txt | Odia story template | Created first; refine for natural spoken Odia, Odisha settings, and flexible timing |
| scripting/pipeline/prompts.py | Template router | Created Odia story routing; extend routing carefully for each stage |
| scripting/pipeline/one_minute.py | Quick-run generator | Remove Hindi-only hooks, North Indian defaults, Devanagari requests, and fixed Hindi assumptions; read the locale profile |
| make_prompts in one_minute.py | Prompt assembly | Replace Hindi accent, Hindi speech, and Devanagari instructions with locale-aware values |
| scripting/prompts/1- IDEA GENERATION.txt | Idea stage | Add Odia audience, original Odisha context, and non-stereotyping guidance |
| scripting/prompts/4- CHARACTER IMAGE PROMPTS.txt | Character stage | Add Odia names, clothing, features, props, and continuity rules |
| scripting/prompts/5- IMAGE PROMPTS.txt | Background stage | Add selected Odisha region, architecture, vegetation, weather, roads, and materials |
| scripting/prompts/6- ANIMATION PROMPTS.txt | Motion stage | Add Odia visual and cultural context without forcing a location that the premise does not need |
| scripting/prompts/7- UPLOADING.txt | Publishing stage | Generate natural Odia metadata and optional English discovery terms without keyword stuffing |
| production/src/createNarrationManifest.ts | Narration manifest | Make narrator direction and locale configurable; remove the Hindi folk-horror fallback |
| production/src/narration.ts | Voice generation | Test an Odia-capable provider/voice, pronunciation, and error handling |
| production/src/addTitle.ts | Title card | Parameterize kicker/title wording and select a font with complete Odia glyph coverage |
| AGENTS.md | Project rules | Replace Hindi-only rules with locale-aware rules and keep an explicit Odia profile |
| scripting/style_reference.md | Visual continuity | Preserve the base 2D style and add Odisha references without turning every story into a stereotype |
| docs/editor.md | Human review | Add Odia pronunciation, subtitle, glyph, timing, and cultural review notes |

## 4. Odisha cultural localization

Localization should be selected per episode, not pasted into every story. A coastal fishing village, a western Odisha town, a hill settlement, and Bhubaneswar should have different visual and social details.

### Episode setting card

Every episode should identify:

- Odisha region or city type.
- A fictional place name unless a real place is genuinely needed.
- Season, weather, time of day, and light.
- Architecture, road surface, transport, vegetation, and local materials.
- Social setting: household, hostel, bus stand, market, school, workplace, village path, or another premise-appropriate space.
- Details that are observed in the scene versus invented for fiction.

Do not force a bus, temple, village, sari, festival, or coastal image into a story merely to signal Odisha. The premise decides what belongs in the scene.

### Character identity card

For each recurring character, specify:

- Odia name, age range, occupation, relationships, and home context.
- Clothing, hair, facial features, skin tone, body shape, and one or two stable identifying details.
- Speech style, politeness level, vocabulary, emotional habits, and any code-switching that is intentional.
- Important props and how they remain visually consistent across scenes.
- What the character knows, fears, wants, and refuses to do.

The purpose is continuity and believable people, not a checklist of stereotypes.

### Folklore and sensitivity

- Mark a story as original fiction, adapted from a documented legend, or inspired by a broad motif.
- Verify factual claims about real communities, places, rituals, and history before presenting them as facts.
- Avoid portraying a tribal, religious, caste, regional, or occupational identity as inherently evil or backward.
- Treat real sacred places and living traditions respectfully; do not invent damaging claims about identifiable people or communities.
- Keep a short source note when a known legend or historical reference is used.

## 5. Audio localization

The narration and dialogue are a separate localization layer from the images.

- Narrator: natural Odia pronunciation, believable rhythm, folk-horror tension, controlled pauses, and consistent names.
- Dialogue: exact Odia words, correct speaker ownership, and no accidental Hindi filler or Hindi cadence.
- Voice selection: test the actual provider and voice; do not assume a language code guarantees good Odia output.
- Timing: measure the generated Odia recording. Re-time scenes or captions when Odia takes longer or shorter than the Hindi draft.
- Mixing: preserve the existing music and effects pipeline, then check that Odia speech remains intelligible on a phone speaker.
- Flow clips: make sure a clip does not contain duplicate generated speech when the separate narration track is used.

## 6. Text and visual rendering

Odia text must be treated as a rendering requirement, not just a translation.

- Use UTF-8 end to end.
- Select a font with complete Odia glyph coverage.
- Test conjuncts, vowel signs, punctuation, numerals, and longer words.
- Check line wrapping, safe margins, stroke/outline, contrast, and mobile readability.
- Inspect the title card and thumbnail at small size; a technically correct glyph can still be unreadable.
- Keep a small rendering test containing Odia vowels, consonants, a sample name, punctuation, and a two-line title before a full render.
- If a provider cannot reliably render Odia, record the limitation and use a controlled fallback rather than silently mixing scripts.

## 7. Publishing localization

The publishing layer should help an Odia viewer understand and find the video.

- Title: natural Odia first; add a concise English transliteration only when it improves discovery.
- Description: one clear Odia summary, fiction/folklore framing, and a short call to action.
- Search terms: use relevant Odia phrases and a small number of meaningful English variants; avoid repetitive keyword lists.
- Thumbnail: short, readable Odia text with a strong visual hook.
- Metadata: set the video language and audience information accurately.
- Channel consistency: keep a recognizable horror identity while varying the episode setting and hook.

## 8. Implementation order

1. Preserve the working Hindi path so the current system remains recoverable.
2. Centralize the locale profile.
3. Route the story stage to the Odia template.
4. Remove Hindi-only follow-up instructions from code.
5. Adapt idea, character, background, and animation prompts.
6. Test an Odia narrator and one speaking character.
7. Parameterize title-card text and verify the Odia font.
8. Adapt publishing metadata.
9. Run a two-scene controlled test before a full episode.
10. Review script, voice, lip sync, text rendering, visuals, timing, and cultural fit.
11. Run the full 12-scene episode.
12. Record failures and fixes in a small test report so future episodes become repeatable.

## 9. Acceptance checks for the first Odia test

A test is successful only when all of these are true:

- Odia is selected by configuration, not by manually editing one prompt.
- Spoken lines are natural Odia and use Odia script where text is displayed.
- No unintended Hindi, Devanagari, North Indian, or Hindi-accent fallback remains.
- The premise, selected Odisha setting, character identities, and props remain consistent.
- The narrator direction asks for Odia pronunciation and the selected voice can deliver it.
- Each line belongs to the correct speaker and no duplicate speech is heard.
- The title card and thumbnail render without missing glyphs or broken wrapping.
- Timing is measured from the Odia audio rather than copied from Hindi timings.
- Visual details match the chosen setting and do not rely on generic Odisha stereotypes.
- The result is reviewed on a phone-sized preview before full publishing.

## 10. First controlled episode profile

Before generating the first complete Odia episode, fill this card:

| Field | Value to decide |
|---|---|
| Working title | An Odia title or a temporary English label |
| Hook | One sentence that creates curiosity |
| Target duration | Keep the initial quick run at about one minute |
| Scene count | 12 for the first controlled run |
| Region/environment | Coastal, western, southern, central, urban, or another justified setting |
| Fictional place | A consistent invented locality |
| Protagonist | Name, age, work, appearance, and voice |
| Supporting characters | Names, roles, appearance, and speaker mapping |
| Supernatural rule | What the entity can and cannot do |
| Narrator | Provider, voice, pronunciation test, and emotional direction |
| Character voice | Provider, voice, delivery, and timing test |
| Visual references | Approved clothing, architecture, palette, and lighting |
| Title text | Short Odia title-card wording |
| Thumbnail text | Short Odia hook readable on a phone |
| Sensitive elements | Real places, communities, rituals, or legends requiring review |

This map remains the plan and review checklist. The locale profile, prompt routing, generator, launcher, narrator manifest, title card, and production fallbacks are now implemented on the odia-adaptation branch. The next step is the live two-scene Odia test, followed by a full 12-scene episode only after voice, glyph, timing, lip-sync, visual continuity, and cultural review pass.