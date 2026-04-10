from db.database import get_connection
from core.model import Document


class DocumentRepository:


    def add_document(self,doc:Document):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO documents(
            name,path, thumbnail_path, tags,description,
            upload_date, lecture_date, total_pages
        )
        VALUES(?,?,?,?,?,?,?,?)
        """,(
            doc.name,
            doc.path,
            doc.thumbnail_path,
            doc.tags,
            doc.description,
            doc.upload_date,
            doc.lecture_date,
            doc.total_pages
        ))

        conn.commit()
        conn.close()