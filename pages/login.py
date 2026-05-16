import streamlit as st
import mysql.connector

if 'login_key' in st.session_state:
    st.switch_page("pages/search_student.py")
else:

    st.title("Welcome to ABC School")
    st.subheader("Please login to continue")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")


    def login(username, password):     
        connection = mysql.connector.connect(
                host="localhost",      # Or your server IP
                user="root",
                password="Samriddhi@2026",
                database="test-db"
            )
        
        cursor = connection.cursor()
        
        sql = "SELECT * FROM auth_table WHERE username = %s AND password = %s"
        val = (username, password)

        cursor.execute(sql, val)

        result = cursor.fetchall()
        connection.commit()
        connection.close()
        return result

    if st.button("Login"):
        user_data = login(username, password)
        if user_data:
            if 'login_key' not in st.session_state:
                st.session_state['login_key'] = username
            st.success(f"Welcome {username}! Login successful!")
            st.switch_page("pages/dashboard.py")
            
                
        else:
            st.error("Invalid username or password.")
            if 'login_key' in st.session_state:
                del st.session_state['login_key']