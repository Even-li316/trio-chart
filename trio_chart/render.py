"""One-glance SVG: three channels, one total, no jargon."""


def svg(report: dict, name_a: str, name_b: str) -> str:
    ch = report["channels"]
    rows = [("BaZi five elements", ch["bazi"]), ("Sun sign layer", ch["zodiac"]),
            ("Personality axes", ch["persona"])]
    y = 210
    bars = ""
    for label, val in rows:
        bars += ('<text x="60" y="%d" fill="#cfd8dc" font-size="20">%s</text>'
                 '<rect x="60" y="%d" width="640" height="20" rx="10" fill="#263238"/>'
                 '<rect x="60" y="%d" width="%d" height="20" rx="10" fill="#ff7a45"/>'
                 '<text x="716" y="%d" fill="#ffb08a" font-size="20">%.0f</text>'
                 % (y - 12, label, y, y, int(640 * val / 100), y + 16, val))
        y += 78
    return """<svg xmlns="http://www.w3.org/2000/svg" width="800" height="560" viewBox="0 0 800 560">
<rect width="800" height="560" fill="#0f1416"/>
<text x="60" y="80" fill="#ff7a45" font-size="26" font-weight="bold">TrioChart</text>
<text x="60" y="120" fill="#ffffff" font-size="34" font-weight="bold">%s  ×  %s</text>
<text x="700" y="120" fill="#ff7a45" font-size="52" font-weight="bold">%.0f</text>
<text x="700" y="150" fill="#90a4ae" font-size="16">total /100</text>
%s
<text x="60" y="440" fill="#90a4ae" font-size="15">confidence %.2f - self-reported inputs only, rules are open in engine.py</text>
<text x="60" y="470" fill="#546e7a" font-size="14">For entertainment and cultural research. No medical, legal or financial advice.</text>
<text x="60" y="500" fill="#546e7a" font-size="14">BaZi via lunar-python; scoring rules are published and replaceable, not a prediction.</text>
<text x="60" y="530" fill="#37474f" font-size="13">github.com/Even-li316</text>
</svg>""" % (name_a, name_b, report["total"], bars, report["confidence"])
