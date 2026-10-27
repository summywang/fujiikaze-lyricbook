from pathlib import Path
import re,json
root=Path('/Users/user/Documents/Codex/2026-10-28/new-chat')
src=Path('/Users/user/Documents/FujiiKaze/index.html').read_text()
src='<!doctype html>\n<html lang="zh-Hant"><head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<meta name="description" content="藤井風歌詞練習帳：逐句繁中翻譯、日文羅馬拼音與詞語學習。">\n'+src
src=src.replace('<meta name="claude:viewport-fit-sides" content="cover">','')
src=src.replace('</style>','''
.study{margin:16px 0 30px;border:1px solid var(--pg-line);border-radius:16px;padding:18px 20px;color:var(--pg-fg);font-family:var(--f-zh);line-height:1.8;font-size:16px}
.study summary{cursor:pointer;font-weight:700}.study p{margin:12px 0}.study ul{padding-left:1.3em}.study li{margin:10px 0}.study .hint{font-size:13px;opacity:.85}.ln-src{overflow-wrap:anywhere}.tip{max-width:min(360px,calc(100vw - 24px));line-height:1.6}.s-tools{flex-wrap:wrap}.s-status{line-height:1.6}.ln-play:disabled{opacity:.3;cursor:default}
@media(max-width:520px){.s-bar{align-items:flex-start}.study{padding:14px}.s-tools{gap:6px}.pill{padding:7px 10px}}
</style>''',1)
src=src.replace('<svg style=', '</head><body><svg style=',1) if '<svg style=' in src else src
# The original starts its markup with an SVG sprite. Insert explicit body boundary.
if '</head>' not in src:
    src=src.replace('</style>', '</style>\n</head><body>',1)
src=src.replace('歌詞只存在這個私人頁面裡，給自己學習用。朗讀用的是瀏覽器內建語音，不是原曲音檔。','21 首歌詞與解析已收錄，開啟即可練習。翻譯為學習用語境解讀；朗讀使用裝置語音，並非原曲。')
src=src.replace('<button type="button" class="pill" id="editBtn">編輯</button>','')
src=re.sub(r'    <div class="paste" id="paste" hidden>.*?    <ol class="lyrics"', '    <details class="study" id="study"><summary>歌曲解讀與學習筆記</summary><div id="studyContent"></div></details>\n    <ol class="lyrics"',src,flags=re.S)
src=src.replace('<script>','<script src="data/lyrics.js"></script>\n<script>',1)
src=src.replace('title:"まっしろ"','title:"真っ白"')
src=src.replace('phrase:"慣用語"','phrase:"片語／學習單位"')
src=re.sub(r'const FATAL = .*?;\n','',src)
src=re.sub(r'function getRec\(key\) \{.*?\n\}', 'function getRec(key) { return PUBLISHED[key] || null; }',src,flags=re.S)
src=src.replace('return s.lang === "en" ? "en" : (JA_RE.test(text) ? "ja" : "en");','return JA_RE.test(text) ? "ja" : "en";')
# Remove on-demand AI and database writes entirely.
start=src.index('function cleanAnn('); end=src.index('/* ---------- poster ---------- */',start)
src=src[:start]+src[end:]
src=src.replace('$("#tgRo").hidden = s.lang === "en";','$("#tgRo").hidden = !JA_RE.test(getRec(s.key).raw);\n  renderStudy(getRec(s.key));')
start=src.index('function refreshSong(force)');end=src.index('// The song\'s own share link',start)
src=src[:start]+'''function refreshSong(force) {
  const s = songByKey(state.view); if (!s) return;
  const rec = getRec(s.key);
  $("#lyrics").hidden = false;
  if (force || rec !== lastRenderedRec) renderLyrics(s, rec);
  $("#spotBtn").href = spotifyUrl(s, rec);
  $("#tgRo").setAttribute("aria-pressed", String(state.showRo));
  $("#tgZh").setAttribute("aria-pressed", String(state.showZh));
  $("#speedBtn").textContent = state.rate.toFixed(1) + "×";
  renderStatus();
}
function renderStudy(rec) {
  const box = $("#studyContent"); box.replaceChildren();
  const p = el("p"); p.textContent = rec.summary; box.append(p);
  const list = el("ul");
  rec.notes.forEach(note => {const li=el("li"); li.textContent=note; list.append(li);});
  box.append(list);
  const hint=el("p","hint"); hint.textContent="依你提供的歌詞解析；保留原文拼寫。詩意與人物指涉容許不同解讀。點日文詞語可看讀音與詞義，點播放鍵可聽整句。"; box.append(hint);
  $("#study").open=false;
}

'''+src[end:]
start=src.index('function preparePaste(');end=src.index('function renderLyrics(',start)
src=src[:start]+'''function renderStatus() {
  const rec = getRec(state.view);
  $("#status").hidden = false;
  $("#stDot").className = "dot idle";
  $("#stBtn").hidden = true;
  $("#stMsg").textContent = "解析已收錄 · " + parseLyrics(rec.raw).filter(Boolean).length + " 句" + (typeof speechSynthesis === "undefined" ? " · 此瀏覽器不支援朗讀" : " · 點日文詞語查看解釋");
}

'''+src[end:]
src=src.replace('a.tk.length && s.lang === "ja"','a.tk.length && JA_RE.test(text)')
src=src.replace('s.lang === "ja" && a.ro && !split','a.ro && !split')
src=re.sub(r'^\$\("#(?:saveBtn|lyricsInput|editBtn|cancelEdit)"\).*?;\n','',src,flags=re.M)
src=src.replace('[POS_ZH[t.p] || "其他", t.m]','[t.k, t.r, POS_ZH[t.p] || "其他", t.m]')
src=src.replace('play.innerHTML = PLAY_SVG;', 'play.innerHTML = PLAY_SVG; play.disabled = !("speechSynthesis" in window);')
start=src.index('/* ---------- capabilities ---------- */');end=src.index('renderHead();',start)
src=src[:start]+src[end:]
src=src.replace('initCaps();','')
src+='\n</body></html>\n'
(root/'outputs/kaze-site/dist/index.html').write_text(src)
js=re.findall(r'<script>(.*?)</script>',src,re.S)[0]
(root/'work/site-main.js').write_text(js)
print('Static site updated; no runtime AI or database dependency.')
