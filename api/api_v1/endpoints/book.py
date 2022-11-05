from app.schemas.book import Book
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.crud.review import read_reviews
from app.api.deps import get_db
from app.services.gutendex import GutendexAPI
from app.crud.book import get_avg_month
from pprint import pprint

router = APIRouter()


@router.get("/{book_id}", status_code=200, response_model=Book)
def fetch_book(book_id: int,  db: Session = Depends(get_db)) -> dict:
    """
    Fetch a single book based on book_id
    </br>
    Response example:
    {
        "id": 2,
        "title": "The United States Bill of Rights: The Ten Original Amendments to the Constitution of the United States",
        "authors": [
            {
                "name": "United States",
                "birth_year": null,
                "death_year": null
            }
        ],
        "languages": [
            "en"
        ],
        "download_count": 407,
        "avg_rating": 4.0,
        "reviews": [
            "really interesting"
        ]
    }


    :param book_id:
    :return: a dictionary with the properties of a book
    """
    # r is a list containing all the related reviews of a book_id
    r, avg = read_reviews(db, book_id)
    if len(r) == 0:
        raise HTTPException(
            status_code=404, detail=f"Book with id {book_id} doesn't have any reviews."
        )
    # if a book review exists then parse the data from gutendex
    b = GutendexAPI.get_book(book_id)
    # add the following properties
    b["avg_rating"] = avg
    b["reviews"] = r
    return b

@router.get("/rating/month/{book_id}", status_code=200)
def fetch_avg_rating(book_id: int, db: Session = Depends(get_db)) -> dict:
    """
    Get the average rating per month
    Months are stored in a short notation format
    e.g. Jun, Jul, Aug, Sep etc.
    </br>
    Response example:
    {
    "book_id": 1342,
        "monthly_rating": [
            {
                "month": "Jun",
                "avg_rating": 4.33
            }
        ]
    }

    :param book_id:
    :param db:
    :return: a dictionary
    """
    res = get_avg_month(db, book_id)

    if len(res) == 0:
        raise HTTPException(
            status_code=404, detail=f"Book with id {book_id} doesn't have any reviews."
        )

    # pprint(res)
    return {
        "book_id": book_id,
        "monthly_rating": res
    }
