from datetime import date, timedelta

import random
from decimal import Decimal

from db.crud import get_partners, create_transaction_and_entries, get_accounts
from db.engine import SessionLocal, get_db
from db.models import DBAccounts, DBPartners, DBTransactions, TransactionsTypes


def seed_accounts(session=SessionLocal()):
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
    session.close()

def seed_partners(session=SessionLocal()):
    existing = session.query(DBPartners).first()
    if existing:
        return
    partners = [DBPartners(name=f"partner {i}") for i in range(1, 10)]
    session.add_all(partners)
    session.commit()
    session.close()


def seed_transactions(db=get_db()):
    with db as session:
        partners = get_partners(db=session)
        if not partners:
            print("Спочатку додайте партнерів!")
            return

        partners_ids = [partner.id for partner in partners]

        # ВИПРАВЛЕННЯ: беремо типи транзакцій з Enum, а не з акаунтів
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
                        partner_id=random.choice(partners_ids)
                    )
                except Exception as e:
                    print(f"Помилка при створенні: {e}")
        session.commit()



if __name__ == '__main__':
    # seed_accounts()
    # seed_partners()
    seed_transactions()