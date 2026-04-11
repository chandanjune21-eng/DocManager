import streamlit as st
import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

sys.path.append(BASE_DIR)

from db.database import init_db

from core.services import DocumentService
from core.analytics import AnalyticsServices


if "selected_doc" not in st.session_state:
    st.session_state.selected_doc = None


if "current_page" not in st.session_state:
    st.session_state.current_page = 0



if "search_results" not in st.session_state:
    st.session_state.search_results = []


if "reader_mode" not in st.session_state:
    st.session_state.reader_mode = False

init_db()

Service = DocumentService()
analytics = AnalyticsServices()

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
        search_date = st.date_input("Search by Date", value=None)

    #  SEARCH BUTTON
    if st.button("Search"):
        st.session_state.search_results = Service.search_document(
            tag=search_tag if search_tag else None,
            date=str(search_date) if search_date else None
        )

    #  ALWAYS define results
    results = st.session_state.search_results

    #  SHOW RESULTS
    if results and not st.session_state.reader_mode:
        st.subheader(f"Results: {len(results)} documents")
        container = st.container(height=500)

        with container:
            for doc in results:
                col1, col2 = st.columns([1, 3])

                with col1:
                    if doc.thumbnail_path:
                        st.image(doc.thumbnail_path, width=120)

                with col2:
                    st.write(f"**{doc.name}**")
                    st.write(f"Tags: {doc.tags}")
                    st.write(f"Description: {doc.description}")
                    st.write(f"Lecture Date: {doc.lecture_date}")

                    if st.button("Open", key=f"open_{doc.id}"):
                        st.session_state.selected_doc = doc
                        st.session_state.current_page = 0
                        st.session_state.reader_mode = True
                        st.rerun()

    
    # READER MODE
# READER MODE
if st.session_state.reader_mode and st.session_state.get("selected_doc"):
    st.write("Reader Mode Active")

    doc = st.session_state.selected_doc
    st.subheader(f"Reading: {doc.name}")

    folder_name = os.path.basename(doc.path).replace(".pdf", "")
    image_dir = f"storage/pdfs/{folder_name}"

    if not os.path.exists(image_dir):
        st.error("Image not found. PDF conversion failed")
    else:
        images = sorted(os.listdir(image_dir))
        total_pages = len(images)

        if total_pages > 0:

            # clamp page safely
            st.session_state.current_page = max(
                0,
                min(st.session_state.current_page, total_pages - 1)
            )

            col1, col2, col3 = st.columns([1, 2, 1])

            with col1:
                if st.button("Previous") and st.session_state.current_page > 0:
                    st.session_state.current_page -= 1
                    st.rerun()

            with col3:
                if st.button("Next") and st.session_state.current_page < total_pages - 1:
                    st.session_state.current_page += 1
                    st.rerun()

            # ALWAYS read directly from session state
            img_path = os.path.join(
                image_dir,
                images[st.session_state.current_page]
            )

            st.image(img_path, width="stretch")

            # record page visit analytics
            analytics.record_page_visit(doc.id,st.session_state.current_page)

            unique_pages = analytics.get_unique_page_viewed(doc.id)
            progress = (unique_pages / doc.total_pages) * 100 if doc.total_pages else 0
            st.progress(progress/100)





            st.write(f"Progress: {progress:.2f}% ({unique_pages}/{doc.total_pages})")
            

        else:
            st.error("No images found")


        if st.button("Closer Reader"):
            st.session_state.reader_mode = False

with tabs[2]:
    pass

