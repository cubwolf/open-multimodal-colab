[English](INSTALL_FOR_AGENTS.md) | **繁體中文**

# 給 AI agent 的安裝說明

你被要求安裝 **open-multimodal-colab**。請依序照下面的步驟做。

## 第 1 步：先跟使用者說明，等對方說「好」

安裝任何東西之前，用使用者的語言說明：

1. **它做什麼**：讓你（agent）用開源模型（Z-Image-Turbo、FLUX.2 klein 4B、Wan 2.2、Qwen3-TTS；Apache 2.0，成品不用標示模型名稱）
   在**使用者自己的 Google Colab GPU** 上生圖、改圖、做短影片、配音和說話影片。你寫提示詞，Colab 負責生成，
   檔案下載回這台電腦，之後 GPU 會關掉。
2. **訂閱**：至少要 **Google AI Pro**（附 Colab 運算單元）。AI Plus 不夠。
3. **費用**：L4 約每小時 1.5 點（大約是 RTX 4060 的等級），G4 約每小時 11 點（大約是 RTX Pro 6000 的等級）。
   AI Pro 每月約 400 點。每次開機都會安裝 ComfyUI，並下載這批需要的模型
   （每種功能約 13–18 GB，說話影片約 26 GB），**下載在 Colab 上**，不佔這台電腦的空間。
4. **這台電腦會裝什麼**：`uv`、Python 3.12、Google 的 `google-colab-cli` 0.7.4
   （隔離安裝的工具），加上這個 skill 資料夾。沒有別的。
5. **登入**：只要一次。你會給使用者一個 Google 登入連結，對方用**有 AI Pro 的帳號**登入，
   按允許，再把授權碼貼回來給你。

也要問：**用 Colab，還是用自己電腦上的 ComfyUI Desktop（本機模式）？** 本機模式需要先裝好並打開 ComfyUI Desktop
（https://comfy.org/download）、NVIDIA 顯示卡 10 GB 以上顯存（RTX 3060 12 GB 可以）、建議 32 GB 系統記憶體、約 35 GB 硬碟空間。
本機模式不需要 colab-cli、不用登入、不扣點：第 2 步照做（它會複製 skill），跳過第 3 步，
照 `SKILL.md` 的本機段落做（`scripts/omlocal.py check` -> `setup` -> `run`）。沒有回答就用 Colab。

使用者同意後才繼續。

## 第 2 步：安裝

Clone（或下載）`https://github.com/cubwolf/open-multimodal-colab`，然後：

- Windows（PowerShell）：`powershell -ExecutionPolicy Bypass -File install\install.ps1`
- macOS / Linux：`bash install/install.sh`

如果你的 skills 放在特別的位置，把資料夾當第一個參數傳進去
（例如 `install.ps1 -SkillsDir C:\path\to\skills`）。預設會把 skill 複製到找得到的每個 agent
skills 資料夾：`~/.claude/skills`、`~/.codex/skills`、`~/.hermes/skills`、`~/.agents/skills`。

## 第 3 步：登入（需要使用者）

```
python <skill>/scripts/colab_login.py url
```
把印出來的連結給使用者。對方貼回授權碼後：
```
python <skill>/scripts/colab_login.py code <授權碼>
python <skill>/scripts/omrun.py check
```
一切正常時，`check` 會印出剩餘的運算單元。

## 第 4 步：第一次執行

讀 `<skill>/SKILL.md`。先做一批很小的（在 L4 上一張圖、一段 3 秒影片），讓使用者在做更大的批次之前，
先看到完整流程和自己帳號上的真實時間。
