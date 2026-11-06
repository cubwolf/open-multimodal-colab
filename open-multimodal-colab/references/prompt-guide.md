**English** | [繁體中文](prompt-guide.zh-TW.md)

# Writing prompts

These models all take natural language, in English or Chinese; **English is usually more reliable**. Describe the concrete picture, not abstract adjectives.

## Text to image (Z-Image-Turbo)
- Order: subject → appearance details → action / pose → setting → lighting → lens and composition → style.
- Put text to be drawn in quotes, e.g. `a neon sign that says "OPEN 24H"`. Chinese characters work too; short text works best.
- 8 steps and cfg 1 are the official settings, and negative prompts are not supported; just leave out what you don't want.
- Example:
  `A young woman with short black hair and a beige trench coat stands under a red umbrella on a rainy Taipei street at night, neon signs reflecting on the wet pavement, shallow depth of field, 35mm photo, cinematic color grading`

## Image editing (FLUX.2 klein 4B)
- Refer to the `inputs` by order as `image 1`, `image 2`; image 1 is the one being changed.
- Say in one sentence **what to change and what to keep**:
  `Change the jacket of the woman in image 1 to a dark green leather jacket, keep her face, hair and pose unchanged`
- Compositing: `Place the woman from image 1 sitting at the table in image 2, matching the warm evening light of image 2`
- Change one or two things at a time; for many changes, split them into several jobs chained with `@id`.

## Video (Wan 2.2 TI2V-5B)
- Write 2–4 English sentences: subject and appearance, **how the action unfolds**, setting, camera movement, lighting and mood.
- Write actions as a sequence ("turns her head, looks at the window, then smiles"), not just a state.
- Use film language for the camera: `slow push-in`, `tracking shot`, `static shot`, `aerial view`, `handheld`.
- Image to video: the image already fixes the look, so focus on **what happens next** and how the camera moves; keep any appearance description consistent with the image.
- A clip is only about 5 seconds; keep to one action or one shot.
- `negative` can list what you don't want; without it the official template's default is used (avoids subtitles, frozen frames, deformed fingers and so on).
- Example:
  `A street musician in a worn leather jacket plays guitar in a retro subway station. Commuters hurry past him and a small crowd slowly gathers. Slow push-in from a medium shot to a close-up of his hands. Warm, dim lighting with soft film grain.`

## Video extension (`extend`)
- The new clip starts from the **last frame** of the earlier clip; the prompt only describes what happens next.
- Make ordered actions explicit and link them with time words:
  `The man walks to the right side of the frame, facing his walking direction. After two steps he turns his head toward the camera while still walking, smiles and waves his right hand.`
  In testing, the order "walk to the right, then turn to the camera" did not come through clearly; be more specific, or try another seed.
- Give directions in frame terms (`to the right side of the frame`), not the character's own left and right.

## Voice-over (Qwen3-TTS) and talking video (S2V)
- `voice` must state gender, age, tone and pace, e.g. `溫和親切的中年男性，語速適中，帶著笑意` (a warm, friendly middle-aged man, moderate pace, smiling).
- The talking-video prompt describes expression and gestures, not lip movement: `A friendly man introduces himself to the camera with a warm smile and natural hand gestures, static shot`.
- The clip is as long as the speech; change the length of the line to control it.
