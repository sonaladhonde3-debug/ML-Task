# src/explain/generator.py

def generate_explanation(profile: dict, outfit: dict, rationale_examples: list[str]) -> str:
    items = [v for v in outfit.values() if v]
    item_names = [item["name"] for item in items]

    base = []
    if profile.get("occasion"):
        base.append(f"This outfit is aligned with a {profile['occasion']} use case.")
    if profile.get("style"):
        base.append(f"It stays close to a {profile['style']} styling preference.")

    base.append(
        f"The selected pieces work together as a complete look: {', '.join(item_names)}."
    )

    if rationale_examples:
        base.append(
            f"This recommendation is also grounded in curated stylist patterns such as: {rationale_examples[0]}"
        )

    return " ".join(base)