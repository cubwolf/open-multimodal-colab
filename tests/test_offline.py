# -*- coding: utf-8 -*-
"""Checks that need no GPU and no ComfyUI:  python tests/test_offline.py"""
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "open-multimodal-colab"
sys.path.insert(0, str(ROOT / "remote"))
sys.path.insert(0, str(ROOT / "scripts"))
import graphs as G  # noqa: E402
import models as M  # noqa: E402
import omrun  # noqa: E402


def test_sizes():
    assert G.image_dims("1:1", "1K") == (1024, 1024)
    w, h = G.image_dims("9:16", "2K")
    assert h == 2048 and w % 16 == 0 and abs(w / h - 9 / 16) < 0.01
    assert G.video_frames(5) == 121 and G.video_frames(2) == 49
    for res in G.VIDEO_SIZES.values():
        for w, h in res.values():
            assert w % 32 == 0 and h % 32 == 0


def test_tiers_and_files():
    assert M.tier_for(24) == "high" and M.tier_for(12) == "low"
    try:
        M.tier_for(8)
        raise AssertionError("8 GB must be refused")
    except RuntimeError:
        pass
    for feature, tiers in M.FEATURES.items():
        for tier, roles in tiers.items():
            assert set(roles) == {"unet", "clip", "vae"}, (feature, tier)
            assert all(k in M.FILES for k in roles.values())
    low = [f[1] for f in M.files_for(["video"], "low")]
    assert any(n.endswith(".gguf") for n in low)
    assert M.feature_of({"type": "image"}) == "t2i" and M.feature_of({"type": "image", "inputs": ["a"]}) == "edit"


def test_graph_links_resolve():
    m = {f: M.FEATURES[f]["low"] for f in M.FEATURES}
    graphs = [G.t2i({"id": "a", "prompt": "x"}, m["t2i"]), G.edit({"id": "b", "prompt": "x"}, m["edit"], ["a.png", "b.png"]),
              G.video({"id": "c", "prompt": "x"}, m["video"], "a.png"), G.video({"id": "d", "prompt": "x"}, m["video"])]
    for g, out in graphs:
        assert out in g
        for nid, node in g.items():
            for v in node["inputs"].values():
                if isinstance(v, list):
                    assert v[0] in g, (nid, v)
    assert graphs[2][0]["unet"]["class_type"] == "UnetLoaderGGUF"


def test_manifest_validation():
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        (d / "inputs").mkdir()
        (d / "inputs" / "a.png").write_bytes(b"x")
        good = {"jobs": [{"id": "pic", "type": "image", "prompt": "a cat"},
                         {"id": "clip", "type": "video", "prompt": "walks", "inputs": ["@pic"], "seconds": 5}]}
        (d / "m.json").write_text(json.dumps(good))
        omrun.load_manifest(d / "m.json")
        bad = {"jobs": [{"id": "clip", "type": "video", "prompt": "x", "seconds": 9, "inputs": ["@later", "inputs/a.png"]},
                        {"id": "img", "type": "tts", "prompt": "x"}]}
        (d / "m.json").write_text(json.dumps(bad))
        try:
            omrun.load_manifest(d / "m.json")
            raise AssertionError("bad manifest passed")
        except SystemExit as e:
            msg = str(e)
            assert "seconds" in msg and "@later" in msg and "type" in msg and "起始圖" in msg, msg


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("OK", name)
