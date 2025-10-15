from typing import Any, List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException

from .. import models, schemas
from ..auth.auth import get_current_active_user

router = APIRouter()

# ✅ Rota GET — retorna o(s) resumos associados a um UUID específico
@router.get("/{resume_uuid}", response_model=List[models.AIResum])
async def get_resumes(resume_uuid: UUID, current_user: models.User = Depends(get_current_active_user)) -> Any:
    try:
        # Busca os resumos correspondentes ao UUID informado
        resumes = await models.AIResum.find(
            models.AIResum.uuid == resume_uuid
        ).to_list()

        return resumes

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar resumos: {e}")
