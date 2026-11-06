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

## 還沒查證的
- `flux2-vae.safetensors` 是從 Comfy-Org 的 `flux2-dev` repo 下載的。FLUX.2 [dev] 的模型權重是非商用授權，VAE 本身的授權要再確認。
- `black-forest-labs/FLUX.2-klein-4b-fp8` 在 Hugging Face 上是否需要先登入同意條款，要在第一次下載時確認。

## 本程式
- 本 repo 的程式：MIT（見 `LICENSE`）。
- 調度骨架改寫自 dseditor/h3-colab-skill（MIT），登入流程依 google-colab-cli（Apache 2.0），見 `THIRD_PARTY_NOTICES.md`。
- ComfyUI（GPL-3.0）與 ComfyUI-GGUF（Apache 2.0）是在 Colab 或使用者電腦上另外下載執行的，沒有包含在本 repo 裡。
