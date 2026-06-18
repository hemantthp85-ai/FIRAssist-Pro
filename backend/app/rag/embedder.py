from sentence_transformers import SentenceTransformer
from backend.app.utils.performance import (
    cached_call,
    timed_agent
)

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


def warm_embedding_model():
    return get_embedding(
        "warmup"
    )


def _get_embedding_uncached(text):
    embedding = model.encode(text)

    return embedding.tolist()


@timed_agent("embedding_model")
def get_embedding(text):

    return cached_call(
        "embedding",
        text,
        _get_embedding_uncached,
        text
    )


if __name__ == "__main__":

    sample_text = """
    Theft of movable property without consent.
    """

    vector = get_embedding(sample_text)

    print(f"Vector Length: {len(vector)}")

    print(vector[:10])
