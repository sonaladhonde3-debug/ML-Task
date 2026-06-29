# src/intent_parser.py

import re


def parse_user_query(query: str) -> dict:
    q = query.lower()

    gender = None
    if "male" in q or "men" in q or "man" in q:
        gender = "men"
    elif "female" in q or "women" in q or "woman" in q:
        gender = "women"

    occasion_keywords = {
        "office": ["office", "meeting", "interview", "work", "business"],
        "party": ["party", "night out", "club"],
        "wedding": ["wedding", "reception"],
        "casual": ["casual", "everyday", "daily"],
        "vacation": ["vacation", "beach", "travel", "summer trip"],
        "festive": ["festive", "festival", "celebration"],
        "winter": ["winter", "cold"],
        "sports": ["sports", "gym", "workout", "running"],
    }

    occasion = None
    for label, keys in occasion_keywords.items():
        if any(key in q for key in keys):
            occasion = label
            break

    age = None
    age_match = re.search(r"\b(\d{2})\b", q)
    if age_match:
        age = int(age_match.group(1))

    style = None
    for s in ["formal", "smart casual", "casual", "ethnic", "western"]:
        if s in q:
            style = s
            break

    return {
        "raw_query": query,
        "gender": gender,
        "occasion": occasion,
        "age": age,
        "style": style,
    }