**English** | [繁體中文](README.zh-TW.md)

# open-multimodal-colab

A skill that lets an AI agent (Claude Code, Codex and others) generate and edit pictures, make short videos, voice-overs and talking-head videos on **your own GPU**.
It only uses open models with clean licenses (Apache 2.0, no model name required on what you make). It runs on Google Colab or on ComfyUI Desktop on your own computer.

This project is adapted from [dseditor/h3-colab-skill](https://github.com/dseditor/h3-colab-skill) (MIT) and replaces MiniMax H3 with other models, because the MiniMax H3 license requires commercial products to show the model's name.

## Features

| Feature | Model | Colab L4 (24 GB) | Local 12 GB (RTX 3060) |
|---|---|---|---|
| Text to image | Z-Image-Turbo | bf16 | int8 |
| Image editing (1–4 reference images) | FLUX.2 [klein] 4B | fp8 | fp8 |
| Text or image to video (1–5 s, silent) | Wan 2.2 TI2V-5B | fp16 | GGUF Q8 |
| Video extension (continues an earlier clip) | Wan 2.2 TI2V-5B | fp16 | GGUF Q8 |
| Voice-over (designed voice or voice clone) | Qwen3-TTS 1.7B | bf16 | bf16 (not tested) |
| Talking video (image + speech) | Wan 2.2 S2V-14B | fp8 + 4-step LoRA | not supported |

The VRAM tier is detected automatically; see [models.py](open-multimodal-colab/remote/models.py). The 12 GB settings are estimated from file sizes and have not been tested yet.

## Measured results (2026-11-06, Colab L4)

| Work | Time | Compute units |
|---|---|---|
| Boot, install ComfyUI, download the edit model | about 3.7 min | about 0.07 |
| Image edit (pose, outfit and background in one prompt), per image | 9–12 s | about 0.004 |
| 14.2 s voice-over (includes the first TTS setup) | 83 s | about 0.04 |
| Boot, download the talking-video and video models (about 26 GB) | about 6 min | about 0.18 |
| 14.5 s talking video (544×736) | 7.7 min | about 0.24 |
| 5 s video extension | 3.3 min | about 0.10 |

L4 costs about 0.03 units per minute. Per-item units are estimates split by GPU time, because Colab only shows the total for a batch. Editing 4 images took 4.4 min and 0.08 units including boot; voice-over plus talking video plus extension takes about 19 min and 0.55 units when nothing fails.

Observations:
- Image editing keeps the face, glasses and art style.
- Mandarin speech runs at about 3.4 characters per second. A talking video is as long as its speech, so shorten the line for a shorter clip.
- Extension produced the wave and the smile, but ordered actions such as "walk, then turn the head" are not always followed.

## Not done yet

- Music (ACE-Step 1.5)
- A real test on a 12 GB local GPU (RTX 3060)
- The license of the original weights of the wav2vec2 audio encoder used for talking video

## Install

Give your agent [INSTALL_FOR_AGENTS.md](INSTALL_FOR_AGENTS.md). To install by hand:

- Windows: `powershell -ExecutionPolicy Bypass -File install\install.ps1`
- macOS / Linux: `bash install/install.sh`

Colab mode needs Google AI Pro. Local mode needs [ComfyUI Desktop](https://comfy.org/download) installed first, then:

```
python open-multimodal-colab/scripts/omlocal.py check
python open-multimodal-colab/scripts/omlocal.py setup
```

## Usage

The agent follows [SKILL.md](open-multimodal-colab/SKILL.md) to write a `manifest.json` (format in [manifest.md](open-multimodal-colab/references/manifest.md)) and runs:

```
python open-multimodal-colab/scripts/omrun.py run omcjob/manifest.json --gpu L4    # Colab
python open-multimodal-colab/scripts/omlocal.py run omcjob/manifest.json           # local
```

## Tests

```
python tests/test_offline.py                       # no GPU needed
python tests/validate_graphs.py --url http://127.0.0.1:8188   # let ComfyUI validate every workflow
```

`validate_graphs.py` only needs a ComfyUI (CPU is fine), empty placeholder model files and the ComfyUI-GGUF nodes. It does not generate anything.

## License

Code: MIT ([LICENSE](LICENSE)). Third-party code sources are in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md); model licenses are in [licenses.md](open-multimodal-colab/references/licenses.md).
