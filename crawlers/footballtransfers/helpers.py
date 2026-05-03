import re
import unicodedata


def normalize_text(text: str) -> str:
    """
    Chuẩn hóa text để so khớp tên cầu thủ:
    - viết thường
    - bỏ dấu
    - bỏ ký tự đặc biệt
    - xóa khoảng trắng thừa
    """
    if text is None:
        return ""

    text = str(text).lower().strip()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def parse_market_value(value_text: str):
    """
    Chuyển giá trị:
    €50M -> 50000000
    €750K -> 750000
    €1.2B -> 1200000000
    """
    if not value_text or value_text == "N/a":
        return None

    text = str(value_text)
    text = text.replace("€", "").replace(",", "").replace(" ", "").strip().upper()

    try:
        if text.endswith("M"):
            return float(text[:-1]) * 1_000_000
        if text.endswith("K"):
            return float(text[:-1]) * 1_000
        if text.endswith("B"):
            return float(text[:-1]) * 1_000_000_000

        return float(text)

    except ValueError:
        return None


def extract_market_value(text: str):
    """
    Tìm giá dạng €50M / €750K / €1.2M trong text.
    """
    if not text:
        return None

    pattern = re.compile(r"€\s?\d+(?:\.\d+)?\s?[KMB]", re.IGNORECASE)
    match = pattern.search(str(text))

    if match:
        return match.group(0).replace(" ", "")

    return None