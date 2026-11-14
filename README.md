# To-Do REST API

A simple REST API built with Python and FastAPI while learning REST.

## Endpoints
- `GET /todos` – list all to-dos
- `GET /todos/{id}` – get one to-do
- `POST /todos` – create a to-do
- `PUT /todos/{id}` – update a to-do
- `DELETE /todos/{id}` – delete a to-do


## How to run
```bash
python -m venv venv
venv\Scripts\activate    # Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```
Then open http://127.0.0.1:8000/docs


Data is stored in a local SQLite database (tools.db).


- `GET /todos` – list all to-dos (filter with `?done=true` or `?done=false`)