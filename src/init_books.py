from werkzeug.utils import secure_filename
import os

def format_book_title(filename):
    """Преобразует имя файла в читаемое название книги"""
    title = os.path.splitext(filename)[0]
    return title.replace('_', ' ')

def ensure_books_folder(books_folder):
    """Создает папку для книг, если она не существует"""
    if not os.path.exists(books_folder):
        os.makedirs(books_folder)
        print(f"Created books folder: {books_folder}")

def add_sample_books(books_folder):
    """Добавляет примеры книг в указанную папку"""
    sample_books = [
        "Pride and Prejudice",
        "The Great Gatsby",
        "To Kill a Mockingbird",
        "1984",
        "The Catcher in the Rye"
    ]
    
    for title in sample_books:
        safe_title = secure_filename(title.replace(' ', '_'))
        book_path = os.path.join(books_folder, safe_title)
        if not os.path.exists(book_path):
            os.makedirs(book_path)
            print(f"Created book directory: {book_path}")

def initialize_books_structure(books_folder):
    """Инициализирует структуру папок для книг"""
    ensure_books_folder(books_folder)
    add_sample_books(books_folder)

def get_all_books(books_folder):
    """Получает список всех книг из указанной папки"""
    books = []
    if os.path.exists(books_folder):
        print(f"Books folder exists at {books_folder}")
        for book_name in os.listdir(books_folder):
            if os.path.isdir(os.path.join(books_folder, book_name)):
                from app import Book  # Импортируем здесь во избежание циклических импортов
                book = Book(book_name)
                books.append(book)
                print(f"Added book: {book_name}")
    print(f"Total books found: {len(books)}")
    return books

if __name__ == '__main__':
    # Можно запускать скрипт отдельно для инициализации структуры
    BOOKS_FOLDER = 'books'
    initialize_books_structure(BOOKS_FOLDER) 