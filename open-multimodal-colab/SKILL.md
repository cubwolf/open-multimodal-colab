---
name: open-multimodal-colab
description: Generate pictures, edit pictures and make short videos with open models whose licenses need no attribution on the output (Z-Image-Turbo, FLUX.2 klein 4B, Wan 2.2), on the user's own Google Colab GPU driven from this computer through google-colab-cli, or on their own ComfyUI Desktop (local mode, 12 GB VRAM and up). Use when the user asks to 生圖／改圖／生成影片／圖生影片／把分鏡生出來, or wants storyboard frames or clips made, including when you yourself have no image or video tool.
---

# 開源多模態生成（Colab GPU 或本機 ComfyUI）

在使用者自己的 GPU 上，用授權乾淨（Apache 2.0、不要求在成品上標示模型名稱）的開源模型生成：

| 種類 | 做什麼 | 模型 |
|---|---|---|
| `image`（沒有 `inputs`） | 文生圖，中英文字都能畫 | Z-Image-Turbo（6B，8 步） |
| `image`（有 `inputs`） | 拿 1–4 張圖編輯或合成（換顏色、換衣服、把人放進場景） | FLUX.2 [klein] 4B |
| `video` | 文生影片，或拿一張圖當第一格，1–5 秒，24 fps，**沒有聲音** | Wan 2.2 TI2V-5B |
| `video` + `extend` | 從前一段影片的最後一格接著演，成品自動接回前一段 | Wan 2.2 TI2V-5B |
| `tts` | 配音：用文字描述設計聲音，或拿一段錄音複製音色 | Qwen3-TTS 1.7B |
| `talk` | 說話影片：一張圖＋一段語音，嘴型對上聲音，長度跟著語音走 | Wan 2.2 S2V-14B（**只有 high 等級**） |

你（大模型）負責**理解需求、寫提示詞、組工作清單、檢查成果**；生成在 Colab 或本機 ComfyUI 上跑。
音樂之後的版本才會加入。

---

## 0. 第一次使用：先問在哪裡跑

**第一件事先問使用者**：「要在 Google Colab 上跑，還是用你自己電腦上的 ComfyUI Desktop（本機）？」
- 本機的條件：NVIDIA 顯示卡、**10 GB 以上**顯示卡記憶體（RTX 3060 12 GB 可以）、系統記憶體建議 32 GB、硬碟約 35 GB。
  ComfyUI Desktop 要先自己安裝好並打開（https://comfy.org/download）。
- 沒回答、或沒有符合條件的顯示卡 → **Colab**。
- 選了就記住，之後每批照用。

### 顯存等級（自動判斷）
| 等級 | 顯存 | 用的版本 |
|---|---|---|
| `high` | 20 GB 以上（Colab L4、G4、24 GB 顯示卡） | Z-Image bf16、Wan 2.2 5B fp16 |
| `low` | 10–19 GB（RTX 3060 12 GB 等） | Z-Image int8、Wan 2.2 5B GGUF Q8（需要 ComfyUI-GGUF 節點，`setup` 會裝） |

### 本機版（ComfyUI Desktop）
```
python scripts/omlocal.py check                # ComfyUI 開了沒、顯存等級、缺哪些模型與節點
python scripts/omlocal.py setup                # 第一次：下載缺的模型、裝需要的節點組
python scripts/omlocal.py run omcjob/manifest.json [--confirmed]
```
- 只要部分功能：`--features t2i,video`（可選 `t2i`、`edit`、`video`），可以少下載。
- 模型放 `~/ComfyUI-Shared/models`（ComfyUI Desktop 的預設）；放別處加 `--models-dir`。
- `setup` 裝了新節點時，照它印出的指令裝節點套件，請使用者**重開 ComfyUI Desktop**，再 `check`。
- 可攜版 ComfyUI 回報不出自己的位置：加 `--comfy-dir <ComfyUI 資料夾>`。
- 判斷錯等級時可以強制：`--tier high` 或 `--tier low`。
- 下面第 1 節的流程照走，只是第 6 步換成 `omlocal.py run`，第 8 步不用問保留 GPU。

### Colab 版：先跟使用者說清楚，再安裝

如果 `python scripts/omrun.py check` 找不到 colab 或還沒登入，**先停下來**，用使用者的語言說明這五件事，等對方說「好」才開始：

1. **會做什麼**：在使用者的 Google 帳號開一台 Colab GPU，裝 ComfyUI 和模型，生成完把檔案下載回這台電腦，然後**關掉那台 GPU**。
2. **要什麼訂閱**：至少 **Google AI Pro**（附 Colab 運算單元）。Plus 不夠。
3. **花多少點**：L4 約每小時 1.5 點，G4 約每小時 11 點。每次開機要先裝環境、下載模型（只下載這批用得到的：文生圖約 18 GB、改圖約 13 GB、影片約 18 GB）。
4. **會從哪裡抓什麼**：GitHub 的 ComfyUI；Hugging Face 的 Comfy-Org、Black Forest Labs、QuantStack 模型檔。**全部下載到 Colab 上，不佔這台電腦的空間。**
5. **何時要登入**：只有第一次。你會給他一個 Google 網址，他用**有 AI Pro 的帳號**登入、按允許，把頁面上的授權碼貼回對話。

