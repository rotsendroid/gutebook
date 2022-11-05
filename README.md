## Gutebook


#### Description
Gutebook is a web API that gives users the ability to search for books, post reviews, and find all the
necessary information about a book in one place.

<br>

#### Technologies used
- API Framework: FastAPI
- ORM: SQLAlchemy
- HTTP library: requests

<br>

#### Project structure
- The application starts within *main.py*. Inside main the following happens:
  - The database is created
  - The FastAPI app object and the APIRouter are initialized
- The module *db.py* contains the SQLAlchemy and SQLite configuration parameters
- The package *api* has the endpoints of the API.
- Within the *crud* package we can find functions that deal with models
- *models* package includes the ORM models definition
- Package *schemas* has the Pydantic models
- *services* contains the appropriate functions to handle the Gutendex API requests and responses (using requests library)
