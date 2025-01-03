import logging
from collections import defaultdict

from flask import Flask, jsonify, redirect, render_template, request, url_for

from agent import create_assistant_chain
from books import Book, BookOperations, get_all_books

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

agent = None

app = Flask(__name__)
app.config["BOOKS_FOLDER"] = "books"
book_ops = BookOperations(app.config["BOOKS_FOLDER"])

chat_histories = defaultdict(list)


@app.route("/")
def home():
    """Render home page with list of all books."""
    books = get_all_books(app.config["BOOKS_FOLDER"])
    return render_template("home.html", books=books)


@app.route("/chat/<path:book_title>")
def chat(book_title):
    """
    Initialize chat page for specific book.

    Args:
        book_title (str): Title of the book to chat about

    Returns:
        rendered template: Chat page with book context
    """
    global agent
    books = get_all_books(app.config["BOOKS_FOLDER"])
    book = Book(book_title)

    try:
        agent = create_assistant_chain(f"{book.path}/faiss_db")
        logging.info(f"* Created agent for book: {book_title}")
    except Exception as e:
        logging.error(f"* Error creating agent: {str(e)}")
        return (
            render_template("error.html", error=f"Failed to load book: {str(e)}"),
            500,
        )

    book_chat_history = chat_histories[book_title]
    return render_template(
        "chat.html", books=books, book=book, chat_history=book_chat_history
    )


@app.route("/upload_book", methods=["POST"])
def upload_book():
    """
    Handle book upload request.

    Returns:
        JSON response with upload status
    """
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    title = request.form["title"]
    success, message, book_id = book_ops.add_book(title, file)

    if success:
        return jsonify({"success": True, "book_id": book_id}), 200
    else:
        return jsonify({"error": message}), 400


@app.route("/delete_book/<path:book_title>", methods=["POST"])
def delete_book(book_title):
    """
    Delete specified book.

    Args:
        book_title (str): Title of book to delete

    Returns:
        redirect: Redirect to home page after deletion
    """
    success, message = book_ops.delete_book(book_title)

    if not success:
        return message, 500

    return redirect(url_for("home"))


@app.route("/api/chat", methods=["POST"])
def api_chat():
    """
    Handle chat API requests.

    Returns:
        JSON response with chat message or error
    """
    global agent

    user_message = request.json["message"]
    book_title = request.json["book_title"]
    logging.info(f"* User message: {user_message}")

    if agent is None:
        logging.info(f"* Agent is not initialized")
        return jsonify({"error": "Please select a book first"})

    try:
        response = agent.invoke(user_message)
        logging.info(f"* Response: {response}")

        chat_histories[book_title].append({"type": "user", "content": user_message})
        chat_histories[book_title].append({"type": "assistant", "content": response})

        return jsonify({"response": response})
    except Exception as e:
        logging.error(f"* Chat error: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8080)
