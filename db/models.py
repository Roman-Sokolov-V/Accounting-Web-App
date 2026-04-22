import enum
from decimal import Decimal

from sqlalchemy import String, Integer, Enum, DECIMAL, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, declarative_base, relationship

Base = declarative_base()

# class AccountCode(enum.Enum):
#     CASH = 1000                       # грошові кошти (каса/рахунки)
#     ACCOUNTS_RECEIVABLE = 1100        # нам винні клієнти (дебіторська заборгованість)
#     ACCOUNTS_PAYABLE = 2000           # ми винні постачальникам (кредиторська заборгованість)
#     REVENUE = 4000                    # дохід (виручка)
#     EXPENSE = 5000                    # витрати

class DBPartners(Base):
    __tablename__ = "partners"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String, unique=False, nullable=True)


class DBAccounts(Base):
    __tablename__ = "accounts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    code: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)
    entries = relationship("DBEntries", back_populates="account")


class TransactionsTypes(enum.Enum):
    INCOME = "income"                      # дохід (нарахований дохід)
    EXPENSE = "expense"                    # витрата (нарахована витрата)
    PAYMENT_RECEIVED = "payment received"  # отримання грошових коштів (інкасація дебіторки)
    PAYMENT_SENT = "payment sent"          # виплата грошових коштів (погашення кредиторки)

class DBTransactions(Base):
    __tablename__ = "transactions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    type: Mapped[TransactionsTypes] = mapped_column(
        Enum(TransactionsTypes, name="transactions_types"),
        nullable=False
    )
    amount: Mapped[Decimal] = mapped_column(DECIMAL, nullable=False)
    description: Mapped[str] = mapped_column(String, unique=False, nullable=True)
    partner_id: Mapped[int] = mapped_column(Integer, ForeignKey("partners.id"))
    partner = relationship(DBPartners)
    entries = relationship("DBEntries", back_populates="transaction")

class DBEntries(Base):
    __tablename__ = "entries"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    debit: Mapped[Decimal] = mapped_column(DECIMAL, default=Decimal("0"))
    credit: Mapped[Decimal] = mapped_column(DECIMAL, default=Decimal("0"))
    transaction_id: Mapped[int] = mapped_column(Integer, ForeignKey("transactions.id"))
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"))
    transaction = relationship("DBTransactions", back_populates="entries")
    account = relationship("DBAccounts", back_populates="entries")

    __table_args__ = (
        CheckConstraint(
            "NOT (debit > 0 AND credit > 0)",
            name="ck_entry_no_debit_and_credit_together"
        ),
    )