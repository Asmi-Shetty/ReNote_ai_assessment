import asyncio
from src.api.auth import register
from src.models.user import UserCreate

async def run():
    try:
        user = UserCreate(username='testuser', email='test@test.com', password='password')
        await register(user)
    except Exception:
        import traceback
        traceback.print_exc()

asyncio.run(run())
