from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

import settings

SQLALCHEMY_DATABASE_URL = settings.SQLALCHEMY_DATABASE_URL

if settings.DATABASE == "sqlite":
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )

    SessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=engine, expire_on_commit=False
    )

    @contextmanager
    def get_db():
        db = SessionLocal()
        try:
            yield db
            db.commit()
        except Exception as e:
            db.rollback()
            raise Exception(e)
        finally:
            db.close()


if settings.DATABASE == "postgres":
    postgresql_engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)

    PostgresqlSessionLocal = sessionmaker(  # type: ignore
        bind=postgresql_engine,
        class_=Session,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
    )

    @contextmanager
    def get_db():
        db = PostgresqlSessionLocal()
        try:
            yield db
            db.commit()
        except Exception as e:
            db.rollback()
            raise Exception(e)
        finally:
            db.close()
