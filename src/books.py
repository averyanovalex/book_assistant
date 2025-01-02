import os
import shutil
from werkzeug.utils import secure_filename
import logging
from werkzeug.datastructures import FileStorage

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BookOperations:
    # Определяем поддерживаемые форматы как атрибут класса
    SUPPORTED_FORMATS = ['txt', 'fb2', 'pdf']
    
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
                # return True, f"Успешно создана папка для книги: {title}", str(hash(safe_title))
            else:
                return False, f"Книга с таким названием уже существует: {title}", None
            
            # Сохраняем файл в папку
            file.save(os.path.join(book_path, file.filename))   

            # Векторизуем книгу
            self._vectorize_book(book_path, file.filename)

            return True, f"Книга успешно добавлена: {title}", str(hash(safe_title))
                
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
        

    def _vectorize_book(self, dir_path, filename):
        """Векторизует книгу"""
        from langchain_community.document_loaders import TextLoader, PyPDFLoader
        from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
        from langchain.vectorstores import FAISS
        from utils import get_openai_embedding_model
        
        file_path = os.path.join(dir_path, filename)
        logging.info(f"* file_path: {file_path}")

        # Определяем расширение файла
        file_extension = filename.split('.')[-1].lower()

        # Выбираем загрузчик в зависимости от расширения
        if file_extension in ['txt', 'fb2']:
            loader = TextLoader(file_path)
        elif file_extension == 'pdf':
            loader = PyPDFLoader(file_path)
        else:
            raise ValueError(f"Неподдерживаемый формат файла: {file_extension}")
        docs = loader.load()

        splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=200)

        if file_extension == 'pdf':
            splited_doc = []
            for page in docs:
                splited_doc += splitter.create_documents([page.page_content], metadatas=[page.metadata])
        else:
            splited_doc = splitter.create_documents([docs[0].page_content])

        logging.info(f"* splited_doc len: {len(splited_doc)}")

        embeddings = get_openai_embedding_model()

        db = FAISS.from_documents(splited_doc, embeddings)  
        db.save_local(f"{dir_path}/faiss_db")

        return
    


if __name__ == '__main__':
    # Создаем тестовую директорию для книг
    test_books_folder = 'books'
    
    # Инициализируем BookOperations 
    book_ops = BookOperations(test_books_folder)

    # Удаляем папку Capt если она существует
    if os.path.exists('books/Capt'):
        shutil.rmtree('books/Capt')
        print('* Папка Capt удалена')
    
    # Создаем тестовый файл
    test_file_path = 'tests/Капитанская дочка.txt'
    # test_file_path = 'tests/martin-eden-by-jack-london.pdf'
    with open(test_file_path, 'rb') as f:
        # Создаем объект FileStorage, который имитирует загруженный файл
        test_file = FileStorage(
            stream=f,
            filename='Капитанская дочка.txt',
            content_type='text/plain'
        )
        
        # Тестируем добавление книги
        success, message, book_id = book_ops.add_book('Capt', test_file)
        print(f'Результат: {success}')
        print(f'Сообщение: {message}')
        print(f'ID книги: {book_id}')

    print('* Тестирование завершено')

