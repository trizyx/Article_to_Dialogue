from fastapi import APIRouter

from src.schemas import StatusSchema

router = APIRouter()


@router.get(
    path="/ping",
    status_code=200,
)
async def check_video() -> StatusSchema:
    return StatusSchema(status="ok")
