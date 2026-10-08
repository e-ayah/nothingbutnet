from fastapi import APIRouter

router = APIRouter()


@router.get("/upload/ping")
def ping():
    return {"router": "upload"}