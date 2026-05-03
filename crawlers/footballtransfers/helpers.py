import re


def build_search_url(player_name: str) -> str:
    query = str(player_name).strip().replace(" ", "%20")
    return f"https://www.footballtransfers.com/en/search?q={query}"


def market_value_to_number(value):
    if value is None:
        return None

    value = str(value).replace("€", "").replace(",", "").replace(" ", "").strip()

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