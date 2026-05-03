import re
import unicodedata


def clean_text(value):
    if value is None:
        return "N/a"

    value = str(value).strip()
    return value if value else "N/a"


def normalize_name(name):
    if name is None:
        return ""

    name = str(name).lower().strip()
    name = unicodedata.normalize("NFD", name)
    name = name.encode("ascii", "ignore").decode("utf-8")
    name = re.sub(r"[^a-z0-9\s]", "", name)
    name = re.sub(r"\s+", " ", name)
    return name


def market_value_to_number(value):
    if value is None:
        return None

    value = str(value).strip()
    value = value.replace("€", "").replace(",", "").replace(" ", "")

    if value in ["", "-", "N/a", "N/A"]:
        return None

    multiplier = 1

    if value.lower().endswith("m"):
        multiplier = 1_000_000
        value = value[:-1]
    elif value.lower().endswith("k"):
        multiplier = 1_000
        value = value[:-1]

    try:
        return float(value) * multiplier
    except Exception:
        return None