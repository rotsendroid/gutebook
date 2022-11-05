from sqlalchemy.orm import Session
from app.models.reviewmodel import ReviewsAvgModel
from typing import List
from app.services.gutendex import GutendexAPI

def get_top_n_books(db: Session, n: int) -> List:
    top_books = []
    reviews_sorted = db.query(ReviewsAvgModel).order_by(ReviewsAvgModel.reviews_avg.desc()).limit(n).all()
    if len(reviews_sorted) > 0:
        for r in reviews_sorted:
            # Gutendex API call
            res = GutendexAPI.get_book(r.book_id)
            # construct the top_books list
            top_books.append({
                "book_id": res["id"],
                "title": res["title"],
                "authors": res["authors"],
                "avg_rating": float("{:.2f}".format(r.reviews_avg))
            })

    return top_books
