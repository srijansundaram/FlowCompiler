# ai_hooks.py — AI-assisted syntax and keyword suggestion system
import difflib


KNOWN_KEYWORDS = [
    "load", "as", "pipeline", "filter", "sum", "group_by", "emit",
    "dropduplicates", "sortby", "avg", "average", "ensure", "join",
    "rename", "select"
]

def suggest_keyword(word: str):

    matches = difflib.get_close_matches(word, KNOWN_KEYWORDS, n=1, cutoff=0.5)
    if matches:
        ratio = int(difflib.SequenceMatcher(None, word, matches[0]).ratio() * 100)
        if ratio >= 65: 
            return f"{matches[0]} ({ratio}% match)"
    return None


def detect_invalid_keywords(src: str):

    found = []
    lines = src.splitlines()

    for i, line in enumerate(lines, start=1):
        if not line.strip() or line.strip().startswith("#"):
            continue

        tokens = [w for w in line.replace("|>", "").replace(":", "").split() if w.isalpha()]

        skip_next = False
        for w in tokens:
            if skip_next:
                skip_next = False
                continue
            if w.lower() == "as":
                skip_next = True
                continue
            if w.lower() in ["to", "on"]:
                continue
            if w not in KNOWN_KEYWORDS:
                suggestion = suggest_keyword(w)
                if suggestion:
                    found.append((i, w, suggestion))
    return found

def auto_correct_source(src: str, issues: list):
    lines = src.splitlines()
    for line_num, wrong, suggestion in issues:
        if not suggestion:
            continue
        corrected = suggestion.split()[0]

        if corrected in ["rename", "as", "to", "on"]:
            continue

        line = lines[line_num - 1]
        lines[line_num - 1] = line.replace(wrong, corrected)
    return "\n".join(lines)
