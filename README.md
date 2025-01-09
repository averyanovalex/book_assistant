# Book Assistant (prototype)

## Project Idea

An assistant that can answer questions about books. It can work with fiction books, technical books, etc. The assistant can serve as an interactive summary or help find needed information in the book.

__Target Audience__ - students and anyone who works with books.

__Main Project Goal__ - to create a prototype assistant for any knowledge base. In this case, the knowledge base is a book. But technically it can be replaced with any wiki, confluence, etc.

## How it Works (video)

[![Book assistant demo](https://img.youtube.com/vi/9ZdERW4Ermo/0.jpg)](https://www.youtube.com/watch?v=9ZdERW4Ermo)

## Key Features

1. New books can be added and are automatically vectorized into RAG
2. Books can be in different languages, and you can communicate with the assistant in different languages
3. The assistant struggles with questions that don't have direct answers in the text (area for improvement)
4. Supports uploading books in txt and pdf formats

## Installation and Setup

1. Clone the repository:
```bash
git clone https://github.com/averyanovalex/book_assistant.git
cd book-assistant
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create .env file with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here

# Optional, if your not use, remove in code
PROXY_URL=your_proxy_url_here  
```

5. Initialize sample books (optional):
```bash
make init_books
```

6. Run the application:
```bash
make run
```

The application will be available at http://localhost:8080

## Required Libraries

```
langchain==0.3.13
langchain_openai==0.2.14
langchain_community==0.3.13
faiss-cpu==1.9.0.post1
Flask==2.3.2
Werkzeug==2.3.6
pypdf==5.1.0
transliterate==1.10.2
```

## Technical Details

1. Uses `gpt-4o-mini` model via proxy
2. `FAISS` as vector storage
3. `LangChain` as the main framework
4. `Flask` for UI
5. Prompting with relevant context from RAG
6. Memory in prompting is not used, couldn't configure it properly initially



## Areas for Improvement

1. The assistant struggles with questions that don't have direct answers in the book. For example, "What is this book about?" or "What is the main idea of the book?". Therefore, we need to create a large checklist of book questions, get answers using a "smart model" with large context, and put the answers in RAG. Alternatively, use prompting techniques with access to `wikipedia` and internet where these answers likely exist.

2. Add memory when working with the assistant.

3. Add sessions so each user works with their own books and chat history.

4. Add smarter book splitting. Currently using simple `TextSplitter`.

5. Expand supported book formats.

6. Set up https for the service.

