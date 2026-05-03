import re
import unicodedata
from urllib.parse import quote_plus


def normalize_name(name: str) -> str:
    if not name:
        return ""

    name = str(name).strip().lower()
    name = unicodedata.normalize("NFKD", name)
    name = "".join(ch for ch in name if not unicodedata.combining(ch))

    name = re.sub(r"[^a-z0-9\s-]", "", name)
    name = re.sub(r"\s+", " ", name)

    return name.strip()


def build_search_url(player_name: str) -> str:
    query = quote_plus(player_name)
    return f"https://www.footballtransfers.com/en/search?search={query}"


def clean_value_text(text: str) -> str:
    if not text:
        return "N/a"

    text = str(text).strip()
    text = re.sub(r"\s+", " ", text)

    if text in ["-", "", "None", "nan", "NaN"]:
        return "N/a"

    return text


def value_to_number(value: str):
    if not value or value == "N/a":
        return None

    value = value.replace("€", "").replace("£", "").replace("$", "")
    value = value.replace(",", "").strip().lower()

    multiplier = 1

    if value.endswith("m"):
        multiplier = 1_000_000
        value = value[:-1]
    elif value.endswith("k"):
        multiplier = 1_000
        value = value[:-1]

    try:
        return float(value) * multiplier
    except ValueError:
        return None