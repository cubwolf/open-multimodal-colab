# -*- coding: utf-8 -*-
"""Send every graph variant to a running ComfyUI and check that it passes ComfyUI's own validation
(node names, input names, model file names, links). The queue is cleared right after, so nothing is generated.

  python tests/validate_graphs.py [--url http://127.0.0.1:8188]

The ComfyUI under test needs the model files (empty placeholder files are enough), ComfyUI-GGUF for the low
tier, and two pictures a.png and b.png in its input folder.
"""
import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "open-multimodal-colab" / "remote"))
import graphs as G  # noqa: E402
import models as M  # noqa: E402


def post(url, path, body):
    req = urllib.request.Request(url + path, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b"{}")


def cases():
    for tier in ("high", "low"):
        m = {f: {k: v for k, v in M.FEATURES[f][tier].items()} for f in M.FEATURES}
        yield f"{tier} t2i 1K 1:1", G.t2i({"id": "t", "prompt": "a cat", "seed": 1}, m["t2i"])
        yield f"{tier} t2i 2K 9:16", G.t2i({"id": "t", "prompt": "a cat", "aspect": "9:16", "size": "2K"}, m["t2i"])
        yield f"{tier} edit 1 pic auto", G.edit({"id": "e", "prompt": "make it blue"}, m["edit"], ["a.png"])
        yield f"{tier} edit 3 pics 16:9", G.edit({"id": "e", "prompt": "mix", "aspect": "16:9", "size": "1.5K"}, m["edit"],
                                                 ["a.png", "b.png", "a.png"])
        yield f"{tier} video text 720P", G.video({"id": "v", "prompt": "waves", "seconds": 5}, m["video"])
        yield f"{tier} video image 480P 9:16", G.video({"id": "v", "prompt": "waves", "seconds": 3, "resolution": "480P",
                                                        "aspect": "9:16"}, m["video"], start_name="a.png")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default="http://127.0.0.1:8188")
    url = ap.parse_args().url.rstrip("/")
    bad = 0
    for label, (graph, _) in cases():
        code, body = post(url, "/prompt", {"prompt": graph, "client_id": "validate"})
        ok = code == 200 and not body.get("node_errors")
        print(("OK   " if ok else "FAIL ") + label)
        if not ok:
            bad += 1
            print("     " + json.dumps(body, ensure_ascii=False)[:1500])
    post(url, "/queue", {"clear": True})
    post(url, "/interrupt", {})
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
