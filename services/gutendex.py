import requests
from typing import Union
from urllib.parse import urlparse, parse_qs

BASE_URL = 'https://gutendex.com/books'


class GutendexAPI:
    """
     GutendexAPI class provides methods for managing the gutendex API requests
    """

    def __init__(self, url, title, page):
        self.url: str = url
        self.title: str = title
        self.page: Union[int, None] = page

    def _get_results(self) -> dict:
        """
        _get_results() makes use of the requests library
        :return: a dictionary containing the requests raw results
        """
        params = {
            "page": self.page if self.page is not None else 1,
            "search": self.title,
        }
        r = requests.get(BASE_URL, params=params, timeout=60)
        if r.status_code == 200:
            return r.json()
        else:
            return {"status_code": r.status_code, "detail": "Loading results failed.", "count": -1}

    def parse_results(self) -> dict:
        """
        Responsible for parsing the raw JSON
        :return: a dictionary which is used as the response by search books endpoint
        """
        raw = self._get_results()

        if raw["count"] < 0:
            return raw

        books_list = []

        for b in raw["results"]:
            books_list.append({
                "id": b["id"],
                "title": b["title"],
                "authors": b["authors"],
                "languages": b["languages"],
                "download_count": b["download_count"]
            })

        raw_next = parse_qs(urlparse(raw["next"]).query)
        raw_prev = parse_qs(urlparse(raw["previous"]).query)

        # Both error handlers solve the case of next and/or previous equals to null
        try:
            next = int(raw_next["page"][0])
        except KeyError:
            next = None

        try:
            prev = int(raw_prev["page"][0])
        except KeyError:
            prev = None

        # The condition below solves the following problem:
        # the 1st page of results doesn't contain the query parameter 'page'
        # so 'raw_prev["page"][0]' raises a KeyError exception and prev is None/null
        # using that kind solution we have the 'previous' property of the 2nd page points to the
        # following: http://localhost:8000/api/v1/books/search?page=1&title=e
        if self.page == 2:
            prev = 1

        search_url_next = urlparse(str(self.url)).scheme + "://" + \
                          urlparse(str(self.url)).netloc + \
                          urlparse(str(self.url)).path + \
                          "?page=" + str(next) + \
                          "&title=" + self.title if next else None

        search_url_prev = urlparse(str(self.url)).scheme + "://" + \
                          urlparse(str(self.url)).netloc + \
                          urlparse(str(self.url)).path + \
                          "?page=" + str(prev) + \
                          "&title=" + self.title if prev else None

        result = {
            "count": raw["count"],
            "next": search_url_next,
            "previous": search_url_prev,
            "books": books_list
        }

        return result

    @staticmethod
    def get_book(book_id: int) -> dict:
        """
        Fetches the basic book properties
        :param book_id:
        :return:
        """
        r = requests.get(BASE_URL + f"/{book_id}", timeout=60)
        if r.status_code == 200:
            b = r.json()
            return {
                "id": b["id"],
                "title": b["title"],
                "authors": b["authors"],
                "languages": b["languages"],
                "download_count": b["download_count"]
            }

        else:
            return {"status_code": r.status_code, "detail": "Book information loading failed."}
