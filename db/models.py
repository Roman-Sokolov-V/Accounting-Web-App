import enum
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    DECIMAL,
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship

Base = declarative_base()


class DBPartners(Base):
    __tablename__ = "partners"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String, unique=False, nullable=True)
    transactions = relationship("DBTransactions", back_populates="partner")


class DBAccounts(Base):
    __tablename__ = "accounts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    code: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)
    entries = relationship("DBEntries", back_populates="account")


class TransactionsTypes(enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"
    PAYMENT_RECEIVED = (
        "payment received"
    )
    PAYMENT_SENT = "payment sent"


class DBTransactions(Base):
    __tablename__ = "transactions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    date: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False, index=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    type: Mapped[TransactionsTypes] = mapped_column(
        Enum(TransactionsTypes, name="transactions_types"), nullable=False
    )
    amount: Mapped[Decimal] = mapped_column(DECIMAL, nullable=False)
    description: Mapped[str] = mapped_column(String, unique=False, nullable=True)
    partner_id: Mapped[int] = mapped_column(Integer, ForeignKey("partners.id"))
    partner = relationship(DBPartners, back_populates="transactions")
    entries = relationship("DBEntries", back_populates="transaction")


class DBEntries(Base):
    __tablename__ = "entries"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    date: Mapped[datetime] = mapped_column(DateTime, index=True)
    debit: Mapped[Decimal] = mapped_column(DECIMAL, default=Decimal("0"))
    credit: Mapped[Decimal] = mapped_column(DECIMAL, default=Decimal("0"))
    transaction_id: Mapped[int] = mapped_column(Integer, ForeignKey("transactions.id"))
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"))
    transaction = relationship("DBTransactions", back_populates="entries")
    account = relationship("DBAccounts", back_populates="entries")

    __table_args__ = (
        Index("ix_entries_account_date", "account_id", "date"),
        CheckConstraint(
            "NOT (debit > 0 AND credit > 0)",
            name="ck_entry_no_debit_and_credit_together",
        ),
    )
