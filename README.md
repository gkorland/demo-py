# demo-py

A demo FastAPI CRUD application for managing items.

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.  
Interactive docs (Swagger UI) at `http://localhost:8000/docs`.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/items` | List all items |
| `POST` | `/items` | Create a new item |
| `GET` | `/items/{id}` | Get an item by ID |
| `PUT` | `/items/{id}` | Update an item |
| `DELETE` | `/items/{id}` | Delete an item |

## Tests

```bash
pytest test_main.py -v
```
