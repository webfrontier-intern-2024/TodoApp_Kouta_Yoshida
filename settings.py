from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import sys
import os

# .env.localファイルを読み込む
load_dotenv('env.local')

# 環境変数を取得
database_url = os.getenv('DATABASE_URL')
#DBがなければエラーをはいて終了　if文
if database_url is None:
    print("Error: Database URL not set in environment variables")
    sys.exit(1)  # エラー終了
engine = create_engine(database_url, echo=True)
# Baseクラスの定義
Base = declarative_base()

# この時点ではまだSessionインスタンスは生成されていない
# Session変数に格納されているのは実はsessionmakerインスタンス
Session = sessionmaker(
    autocommit = False,
    autoflush = True,
    bind = engine
    )

