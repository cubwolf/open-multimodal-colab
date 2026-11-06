**English** | [繁體中文](manifest.zh-TW.md)

# manifest.json

Put it in a working folder; every `inputs` path is **relative to the folder that holds the manifest**.
Results are downloaded to `out/<id>.<ext>` in the same folder, with a summary in `out/results.json`.

```json
{
  "gpu": "L4",
  "stop_on_error": false,
  "jobs": [
    {"id": "cast_lin", "type": "image",
     "prompt": "A clean studio portrait of a young woman with short black hair ...",
     "aspect": "3:4", "size": "1.5K", "seed": 1},

    {"id": "frame01", "type": "image",
     "prompt": "Put the woman from image 1 at the reading table in image 2, warm evening light",
     "inputs": ["@cast_lin", "inputs/library.png"], "aspect": "16:9"},

    {"id": "shot01", "type": "video",
     "prompt": "She looks up from her book and smiles, the camera slowly pushes in ...",
     "inputs": ["@frame01"], "seconds": 5, "aspect": "16:9", "resolution": "720P"},

    {"id": "establish", "type": "video",
     "prompt": "Aerial view of a rainy city at night, neon reflections on wet streets ...",
     "seconds": 4, "aspect": "16:9", "resolution": "480P"}
  ]
}
```

## Fields

| Field | Used by | Meaning |
|---|---|---|
| `id` | all | letters, digits, `-`, `_`; also the output file name |
| `type` | all | `image` / `video` / `tts` / `talk` |
| `prompt` | all | see prompt-guide.md |
| `inputs` | image, video, talk | talk: 1 portrait. image: 0 = text to image, 1–4 = edit (image 1 is the one changed). video: 0 = text to video, 1 = first frame |
| `aspect` | image, video | image: `auto` (when editing, same ratio as image 1; for text to image it means `1:1`), `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `3:2`, `2:3`, `21:9`. video: `16:9` (default), `9:16`, `1:1`, `4:3`, `3:4` |
| `size` | image | `1K` (default), `1.5K`, `2K` |
| `seconds` | video | 1–5, default 5 |
| `resolution` | video, talk | video defaults to `720P` (1280×704), talk to `480P`; `480P` is 832×480 (16:9) |
| `negative` | video | things that should not appear; defaults to the official Wan template's negative prompt |
| `steps` | all | advanced: text to image 8, edit 4, video 20 by default |
| `seed` | all | random if omitted; the seed actually used goes into `results.json`; fix it to reproduce |
| `timeout` | video, talk | wait limit per job in seconds; video 2400, talk 3600 by default |
| `extend` | video | `@<id>` or a video file: start from its last frame and append the result to it (no `inputs` allowed). `"join": false` returns only the new clip |
| `voice` | tts | voice description (gender, age, tone) |
| `voices` | tts | 1 reference recording (voice clone); `voice_text` can hold what it says, which makes the clone closer |
| `language` | tts | default `Chinese` |
| `audio` | talk | a speech file or `@<tts id>` |
| `trim_to_audio` | talk | default `true`: cut the frames left after the speech ends |

Talking-video example:
```json
{"id": "line01", "type": "tts", "prompt": "大家好，很高興認識你。", "voice": "溫和的中年男性，語速適中，親切"},
{"id": "say01", "type": "talk", "inputs": ["inputs/me.png"], "audio": "@line01",
 "prompt": "A friendly man facing the camera introduces himself, natural head movement and hand gestures"},
{"id": "walk01", "type": "video", "extend": "@say01", "seconds": 5, "resolution": "480P", "aspect": "3:4",
 "prompt": "He walks happily to the right, then turns his head to the camera and waves"}
```

Batch level: `gpu` (`L4`, `G4`, `A100`, `H100`), `stop_on_error`, `tier` (force `high` / `low`; usually leave it out).

## Order within a batch and `@id`
Jobs in a batch run in order. `inputs` can contain `@<id>`, meaning "**the result of that earlier job in this batch**",
e.g. make the picture `frame01` first, then let `shot01` use `"inputs": ["@frame01"]`.
The referenced job must come earlier and succeed, otherwise this job fails (the others still run).

## Resuming
A job is skipped when `out/` already has a file with its id, and jobs that reference it use that file. Add `--force` to redo.
