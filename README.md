# ITSC 3155 Final Project — Sandwich Maker API

FastAPI backend for the restaurant / sandwich ordering project.

## Prerequisites

- Python 3.9+ (or similar)
- MySQL with a database created (see `api/dependencies/config.py`)

## Setup

```bash
pip install -r requirements.txt
```

Edit **`api/dependencies/config.py`** with your MySQL host, database name, username, and password.

On startup the app creates tables and applies simple schema updates for new columns (see `api/dependencies/schema_migrate.py` if you use an existing database).

## Run the server

From the project root (`ITSC3155_FinalProject`):

```bash
uvicorn api.main:app --reload
```

- API base: [http://127.0.0.1:8000](http://127.0.0.1:8000)  
- Interactive docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Tests

```bash
python -m pytest tests/ -v
```

Tests need a working MySQL connection with the same settings as in `config.py`.
