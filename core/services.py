from db.repository import DocumentRepository
from core.file_manager import FileManager
from core.thumbnail import ThumbnailGenerator



class DocumentService:
    def __init__(self):
        self.repo = DocumentRepository()
        self.file_manager = FileManager()
        self.thumbnail_generator = ThumbnailGenerator()

    def upload_document(self, uploaded_file,tags,description,lecture_date=None):
        doc= []
        # 1. Save file
        file_path = self.file_manager.save_file(uploaded_file)

        # 2. Generate Thumbnail
        thumbnail_path = self.thumbnail_generator.generate_thumbnail(file_path)

        #3. total pages 
        total_pages = self.thumbnail_generator.get_total_pages(file_path)


        #self.repo.add_document(doc)