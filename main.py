from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from settings import Session
from models import Models
# 非同期データベースエンジンの作成
session = Session()

# データベースのベースモデル
Base = declarative_base()

# モデル定義
models = Models()

# FastAPIアプリケーションの初期化
from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")

# データベースの初期化
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Todo一覧取得
@app.get("/todos", response_model=List[TodoResponse])
async def get_todos():
    async with async_session() as session:
        result = await session.execute(select(TodoModel))
        todos = result.scalars().all()
        return todos

# Todo作成
@app.post("/todos", response_model=TodoResponse)
async def create_todo(todo: TodoCreate):
    new_todo = TodoModel(title=todo.title)
    async with async_session() as session:
        session.add(new_todo)
        await session.commit()
        await session.refresh(new_todo)
        return new_todo

# Todo完了の更新
@app.put("/todos/{id}", response_model=TodoResponse)
async def update_todo_status(id: int):
    async with async_session() as session:
        result = await session.execute(select(TodoModel).where(TodoModel.Todonumber == id))
        todo = result.scalar_one_or_none()
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        todo.done_tasks = True
        await session.commit()
        return todo

# Todo削除
@app.delete("/todos/{id}")
async def delete_todo(id: int):
    async with async_session() as session:
        result = await session.execute(select(TodoModel).where(TodoModel.Todonumber == id))
        todo = result.scalar_one_or_none()
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        await session.delete(todo)
        await session.commit()
        return {"message": "Todo deleted"}

# タグ一覧取得
@app.get("/tags", response_model=List[TagResponse])
async def get_tags():
    async with async_session() as session:
        result = await session.execute(select(TagModel))
        tags = result.scalars().all()
        return tags

# タグ作成
@app.post("/tags", response_model=TagResponse)
async def create_tag(tag: TagCreate):
    new_tag = TagModel(outline=tag.outline)
    async with async_session() as session:
        session.add(new_tag)
        await session.commit()
        await session.refresh(new_tag)
        return new_tag