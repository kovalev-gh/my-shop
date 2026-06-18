from fastapi import APIRouter

router = APIRouter(
    prefix="/webhooks",
    tags=["Payment Webhooks"],
)


@router.post("/yookassa")
async def yookassa_webhook(
    payload: dict,
):
    print(payload)

    return {
        "status": "ok",
    }