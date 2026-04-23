import streamlit as st
from db.crud import create_partner, get_partners
from db.engine import get_db
from pages.include.sidebar import get_sidebar

get_sidebar()

st.write("Add new partner")
name = st.text_input("name", placeholder="Enter a description (required)")
description = st.text_input("description", placeholder="Enter a description (not required)")

if name:
    if st.button("Add partner"):
        with get_db() as session:
            create_partner(db=session, name=name, description=description)
        st.write ("New partner is added to database")


st.write("Our partner ledger")
with get_db() as session:
    partners = get_partners(db=session)

partners_data = [
    {
        "ID": p.id,
        "Name": p.name,
        "Description": p.description,
        # Формуємо посилання на сторінку деталей
        "Details": f"/partner_details?partner_id={p.id}"
    } for p in partners
]

st.dataframe(
    partners_data,
    column_config={
        "Details": st.column_config.LinkColumn(
            "Взаєморозрахунки",
            help="Натисніть, щоб переглянути історію операцій",
            validate=r"^/partner_details\?partner_id=\d+$",
            display_text="Відкрити деталі 🔍" # Текст, який бачить користувач
        ),
    },
    use_container_width=True,
    hide_index=True
)