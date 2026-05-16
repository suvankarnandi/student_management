import streamlit as st
import mysql.connector
import matplotlib.pyplot as plt

st.title("Search Student")
st.write("This is the content of Search Student.")

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Samriddhi@2026",
    "database": "test-db"
}

def get_db_connection():
    """Get database connection"""
    return mysql.connector.connect(**DB_CONFIG)

def search_student(id, student_name, subject, years):
    connection = get_db_connection()
    cursor = connection.cursor()

    sql = "SELECT id, student_name, subject, years, total_marks, obtained_marks FROM std_marks"
    conditions = []
    params = []

    if student_name and student_name != "All Students":
        conditions.append("student_name = %s")
        params.append(student_name)
    if id and id != "All IDs":
        conditions.append("id = %s")
        params.append(id)
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

st.header("Student Marks Records")

student_names = ["All Students", "Aarav Kumar", "Priya Singh", "Rajesh Patel", "Neha Sharma", "Vikram Yadav", "Ananya Desai"]
subjects = ["All Subjects", "Mathematics", "English", "Science", "Social Studies", "Computer Science", "Hindi", "Physics", "Chemistry", "Biology"]
years = ["All Years", "2024", "2025", "2026"]
ids = ["All IDs"] + [str(i) for i in range(1, 101)]  # Assuming IDs from 1 to 100
col_search1, col_search2, col_search3, col_search4 = st.columns(4)

with col_search1:
        search_name = st.selectbox("Select Student", student_names, index=0)
with col_search2:
        search_subject = st.selectbox("Select Subject", subjects, index=0)
with col_search3:
        search_year = st.selectbox("Select Year", years, index=0)
with col_search4:
     search_id = st.selectbox("Select ID", ids, index=0)


search_results = []
if st.button("Search Records", use_container_width=True):
        search_results = search_student(search_id, search_name, search_subject, search_year)

if search_results:
        filter_label = []
        if search_name != "All Students":
            filter_label.append(search_name)
        if search_subject != "All Subjects":
            filter_label.append(search_subject)
        if search_year != "All Years":
            filter_label.append(search_year)
        if search_id != "All IDs":
            filter_label.append(search_id)
        filter_text = " - ".join(filter_label) if filter_label else "All Records"
        
        st.subheader(f"Search Results: {filter_text}")
        for row in search_results:
            student, subject, year, total, obtained = row
            if total > 0:
                percentage = (obtained / total) * 100
            else:
                percentage = 0

            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric("Year", year)
            with col2:
                st.metric("Student", student)
            with col3:
                st.metric("Subject", subject)
            with col4:
                st.metric("Marks", f"{obtained}/{total}")
            with col5:
                st.metric("Percentage", f"{percentage:.2f}%")
            st.divider()
    
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