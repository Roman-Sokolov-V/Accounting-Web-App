from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

BASE_DIR = Path(__file__).resolve().parent.parent
#SQLALCHEMY_DATABASE_URL = "sqlite:///./db.sqlite3"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{BASE_DIR / 'db.sqlite3'}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db  # передаємо сесію в код
        db.commit()
    except Exception as e:
        db.rollback() # відкат при помилці
        raise Exception(e)
    finally:
        db.close() # ГАРАНТОВАНЕ закриття