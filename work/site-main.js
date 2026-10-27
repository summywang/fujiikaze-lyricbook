
// Setlist order. `legacy` is the number the song had in the first catalog, so lyrics saved then still load.
const SONGS = [
  {n:1,  key:"casket-girl",    legacy:7,  title:"Casket Girl",    lang:"en", ink:"b"},
  {n:2,  key:"its-alright",    legacy:0,  title:"It’s Alright",   lang:"en", ink:"f"},
  {n:3,  key:"i-need-u-back",  legacy:6,  title:"I Need U Back",  lang:"en", ink:"e"},
  {n:4,  key:"nan-nan",        legacy:15, title:"何なんw",        sub:"Nan-Nan",        lang:"ja", ink:"a"},
  {n:5,  key:"shinunoga-e-wa", legacy:10, title:"死ぬのがいいわ", sub:"Shinunoga E-Wa", lang:"ja", ink:"c"},
  {n:6,  key:"garden",         legacy:16, title:"ガーデン",       sub:"Garden",         lang:"ja", ink:"f"},
  {n:7,  key:"kirari",         legacy:12, title:"きらり",         sub:"Kirari",         lang:"ja", ink:"b"},
  {n:8,  key:"hana",           legacy:13, title:"花",             sub:"Hana",           lang:"ja", ink:"f"},
  {n:9,  key:"it-aint-over",   legacy:8,  title:"It Ain’t Over",  lang:"en", ink:"a"},
  {n:10, key:"love-like-this", legacy:3,  title:"Love Like This", lang:"en", ink:"c"},
  {n:11, key:"you",            legacy:4,  title:"You",            lang:"en", ink:"e"},
  {n:12, key:"workin-hard",    legacy:22, title:"Workin’ Hard",   lang:"ja", ink:"b"},
  {n:13, key:"damn",           legacy:0,  title:"damn",           lang:"ja", ink:"f"},
  {n:14, key:"tabiji",         legacy:21, title:"旅路",           sub:"Tabiji",         lang:"ja", ink:"a"},
  {n:15, key:"michi-teyu-ku",  legacy:14, title:"満ちてゆく",     sub:"Michi Teyu Ku",  lang:"ja", ink:"e"},
  {n:16, key:"prema",          legacy:1,  title:"Prema",          lang:"en", ink:"c"},
  {n:17, key:"okay-goodbye",   legacy:5,  title:"Okay, Goodbye",  lang:"en", ink:"a"},
  {n:18, key:"matsuri",        legacy:11, title:"まつり",         sub:"Matsuri",        lang:"ja", ink:"b"},
  {n:19, key:"hachiko",        legacy:2,  title:"Hachikō",        lang:"en", ink:"f"},
  {n:20, key:"forever-young",  legacy:9,  title:"Forever Young",  lang:"en", ink:"e"},
  {n:21, key:"masshiro",       legacy:20, title:"真っ白",       sub:"Masshiro",       lang:"ja", ink:"a", gapBefore:true},
];

