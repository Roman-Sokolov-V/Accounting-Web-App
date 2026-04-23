import streamlit as st
from db.crud import (
    get_total_expense,
    get_total_revenue,
    get_total_cash,
    get_total_expense_prev_month,
    get_total_revenue_prev_month,
    get_total_cash_prev_month,
    get_total_receivable,
    get_total_payable
)
from db.engine import get_db
from pages.include.sidebar import get_sidebar

get_sidebar()

with get_db() as db:
    total_revenue = get_total_revenue(db)
    total_expense = get_total_expense(db)
    total_receivable = get_total_receivable(db)
    total_payable = get_total_payable(db)

    prev_revenue = get_total_revenue_prev_month(db)
    prev_expense = get_total_expense_prev_month(db)
    cash = get_total_cash(db)
    prev_cash = get_total_cash_prev_month(db)

profit = total_expense - total_revenue
prev_profit = prev_revenue - prev_expense
col1, col2 = st.columns(2)

with col1:
    st.metric(label="Total Revenue", value=f"{total_revenue:.2f} ₴")
    st.caption("Total accrued income (work performed)")

with col2:
    st.metric(label="Total Expense", value=f"{total_expense:.2f} ₴")
    st.caption("Total accrued expenses (services received)")

st.divider()

col1, col2 = st.columns(2)
with col1:
    st.metric(label="Total Receivable", value=f"{total_receivable:.2f} ₴")
    st.caption("Accounts receivable (customers owe us)")
with col2:
    st.metric(label="Total Payable", value=f"{total_payable:.2f} ₴")
    st.caption("Accounts payable (we owe suppliers)")

st.divider()

col1, col2 = st.columns(2)
with col1:
    st.metric(
    label="Profit",
    value=f"{profit:,.2f} ₴",
    delta=f"{(prev_profit):,.2f}",
    delta_color="normal"
    )
    st.caption("Difference between income and expenses")

with col2:
    st.metric(
    label="CASH",
    value=f"{cash:.2f} ₴",
    delta=f"{(prev_cash):,.2f}",
    delta_color="normal"
    )
    st.caption("Real money at the cash desk / in accounts")
st.divider()
