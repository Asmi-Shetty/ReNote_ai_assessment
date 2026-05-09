"""
FastAPI dependencies.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from bson import ObjectId

from src.core.config import settings
from src.db.mongo_client import users_collection
from src.models.user import TokenData, UserResponse

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserResponse:
    """
    Dependency to get the current authenticated user from JWT token.
    
    Args:
        token: JWT access token.
        
    Returns:
        UserResponse object representing the authenticated user.
        
    Raises:
        HTTPException: If token is invalid or user doesn't exist.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("user_id")
        email: str = payload.get("email")
        if user_id is None or email is None:
            raise credentials_exception
        token_data = TokenData(email=email, user_id=user_id)
    except JWTError:
        raise credentials_exception

    # Find user in database
    user = await users_collection.find_one({"_id": ObjectId(token_data.user_id)})
    if user is None:
        raise credentials_exception
        
    return UserResponse(
        id=str(user["_id"]),
        email=user["email"],
        username=user["username"],
        created_at=user["created_at"]
    )
