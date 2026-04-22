import streamlit as st
from db.crud import get_total_expense, get_total_revenue, get_total_cash
from db.engine import get_db

with st.sidebar:
    st.page_link("pages/transactions.py", label="Add transaction", icon="➕")
    st.page_link("pages/profit_loss.py", label="Profit & Loss", icon="📊")
    st.page_link("pages/partner_ledger.py", label="Partner ledger", icon="👥")
    st.page_link("pages/transactions_list.py", label="Transactions list", icon="📋")

with get_db() as db:
    total_revenue = get_total_revenue(db)
    total_expense = get_total_expense(db)
    cash = get_total_cash(db)

profit = total_expense - total_revenue
col1, col2 = st.columns(2)

col1.metric(label="Total Revenue", value=f"{total_revenue:.2f} ₴")
col2.metric(label="Total Expense", value=f"{total_expense:.2f} ₴")
col1.metric(
    label="Net Profit",
    value=f"{profit:,.2f} ₴",
    delta=f"{(profit):,.2f}",
    delta_color="normal" # "normal" зробить колір залежно від знаку
)
col2.metric(label="CASH", value=f"{cash:.2f} ₴")