const PHOTO_AR = {a:1.21,b:1.04,c:.69,e:.79,h:.70,i:.37,k1:1,k2:1.09,k3:.93,k4:1.49,k5:.71,k7:1.35,m1:.91,m2:.87,m3:1,m4:.56,m5:.94,n1:1.03,n2:1,n3:1,n4:1,n5:1.02,n6:1.62,n7:1,"kaze.gif":1};
const DUO = new Set(["k1","k2","k3","k4","k5","k7"]);
// Shown in its own colors, without the film tone.
const RAW = new Set(["kaze.gif"]);
// The cutout beside each song's strip; it is also the song's thumbnail on its lyric page.
const SONG_PHOTO = {"casket-girl":"m1","its-alright":"m4","i-need-u-back":"k3","nan-nan":"n3","shinunoga-e-wa":"m3","garden":"k4","kirari":"c","hana":"n5","it-aint-over":"e","love-like-this":"n4","you":"h","workin-hard":"k5","damn":"m2","tabiji":"n6","michi-teyu-ku":"k2","prema":"n2","okay-goodbye":"k1","matsuri":"i","hachiko":"n1","forever-young":"m5","masshiro":"k7"};
const SPILL = ["b","k7","a","k2","n4"];
// Fixed pieces of the title cluster: [key, x, y, width, rotation, cut, z]
const HEAD_PHOTOS = [["kaze.gif",58,4,40,4,"heart",2], ["a",62,44,36,5,6,1]];
const HEAD_STICKERS = [["bf","c-orange",50,72,8,18], ["sp","c-paper",54,44,4,0], ["fl","c-pink",92,80,6,0]];
// Per-slot variety for the track strips; slot i is the i-th visible song after filtering.
const TOP = 97;
const SIDE = "LRLLRLRRLRLRRLLRLRLRL";
const ROTS = [-5,4,-3,6,-4,3,-6,5,-2,4,-5,3,-4,6,-3,5,-6,2,-4,5,-3];
const INSET = [6,5,9,4,7,12,5,6,10,4,7,5,8,6,4,9,5,7,6,8,5];
const SCALE = [1,.92,.86,1,.9,1,.95,.88,1,.93,.9,1,.87,.96,1,.9,1,.94,.9,1,.92];
const CUTS = [1,4,3,2,1,3,5,4,2,6,3,1,2,4,1,5,3,2,4];
const SLOT_STICKERS = [["bf","c-orange"],["sp","c-paper"],["fl","c-yellow"],["bf","c-pink"],["sp","c-paper"],["bf","c-orchid"],["fl","c-pink"]];

const POS_ZH = {noun:"名詞",pronoun:"代名詞",verb:"動詞",adj:"い形容詞",na:"な形容詞",adv:"副詞",particle:"助詞",aux:"助動詞",conj:"接續詞",interj:"感嘆詞",prenoun:"連體詞",prefix:"接頭詞",suffix:"接尾詞",phrase:"片語／學習單位",en:"英文",other:"其他"};
// Bumped when the parsing rules change; Japanese lines parsed under an older rule can be re-parsed.
// v2: idioms and set phrases stay together as one tappable word.
const PARSE_V = 2;
const PLAY_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>';
const ARROW_SVG = '<svg viewBox="0 0 24 24"><path d="M4 11h12.2l-4.6-4.6L13 5l7 7-7 7-1.4-1.4 4.6-4.6H4z"/></svg>';
const JA_RE = /[぀-ヿ㐀-鿿]/;
const RATES = [1, 0.8, 0.6];
const CHUNK = 6;

const $ = (s) => document.querySelector(s);
const pad = (n) => String(n).padStart(2, "0");
const songByKey = (k) => SONGS.find((s) => s.key === k);
const isZhText = (s) => /^[一-鿿]+$/.test(s);
const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;
const store = {
  get(k, d) { try { const v = localStorage.getItem(k); return v === null ? d : JSON.parse(v); } catch (e) { return d; } },
  set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} },
  del(k) { try { localStorage.removeItem(k); } catch (e) {} },
};
function el(tag, cls) { const e = document.createElement(tag); if (cls) e.className = cls; return e; }
function str(v) { return typeof v === "string" ? v.trim() : ""; }
function jit(i, a, b) { return a + ((i * 37 + 11) % 97) / 97 * (b - a); }

const state = {
  db: null, sample: null, capsSettled: false,
  docs: {}, local: {}, jobs: {}, saveErr: null,
  view: null, editing: false, pasteFor: null, filter: "all",
  lines: [], speaking: -1,
  rate: RATES.includes(store.get("kaze.rate", 1)) ? store.get("kaze.rate", 1) : 1,
  showRo: store.get("kaze.ro", true), showZh: store.get("kaze.zh", true),
  sel: null,
};
let lastRenderedRec = null, catalogY = 0, lastSongKey = null;

