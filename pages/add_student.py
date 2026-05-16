import streamlit as st
import mysql.connector

st.title("add student")
st.write("This is the content of add student.")

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Samriddhi@2026",
    "database": "test-db"
}

def get_db_connection():
    """Get database connection"""
    return mysql.connector.connect(**DB_CONFIG)

def add_student(years, student_name, total_marks, obtained_marks, subject):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    sql = "INSERT INTO std_marks (student_name, subject, years, total_marks, obtained_marks) VALUES (%s, %s, %s, %s, %s)"
    val = (student_name, subject, years, total_marks, obtained_marks)

    cursor.execute(sql, val)
   
    connection.commit()
    connection.close()

col1, col2 = st.columns(2)
    
with col1:
        st.subheader("Student Information")
        
        years = st.selectbox(
            "Select Year",
            options=[ "2024", "2025", "2026"],
            index=2
        )
        
        student_names = ["Aarav Kumar", "Priya Singh", "Rajesh Patel", "Neha Sharma", "Vikram Yadav", "Ananya Desai"]
        student_name = st.selectbox(
            "Select Student Name",
            options=student_names,
            index=0
        )
        
       
        subject = st.selectbox(
            " Select Subject",
            options=["Mathematics", "English", "Science", "Social Studies", "Computer Science", "Hindi", "Physics", "Chemistry", "Biology"],
            index=0
        )
    
with col2:
        st.subheader("Marks Information")
        
        total_marks = st.number_input(
            " Total Marks",
            min_value=0,
            max_value=1000,
            value=100,
            step=1
        )
        
        obtained_marks = st.number_input(
            " Obtained Marks",
            min_value=0,
            max_value=int(total_marks) if total_marks > 0 else 1000,
            value=0,
            step=1
        )
        if total_marks > 0:
            percentage = (obtained_marks / total_marks) * 100
            st.metric("Percentage", f"{percentage:.2f}%")
    
st.divider()
st.header("Summary")
col_summary1, col_summary2, col_summary3, col_summary4, col_summary5 = st.columns(5)
    
with col_summary1:
        st.metric("Year", years)
    
with col_summary2:
        st.metric("Student", student_name)
    
with col_summary3:
        st.metric("Subject", subject)
    
with col_summary4:
        st.metric("Total Marks", total_marks)
    
with col_summary5:
        if total_marks > 0:
            st.metric("Obtained", f"{obtained_marks}/{total_marks}")
        else:
            st.metric("Obtained", obtained_marks)
    
col_btn1, col_btn2 = st.columns(2)
    
with col_btn1:
        if st.button("Save Marks", use_container_width=True):
            if student_name and total_marks > 0:
                if 'marks_records' not in st.session_state:
                    st.session_state.marks_records = []
                
                record = {
                    'year': years,
                    'student': student_name,
                    'subject': subject,
                    'total': total_marks,
                    'obtained': obtained_marks
                }
                add_student(years, student_name, total_marks, obtained_marks, subject)
                
                st.session_state.marks_records.append(record)
                st.success(f" Marks saved successfully for {student_name} in {subject}!")
                # st.balloons()
            else:
                st.error("Please fill all fields correctly")
    
with col_btn2:
        if st.button("Clear Form", use_container_width=True):
            st.rerun()
