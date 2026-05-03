from difflib import SequenceMatcher

from crawlers.footballtransfers.helpers import normalize_name


def similarity(a: str, b: str) -> float:
    a = normalize_name(a)
    b = normalize_name(b)

    if not a or not b:
        return 0.0

    return SequenceMatcher(None, a, b).ratio()


def is_good_match(source_name: str, candidate_name: str, threshold: float = 0.75) -> bool:
    return similarity(source_name, candidate_name) >= threshold


def find_best_match(source_name: str, candidates: list[dict]) -> dict | None:
    if not candidates:
        return None

    best = None
    best_score = 0

    for candidate in candidates:
        candidate_name = candidate.get("player_name", "")
        score = similarity(source_name, candidate_name)

        if score > best_score:
            best = candidate
            best_score = score

    if best is None:
        return None

    best["match_score"] = round(best_score, 3)

    if best_score < 0.75:
        return None

    return best