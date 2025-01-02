import os
import shutil

def clean_books_folder(books_folder):
    """Удаляет все содержимое папки books"""
    if os.path.exists(books_folder):
        for item in os.listdir(books_folder):
            item_path = os.path.join(books_folder, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)
        print(f"Очищена папка книг: {books_folder}")
    else:
        os.makedirs(books_folder)
        print(f"Создана папка книг: {books_folder}")

def copy_preinstalled_books(books_folder):
    """Копирует предустановленные книги"""
    preinstalled_dir = "pre_installed/books_dir"
    if not os.path.exists(preinstalled_dir):
        print(f"Ошибка: директория {preinstalled_dir} не найдена")
        return
        
    for item in os.listdir(preinstalled_dir):
        src_path = os.path.join(preinstalled_dir, item)
        dst_path = os.path.join(books_folder, item)
        if os.path.isdir(src_path):
            shutil.copytree(src_path, dst_path)
        else:
            shutil.copy2(src_path, dst_path)
    print(f"Скопированы предустановленные книги из {preinstalled_dir}")

def initialize_books_structure(books_folder):
    """Инициализирует структуру папок для книг"""
    

if __name__ == '__main__':
    # Можно запускать скрипт отдельно для инициализации структуры
    BOOKS_FOLDER = 'books'
    clean_books_folder(BOOKS_FOLDER)
    copy_preinstalled_books(BOOKS_FOLDER)