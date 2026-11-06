# Third-party notices

## dseditor/h3-colab-skill

Parts of this repository are adapted from https://github.com/dseditor/h3-colab-skill :
`open-multimodal-colab/scripts/omrun.py` (from `h3run.py`), `omlocal.py` (from `h3local.py`),
`colab_login.py`, `open-multimodal-colab/remote/remote_job.py`, `start.py`, `status.py`,
`install/install.sh`, `install/install.ps1`, `install/patch_colab_cli.py`,
`INSTALL_FOR_AGENTS.md` and `open-multimodal-colab/references/troubleshooting.md`.
That project is licensed as follows:

```
MIT License

Copyright (c) 2026 dseditor (DSLab)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## google-colab-cli

`open-multimodal-colab/scripts/colab_login.py` follows the OAuth client, scopes and redirect of
google-colab-cli's `auth.py` (Apache License 2.0, Copyright Google LLC).

## ComfyUI workflow templates

The graphs in `open-multimodal-colab/remote/graphs.py` follow the official templates in
https://github.com/Comfy-Org/workflow_templates (`image_z_image_turbo*.json`,
`image_flux2_klein_image_edit_4b_distilled.json`, `video_wan2_2_5B_ti2v.json`,
`video_wan2_2_14B_s2v.json`). The graphs are rebuilt in code from those templates' node layout; no template file is copied
into this repository. That repository declared no license when checked on 2026-11-06.
