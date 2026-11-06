# -*- coding: utf-8 -*-
"""Which model files each feature needs, per VRAM tier.

Two tiers:
  high  >= 20 GB VRAM (Colab L4 24 GB, G4, A100, a local 24 GB card): bf16 / fp16 weights
  low   10-19 GB VRAM (e.g. RTX 3060 12 GB): int8 / GGUF weights; ComfyUI moves text encoders to system RAM

Every model here is Apache 2.0 (see references/licenses.md). Sizes are what Hugging Face shows.
"""

# key: (Hugging Face repo, file in repo, ComfyUI models/ subfolder, size GB)
FILES = {
    # Z-Image-Turbo (text to image) - Tongyi-MAI, Apache 2.0
    "zimage_bf16": ("Comfy-Org/z_image_turbo", "split_files/diffusion_models/z_image_turbo_bf16.safetensors", "diffusion_models", 12.3),
    "zimage_int8": ("Comfy-Org/z_image_turbo", "split_files/diffusion_models/z_image_turbo_int8_convrot.safetensors", "diffusion_models", 6.2),
    "qwen3_4b": ("Comfy-Org/z_image_turbo", "split_files/text_encoders/qwen_3_4b.safetensors", "text_encoders", 8.0),
    "qwen3_4b_fp8": ("Comfy-Org/z_image_turbo", "split_files/text_encoders/qwen_3_4b_fp8_mixed.safetensors", "text_encoders", 5.6),
    "zimage_vae": ("Comfy-Org/z_image_turbo", "split_files/vae/ae.safetensors", "vae", 0.3),
    # FLUX.2 [klein] 4B distilled (image edit, 1-4 reference pictures) - Black Forest Labs, Apache 2.0 (4B only)
    "klein4b_fp8": ("black-forest-labs/FLUX.2-klein-4b-fp8", "flux-2-klein-4b-fp8.safetensors", "diffusion_models", 4.0),
    "flux2_vae": ("Comfy-Org/Flux-2-Klein-4B", "split_files/vae/flux2-vae.safetensors", "vae", 0.3),  # apache-2.0 repo
    # Wan 2.2 TI2V-5B (text or picture to video, 24 fps) - Wan-AI, Apache 2.0
    "wan5b_fp16": ("Comfy-Org/Wan_2.2_ComfyUI_Repackaged", "split_files/diffusion_models/wan2.2_ti2v_5B_fp16.safetensors", "diffusion_models", 10.0),
    "wan5b_q8": ("QuantStack/Wan2.2-TI2V-5B-GGUF", "Wan2.2-TI2V-5B-Q8_0.gguf", "diffusion_models", 5.4),
    "umt5_fp8": ("Comfy-Org/Wan_2.1_ComfyUI_repackaged", "split_files/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors", "text_encoders", 6.7),
    "wan22_vae": ("Comfy-Org/Wan_2.2_ComfyUI_Repackaged", "split_files/vae/wan2.2_vae.safetensors", "vae", 1.4),
    # Wan 2.2 S2V-14B (talking video: a picture + speech) - Wan-AI, Apache 2.0. 4-step lightx2v LoRA as in the template
    "s2v_fp8": ("Comfy-Org/Wan_2.2_ComfyUI_Repackaged", "split_files/diffusion_models/wan2.2_s2v_14B_fp8_scaled.safetensors", "diffusion_models", 16.4),
    "lightx2v_t2v_high": ("Comfy-Org/Wan_2.2_ComfyUI_Repackaged", "split_files/loras/wan2.2_t2v_lightx2v_4steps_lora_v1.1_high_noise.safetensors", "loras", 1.2),
    "wan21_vae": ("Comfy-Org/Wan_2.2_ComfyUI_Repackaged", "split_files/vae/wan_2.1_vae.safetensors", "vae", 0.3),
    "wav2vec2": ("Comfy-Org/Wan_2.2_ComfyUI_Repackaged", "split_files/audio_encoders/wav2vec2_large_english_fp16.safetensors", "audio_encoders", 0.6),
}

# Qwen3-TTS (Alibaba Qwen, Apache 2.0) runs outside ComfyUI with the qwen-tts package in its own venv;
# the weights are fetched by the package from these Hugging Face repos
TTS_MODELS = {"design": "Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign", "clone": "Qwen/Qwen3-TTS-12Hz-1.7B-Base"}
TTS_PACKAGE = "qwen-tts==0.1.1"
TTS_DEPS = ["librosa", "soundfile", "sox", "onnxruntime", "einops", "huggingface_hub>=0.34,<1.0", "tokenizers>=0.22,<=0.23.0",
            "safetensors", "regex"]
TTS_NODEPS = [TTS_PACKAGE, "transformers==4.57.3", "accelerate==1.12.0"]  # torch comes from the system

# feature -> tier -> {role: file key}
FEATURES = {
    "t2i": {
        "high": {"unet": "zimage_bf16", "clip": "qwen3_4b_fp8", "vae": "zimage_vae"},
        "low": {"unet": "zimage_int8", "clip": "qwen3_4b_fp8", "vae": "zimage_vae"},
    },
    "edit": {
        "high": {"unet": "klein4b_fp8", "clip": "qwen3_4b", "vae": "flux2_vae"},
        "low": {"unet": "klein4b_fp8", "clip": "qwen3_4b_fp8", "vae": "flux2_vae"},
    },
    "video": {
        "high": {"unet": "wan5b_fp16", "clip": "umt5_fp8", "vae": "wan22_vae"},
        "low": {"unet": "wan5b_q8", "clip": "umt5_fp8", "vae": "wan22_vae"},
    },
    "talk": {  # 14B: high tier only (no 12 GB version yet)
        "high": {"unet": "s2v_fp8", "lora": "lightx2v_t2v_high", "clip": "umt5_fp8", "vae": "wan21_vae", "audio": "wav2vec2"},
    },
    "tts": {"high": {}, "low": {}},  # no ComfyUI files: see TTS_MODELS
}

# custom node packs a tier needs: name -> (git url, pinned commit)
NODES = {
    "low": {"ComfyUI-GGUF": ("https://github.com/city96/ComfyUI-GGUF", "6ea2651e7df66d7585f6ffee804b20e92fb38b8a")},
    "high": {},
}

# ComfyUI version the workflows were validated against
COMFY_COMMIT = "52a20aa7707d859946d1f2adbaacca31f3df6239"


def tier_for(vram_gb):
    if vram_gb >= 20:
        return "high"
    if vram_gb >= 10:
        return "low"
    raise RuntimeError(f"{vram_gb:.0f} GB VRAM is below the 10 GB minimum")


def feature_of(job):
    if job["type"] == "image":
        return "edit" if job.get("inputs") else "t2i"
    return job["type"]


def check_tier(features, tier):
    missing = [f for f in features if tier not in FEATURES[f]]
    if missing:
        raise RuntimeError(f"{', '.join(missing)} needs the high tier (20 GB VRAM or more); use Colab L4 or bigger")


def files_for(features, tier):
    check_tier(features, tier)
    keys = []
    for f in features:
        for k in FEATURES[f][tier].values():
            if k not in keys:
                keys.append(k)
    return [FILES[k] for k in keys]


def name(key):
    return FILES[key][1].rsplit("/", 1)[-1]
