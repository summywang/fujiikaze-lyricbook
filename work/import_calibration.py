"""Apply a browser timing export to the matching published videos, without changing audio timings."""
import argparse
import copy
import json
import math
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def apply_records(media, payload):
    if payload.get("format") != "kaze-calibration" or payload.get("version") != 1:
        raise ValueError("Unsupported calibration backup")
    result = copy.deepcopy(media)
    seen = set()
    for record in payload["records"]:
        key, video = record["song"], record["videoId"]
        if (key, video) in seen:
            raise ValueError("Duplicate song/video calibration")
        seen.add((key, video))
        song = result[key]
        timing = song["timing"]
        if timing["lyricsSha"] != record["lyricsSha"]:
            raise ValueError(f"Lyrics changed for {key}; do not reuse these timings")
        source = next(s for s in song["sources"] if s["id"] == video)
        data = record["data"]
        if set(data) - {"o", "l"} or not isinstance(data.get("l"), dict):
            raise ValueError(f"Invalid calibration structure: {key}")
        if "o" in data and (type(data["o"]) not in (int, float) or not math.isfinite(data["o"])):
            raise ValueError(f"Invalid video offset: {key}")
        for n, values in data["l"].items():
            if not n.isdigit() or not 0 <= int(n) < len(timing["lines"]) or not isinstance(values, dict):
                raise ValueError(f"Invalid line index: {key}/{n}")
            if set(values) - {"s", "e", "ok"}:
                raise ValueError(f"Unknown timing fields: {key}/{n}")
            for field in ("s", "e"):
                if field in values and (type(values[field]) not in (int, float) or not math.isfinite(values[field])):
                    raise ValueError(f"Invalid seconds: {key}/{n}/{field}")
            if "s" in values and "e" in values and values["e"] <= values["s"]:
                raise ValueError(f"Line end is not after start: {key}/{n}")
        source["calibration"] = {"lyricsSha": record["lyricsSha"], "data": copy.deepcopy(data)}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("backup", type=Path)
    args = parser.parse_args()
    payload = json.loads(args.backup.read_text(encoding="utf-8"))
    data = REPO / "dist/data"
    media = apply_records(json.loads((data / "media.json").read_text(encoding="utf-8")), payload)
    (data / "media.json").write_text(json.dumps(media, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (data / "media.js").write_text("const MEDIA = " + json.dumps(media, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")
    print(f"Applied {len(payload['records'])} video calibrations. Bump media.js's version in index.html before publishing.")


if __name__ == "__main__":
    main()
