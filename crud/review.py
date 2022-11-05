from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.models.reviewmodel import ReviewModel, ReviewsAvgModel
from app.schemas.review import ReviewCreate
from typing import Tuple, List


def create_review(db: Session, review_in: ReviewCreate) -> ReviewModel:
    db_review = ReviewModel(book_id=review_in.book_id,
                            rating=review_in.rating,
                            review=review_in.review)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    avg = db.query(func.avg(ReviewModel.rating).label('rating (avg)')).filter(ReviewModel.book_id == review_in.book_id).scalar()
    _calculate_avg(db, review_in.book_id, avg)
    return db_review


def read_reviews(db: Session, book_id: int) -> Tuple[List, float]:
    reviews = [r["review"] for r in db.query(ReviewModel.review).filter(ReviewModel.book_id == book_id).all()]
    if len(reviews) > 0:
        avg = db.query(ReviewsAvgModel.reviews_avg).filter(ReviewsAvgModel.book_id == book_id).scalar()
    else:
        avg = -1
    return reviews, float("{:.2f}".format(avg))

def _calculate_avg(db: Session, book_id: int, avg: float):
    # first check if it doesn't exist a record for this book_id
    # if it exists it will be updated (within condition)
    # else add a new one
    if db.query(ReviewsAvgModel).filter(ReviewsAvgModel.book_id == book_id).update({"reviews_avg": avg}) < 1:
        db_review_avg = ReviewsAvgModel(book_id=book_id, reviews_avg=avg)
        db.add(db_review_avg)
        db.commit()
    db.commit()
