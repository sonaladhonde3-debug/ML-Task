# src/ranking/cooccurrence_graph.py

from collections import Counter
from itertools import combinations


def build_cooccurrence_counts(outfits_df) -> Counter:
    pair_counts = Counter()

    item_columns = [
        "hero_id",
        "second_id",
        "layer_id",
        "footwear_id",
        "accessory_1_id",
        "accessory_2_id",
    ]

    for _, row in outfits_df.iterrows():
        items = [row[col] for col in item_columns if str(row[col]).strip()]
        for a, b in combinations(sorted(items), 2):
            pair_counts[(a, b)] += 1

    return pair_counts


def pair_score(item_ids: list[str], pair_counts: Counter) -> float:
    if len(item_ids) < 2:
        return 0.0

    pairs = list(combinations(sorted(item_ids), 2))
    total = sum(pair_counts.get(pair, 0) for pair in pairs)
    max_possible = max(len(pairs), 1)

    return min(total / max_possible, 1.0)