"""BaZi (Four Pillars) extraction, built on lunar_python."""
from lunar_python import Solar

GAN_WUXING = {"甲":"木","乙":"木","丙":"火","丁":"火","戊":"土","己":"土","庚":"金","辛":"金","壬":"水","癸":"水"}
ZHI_WUXING = {"子":"水","丑":"土","寅":"木","卯":"木","辰":"土","巳":"火","午":"火","未":"土","申":"金","酉":"金","戌":"土","亥":"水"}
HIDE_W = [1.0, 0.5, 0.3, 0.2]
ELEMENTS = ["木","火","土","金","水"]


def chart(birth: str) -> dict:
    """birth: "YYYY-MM-DD HH:MM"; returns pillars, elements and a few classics."""
    date, _, clock = birth.partition(" ")
    y, mo, d = [int(x) for x in date.split("-")]
    hh, mm = ([int(x) for x in clock.split(":")] + [0, 0])[:2] if clock else (12, 0)
    solar = Solar.fromYmdHms(y, mo, d, hh, mm, 0)
    lunar = solar.getLunar()
    ec = lunar.getEightChar()
    pillars = [ec.getYear(), ec.getMonth(), ec.getDay(), ec.getTime()]
    gan = [p[0] for p in pillars]
    zhi = [p[1] for p in pillars]
    w = {e: 0.0 for e in ELEMENTS}
    for g in gan:
        w[GAN_WUXING[g]] += 1.0
    for z in zhi:
        w[ZHI_WUXING[z]] += 1.0
    for hs in [ec.getYearHideGan(), ec.getMonthHideGan(), ec.getDayHideGan(), ec.getTimeHideGan()]:
        for i, gg in enumerate(hs):
            w[GAN_WUXING[gg]] += HIDE_W[min(i, len(HIDE_W) - 1)]
    total = sum(w.values())
    return {
        "pillars": pillars, "gan": gan, "zhi": zhi,
        "day_master": gan[2], "day_master_element": GAN_WUXING[gan[2]],
        "wuxing_raw": w, "wuxing": {k: round(v / total, 4) for k, v in w.items()},
        "zodiac": lunar.getYearShengXiao(), "lunar_date": lunar.toString(),
        "nayin_day": ec.getDayNaYin(), "ming_gong": ec.getMingGong(), "tai_yuan": ec.getTaiYuan(),
    }
