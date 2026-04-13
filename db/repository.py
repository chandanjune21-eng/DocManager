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

    
    def search_document(self,tag=None,date=None):
        conn = get_connection()
        cursor = conn.cursor()

        query = """
    SELECT 
        id,
        name,
        path,
        thumbnail_path,
        tags,
        description,
        upload_date,
        lecture_date,
        total_pages
    FROM documents
    """
        condition = []
        params = []

        # WHERE, OR

        if tag:
            condition.append("tags LIKE ?")
            params.append(f"%{tag}%")

        if date:
            condition.append("lecture_date = ?")
            params.append(date)


        if condition:
            query += " WHERE " + " AND ".join(condition)

        cursor.execute(query,params)
        rows = cursor.fetchall()
        conn.close()

        return [Document(*row) for row in rows]
    
    def get_all_documents(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT 
            id,
            name,
            path,
            thumbnail_path,
            tags,
            description,
            upload_date,
            lecture_date,
            total_pages
        FROM documents
        """)

        rows = cursor.fetchall()
        conn.close()

        return [Document(*row) for row in rows]
        

