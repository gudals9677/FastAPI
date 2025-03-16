from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:todos@127.0.0.1:3306/todos"

# echo = true 옵션을 통해 실행되는 쿼리 확인 -> bind=engine을 통해 연결
engine = create_engine(DATABASE_URL)
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# db connection
def get_db():
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()