安裝：照 repo 的 `INSTALL_FOR_AGENTS.md`。登入：
```
python scripts/colab_login.py url          # 把網址給使用者
python scripts/colab_login.py code <授權碼>  # 使用者貼回來之後
python scripts/omrun.py check              # 看到剩餘運算單元＝成功
```

---

## 1. 每次生成的流程

1. **問清楚要什麼**：幾張圖、幾段影片、誰的臉、什麼比例。
2. **準備輸入檔**：角色照、場景圖放進一個工作資料夾，例如 `omcjob/inputs/`。
3. **寫提示詞**：照 `references/prompt-guide.md`。
4. **寫 `manifest.json`**：格式見 `references/manifest.md`。整批一次送，不要一個一個開機。
5. **確認規格**：
   - **兩支以上的影片，一定要先跟使用者確認規格**：解析度（480P／720P）、直式或橫式、每段秒數。
     沒有 `--confirmed` 不會開機，它會先印出這批的摘要，給使用者看，確認後再加 `--confirmed`。
   - 影片預設 720P（Wan 2.2 5B 訓練時的解析度）。480P 比較快，但畫質還沒實測。
   - 第一次的批次先試一張圖和一段 3 秒影片，讓使用者看到真實的時間。
6. **送出**：
   ```
   python scripts/omrun.py run omcjob/manifest.json --gpu L4
   ```
   它會開機 → 上傳 → 背景生成 → 每 30 秒回報 → 每完成一個就下載到 `omcjob/out/`。
7. **檢查成果**：圖片打開看；影片至少抽幾格看；有錯就只重做那一個（改 prompt 或 seed）。
8. **回報，並問使用者要不要保留 GPU**：每個檔案的路徑、花了多久、用了哪個 seed（在 `out/results.json`）。
   做完之後 GPU **先留著 15 分鐘**（模型都還在上面）。一定要問一句：
   「要繼續生成或修改嗎？要的話 GPU 先留著（L4 一小時約 1.5 點）；不用的話我現在關掉。」
   - 要繼續 → 下一批加 `--session <名字>`，不用重新下載模型
   - 要多留一下 → `python scripts/omrun.py keep --session <名字> --minutes 60`（最多 240）
   - 不用了 → `python scripts/omrun.py stop --session <名字>`
   - 使用者沒回答也沒關係：本機有獨立的計時器，15 分鐘沒有新工作就自動關掉。
   - 確定只做一次：第 6 步加 `--stop-after`。中途失敗、被中斷的批次一律馬上關機。

---

## 2. 任務判準

### 圖片
- 沒有 `inputs` → 文生圖。`size`：`1K`（預設）、`1.5K`、`2K`（長邊像素）；`aspect` 預設 `1:1`。
- 有 `inputs` → 編輯。第 1 張是**要被改的那張**，其餘是參考，最多 4 張。`aspect: "auto"`（預設）會跟第 1 張同比例。
- 提示詞裡用「image 1」「image 2」指稱 `inputs` 的順序。

### 影片
- 沒有 `inputs` → 文生影片；`inputs` 放 1 張圖 → 那張圖當第一格（會置中裁成影片比例）。
- `seconds`：1–5（Wan 2.2 一段約 5 秒）。更長的片段要切成多段，之後的版本會加延伸功能。
- `aspect`：`16:9`（預設）、`9:16`、`1:1`、`4:3`、`3:4`。
- 影片**沒有聲音**。
- 分鏡流程：先用 `image` 生出分鏡圖，再讓 `video` 用 `"inputs": ["@<圖片 id>"]` 接著動起來，一次開機做完。

### 配音與說話影片
- `tts` 的 `prompt` 是要念的台詞；`voice` 是聲音描述，**一定要寫性別和年齡**（例如「溫和的中年男性，語速適中，親切」）。
  要複製某人的聲音，把錄音放 `voices`（1 段，3 秒以上），**只用本人或已同意的聲音**。
- 中文台詞約每秒 4 字。說話影片長度跟著語音走（每 4.8 秒一段，最後會裁到語音結束）。
- `talk` 用 `"audio": "@<tts 的 id>"` 接上配音，`inputs` 放 1 張人物圖。預設 480P、3:4。14B 模型只能在 Colab（high 等級）跑。
- 說話影片之後要接動作：下一個 `video` 寫 `"extend": "@<talk 的 id>"`，成品會是兩段接好的影片（延伸那段沒有聲音）。

---

## 3. 失敗時

先看 `references/troubleshooting.md`。最常見：
- 沒有登入／token 過期 → 重跑 `colab_login.py url`。
- 點數不足、分配不到 GPU → 換 L4 或晚點再試；**不要**改成 A100（很貴）。
- 某一段生成失敗 → 讀 `out/results.json` 的 error，只重送那一段（可以 `--session` 沿用還開著的機器）。
- 本機顯存不夠（`out of memory`）→ 改 480P、縮短秒數，或 `--tier low`。

授權說明見 `references/licenses.md`。
