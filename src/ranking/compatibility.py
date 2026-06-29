# src/ranking/compatibility.py

from dataclasses import dataclass
from statistics import mean
from itertools import combinations
import math


@dataclass
class CompatibilityBreakdown:
    occasion_match: float
    category_completeness: float
    embedding_cohesion: float
    curated_cooccurrence: float
    palette_harmony: float
    total_score: float


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def score_occasion_match(outfit_items: list[dict], user_occasion: str) -> float:
    if not user_occasion:
        return 1.0
    hits = sum(1 for item in outfit_items if item.get("occasion") == user_occasion)
    return hits / max(len(outfit_items), 1)


def score_category_completeness(outfit_items: list[dict]) -> float:
    labels = {item.get("category_label", "").lower() for item in outfit_items}
    has_dress = any("dress" in label for label in labels)

    has_top = any(label in {
        "formal shirts", "shirts", "t-shirts", "tops", "sweatshirts", "kurtas"
    } for label in labels)

    has_bottom = any(label in {
        "trousers", "jeans", "chinos", "skirts", "palazzos", "leggings"
    } for label in labels)

    has_footwear = any(label in {
        "formal shoes", "heels", "boots", "sneakers", "sandals", "ethnic footwear"
    } for label in labels)

    if has_dress and has_footwear:
        return 1.0

    score = 0
    score += 1 if has_top else 0
    score += 1 if has_bottom else 0
    score += 1 if has_footwear else 0
    return score / 3.0


def score_embedding_cohesion(outfit_items: list[dict]) -> float:
    vectors = [item.get("embedding") for item in outfit_items if item.get("embedding") is not None]
    if len(vectors) < 2:
        return 0.5

    sims = [cosine_similarity(a, b) for a, b in combinations(vectors, 2)]
    return (mean(sims) + 1.0) / 2.0


def score_palette_harmony(outfit_items: list[dict]) -> float:
    colors = [item.get("dominant_color", "").lower() for item in outfit_items if item.get("dominant_color")]
    if not colors:
        return 0.5

    neutral = {"black", "white", "grey", "gray", "beige", "brown", "navy"}
    unique_colors = set(colors)

    if len(unique_colors) == 1:
        return 0.85
    if any(c in neutral for c in unique_colors) and len(unique_colors) <= 3:
        return 0.90
    if len(unique_colors) <= 3:
        return 0.75
    return 0.50


def compute_compatibility_score(
    outfit_items: list[dict],
    user_occasion: str,
    curated_cooccurrence_score: float,
    weights: dict[str, float],
) -> CompatibilityBreakdown:
    occasion_match = score_occasion_match(outfit_items, user_occasion)
    category_completeness = score_category_completeness(outfit_items)
    embedding_cohesion = score_embedding_cohesion(outfit_items)
    palette_harmony = score_palette_harmony(outfit_items)

    total = (
        weights["occasion_match"] * occasion_match
        + weights["category_completeness"] * category_completeness
        + weights["embedding_cohesion"] * embedding_cohesion
        + weights["curated_cooccurrence"] * curated_cooccurrence_score
        + weights["palette_harmony"] * palette_harmony
    )

    return CompatibilityBreakdown(
        occasion_match=occasion_match,
        category_completeness=category_completeness,
        embedding_cohesion=embedding_cohesion,
        curated_cooccurrence=curated_cooccurrence_score,
        palette_harmony=palette_harmony,
        total_score=round(total, 4),
    )