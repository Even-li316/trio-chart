"""Three-channel engine. Every rule is in code so it can be read, audited and replaced."""
from . import bazi, zodiac, persona

WEIGHTS = {"bazi": 0.4, "zodiac": 0.3, "persona": 0.3}
ELEMENTS = bazi.ELEMENTS


def _cos(a: dict, b: dict) -> float:
    keys = ELEMENTS
    num = sum(a[k] * b[k] for k in keys)
    da = sum(a[k] ** 2 for k in keys) ** 0.5
    db = sum(b[k] ** 2 for k in keys) ** 0.5
    return num / (da * db) if da and db else 0.0


def _complement(a: dict, b: dict) -> tuple:
    """How much each side supplies what the other lacks."""
    mean = 1 / len(ELEMENTS)
    out = {}
    for x, y in (("a", "b"), ("b", "a")):
        lack = {k: max(0.0, mean - (a if x == "a" else b)[k]) for k in ELEMENTS}
        supply = (b if x == "a" else a)
        out[x] = sum(lack[k] * supply[k] for k in ELEMENTS) / (sum(lack.values()) or 1)
    return out["a"], out["b"]


def run(a: dict, b: dict) -> dict:
    ba, bb = bazi.chart(a["birth"]), bazi.chart(b["birth"])
    za, zb = zodiac.sign_of(a["birth"]), zodiac.sign_of(b["birth"])
    sim = _cos(ba["wuxing"], bb["wuxing"])
    ca, cb = _complement(ba["wuxing"], bb["wuxing"])
    bazi_score = 100 * (0.5 * sim + 0.5 * (ca + cb) / 2)

    pair = tuple(sorted([za["element"], zb["element"]]))
    if pair[0] == pair[1]:
        zs, znote = 0.90, "same element: same tempo, risk of shared blind spot"
    else:
        zs = zodiac.ELEMENT_PAIR.get(pair, 0.6)
        znote = "element pair %s-%s" % pair
    zs += 0.05 if za["modality"] == zb["modality"] else 0.0
    zodiac_score = 100 * min(zs, 1.0)

    pnote = []
    if a.get("mbti") and b.get("mbti"):
        ps, pnote = persona.axes_score(a["mbti"], b["mbti"])
        b5, n5 = persona.big5_score(a.get("big5"), b.get("big5"))
        pnote = pnote + n5
        if b5 is not None:
            ps = 0.7 * ps + 0.3 * b5
    else:
        ps = 0.5
        pnote = ["no personality input given: this channel is a placeholder"]
    persona_score = 100 * ps

    scores = {"bazi": bazi_score, "zodiac": zodiac_score, "persona": persona_score}
    total = sum(scores[k] * WEIGHTS[k] for k in scores)
    conf = 0.75 if (a.get("mbti") and b.get("mbti")) else 0.55
    if not a.get("birth", "").count(":") or not b.get("birth", "").count(":"):
        conf -= 0.1

    return {
        "total": round(total, 1), "confidence": round(conf, 2),
        "channels": {k: round(v, 1) for k, v in scores.items()}, "weights": WEIGHTS,
        "bazi": {"a": ba, "b": bb, "cosine": round(sim, 3), "complement": [round(ca, 3), round(cb, 3)]},
        "zodiac": {"a": za, "b": zb, "note": znote},
        "persona_notes": pnote,
        "why": [
            "five-element overlap %.2f, mutual supply a->b %.2f b->a %.2f" % (sim, ca, cb),
            "day masters %s vs %s" % (ba["day_master"], bb["day_master"]),
            "sun signs %s(%s) vs %s(%s)" % (za["sign_cn"], za["element"], zb["sign_cn"], zb["element"]),
        ],
    }
