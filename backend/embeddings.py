from sentence_transformers import SentenceTransformer
from config import EMBED_MODEL

_model = None


def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBED_MODEL)
    return _model


def embed_text(text: str) -> list[float]:
    model = get_model()
    return model.encode(text, normalize_embeddings=True).tolist()


def embed_failure(record) -> list[float]:
    """Create a rich text representation for embedding a FailureRecord."""
    text = f"""
    Title: {record.title}
    Domain: {record.domain}
    What failed: {record.what_failed}
    Root cause: {record.root_cause}
    Root cause category: {record.root_cause_category}
    Lesson: {record.lesson}
    Tags: {', '.join(record.tags)}
    Warning signs: {', '.join(record.warning_signs)}
    """
    return embed_text(text.strip())
