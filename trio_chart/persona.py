"""Self-reported personality layer: MBTI axis match + optional Big Five agreement."""
MBTI_AXES = [("E", "I"), ("S", "N"), ("T", "F"), ("J", "P")]
# same-ends vs opposite-ends weight, per axis (published, auditable rule table)
AXIS_MATCH = {"EI": (0.75, 0.55), "SN": (0.85, 0.45), "TF": (0.80, 0.50), "JP": (0.80, 0.50)}


def parse(mbti: str) -> dict:
    m = (mbti or "").strip().upper()
    if len(m) != 4 or any(m[i] not in MBTI_AXES[i] for i in range(4)):
        raise ValueError("MBTI must be 4 letters from the 16-type set, e.g. INFP")
    return {MBTI_AXES[i][0] + MBTI_AXES[i][1]: m[i] for i in range(4)}


def axes_score(a: str, b: str) -> tuple:
    pa, pb = parse(a), parse(b)
    parts, notes = [], []
    for key, (same, diff) in AXIS_MATCH.items():
        left = key[0]
        sa = pa[key] == left
        sb = pb[key] == left
        hit = sa == sb
        parts.append(same if hit else diff)
        if key == "SN" and not hit:
            notes.append("S/N differs: information style differs most, expect translation cost")
        if key == "EI" and not hit:
            notes.append("E/I differs: different social batteries, plan recharge time")
        if key in ("TF", "JP") and not hit:
            notes.append("%s differs: needs explicit negotiation, not intuition" % key)
    return sum(parts) / len(parts), notes


def big5_score(a: dict, b: dict) -> tuple:
    if not a or not b:
        return None, []
    keys = sorted(set(a) & set(b))
    if not keys:
        return None, []
    # similarity on a 1-5 scale, then two "complementary" traits get credit for difference
    sims = [1 - abs(float(a[k]) - float(b[k])) / 4 for k in keys]
    base = sum(sims) / len(sims)
    notes = []
    if "N" in keys and abs(float(a["N"]) - float(b["N"])) >= 1.5:
        notes.append("Big Five N differs a lot: one is much more reactive to stress")
    if "A" in keys and min(float(a["A"]), float(b["A"])) >= 4:
        notes.append("both high agreeableness: low friction, but watch conflict avoidance")
    return base, notes
