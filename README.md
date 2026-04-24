# 📊 Accounting Web App

A minimal accounting web application built with **Python** and **Streamlit**.
The project demonstrates core accounting principles such as **double-entry bookkeeping**, **basic financial flows**, and **simple reporting**.

---

# 🚀 Features

## Core Accounting Logic

* Double-entry system (debit / credit)
* Fixed chart of accounts
* Automatic posting from transactions to entries
* Supported operations:

  * Income (accrued revenue)
  * Expense (accrued expense)
  * Payment received (cash inflow)
  * Payment sent (cash outflow)

---

## 📄 Reports

### Profit & Loss (P&L)

* Displays total **Revenue vs Expenses**
* Based on accrual accounting

### Partner Ledger

* Shows movements for a selected partner
* Running balance (who owes whom)
* Based on Accounts Receivable (AR) and Accounts Payable (AP)

---

## 👥 Partners

* Create and manage partners (customers/vendors)
* Track balances per partner

---

## 📋 Transactions & Entries

* Create business transactions
* Automatically generate accounting entries
* View all entries

---

# 🧠 Accounting Model

## Fixed Chart of Accounts

| Code | Name                | Type      |
| ---- | ------------------- | --------- |
| 1000 | Cash                | Asset     |
| 1100 | Accounts Receivable | Asset     |
| 2000 | Accounts Payable    | Liability |
| 4000 | Revenue             | Income    |
| 5000 | Expense             | Expense   |

---

## Double Entry Principle

Each transaction generates at least **two entries**:

* one **debit**
* one **credit**

Example:

```
# Income (not yet paid)
AR       debit 1000
Revenue  credit 1000
```

---

# 🏗️ Project Structure

```
Accounting-Web-App/
├── alembic/              # Database migrations
├── db/                   # DB layer (models, CRUD, engine, seed)
├── pages/                # Streamlit pages
├── Dockerfile
├── docker-compose.yml
├── profit_loss.py
├── prompt_history.md     # LLM usage log (required)
├── requirements.txt
└── settings.py
```

---

# ⚙️ Tech Stack

* Python 3.11+
* Streamlit
* SQLAlchemy
* Alembic
* SQLite / PostgreSQL
* Docker

---

# ▶️ Running the Project

## 🟢 Option 1 — Run locally (SQLite, no Docker)

1. Switch database in `settings.py`:

```python
DATABASE = "sqlite"
# DATABASE = "postgres"
```

2. Apply migrations:

```bash
alembic upgrade head
```

3. Seed initial data (accounts):

```bash
python db/seed_db.py
```

4. Run the app:

```bash
streamlit run profit_loss.py
```

---

## 🐳 Option 2 — Run with Docker (PostgreSQL)

1. Rename environment file:

```bash
mv .env.sample .env
```

2. Start the project:

```bash
docker compose up --build
```

3. Open in browser:

```
http://localhost:8502
```

---

# 🌱 Database Initialization

The application uses **seed data** for the chart of accounts.

* Implemented in: `db/seed_db.py`
* Ensures fixed accounts are always present
* Runs manually (SQLite) or via container startup (Docker)

---

# 🤖 LLM Usage

LLM tools were used during development for:

* system design
* accounting domain understanding
* implementation support

Full prompt history is available in:

```
prompt_history.md
```

---

# 🎯 Design Decisions

* Fixed chart of accounts (no account CRUD)
* Double-entry bookkeeping model
* Clear separation: Transactions → Entries
* Minimal UI (Streamlit)
* Simple DB setup (SQLite / PostgreSQL)

---

# ⚠️ Limitations

* No authentication
* No multi-currency
* No taxes
* No reconciliation
* Minimal validation layer

---

# 📌 Notes

* Partner ledger balance is meaningful only in chronological order
* UI sorting may affect interpretation of running balance
* System follows accrual accounting principles

---

# ✅ Status

* Working minimal accounting system
* Covers core flows and reports
* Ready for review

## 📬 Contacts

If you have any questions or feedback regarding this project, feel free to reach out:

* GitHub: https://github.com/Roman-Sokolov-V/
* linkedin: https://www.linkedin.com/in/roman-sokolov-a7614330b/
* Email: [roman.sokolov.developer@gmail.com](mailto:roman.sokolov.developer.gmail.com)

