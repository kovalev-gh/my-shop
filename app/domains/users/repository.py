# app/domains/users/repository.py

from sqlalchemy.ext.asyncio import AsyncSession
from domains.base.repository import BaseRepository
from .models import User

class UserRepository(BaseRepository[User],
):
    model = User
