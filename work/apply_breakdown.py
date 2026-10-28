"""Merge work/breakdown/<song>.json into dist/data/lyrics.{json,js}.

Run from the repository root:
  python3 work/apply_breakdown.py shinunoga-e-wa [more-song-keys ...]   write into the site data
  python3 work/apply_breakdown.py --check nan-nan damn                  only validate, write nothing

Every Japanese chunk in the song's word data takes its meaning (m), parts (b), sentence pattern (g) and tag
from the breakdown file, matched by the chunk's text. The song is marked tipV 2, which tells the site to show
the newer word tip (parts listed, tag only for 慣用語 / 口語 / 方言). English words and interjections are left as they are.
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKIP = {"sym", "en", "interj"}
TAGS = {"慣用語", "口語", "方言"}
KANJI = re.compile(r"[㐀-鿿々]")
KANA = re.compile(r"^[぀-ヿー・ ]+$")
# Grammar terms the tips avoid; explanations stay in plain words.
JARGON = ("使役", "て形", "連用", "連體", "未然", "終止", "命令形", "可能形", "受身", "被動形", "助動詞", "接續形", "活用", "語幹", "格助詞", "副助詞", "終助詞")
LOOSE = re.compile(r"[\s、。，,!?！？…~〜「」（）()]")


def problems(key, rec, chunks):
    """Everything wrong with one song's breakdown file, as readable lines."""
    out, used = [], set()
    for ann in rec["ann"]:
        for t in (ann or {}).get("tk", []):
            if t.get("p") in SKIP:
                continue
            if t["t"] not in chunks:
                out.append(f"no entry for chunk {t['t']!r}")
            used.add(t["t"])
    for text, c in chunks.items():
        where = f"{text!r}:"
        if text not in used:
            out.append(f"{where} not a chunk of this song (check the exact text)")
        if not isinstance(c.get("m"), str) or not c["m"].strip():
            out.append(f"{where} missing m")
        if c.get("tag") and c["tag"] not in TAGS:
            out.append(f"{where} tag must be one of {sorted(TAGS)}")
        if "g" in c and not (isinstance(c["g"], str) and "＝" in c["g"]):
            out.append(f"{where} g should read like 「〜のがいい ＝ 做…比較好」")
        parts = c.get("b")
        if parts is not None:
            if not (isinstance(parts, list) and len(parts) >= 2 and all(isinstance(p, list) and len(p) == 3 and all(isinstance(x, str) for x in p) for p in parts)):
                out.append(f"{where} b must be a list of at least two [part, reading, explanation]")
            else:
                joined, whole = LOOSE.sub("", "".join(p[0] for p in parts)), LOOSE.sub("", text)
                if whole not in (joined, joined * 2):
                    out.append(f"{where} parts spell {joined!r}, not the chunk")
                for part, reading, expl in parts:
                    if KANJI.search(part) and not (reading and KANA.match(reading)):
                        out.append(f"{where} part {part!r} has kanji, needs a kana reading")
                    if not KANJI.search(part) and reading:
                        out.append(f"{where} part {part!r} has no kanji, leave its reading empty")
                    if not expl.strip():
                        out.append(f"{where} part {part!r} has no explanation")
        text_all = " ".join([c.get("m", ""), c.get("g", "")] + [p[2] for p in (parts or []) if isinstance(p, list) and len(p) == 3])
        for word in JARGON:
            if word in text_all:
                out.append(f"{where} uses the grammar term {word!r}; say it in plain words")
    return out


def main(args):
    check = "--check" in args
    keys = [a for a in args if not a.startswith("--")] or ["shinunoga-e-wa"]
    path = REPO / "dist/data/lyrics.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    failed = False
    for key in keys:
        chunks = json.loads((REPO / f"work/breakdown/{key}.json").read_text(encoding="utf-8"))["chunks"]
        found = problems(key, data[key], chunks)
        if found:
            failed = True
            print(f"{key}: {len(found)} problem(s)")
            for line in found:
                print("  -", line)
            continue
        print(f"{key}: ok ({len(chunks)} chunks)")
        if check:
            continue
        for ann in data[key]["ann"]:
            for t in (ann or {}).get("tk", []):
                if t.get("p") in SKIP:
                    continue
                c = chunks[t["t"]]
                t["m"] = c["m"]
                for field in ("b", "g", "tag"):
                    if c.get(field):
                        t[field] = c[field]
                    else:
                        t.pop(field, None)
        data[key]["tipV"] = 2
    if failed:
        raise SystemExit("fix the problems above; nothing was written" if not check else 1)
    if not check:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        (REPO / "dist/data/lyrics.js").write_text("const PUBLISHED = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv[1:])
