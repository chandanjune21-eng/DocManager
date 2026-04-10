import streamlit as st
import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

sys.path.append(BASE_DIR)

from db.database import init_db

from core.services import DocumentService

init_db()

Service = DocumentService()

st.set_page_config(page_title="DocManager",layout="wide")

st.title("Smart PDF Document Manager")

st.divider()

tabs = st.tabs(["Upload","Search & View","Analytics"])
        

with tabs[0]:
    st.header("Upload PDF")

    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
    tags = st.text_input("Tags(comma separated)")
    description = st.text_area("Description")
    lecture_date = st.date_input("Lecture Date (optional)",value=None)


    if st.button("Upload"):
        if uploaded_file:
            Service.upload_document( uploaded_file,tags,description,lecture_date)
    else :
        st.error("Please upload a file")


with tabs[1]:
    st.header("Search & View")

    col1, col2 = st.columns(2)

    with col1:
        search_tag = st.text_input("Search by Tag")

    with col2:
        search_date = st.date_input("Search by Date",value=None)
    
    if st.button("Search"):
        

with tabs[2]:
    pass

