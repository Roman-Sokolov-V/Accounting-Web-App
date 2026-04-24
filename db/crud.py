from datetime import date, datetime, timedelta
from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql.functions import coalesce

from db.engine import get_db
from db.models import (
    DBAccounts,
    DBEntries,
    DBPartners,
    DBTransactions,
    TransactionsTypes,
)


def get_accounts(db: Session):
    accounts = db.query(DBAccounts).all()
    return accounts


def create_partner(db: Session, name: str, description: str | None = None):
    partner = DBPartners(name=name, description=description)
    db.add(partner)
    return partner


def get_partners(db: Session):
    return db.query(DBPartners).all()


def get_partner(db: Session, partner_id: int | None = None):
    if partner_id is not None:
        partner = db.query(DBPartners).filter(DBPartners.id == partner_id).first()
        return partner
    else:
        raise Exception("No partner_id provided")


def get_partner_entries(db: Session, partner_id: int | None = None):
    if partner_id is not None:
        entries = (
            db.query(DBEntries)
            .join(DBEntries.transaction)
            .join(DBEntries.account)
            .filter(
                DBTransactions.partner_id == partner_id,
                DBAccounts.code.in_([1100, 2000]),
            )
            .options(joinedload(DBEntries.account), joinedload(DBEntries.transaction))
            .order_by(DBEntries.date.asc())
            .all()
        )
        return entries
    else:
        raise Exception("No partner_id provided")


def create_transaction(
    db: Session,
    date: datetime,
    type: str,
    amount: Decimal,
    partner_id: int,
    description: str | None = None,
):
    transaction = DBTransactions(
        date=date,
        type=type,
        amount=amount,
        partner_id=partner_id,
        description=description,
    )
    db.add(transaction)
    return transaction


def get_all_transactions(db: Session):
    return db.query(DBTransactions).options(joinedload(DBTransactions.entries)).all()


def get_account_id(db: Session, name: str | None = None, code: int | None = None):
    if name:
        id = db.query(DBAccounts).filter(DBAccounts.name == name).first()
    elif code:
        id = db.query(DBAccounts).filter(DBAccounts.code == code).first()
    else:
        raise Exception("No name or code provided")
    return id


def create_entry(
    db: Session,
    date: datetime,
    transaction_id: int,
    account_id: int,
    debit: Decimal | None = None,
    credit: Decimal | None = None,
):
    entry = DBEntries(
        transaction_id=transaction_id,
        date=date,
        account_id=account_id,
        debit=debit,
        credit=credit,
    )
    db.add(entry)
    return entry


def get_all_entries(db: Session):
    return db.query(DBEntries).options(joinedload(DBEntries.account)).all()


def get_account_by_name(db: Session, name: str):
    return db.query(DBAccounts).filter(DBAccounts.name == name).first()


def create_transaction_and_entries(
    db: Session,
    date: datetime,
    type: TransactionsTypes,
    amount: Decimal,
    partner_id: int,
    description: str | None = None,
):
    cash = get_account_by_name(db, "Cash")
    expense = get_account_by_name(db, "Expense")
    payable = get_account_by_name(
        db, "Accounts Payable"
    )
    revenue = get_account_by_name(db, "Revenue")
    receivable = get_account_by_name(
        db, "Accounts Receivable"
    )
    try:
        transaction = create_transaction(
            db, date, type, amount, partner_id, description
        )
        db.flush()
        if type == TransactionsTypes.EXPENSE:
            entries = [
                {"debit": amount, "account_id": expense.id},
                {
                    "credit": amount,
                    "account_id": payable.id,
                },
            ]

        elif type == TransactionsTypes.INCOME:
            entries = [
                {
                    "debit": amount,
                    "account_id": receivable.id,
                },
                {"credit": amount, "account_id": revenue.id},
            ]

        elif type == TransactionsTypes.PAYMENT_RECEIVED:
            entries = [
                {"debit": amount, "account_id": cash.id},
                {
                    "credit": amount,
                    "account_id": receivable.id,
                },
            ]

        elif type == TransactionsTypes.PAYMENT_SENT:
            entries = [
                {
                    "debit": amount,
                    "account_id": payable.id,
                },
                {"credit": amount, "account_id": cash.id},
            ]

        # 3. Створюємо записи (Entries)
        for entry_data in entries:
            create_entry(
                db=db,
                transaction_id=transaction.id,
                date=transaction.date,
                **entry_data,
            )
        return transaction
    except Exception as e:
        db.rollback()
        raise e


