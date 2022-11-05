from pydantic import BaseModel, conint
from datetime import datetime

class ReviewBase(BaseModel):
    book_id: int
    rating: conint(ge=0, le=5)
    review: str


class ReviewCreate(ReviewBase):
    pass


class Review(ReviewBase):
    review_id: int
    created_at: datetime

    class Config:
        orm_mode = True
