from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

COLLECTION_NAME = "bns_sections"

client = QdrantClient(
    path="./qdrant_data"
)


def create_collection():

    collections = client.get_collections().collections

    existing_collections = [
        collection.name
        for collection in collections
    ]

    if COLLECTION_NAME not in existing_collections:

        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )

        print(f"✅ Collection '{COLLECTION_NAME}' created")

    else:

        print(f"✅ Collection '{COLLECTION_NAME}' already exists")


def list_collections():

    collections = client.get_collections().collections

    print("\nAvailable Collections:\n")

    for collection in collections:

        print(collection.name)


if __name__ == "__main__":

    print("Starting Qdrant...")

    create_collection()

    list_collections()