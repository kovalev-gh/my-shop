from domains.mailing.send_email import send_email
from domains.orders.models import Order
from core.config import settings


async def send_order_notification_email(order: Order) -> None:
    subject = f"Новый заказ #{order.id}"

    items_text = "\n".join(
        f"- [{item.product.id}] {item.product.title} x {item.quantity}"
        for item in order.items
    )

    body = (
        f"Новый заказ от пользователя: {order.user.name}\n"
        f"Email: {order.user.email}\n"
        f"Телефон: {order.user.phone}\n"
        f"Имя: {order.user.name}\n"
        f"\n"
        f"ID заказа: {order.id}\n"
        f"\n"
        f"Товары:\n{items_text}"
    )

    await send_email(
        recipient=settings.smtp.user,  # обычно это админ/менеджер
        subject=subject,
        body=body,
    )
