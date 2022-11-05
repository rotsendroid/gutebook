from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.reviewmodel import ReviewModel
from typing import List

def get_avg_month(db: Session, book_id: int) -> List:
    db_avg_month = db.query(ReviewModel.month, func.avg(ReviewModel.rating))\
        .filter(ReviewModel.book_id == book_id).group_by(ReviewModel.month).all()

    return [{"month": r[0], "avg_rating": float("{:.2f}".format(r[1])) } for r in db_avg_month]
