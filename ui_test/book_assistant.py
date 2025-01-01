import streamlit as st
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu
import base64
import time

# Set page config
st.set_page_config(page_title="Book Assistant", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background-color: #f3f4f6;
    }
    .sidebar .sidebar-content {
        background-color: white;
    }
    .stButton>button {
        background-color: #3b82f6;
        color: white;
        border-radius: 0.375rem;
    }
    .stButton>button:hover {
        background-color: #2563eb;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: flex-start;
    }
    .chat-message.user {
        background-color: #3b82f6;
        color: white;
        margin-left: auto;
    }
    .chat-message.assistant {
        background-color: #e5e7eb;
        margin-right: auto;
    }
    .chat-message .avatar {
        width: 20px;
        height: 20px;
        border-radius: 50%;
        margin-right: 10px;
    }
    .book-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.5rem;
        border-radius: 0.375rem;
        margin-bottom: 0.5rem;
        background-color: #f3f4f6;
    }
    .book-item:hover {
        background-color: #e5e7eb;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'books' not in st.session_state:
    st.session_state.books = [
        {"id": "1", "title": "To Kill a Mockingbird"},
        {"id": "2", "title": "1984"},
        {"id": "3", "title": "Pride and Prejudice"},
    ]

if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'current_book' not in st.session_state:
    st.session_state.current_book = None

# Sidebar
with st.sidebar:
    st.title("Book Assistant")
    
    # Upload book button
    uploaded_file = st.file_uploader("Upload a book", type=["pdf", "epub", "txt"])
    if uploaded_file is not None:
        book_title = st.text_input("Book Title", value=uploaded_file.name.split('.')[0])
        if st.button("Add Book"):
            new_id = str(len(st.session_state.books) + 1)
            st.session_state.books.append({"id": new_id, "title": book_title})
            st.success(f"Book '{book_title}' added successfully!")

    st.subheader("Your Books")
    for book in st.session_state.books:
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button(book['title'], key=f"book_{book['id']}"):
                st.session_state.current_book = book
                st.session_state.messages = []  # Clear chat when switching books
        with col2:
            if st.button("🗑️", key=f"delete_{book['id']}"):
                st.session_state.books.remove(book)
                if st.session_state.current_book == book:
                    st.session_state.current_book = None
                st.rerun()

# Main content
if st.session_state.current_book:
    st.title(f"Chat about: {st.session_state.current_book['title']}")

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input
    user_input = st.chat_input("Ask a question about the book...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        # Simulate assistant response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = f"This is a response about the book \"{st.session_state.current_book['title']}\""
            for chunk in full_response.split():
                message_placeholder.write(f"{chunk} ", unsafe_allow_html=True)
                time.sleep(0.05)
            message_placeholder.write(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

else:
    st.title("Welcome to Book Assistant")
    st.write("Select a book from the sidebar to start chatting, or upload a new book.")

# Add some spacing at the bottom
st.markdown("<br><br>", unsafe_allow_html=True)