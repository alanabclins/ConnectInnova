from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from .. import models
from ..auth.auth import get_current_active_user

router = APIRouter()


#  Rota GET — retorna todos os feedbacks do usuário logado
@router.get("/{feedback_uuid}", response_model=List[models.Feedback])
async def get_feedbacks(
    feedback_uuid: UUID, current_user: models.User = Depends(get_current_active_user)
) -> Any:
    try:
        # Busca todos os feedbacks do usuário atual
        feedbacks = await models.Feedback.find(
            models.Feedback.uuid == feedback_uuid
        ).to_list()

        return feedbacks

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar feedbacks: {e}")
