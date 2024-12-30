import streamlit as st




# Пример структуры книги (реально, можно будет загрузить текст книги с номерами страниц)
book_content = {
    1: "This is the first page. It talks about the introduction of the book.",
    2: "This is the second page. It discusses the main character.",
    3: "This is the third page. It talks about the setting of the story.",
    # Добавить остальные страницы по аналогии...
}

# Список для хранения истории переписки
if "history" not in st.session_state:
    st.session_state.history = []

st.title("Book Assistant")
st.caption("I can read your book and answer your questions.")

# Функция поиска по тексту
def generate_response(input_text):
    response = "rrerer"
    pages_found = [2]
    
    # Поиск текста в содержимом книги
    for page_num, page_text in book_content.items():
        if input_text.lower() in page_text.lower():
            response = f"{page_text}"
            pages_found.append(page_num)
    
    # Сохраняем текущий вопрос и ответ в историю
    if pages_found:
        answer = response
        pages = f"Page(s): {', '.join(map(str, pages_found))}"
    else:
        answer = "Sorry, I couldn't find an answer to your question."
        pages = ""
    
    # Добавляем вопрос и ответ в историю
    st.session_state.history.append((input_text, answer, pages))

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
        
        # Номера страниц
        if pages:
            st.markdown("### **Pages Mentioned:**")
            st.markdown(f"<div style='background-color:#fff3e0; padding: 10px; border: 2px solid #ffcc80; border-radius: 5px;'>{pages}</div>", unsafe_allow_html=True)