/* ---------- lyric data ---------- */
function parseLyrics(raw) {
  const out = [];
  for (const line of String(raw).replace(/\r/g, "").split("\n").map((s) => s.trim())) {
    if (line) out.push(line);
    else if (out.length && out[out.length - 1] !== "") out.push("");
  }
  while (out.length && out[out.length - 1] === "") out.pop();
  return out;
}
function validRec(r) { return r && typeof r.raw === "string" && Array.isArray(r.uniq) && Array.isArray(r.ann) ? r : null; }
// Newest first: this visit's edits, the saved record, the record saved under the old numbering, this device's backup copy.
function getRec(key) { return PUBLISHED[key] || null; }
function lineLang(s, text) { return JA_RE.test(text) ? "ja" : "en"; }

// Wrap each token found in the line; anything unmatched stays plain so the original line always shows exactly.
function segment(line, tk) {
  const out = []; let pos = 0;
  tk.forEach((t, ti) => {
    if (t.p === "sym" || !t.t.trim()) return;
    const at = line.indexOf(t.t, pos);
    if (at < 0 || at - pos > 12) return;
    if (at > pos) out.push({ text: line.slice(pos, at) });
    out.push({ text: t.t, ti });
    pos = at + t.t.length;
  });
  if (pos < line.length) out.push({ text: line.slice(pos) });
  return out;
}

