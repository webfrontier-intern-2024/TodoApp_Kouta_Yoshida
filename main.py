from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from models import TodoModel
from settings import SessionLocal
from operation import router as api_router  # operation.py のルーターをインポート
import uvicorn

# Jinja2Templatesの初期化
templates = Jinja2Templates(directory="templates")

# FastAPIアプリケーションの初期化
app = FastAPI()

# データベースセッションの依存関係
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# タスク一覧ページ
@app.get("/", response_class=HTMLResponse)
async def get_tasks(request: Request, db: Session = Depends(get_db)):
    # データベースから全てのタスクを取得
    tasks = db.query(TodoModel).all()
    return templates.TemplateResponse("home.html", {"request": request, "tasks": tasks})

# タスク追加ページ
@app.get("/add-task", response_class=HTMLResponse)
async def add_task_page(request: Request):
    return templates.TemplateResponse("add_task.html", {"request": request})

# タスク追加処理
@app.post("/submit-task")
async def submit_task(request: Request, task_name: str = Form(...), task_details: str = Form(...), task_deadline: str = Form(...), db: Session = Depends(get_db)):
    # 新しいタスクをデータベースに追加
    new_task = TodoModel(title=task_name, done_tasks=False)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    # タスク一覧ページにリダイレクト
    tasks = db.query(TodoModel).all()
    return templates.TemplateResponse("home.html", {"request": request, "tasks": tasks})

# operation.pyのAPIルーターを追加
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")