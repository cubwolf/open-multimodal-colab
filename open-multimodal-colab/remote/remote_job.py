# -*- coding: utf-8 -*-
# Adapted from dseditor/h3-colab-skill (MIT, Copyright (c) 2026 dseditor (DSLab)); see THIRD_PARTY_NOTICES.md.
"""Runs ON the Colab VM (or, with OMC_LOCAL=1, on this computer against a running ComfyUI).
Started in the background by start.py; progress goes to <job dir>/status.json.

One batch = <job dir>/manifest.json (written by omrun.py / omlocal.py). Steps:
  1 install (skipped when the marker exists): ComfyUI at a pinned commit + the node packs the tier needs
  2 models: only the files the batch's features need, for this GPU's VRAM tier (models.py)
  3 start ComfyUI (127.0.0.1:8188, private to the VM)
  4 every job in order -> <job dir>/out/<id>.<ext>, each one an API graph from graphs.py sent to /prompt
"""
import json
import os
import shutil
import subprocess
import sys
import time
import traceback
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import graphs as G  # noqa: E402
import models as M  # noqa: E402

LOCAL = os.environ.get("OMC_LOCAL") == "1"
JOB = Path(os.environ.get("OMC_DIR", "/content/omcjob"))
OUT = JOB / "out"
STATUS = JOB / "status.json"
COMFY = Path(os.environ.get("OMC_COMFY", "/content/ComfyUI"))
COMFY_URL = os.environ.get("OMC_COMFY_URL", "http://127.0.0.1:8188")
MARK = Path("/content/.omc_setup_v1")
STATE = {"stage": "starting", "log": [], "jobs": {}, "done": False, "error": None, "started": time.time()}


