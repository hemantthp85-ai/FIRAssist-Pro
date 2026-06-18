from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

from backend.app.rag.section_parser import extract_sections
from backend.app.rag.embedder import get_embedding

COLLECTION_NAME = "bns_sections"

client = QdrantClient(
    path="./qdrant_data"
)


def ingest_sections():

    print("Loading Sections...")

    sections = extract_sections()

    print(f"Found {len(sections)} Sections")

    points = []

    for idx, section in enumerate(sections):

        section_text = section["text"]

        vector = get_embedding(section_text)

        points.append(
            PointStruct(
                id=idx,
                vector=vector,
                payload={
                    "section": section["section"],
                    "text": section_text
                }
            )
        )

    print("Uploading Sections to Qdrant...")

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    print("✅ Section Upload Complete")


if __name__ == "__main__":

    ingest_sections()