# 風の歌詞帳

藤井風 21 首歌曲的歌詞練習網站，包含繁體中文翻譯、日文讀音與羅馬拼音、可點選詞語解釋及歌曲學習筆記。

[開啟公開網站](https://kaze-lyrics-notebook-1028.summy5677.chatgpt.site)

## 目錄

- `dist/`：可直接部署的完整靜態網站。
- `dist/index.html`：網站介面、樣式與互動。
- `dist/img/`：網站圖片。
- `dist/data/lyrics.js`：網站載入的固定解析資料。
- `dist/data/lyrics.json`：可閱讀及備份的同一份資料。
- `work/lyrics/`、`work/analysis/`：歌詞與逐首解析原始資料。
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

## 學習說明

翻譯與解讀依使用者提供的歌詞製作；有歧義的原文已於筆記註明。朗讀使用裝置內建語音，並非原曲，聲音會依裝置與瀏覽器而異。
