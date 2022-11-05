from fastapi import APIRouter

from app.api.api_v1.endpoints import book, books, review


API_VERSION_1: str = "/api/v1"
BASE_URL: str = ""



api_router = APIRouter()
api_router.include_router(book.router, prefix=API_VERSION_1+"/book")
api_router.include_router(books.router, prefix=API_VERSION_1+"/books")
api_router.include_router(review.router, prefix=API_VERSION_1+"/review")