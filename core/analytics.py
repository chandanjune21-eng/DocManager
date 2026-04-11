from datetime import datetime
from db.database import get_connection

class AnalyticsServices:

    def record_page_visit(self, document_id, page_number):
        conn= get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO page_visits(document_id,page_number,timestamp)
        VALUES(?,?,?)    
        """,(document_id,page_number,datetime.now().isoformat()))

        conn.commit()
        conn.close()


    def get_unique_page_viewed(self,document_id):
        conn = get_connection()
        cursor = conn.cursor()


        cursor.execute("""
        SELECT COUNT(DISTINCT page_number)
        FROM page_visits
        WHERE document_id= ?
        """,(document_id,))

        result = cursor.fetchone()[0]
        conn.close()

        return result if result else 0
    