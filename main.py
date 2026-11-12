import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()
DB_NAME = "todos.db"


# -----------Database setup -------------------

def get_connection():
    """Open a connection to the database file."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row #lets us read columns by name
    return conn

def create_table():
    """Create the todos table it it doesn't exist yet."""
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS todos(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER NOT NULL DEFAULT 0
        )
""")
    conn.commit()
    conn.close()


create_table() #runs once when the server starts


def row_to_dict(row):
    """Turn a database row into a dictionary for JSON."""
    return {"id": row["id"], "title": row["title"], "done":bool(row["done"])}

#------------------Data Model -------------------

class Todo(BaseModel):
    title: str
    done: bool = False


# ---------- Endpoints -----------------

@app.get("/todos")
def get_todos():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM todos").fetchall()
    conn.close()
    return [row_to_dict(row) for row in rows]

@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM todos WHERE ID = ?", (todo_id,)).fetchone()
    #the ? marks are important. Never put user input directly into SQL text like 
    #f"... WHERE id = {todo_id}". The ? placeholders let SQLite insert the values 
    # safely, which protects against an attack called SQL injection.
    conn.close()
    if row is None:
        raise HTTPException(status_code = 404, detail = "Todo not found")
    return row_to_dict(row)

@app.post("/todos", status_code = 201)
def create_todo(todo: Todo):
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO todos(title, done) VALUES (?, ?)",
        (todo.title, todo.done)

    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return{"id":new_id, "title":todo.title, "done":todo.done}


@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, updated: Todo):
    conn = get_connection()
    cursor = conn.execute(
        "UPDATE todos SET title = ?, done = ? WHERE id = ?",
        (updated.title, updated.done, todo_id),
    )
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail ="Todo not found")
    return {"id":todo_id, "title":updated.title, "done":updated.done}


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id:int):
    conn = get_connection()
    cursor = conn.execute("DELETE FROM toods WHERE id = ?", (todo_id,))
    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail = "Todo not found")
    return {"deleted_id": todo_id}