
---

# Step 1: FastAPI TODO App — Initial Setup

---

### Prerequisites

* Python 3.7+ installed
* Navigate to your project folder

---

### 1. Create `requirements.txt`

```txt
fastapi
uvicorn
```

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Create `main.py`

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the TODO app!"}
```

---

### 4. Run the app

```bash
uvicorn main:app --reload
```

Open [http://localhost:8000](http://localhost:8000) and [http://localhost:8000/docs](http://localhost:8000/docs)

---

