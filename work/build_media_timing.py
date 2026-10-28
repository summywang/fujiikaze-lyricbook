"""Build dist/data/media.{json,js}: official cover, Spotify link, YouTube sources and per-line timing.

Run from the repository root:  python3 work/build_media_timing.py [--refresh]

1. Covers and Spotify links come from work/media/media-map.json (verified Spotify metadata).
2. For each song, find the official YouTube art track ("Provided to YouTube by ..." upload on Fujii Kaze's
   channel) whose length matches the Spotify track, and confirm it is embeddable through oEmbed. The official
   video, when there is one, is a second source; its offset from the studio timing is usually unknown, so the
   listener aligns it once on the site.
3. Take LRCLIB synced lyrics whose duration matches the same recording, and align its cues to this site's own
   lyric lines in order. Only timestamps are kept; LRCLIB's lyric text is not stored in the repository.
   Lines without a confident match stay null ("待校對"); nothing is interpolated.

Network responses are cached in ../work/timing/cache (outside the repository).
"""
import difflib
import hashlib
import json
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CACHE = REPO.parent / "work" / "timing" / "cache"
UA_BROWSER = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
UA_LRCLIB = "kaze-lyricbook (https://github.com/summywang/fujiikaze-lyricbook)"
REFRESH = "--refresh" in sys.argv
DURATION_TOLERANCE = 2.0  # seconds between Spotify, YouTube and LRCLIB lengths of the same recording
MATCH_MIN = 0.6           # minimum text similarity for a lyric line to take a cue's timestamp
SHARE_MIN = 0.85          # lines sharing one cue must together read almost exactly like it
TODAY = time.strftime("%Y-%m-%d")


def fetch(url, ua, name):
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / name
    if path.exists() and not REFRESH:
        return path.read_text(encoding="utf-8")
    req = urllib.request.Request(url, headers={"User-Agent": ua, "Accept-Language": "en"})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                body = r.read().decode("utf-8")
            break
        except urllib.error.HTTPError as e:
            if e.code < 500 or attempt == 4:
                return json.dumps({"httpError": e.code})  # not cached, so a later run asks again
            time.sleep(2 + attempt * 3)
    path.write_text(body, encoding="utf-8")
    time.sleep(0.4)
    return body


# ---------- YouTube art track ----------
def youtube_search(key, query):
    html = fetch("https://www.youtube.com/results?search_query=" + urllib.parse.quote(query), UA_BROWSER, f"yt-search-{key}.html")
    m = re.search(r"var ytInitialData = (\{.*?\});</script>", html)
    out = []

    def walk(o):
        if isinstance(o, dict):
            if "videoRenderer" in o:
                v = o["videoRenderer"]
                snippet = "".join(r["text"] for s in v.get("detailedMetadataSnippets", []) for r in s.get("snippetText", {}).get("runs", []))
                length = v.get("lengthText", {}).get("simpleText", "")
                parts = [int(x) for x in length.split(":")] if length else []
                secs = sum(p * 60 ** i for i, p in enumerate(reversed(parts))) if parts else None
                out.append({
                    "id": v["videoId"],
                    "title": "".join(r["text"] for r in v["title"]["runs"]),
                    "owner": "".join(r["text"] for r in v.get("ownerText", {}).get("runs", [])),
                    "seconds": secs,
                    "snippet": snippet,
                })
            for x in o.values():
                walk(x)
        elif isinstance(o, list):
            for x in o:
                walk(x)

    if m:
        walk(json.loads(m.group(1)))
    return out


def fold(s):
    s = unicodedata.normalize("NFKC", s).casefold()
    return re.sub(r"[\s'’\-.,!?]", "", s)


def embeddable(video_id):
    oembed = json.loads(fetch(f"https://www.youtube.com/oembed?format=json&url=https://www.youtube.com/watch?v={video_id}", UA_BROWSER, f"yt-oembed-{video_id}.json"))
    return not oembed.get("httpError")


def find_art_track(key, title, seconds):
    queries = (f'"{title} · Fujii Kaze"', f'"{title}" Fujii Kaze "Provided to YouTube by"', f"{title} Fujii Kaze Provided to YouTube by Universal Music Group")
    for qi, query in enumerate(queries):
        for v in youtube_search(f"{key}-{qi}", query):
            if v["owner"] != "Fujii Kaze" or not v["snippet"].startswith("Provided to YouTube by"):
                continue
            if fold(v["title"]) != fold(title) or v["seconds"] is None or abs(v["seconds"] - seconds) > DURATION_TOLERANCE:
                continue
            if embeddable(v["id"]):
                return {**v, "query": query}
    return None


