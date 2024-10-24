from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from settings import SessionLocal, engine
from models import TodoModel, TagModel, SettingsModel

# FastAPIのインスタンス
app = FastAPI()

# データベースセッションの依存関係を定義
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydanticモデル (APIに渡すデータ用)
class TodoCreate(BaseModel):
    title: str
    done_tasks: bool = False

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    done_tasks: Optional[bool] = None

class TagCreate(BaseModel):
    outline: str

class TagUpdate(BaseModel):
    outline: Optional[str] = None

# Todo 一覧取得 (GET)
@app.get("/todo", response_model=List[TodoCreate])
def get_todos(skip: int = 0, limit: int = 100, completed: Optional[bool] = None, db: Session = Depends(get_db)):
    query = db.query(TodoModel).offset(skip).limit(limit)
    if completed is not None:
        query = query.filter(TodoModel.done_tasks == completed)
    todos = query.all()
    return todos

# Todo 個別取得 (GET)
@app.get("/todo/{todo_id}", response_model=TodoCreate)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

# Todo 作成 (POST)
@app.post("/todo", response_model=TodoCreate)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    new_todo = TodoModel(**todo.dict())
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

# Todo 更新 (PUT)
@app.put("/todo/{todo_id}", response_model=TodoCreate)
def update_todo(todo_id: int, todo: TodoUpdate, db: Session = Depends(get_db)):
    db_todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    if todo.title is not None:
        db_todo.title = todo.title
    if todo.done_tasks is not None:
        db_todo.done_tasks = todo.done_tasks
    db.commit()
    db.refresh(db_todo)
    return db_todo

# Todo 削除 (DELETE)
@app.delete("/todo/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(db_todo)
    db.commit()
    return {"message": "Todo deleted"}

# Tag 一覧取得 (GET)
@app.get("/tag", response_model=List[TagCreate])
def get_tags(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tags = db.query(TagModel).offset(skip).limit(limit).all()
    return tags

# Tag 個別取得 (GET)
@app.get("/tag/{tag_id}", response_model=TagCreate)
def get_tag(tag_id: int, db: Session = Depends(get_db)):
    tag = db.query(TagModel).filter(TagModel.id == tag_id).first()
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag

# Tag 作成 (POST)
@app.post("/tag", response_model=TagCreate)
def create_tag(tag: TagCreate, db: Session = Depends(get_db)):
    new_tag = TagModel(**tag.dict())
    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)
    return new_tag

# Tag 更新 (PUT)
@app.put("/tag/{tag_id}", response_model=TagCreate)
def update_tag(tag_id: int, tag: TagUpdate, db: Session = Depends(get_db)):
    db_tag = db.query(TagModel).filter(TagModel.id == tag_id).first()
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    if tag.outline is not None:
        db_tag.outline = tag.outline
    db.commit()
    db.refresh(db_tag)
    return db_tag

# Tag 削除 (DELETE)
@app.delete("/tag/{tag_id}")
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    db_tag = db.query(TagModel).filter(TagModel.id == tag_id).first()
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    db.delete(db_tag)
    db.commit()
    return {"message": "Tag deleted"}