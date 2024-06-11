import streamlit as st
from db_utils import insert_card_info, get_card_info, get_all_card_info, initialize_db

# 데이터베이스 초기화
initialize_db()

st.title("Card Information Management")

menu = ["Add Card Info", "View Card Info", "View All Card Info"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add Card Info":
    st.subheader("Add Card Information")

    card_number = st.text_input("Card Number")
    card_holder_name = st.text_input("Card Holder Name")
    expiration_date = st.text_input("Expiration Date (MM/YY)")
    cvv = st.text_input("CVV")

    if st.button("Submit"):
        insert_card_info(card_number, card_holder_name, expiration_date, cvv)
        st.success("Card information added successfully!")

elif choice == "View Card Info":
    st.subheader("View Card Information")
    card_id = st.number_input("Enter Card ID", min_value=1)

    if st.button("View"):
        card_info = get_card_info(card_id)
        if card_info:
            encrypted = card_info['encrypted']
            decrypted = card_info['decrypted']
            
            st.write("### Encrypted Data")
            st.write("Card Number (Encrypted):", encrypted['card_number'].hex())
            st.write("Card Holder Name (Encrypted):", encrypted['card_holder_name'].hex())
            st.write("Expiration Date (Encrypted):", encrypted['expiration_date'].hex())
            st.write("CVV (Encrypted):", encrypted['cvv'].hex())
            
            st.write("### Decrypted Data")
            st.write("Card Number:", decrypted['card_number'])
            st.write("Card Holder Name:", decrypted['card_holder_name'])
            st.write("Expiration Date:", decrypted['expiration_date'])
            st.write("CVV:", decrypted['cvv'])
        else:
            st.error("Card not found")

elif choice == "View All Card Info":
    st.subheader("View All Card Information")
    card_infos = get_all_card_info()
    
    for card_info in card_infos:
        st.write(f"## Card ID: {card_info['id']}")
        
        encrypted = card_info['encrypted']
        decrypted = card_info['decrypted']
        
        st.write("### Encrypted Data")
        st.write("Card Number (Encrypted):", encrypted['card_number'].hex())
        st.write("Card Holder Name (Encrypted):", encrypted['card_holder_name'].hex())
        st.write("Expiration Date (Encrypted):", encrypted['expiration_date'].hex())
        st.write("CVV (Encrypted):", encrypted['cvv'].hex())
        
        st.write("### Decrypted Data")
        st.write("Card Number:", decrypted['card_number'])
        st.write("Card Holder Name:", decrypted['card_holder_name'])
        st.write("Expiration Date:", decrypted['expiration_date'])
        st.write("CVV:", decrypted['cvv'])
