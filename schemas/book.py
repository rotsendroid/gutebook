from pydantic import BaseModel
from typing import List


class Book(BaseModel):
    id: int
    title: str
    authors: List[dict]
    languages: List[str]
    download_count: int
    avg_rating: float
    reviews: List[str]
