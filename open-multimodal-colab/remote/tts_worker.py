# -*- coding: utf-8 -*-
"""Runs in its own venv (qwen-tts pins its own transformers): one Qwen3-TTS line to a .wav file.

  python tts_worker.py <job.json> <out.wav>

job.json: {"text": ..., "language": "Chinese", "voice": "<description>"}            -> VoiceDesign model
          {"text": ..., "language": "Chinese", "ref_audio": path, "ref_text": ...}  -> Base model, clones the voice
"""
import json
import sys

import soundfile as sf
import torch
from qwen_tts import Qwen3TTSModel


def main():
    job = json.load(open(sys.argv[1], encoding="utf-8"))
    out = sys.argv[2]
    clone = bool(job.get("ref_audio"))
    model = Qwen3TTSModel.from_pretrained(job["model"], device_map="cuda:0", dtype=torch.bfloat16)
    lang = job.get("language") or "Chinese"
    if clone:
        wavs, sr = model.generate_voice_clone(text=job["text"], language=lang, ref_audio=job["ref_audio"],
                                              ref_text=job.get("ref_text") or None,
                                              x_vector_only_mode=not job.get("ref_text"))
    else:
        wavs, sr = model.generate_voice_design(text=job["text"], language=lang, instruct=job.get("voice") or "")
    sf.write(out, wavs[0], sr)
    print(json.dumps({"seconds": round(len(wavs[0]) / sr, 2), "sample_rate": sr}))


if __name__ == "__main__":
    main()
