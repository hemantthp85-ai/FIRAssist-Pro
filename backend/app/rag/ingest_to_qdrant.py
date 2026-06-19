from app.rag.ingest_bns import (
    extract_pdf_text,
    chunk_text
)

from app.rag.embedder import (
    get_embedding
)

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

COLLECTION_NAME = "bns_sections"

client = QdrantClient(
    path="./qdrant_data"
)


def ingest():

    print("Extracting PDF...")

    text = extract_pdf_text()

    print("Creating Chunks...")

    chunks = chunk_text(text)

    print(f"Total Chunks: {len(chunks)}")

    points = []

    for idx, chunk in enumerate(chunks):

        vector = get_embedding(chunk)

        points.append(
            PointStruct(
                id=idx,
                vector=vector,
                payload={
                    "text": chunk
                }
            )
        )

    print("Uploading to Qdrant...")

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    print("✅ Upload Complete")


if __name__ == "__main__":

    ingest()