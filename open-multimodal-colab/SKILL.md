---
name: open-multimodal-colab
description: Generate pictures, edit pictures, make short videos, voice-overs and talking-head videos with open models whose licenses need no attribution on the output (Z-Image-Turbo, FLUX.2 klein 4B, Wan 2.2, Qwen3-TTS), on the user's own Google Colab GPU driven from this computer through google-colab-cli, or on their own ComfyUI Desktop (local mode, 12 GB VRAM and up). Use when the user asks to 生圖／改圖／生成影片／圖生影片／配音／說話影片／把分鏡生出來, or wants storyboard frames, clips, voice-overs or talking videos made, including when you yourself have no image or video tool.
---

**English** | [繁體中文](SKILL.zh-TW.md)

# Open multimodal generation (Colab GPU or local ComfyUI)

On the user's own GPU, generate with open models whose licenses are clean (Apache 2.0, no model name required on the output):

| Type | What it does | Model |
|---|---|---|
| `image` (no `inputs`) | text to image; can draw English and Chinese text | Z-Image-Turbo (6B, 8 steps) |
| `image` (with `inputs`) | edit or combine 1–4 images (change colors, change clothes, put a person into a scene) | FLUX.2 [klein] 4B |
| `video` | text to video, or one image as the first frame; 1–5 s, 24 fps, **no sound** | Wan 2.2 TI2V-5B |
| `video` + `extend` | continue from the last frame of an earlier clip; the result is joined to that clip automatically | Wan 2.2 TI2V-5B |
| `tts` | voice-over: design a voice from a text description, or clone a voice from a recording | Qwen3-TTS 1.7B |
| `talk` | talking video: one image plus speech, lips matched to the audio, length follows the speech | Wan 2.2 S2V-14B (**high tier only**) |

You (the language model) **understand the request, write the prompts, build the job list and check the results**; generation runs on Colab or on the local ComfyUI.
Music will be added in a later version.

Talk to the user in their own language (for Chinese-speaking users, Traditional Chinese).

---

## 0. First use: ask where to run

