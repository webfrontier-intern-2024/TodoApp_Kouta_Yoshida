
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from models import TodoModel, TagModel, create_tables
from settings import SessionLocal
from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

# Dependency for getting the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic models for request and response validation
class TodoCreate(BaseModel):
    title: str
    details: str
    deadline: str
    # tag: str

class TodoUpdate(BaseModel):
    title: str
    done_tasks: bool

class TagCreate(BaseModel):
    outline: str

class TagUpdate(BaseModel):
    outline: str

# Initialize database tables
create_tables()

### Todo Endpoints ###

@router.get("/api/todos", response_model=List[TodoCreate])
def get_todos(db: Session = Depends(get_db)):
    todos = db.query(TodoModel).all()
    return todos

@router.get("/api/todos/{todo_id}", response_model=TodoCreate)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.post("/api/todos", response_model=TodoCreate)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = TodoModel(
        title=todo.title,
        details=todo.details,
        deadline=datetime.strptime(todo.deadline, "%Y-%m-%d").date(),
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    change_string = TodoCreate(
        title=todo.title,
        details=todo.details,
        deadline=todo.deadline,
    )
    return change_string

@router.put("/todos/{todo_id}", response_model=TodoCreate)
def update_todo(todo_id: int, todo: TodoUpdate, db: Session = Depends(get_db)):
    db_todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db_todo.title = todo.title
    db_todo.done_tasks = todo.done_tasks
    db.commit()
    db.refresh(db_todo)
    return db_todo

@router.delete("/todos/{todo_id}", response_model=dict)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(db_todo)
    db.commit()
    return {"message": "Todo deleted successfully"}

### Tag Endpoints ###

@router.get("/tags", response_model=List[TagCreate])
def get_tags(db: Session = Depends(get_db)):
    tags = db.query(TagModel).all()
    return tags

@router.get("/tags/{tag_id}", response_model=TagCreate)
def get_tag(tag_id: int, db: Session = Depends(get_db)):
    tag = db.query(TagModel).filter(TagModel.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag

@router.post("/tags", response_model=TagCreate)
def create_tag(tag: TagCreate, db: Session = Depends(get_db)):
    db_tag = TagModel(outline=tag.outline)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

@router.put("/tags/{tag_id}", response_model=TagCreate)
def update_tag(tag_id: int, tag: TagUpdate, db: Session = Depends(get_db)):
    db_tag = db.query(TagModel).filter(TagModel.id == tag_id).first()
    if not db_tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    db_tag.outline = tag.outline
    db.commit()
    db.refresh(db_tag)
    return db_tag

@router.delete("/tags/{tag_id}", response_model=dict)
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    db_tag = db.query(TagModel).filter(TagModel.id == tag_id).first()
    if not db_tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    db.delete(db_tag)
    db.commit()
    return {"message": "Tag deleted successfully"}
