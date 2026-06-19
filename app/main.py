from contextlib import asynccontextmanager

from fastapi import FastAPI

import uvicorn

#import core.db.models # разобраться зачем этот импорт. без него пятисотил поинт просмотра пользователя по айди
from domains.products.router import router as products_router
from domains.auth.router import router as auth_router
from domains.users.router import router as users_router
from domains.orders.router import router as orders_router
from domains.mailing.router import router as mailing_router
from domains.payments.router import router as payments_router
from domains.payments.webhooks import router as payment_webhook_router
from core.logger import configure_logging

configure_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(products_router)
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(orders_router)
app.include_router(mailing_router)
app.include_router(payments_router)
app.include_router(payment_webhook_router)#, prefix="/api/v1")


@app.get("/hello/")
def hello(name: str = "World"):
    name = name.strip().title()
    return {"message": f"Hello {name}!"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
