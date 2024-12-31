import streamlit as st

def main():
    # Sidebar
    st.sidebar.title("Меню")
    menu_options = ["Загрузить книгу", "Список книг", "Чат"]
    choice = st.sidebar.radio("Выберите действие:", menu_options)

    # UploadBook
    if choice == "Загрузить книгу":
        st.title("Загрузка книги")
        uploaded_file = st.file_uploader("Выберите файл книги", type=["txt", "pdf"])
        if uploaded_file:
            st.success("Книга успешно загружена!")

    # BookList
    elif choice == "Список книг":
        st.title("Список книг")
        books = ["Книга 1", "Книга 2", "Книга 3"]  # Заглушка для демонстрации
        for book in books:
            st.write(f"- {book}")

    # ChatComponent
    elif choice == "Чат":
        st.title("Чат")
        st.write("Введите сообщение ниже:")
        user_message = st.text_input("Сообщение")
        if user_message:
            st.write(f"Вы: {user_message}")
            st.write("Бот: Это тестовый ответ.")

if __name__ == "__main__":
    main()