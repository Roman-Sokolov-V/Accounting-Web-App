from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, declarative_base

Base = declarative_base()


class DBPartners(Base):
    __tablename__ = "partners"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    description: Mapped[str] = mapped_column(String, unique=False, nullable=True)