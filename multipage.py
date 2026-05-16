import streamlit as st

pg = st.navigation([st.Page("login.py"), st.Page("studentmarks_app.py")])
pg.run()