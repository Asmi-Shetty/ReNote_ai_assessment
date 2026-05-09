from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_core.tools import create_retriever_tool
from qdrant_client import QdrantClient
from qdrant_client.http import models as rest

def test_tool_invoke():
    # Use in-memory Qdrant
    qdrant_client = QdrantClient(location=":memory:")
    
    qdrant_client.create_collection(
        collection_name="test_collection",
        vectors_config=rest.VectorParams(
            size=1536,  # OpenAI embeddings size
            distance=rest.Distance.COSINE
        )
    )
    
    embeddings = OpenAIEmbeddings()
    vectorstore = QdrantVectorStore(
        client=qdrant_client,
        collection_name="test_collection",
        embedding=embeddings,
    )
    
    doc = Document(page_content="The candidate's name is John Doe and he lives in New York.", metadata={"user_id": "test_user_id"})
    vectorstore.add_documents([doc])
    
    user_filter = rest.Filter(
        must=[
            rest.FieldCondition(
                key="metadata.user_id",
                match=rest.MatchValue(value="test_user_id")
            )
        ]
    )
    
    retriever = vectorstore.as_retriever(search_kwargs={"filter": user_filter})
    retriever_tool = create_retriever_tool(
        retriever,
        "retriever_test",
        "description"
    )
    
    result = retriever_tool.invoke("What is the candidate's name?")
    print("Tool invoke result type:", type(result))
    print("Tool invoke result content:", repr(result))

if __name__ == "__main__":
    test_tool_invoke()
