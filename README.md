# open-multimodal-colab

讓 AI agent（Claude Code、Codex 等）在**你自己的 GPU** 上生圖、改圖、做短影片的 skill。
用的都是授權乾淨的開源模型（Apache 2.0，成品不需要標示模型名稱），可以在 Google Colab 上跑，也可以在自己電腦的 ComfyUI Desktop 上跑。

這個專案改寫自 [dseditor/h3-colab-skill](https://github.com/dseditor/h3-colab-skill)（MIT），把 MiniMax H3 換成其他模型。原因是 MiniMax H3 的授權要求商用產品標示模型名稱。

## 功能（第一版）

| 功能 | 模型 | Colab L4（24 GB） | 本機 12 GB（RTX 3060） |
|---|---|---|---|
| 文生圖 | Z-Image-Turbo | bf16 | int8 |
| 圖片編輯（1–4 張參考圖） | FLUX.2 [klein] 4B | fp8 | fp8 |
| 文生影片、圖生影片（1–5 秒，無聲） | Wan 2.2 TI2V-5B | fp16 | GGUF Q8 |
| 影片延伸（接在前一段之後） | Wan 2.2 TI2V-5B | fp16 | GGUF Q8 |
| 配音（設計聲音或複製音色） | Qwen3-TTS 1.7B | bf16 | bf16（未實測） |
| 說話影片（圖＋語音） | Wan 2.2 S2V-14B | fp8＋4 步 LoRA | 不支援 |

顯存等級會自動判斷，見 [models.py](open-multimodal-colab/remote/models.py)。12 GB 的設定是依檔案大小推估的，還沒實測。

之後的版本會加入：音樂（ACE-Step 1.5）。

## 安裝

給 agent 看 [INSTALL_FOR_AGENTS.md](INSTALL_FOR_AGENTS.md)。手動安裝：

- Windows：`powershell -ExecutionPolicy Bypass -File install\install.ps1`
- macOS / Linux：`bash install/install.sh`

Colab 模式需要 Google AI Pro。本機模式需要先裝好 [ComfyUI Desktop](https://comfy.org/download)，然後：

```
python open-multimodal-colab/scripts/omlocal.py check
python open-multimodal-colab/scripts/omlocal.py setup
```

## 用法

agent 會照 [SKILL.md](open-multimodal-colab/SKILL.md) 寫一份 `manifest.json`（格式見 [manifest.md](open-multimodal-colab/references/manifest.md)），再執行：

```
python open-multimodal-colab/scripts/omrun.py run omcjob/manifest.json --gpu L4    # Colab
python open-multimodal-colab/scripts/omlocal.py run omcjob/manifest.json           # 本機
```

## 測試

```
python tests/test_offline.py                       # 不需要 GPU
python tests/validate_graphs.py --url http://127.0.0.1:8188   # 讓 ComfyUI 驗證所有工作流
```

`validate_graphs.py` 只需要一個 ComfyUI（CPU 也可以）、空的模型佔位檔和 ComfyUI-GGUF 節點，不會真的生成。

## 授權

程式：MIT（[LICENSE](LICENSE)）。第三方程式來源見 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)，模型授權見 [licenses.md](open-multimodal-colab/references/licenses.md)。
