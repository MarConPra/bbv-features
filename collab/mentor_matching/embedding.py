import numpy as np
from sentence_transformers import SentenceTransformer
from functools import lru_cache


_model: SentenceTransformer = None


def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def embed_text(text: str) -> np.ndarray:
    model = get_model()
    return model.encode(text, normalize_embeddings=True)


def embed_texts(texts: list[str]) -> np.ndarray:
    model = get_model()
    return model.encode(texts, normalize_embeddings=True)


def build_mentor_text(bio: str, research_areas: list[str], publication_titles: list[str]) -> str:
    return f"{bio} {' '.join(research_areas)} {' '.join(publication_titles)}"


def build_project_text(title: str, abstract: str, domain: str) -> str:
    return f"{title} {abstract} {domain}"
