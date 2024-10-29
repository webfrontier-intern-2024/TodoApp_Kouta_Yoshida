from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from models import TodoModel, create_tables
from settings import SessionLocal
from api import operation
import uvicorn

# Jinja2Templates setup
templates = Jinja2Templates(directory="templates")

# FastAPI app initialization
app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables on startup
create_tables()


### Routes ###




app = FastAPI()
app.include_router(operation.router)
# Render the Todo list page
@app.get("/", response_class=HTMLResponse)
async def read_todos(request: Request, db: Session = Depends(get_db)):
    todos = db.query(TodoModel).all()
    return templates.TemplateResponse("home.html", {"request": request, "todos": todos})

# Render the add Todo form
@app.get("/add-task", response_class=HTMLResponse)
async def add_todo_form(request: Request):
    return templates.TemplateResponse("add_task.html", {"request": request})

# Handle form submission to create a new Todo
@app.get("/todos/{todo_id}", response_class=HTMLResponse)
async def get_todo(todo_id: int, request: Request, db: Session = Depends(get_db)):
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return templates.TemplateResponse("home.html", {"request": request, "todo": todo})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
