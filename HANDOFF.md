# 交接文件

最後更新：2026-10-28。給之後接手的人（或新的 AI session）：先讀 `README.md` 了解怎麼用，再讀這份了解「為什麼這樣做」和「還有什麼沒做」。

## 現在網站能做什麼

- **目錄**：21 首歌，封面用 Spotify 上該曲的正式封面（原比例、原色）。
- **歌詞頁**：YouTube 影片固定在最上方、滿版；點任一句從那句播放原唱，只有正在唱的那句會亮起；播放或拖時間軸時歌詞自動捲動。
- **底部播放列**：時間軸、速度（1x / 0.75x / 0.5x）、倒退／快轉 5 秒、播放／暫停、「調整」。
- **調整**：羅馬拼音、中文翻譯開關，以及進入「時間校準」。
- **點詞組**：提示一次列出整段拆解（讀音、白話意思、每個部分、句型）；標籤只標慣用語／口語／方言。
- **音源 / MV 切換**：歌名下方，有兩種來源的歌才出現，選擇會套用到其他歌。
- **時間校準模式**：每句下方有按鈕（第一句「對齊整首」，其他句「從這句起對齊」「開始」「結束」），最底部是「時間校準中 ? ／ 還原預設值 ／ 完成編輯」。

## 重要決策與原因

| 決策 | 原因 |
| --- | --- |
| 原唱用 YouTube 官方播放器，不用 Spotify | Spotify 開發者政策禁止把歌曲和視覺內容同步；2026 年 2 月起開發模式只限 5 位 Premium 使用者；網頁播放器在 iPhone Safari 不穩。YouTube 免登入、iPhone 可用。 |
| 預設用藤井風頻道的「官方音源」（Provided to YouTube by…），不是 MV | 長度和 Spotify 錄音室版相同，LRCLIB 的時間可以直接用；MV 前奏長度不同，要對齊。 |
| 不下載、不轉存任何音訊或歌詞 | 只存時間數字；LRCLIB 的歌詞文字只在本機快取（儲存庫外），不進 repo。 |
| 收合影片功能已移除 | YouTube 規定播放器播放時不能隱藏；使用者選擇不收合。 |
| 返回鍵放在影片正下方，不蓋在影片上 | YouTube 規定不能遮住播放器。 |
| 時間不顯示秒數，「開始／結束」按下去就是那一刻 | 使用者覺得數字和 ±0.1 微調看不懂。 |
| 詞組維持原本一小段，點開才列出拆解 | 拆太細要點太多次；說明全用白話，不用文法術語。規則見 `work/breakdown/README.md`。 |
| 修改存在瀏覽器 localStorage，沒有匯出／匯入 | 使用者不需要；代價是清除 Safari 網站資料就會不見。 |

## 時間資料狀態（`dist/data/media.json`）

- 989 句中 970 句有自動對好的時間（未人工逐句確認）。沒有時間的多是即興哼唱，例如死ぬのがいいわ中段的 scat。
- 打開就能用（音源，不需對齊）：除下列三首外的 18 首。
- 需要使用者先按一次「對齊整首」：花、満ちてゆく（只有 MV）、真っ白（官方音源長度和 Spotify 版不同）。
- MV：何なんw（+5.38 秒，有 LRCLIB 依 MV 同步的紀錄佐證）和 Garden（Not a MV，長度相同）已預先對齊；其他 MV 第一次都要對齊。Okay, Goodbye、Forever Young 沒有官方 MV。
- 有 13 句的播放區間超過 12 秒（66 句超過 8 秒），多半是拖到了間奏或長音，可用校準的「結束」修正。

## 還沒做或沒驗證的

1. **還沒在 iPhone 實機測過**。所有測試都是在電腦瀏覽器模擬 iPhone 尺寸。要確認的重點：第一次播放需先點影片的 ▶（iOS 限制，網頁會提示）、點句跳轉、自動捲動、時間校準按鈕。
2. **公開網站還是舊版**。`https://kaze-lyrics-notebook-1028.summy5677.chatgpt.site` 由 Codex Sites 部署（`.openai/hosting.json`），需要從 Codex 重新部署 `dist/`。
3. **時間沒人工確認**，可能有個別句子早或晚，需要邊聽邊用校準模式修。
4. 舊的歌曲解讀筆記（`lyrics.json` 的 `summary`、`notes`）仍在資料裡，頁面已不顯示。

## 怎麼更新

- **重建封面、YouTube 來源與時間**：`python3 work/build_media_timing.py`（需要網路，快取在儲存庫外的 `../work/timing/cache`；已找到的官方音源記在 `work/media/art-tracks.json`，重建不會因搜尋排序改變）。
- **詞組拆解**：改 `work/breakdown/<歌曲>.json`，先 `python3 work/apply_breakdown.py --check <歌曲>`，通過再不加 `--check` 寫入。
- **改了資料檔後**：把 `dist/index.html` 裡 `data/lyrics.js?v=…` 或 `data/media.js?v=…` 的版本號改掉，否則手機可能讀到舊檔。
- **本機預覽**：`python3 -m http.server 8765 --directory dist`，開 `http://localhost:8765`。

## 主要檔案

- `dist/index.html`：整個網站（樣式、介面、播放與校準邏輯都在這一個檔）。圖示是內嵌的 Material Symbols（圓角、weight 600）。
- `dist/data/lyrics.js`／`lyrics.json`：歌詞、翻譯、詞組與拆解。
- `dist/data/media.js`／`media.json`：封面、Spotify 連結、YouTube 來源、逐句時間。
- `work/build_media_timing.py`、`work/apply_breakdown.py`：上面兩份資料的產生程式。
- `work/media/`、`work/breakdown/`：來源核對紀錄與詞組拆解原稿。