**First ask the user**: "Run on Google Colab, or on ComfyUI Desktop on your own computer (local)?"
- Local needs: an NVIDIA graphics card with **10 GB or more** of VRAM (an RTX 3060 12 GB works), 32 GB of system RAM recommended, about 35 GB of disk.
  ComfyUI Desktop must already be installed and open (https://comfy.org/download).
- No answer, or no suitable graphics card → **Colab**.
- Remember the choice and use it for later batches.

### VRAM tiers (detected automatically)
| Tier | VRAM | Versions used |
|---|---|---|
| `high` | 20 GB or more (Colab L4, G4, 24 GB cards) | Z-Image bf16, Wan 2.2 5B fp16 |
| `low` | 10–19 GB (RTX 3060 12 GB and similar) | Z-Image int8, Wan 2.2 5B GGUF Q8 (needs the ComfyUI-GGUF nodes; `setup` installs them) |

### Local mode (ComfyUI Desktop)
```
python scripts/omlocal.py check                # is ComfyUI open, VRAM tier, which models and nodes are missing
python scripts/omlocal.py setup                # first time: download missing models, install needed node packs
python scripts/omlocal.py run omcjob/manifest.json [--confirmed]
```
- Only some features: `--features t2i,video` (choose from `t2i`, `edit`, `video`) to download less.
- Models go to `~/ComfyUI-Shared/models` (ComfyUI Desktop's default); add `--models-dir` if they live elsewhere.
- When `setup` installs new nodes, follow the commands it prints to install the node packages, ask the user to **restart ComfyUI Desktop**, then `check` again.
- A portable ComfyUI that cannot report its location: add `--comfy-dir <ComfyUI folder>`.
- To force a tier when detection is wrong: `--tier high` or `--tier low`.
- Follow the flow in section 1 below, except step 6 becomes `omlocal.py run` and step 8 does not ask about keeping a GPU.

### Colab mode: explain first, then install

If `python scripts/omrun.py check` cannot find colab or is not logged in, **stop first** and explain these five things in the user's language; only start after they say yes:

1. **What happens**: a Colab GPU is started on the user's Google account, ComfyUI and the models are installed there, the files are downloaded back to this computer after generation, and then **that GPU is shut down**.
2. **Subscription**: at least **Google AI Pro** (it includes Colab compute units). Plus is not enough.
3. **Cost**: L4 about 1.5 units per hour, G4 about 11 units per hour. Every boot installs the environment and downloads models first (only what the batch needs: about 18 GB for text to image, 13 GB for editing, 18 GB for video, 26 GB for talking video).
   Measured on L4: editing 4 images including boot took about 4.4 minutes and 0.08 units; voice-over plus a 14 s talking video plus a 5 s extension takes about 19 minutes and 0.55 units when nothing fails.
4. **What is downloaded from where**: ComfyUI from GitHub; model files from Comfy-Org, Black Forest Labs and QuantStack on Hugging Face. **Everything is downloaded on Colab and takes no space on this computer.**
5. **When to log in**: only the first time. You give them a Google link; they sign in with **the AI Pro account**, click Allow and paste the code shown back into the conversation.

Install: follow the repo's `INSTALL_FOR_AGENTS.md`. Log in:
```
python scripts/colab_login.py url          # give the link to the user
python scripts/colab_login.py code <CODE>  # after they paste it back
python scripts/omrun.py check              # seeing the remaining compute units = success
```

---

## 1. The flow for each generation

1. **Find out what is wanted**: how many pictures, how many clips, whose face, what aspect ratio.
2. **Prepare the input files**: put character photos and scene images in a working folder, e.g. `omcjob/inputs/`.
3. **Write the prompts**: follow `references/prompt-guide.md`.
4. **Write `manifest.json`**: format in `references/manifest.md`. Send the whole batch at once; don't boot once per item.
5. **Confirm the specs**:
   - **For two or more videos, always confirm the specs with the user first**: resolution (480P / 720P), portrait or landscape, seconds per clip.
     Without `--confirmed` nothing boots; it first prints a summary of the batch for the user to review, then add `--confirmed`.
   - Video defaults to 720P (the resolution Wan 2.2 5B was trained at). 480P is faster, but its quality has not been tested.
   - For the first batch, try one picture and one 3-second clip so the user sees the real time.
   - Measured on L4: 9–12 s per edited image; a talking video takes about 32 s per second of output (7.7 minutes for 14.5 s); a 5 s extension about 3.3 minutes.
6. **Send it**:
   ```
   python scripts/omrun.py run omcjob/manifest.json --gpu L4
   ```
   It boots → uploads → generates in the background → reports every 30 s → downloads each result to `omcjob/out/` as it finishes.
7. **Check the results**: open the pictures; sample at least a few frames of each video; if something is wrong, redo only that one (change the prompt or the seed).
8. **Report, and ask whether to keep the GPU**: each file's path, how long it took, which seed was used (in `out/results.json`).
   After finishing, the GPU is **kept for 15 minutes** (the models are still on it). Always ask:
   "Do you want to generate or change anything else? If so I'll keep the GPU (L4 costs about 1.5 units an hour); if not I'll shut it down now."
   - Continue → add `--session <name>` to the next batch; no model download needed
   - Keep it longer → `python scripts/omrun.py keep --session <name> --minutes 60` (at most 240)
   - Done → `python scripts/omrun.py stop --session <name>`
   - No answer is fine: an independent local timer shuts it down after 15 minutes without new work.
   - Certain it's a one-off: add `--stop-after` in step 6. Failed or interrupted batches always shut down immediately.

---

## 2. Job rules

### Images
- No `inputs` → text to image. `size`: `1K` (default), `1.5K`, `2K` (long edge in pixels); `aspect` defaults to `1:1`.
- With `inputs` → edit. Image 1 is **the one being changed**, the rest are references, at most 4. `aspect: "auto"` (default) keeps image 1's ratio.
- In prompts, refer to the order of `inputs` as "image 1", "image 2".

### Video
- No `inputs` → text to video; 1 image in `inputs` → that image is the first frame (center-cropped to the video ratio).
- `seconds`: 1–5 (a Wan 2.2 clip is about 5 s). For longer footage, use `extend` to continue after the previous clip.
- `aspect`: `16:9` (default), `9:16`, `1:1`, `4:3`, `3:4`.
- Video has **no sound**.
- Storyboard flow: make the frames with `image` first, then animate them with `video` using `"inputs": ["@<image id>"]`, all in one boot.

### Voice-over and talking video
- The `tts` `prompt` is the line to speak; `voice` is the voice description and **must state gender and age** (e.g. "溫和的中年男性，語速適中，親切", a warm middle-aged man, moderate pace, friendly).
  To clone someone's voice, put a recording in `voices` (1 clip, 3 s or longer); **only use the user's own voice or one whose owner has agreed**.
- Mandarin lines run at about 3.4 characters per second (measured: 48 characters in 14.2 s). For a 5 s talking video, keep the line to about 15–17 characters. A talking video is as long as its speech (one chunk per 4.8 s, trimmed to where the speech ends).
- `talk` takes the voice-over with `"audio": "@<tts id>"` and 1 portrait in `inputs`. Defaults to 480P, 3:4. The 14B model only runs on Colab (high tier).
- To add motion after a talking video: the next `video` uses `"extend": "@<talk id>"`, and the result is both clips joined (the extension has no sound).

---

## 3. When something fails

Read `references/troubleshooting.md` first. Most common:
- Not logged in / token expired → rerun `colab_login.py url`.
- Not enough units or no GPU assigned → use L4 or try later; **do not** switch to A100 (very expensive).
- One job failed → read its error in `out/results.json` and resend only that job (`--session` reuses a machine that is still running).
- Not enough local VRAM (`out of memory`) → use 480P, shorten the clip, or `--tier low`.

Licenses: see `references/licenses.md`.
