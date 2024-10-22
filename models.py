from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from settings import engine, Base

# TodoModelクラス (Todoテーブル用)
class TodoModel(Base):
    __tablename__ = 'Todo'

    Todonumber = Column(Integer, primary_key=True)
    title = Column(String)
    created_date = Column(DateTime, default=datetime.utcnow)
    done_tasks = Column(Boolean,default=False)

# TagModelクラス (Tagテーブル用)
class TagModel(Base):
    __tablename__ = 'Tag'

    tagnumber = Column(Integer, primary_key=True)
    outline = Column(String)

# settingsModelクラス (外部キーを持つ設定用のテーブル)
class SettingsModel(Base):
    __tablename__ = 'Settings' 

    id = Column(Integer, primary_key=True)

    # 外部キーとしてTodonumberを定義 (TodoテーブルのTodonumberを参照)
    Todonumber = Column(Integer, ForeignKey('Todo.Todonumber'))

    # 外部キーとしてtagnumberを定義 (Tagテーブルのtagnumberを参照)
    tagnumber = Column(Integer, ForeignKey('Tag.tagnumber'))

# create_tables.py


# テーブルをデータベースに作成する
def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()
    print("テーブルが正常に作成されました。")