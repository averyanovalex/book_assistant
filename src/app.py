from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
import os
import shutil
from init_books import format_book_title, initialize_books_structure, get_all_books
from books import BookOperations

app = Flask(__name__)
app.config['BOOKS_FOLDER'] = 'books'
book_ops = BookOperations(app.config['BOOKS_FOLDER'])

class Book:
    def __init__(self, title):
        self.raw_title = title
        self.title = format_book_title(title)
        self.id = hash(title)
        self.path = os.path.join(app.config['BOOKS_FOLDER'], title)

@app.route('/')
def home():
    books = get_all_books(app.config['BOOKS_FOLDER'])
    return render_template('home.html', books=books)

@app.route('/chat/<path:book_title>')
def chat(book_title):
    books = get_all_books(app.config['BOOKS_FOLDER'])
    book = Book(book_title)
    return render_template('chat.html', books=books, book=book)

@app.route('/upload_book', methods=['POST'])
def upload_book():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    title = request.form['title']
    success, message, book_id = book_ops.add_book(title, file)
    
    if success:
        return jsonify({'success': True, 'book_id': book_id}), 200
    else:
        return jsonify({'error': message}), 400

@app.route('/delete_book/<path:book_title>', methods=['POST'])
def delete_book(book_title):
    success, message = book_ops.delete_book(book_title)
    print(message)  # Логируем результат операции
    
    if not success:
        return message, 500
        
    return redirect(url_for('home'))

@app.route('/api/chat', methods=['POST'])
def api_chat():
    # Это заглушка. В реальном приложении здесь будет обработка сообщения и генерация ответа.
    user_message = request.json['message']
    return jsonify({'response': f"This is a response to: {user_message}"})

if __name__ == '__main__':
    app.run(debug=True)