def video_photo(video_id):
    """The video's widest thumbnail without letterbox bars: maxresdefault when it exists, else mqdefault (320x180)."""
    url = f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, method="HEAD", headers={"User-Agent": UA_BROWSER}), timeout=20):
            return url
    except urllib.error.HTTPError:
        return f"https://i.ytimg.com/vi/{video_id}/mqdefault.jpg"


def video_seconds(video_id):
    page = fetch(f"https://www.youtube.com/watch?v={video_id}", UA_BROWSER, f"yt-watch-{video_id}.html")
    m = re.search(r'"lengthSeconds":"(\d+)"', page)
    return int(m.group(1)) if m else None


# ---------- LRCLIB ----------
TS = re.compile(r"\[(\d+):(\d+(?:\.\d+)?)\]")
JA = re.compile(r"[぀-ヿ㐀-鿿]")


def parse_lrc(text):
    cues = []
    for raw in text.splitlines():
        stamps = TS.findall(raw)
        body = TS.sub("", raw).strip()
        for mm, ss in stamps:
            cues.append({"t": round(int(mm) * 60 + float(ss), 2), "text": body})
    cues.sort(key=lambda c: c["t"])
    # Bilingual records repeat each Japanese cue with a romaji line at the same time; keep the Japanese one.
    out = []
    for c in cues:
        if out and out[-1]["t"] == c["t"] and JA.search(out[-1]["text"]) and not JA.search(c["text"]):
            continue
        out.append(c)
    for c in out:
        c["break"] = not re.sub(r"[♪♫♬\s]", "", c["text"])
    return out


def lrclib_candidates(key, names, seconds, tolerance=DURATION_TOLERANCE):
    seen, found = set(), []
    for i, name in enumerate(names):
        q = urllib.parse.urlencode({"track_name": name, "artist_name": "Fujii Kaze"})
        res = json.loads(fetch("https://lrclib.net/api/search?" + q, UA_LRCLIB, f"lrclib-{key}-{i}.json"))
        if isinstance(res, dict):
            raise SystemExit(f"LRCLIB unavailable for {key} ({res}); run again later")
        for r in res:
            if r["id"] in seen or not r.get("syncedLyrics") or r.get("duration") is None:
                continue
            seen.add(r["id"])
            if abs(r["duration"] - seconds) <= tolerance:
                found.append(r)
    return found


# ---------- alignment ----------
def kata_to_hira(s):
    return "".join(chr(ord(ch) - 0x60) if "ァ" <= ch <= "ヶ" else ch for ch in s)


def norm(s):
    s = unicodedata.normalize("NFKC", s)
    bare = re.sub(r"\([^)]*\)", "", s)
    # Backing vocals are often in parentheses; a line that is only backing vocals is compared by its contents.
    s = bare if re.sub(r"[\W_]", "", bare) else s
    s = kata_to_hira(s).casefold()
    return re.sub(r"[\W_]", "", s)


def sim(a, b):
    a, b = norm(a), norm(b)
    if not a or not b:
        return 0.0
    return difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()


def align(lines, cues):
    """Order-preserving alignment. A lyric line takes 1-3 consecutive cues, or 2-3 lines share one cue (they then
    share its window; the cue is never split by guesswork), or a line stays untimed. Cues may be skipped."""
    sing = [i for i, c in enumerate(cues) if not c["break"]]
    n, m = len(lines), len(sing)
    NEG = float("-inf")
    best = [[NEG] * (m + 1) for _ in range(n + 1)]
    back = [[None] * (m + 1) for _ in range(n + 1)]
    best[0][0] = 0.0
    for i in range(n + 1):
        for j in range(m + 1):
            cur = best[i][j]
            if cur == NEG:
                continue
            for ni, nj, step in ((i + 1, j, ("skip-line",)), (i, j + 1, ("skip-cue",))):
                if ni <= n and nj <= m and cur > best[ni][nj]:
                    best[ni][nj], back[ni][nj] = cur, (i, j, step)
            if i < n:
                for k in (1, 2, 3):
                    if j + k > m:
                        break
                    s = sim(lines[i], " ".join(cues[sing[j + x]]["text"] for x in range(k)))
                    if s >= MATCH_MIN and cur + s > best[i + 1][j + k]:
                        best[i + 1][j + k], back[i + 1][j + k] = cur + s, (i, j, ("match", k, s))
                for k in (2, 3):
                    if i + k > n or j >= m:
                        break
                    s = sim(" ".join(lines[i:i + k]), cues[sing[j]]["text"])
                    if s >= SHARE_MIN and cur + s * k > best[i + k][j + 1]:
                        best[i + k][j + 1], back[i + k][j + 1] = cur + s * k, (i, j, ("share", k, s))
    i, j, picks = n, m, {}
    while (i, j) != (0, 0):
        pi, pj, step = back[i][j]
        if step[0] == "match":
            picks[pi] = ([sing[pj + x] for x in range(step[1])], step[2])
        elif step[0] == "share":
            for x in range(step[1]):
                picks[pi + x] = ([sing[pj]], step[2])
        i, j = pi, pj
    return picks, best[n][m]


