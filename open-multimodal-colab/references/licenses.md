# 授權

這個 skill 只下載授權不要求在成品上標示模型名稱的模型。完整查證見專案的授權調查文件；這裡是摘要。

| 模型 | 用途 | 授權 | 生成內容要標示嗎 |
|---|---|---|---|
| Z-Image-Turbo（Tongyi-MAI） | 文生圖 | Apache 2.0 | 不用 |
| Qwen3-4B 文字編碼器 | Z-Image、FLUX.2 klein 共用 | Apache 2.0 | 不用 |
| FLUX.2 [klein] 4B（Black Forest Labs） | 圖片編輯 | Apache 2.0（**只有 4B**；9B 與 [dev] 是非商用授權，不可換用） | 不用（但不可冒用 BFL／FLUX 商標） |
| Wan 2.2 TI2V-5B（Wan-AI） | 影片 | Apache 2.0，官方不主張生成內容的權利 | 不用 |
| UMT5-XXL 文字編碼器 | Wan 2.2 | Apache 2.0 | 不用 |

Apache 2.0 的要求只在**散布模型或程式碼本身**時才有（附上授權與 NOTICE），自己生成的圖片和影片不用署名。

## 下載來源的授權
- FLUX.2 的 VAE（`flux2-vae.safetensors`）從 `Comfy-Org/Flux-2-Klein-4B` 下載，這個 repo 標示 apache-2.0；BFL 官方 README 也寫明 autoencoder 以 Apache 2.0 釋出。
  不要改從 `Comfy-Org/flux2-dev` 下載：那個 repo 標示的是非商用授權。
- `black-forest-labs/FLUX.2-klein-4b-fp8` 標示 apache-2.0，沒有存取限制（2026-11-06 查）。

## 本程式
- 本 repo 的程式：MIT（見 `LICENSE`）。
- 調度骨架改寫自 dseditor/h3-colab-skill（MIT），登入流程依 google-colab-cli（Apache 2.0），見 `THIRD_PARTY_NOTICES.md`。
- ComfyUI（GPL-3.0）與 ComfyUI-GGUF（Apache 2.0）是在 Colab 或使用者電腦上另外下載執行的，沒有包含在本 repo 裡。
