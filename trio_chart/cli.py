"""Command line: python -m trio_chart --a a.json --b b.json --svg out.svg"""
import argparse, json, sys
from pathlib import Path
from .engine import run
from .render import svg
from . import bazi, zodiac


def _person(raw: dict) -> dict:
    bz = bazi.chart(raw["birth"])
    z = zodiac.sign_of(raw["birth"])
    return {"name": raw.get("name", "A"), "birth": raw["birth"], "mbti": raw.get("mbti"),
            "big5": raw.get("big5"), "bazi": bz, "zodiac": z}


def main(argv=None):
    ap = argparse.ArgumentParser(prog="trio_chart")
    ap.add_argument("--a", required=True); ap.add_argument("--b", required=True)
    ap.add_argument("--svg"); ap.add_argument("--json")
    args = ap.parse_args(argv)
    a = _person(json.loads(Path(args.a).read_text(encoding="utf-8")))
    b = _person(json.loads(Path(args.b).read_text(encoding="utf-8")))
    rep = run(a, b)
    rep["people"] = {"a": a["name"], "b": b["name"],
                     "a_pillars": a["bazi"]["pillars"], "b_pillars": b["bazi"]["pillars"],
                     "a_sign": a["zodiac"]["sign_cn"], "b_sign": b["zodiac"]["sign_cn"]}
    text = json.dumps(rep, ensure_ascii=False, indent=2)
    print(text)
    if args.json:
        Path(args.json).write_text(text, encoding="utf-8")
    if args.svg:
        Path(args.svg).write_text(svg(rep, a["name"], b["name"]), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