def timings_for(lines, cues, total):
    picks, score = align(lines, cues)
    rows = []
    for idx, text in enumerate(lines):
        if idx not in picks:
            rows.append(None)
            continue
        cue_ids, s = picks[idx]
        last = cue_ids[-1]
        end = cues[last + 1]["t"] if last + 1 < len(cues) else round(total, 2)
        rows.append([cues[cue_ids[0]]["t"], end, round(s, 2)])
    return rows, score


LONG_WINDOW = 8.0  # seconds; a sung line rarely lasts longer, so its end probably runs into an instrumental


def trim_long_windows(rows, chosen, candidates):
    """End a long window at an instrumental marker found in another LRCLIB record of the same recording.

    The other record must have a cue within 0.6s of the line's start, so both describe the same moment;
    the marker must fall inside the window. Without such evidence the window is left as it is."""
    others = [parse_lrc(r["syncedLyrics"]) for r in candidates if r["id"] != chosen["id"]]
    out = []
    for row in rows:
        if row is None or row[1] - row[0] <= LONG_WINDOW:
            out.append(row)
            continue
        s, e = row[0], row[1]
        ends = [c["t"] for cues in others if any(abs(x["t"] - s) <= 0.6 and not x["break"] for x in cues)
                for c in cues if c["break"] and s + 1 < c["t"] < e]
        out.append([s, min(ends), row[2]] if ends else row)
    return out


# ---------- build ----------
# Official uploads on Fujii Kaze's channel that the artist site's video page does not list.
EXTRA_MV = {"shinunoga-e-wa": ("dawrQnvwMTY", "Shinunoga E-Wa (Not a MV)"), "garden": ("vkPfKnUaq5k", "Garden (Not a MV)")}
EXTRA_AUDIO = {"masshiro": ("XwgL4C2WaU8", "\"真っ白\" (Official Audio)")}
SAME_LENGTH = 1.0  # seconds; an official video this close to the studio length is taken to start in step with it


