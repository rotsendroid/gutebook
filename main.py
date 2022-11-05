from fastapi import FastAPI, APIRouter, Request
from app.api.api_v1.api import api_router
from app.models.reviewmodel import Base
from app.db import engine

Base.metadata.create_all(bind=engine)

root_router = APIRouter()
app = FastAPI()



@app.get("/", status_code=200)
async def root(
        request: Request
) -> dict:
    return {"message": "This is the Gutebook API. Documentation can be found at the /docs path."}

app.include_router(api_router)
app.include_router(root_router)


