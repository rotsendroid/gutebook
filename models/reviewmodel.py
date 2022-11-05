from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base
import datetime


class ReviewModel(Base):
    __tablename__ = "reviews"

    review_id = Column(Integer, primary_key=True)
    book_id = Column(Integer)
    rating = Column(Integer)
    review = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    month = Column(String, default=datetime.datetime.utcnow().strftime("%b"))

    def __repr__(self):
        return f"Review(review_id={self.review_id}, book_id={self.book_id}, rating={self.rating}, review={self.review})"


class ReviewsAvgModel(Base):
    __tablename__ = "reviews_avg"

    book_id = Column(Integer, ForeignKey("reviews.book_id"), primary_key=True)
    reviews_avg = Column(Float)
    book = relationship("ReviewModel", backref="reviews")

    def __repr__(self):
        return f"ReviewsAvgModel(book_id={self.book_id}), reviews_avg={self.reviews_avg}"



