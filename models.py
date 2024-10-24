from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship,mapped_column,Mapped
from datetime import datetime
from settings import engine, Base

# TodoModelクラス (Todoテーブル用)
class TodoModel(Base):
    __tablename__ = 'todo'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String,nullable=False)
    created_date = Column(DateTime, default=datetime.utcnow)
    done_tasks: Mapped[bool] = mapped_column(Boolean,default=False)

    # リレーションシップ（SettingsModelに対するリレーション）
    settings = relationship('SettingsModel', back_populates='todo')

# TagModelクラス (Tagテーブル用)
class TagModel(Base):
    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True, autoincrement=True)
    outline: Mapped[str] = mapped_column(String,nullable=False)

    # リレーションシップ（SettingsModelに対するリレーション）
    settings = relationship('SettingsModel', back_populates='tag')

# SettingsModelクラス (外部キーを持つ設定用のテーブル)
class SettingsModel(Base):
    __tablename__ = 'settings' 

    id = Column(Integer, primary_key=True, autoincrement=True)

    # 外部キーとしてTodonumberを定義 (Todoテーブルのidを参照)
    todo_id = Column(Integer, ForeignKey('todo.id'), nullable=True)

    # 外部キーとしてtagnumberを定義 (Tagテーブルのidを参照)
    tag_id = Column(Integer, ForeignKey('tag.id'), nullable=False)

    # リレーションシップ
    todo = relationship('TodoModel', back_populates='settings')
    tag = relationship('TagModel', back_populates='settings')

# テーブルをデータベースに作成する
def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()
    print("テーブルが正常に作成されました。")
