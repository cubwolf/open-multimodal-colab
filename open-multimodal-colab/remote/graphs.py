# -*- coding: utf-8 -*-
"""ComfyUI API-format graphs, built from the official ComfyUI templates (Comfy-Org/workflow_templates):
  t2i    image_z_image_turbo.json / image_z_image_turbo_int8.json
  edit   image_flux2_klein_image_edit_4b_distilled.json (reference chain extended to 1-4 pictures)
  video  video_wan2_2_5B_ti2v.json
Only core ComfyUI nodes, plus UnetLoaderGGUF (ComfyUI-GGUF) when the video model is a .gguf file.

Each builder returns (graph, output_node_id). Model file names come from models.py.
"""
import os

import models as M

ASPECTS = {"1:1": (1, 1), "16:9": (16, 9), "9:16": (9, 16), "4:3": (4, 3), "3:4": (3, 4), "3:2": (3, 2),
           "2:3": (2, 3), "21:9": (21, 9)}
IMAGE_SIZES = {"1K": 1024, "1.5K": 1536, "2K": 2048}  # long edge
# Wan 2.2 TI2V-5B is trained at 1280x704; 480P is faster but untested for quality
VIDEO_SIZES = {
    "720P": {"16:9": (1280, 704), "9:16": (704, 1280), "1:1": (960, 960), "4:3": (1088, 832), "3:4": (832, 1088)},
    "480P": {"16:9": (832, 480), "9:16": (480, 832), "1:1": (640, 640), "4:3": (736, 544), "3:4": (544, 736)},
}
VIDEO_FPS = 24
MAX_VIDEO_SECONDS = 5
WAN_NEGATIVE = ("色调艳丽，过曝，静态，细节模糊不清，字幕，风格，作品，画作，画面，静止，整体发灰，最差质量，低质量，JPEG压缩残留，"
                "丑陋的，残缺的，多余的手指，画得不好的手部，画得不好的脸部，畸形的，毁容的，形态畸形的肢体，手指融合，"
                "静止不动的画面，杂乱的背景，三条腿，背景人很多，倒着走")


def seed_of(job):
    return int(job["seed"]) if job.get("seed") is not None else int.from_bytes(os.urandom(6), "big")


def image_dims(aspect, size):
    a, b = ASPECTS.get(aspect or "1:1", (1, 1))
    edge = IMAGE_SIZES[size or "1K"]
    w, h = (edge, edge * b / a) if a >= b else (edge * a / b, edge)
    return int(round(w / 16)) * 16, int(round(h / 16)) * 16


def video_frames(seconds):
    n = int(round(float(seconds) * VIDEO_FPS))
    return n - n % 4 + 1  # Wan wants 4k+1 frames


def _unet(models, key):
    fname = M.name(models["unet"])
    if fname.endswith(".gguf"):
        return {"class_type": "UnetLoaderGGUF", "inputs": {"unet_name": fname}}
    return {"class_type": "UNETLoader", "inputs": {"unet_name": fname, "weight_dtype": "default"}}


def t2i(job, models):
    w, h = image_dims(job.get("aspect"), job.get("size"))
    g = {
        "unet": _unet(models, "unet"),
        "clip": {"class_type": "CLIPLoader", "inputs": {"clip_name": M.name(models["clip"]), "type": "lumina2", "device": "default"}},
        "vae": {"class_type": "VAELoader", "inputs": {"vae_name": M.name(models["vae"])}},
        "shift": {"class_type": "ModelSamplingAuraFlow", "inputs": {"model": ["unet", 0], "shift": 3}},
        "pos": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["clip", 0], "text": job["prompt"]}},
        "neg": {"class_type": "ConditioningZeroOut", "inputs": {"conditioning": ["pos", 0]}},
        "latent": {"class_type": "EmptySD3LatentImage", "inputs": {"width": w, "height": h, "batch_size": 1}},
        "sample": {"class_type": "KSampler", "inputs": {
            "model": ["shift", 0], "positive": ["pos", 0], "negative": ["neg", 0], "latent_image": ["latent", 0],
            "seed": seed_of(job), "steps": int(job.get("steps", 8)), "cfg": 1.0,
            "sampler_name": "res_multistep", "scheduler": "simple", "denoise": 1.0}},
        "decode": {"class_type": "VAEDecode", "inputs": {"samples": ["sample", 0], "vae": ["vae", 0]}},
        "save": {"class_type": "SaveImage", "inputs": {"images": ["decode", 0], "filename_prefix": f"omc/{job['id']}"}},
    }
    return g, "save"


