from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.postgres import get_async_session
from domains.mailing.send_welcome_email import send_welcome_email

router = APIRouter(prefix="/mailing", tags=["Mailing"])


@router.post("/welcome/{user_id}")
async def send_welcome(
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    await send_welcome_email(
        session=session,
        user_id=user_id,
    )

    return {"status": "ok"}