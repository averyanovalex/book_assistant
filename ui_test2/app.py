from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    file_path = db.Column(db.String(200), nullable=False)

def add_sample_books():
    sample_books = [
        {"title": "Pride and Prejudice", "file_path": "uploads/pride_and_prejudice.epub"},
        {"title": "The Great Gatsby", "file_path": "uploads/the_great_gatsby.pdf"},
        {"title": "To Kill a Mockingbird", "file_path": "uploads/to_kill_a_mockingbird.epub"},
        {"title": "1984", "file_path": "uploads/1984.pdf"},
        {"title": "The Catcher in the Rye", "file_path": "uploads/the_catcher_in_the_rye.epub"},
    ]
    
    for book in sample_books:
        if not Book.query.filter_by(title=book["title"]).first():
            new_book = Book(title=book["title"], file_path=book["file_path"])
            db.session.add(new_book)
    
    db.session.commit()

def get_all_books():
    return Book.query.all()

@app.route('/')
def home():
    books = get_all_books()
    return render_template('home.html', books=books)

@app.route('/chat/<int:book_id>')
def chat(book_id):
    books = get_all_books()
    book = Book.query.get_or_404(book_id)
    return render_template('chat.html', books=books, book=book)

@app.route('/upload_book', methods=['POST'])
def upload_book():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and file.filename.split('.')[-1].lower() in ['txt', 'fb2']:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        new_book = Book(title=request.form['title'], file_path=file_path)
        db.session.add(new_book)
        db.session.commit()
        return jsonify({'success': True, 'book_id': new_book.id}), 200
    else:
        return jsonify({'error': 'Unsupported file format. Please upload TXT or FB2 files.'}), 400

@app.route('/delete_book/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    os.remove(book.file_path)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/api/chat', methods=['POST'])
def api_chat():
    # This is a mock response. In a real application, you'd process the message and generate a response.
    user_message = request.json['message']
    return jsonify({'response': f"This is a response to: {user_message}"})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        add_sample_books()
    app.run(debug=True)

