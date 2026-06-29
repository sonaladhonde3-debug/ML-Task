# src/outfit/assembler.py

from src.outfit.slots import TOPWEAR, BOTTOMWEAR, FOOTWEAR, ACCESSORIES, LAYERS, DRESSES


def label_of(item: dict) -> str:
    return item.get("category_label", "").strip().lower()


def assemble_outfit(candidates: list[dict]) -> dict:
    chosen = {
        "hero": None,
        "bottomwear": None,
        "footwear": None,
        "layer": None,
        "accessory": None,
    }

    sorted_candidates = sorted(candidates, key=lambda x: x.get("retrieval_score", 0), reverse=True)

    dress = next((x for x in sorted_candidates if label_of(x) in DRESSES), None)
    if dress:
        chosen["hero"] = dress
        chosen["footwear"] = next((x for x in sorted_candidates if label_of(x) in FOOTWEAR), None)
        chosen["accessory"] = next((x for x in sorted_candidates if label_of(x) in ACCESSORIES), None)
        return chosen

    chosen["hero"] = next((x for x in sorted_candidates if label_of(x) in TOPWEAR), None)
    chosen["bottomwear"] = next((x for x in sorted_candidates if label_of(x) in BOTTOMWEAR), None)
    chosen["footwear"] = next((x for x in sorted_candidates if label_of(x) in FOOTWEAR), None)
    chosen["layer"] = next((x for x in sorted_candidates if label_of(x) in LAYERS), None)
    chosen["accessory"] = next((x for x in sorted_candidates if label_of(x) in ACCESSORIES), None)

    return chosen