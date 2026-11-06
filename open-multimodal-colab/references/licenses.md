**English** | [繁體中文](licenses.zh-TW.md)

# Licenses

This skill only downloads models whose licenses do not require the model name on what you make. The full research is in the project's license investigation document; this is the summary.

| Model | Used for | License | Credit needed on outputs? |
|---|---|---|---|
| Z-Image-Turbo (Tongyi-MAI) | text to image | Apache 2.0 | no |
| Qwen3-4B text encoder | shared by Z-Image and FLUX.2 klein | Apache 2.0 | no |
| FLUX.2 [klein] 4B (Black Forest Labs) | image editing | Apache 2.0 (**4B only**; 9B and [dev] are non-commercial and must not be swapped in) | no (but do not misuse the BFL / FLUX trademarks) |
| Wan 2.2 TI2V-5B (Wan-AI) | video | Apache 2.0; claims no rights over generated content | no |
| UMT5-XXL text encoder | Wan 2.2 | Apache 2.0 | no |
| Wan 2.2 S2V-14B (Wan-AI) | talking video | Apache 2.0; claims no rights over generated content | no |
| Wan2.2-Lightning (lightx2v 4-step LoRA) | faster talking video | Apache 2.0 | no |
| Qwen3-TTS 1.7B (Alibaba Qwen) | voice-over | Apache 2.0 | no |
| wav2vec2 large english (audio encoder) | talking video | to be verified (repackaged by Comfy-Org; source of the original weights not confirmed) | — |

Only clone your own voice or a voice whose owner has agreed.

Apache 2.0 obligations apply only when you **distribute the model or the code itself** (include the license and NOTICE). Pictures and videos you generate need no credit.

## Licenses of the download sources
- The FLUX.2 VAE (`flux2-vae.safetensors`) is downloaded from `Comfy-Org/Flux-2-Klein-4B`, which is marked apache-2.0; BFL's official README also states the autoencoder is released under Apache 2.0.
  Do not download it from `Comfy-Org/flux2-dev` instead: that repo is marked with the non-commercial license.
- `black-forest-labs/FLUX.2-klein-4b-fp8` is marked apache-2.0 and has no access gate (checked 2026-11-06).

## This program
- The code in this repo: MIT (see `LICENSE`).
- The orchestration is adapted from dseditor/h3-colab-skill (MIT) and the login flow follows google-colab-cli (Apache 2.0); see `THIRD_PARTY_NOTICES.md`.
- ComfyUI (GPL-3.0) and ComfyUI-GGUF (Apache 2.0) are downloaded and run separately on Colab or on the user's computer and are not included in this repo.
