import streamlit as st
from db.crud import (
    get_total_expense,
    get_total_revenue,
    get_total_cash,
    get_total_expense_prev_month,
    get_total_revenue_prev_month,
    get_total_cash_prev_month
)
from db.engine import get_db

with st.sidebar:
    st.page_link("pages/transactions.py", label="Add transaction", icon="➕")
    st.page_link("pages/profit_loss.py", label="Profit & Loss", icon="📊")
    st.page_link("pages/partner_ledger.py", label="Partner ledger", icon="👥")
    st.page_link("pages/transactions_list.py", label="Transactions list", icon="📋")

with get_db() as db:
    total_revenue = get_total_revenue(db)
    total_expense = get_total_expense(db)
    prev_revenue = get_total_revenue_prev_month(db)
    prev_expense = get_total_expense_prev_month(db)
    cash = get_total_cash(db)
    prev_cash = get_total_cash_prev_month(db)

profit = total_expense - total_revenue
prev_profit = prev_revenue - prev_expense
col1, col2 = st.columns(2)

col1.metric(label="Total Revenue", value=f"{total_revenue:.2f} ₴")
col2.metric(label="Total Expense", value=f"{total_expense:.2f} ₴")
col1.metric(
    label="Net Profit",
    value=f"{profit:,.2f} ₴",
    delta=f"{(prev_profit):,.2f}",
    delta_color="normal"
)
col2.metric(
    label="CASH",
    value=f"{cash:.2f} ₴",
    delta=f"{(prev_cash):,.2f}",
    delta_color="normal"
)