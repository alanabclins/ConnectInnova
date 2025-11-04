from fastapi import APIRouter

from . import feedback, login, projects, resum, users

api_router = APIRouter()
api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(feedback.router, prefix="/feedback", tags=["feedback"])
api_router.include_router(resum.router, prefix="/resum", tags=["resum"])


@api_router.get("/")
async def root():
    return {"message": "Backend API for FARM-docker operational !"}
