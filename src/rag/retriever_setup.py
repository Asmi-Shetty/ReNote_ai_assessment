"""
Retriever setup and vector store configuration.
"""

import os
import atexit

from langchain_core.documents import Document
from langchain_core.tools import create_retriever_tool
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

from src.core.config import settings
from qdrant_client import QdrantClient
from qdrant_client.http import models as rest

embeddings = OpenAIEmbeddings()

# Initialize Qdrant Client in Serverless Local Mode (No Docker required)
qdrant_client = QdrantClient(path="./qdrant_storage")
atexit.register(qdrant_client.close)

# Ensure collection exists
try:
    qdrant_client.get_collection(settings.CODE_COLLECTION)
except Exception:
    qdrant_client.create_collection(
        collection_name=settings.CODE_COLLECTION,
        vectors_config=rest.VectorParams(
            size=1536,  # OpenAI embeddings size
            distance=rest.Distance.COSINE
        )
    )


def retriever_chain(chunks: list[Document]):
    """
    Initialize and store documents in Qdrant vector database.

    Args:
        chunks: List of document chunks to store.

    Returns:
        Boolean indicating success of the operation.
    """
    try:
        vectorstore = QdrantVectorStore(
            client=qdrant_client,
            collection_name=settings.CODE_COLLECTION,
            embedding=embeddings,
        )
        vectorstore.add_documents(chunks)

        print(f"Qdrant vector store initialized with {len(chunks)} documents")
        return True
    except Exception as e:
        print(f"Error storing documents in Qdrant: {e}")
        return False


def get_retriever(user_id: str):
    """
    Get a retriever tool connected to the Qdrant vector store, scoped to the user.

    Returns:
        A LangChain retriever tool configured for the vector store.

    Raises:
        Exception: If vector store initialization fails.
    """
    try:
        # Check if collection exists to avoid errors on fresh start
        try:
            qdrant_client.get_collection(settings.CODE_COLLECTION)
        except Exception:
            # Collection might not exist yet
            pass

        vectorstore = QdrantVectorStore(
            client=qdrant_client,
            collection_name=settings.CODE_COLLECTION,
            embedding=embeddings,
        )

        # Apply metadata filter for user_id
        user_filter = rest.Filter(
            must=[
                rest.FieldCondition(
                    key="metadata.user_id",
                    match=rest.MatchValue(value=user_id)
                )
            ]
        )

        retriever = vectorstore.as_retriever(search_kwargs={"filter": user_filter})

        retriever_tool = create_retriever_tool(
            retriever,
            "retriever_customer_uploaded_documents",
            "Use this tool to search for specific information within the documents uploaded by the user. "
            "Always use this tool when the user asks questions about their uploaded files or content."
        )

        return retriever_tool

    except Exception as e:
        print(f"Error initializing retriever: {e}")
        raise Exception(e)
