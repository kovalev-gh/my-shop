from sqlalchemy.ext.asyncio import AsyncSession

from domains.users.service import UserService
from domains.mailing.send_email import send_email


user_service = UserService()


async def send_welcome_email(
    session: AsyncSession,
    user_id: int,
) -> None:

    user = await user_service.get_by_id(
        session=session,
        user_id=user_id,
    )

    if user is None:
        return

    await send_email(
        recipient=user.email,
        subject="Welcome to our site!",
        body=(
            f"Dear {user.name or user.email},\n\n"
            "Welcome to our site!"
        ),
    )