/* ---------- poster ---------- */
function photoEl(key, x, y, w, r, cut, z, extra) {
  const wrap = el("div", "pc ph-wrap");
  wrap.style.cssText = `--x:${x};--y:${y};--w:${w};--r:${r};--z:${z}`;
  const ph = el("div", `ph cut-${cut}${DUO.has(key) ? " duo" : ""}${RAW.has(key) ? " raw" : ""}${extra ? " " + extra : ""}`);
  ph.style.setProperty("--ar", cut === "heart" ? 10 / 9 : PHOTO_AR[key]);
  const img = el("img"); img.src = `img/${key.includes(".") ? key : key + ".jpg"}`; img.alt = ""; img.decoding = "async";
  ph.append(img); wrap.append(ph);
  return wrap;
}
function stickerEl(sym, color, x, y, w, r) {
  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute("class", `pc stk ${color}`); svg.setAttribute("aria-hidden", "true");
  svg.style.cssText = `--x:${x};--y:${y};--w:${w};--r:${r};--z:3`;
  svg.innerHTML = `<use href="#${sym}"/>`;
  return svg;
}
function charW(ch) {
  if (JA_RE.test(ch)) return 1;
  if (ch === " ") return .28;
  if (/[ilj’'.,!]/.test(ch)) return .3;
  if (/[A-Z]/.test(ch)) return .68;
  if (/[mw]/.test(ch)) return .78;
  return .52;
}
// Fit each title into about 56% of the poster width; titles with " / " print on two lines.
function titleFit(s, i) {
  const parts = s.title.split(" / ");
  const lines = parts.map((p, k) => (k < parts.length - 1 ? p + " /" : p));
  const em = Math.max(...lines.map((l) => [...l].reduce((w, ch) => w + charW(ch), 0))) + .7;
  const short = [...s.title].length <= 2 && JA_RE.test(s.title);
  const cap = lines.length > 1 ? 9 : short ? 17 : 13;
  const fs = Math.min(cap, 56 / em) * SCALE[i % SCALE.length];
  return { lines, fs: Math.round(fs * 100) / 100, width: fs * em };
}
function trackEl(s, i, y, fit) {
  const side = SIDE[i % SIDE.length];
  const a = el("a", `tk dyn ink-${s.ink}${side === "R" ? " ra" : ""}`);
  a.href = "#song-" + s.key; a.dataset.key = s.key;
  a.style.cssText = `${side === "R" ? "--rx" : "--x"}:${INSET[i % INSET.length]};--y:${y.toFixed(1)};--r:${ROTS[i % ROTS.length]};--fs:${fit.fs}`;
  const no = el("span", "tk-no"); no.textContent = pad(s.n);
  const ti = el("span", "tk-ti"); ti.lang = JA_RE.test(s.title) ? "ja" : "en";
  const pr = el("span", "pr"); const inner = el("i");
  fit.lines.forEach((line, k) => { if (k) inner.append(el("br")); inner.append(line); });
  pr.append(inner); ti.append(pr);
  const go = el("span", "tk-go"); go.setAttribute("aria-hidden", "true"); go.innerHTML = ARROW_SVG;
  a.append(no, ti, go);
  return a;
}
function layoutPoster() {
  const board = $("#board");
  board.querySelectorAll(".dyn").forEach((n) => n.remove());
  const list = SONGS.filter((s) => state.filter === "all" || s.lang === state.filter);
  let y = TOP;
  list.forEach((s, i) => {
    if (s.gapBefore && i > 0 && list[i - 1].n === s.n - 1) y += 10;
    const fit = titleFit(s, i);
    const side = SIDE[i % SIDE.length];
    const h = fit.lines.length * fit.fs * 1.3 + 1.5;
    board.append(trackEl(s, i, y, fit));
    // the song's photo cutout on the open side of its strip, sometimes tucked under its end
    const key = SONG_PHOTO[s.key]; const ar = PHOTO_AR[key];
    const w = Math.max(18, Math.min(34, 44 * ar));
    const px = side === "L" ? 100 - w - 2 + jit(i, -5, 5) : -4 + jit(i, 0, 6);
    const photo = photoEl(key, px.toFixed(1), (y - 6 + jit(i + 3, -2, 6)).toFixed(1), w.toFixed(1), ROTS[(i + 5) % ROTS.length], CUTS[i % CUTS.length], 1, i % 4 === 2 ? "dots" : "");
    photo.classList.add("dyn"); board.append(photo);
    // spill past the poster edges every few strips; only seen on wide screens
    if (i % 4 === 1) {
      const sk = SPILL[Math.floor(i / 4) % SPILL.length];
      const spill = photoEl(sk, side === "L" ? -44 : 106, y.toFixed(1), 34, ROTS[(i + 2) % ROTS.length], CUTS[(i + 3) % CUTS.length], 0);
      spill.classList.add("dyn"); board.append(spill);
    }
    if (i % 3 === 0) {
      const [sym, color] = SLOT_STICKERS[(i / 3) % SLOT_STICKERS.length];
      const inset = INSET[i % INSET.length];
      const sx = side === "L" ? Math.min(88, inset + fit.width + 2) : Math.max(2, 100 - inset - fit.width - 10);
      const st = stickerEl(sym, color, sx.toFixed(1), (y - 4).toFixed(1), sym === "sp" ? 4 : 8, ROTS[(i + 1) % ROTS.length] * 3);
      st.classList.add("dyn"); board.append(st);
    }
    y += h + 8 + (i % 3);
  });
  $("#colophon").style.setProperty("--y", (y + 10).toFixed(1));
  board.style.aspectRatio = `100 / ${Math.ceil(y + 34)}`;
  updateFocus();
}
// The strip nearest the middle of the screen grows and straightens, as on hover.
let focusRaf = 0;
function updateFocus() {
  focusRaf = 0;
  if ($("#catalog").hidden) return;
  const mid = window.innerHeight / 2, limit = window.innerHeight * .22;
  let best = null, bestD = Infinity;
  document.querySelectorAll(".tk").forEach((a) => {
    const r = a.getBoundingClientRect(); const d = Math.abs((r.top + r.bottom) / 2 - mid);
    if (d < bestD) { bestD = d; best = a; }
  });
  if (bestD > limit) best = null;
  document.querySelectorAll(".tk.on").forEach((a) => { if (a !== best) a.classList.remove("on"); });
  if (best) best.classList.add("on");
}
const queueFocus = () => { if (!focusRaf) focusRaf = requestAnimationFrame(updateFocus); };
window.addEventListener("scroll", queueFocus, { passive: true });
window.addEventListener("resize", queueFocus);
function renderHead() {
  const board = $("#board");
  for (const p of HEAD_PHOTOS) board.append(photoEl(...p));
  for (const st of HEAD_STICKERS) board.append(stickerEl(...st));
}
function setFilter(f) {
  state.filter = f;
  document.querySelectorAll(".fbtn").forEach((b) => {
    const on = b.dataset.f === f;
    b.setAttribute("aria-pressed", String(on));
    b.className = "fbtn " + (on ? "ink-p" : "ink-a");
  });
  store.set("kaze.filter", f);
  layoutPoster();
}
document.querySelector(".filters").addEventListener("click", (e) => {
  const b = e.target.closest("button[data-f]"); if (b && b.dataset.f !== state.filter) setFilter(b.dataset.f);
});

/* ---------- song view ---------- */
function showSong(s) {
  if (!$("#catalog").hidden) catalogY = window.scrollY;
  stopSpeech(); hideTip();
  state.view = s.key; lastSongKey = s.key; state.editing = false; state.pasteFor = null; lastRenderedRec = null;
  document.body.className = "on-song theme-" + s.ink;
  $("#catalog").hidden = true; $("#song").hidden = false;
  const title = $("#songTitle"); title.textContent = s.title; title.lang = JA_RE.test(s.title) ? "ja" : "en";
  const sub = s.sub && !isZhText(s.sub) ? s.sub : "";
  $("#songSub").textContent = sub ? `Fujii Kaze · ${sub}` : "Fujii Kaze";
  const thumb = $("#songThumb"); const pk = SONG_PHOTO[s.key];
  thumb.src = `img/${pk}.jpg`; thumb.className = "s-thumb" + (DUO.has(pk) ? " duo" : "");
  $("#tgRo").hidden = !JA_RE.test(getRec(s.key).raw);
  renderStudy(getRec(s.key));
  refreshSong(true);
  window.scrollTo(0, 0);
}

function refreshSong(force) {
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

// The song's own share link when one was saved, otherwise a Spotify search for it.
const SPOTIFY_RE = /^https:\/\/open\.spotify\.com\/\S+$/;
function spotifyUrl(s, rec) {
  if (rec && typeof rec.spotify === "string" && SPOTIFY_RE.test(rec.spotify)) return rec.spotify;
  return "https://open.spotify.com/search/" + encodeURIComponent(`${s.title} Fujii Kaze`);
}

function renderStatus() {
  const rec = getRec(state.view);
  $("#status").hidden = false;
  $("#stDot").className = "dot idle";
  $("#stBtn").hidden = true;
  $("#stMsg").textContent = "解析已收錄 · " + parseLyrics(rec.raw).filter(Boolean).length + " 句" + (typeof speechSynthesis === "undefined" ? " · 此瀏覽器不支援朗讀" : " · 點日文詞語查看解釋");
}

function renderLyrics(s, rec) {
  lastRenderedRec = rec;
  const ol = $("#lyrics"); ol.replaceChildren();
  ol.classList.toggle("hide-ro", !state.showRo);
  ol.classList.toggle("hide-zh", !state.showZh);
  const job = state.jobs[s.key]; const running = !!(job && job.running);
  state.lines = [];
  for (const text of parseLyrics(rec.raw)) {
    if (!text) { const g = el("li", "gap"); g.setAttribute("aria-hidden", "true"); ol.append(g); continue; }
    const n = state.lines.length; const u = rec.uniq.indexOf(text); const a = u >= 0 ? rec.ann[u] : null;
    state.lines.push({ text, u });
    const li = el("li", "ln" + (a ? "" : running ? " pending" : "")); li.dataset.n = n;
    const body = el("div", "ln-body");
    const src = el("p", "ln-src"); src.lang = lineLang(s, text);
    const split = !!(a && a.tk && a.tk.length && JA_RE.test(text));
    if (split) {
      // each word stacks its romaji right under it
      src.classList.add("split");
      for (const seg of segment(text, a.tk)) {
        if (!seg.text.trim()) { src.append(el("span", "sp-gap")); continue; }
        const t = seg.ti == null ? null : a.tk[seg.ti];
        const box = el("span", t ? "seg w" : "seg");
        const jp = el("span", "seg-jp"); jp.textContent = seg.text.trim();
        const ro = el("span", "seg-ro"); ro.lang = "ja-Latn"; ro.textContent = (t && t.p !== "en" && t.r) || " ";
        box.append(jp, ro);
        if (t) { box.dataset.ti = seg.ti; box.tabIndex = 0; box.setAttribute("role", "button"); }
        src.append(box);
      }
    } else src.textContent = text;
    body.append(src);
    if (a) {
      if (a.ro && !split) { const ro = el("p", "ln-ro"); ro.lang = "ja-Latn"; ro.textContent = a.ro; body.append(ro); }
      if (a.zh) { const zh = el("p", "ln-zh"); zh.lang = "zh-Hant"; zh.textContent = a.zh; body.append(zh); }
    } else if (running) {
      const zh = el("p", "ln-zh"); zh.textContent = "· · ·"; body.append(zh);
    }
    const play = el("button", "ln-play"); play.type = "button"; play.setAttribute("aria-label", "朗讀這句"); play.innerHTML = PLAY_SVG; play.disabled = !("speechSynthesis" in window);
    li.append(body, play); ol.append(li);
  }
  if (state.speaking >= 0) markSpeaking(state.speaking);
  if (state.sel) {
    const w = document.querySelector(`.ln[data-n="${state.sel.n}"] .w[data-ti="${state.sel.ti}"]`);
    if (w) { w.classList.add("sel"); tipFor = w; placeTip(); } else hideTip();
  }
}

$("#lyrics").addEventListener("click", (e) => {
  const li = e.target.closest(".ln"); if (!li) return;
  const n = Number(li.dataset.n); const w = e.target.closest(".w");
  if (w) { tapWord(n, Number(w.dataset.ti), w); return; }
  hideTip(); sayLine(n);
});
$("#lyrics").addEventListener("keydown", (e) => {
  const w = e.target.closest && e.target.closest(".w");
  if (w && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); w.click(); }
});
$("#tgRo").addEventListener("click", () => { state.showRo = !state.showRo; store.set("kaze.ro", state.showRo); $("#tgRo").setAttribute("aria-pressed", String(state.showRo)); $("#lyrics").classList.toggle("hide-ro", !state.showRo); });
$("#tgZh").addEventListener("click", () => { state.showZh = !state.showZh; store.set("kaze.zh", state.showZh); $("#tgZh").setAttribute("aria-pressed", String(state.showZh)); $("#lyrics").classList.toggle("hide-zh", !state.showZh); });
$("#speedBtn").addEventListener("click", () => { state.rate = RATES[(RATES.indexOf(state.rate) + 1) % RATES.length]; store.set("kaze.rate", state.rate); $("#speedBtn").textContent = state.rate.toFixed(1) + "×"; });

/* ---------- word tip: tap a word to hear it and see romaji · part of speech · meaning ---------- */
function tapWord(n, ti, wEl) {
  const s = songByKey(state.view); const rec = getRec(s.key); const L = state.lines[n];
  const a = L && rec ? rec.ann[L.u] : null; const t = a && a.tk ? a.tk[ti] : null;
  if (!t) return;
  document.querySelectorAll(".w.sel").forEach((x) => x.classList.remove("sel"));
  wEl.classList.add("sel");
  state.sel = { n, ti };
  markSpeaking(-1);
  speak(t.k || t.t, t.p === "en" ? "en" : "ja");
  $("#tipText").textContent = [t.k, t.r, POS_ZH[t.p] || "其他", t.m].filter(Boolean).join(" · ");
  $("#tip").hidden = false;
  tipFor = wEl;
  placeTip();
}
let tipFor = null;
// Keep the tip pinned to its word while the page scrolls or resizes; close it once the word leaves the screen.
function placeTip() {
  const tip = $("#tip");
  if (tip.hidden || !tipFor || !tipFor.isConnected) return;
  const r = tipFor.getBoundingClientRect();
  if (r.bottom < 0 || r.top > window.innerHeight) { hideTip(); return; }
  const tw = tip.offsetWidth, th = tip.offsetHeight;
  const left = Math.max(12, Math.min(window.innerWidth - tw - 12, r.left + r.width / 2 - tw / 2));
  let top = r.top - th - 10; const below = top < 8;
  if (below) top = r.bottom + 10;
  tip.style.left = left + "px"; tip.style.top = top + "px";
  tip.style.setProperty("--ax", (r.left + r.width / 2 - left) + "px");
  tip.classList.toggle("below", below);
}
function hideTip() {
  $("#tip").hidden = true; state.sel = null; tipFor = null;
  document.querySelectorAll(".w.sel").forEach((x) => x.classList.remove("sel"));
}
document.addEventListener("pointerdown", (e) => {
  if ($("#tip").hidden) return;
  if (e.target.closest(".w") || e.target.closest("#tip")) return;
  hideTip();
});
window.addEventListener("scroll", placeTip, { passive: true });
window.addEventListener("resize", placeTip);
document.addEventListener("keydown", (e) => { if (e.key === "Escape") hideTip(); });

/* ---------- reading aloud: one line or one word at a time ---------- */
const synth = "speechSynthesis" in window ? window.speechSynthesis : null;
let voices = [], speakToken = 0, currentUtter = null;
function loadVoices() { try { voices = synth.getVoices() || []; } catch (e) { voices = []; } }
if (synth) { loadVoices(); synth.addEventListener ? synth.addEventListener("voiceschanged", loadVoices) : (synth.onvoiceschanged = loadVoices); }
const VOICE_PREF = { ja: ["Kyoko", "O-Ren", "Google 日本語", "Hattori", "Otoya", "Nanami"], en: ["Samantha", "Google US English", "Ava", "Alex", "Daniel"] };
function pickVoice(lang) {
  const pool = voices.filter((v) => v.lang && v.lang.toLowerCase().replace("_", "-").startsWith(lang));
  for (const name of VOICE_PREF[lang]) { const v = pool.find((x) => x.name.includes(name)); if (v) return v; }
  return pool[0] || null;
}
function speak(text, lang, done) {
  if (!synth) return;
  const my = ++speakToken;
  try { synth.cancel(); } catch (e) {}
  const u = new SpeechSynthesisUtterance(text);
  u.lang = lang === "ja" ? "ja-JP" : "en-US";
  const v = pickVoice(lang); if (v) u.voice = v;
  u.rate = state.rate;
  u.onend = u.onerror = () => { if (my === speakToken && done) done(); };
  currentUtter = u;
  synth.speak(u);
  if (synth.paused) synth.resume();
}
function stopSpeech() { speakToken++; markSpeaking(-1); if (synth) { try { synth.cancel(); } catch (e) {} } }
function markSpeaking(n) {
  state.speaking = n;
  document.querySelectorAll(".ln.now").forEach((x) => x.classList.remove("now"));
  if (n >= 0) { const li = document.querySelector(`.ln[data-n="${n}"]`); if (li) li.classList.add("now"); }
}
function sayLine(n) {
  const s = songByKey(state.view); const L = state.lines[n]; if (!L) return;
  markSpeaking(n);
  speak(L.text, lineLang(s, L.text), () => { if (state.speaking === n) markSpeaking(-1); });
}

/* ---------- routing ---------- */
function showCatalog() {
  stopSpeech(); hideTip();
  state.view = null; state.lines = [];
  document.body.className = "";
  $("#song").hidden = true; $("#catalog").hidden = false;
  window.scrollTo(0, catalogY);
  updateFocus();
  if (lastSongKey) { const row = document.querySelector(`.tk[data-key="${lastSongKey}"]`); if (row) row.focus({ preventScroll: true }); }
}
function route() {
  const m = /^#song-([a-z0-9-]+)$/.exec(location.hash);
  const s = m && songByKey(m[1]);
  if (s) showSong(s); else showCatalog();
}

renderHead();
const savedFilter = store.get("kaze.filter", "all");
setFilter(["all", "en", "ja"].includes(savedFilter) ? savedFilter : "all");
window.addEventListener("hashchange", route);
route();

