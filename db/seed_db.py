import random
from datetime import date, timedelta
from decimal import Decimal

from db.crud import create_transaction_and_entries, get_partners
from db.engine import get_db
from db.models import DBAccounts, DBPartners, TransactionsTypes


def seed_accounts(db=get_db()):
    with db as session:
        existing = session.query(DBAccounts).first()
        if existing:
            return

        accounts = [
            DBAccounts(code=1000, name="Cash", type="asset"),
            DBAccounts(code=1100, name="Accounts Receivable", type="asset"),
            DBAccounts(code=2000, name="Accounts Payable", type="liability"),
            DBAccounts(code=4000, name="Revenue", type="income"),
            DBAccounts(code=5000, name="Expense", type="expense"),
        ]

        session.add_all(accounts)
        session.commit()


def seed_partners(db=get_db()):
    with db as session:
        existing = session.query(DBPartners).first()
        if existing:
            return
        partners = [DBPartners(name=f"partner {i}") for i in range(1, 10)]
        session.add_all(partners)
        session.commit()


def seed_transactions(db=get_db()):
    with db as session:
        partners = get_partners(db=session)
        if not partners:
            print("Спочатку додайте партнерів!")
            return

        partners_ids = [partner.id for partner in partners]

        transaction_types = list(TransactionsTypes)

        today_val = date.today()
        dates_list = [today_val - timedelta(days=delta) for delta in range(1, 30)]

        for d in dates_list:
            for _ in range(5):
                try:
                    create_transaction_and_entries(
                        db=session,
                        date=d,
                        type=random.choice(transaction_types),
                        amount=Decimal(random.randint(100, 10000)),
                        partner_id=random.choice(partners_ids),
                    )
                except Exception as e:
                    print(f"Помилка при створенні: {e}")
        session.commit()


if __name__ == "__main__":
    seed_accounts()
    seed_partners()
    seed_transactions()
