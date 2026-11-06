[English](prompt-guide.md) | **繁體中文**

# 提示詞寫法

這些模型都吃自然語言，中英文都可以，**英文通常比較穩**。寫具體的畫面，不要寫抽象形容詞。

## 文生圖（Z-Image-Turbo）
- 順序：主體 → 外觀細節 → 動作／姿勢 → 場景 → 光線 → 鏡頭與構圖 → 風格。
- 要畫的字用引號包起來，例如 `a neon sign that says "OPEN 24H"`。中文字也可以，短字效果最好。
- 8 步、cfg 1 是官方設定，不支援負面提示詞；不要的東西就別寫進去。
- 範例：
  `A young woman with short black hair and a beige trench coat stands under a red umbrella on a rainy Taipei street at night, neon signs reflecting on the wet pavement, shallow depth of field, 35mm photo, cinematic color grading`

## 圖片編輯（FLUX.2 klein 4B）
- 用 `image 1`、`image 2` 指稱 `inputs` 的順序；第 1 張是要被改的那張。
- 一句話講清楚**要改什麼、保留什麼**：
  `Change the jacket of the woman in image 1 to a dark green leather jacket, keep her face, hair and pose unchanged`
- 合成：`Place the woman from image 1 sitting at the table in image 2, matching the warm evening light of image 2`
- 一次只改一兩件事；要改很多就分成幾個 job，用 `@id` 串起來。

## 影片（Wan 2.2 TI2V-5B）
- 寫 2–4 句英文：主體與外觀、**動作的過程**、場景、鏡頭運動、光線氣氛。
- 動作要寫成連續的過程（「turns her head, looks at the window, then smiles」），不要只寫狀態。
- 鏡頭用電影語言：`slow push-in`、`tracking shot`、`static shot`、`aerial view`、`handheld`。
- 圖生影片：圖已經決定外觀，提示詞重點放在**接下來發生什麼**和鏡頭怎麼動，外觀描述要跟圖一致。
- 一段只有約 5 秒，只放一個動作或一個鏡頭。
- `negative` 可以加不要的東西；不給就用官方範本的預設（避免字幕、靜止畫面、畸形手指等）。
- 範例：
  `A street musician in a worn leather jacket plays guitar in a retro subway station. Commuters hurry past him and a small crowd slowly gathers. Slow push-in from a medium shot to a close-up of his hands. Warm, dim lighting with soft film grain.`

## 影片延伸（`extend`）
- 新的一段從前一段的**最後一格**開始，提示詞只寫接下來的動作。
- 有先後順序的動作要寫得很明確，並用時間詞串起來：
  `The man walks to the right side of the frame, facing his walking direction. After two steps he turns his head toward the camera while still walking, smiles and waves his right hand.`
  實測時「先朝右走、再轉頭看鏡頭」的順序不明顯；寫得更具體，或換 seed 再試。
- 方向用畫面的方向（`to the right side of the frame`），不要用人物自己的左右。

## 配音（Qwen3-TTS）與說話影片（S2V）
- `voice` 一定寫性別、年齡、語氣、語速，例如 `溫和親切的中年男性，語速適中，帶著笑意`。
- 說話影片的提示詞寫表情和手勢，不用寫嘴型：`A friendly man introduces himself to the camera with a warm smile and natural hand gestures, static shot`。
- 片長跟著語音走，要控制長度就調整台詞字數。
