from qdrant_client import QdrantClient
try:
    client = QdrantClient(path="./qdrant_storage")
    result = client.scroll(
        collection_name="code_documents",
        limit=5,
        with_payload=True
    )
    with open("qdrant_output.txt", "w", encoding="utf-8") as f:
        f.write(f"Found points: {len(result[0])}\n")
        if result[0]:
            f.write(f"Payload: {result[0][0].payload}\n")
except Exception as e:
    with open("qdrant_output.txt", "w", encoding="utf-8") as f:
        f.write(f"Error: {e}\n")
