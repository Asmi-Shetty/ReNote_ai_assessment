"""
API routes for RAG operations.
"""

from fastapi import APIRouter, UploadFile, File, Header, Depends
from langchain_core.messages import HumanMessage, AIMessage

from src.memory.chat_history_mongo import ChatHistory
from src.models.query_request import QueryRequest
from src.rag.document_upload import documents
from src.rag.graph_builder import builder
from src.core.dependencies import get_current_user
from src.models.user import UserResponse

router = APIRouter()


@router.post("/rag/query")
async def rag_query(
    req: QueryRequest,
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Process a RAG query and return the result.

    Args:
        req: The query request containing query text and session_id.
        current_user: Authenticated user.

    Returns:
        The generated response from the RAG pipeline.
    """
    chat_history = ChatHistory.get_session_history(req.session_id, current_user.id)
    await chat_history.add_message(HumanMessage(content=req.query))

    # Fetch full history
    messages = await chat_history.get_messages()
    try:
        result = builder.invoke({
            "messages": messages,
            "user_id": current_user.id
        })
    except Exception as e:
        import traceback
        with open("error.log", "a") as f:
            f.write(traceback.format_exc() + "\n")
        raise e
        
    output_text = result["messages"][-1].content

    # Save assistant message
    await chat_history.add_message(AIMessage(content=output_text))

    return {"result": result["messages"][-1]}


@router.post("/rag/documents/upload")
async def upload_file(
    file: UploadFile = File(...),
    description: str = Header(..., alias="X-Description"),
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Upload a document for RAG processing.

    Args:
        file: The file to upload (PDF or TXT).
        description: Document description provided via header.
        current_user: Authenticated user.

    Returns:
        Upload status.
    """
    status_upload = documents(description, file, current_user.id)
    return {"status": status_upload}

