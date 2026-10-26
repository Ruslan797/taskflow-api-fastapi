from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.ai_agent.agent import generate_response
from app.ai_agent.schemas import ChatRequest, ChatResponse

from app.database.db import get_db
from app.core.auth import get_current_user
from app.models.users import User


router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


@router.post("/chat")
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ChatResponse:
    response = await generate_response(
        request.message,
        db,
        current_user.id,
    )

    return ChatResponse(response=response)