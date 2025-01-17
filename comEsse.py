import streamlit as st
import os
from transformers import pipeline
from gtts import gTTS
import tempfile
import speech_recognition as sr
from pydub import AudioSegment

# Load AI model for summarization
@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="facebook/bart-large-cnn")

def text_summarization(summarizer, article):
    summary = summarizer(article, max_length=130, min_length=50, do_sample=False)
    return summary[0]['summary_text']

def text_to_speech(text):
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            temp_path = tmp_file.name
            tts.save(temp_path)
        return temp_path
    except Exception as e:
        st.error(f"Error: {e}")
        return None

def speech_to_text(audio_file):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)
        transcription = recognizer.recognize_google(audio)
        return transcription
    except sr.UnknownValueError:
        return "Tidak dapat memahami audio. Pastikan suara jelas dan minim gangguan."
    except sr.RequestError as e:
        return f"Kesalahan pada layanan Speech Recognition: {e}"

def convert_audio_to_wav(audio_file, input_format):
    try:
        wav_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
        audio = AudioSegment.from_file(audio_file, format=input_format)
        audio = audio.set_frame_rate(16000).set_channels(1)
        audio.export(wav_file, format="wav")
        return wav_file
    except Exception as e:
        st.error(f"Gagal mengonversi {input_format} ke WAV: {e}")
        return None

# Streamlit Interface
st.title("ComEsse: Ez Comm for all :)")

menu = ["Text Summarization", "Text Summarization & Text-to-Speech", "Speech-to-Text", "Text-to-Speech"]
choice = st.sidebar.selectbox("Pilih fitur:", menu)

summarizer = load_summarizer()

if choice == "Text Summarization":
    st.header("Text Summarization")
    article = st.text_area("Masukkan artikel untuk diringkas:")
    if st.button("Ringkas Teks"):
        if article.strip():
            summary = text_summarization(summarizer, article)
            st.subheader("Ringkasan:")
            st.write(summary)
        else:
            st.warning("Masukkan artikel yang valid.")

elif choice == "Text Summarization & Text-to-Speech":
    st.header("Text Summarization & Text-to-Speech")
    article = st.text_area("Masukkan artikel untuk diringkas:")
    if st.button("Ringkas & Baca Teks"):
        if article.strip():
            summary = text_summarization(summarizer, article)
            st.subheader("Ringkasan:")
            st.write(summary)

            audio_file = text_to_speech(summary)
            if audio_file:
                st.audio(audio_file, format="audio/mp3")
        else:
            st.warning("Masukkan artikel yang valid.")

elif choice == "Speech-to-Text":
    st.header("Speech-to-Text")
    audio_file = st.file_uploader("Unggah file audio (MP3/WAV/M4A):", type=["mp3", "wav", "m4a"])
    if st.button("Transkripsi Audio"):
        if audio_file:
            input_format = "mp3" if audio_file.name.endswith(".mp3") else "m4a" if audio_file.name.endswith(".m4a") else "wav"
            if input_format in ["mp3", "m4a"]:
                wav_file = convert_audio_to_wav(audio_file, input_format)
                transcription = speech_to_text(wav_file)
            else:
                transcription = speech_to_text(audio_file.name)
            
            st.subheader("Hasil Transkripsi:")
            st.write(transcription)
        else:
            st.warning("Unggah file audio terlebih dahulu.")

elif choice == "Text-to-Speech":
    st.header("Text-to-Speech")
    text = st.text_area("Masukkan teks untuk diubah menjadi suara:")
    if st.button("Ubah ke Suara"):
        if text.strip():
            audio_file = text_to_speech(text)
            if audio_file:
                st.audio(audio_file, format="audio/mp3")
        else:
            st.warning("Masukkan teks yang valid.")
