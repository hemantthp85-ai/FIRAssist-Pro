from qdrant_client import QdrantClient
from app.rag.embedder import get_embedding
from app.utils.performance import (
    cached_call,
    timed_agent
)

COLLECTION_NAME = "bns_sections"

client = QdrantClient(path="./qdrant_data")


def _search_bns_uncached(query, limit=5):

    vector = get_embedding(query)

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=vector,
        limit=limit
    )

    return results.points


@timed_agent("bns_retriever")
def search_bns(query, limit=5):

    return cached_call(
        "bns_retrieval",
        {
            "query": query,
            "limit": limit
        },
        _search_bns_uncached,
        query,
        limit
    )


if __name__ == "__main__":

    results = search_bns(
        "motorcycle theft"
    )

    for result in results:

        print("\n====================")

        print(
            "SECTION:",
            result.payload["section"]
        )

        print(
            result.payload["text"][:1000]
        )
