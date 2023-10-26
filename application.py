import streamlit as st
from audio_recorder_streamlit import audio_recorder
import openai
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("API_KEY_OPENAI")

audio_bytes = audio_recorder(text="Clique para gravar")
if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")

    with open("audios/temp.wav", "wb") as temp_file:
        temp_file.write(audio_bytes)

    audio_file = open("audios/temp.wav", "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)

    st.text_area("Speech-To-Text", transcript.text, disabled=True)
