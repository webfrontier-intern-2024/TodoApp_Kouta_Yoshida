from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse  # HTMLResponseをインポート
from pydantic import BaseModel
from typing import List
from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from settings import Session 
import uvicorn

# データベースのベースモデル
Base = declarative_base()

# Jinja2Templatesの初期化
templates = Jinja2Templates(directory="templates")

# FastAPIアプリケーションの初期化
app = FastAPI()

# タスクのリストを保持するための変数 (仮データベース)
tasks = []

# タスク一覧ページ
@app.get("/", response_class=HTMLResponse)
async def get_tasks(request: Request):
    # 現在のタスクのリストをテンプレートに渡す
    return templates.TemplateResponse("home.html", {"request": request, "tasks": tasks})

# タスク追加ページ
@app.get("/add-task", response_class=HTMLResponse)
async def add_task_page(request: Request):
    return templates.TemplateResponse("add_task.html", {"request": request})

# タスク追加処理
@app.post("/submit-task")
async def submit_task(request: Request, task_name: str = Form(...), task_details: str = Form(...), task_deadline: str = Form(...)):
    # フォームから送られてきたタスクを追加
    new_task = {
        "name": task_name,
        "details": task_details,
        "deadline": task_deadline
    }
    tasks.append(new_task)
    # タスク一覧ページにリダイレクト
    return templates.TemplateResponse("home.html", {"request": request, "tasks": tasks})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