def mv_offset_evidence(key, names, lines, studio_rows, mv_secs):
    """How much later the song runs in the video, when LRCLIB holds records synced to the video itself.

    A record whose length matches the video and whose cues sit a steady, non-zero amount after the studio
    timing is taken as synced to the video. Two such records must agree; otherwise the offset stays unknown
    (records at offset 0 are usually studio timings merely labelled with the video's length)."""
    found = []
    for r in lrclib_candidates(key + "-mv", names, mv_secs):
        if abs(r["duration"] - mv_secs) > 1.5:
            continue
        rows, _ = timings_for(lines, parse_lrc(r["syncedLyrics"]), mv_secs)
        d = [x[0] - y[0] for x, y in zip(rows, studio_rows) if x and y]
        if len(d) < len(lines) * 0.6:
            continue
        med = sorted(d)[len(d) // 2]
        if abs(med) >= 0.5 and sum(abs(x - med) <= 0.7 for x in d) >= 0.9 * len(d):
            found.append((r["id"], round(med, 2)))
    for i, (_, a) in enumerate(found):
        agree = [f for f in found if abs(f[1] - a) <= 0.3]
        if len(agree) >= 2:
            return round(sum(f[1] for f in agree) / len(agree), 2), [f[0] for f in agree]
    return None, [f[0] for f in found]


def main():
    media = json.loads((REPO / "work/media/media-map.json").read_text(encoding="utf-8"))
    lyrics = json.loads((REPO / "dist/data/lyrics.json").read_text(encoding="utf-8"))
    # Extra names LRCLIB may file a song under, besides its Spotify title.
    alt_names = {"michi-teyu-ku": ["Michi Teyu Ku (Overflowing)", "Michi Teyu Ku"], "masshiro": ["Masshiro", "masshiro (pure white)"],
                 "hachiko": ["Hachiko"], "nan-nan": ["Nan-Nan"], "workin-hard": ["Workin' Hard", "Workin Hard"],
                 "it-aint-over": ["It Ain't Over", "It Aint Over"], "its-alright": ["It's Alright"]}
    # Art tracks found once are kept here so a rebuild does not depend on YouTube's search ranking.
    art_file = REPO / "work/media/art-tracks.json"
    art_tracks = json.loads(art_file.read_text(encoding="utf-8")) if art_file.exists() else {}
    out, report = {}, {}
    for key, m in media.items():
        seconds = m["durationMs"] / 1000
        lines = [l.strip() for l in lyrics[key]["raw"].replace("\r", "").split("\n") if l.strip()]
        names = [m["title"]] + alt_names.get(key, [])
        entry = {
            "spotify": m["spotify"], "cover": m["coverUrl"], "thumb": m["thumbnailUrl"],
            "durationMs": m["durationMs"], "releaseDate": m["releaseDate"], "sources": [],
        }
        rep = {"title": m["title"], "lines": len(lines), "sources": []}
        # Each source is a YouTube video with the song-wide offset at which the studio timing applies to it;
        # null means the listener aligns it once.
        art = None if REFRESH else art_tracks.get(key)
        if art is None:
            art = find_art_track(key, m["title"], seconds)
            if art:
                art_tracks[key] = {"id": art["id"], "title": art["title"], "seconds": art["seconds"], "query": art["query"], "found": TODAY}
        if art:
            entry["sources"].append({"id": art["id"], "kind": "audio", "title": art["title"], "offset": 0})
        elif key in EXTRA_AUDIO and embeddable(EXTRA_AUDIO[key][0]):
            vid, title = EXTRA_AUDIO[key]; secs = video_seconds(vid)
            entry["sources"].append({"id": vid, "kind": "audio", "title": title,
                                     "offset": 0 if secs is not None and abs(secs - seconds) <= SAME_LENGTH else None})
        mv_id, mv_title = (m["youtubeId"], m["youtubeTitle"]) if m.get("youtubeId") else EXTRA_MV.get(key, (None, None))
        if mv_id and embeddable(mv_id):
            entry["sources"].append({"id": mv_id, "kind": "mv", "title": mv_title, "offset": None, "seconds": video_seconds(mv_id)})
        if entry["sources"]:
            best = None
            # When every source is aligned by the listener anyway, a record a little off in length still helps:
            # the alignment absorbs a constant difference.
            tol = DURATION_TOLERANCE if any(src["offset"] == 0 for src in entry["sources"]) else 3.0
            candidates = lrclib_candidates(key, names, seconds, tol)
            for r in candidates:
                rows, score = timings_for(lines, parse_lrc(r["syncedLyrics"]), seconds)
                timed = sum(x is not None for x in rows)
                if best is None or (timed, score) > (best[1], best[2]):
                    best = (r, timed, score, rows)
            if best:
                r, timed, score, rows = best
                rows = trim_long_windows(rows, r, candidates)
                entry["timing"] = {
                    "lyricsSha": hashlib.sha256(lyrics[key]["raw"].encode()).hexdigest()[:12],
                    "source": {"provider": "LRCLIB", "id": r["id"], "duration": r["duration"]},
                    "lines": [None if x is None else x[:2] for x in rows],
                }
                rep["lrclib"] = {"id": r["id"], "album": r["albumName"], "duration": r["duration"], "timed": timed,
                                 "low": [[i, lines[i], x[2]] for i, x in enumerate(rows) if x and x[2] < 0.8],
                                 "untimed": [[i, lines[i]] for i, x in enumerate(rows) if x is None]}
                for src in entry["sources"]:
                    if src["kind"] != "mv" or src["seconds"] is None:
                        continue
                    if abs(src["seconds"] - seconds) <= SAME_LENGTH:
                        src["offset"] = 0
                        src["offsetBasis"] = "same length as the studio track"
                    else:
                        off, ids = mv_offset_evidence(key, names, lines, rows, src["seconds"])
                        if off is not None:
                            src["offset"] = off
                            src["offsetBasis"] = f"LRCLIB records {ids} synced to this video"
        for src in entry["sources"]:
            src.pop("seconds", None)
            rep["sources"].append(dict(src))
        # The song's photo on the site: a frame from its official video, else from its audio upload.
        pick = next((x for x in entry["sources"] if x["kind"] == "mv"), entry["sources"][0] if entry["sources"] else None)
        if pick:
            entry["photo"] = video_photo(pick["id"])
        out[key] = entry
        report[key] = rep
        srcs = " ".join(f"{s['kind']}:{s['id']}@{s['offset']}" for s in entry["sources"]) or "-"
        print(f"{key:16} timed={rep.get('lrclib', {}).get('timed', 0):3}/{len(lines):<3} {srcs}")
    art_file.write_text(json.dumps(art_tracks, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    data = REPO / "dist/data"
    (data / "media.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (data / "media.js").write_text("const MEDIA = " + json.dumps(out, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")
    (REPO / "work/media/timing-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
