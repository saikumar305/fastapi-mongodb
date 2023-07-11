from fastapi import FastAPI
from app.core.config import settings
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.user_model import User
from app.models.todo_model import Todo
from app.api.api_v1.router import router

app = FastAPI(
    title=settings.PROJECT_NAME
)


@app.on_event("startup")
async def app_init():
    """
        Initialise database
    """

    db_client =AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING).todo_db

    await init_beanie(
        database=db_client,
        document_models=[
            User,
            Todo
        ]
    )

app.include_router(router , prefix= settings.API_V1_STR)

@app.get('/')
def root():
    return {"message" : "Welcome to FastAPI"}