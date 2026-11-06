**English** | [繁體中文](licenses.zh-TW.md)

# Licenses

This skill only downloads models whose licenses do not require the model name on what you make. The license of every download source was checked on its Hugging Face page on 2026-11-06; see "Download sources" below.

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
| wav2vec2-large-xlsr-53-english (audio encoder) | talking video | Apache 2.0 (Jonatas Grosman's fine-tune of Meta's wav2vec2-large-xlsr-53, also Apache 2.0, trained on Common Voice, CC0) | no |

Only clone your own voice or a voice whose owner has agreed.

Apache 2.0 obligations apply only when you **distribute the model or the code itself** (include the license and NOTICE). Pictures and videos you generate need no credit.

## Download sources

| Files | Downloaded from | License on that page |
|---|---|---|
| Z-Image-Turbo bf16 / int8, Qwen3-4B encoder, Z-Image VAE | `Comfy-Org/z_image_turbo` (original: `Tongyi-MAI/Z-Image-Turbo`) | apache-2.0 |
| FLUX.2 klein 4B fp8 | `black-forest-labs/FLUX.2-klein-4b-fp8` | apache-2.0, not gated |
| FLUX.2 VAE | `Comfy-Org/Flux-2-Klein-4B` | apache-2.0 |
| Wan 2.2 TI2V-5B fp16, Wan 2.2 / 2.1 VAE, S2V-14B fp8, Lightning LoRA, wav2vec2 | `Comfy-Org/Wan_2.2_ComfyUI_Repackaged` (now redirects to `Comfy-Org/Wan-2.2`; originals: `Wan-AI/Wan2.2-TI2V-5B`, `Wan-AI/Wan2.2-S2V-14B`, `lightx2v/Wan2.2-Lightning`) | apache-2.0 |
| Wan 2.2 TI2V-5B GGUF Q8 | `QuantStack/Wan2.2-TI2V-5B-GGUF` | apache-2.0 |
| UMT5-XXL fp8 encoder | `Comfy-Org/Wan_2.1_ComfyUI_repackaged` (now `Comfy-Org/Wan-2.1`) | apache-2.0 |
| Qwen3-TTS 1.7B | `Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign`, `Qwen/Qwen3-TTS-12Hz-1.7B-Base` | apache-2.0 |

About wav2vec2: Wan-AI ships the same encoder inside its official `Wan-AI/Wan2.2-S2V-14B` repo, in the folder `wav2vec2-large-xlsr-53-english/`. Its model card names `jonatasgrosman/wav2vec2-large-xlsr-53-english` with license apache-2.0, and the base model `facebook/wav2vec2-large-xlsr-53` is apache-2.0 too. ComfyUI's `wav2vec2_large_english_fp16.safetensors` is the fp16 repackage of that encoder for ComfyUI (Comfy-Org did not state this file by file; it is inferred from the name, the size and its use in the official S2V template).

Notes on sources:
- The FLUX.2 VAE (`flux2-vae.safetensors`) is downloaded from `Comfy-Org/Flux-2-Klein-4B`, which is marked apache-2.0; BFL's official README also states the autoencoder is released under Apache 2.0.
  Do not download it from `Comfy-Org/flux2-dev` instead: that repo is marked with the non-commercial license.
- `black-forest-labs/FLUX.2-klein-4b-fp8` is marked apache-2.0 and has no access gate (checked 2026-11-06).

## This program
- The code in this repo: MIT (see `LICENSE`).
- The orchestration is adapted from dseditor/h3-colab-skill (MIT) and the login flow follows google-colab-cli (Apache 2.0); see `THIRD_PARTY_NOTICES.md`.
- ComfyUI (GPL-3.0) and ComfyUI-GGUF (Apache 2.0) are downloaded and run separately on Colab or on the user's computer and are not included in this repo.
