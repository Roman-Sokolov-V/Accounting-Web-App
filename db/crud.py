from decimal import Decimal

from sqlalchemy.orm import Session

from db.engine import SessionLocal, engine
from db.models import (
    DBTransactions, DBAccounts, DBPartners, TransactionsTypes, DBEntries
)

db = SessionLocal()

def get_accounts(db: Session):
    accounts = db.query(DBAccounts).all()
    print(accounts)
    return accounts

def create_partner(db: Session, name: str, description: str|None=None):
    partner = DBPartners(name=name, description=description)
    db.add(partner)
    db.commit()
    db.refresh(partner)
    print(partner)
    return partner

def create_not_commited_transaction(
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
    db.commit()
    db.refresh(entry)
    print(entry)
    return entry

def create_not_commited_entry(
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

def get_partners_dict(db: Session):
    partners = db.query(DBPartners).all()
    partners_dict = {f"id: {partner.id}, name: {partner.name}": partner.id for partner in partners}
    print(partners_dict)
    return partners_dict

def get_partners(db):
    return db.query(DBPartners).all()

def get_account_by_name(db: Session, name: str):
    return db.query(DBAccounts).filter(DBAccounts.name == name).first()

def create_transaction_and_entries(
        db:Session,
        type: TransactionsTypes,
        amount: Decimal,
        partner_id: int,
        description: str|None=None):
    cash = get_account_by_name(db,"Cash")
    expense = get_account_by_name(db, "Expense")
    payable = get_account_by_name(db, "Accounts Payable")
    revenue = get_account_by_name(db, "Revenue")
    receivable = get_account_by_name(db, "Receivable")
    try:
        transaction = create_not_commited_transaction(
            db, type, amount, partner_id, description
        )
        db.flush()  # Отримуємо ID транзакції

        # 2. Логіка вибору рахунків (Accounting Logic)
        if type == TransactionsTypes.EXPENSE:
            entries = [
                {"debit": amount, "account_id": expense.id},
                {"credit": amount, "account_id": payable.id}
            ]
        elif type == TransactionsTypes.INCOME:
            entries = [
                {"debit": amount, "account_id": receivable.id},  # Зменшуємо борг що нам заборговано
                {"credit": amount, "account_id": revenue.id}  # і наш дохід
            ]
        elif type == TransactionsTypes.PAYMENT_RECEIVED:
            entries = [
                {"debit": amount, "account_id": cash.id},
                {"credit": amount, "account_id": receivable.id}
            ]
        elif type == TransactionsTypes.PAYMENT_SENT:
            entries = [
                {"debit": amount, "account_id": payable.id},  # Зменшуємо борг перед постачальником
                {"credit": amount, "account_id": cash.id}  # Зменшуємо готівку
            ]
        else:
            raise ValueError(f"Unknown transaction type: {type}")

        # 3. Створюємо записи (Entries)
        for entry_data in entries:
            create_entry(db=db, transaction_id=transaction.id, **entry_data)
        db.commit()
        return transaction

    except Exception as e:
        db.rollback()  # Скасовуємо ВСЕ, якщо хоча б один крок не вдався
        raise e

if __name__ == "__main__":
    #get_accounts(db)
    create_partner(db, 'Рога і ратиці', '')
    #create_transaction(db, TransactionsTypes.EXPENSE, "100", "1")
    #create_entry(db=db, transaction_id=1, account_id=1, debit=100)
    get_partners = get_partners_dict(db)
