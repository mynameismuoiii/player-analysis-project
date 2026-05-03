from difflib import SequenceMatcher

from crawlers.footballtransfers.helpers import normalize_text, extract_market_value


def similarity(a: str, b: str) -> float:
    """
    Tính độ giống nhau giữa 2 chuỗi.
    """
    a = normalize_text(a)
    b = normalize_text(b)

    if not a or not b:
        return 0

    return SequenceMatcher(None, a, b).ratio()


def find_from_top_table(player_name, top_data):
    """
    Tìm cầu thủ trong bảng top:
    - match đúng tên
    - nếu không có thì fuzzy match
    """
    key = normalize_text(player_name)

    if key in top_data:
        result = top_data[key].copy()
        result["status"] = "TOP_EXACT"
        return result

    best_key = None
    best_score = 0

    for candidate_key in top_data.keys():
        score = similarity(key, candidate_key)

        if score > best_score:
            best_score = score
            best_key = candidate_key

    if best_key and best_score >= 0.88:
        result = top_data[best_key].copy()
        result["status"] = "TOP_FUZZY"
        return result

    return None


def find_value_from_page_text(page_text: str, target_player: str):
    """
    Tìm giá trị chuyển nhượng trên trang search.

    Cách làm:
    - tách page text thành từng dòng
    - tìm dòng giống tên cầu thủ
    - lấy các dòng gần đó
    - tìm giá €...M / €...K / €...B
    """
    lines = [line.strip() for line in page_text.splitlines() if line.strip()]

    best_result = None
    best_score = 0

    for i, line in enumerate(lines):
        score = similarity(target_player, line)

        if score < 0.60:
            continue

        nearby_lines = lines[i:i + 10]
        nearby_text = " ".join(nearby_lines)

        market_value_text = extract_market_value(nearby_text)

        if market_value_text and score > best_score:
            best_score = score
            best_result = {
                "matched_name": line,
                "market_value_text": market_value_text,
                "score": score,
            }

    if best_result and best_result["score"] >= 0.72:
        return best_result

    return None