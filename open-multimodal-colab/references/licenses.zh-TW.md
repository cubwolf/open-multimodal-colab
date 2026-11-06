[English](licenses.md) | **繁體中文**

# 授權

這個 skill 只下載授權不要求在成品上標示模型名稱的模型。每個下載來源的授權都在 2026-11-06 查過它的 Hugging Face 頁面，見下面的「下載來源」。

| 模型 | 用途 | 授權 | 生成內容要標示嗎 |
|---|---|---|---|
| Z-Image-Turbo（Tongyi-MAI） | 文生圖 | Apache 2.0 | 不用 |
| Qwen3-4B 文字編碼器 | Z-Image、FLUX.2 klein 共用 | Apache 2.0 | 不用 |
| FLUX.2 [klein] 4B（Black Forest Labs） | 圖片編輯 | Apache 2.0（**只有 4B**；9B 與 [dev] 是非商用授權，不可換用） | 不用（但不可冒用 BFL／FLUX 商標） |
| Wan 2.2 TI2V-5B（Wan-AI） | 影片 | Apache 2.0，官方不主張生成內容的權利 | 不用 |
| UMT5-XXL 文字編碼器 | Wan 2.2 | Apache 2.0 | 不用 |
| Wan 2.2 S2V-14B（Wan-AI） | 說話影片 | Apache 2.0，官方不主張生成內容的權利 | 不用 |
| Wan2.2-Lightning（lightx2v 4 步 LoRA） | 說話影片加速 | Apache 2.0 | 不用 |
| Qwen3-TTS 1.7B（Alibaba Qwen） | 配音 | Apache 2.0 | 不用 |
| wav2vec2-large-xlsr-53-english（音訊編碼器） | 說話影片 | Apache 2.0（Jonatas Grosman 以 Meta 的 wav2vec2-large-xlsr-53 微調，底模也是 Apache 2.0，訓練資料 Common Voice 是 CC0） | 不用 |

複製聲音只用本人或已取得同意的聲音。

Apache 2.0 的要求只在**散布模型或程式碼本身**時才有（附上授權與 NOTICE），自己生成的圖片和影片不用署名。

## 下載來源

| 檔案 | 下載自 | 該頁面標示的授權 |
|---|---|---|
| Z-Image-Turbo bf16／int8、Qwen3-4B 編碼器、Z-Image VAE | `Comfy-Org/z_image_turbo`（原始：`Tongyi-MAI/Z-Image-Turbo`） | apache-2.0 |
| FLUX.2 klein 4B fp8 | `black-forest-labs/FLUX.2-klein-4b-fp8` | apache-2.0，沒有存取限制 |
| FLUX.2 VAE | `Comfy-Org/Flux-2-Klein-4B` | apache-2.0 |
| Wan 2.2 TI2V-5B fp16、Wan 2.2／2.1 VAE、S2V-14B fp8、Lightning LoRA、wav2vec2 | `Comfy-Org/Wan_2.2_ComfyUI_Repackaged`（現在會轉到 `Comfy-Org/Wan-2.2`；原始：`Wan-AI/Wan2.2-TI2V-5B`、`Wan-AI/Wan2.2-S2V-14B`、`lightx2v/Wan2.2-Lightning`） | apache-2.0 |
| Wan 2.2 TI2V-5B GGUF Q8 | `QuantStack/Wan2.2-TI2V-5B-GGUF` | apache-2.0 |
| UMT5-XXL fp8 編碼器 | `Comfy-Org/Wan_2.1_ComfyUI_repackaged`（現在是 `Comfy-Org/Wan-2.1`） | apache-2.0 |
| Qwen3-TTS 1.7B | `Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign`、`Qwen/Qwen3-TTS-12Hz-1.7B-Base` | apache-2.0 |

關於 wav2vec2：Wan-AI 在官方 `Wan-AI/Wan2.2-S2V-14B` repo 裡附了同一個編碼器（資料夾 `wav2vec2-large-xlsr-53-english/`），它的模型卡寫明是 `jonatasgrosman/wav2vec2-large-xlsr-53-english`、授權 apache-2.0，底模 `facebook/wav2vec2-large-xlsr-53` 也是 apache-2.0。ComfyUI 用的 `wav2vec2_large_english_fp16.safetensors` 是這個編碼器給 ComfyUI 用的 fp16 版本（Comfy-Org 沒有逐檔說明，這是依檔名、大小和官方 S2V 範本的用法判斷的）。

來源補充：
- FLUX.2 的 VAE（`flux2-vae.safetensors`）從 `Comfy-Org/Flux-2-Klein-4B` 下載，這個 repo 標示 apache-2.0；BFL 官方 README 也寫明 autoencoder 以 Apache 2.0 釋出。
  不要改從 `Comfy-Org/flux2-dev` 下載：那個 repo 標示的是非商用授權。
- `black-forest-labs/FLUX.2-klein-4b-fp8` 標示 apache-2.0，沒有存取限制（2026-11-06 查）。

## 本程式
- 本 repo 的程式：MIT（見 `LICENSE`）。
- 調度骨架改寫自 dseditor/h3-colab-skill（MIT），登入流程依 google-colab-cli（Apache 2.0），見 `THIRD_PARTY_NOTICES.md`。
- ComfyUI（GPL-3.0）與 ComfyUI-GGUF（Apache 2.0）是在 Colab 或使用者電腦上另外下載執行的，沒有包含在本 repo 裡。
