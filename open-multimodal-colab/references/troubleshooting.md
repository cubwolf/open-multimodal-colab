**English** | [繁體中文](troubleshooting.zh-TW.md)

# Troubleshooting

Run `python scripts/omrun.py check` first. It shows three things: whether the colab command exists, whether you are logged in, and how many units are left.

## The one thing to remember: a GPU left running keeps using units
- When `omrun.py run` finishes normally, the GPU is kept for 15 minutes (`--idle-minutes`) for the next batch, and an independent local timer runs `stop` when it expires. Failed or interrupted batches `stop` immediately. The timer log is in `~/.config/omcskill/keep/<session>.log`.
- If the local program is killed, the computer sleeps or the network drops, **the remote machine does not stop by itself**. First thing when you come back:
  ```
  python scripts/omrun.py sessions
  python scripts/omrun.py stop --all
  ```
- Before the conversation ends, make sure `sessions` is empty.

## Install and login
| Symptom | Cause and fix |
|---|---|
| `No module named 'termios'` (Windows) | colab-cli's interactive terminal only supports Linux / macOS. The install script patches it; to fix by hand, rerun `install/install.ps1` |
| `WebSocketConnectionClosedException: socket is already closed` (Windows) | A colab-cli 0.7.5 problem. The install script pins **0.7.4** |
| `colab` checks for updates first and hangs | Write `{"enable_update_check": false}` to `~/.config/colab-cli/settings.json` (the install script does this) |
| `redirect_uri_mismatch` after login | Always use `colab_login.py` (it uses colab-cli's own client and redirect); don't build the URL yourself |
| `invalid_grant` | The code works once and only for a few minutes: rerun `colab_login.py url` |
| Switching accounts | Delete `~/.config/colab-cli/token.json` and log in again |

## Boot
| Symptom | Fix |
|---|---|
| Enough units but no GPU assigned | Common at peak times. Wait a few minutes and retry, or switch between L4 / G4. **Do not switch to A100** (much more expensive) |
| GPU name mistyped | colab-cli silently starts an A100. `omrun.py` only accepts L4, G4, A100, H100 |
| `GPU capability ... has no bf16` | You got a T4 (too old); use L4 or better |
| `沒有登入` (not logged in) / `401` | The token expired or was revoked: log in again |

## Generation
| Symptom | Fix |
|---|---|
| One job failed, the others succeeded | Read that job's `error` in `out/results.json`; resend only that job (add `--session` to reuse a machine that is still running) |
| `that job has not produced a file` | The job referenced by `@id` comes later or failed |
| The video barely moves, like a photo wobbling | Describe the subject's action and the camera movement clearly; or change the seed |
| The edit ignores the reference image | Say "the person in image 1", "the background of image 2" explicitly; put the image to change first |
| Local `out of memory` | Use 480P, shorten the clip; check that `check` chose the `low` tier; close other programs using VRAM |
| Local `UnetLoaderGGUF` not recognized | The ComfyUI-GGUF nodes from `setup` are missing their packages or ComfyUI was not restarted: follow the commands `setup` printed |
| Progress stuck at `models` | The first run downloads the models this batch needs (about 13–18 GB per feature, about 26 GB for talking video); after 15 minutes, check Hugging Face's status |
| Voice-over fails: `No module named ensurepip` or `torchvision::nms does not exist` | Caused by the old install method; this version uses uv and leaves torch alone. If it still fails, delete `/content/ttsenv` and run again |
| The talking video is longer than expected | Its length follows the speech; shorten the line |

## Reading the full remote log
```
colab exec -s <session> -f <a file containing only print(open('/content/omcjob/remote_job.log').read()[-5000:])>
```
The ComfyUI log is in `/content/comfyui.log`. In local mode the log is `.omclocal/runner.log` in the working folder.

## Getting files back
- By default files are fetched one by one with `colab download` (pictures and short clips are small).
- **Do not** turn a video into text and print it in the log to bring it back; it is tens of minutes slower and keeps using units.
- For many or large files: if you (the agent) are connected to Google Drive, the remote side can copy `out/` to Drive first and you fetch it with your connector.
  This needs Drive authorization on Colab (`colab drivemount` opens a browser authorization on the VM that must be completed within 10 minutes), so only use it when really needed.

## Prior work we learned from
- dseditor/h3-colab-skill (MIT): the source of this skill's orchestration.
- bockybocky/colab-gpu-runner (MIT): pin 0.7.4 plus the patch on Windows, short execs are more stable than long ones, always check for leftover runtimes at the end, don't move files through the log.
- Google's google-colab-cli (Apache-2.0): the login flow (client, scope, redirect) follows its `auth.py`.
