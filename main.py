from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

#1. Describe what a to do looks like
class Todo(BaseModel):
    title: str
    done: bool = False

#2. Our "database" for now: a simple list
todos = []

#3. GET all to-dos
@app.get("/todos")

def get_todos():
    return todos


# 4. Get one to-do by its id
@app.get("/todos/{todo_id}")

def get_todo(todo_id: int):
    if todo_id < 0 or todo_id >= len(todos):
        raise HTTPException(status_code = 404, detail="Todo not found")
    return todos[todo_id]

#5. POST: create a new to-do
@app.post("/todos", status_code=201)
def create_todo(todo: Todo):
    todos.append(todo)
    return{"id": len(todos) -1, "todo": todo}

# 6. PUT: update an existing to-do
@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, updated: Todo):
    if todo_id < 0 or todo_id >= len(todos):
        raise HTTPException(status_code=404, detail="Todo not found")
    todos[todo_id] = updated
    return updated

#7. Delete: remove a to-do
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    if todo_id < 0 or todo_id >= len(todos):
        raise HTTPException(status_code=404, detail = "Todo not found")
    removed = todos.pop(todo_id)
    return {"delted": removed}