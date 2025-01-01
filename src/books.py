import os
import shutil
from werkzeug.utils import secure_filename

class BookOperations:
    def __init__(self, books_folder):
        self.books_folder = books_folder
        
    def delete_book(self, book_title):
        """
        Удаляет книгу и её папку
        
        Args:
            book_title (str): Название книги
            
        Returns:
            tuple: (bool, str) - (успех операции, сообщение)
        """
        try:
            # Преобразуем название книги, заменяя пробелы на подчеркивания
            safe_title = book_title.replace(' ', '_')
            book_path = os.path.join(self.books_folder, safe_title)
            
            if os.path.exists(book_path):
                shutil.rmtree(book_path)  # Удаляем папку и всё её содержимое
                return True, f"Successfully deleted book: {book_title}"
            else:
                return False, f"Book directory not found: {book_path}"
                
        except Exception as e:
            return False, f"Error deleting book: {str(e)}" 