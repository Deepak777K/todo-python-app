from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from typing import List
# from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

class TodoDto(BaseModel):
    title: str
    completed: bool = False

class Todo(BaseModel):
    id: int
    title: str
    completed: bool = False

todos: List[Todo] = [
    Todo(id=1, title="Learn FastAPI", completed=False),
]
next_id = 2

@app.get("/")
def read_root():
    return {"message": "Welcome to the TODO app!"}

@app.get("/todos", response_model=List[Todo])
def get_all_todos():
    return todos

@app.get("/todos/todo/{todo_id}", response_model=Todo)
def get_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.post("/todos/create", response_model=Todo, status_code=201)
def create_todo(todo_data: TodoDto):
    global next_id
    todo_item = Todo(id=next_id, title=todo_data.title, completed=todo_data.completed)
    todos.append(todo_item)
    next_id += 1
    return todo_item

@app.put("/todos/update/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, updated_todo: TodoDto):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            todos[index].title = updated_todo.title
            todos[index].completed = updated_todo.completed
            return todos[index]
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/delete/{todo_id}", status_code=204)
def delete_todo(todo_id: int):
    global todos
    initial_length = len(todos)
    todos = [todo for todo in todos if todo.id != todo_id]
    if len(todos) == initial_length:
        raise HTTPException(status_code=404, detail="Todo not found")
    return Response(status_code=204)
