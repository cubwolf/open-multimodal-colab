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
}

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


def files_for(features, tier):
    keys = []
    for f in features:
        for k in FEATURES[f][tier].values():
            if k not in keys:
                keys.append(k)
    return [FILES[k] for k in keys]


def name(key):
    return FILES[key][1].rsplit("/", 1)[-1]
