# manifest.json

放在工作資料夾裡；`inputs` 的路徑都**相對於 manifest 所在的資料夾**。
成品下載到同一個資料夾的 `out/<id>.<副檔名>`，總結在 `out/results.json`。

```json
{
  "gpu": "L4",
  "stop_on_error": false,
  "jobs": [
    {"id": "cast_lin", "type": "image",
     "prompt": "A clean studio portrait of a young woman with short black hair ...",
     "aspect": "3:4", "size": "1.5K", "seed": 1},

    {"id": "frame01", "type": "image",
     "prompt": "Put the woman from image 1 at the reading table in image 2, warm evening light",
     "inputs": ["@cast_lin", "inputs/library.png"], "aspect": "16:9"},

    {"id": "shot01", "type": "video",
     "prompt": "She looks up from her book and smiles, the camera slowly pushes in ...",
     "inputs": ["@frame01"], "seconds": 5, "aspect": "16:9", "resolution": "720P"},

    {"id": "establish", "type": "video",
     "prompt": "Aerial view of a rainy city at night, neon reflections on wet streets ...",
     "seconds": 4, "aspect": "16:9", "resolution": "480P"}
  ]
}
```

## 欄位

| 欄位 | 用在 | 說明 |
|---|---|---|
| `id` | 全部 | 英數、`-`、`_`；也是輸出檔名 |
| `type` | 全部 | `image`／`video` |
| `prompt` | 全部 | 見 prompt-guide.md |
| `inputs` | image、video | image：0 張＝文生圖，1–4 張＝編輯（第 1 張是要改的那張）。video：0 張＝文生影片，1 張＝第一格 |
| `aspect` | image、video | image：`auto`（編輯時跟第 1 張同比例；文生圖等於 `1:1`）、`1:1`、`16:9`、`9:16`、`4:3`、`3:4`、`3:2`、`2:3`、`21:9`。video：`16:9`（預設）、`9:16`、`1:1`、`4:3`、`3:4` |
| `size` | image | `1K`（預設）、`1.5K`、`2K` |
| `seconds` | video | 1–5，預設 5 |
| `resolution` | video | `720P`（預設，1280×704）、`480P`（832×480） |
| `negative` | video | 不要出現的東西；不給就用 Wan 官方範本的預設 |
| `steps` | 全部 | 進階：文生圖預設 8、編輯 4、影片 20 |
| `seed` | 全部 | 不給就隨機，實際用的 seed 會寫進 `results.json`；要重現就固定 |
| `timeout` | video | 單段等待上限（秒），預設 2400 |

批次層級：`gpu`（`L4`、`G4`、`A100`、`H100`）、`stop_on_error`、`tier`（強制 `high`／`low`，通常不用填）。

## 一批的順序與 `@id`
同一批依序執行。`inputs` 裡可以寫 `@<id>`，意思是「**用這一批裡前面那個 job 的成品**」，
例如先生 `frame01` 這張圖，再讓 `shot01` 用 `"inputs": ["@frame01"]`。
被引用的 job 一定要排在前面而且成功，否則這一段會失敗（其他段照跑）。

## 續跑
`out/` 裡已經有同 id 的檔案就跳過，引用它的 job 會直接拿那個檔案。要重做加 `--force`。
