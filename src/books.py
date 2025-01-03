import logging
import os
import shutil

from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import FAISS
from transliterate import translit
from werkzeug.utils import secure_filename

from utils import get_openai_embedding_model

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def format_book_title(filename):
    """Converts filename to readable book title"""
    title = os.path.splitext(filename)[0]
    return title.replace("_", " ")


def format_book_path(book_title):
    """Converts book title to path"""
    return book_title.replace(" ", "_")


def ensure_books_folder(books_folder):
    """Creates books folder if it doesn't exist"""
    if not os.path.exists(books_folder):
        os.makedirs(books_folder)
        print(f"Created books folder: {books_folder}")


def get_all_books(books_folder):
    """Gets list of all books from specified folder"""
    books = []
    if os.path.exists(books_folder):
        print(f"Books folder exists at {books_folder}")
        for book_name in os.listdir(books_folder):
            if os.path.isdir(os.path.join(books_folder, book_name)):
                book = Book(book_name)
                books.append(book)
                print(f"Added book: {book_name}")
    print(f"Total books found: {len(books)}")
    return books


class Book:
    def __init__(self, title):
        self.raw_title = format_book_path(title)
        self.title = format_book_title(title)
        self.id = hash(title)
        self.path = os.path.join("books", self.raw_title)


class BookOperations:
    """Class for handling book operations like adding and deleting books"""

    SUPPORTED_FORMATS = ["txt", "pdf"]

    def __init__(self, books_folder):
        self.books_folder = books_folder

    def add_book(self, title, file):
        """
        Adds a new book to the library.

        Args:
            title (str): Book title
            file: Book file (from request.files)

        Returns:
            tuple: (bool, str, str) - (operation success, message, book id)
        """
        try:
            if not self._is_supported_format(file.filename):
                return (
                    False,
                    (
                        f"Unsupported format. Supported formats: "
                        f"{', '.join(self.SUPPORTED_FORMATS)}"
                    ),
                    None,
                )

            try:
                safe_title = translit(title, "ru", reversed=True)
            except:
                safe_title = title

            safe_title = secure_filename(safe_title.replace(" ", "_"))
            book_path = os.path.join(self.books_folder, safe_title)

            if not os.path.exists(book_path):
                os.makedirs(book_path)
            else:
                return False, f"Book with this title already exists: {title}", None

            file.save(os.path.join(book_path, file.filename))
            self._vectorize_book(book_path, file.filename)

            return True, f"Book successfully added: {title}", str(hash(safe_title))

        except Exception as e:
            return False, f"Error adding book: {str(e)}", None

    def _is_supported_format(self, filename):
        """Checks if file format is supported"""
        return filename.split(".")[-1].lower() in self.SUPPORTED_FORMATS

    def delete_book(self, book_title):
        """
        Deletes book and its folder.

        Args:
            book_title (str): Book title

        Returns:
            tuple: (bool, str) - (operation success, message)
        """
        try:
            try:
                safe_title = translit(book_title, "ru", reversed=True)
            except:
                safe_title = book_title

            safe_title = secure_filename(safe_title.replace(" ", "_"))
            book_path = os.path.join(self.books_folder, safe_title)

            if os.path.exists(book_path):
                shutil.rmtree(book_path)
                return True, f"Book successfully deleted: {book_title}"
            else:
                return False, f"Book folder not found: {book_path}"

        except Exception as e:
            return False, f"Error deleting book: {str(e)}"

    def _vectorize_book(self, dir_path, filename):
        """
        Vectorizes the book content for search functionality.

        Args:
            dir_path (str): Path to book directory
            filename (str): Name of the book file
        """
        file_path = os.path.join(dir_path, filename)
        logging.info(f"* file_path: {file_path}")

        file_extension = filename.split(".")[-1].lower()

        if file_extension == "txt":
            loader = TextLoader(file_path)
        elif file_extension == "pdf":
            loader = PyPDFLoader(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
        docs = loader.load()

        splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=200)

        if file_extension == "pdf":
            splited_doc = []
            for page in docs:
                splited_doc += splitter.create_documents(
                    [page.page_content], metadatas=[page.metadata]
                )
        else:
            splited_doc = splitter.create_documents([docs[0].page_content])

        logging.info(f"* splited_doc len: {len(splited_doc)}")

        embeddings = get_openai_embedding_model()

        db = FAISS.from_documents(splited_doc, embeddings)
        db.save_local(f"{dir_path}/faiss_db")

        return
