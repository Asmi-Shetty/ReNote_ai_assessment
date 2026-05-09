"""
API client for communicating with backend services.
"""

import logging
import os

import requests

logger = logging.getLogger(__name__)

# Backend service URLs
RUST_BASE_URL = "http://localhost:8080/api"
PYTHON_BASE_URL = "http://127.0.0.1:8000"


def create_user(username: str, password: str, api_token: str) -> bool:
    """
    Create a new user account on the FastAPI backend.
    """
    url = f"{PYTHON_BASE_URL}/auth/register"
    # The backend schema requires an email, so we generate a mock one
    payload = {
        "username": username,
        "email": f"{username}@example.com",
        "password": password
    }
    response = requests.post(url, json=payload)
    if response.status_code == 201:
        return True
    else:
        logger.error("Register failed: %s", response.text)
        return False


def login_user(username: str, password: str, api_token: str) -> dict:
    """
    Authenticate user login via FastAPI OAuth2.
    """
    url = f"{PYTHON_BASE_URL}/auth/login"
    payload = {
        "username": username,
        "password": password
    }
    response = requests.post(url, data=payload)  # OAuth2 uses form data
    if response.status_code == 200:
        data = response.json()
        return {"jwt": data["access_token"], "username": username}
    else:
        logger.error("Login failed: %s", response.text)
        return {}


def get_api_token() -> str:
    """
    Get an API token for authentication.

    Returns:
        API token string if successful, None otherwise.
    """
    import uuid
    token = str(uuid.uuid4())
    logger.info("Mock get_api_token generated: %s", token)
    return token


def query_backend(query: str, session_id: str, jwt_token: str) -> str:
    """
    Send a query to the RAG backend.

    Args:
        query: The user's query text.
        session_id: Session identifier for tracking conversation.
        jwt_token: The authenticated user's JWT token.

    Returns:
        Response text from the backend or error message.
    """
    url = f"{PYTHON_BASE_URL}/rag/query"
    headers = {"Authorization": f"Bearer {jwt_token}"}
    print(f"[query_backend] Calling: {url}")

    response = requests.post(
        url,
        json={"query": query, "session_id": session_id},
        headers=headers,
        allow_redirects=False
    )

    if response.status_code == 200:
        return response.json()["result"]["content"]
    else:
        return f"Error: {response.status_code} - {response.text}"


def document_upload_rag(file, description: str, jwt_token: str) -> bool:
    """
    Upload a document to the RAG system.

    Args:
        file: File object to upload.
        description: Description of the document.
        jwt_token: The authenticated user's JWT token.

    Returns:
        True if upload succeeds, False otherwise.
    """
    headers = {
        "X-Description": description,
        "Authorization": f"Bearer {jwt_token}"
    }
    url = f"{PYTHON_BASE_URL}/rag/documents/upload"

    if file:
        files = {"file": (file.name, file, file.type)}
        response = requests.post(url, files=files, headers=headers)
        print(response)

        if response.status_code == 200:
            return True

    return False
