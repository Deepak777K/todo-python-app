


# Step 1: FastAPI TODO App — Initial Setup

---

### Prerequisites

* Python 3.7+ installed
* Navigate to your project folder

---

### 1.1. Create `requirements.txt`

```txt
fastapi
uvicorn
```

---

### 1.2. Install Dependencies (FastAPI and Uvicorn)

```bash
pip install -r requirements.txt
```

Or:

```bash
pip install fastapi uvicorn
```

Or (if using the Python launcher):

```bash
py -m pip install fastapi uvicorn
```

---

### 1.3. Create a Server File (`main.py`)

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the TODO app!"}
```

---

### 1.4. Run the FastAPI App

```bash
uvicorn main:app --reload
```

Or (using the Python launcher):

```bash
py -m uvicorn main:app --reload
```

---

### Access API Docs

* Open [http://localhost:8000](http://localhost:8000) and 

* Interactive API docs for testing : [http://localhost:8000/docs](http://localhost:8000/docs)

---

# Step 2: Create Endpoints for CRUD Operations

---

### 2.1. Add In-Memory Storage and Models

In `main.py`:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

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
```

> This provides temporary storage of tasks while the server is running.

---

### 2.2. Add CRUD Endpoints

#### Get All Todos

```python
@app.get("/todos", response_model=List[Todo])
def get_all_todos():
    return todos
```

#### Get Todo by ID

```python
@app.get("/todos/todo/{todo_id}", response_model=Todo)
def get_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")
```

#### Create a New Todo

```python
@app.post("/todos/create", response_model=Todo, status_code=201)
def create_todo(todo_data: TodoDto):
    global next_id
    todo_item = Todo(id=next_id, title=todo_data.title, completed=todo_data.completed)
    todos.append(todo_item)
    next_id += 1
    return todo_item
```

#### Update an Existing Todo

```python
@app.put("/todos/update/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, updated_todo: TodoDto):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            todos[index].title = updated_todo.title
            todos[index].completed = updated_todo.completed
            return todos[index]
    raise HTTPException(status_code=404, detail="Todo not found")
```

#### Delete a Todo

```python
@app.delete("/todos/delete/{todo_id}", status_code=204)
def delete_todo(todo_id: int):
    global todos
    initial_length = len(todos)
    todos = [todo for todo in todos if todo.id != todo_id]
    if len(todos) == initial_length:
        raise HTTPException(status_code=404, detail="Todo not found")
    return Response(status_code=204)
```

---

### Optional: Local Testing with CORS

If you're testing with a frontend (e.g., `test_api.html`), you may need to enable CORS.

#### 1. Install `fastapi` and `starlette` (already included with FastAPI, but ensure it's up-to-date):

```bash
pip install fastapi[all]
```

#### 2. Add CORS middleware in `main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

> Now you can place `test_api.html` in your project root and test basic frontend interactions with the API.

---

