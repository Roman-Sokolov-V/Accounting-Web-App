from db.engine import SessionLocal


def seed_accounts(session=SessionLocal()):
    from db.models import DBAccounts

    existing = session.query(DBAccounts).first()
    if existing:
        return  # вже заініціалізовано

    accounts = [
        DBAccounts(code=1000, name="Cash", type="asset"),
        DBAccounts(code=1100, name="Accounts Receivable", type="asset"),
        DBAccounts(code=2000, name="Accounts Payable", type="liability"),
        DBAccounts(code=4000, name="Revenue", type="income"),
        DBAccounts(code=5000, name="Expense", type="expense"),
    ]

    session.add_all(accounts)
    session.commit()

if __name__ == '__main__':
    seed_accounts()