import streamlit as st
import os
import sys
from dotenv import load_dotenv



BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

sys.path.append(BASE_DIR)

env_path = os.path.join(BASE_DIR, ".env")
load_dotenv(env_path)

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")


#st.write("ENV PATH:", env_path)
#st.write("FILE EXISTS:", os.path.exists(env_path))
#st.write("ADMIN PASSWORD LOADED:", ADMIN_PASSWORD)

from db.database import init_db

from core.services import DocumentService
from core.analytics import AnalyticsServices


if "selected_doc" not in st.session_state:
    st.session_state.selected_doc = None


if "current_page" not in st.session_state:
    st.session_state.current_page = 0


if "last_recorded_page" not in st.session_state:
    st.session_state.last_recorded_page = -1 



if "search_results" not in st.session_state:
    st.session_state.search_results = []


if "reader_mode" not in st.session_state:
    st.session_state.reader_mode = False

if "show_reset" not in st.session_state:
    st.session_state.show_reset = False

init_db()

Service = DocumentService()
analytics = AnalyticsServices()

st.set_page_config(page_title="DocManager",layout="wide")

st.title("Smart PDF Document Manager")

st.divider()

st.subheader("Admin Controls")

if st.button("Clean Database"):
    st.session_state.show_reset = True

if st.session_state.show_reset:
    password_input = st.text_input("Enter Admin password", type="password")

    st.write("DEBUG:", ADMIN_PASSWORD)
    st.write("INPUT:", password_input)

    if st.button("Confirm Reset"):
        if password_input == ADMIN_PASSWORD:
            st.success("Access granted")
        
            import shutil
            # Delete DB
            if os.path.exists("data/documents.db"):
                os.remove("data/documents.db")

            # Delete storage
            pdf_dir = os.path.join("storage","pdf")
            thumbnail_dir = os.path.join("storage","Thumbnail")

            shutil.rmtree(pdf_dir, ignore_errors=True)
            shutil.rmtree(thumbnail_dir,ignore_errors=True)


            os.makedirs(pdf_dir,exist_ok=True)
            os.makedirs(thumbnail_dir,exist_ok=True)

            st.success("System reset successfully. Reset app.")

        else:
            st.error("Incorrect Password")


   
tabs = st.tabs(["Upload","Search & View","Analytics"])
        

with tabs[0]:
    st.header("Upload PDF")

    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
    tags = st.text_input("Tags(comma separated)")
    description = st.text_area("Description")
    lecture_date = st.date_input("Lecture Date (optional)",value=None)


    if st.button("Upload"):
        
        if uploaded_file:
            analytics.record_app_visit("upload_click")
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
        analytics.record_app_visit("search_click")
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
                        analytics.record_app_visit("open_click")
                        st.session_state.selected_doc = doc
                        st.session_state.current_page = 0
                        st.session_state.last_recorded_page = -1 
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
                    analytics.record_app_visit("previ_click")
                    st.session_state.current_page -= 1
                    st.rerun()

            with col3:
                if st.button("Next") and st.session_state.current_page < total_pages - 1:
                    analytics.record_app_visit("next_click")
                    st.session_state.current_page += 1
                    st.rerun()

            # ALWAYS read directly from session state
            img_path = os.path.join(
                image_dir,
                images[st.session_state.current_page]
            )

            st.image(img_path, width="stretch")

            # record page visit analytics
            if st.session_state.current_page != st.session_state.last_recorded_page:
                analytics.record_page_visit(doc.id, st.session_state.current_page)
                st.session_state.last_recorded_page = st.session_state.current_page

            unique_pages = analytics.get_unique_page_viewed(doc.id)
            progress = (unique_pages / doc.total_pages) * 100 if doc.total_pages else 0
            st.progress(progress/100)





            st.write(f"Progress: {progress:.2f}% ({unique_pages}/{doc.total_pages})")
            
            

        else:
            st.error("No images found")


        if st.button("Closer Reader"):
            analytics.record_app_visit("close_click")
            st.session_state.reader_mode = False
            st.session_state.last_recorded_page = -1




with tabs[2]:
    st.header("Analytics")


    if st.button("Reset Analytics"):
        analytics.reset_analytics()
        st.success("Analytics reset successfully ")

    st.subheader("App Usage")

    app_data = analytics.get_app_visits()

    import pandas as pd

    df = pd.DataFrame(app_data,columns=["Event" , "Count"])

    if df.empty:
        st.info("No analytics data yet. Perform some action to get insights.")
    else:
        st.bar_chart(df.set_index("Event"))


    st.subheader("Document Progress")

    docs = Service.get_all_documents()

    data = []

    for doc in docs:
        unique_pages= analytics.get_unique_page_viewed(doc.id)
        progress = (unique_pages / doc.total_pages) * 100 if doc.total_pages else 0


        data.append({
            "Document": doc.name,
            "Page Read" : unique_pages,
            "Total Pages": doc.total_pages,
            "Progress(%)": round(progress,2)
        })

    df_docs = pd.DataFrame(data)
    st.dataframe(df_docs)



    













