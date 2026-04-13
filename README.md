# 📄 DocManager

## Smart PDF Document Manager

A **Streamlit-based Smart PDF management system** for uploading, searching, reading, and tracking documents with built-in analytics and admin controls.

---

# 🚀 Features

## 📤 Upload PDFs
- Upload PDF files
- Add tags, description, and lecture date
- Auto storage & processing

---

## 🔍 Smart Search
- Search by tags
- Search by date
- Instant results with preview thumbnails

---

## 📖 PDF Reader Mode
- Page-by-page navigation
- Next / Previous controls
- Reading progress tracking
- Resume reading support

---

## 📊 Analytics Dashboard
- App usage tracking (upload, search, open, navigation)
- Document-wise reading progress
- Page-level engagement insights
- Visual charts using Streamlit

---

## 🔐 Admin System
- Password-protected admin controls
- Full system reset (DB + storage cleanup)

---

# 🖼️ Screenshots

> Add your screenshots inside a folder called `/screenshots`

### 📌 Home / Upload Page
![Upload](screenshots/upload.png)

### 📌 Search & Results Page
![Search](screenshots/search.png)

### 📌 PDF Reader Mode
![Reader](screenshots/reader.png)

### 📌 Analytics Dashboard
![Analytics](screenshots/analytics.png)

---

# 🛠️ Tech Stack

- Python 🐍
- Streamlit ⚡
- SQLite 🗄️
- Pandas 📊
- dotenv 🔐
- OS & shutil

---

# 📁 Project Structure

```text
DocManager/
│
├── app/
│   └── project.py
│
├── core/
│   ├── services.py
│   ├── analytics.py
│   └── reader.py
│
├── db/
│   ├── database.py
│   └── repository.py
│
├── data/
│   └── documents.db
│
├── storage/
│   ├── pdf/
│   ├── Thumbnail/
│   └── pdfs/
│
├── screenshots/
│   ├── upload.png
│   ├── search.png
│   ├── reader.png
│   └── analytics.png
│
├── .env
├── pyproject.toml
└── README.md