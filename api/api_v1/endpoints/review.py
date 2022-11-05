from app.schemas.review import ReviewCreate, Review
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud import review

router = APIRouter()

@router.post("/", status_code=201, response_model=Review)
def create_review(review_in: ReviewCreate,
                        db: Session = Depends(get_db)) -> dict:
    """
    Insert a new review in DB
    </br>
    Example Request body:
    {
        "book_id": 1342,
        "rating": 5,
        "review": "really interesting"
    }

    The corresponding Response:
    {
        "book_id": 1342,
        "rating": 5,
        "review": "really interesting",
        "review_id": 6,
        "created_at": "2022-06-07T14:47:37.397833"
    }

    :param review_in:
    :return:
    """

    return review.create_review(db, review_in)

