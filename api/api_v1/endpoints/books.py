from fastapi import APIRouter, Request, Depends, HTTPException
from typing import Union
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.services.gutendex import GutendexAPI
from app.crud.books import get_top_n_books

router = APIRouter()

@router.get("/search", status_code=200)
def search_books(
        request: Request,
        title: str,
        page: Union[int, None] = None,
        ) -> dict:
    """
    Usage
    1) Calls the Gutendex API
    2) Parses the required properties
    3) Handles pagination (next and previous fields)
    </br>
    Example response:
    {
        "count": 3834,
        "next": "http://172.105.76.41:9157/api/v1/books/search?page=5&title=william",
        "previous": "http://172.105.76.41:9157/api/v1/books/search?page=3&title=william",
        "books": [
            {
                "id": 808,
                "title": "The Complete Plays of Gilbert and Sullivan",
                "authors": [
                    {
                        "name": "Gilbert, W. S. (William Schwenck)",
                        "birth_year": 1836,
                        "death_year": 1911
                    },
                    {
                        "name": "Sullivan, Arthur",
                        "birth_year": 1842,
                        "death_year": 1900
                    }
                ],
                "languages": [
                    "en"
                ],
                "download_count": 304
            },
            ....]
    }
    :param request:
    :param title:
    :param page:
    :return:
    """

    gutendex = GutendexAPI(request.url, title, page)
    return gutendex.parse_results()

@router.get("/top/{n}", status_code=200)
def fetch_top_n_books(n: int = 10, db: Session = Depends(get_db)) -> dict:
    """
    Returns the top N books based on their average rating
    N defaults to 10
    </br>
    Example response:
    {
        "top_books": [
            {
                "book_id": 1342,
                "title": "Pride and Prejudice",
                "authors": [
                    {
                        "name": "Austen, Jane",
                        "birth_year": 1775,
                        "death_year": 1817
                    }
                ],
                "avg_rating": 4.33
            },
            {
                "book_id": 2,
                "title": "The United States Bill of Rights: The Ten Original Amendments to the Constitution of the United States",
                "authors": [
                    {
                        "name": "United States",
                        "birth_year": null,
                        "death_year": null
                    }
                ],
                "avg_rating": 4.0
            }
        ]
    }

    :param n:
    :param db:
    :return:
    """

    res = get_top_n_books(db, n)

    if len(res) == 0:
        raise HTTPException(
            status_code=404, detail=f"No book reviews exist. Please add one first and then try again."
        )

    return {
        "top_books": res
    }
