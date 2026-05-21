# OnlineStoreAPI
End-to-end API test automation project using Python + Pytest against the public Fake Store API (`https://fakestoreapi.com`).

This repo demonstrates:
- A clean test structure for Products, Carts, and Users APIs
- Centralized route management (single source of truth for endpoints)
- Payload generation using `faker` and typed datamodels (`@dataclass`)
- Data-driven testing from JSON files
- Request/response logging via a pytest fixture

## What This Project Tests
- **Products**: list, get by id, limit, sort, categories, create, update, delete
- **Carts**: list, get by id, date-range query, get carts by user, create, update, delete
- **Users**: list, get by id, limit, sort, create, update, delete

## Repo Structure
- `routes/Routes.py`: endpoint constants and `BASE_URL`
- `payloads/Payload.py`: test data builders for product/user/cart requests
- `datamodels/`: request body shapes (dataclasses)
  - `Product`, `Cart`, `CartProduct`, `User`, `Name`, `Address`, `Geolocation`
- `testCases/`: pytest suites
  - `test_product_tests.py`: functional product API tests
  - `test_product_datadriven_tests.py`: data-driven create/delete product tests
  - `test_cart_tests.py`: cart API tests
  - `test_user_tests.py`: user API tests
  - `conftest.py`: shared setup + request/response logging fixture
- `utils/`:
  - `ConfigReader.py`: reads values from `configurations/config.ini`
  - `DataProviders.py`: Excel/JSON/CSV test data readers
  - `date_utils.py`: date range validation helper for cart tests
- `configurations/config.ini`: test configuration (ids, date range, limits)
- `testData/` and `testdata/`: sample product JSON data (used by data-driven tests)
- `logs/test_logging.log`: generated request/response log output (created on test runs)

## Setup
1. Create/activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run Tests
Run everything:

```bash
pytest -q
```

Run a single test file:

```bash
pytest -q testCases/test_product_tests.py
```

Run by marker (examples):

```bash
pytest -q -m smoke
pytest -q -m sanity
pytest -q -m regression
```

## Key Implementation Notes (Interview Talking Points)
- **Centralized routes**: All endpoints are in `routes/Routes.py` so tests don’t hardcode URLs.
- **Reusable setup**: `testCases/conftest.py` provides a class-scoped `setup` fixture for `base_url` and config access.
- **Request/response logging**: The `setup` fixture patches `requests.Session.request` to log every HTTP request and response to `logs/test_logging.log`.
- **Typed payloads**: Payloads are built from dataclasses to keep request structures explicit and consistent.
  - Simple payloads use `payload.__dict__`
  - Nested dataclasses (User/Cart) use `dataclasses.asdict(...)`
- **Data-driven testing**: `testCases/test_product_datadriven_tests.py` parameterizes tests from `testData/product.json`.
- **API-accurate assertions**: Create operations (`POST`) expect `201 Created` based on Fake Store API behavior.

## Configuration
Edit `configurations/config.ini` to adjust the ids and test inputs used across suites:
- `productId`, `userId`, `cartId`
- `limit`
- `startdate`, `enddate`

## Notes / Limitations
- This project targets a public external API, so test results depend on network availability and the API being up.
- The Fake Store API is a demo service; returned ids and payload behavior may differ from production-grade APIs.
