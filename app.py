import streamlit as st
import mysql.connector
from utils import encrypt, decrypt, connect_db

# MySQL 데이터베이스 연결 설정
db = connect_db()
cursor = db.cursor()

# Streamlit 애플리케이션
st.title("Card Information Management")

menu = ["Add Card Info", "View Card Info"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add Card Info":
    st.subheader("Add Card Information")

    card_number = st.text_input("Card Number")
    card_holder_name = st.text_input("Card Holder Name")
    expiration_date = st.text_input("Expiration Date (MM/YY)")
    cvv = st.text_input("CVV")

    if st.button("Submit"):
        encrypted_card_number = encrypt(card_number)
        encrypted_card_holder_name = encrypt(card_holder_name)
        encrypted_expiration_date = encrypt(expiration_date)
        encrypted_cvv = encrypt(cvv)

        sql = "INSERT INTO card_info (card_number, card_holder_name, expiration_date, cvv) VALUES (%s, %s, %s, %s)"
        val = (encrypted_card_number, encrypted_card_holder_name, encrypted_expiration_date, encrypted_cvv)
        cursor.execute(sql, val)
        db.commit()
        st.success("Card information added successfully!")

elif choice == "View Card Info":
    st.subheader("View Card Information")
    card_id = st.number_input("Enter Card ID", min_value=1)

    if st.button("View"):
        sql = "SELECT card_number, card_holder_name, expiration_date, cvv FROM card_info WHERE id = %s"
        val = (card_id,)
        cursor.execute(sql, val)
        result = cursor.fetchone()

        if result:
            encrypted_card_number, encrypted_card_holder_name, encrypted_expiration_date, encrypted_cvv = result
            card_number = decrypt(encrypted_card_number)
            card_holder_name = decrypt(encrypted_card_holder_name)
            expiration_date = decrypt(encrypted_expiration_date)
            cvv = decrypt(encrypted_cvv)

            st.write("Card Number:", card_number)
            st.write("Card Holder Name:", card_holder_name)
            st.write("Expiration Date:", expiration_date)
            st.write("CVV:", cvv)
        else:
            st.error("Card not found")

# 데이터베이스 연결 종료
cursor.close()
db.close()
