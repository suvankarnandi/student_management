import streamlit as st
import mysql.connector
import matplotlib.pyplot as plt
import numpy as np

st.title("Page 1: Search Student")

student_id = st.number_input('Enter the student ID', min_value=1, placeholder='Student ID')

def search_student(id):
    connection = mysql.connector.connect(
            host="localhost",      # Or your server IP
            user="root",
            password="Samriddhi@2026",
            database="test-db"
        )
    
    cursor = connection.cursor()
    
    sql = "SELECT * FROM std_marks WHERE id = %s"
    val = (id,)

    cursor.execute(sql, val)

    result = cursor.fetchall()
    connection.commit()
    connection.disconnect()
    return result

if st.button('Search Student'):
    student_data = search_student(id=student_id)
    if student_data:
        st.success("Student found!")
    st.subheader("Student Details")
    st.table(student_data)
        # for row in student_data:
        #     st.write(f"Student ID: {row[0]}")
        #     st.write(f"Student Name: {row[1]}")
        #     st.write(f"Student Class: {row[2]}")