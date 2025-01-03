from langchain.schema import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

from utils import get_openai_llm, get_openai_embedding_model

import os
import logging

load_dotenv()


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logging.info('** OpenAI API key loaded: ' + str(os.getenv("OPENAI_API_KEY")[:5])+ '...' + str(os.getenv("OPENAI_API_KEY")[-5:]))

openai_llm = get_openai_llm(run_test_question=False)
embeddings = get_openai_embedding_model()




def create_assistant_chain(path: str):

    # Создаём простой шаблон
    template = """
    Answer the question based only on the following context and point out pages. 
    If there is not information in context, answer 'I don't know'.


    {context}

    Question: {question}
    """

    logging.info(f'* Database path: {path}')
    if not os.path.exists(path):
        logging.error(f'* Database not found: {path}')
        return None

    # Создаём промпт из шаблона
    prompt = ChatPromptTemplate.from_template(template)

    db = FAISS.load_local(path, embeddings=embeddings, allow_dangerous_deserialization=True)
    retriever = db.as_retriever(
        search_type="similarity",
    )


    # Объявляем функцию, которая будет собирать строку из полученных документов
    def format_docs(docs):
        context = "\n\n".join([d.page_content for d in docs])
        if 'page' in docs[0].metadata:
            pages = ','.join(sorted(str(d.metadata['page']) for d in docs))
            result = f"{context}\n\nPages: {pages}"
        else:
            result = context
        return result


    # Создаём цепочку
    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | openai_llm
        | StrOutputParser()
    )

    return chain



