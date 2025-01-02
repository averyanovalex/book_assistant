from flask import Flask, render_template, request, jsonify, redirect, url_for, g
from werkzeug.utils import secure_filename
import os
import shutil
from init_books import format_book_title, initialize_books_structure, get_all_books
from books import BookOperations
from agent import create_assistant_chain
import logging
from collections import defaultdict

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

agent = None

app = Flask(__name__)
app.config['BOOKS_FOLDER'] = 'books'
book_ops = BookOperations(app.config['BOOKS_FOLDER'])

chat_histories = defaultdict(list)

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
    global agent
    books = get_all_books(app.config['BOOKS_FOLDER'])
    book = Book(book_title)
    
    # Инициализируем агента для выбранной книги
    try:
        agent = create_assistant_chain(f'{book.path}/faiss_db')
        logging.info(f"* Created agent for book: {book_title}")
    except Exception as e:
        logging.error(f"* Error creating agent: {str(e)}")
        return render_template('error.html', error=f"Failed to load book: {str(e)}"), 500

    # Получаем историю чата для этой книги
    book_chat_history = chat_histories[book_title]
    return render_template('chat.html', books=books, book=book, chat_history=book_chat_history)

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
    
    if not success:
        return message, 500
        
    return redirect(url_for('home'))

@app.route('/api/chat', methods=['POST'])
def api_chat():
    global agent

    user_message = request.json['message']
    book_title = request.json['book_title']
    logging.info(f"* User message: {user_message}")

    if agent is None:
        logging.info(f'* Agent is not initialized')
        return jsonify({'error': 'Please select a book first'})
    
    try:
        response = agent.invoke(user_message)
        logging.info(f"* Response: {response}")
        
        # Сохраняем сообщения в историю
        chat_histories[book_title].append({
            'type': 'user',
            'content': user_message
        })
        chat_histories[book_title].append({
            'type': 'assistant',
            'content': response
        })
        
        return jsonify({'response': response})
    except Exception as e:
        logging.error(f"* Chat error: {str(e)}")
        return jsonify({'error': str(e)}), 500
    

if __name__ == '__main__':
    app.run(debug=True)

