import streamlit as st
import mysql.connector
import matplotlib.pyplot as plt

# Initialize session state for marks records
if 'marks_records' not in st.session_state:
    st.session_state.marks_records = []

col1, col2, col3 = st.columns([1,1,1])

# with col1:
#     st.image("https://www.pngall.com/wp-content/uploads/5/Student-Icon-PNG-Picture.png", width=200)
# with col2:
st.header("Student Marks Management System")
st.write("Welcome to the Student Marks Management System. Please fill out the form below to add student marks.")
# with col3:
#     st.image("https://www.pngall.com/wp-content/uploads/5/Student-Icon-PNG-Picture.png", width=200)

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

def search_student(student_name, subject, years):
    connection = get_db_connection()
    cursor = connection.cursor()

    sql = "SELECT student_name, subject, years, total_marks, obtained_marks FROM std_marks"
    conditions = []
    params = []

    if student_name and student_name != "All Students":
        conditions.append("student_name = %s")
        params.append(student_name)
    if subject and subject != "All Subjects":
        conditions.append("subject = %s")
        params.append(subject)
    if years and years != "All Years":
        conditions.append("years = %s")
        params.append(years)

    if conditions:
        sql += " WHERE " + " AND ".join(conditions)

    cursor.execute(sql, tuple(params))
    results = cursor.fetchall()
    connection.close()
    return results

tab1, tab2 = st.tabs(["Add Marks", "View Records "])

with tab1:
    st.header("Enter Student Marks")
    
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

with tab2:
    st.header("Student Marks Records")

    student_names = ["All Students", "Aarav Kumar", "Priya Singh", "Rajesh Patel", "Neha Sharma", "Vikram Yadav", "Ananya Desai"]
    subjects = ["All Subjects", "Mathematics", "English", "Science", "Social Studies", "Computer Science", "Hindi", "Physics", "Chemistry", "Biology"]
    years = ["All Years", "2024", "2025", "2026"]
    col_search1, col_search2, col_search3 = st.columns(3)

    with col_search1:
        search_name = st.selectbox("Select Student", student_names, index=0)
    with col_search2:
        search_subject = st.selectbox("Select Subject", subjects, index=0)
    with col_search3:
        search_year = st.selectbox("Select Year", years, index=0)

    search_results = []
    if st.button("Search Records", use_container_width=True):
        search_results = search_student(search_name, search_subject, search_year)

    if search_results:
        filter_label = []
        if search_name != "All Students":
            filter_label.append(search_name)
        if search_subject != "All Subjects":
            filter_label.append(search_subject)
        if search_year != "All Years":
            filter_label.append(search_year)
        filter_text = " - ".join(filter_label) if filter_label else "All Records"

        # st.subheader(f"Search Results: {filter_text}")
        # for row in search_results:
        #     student, subject, year, total, obtained = row
        #     if total > 0:
        #         percentage = (obtained / total) * 100
        #     else:
        #         percentage = 0

        #     col1, col2, col3, col4, col5 = st.columns(5)
        #     with col1:
        #         st.metric("Year", year)
        #     with col2:
        #         st.metric("Student", student)
        #     with col3:
        #         st.metric("Subject", subject)
        #     with col4:
        #         st.metric("Marks", f"{obtained}/{total}")
        #     with col5:
        #         st.metric("Percentage", f"{percentage:.2f}%")
        #     st.divider()

        labels = [f"{row[0]} ({row[1]}, {row[2]})" for row in search_results]
        marks = [row[4] for row in search_results]

        fig, ax = plt.subplots(figsize=(10, 5))
        bars = ax.bar(labels, marks, color='skyblue', edgecolor='navy', linewidth=1)
        for bar, mark in zip(bars, marks):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                    f'{mark}', ha='center', va='bottom', fontweight='bold')

        ax.set_ylabel('Obtained Marks')
        ax.set_title(f'Marks for {filter_text}')
        ax.set_xlabel('Record')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.info("Select filters and click Search Records to display matching entries.")

    # if 'marks_records' in st.session_state and st.session_state.marks_records:
    #     st.subheader("All Marks Records")
    #     for idx, record in enumerate(st.session_state.marks_records):
    #         years = record['year']
    #         student = record['student']
    #         subject = record['subject']
    #         total = record['total']
    #         obtained = record['obtained']

    #         if total > 0:
    #             percentage = (obtained / total) * 100
    #         else:
    #             percentage = 0

    #         col1, col2, col3, col4, col5 = st.columns(5)
    #         with col1:
    #             st.metric("Year", years)
    #         with col2:
    #             st.metric("Student", student)
    #         with col3:
    #             st.metric("Subject", subject)
    #         with col4:
    #             st.metric("Marks", f"{obtained}/{total}")
    #         with col5:
    #             st.metric("Percentage", f"{percentage:.2f}%")
    #         st.divider()
    # else:
    #     st.info("No marks records found. Please add marks first.")