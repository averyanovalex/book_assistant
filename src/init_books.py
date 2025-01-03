import os
import shutil


def clean_books_folder(books_folder):
    """Removes all contents of the books folder."""
    if os.path.exists(books_folder):
        for item in os.listdir(books_folder):
            item_path = os.path.join(books_folder, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)
        print(f"Cleaned books folder: {books_folder}")
    else:
        os.makedirs(books_folder)
        print(f"Created books folder: {books_folder}")


def copy_preinstalled_books(books_folder):
    """Copies pre-installed books."""
    preinstalled_dir = "pre_installed/books_dir"
    if not os.path.exists(preinstalled_dir):
        print(f"Error: directory {preinstalled_dir} not found")
        return

    for item in os.listdir(preinstalled_dir):
        src_path = os.path.join(preinstalled_dir, item)
        dst_path = os.path.join(books_folder, item)
        if os.path.isdir(src_path):
            shutil.copytree(src_path, dst_path)
        else:
            shutil.copy2(src_path, dst_path)
    print(f"Copied pre-installed books from {preinstalled_dir}")


def initialize_books_structure(books_folder):
    """Initializes the folder structure for books."""


if __name__ == "__main__":
    # Script can be run separately to initialize the structure
    BOOKS_FOLDER = "books"
    clean_books_folder(BOOKS_FOLDER)
    copy_preinstalled_books(BOOKS_FOLDER)
