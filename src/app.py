import streamlit as st
import agent
import logging
import os

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
assistant = agent.create_assistant_chain()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Список для хранения истории переписки
if "history" not in st.session_state:
    st.session_state.history = []

st.title("Book Assistant")
st.caption("I can read your book and answer your questions.")


def generate_response(input_text):
    response = assistant.invoke(input_text)
    st.session_state.history.append((input_text, response, ""))

# Форм для ввода текста пользователем
with st.form('my_form'):
    text = st.text_area('Enter your question:', 'Ask me something...')
    submitted = st.form_submit_button('Ask me')
    if submitted:
        generate_response(text)

# Отображаем историю переписки в обратном порядке с рамками и фоном
for i, (question, answer, pages) in enumerate(reversed(st.session_state.history)):
    with st.container():
        # Вопрос
        st.markdown(f"### **Question {i + 1}:**")
        st.markdown(f"<div style='background-color:#f0f0f0; padding: 10px; border: 2px solid #dcdcdc; border-radius: 5px;'>{question}</div>", unsafe_allow_html=True)
        
        # Ответ
        st.markdown("### **Answer:**")
        st.markdown(f"<div style='background-color:#e0f7fa; padding: 10px; border: 2px solid #b2ebf2; border-radius: 5px;'>{answer}</div>", unsafe_allow_html=True)