def get_total_revenue(db: Session):
    revenue_account = get_account_by_name(db, "Revenue")
    return (
        db.query(
            func.sum(coalesce(DBEntries.credit, 0))
            - func.sum(coalesce(DBEntries.debit, 0))
        )
        .filter(DBEntries.account_id == revenue_account.id)
        .scalar()
    )


def first_last_days_prev_month():
    today = date.today()
    first_day_current = today.replace(day=1)
    last_day_prev_month = first_day_current - timedelta(days=1)
    first_day_prev_month = last_day_prev_month.replace(day=1)
    return first_day_prev_month, last_day_prev_month


def get_total_revenue_prev_month(db: Session):
    revenue_account = get_account_by_name(db, "Revenue")
    first_day_last_month, last_day_last_month = first_last_days_prev_month()

    return (
        db.query(
            func.sum(coalesce(DBEntries.credit, 0))
            - func.sum(coalesce(DBEntries.debit, 0))
        )
        .filter(
            DBEntries.account_id == revenue_account.id,
            DBEntries.date >= first_day_last_month,
            DBEntries.date <= last_day_last_month,
        )
        .scalar()
    )


def get_total_expense(db: Session):
    expense_account = get_account_by_name(db, "Expense")
    return (
        db.query(
            func.sum(coalesce(DBEntries.debit, 0))
            - func.sum(coalesce(DBEntries.credit, 0))
        )
        .filter(DBEntries.account_id == expense_account.id)
        .scalar()
    )


def get_total_expense_prev_month(db: Session):
    expense_account = get_account_by_name(db, "Expense")
    first_day_last_month, last_day_last_month = first_last_days_prev_month()
    return (
        db.query(
            func.sum(coalesce(DBEntries.debit, 0))
            - func.sum(coalesce(DBEntries.credit, 0))
        )
        .filter(
            DBEntries.account_id == expense_account.id,
            DBEntries.date >= first_day_last_month,
            DBEntries.date <= last_day_last_month,
        )
        .scalar()
    )


def get_total_cash(db: Session):
    cash_account = get_account_by_name(db, "Cash")
    return (
        db.query(
            func.sum(coalesce(DBEntries.debit, 0))
            - func.sum(coalesce(DBEntries.credit, 0))
        )
        .filter(DBEntries.account_id == cash_account.id)
        .scalar()
    )


def get_total_cash_prev_month(db: Session):
    cash_account = get_account_by_name(db, "Cash")
    _, last_day_last_month = first_last_days_prev_month()
    return (
        db.query(
            func.sum(coalesce(DBEntries.debit, 0))
            - func.sum(coalesce(DBEntries.credit, 0))
        )
        .filter(
            DBEntries.account_id == cash_account.id,
            DBEntries.date <= last_day_last_month,
        )
        .scalar()
    )


def get_total_receivable(db: Session):
    account = get_account_by_name(db, "Accounts Receivable")
    return (
        db.query(
            func.sum(coalesce(DBEntries.debit, 0))
            - func.sum(coalesce(DBEntries.credit, 0))
        )
        .filter(DBEntries.account_id == account.id)
        .scalar()
    )


def get_total_payable(db: Session):
    account = get_account_by_name(db, "Accounts Payable")
    return (
        db.query(
            func.sum(func.coalesce(DBEntries.credit, 0))
            - func.sum(func.coalesce(DBEntries.debit, 0))
        )
        .filter(DBEntries.account_id == account.id)
        .scalar()
    )


if __name__ == "__main__":
    with get_db() as db:
        print(get_total_revenue(db))
        print(get_total_expense(db))
        print(get_total_cash(db))
