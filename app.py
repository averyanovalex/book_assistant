import streamlit as st
from audiorecorder import audiorecorder


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

audio = audiorecorder("", "")

if len(audio) > 0:
    # To play audio in frontend:
    st.audio(audio.export().read())  

    # To save audio to a file, use pydub export method:
    audio.export("audio.wav", format="wav")

    # To get audio properties, use pydub AudioSegment properties:
    st.write(f"Frame rate: {audio.frame_rate}, Frame width: {audio.frame_width}, Duration: {audio.duration_seconds} seconds")