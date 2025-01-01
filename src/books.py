import os
import shutil
from werkzeug.utils import secure_filename

class BookOperations:
    # Определяем поддерживаемые форматы как атрибут класса
    SUPPORTED_FORMATS = ['txt', 'fb2']
    
    def __init__(self, books_folder):
        self.books_folder = books_folder
        
    def add_book(self, title, file):
        """
        Добавляет новую книгу
        
        Args:
            title (str): Название книги
            file: Файл книги (из request.files)
            
        Returns:
            tuple: (bool, str, str) - (успех операции, сообщение, id книги)
        """
        try:
            # Проверяем формат файла
            if not self._is_supported_format(file.filename):
                return False, f"Неподдерживаемый формат. Поддерживаются: {', '.join(self.SUPPORTED_FORMATS)}", None
            
            # Подготавливаем название книги
            safe_title = secure_filename(title.replace(' ', '_'))
            book_path = os.path.join(self.books_folder, safe_title)
            
            # Создаем папку для книги
            if not os.path.exists(book_path):
                os.makedirs(book_path)
                return True, f"Успешно создана папка для книги: {title}", str(hash(safe_title))
            else:
                return False, f"Книга с таким названием уже существует: {title}", None
                
        except Exception as e:
            return False, f"Ошибка при добавлении книги: {str(e)}", None
            
    def _is_supported_format(self, filename):
        """Проверяет, поддерживается ли формат файла"""
        return filename.split('.')[-1].lower() in self.SUPPORTED_FORMATS
        
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