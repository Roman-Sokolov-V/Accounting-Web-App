from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.sql.functions import coalesce
from sqlalchemy.orm import Session

from db.engine import SessionLocal, engine, get_db
from db.models import (
    DBTransactions, DBAccounts, DBPartners, TransactionsTypes, DBEntries
)


def get_accounts(db: Session):
    accounts = db.query(DBAccounts).all()
    return accounts

def create_partner(db: Session, name: str, description: str|None=None):
    partner = DBPartners(name=name, description=description)
    db.add(partner)
    return partner

def get_partners(db: Session):
    return db.query(DBPartners).all()

def create_transaction(
        db: Session,
        type: str,
        amount: Decimal,
        partner_id: int,
        description: str|None=None
):
    transaction = DBTransactions(
        type=type,
        amount=amount,
        partner_id=partner_id,
        description=description
    )
    db.add(transaction)
    return transaction

def get_account_id(db: Session, name:str|None = None, code: int|None = None):
    if name:
        id = db.query(DBAccounts).filter(DBAccounts.name == name).first()
    elif code:
        id = db.query(DBAccounts).filter(DBAccounts.code == code).first()
    else:
        raise Exception('No name or code provided')
    return id

def create_entry(
        db: Session,
        transaction_id: int,
        account_id: int,
        debit: Decimal|None = None,
        credit: Decimal|None = None
):
    entry = DBEntries(
        transaction_id=transaction_id,
        account_id=account_id,
        debit=debit,
        credit=credit
    )
    db.add(entry)
    return entry



def get_account_by_name(db: Session, name: str):
    return db.query(DBAccounts).filter(DBAccounts.name == name).first()

def create_transaction_and_entries(
        db:Session,
        type: TransactionsTypes,
        amount: Decimal,
        partner_id: int,
        description: str|None=None):
    cash = get_account_by_name(db,"Cash")                      # грошові кошти (каса/рахунки)
    expense = get_account_by_name(db, "Expense")               # витрати
    payable = get_account_by_name(db, "Accounts Payable")      # ми винні постачальникам (кредиторська заборгованість)
    revenue = get_account_by_name(db, "Revenue")               # дохід (виручка)
    receivable = get_account_by_name(db, "Accounts Receivable")# нам винні клієнти (дебіторська заборгованість)
    try:
        # Активні
        # рахунки(Cash, Receivable, Expense):
        # + (Збільшення) = Debit
        # - (Зменшення) = Credit
        # Пасивні
        # рахунки(Payable, Revenue, Equity):
        # + (Збільшення) = Credit
        # - (Зменшення) = Debit
        transaction = create_transaction(
            db, type, amount, partner_id, description
        )
        db.flush()  # Отримуємо ID транзакції
        # 2. Логіка вибору рахунків (Accounting Logic)
        if type == TransactionsTypes.EXPENSE:
            # Нам надали послугу/товар, ми тепер ВИННІ гроші
            entries = [
                {"debit": amount, "account_id": expense.id},  # Витрати (+) -> Дебет
                {"credit": amount, "account_id": payable.id}  # Борг перед постачальником (+) -> Кредит
            ]

        elif type == TransactionsTypes.INCOME:
            # Ми надали послугу, нам ТЕПЕР ВИННІ гроші
            entries = [
                {"debit": amount, "account_id": receivable.id},  # Борг клієнта перед нами (+) -> Дебет
                {"credit": amount, "account_id": revenue.id}  # Дохід (+) -> Кредит
            ]

        elif type == TransactionsTypes.PAYMENT_RECEIVED:
            # Клієнт погасив свій борг грошима
            entries = [
                {"debit": amount, "account_id": cash.id},  # Готівка (+) -> Дебет
                {"credit": amount, "account_id": receivable.id}  # Борг клієнта перед нами (-) -> Кредит
            ]

        elif type == TransactionsTypes.PAYMENT_SENT:
            # Ми погасили свій борг перед постачальником
            entries = [
                {"debit": amount, "account_id": payable.id},  # Наш борг перед постачальником (-) -> Дебет
                {"credit": amount, "account_id": cash.id}  # Готівка (-) -> Кредит
            ]

        # 3. Створюємо записи (Entries)
        for entry_data in entries:
            create_entry(db=db, transaction_id=transaction.id, **entry_data)
        return transaction
    except Exception as e:
        db.rollback()  # Скасовуємо ВСЕ, якщо хоча б один крок не вдався
        raise e

def get_total_revenue(db: Session):
    revenue_account = get_account_by_name(db, "Revenue")
    return db.query(
        func.sum(coalesce(DBEntries.credit, 0)) -
        func.sum(coalesce(DBEntries.debit, 0))
    ).filter(DBEntries.account_id == revenue_account.id).scalar()

def get_total_expense(db: Session):
    expense_account = get_account_by_name(db, "Expense")
    return db.query(
        func.sum(coalesce(DBEntries.debit, 0)) -
        func.sum(coalesce(DBEntries.credit, 0))
    ).filter(DBEntries.account_id == expense_account.id).scalar()

def get_total_cash(db: Session):
    cash_account = get_account_by_name(db, "Cash")
    return db.query(
        func.sum(coalesce(DBEntries.debit, 0)) -
        func.sum(coalesce(DBEntries.credit, 0))
    ).filter(DBEntries.account_id == cash_account.id).scalar()

if __name__ == "__main__":
    with get_db() as db:

        print(get_total_revenue(db))
        print(get_total_expense(db))
        print(get_total_cash(db))
