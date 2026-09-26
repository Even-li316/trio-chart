"""Western sun-sign layer: element + modality."""
SIGNS = [
    ((3, 21), "Aries", "fire", "cardinal"), ((4, 20), "Taurus", "earth", "fixed"),
    ((5, 21), "Gemini", "air", "mutable"), ((6, 22), "Cancer", "water", "cardinal"),
    ((7, 23), "Leo", "fire", "fixed"), ((8, 23), "Virgo", "earth", "mutable"),
    ((9, 23), "Libra", "air", "cardinal"), ((10, 24), "Scorpio", "water", "fixed"),
    ((11, 23), "Sagittarius", "fire", "mutable"), ((12, 22), "Capricorn", "earth", "cardinal"),
    ((1, 20), "Aquarius", "air", "fixed"), ((2, 19), "Pisces", "water", "mutable"),
]
CN = {"Aries": "白羊", "Taurus": "金牛", "Gemini": "双子", "Cancer": "巨蟹", "Leo": "狮子",
      "Virgo": "处女", "Libra": "天秤", "Scorpio": "天蝎", "Sagittarius": "射手",
      "Capricorn": "摩羯", "Aquarius": "水瓶", "Pisces": "双鱼"}


def sign_of(birth: str) -> dict:
    mo, d = [int(x) for x in birth.split(" ")[0].split("-")[1:3]]
    sign = "Capricorn"
    for (sm, sd), name, el, mod in SIGNS:
        if (mo, d) >= (sm, sd):
            sign = name
    for (sm, sd), name, el, mod in SIGNS:
        if name == sign:
            return {"sign": name, "sign_cn": CN[name], "element": el, "modality": mod}
    return {"sign": "Capricorn", "sign_cn": "摩羯", "element": "earth", "modality": "cardinal"}


ELEMENT_PAIR = {("air", "fire"): 0.85, ("earth", "water"): 0.85, ("earth", "fire"): 0.55,
                ("fire", "water"): 0.50, ("air", "earth"): 0.55, ("air", "water"): 0.55}