def edit(job, models, input_names):
    """input_names: file names already in ComfyUI's input folder, in order (<Picture 1> first)."""
    megapixels = {"1K": 1.0, "1.5K": 2.25, "2K": 4.0}[job.get("size") or "1K"]
    g = {
        "unet": _unet(models, "unet"),
        "clip": {"class_type": "CLIPLoader", "inputs": {"clip_name": M.name(models["clip"]), "type": "flux2", "device": "default"}},
        "vae": {"class_type": "VAELoader", "inputs": {"vae_name": M.name(models["vae"])}},
        "pos0": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["clip", 0], "text": job["prompt"]}},
        "neg0": {"class_type": "ConditioningZeroOut", "inputs": {"conditioning": ["pos0", 0]}},
    }
    pos, neg = "pos0", "neg0"
    for k, fname in enumerate(input_names):
        g[f"load{k}"] = {"class_type": "LoadImage", "inputs": {"image": fname}}
        g[f"scale{k}"] = {"class_type": "ImageScaleToTotalPixels", "inputs": {
            "image": [f"load{k}", 0], "upscale_method": "nearest-exact", "megapixels": megapixels, "resolution_steps": 1}}
        g[f"enc{k}"] = {"class_type": "VAEEncode", "inputs": {"pixels": [f"scale{k}", 0], "vae": ["vae", 0]}}
        g[f"pos{k + 1}"] = {"class_type": "ReferenceLatent", "inputs": {"conditioning": [pos, 0], "latent": [f"enc{k}", 0]}}
        g[f"neg{k + 1}"] = {"class_type": "ReferenceLatent", "inputs": {"conditioning": [neg, 0], "latent": [f"enc{k}", 0]}}
        pos, neg = f"pos{k + 1}", f"neg{k + 1}"
    if (job.get("aspect") or "auto") == "auto":  # output takes the size of <Picture 1>
        g["size"] = {"class_type": "GetImageSize", "inputs": {"image": ["scale0", 0]}}
        w, h = ["size", 0], ["size", 1]
    else:
        a, b = ASPECTS[job["aspect"]]
        side = (megapixels * 1024 * 1024 / (a * b)) ** 0.5
        w, h = int(round(side * a / 16)) * 16, int(round(side * b / 16)) * 16
    steps = int(job.get("steps", 4))
    g.update({
        "latent": {"class_type": "EmptyFlux2LatentImage", "inputs": {"width": w, "height": h, "batch_size": 1}},
        "sched": {"class_type": "Flux2Scheduler", "inputs": {"steps": steps, "width": w, "height": h}},
        "guider": {"class_type": "CFGGuider", "inputs": {"model": ["unet", 0], "positive": [pos, 0], "negative": [neg, 0], "cfg": 1.0}},
        "sampler": {"class_type": "KSamplerSelect", "inputs": {"sampler_name": "euler"}},
        "noise": {"class_type": "RandomNoise", "inputs": {"noise_seed": seed_of(job)}},
        "sample": {"class_type": "SamplerCustomAdvanced", "inputs": {
            "noise": ["noise", 0], "guider": ["guider", 0], "sampler": ["sampler", 0], "sigmas": ["sched", 0],
            "latent_image": ["latent", 0]}},
        "decode": {"class_type": "VAEDecode", "inputs": {"samples": ["sample", 0], "vae": ["vae", 0]}},
        "save": {"class_type": "SaveImage", "inputs": {"images": ["decode", 0], "filename_prefix": f"omc/{job['id']}"}},
    })
    return g, "save"


def video(job, models, start_name=None):
    """Text to video, or picture to video when start_name (a file in ComfyUI's input folder) is given."""
    res = job.get("resolution") or "720P"
    w, h = VIDEO_SIZES[res][job.get("aspect") or "16:9"]
    g = {
        "unet": _unet(models, "unet"),
        "clip": {"class_type": "CLIPLoader", "inputs": {"clip_name": M.name(models["clip"]), "type": "wan", "device": "default"}},
        "vae": {"class_type": "VAELoader", "inputs": {"vae_name": M.name(models["vae"])}},
        "shift": {"class_type": "ModelSamplingSD3", "inputs": {"model": ["unet", 0], "shift": 8}},
        "pos": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["clip", 0], "text": job["prompt"]}},
        "neg": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["clip", 0], "text": job.get("negative") or WAN_NEGATIVE}},
        "latent": {"class_type": "Wan22ImageToVideoLatent", "inputs": {
            "vae": ["vae", 0], "width": w, "height": h, "length": video_frames(job.get("seconds", 5)), "batch_size": 1}},
        "sample": {"class_type": "KSampler", "inputs": {
            "model": ["shift", 0], "positive": ["pos", 0], "negative": ["neg", 0], "latent_image": ["latent", 0],
            "seed": seed_of(job), "steps": int(job.get("steps", 20)), "cfg": 5.0,
            "sampler_name": "uni_pc", "scheduler": "simple", "denoise": 1.0}},
        "decode": {"class_type": "VAEDecode", "inputs": {"samples": ["sample", 0], "vae": ["vae", 0]}},
        "create": {"class_type": "CreateVideo", "inputs": {"images": ["decode", 0], "fps": float(VIDEO_FPS)}},
        "save": {"class_type": "SaveVideo", "inputs": {"video": ["create", 0], "filename_prefix": f"omc/{job['id']}",
                                                       "format": "mp4", "format.codec": "h264"}},
    }
    if start_name:  # crop the picture to the video frame so it is not stretched
        g["load"] = {"class_type": "LoadImage", "inputs": {"image": start_name}}
        g["fit"] = {"class_type": "ImageScale", "inputs": {"image": ["load", 0], "upscale_method": "lanczos",
                                                           "width": w, "height": h, "crop": "center"}}
        g["latent"]["inputs"]["start_image"] = ["fit", 0]
    return g, "save"
