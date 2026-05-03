import re
import unicodedata


def normalize_text(text):
    if text is None:
        return ""

    text = str(text).strip().lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))

    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text)

    return text


def safe_value(value):
    if value is None:
        return "N/a"

    value = str(value).strip()

    if value == "" or value.lower() in ["nan", "none", "n/a"]:
        return "N/a"

    return value