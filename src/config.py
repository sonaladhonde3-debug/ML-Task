# src/config.py

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    project_root: Path = Path(__file__).resolve().parents[1]
    data_dir: Path = project_root / "data"
    artifacts_dir: Path = project_root / "artifacts"

    products_csv: Path = data_dir / "products.csv"
    outfits_csv: Path = data_dir / "outfits.csv"
    images_dir: Path = data_dir / "images"

    embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    faiss_top_k: int = 20
    bm25_top_k: int = 20
    rrf_k: int = 60

    dense_weight: float = 0.50
    sparse_weight: float = 0.50

    compatibility_weights = {
        "occasion_match": 0.30,
        "category_completeness": 0.20,
        "embedding_cohesion": 0.20,
        "curated_cooccurrence": 0.20,
        "palette_harmony": 0.10,
    }


settings = Settings()