# ---------------------------------------------------------------- status
def save():
    tmp = STATUS.with_suffix(".tmp")
    tmp.write_text(json.dumps(STATE, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(STATUS)


def log(msg, stage=None):
    if stage:
        STATE["stage"] = stage
    line = f"{time.strftime('%H:%M:%S')} {msg}"
    print(line, flush=True)
    STATE["log"] = (STATE["log"] + [line])[-60:]
    save()


def sh(args, **kw):
    subprocess.run(args, check=True, **kw)


# ---------------------------------------------------------------- 1 install
def gpu_tier():
    import torch
    if not torch.cuda.is_available():
        raise RuntimeError("no GPU on this runtime")
    cap = torch.cuda.get_device_capability(0)
    if cap < (8, 0):
        raise RuntimeError(f"GPU capability {cap} has no bf16 (T4 is too old); use L4 or G4")
    vram = torch.cuda.get_device_properties(0).total_memory / 2**30
    tier = M.tier_for(vram)
    log(f"GPU {torch.cuda.get_device_name(0)}, {vram:.0f} GB, tier {tier}")
    return tier


def clone(url, dest, commit):
    dest = Path(dest)
    if not dest.exists():
        sh(["git", "clone", "--filter=blob:none", url, str(dest)])
    sh(["git", "-C", str(dest), "checkout", "-q", commit])


def install(tier):
    if MARK.exists():
        log("install: already done on this runtime")
        return
    log("install: ComfyUI", "install")
    clone("https://github.com/Comfy-Org/ComfyUI.git", COMFY, M.COMFY_COMMIT)
    # torch is already on Colab; requirements.txt only adds what is missing
    sh([sys.executable, "-m", "pip", "install", "-q", "-r", str(COMFY / "requirements.txt"), "huggingface_hub", "hf_xet"])
    for name, (url, commit) in M.NODES[tier].items():
        clone(url, COMFY / "custom_nodes" / name, commit)
        req = COMFY / "custom_nodes" / name / "requirements.txt"
        if req.exists():
            sh([sys.executable, "-m", "pip", "install", "-q", "-r", str(req)])
    MARK.write_text(time.ctime())
    log("install: done")


# ---------------------------------------------------------------- 2 models
def download(files):
    from huggingface_hub import hf_hub_download
    for repo, name, folder, _size in files:
        target = COMFY / "models" / folder / Path(name).name
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.is_file():
            got = Path(hf_hub_download(repo_id=repo, filename=name, local_dir="/content/hf"))
            shutil.move(str(got), str(target))
        log(f"model ready: {target.name} ({target.stat().st_size / 2**30:.1f} GiB)")


# ---------------------------------------------------------------- 3 server
def wait_http(url, name, logfile, tries=180):
    for _ in range(tries):
        try:
            urllib.request.urlopen(url, timeout=2)
            return
        except Exception:
            time.sleep(2)
    raise RuntimeError(f"{name} did not start:\n" + Path(logfile).read_text(errors="ignore")[-2000:])


def start_comfy():
    try:
        urllib.request.urlopen(COMFY_URL + "/system_stats", timeout=2)
        log("ComfyUI already running")
        return
    except Exception:
        pass
    subprocess.Popen([sys.executable, "main.py", "--listen", "127.0.0.1", "--port", "8188"], cwd=str(COMFY),
                     stdout=open("/content/comfyui.log", "w"), stderr=subprocess.STDOUT, start_new_session=True)
    wait_http(COMFY_URL + "/system_stats", "ComfyUI", "/content/comfyui.log")
    log("ComfyUI started")


# ---------------------------------------------------------------- 4 jobs
def call(url, body=None, timeout=120):
    req = urllib.request.Request(url, headers={"Content-Type": "application/json"},
                                 data=None if body is None else json.dumps(body).encode())
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read()
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"{url} -> {e.code}: {e.read().decode('utf-8', 'replace')[:1500]}")
    return json.loads(raw) if raw.strip() else {}


def comfy_input():
    return Path(os.environ.get("OMC_COMFY_INPUT") or COMFY / "input")


def comfy_file(info):
    if os.environ.get("OMC_FETCH") == "1":  # a local ComfyUI: its output folder can be anywhere, so ask it
        q = urllib.parse.urlencode({"filename": info["filename"], "subfolder": info.get("subfolder", ""),
                                    "type": info.get("type", "output")})
        dst = JOB / "fetch" / info["filename"]
        dst.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(f"{COMFY_URL}/view?{q}", timeout=300) as r, open(dst, "wb") as f:
            shutil.copyfileobj(r, f)
        return dst
    return COMFY / "output" / info.get("subfolder", "") / info["filename"]


def stage_input(job, k, rel):
    """Copy one input (a file, or "@id" = an earlier job's output) into ComfyUI's input folder."""
    if rel.startswith("@"):
        st = STATE["jobs"].get(rel[1:], {})
        if st.get("status") != "done":
            raise RuntimeError(f"{rel}: that job has not produced a file (it must come earlier and succeed)")
        src = OUT / st["file"]
    else:
        src = JOB / "inputs" / rel
    if not src.is_file():
        raise RuntimeError(f"input not found: {rel}")
    name = f"omc_{job['id']}_{k}{src.suffix}"
    comfy_input().mkdir(parents=True, exist_ok=True)
    shutil.copy(str(src), str(comfy_input() / name))
    return name


def run_graph(graph, out_node, timeout):
    pid = call(COMFY_URL + "/prompt", {"prompt": graph, "client_id": "omc"})["prompt_id"]
    t0 = time.time()
    while time.time() - t0 < timeout:
        h = call(COMFY_URL + f"/history/{pid}").get(pid)
        if h and h.get("status", {}).get("completed") is not None:
            if h["status"].get("status_str") == "error":
                msgs = [m[1] for m in h["status"].get("messages", []) if m[0] == "execution_error"]
                raise RuntimeError(f"ComfyUI: {msgs[0].get('exception_message', '')[:600] if msgs else 'error'}")
            files = h["outputs"].get(out_node, {}).get("images") or []
            if not files:
                raise RuntimeError("ComfyUI finished but returned no file")
            return comfy_file(files[0])
        time.sleep(3)
    raise RuntimeError(f"no result after {timeout} s")


def run_job(j, tier):
    feature = M.feature_of(j)
    models = M.FEATURES[feature][tier]
    if feature == "t2i":
        graph, out = G.t2i(j, models)
        timeout = 900
    elif feature == "edit":
        names = [stage_input(j, k, rel) for k, rel in enumerate(j["inputs"])]
        graph, out = G.edit(j, models, names)
        timeout = 900
    else:
        start = j.get("inputs", [None])[0] if j.get("inputs") else None
        graph, out = G.video(j, models, start_name=stage_input(j, 0, start) if start else None)
        timeout = int(j.get("timeout", 2400))
    return run_graph(graph, out, timeout)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((JOB / "manifest.json").read_text(encoding="utf-8"))
    jobs = manifest["jobs"]
    for j in jobs:
        STATE["jobs"][j["id"]] = {"type": j["type"], "status": "queued"}
    save()
    if LOCAL:
        tier = os.environ["OMC_TIER"]
    else:
        tier = manifest.get("tier") or gpu_tier()
        install(tier)
        features = sorted({M.feature_of(j) for j in jobs} | set(manifest.get("preload", [])))
        log(f"models for {', '.join(features)} (tier {tier})", "models")
        download(M.files_for(features, tier))
        start_comfy()
    STATE.update(stage="generating", tier=tier)
    for j in jobs:
        st = STATE["jobs"][j["id"]]
        st.update(status="running", started=time.time())
        save()
        try:
            if j.get("seed") is None:  # pick it here so results.json can say how to make it again
                j["seed"] = G.seed_of(j)
            src = run_job(j, tier)
            dst = OUT / f"{j['id']}{Path(src).suffix}"
            shutil.copy(str(src), str(dst))
            st.update(status="done", file=dst.name, bytes=dst.stat().st_size,
                      seconds_used=round(time.time() - st["started"], 1), seed=j.get("seed"))
            log(f"{j['id']}: done in {st['seconds_used']} s -> {dst.name}")
        except Exception as e:
            st.update(status="error", error=str(e)[:1500])
            log(f"{j['id']}: ERROR {e}")
            if manifest.get("stop_on_error"):
                break
        save()
    STATE.update(done=True, stage="finished", finished=time.time())
    save()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        STATE.update(done=True, stage="failed", error=f"{e}\n{traceback.format_exc()[-1500:]}")
        save()
        raise
