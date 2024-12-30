import streamlit as st


st.title("Book assistant")
st.caption("I can read your book and ask you questions.")

def generate_response(input_text):
    st.info(input_text)
    st.info('Это просто ответ 3...')

with st.form('my_form'):
    text = st.text_area('Enter text:', 'Ask me something...')
    submitted = st.form_submit_button('Submit')
    if submitted:
        generate_response(text)
