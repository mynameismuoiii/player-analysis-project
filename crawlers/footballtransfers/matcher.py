from difflib import SequenceMatcher


def normalize_name(name):
    return str(name).lower().strip()


def similarity(a, b):
    return SequenceMatcher(None, normalize_name(a), normalize_name(b)).ratio() * 100


def match_player_name(target_name, candidate_names, min_score=75):
    best_name = None
    best_score = 0

    for candidate in candidate_names:
        score = similarity(target_name, candidate)

        if score > best_score:
            best_name = candidate
            best_score = score

    if best_score >= min_score:
        return best_name, best_score

    return None, best_score