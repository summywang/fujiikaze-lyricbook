# 風の歌詞帳

藤井風 21 首歌曲的歌詞練習網站，包含繁體中文翻譯、日文讀音與羅馬拼音、可點選詞語解釋。點任一句可用 YouTube 官方音源聽原唱，並可單句循環。

[開啟公開網站](https://kaze-lyrics-notebook-1028.summy5677.chatgpt.site)

## 目錄

- `dist/`：可直接部署的完整靜態網站。
- `dist/index.html`：網站介面、樣式與互動。
- `dist/img/`：網站圖片。
- `dist/data/lyrics.js`：網站載入的固定解析資料。
- `dist/data/lyrics.json`：可閱讀及備份的同一份資料。逐首解讀筆記（`summary`、`notes`）仍保存在資料中，目前頁面不顯示。
- `dist/data/media.js`、`media.json`：每首歌的 Spotify 封面與連結、YouTube 原唱影片、逐句時間（由 `work/build_media_timing.py` 產生）。
- `work/lyrics/`、`work/analysis/`：歌詞與逐首解析原始資料。
- `work/breakdown/`：點詞組時提示裡的拆解（白話說明、句型、慣用語／口語／方言標籤），用 `python3 work/apply_breakdown.py <歌曲 key>` 寫入網站資料。21 首都已完成；同一個助詞的固定說法見 `work/breakdown/README.md`。
- `work/media/`：Spotify 與 YouTube 的核對資料、已找到的 YouTube 官方音源（`art-tracks.json`）、逐首時間對齊報告（`timing-report.json`）。
- `work/` 內的程式：製作時使用的輔助腳本，部分路徑依原始工作環境設定。

解析資料已隨網站保存，換瀏覽器或裝置不需重新解析，也不需要 AI 帳號或 API 金鑰。

## 本機預覽

在儲存庫根目錄執行：

```sh
python3 -m http.server 8000 --directory dist
```

然後開啟 http://localhost:8000 。網站不需要安裝套件或建置，可直接將 `dist/` 部署至靜態網站服務。

## 更新網站解析資料

修改 `dist/data/lyrics.json` 後，將同一份資料同步至網站使用的 JavaScript：

```sh
python3 - <<'PY'
import json
from pathlib import Path
p = Path('dist/data')
data = json.loads((p / 'lyrics.json').read_text(encoding='utf-8'))
(p / 'lyrics.js').write_text('const PUBLISHED = ' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n', encoding='utf-8')
PY
```

## 原唱與逐句時間

- 播放使用 YouTube 官方 IFrame 播放器，不下載或轉存音訊。每首最多兩個來源，歌名下方可切換「音源 / MV」，選擇會套用到其他歌曲：
  - 音源：藤井風頻道上的官方音源（「Provided to YouTube by …」，與 Spotify 錄音室版長度相同），時間直接可用。
  - MV：官方影片（含 Not a MV）。MV 的前奏長度和錄音室版不同，第一次需按一次「對齊」；何なんw（LRCLIB 有兩筆依 MV 同步的紀錄，晚 5.38 秒）與 Garden（長度相同）已預先對齊。
- 逐句時間取自 [LRCLIB](https://lrclib.net) 中長度相同的同步歌詞，依順序比對到本站歌詞；只保存時間，不保存 LRCLIB 的歌詞文字。比對不到的句子沒有時間（校準模式顯示「還沒有時間」），不推算。
- 花、満ちてゆく 只有 MV；真っ白 只有官方音源（長度和 Spotify 版不同），三首第一次都要對齊。Okay, Goodbye、Forever Young 沒有 MV。
- 重新產生（需要網路；快取放在儲存庫外的 `../work/timing/cache`）：

```sh
python3 work/build_media_timing.py
```

## 時間校準

影片固定在歌詞頁最上方。點任一句會直接從那句播放，只有正在唱的那句會亮起。底部播放列：時間軸、播放速度（1x / 0.75x / 0.5x）、倒退／快轉 5 秒、播放／暫停，以及「調整」（羅馬拼音、中文翻譯、時間校準）。播放或拖動時間軸時，歌詞會自動捲到正在唱的那句；手動捲動後約 3 秒才恢復跟隨。

「調整 › 時間校準」進入校準模式，每句歌詞下方會出現按鈕，畫面不顯示秒數；最底部是「時間校準中」列，點旁邊的 ? 可看使用說明。播放歌曲，在句子開唱的瞬間按：

- 對齊整首（只在第一句）：整首一起移動，讓第一句從這一刻開始。MV 前奏長度不同、或想重新對齊時用。
- 從這句起對齊（其他句）：這句和後面所有句子一起移動，前面不動。MV 中途有剪接時用。
- 開始／結束（每一句，對齊後出現）：按「開始」＝現在是這句的開始；按「結束」＝現在是這句的結束。只改這一句；上一句若唱到這裡還沒結束，會自動在這裡結束。

最底部列的「還原預設值」會先跳出確認，才清除這首歌在這支影片上的所有修改；「完成編輯」離開校準模式。修改存在這個瀏覽器（localStorage），依歌曲、影片與歌詞版本區分；清除瀏覽器資料會一併清掉。

iPhone Safari 第一次播放需要先點一次影片中的播放鍵，之後點句子就會直接跳轉播放。

## 學習說明

翻譯與解讀依使用者提供的歌詞製作；有歧義的原文已於筆記註明。朗讀使用裝置內建語音，並非原曲，聲音會依裝置與瀏覽器而異。
