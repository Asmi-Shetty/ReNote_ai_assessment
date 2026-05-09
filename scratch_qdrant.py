import sys
import asyncio
from src.rag.retriever_setup import qdrant_client, embeddings
from src.core.config import settings
from qdrant_client.http import models as rest
from langchain_qdrant import QdrantVectorStore

def test_qdrant(user_id):
    # Check all records in Qdrant
    try:
        count = qdrant_client.count(collection_name=settings.CODE_COLLECTION)
        print(f"Total documents in Qdrant: {count.count}")
        
        # Get one record to see metadata structure
        if count.count > 0:
            records = qdrant_client.scroll(collection_name=settings.CODE_COLLECTION, limit=1)
            if records and records[0]:
                print(f"Sample record payload: {records[0][0].payload}")
    except Exception as e:
        print(f"Error checking Qdrant: {e}")

    vectorstore = QdrantVectorStore(
        client=qdrant_client,
        collection_name=settings.CODE_COLLECTION,
        embedding=embeddings,
    )
    
    # Try retrieving without filter
    docs = vectorstore.similarity_search("test", k=2)
    print(f"Docs without filter: {len(docs)}")
    if docs:
        print(f"Metadata of first doc: {docs[0].metadata}")
        
    # Try retrieving with filter
    user_filter = rest.Filter(
        must=[
            rest.FieldCondition(
                key="metadata.user_id",
                match=rest.MatchValue(value=user_id)
            )
        ]
    )
    docs_filtered = vectorstore.similarity_search("test", k=2, filter=user_filter)
    print(f"Docs with filter 'metadata.user_id': {len(docs_filtered)}")

if __name__ == "__main__":
    user_id = "test_user_id" # Need to know the actual user_id or we can just check what is in Qdrant
    test_qdrant(user_id)
