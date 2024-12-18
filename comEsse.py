import os
from transformers import pipeline
from gtts import gTTS
from playsound import playsound
from pydub import AudioSegment
import pyaudio
import wave
import speech_recognition as sr
import tempfile
from tkinter import Tk, filedialog

def text_summarization():
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    print("Masukkan artikel untuk diringkas (tekan Enter pada baris kosong untuk menyelesaikan input):")
    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)

    article = " ".join(lines)
    summary = summarizer(article, max_length=130, min_length=50, do_sample=False)
    print("\nRingkasan:")
    print(summary[0]['summary_text'])

def text_to_speech(text):
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            temp_path = tmp_file.name
            tts.save(temp_path)
        playsound(temp_path)
        os.remove(temp_path)
    except Exception as e:
        print(f"Error: {e}")

def text_summarization_with_speech():
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    print("Masukkan artikel untuk diringkas (tekan Enter pada baris kosong untuk menyelesaikan input):")
    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)

    article = " ".join(lines)
    summary = summarizer(article, max_length=130, min_length=50, do_sample=False)
    summary_text = summary[0]['summary_text']
    print("\nRingkasan:")
    print(summary_text)
    text_to_speech(summary_text)

def speech_to_text():
    recognizer = sr.Recognizer()

    def record_audio():
        audio_format = pyaudio.paInt16
        channels = 1
        rate = 16000
        chunk = 1024
        output_file = "mic_recording.wav"

        p = pyaudio.PyAudio()
        stream = p.open(format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)

        print("Recording... Press Enter to stop.")
        frames = []
        try:
            while True:
                data = stream.read(chunk)
                frames.append(data)
        except KeyboardInterrupt:
            print("Recording stopped.")
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()

        with wave.open(output_file, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(p.get_sample_size(audio_format))
            wf.setframerate(rate)
            wf.writeframes(b''.join(frames))

        return output_file

    def transcribe(file_path):
        with sr.AudioFile(file_path) as source:
            audio = recognizer.record(source)
        return recognizer.recognize_google(audio)

    print("Pilih opsi input:")
    print("1. Rekam audio dengan mikrofon")
    print("2. Pilih file audio")
    choice = input("Masukkan pilihan (1/2): ")

    if choice == "1":
        audio_file = record_audio()
    elif choice == "2":
        root = Tk()
        # root.withdraw()
        audio_file = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3")])
    else:
        print("Pilihan tidak valid.")
        return

    try:
        print("Transkripsi:")
        print(transcribe(audio_file))
    except Exception as e:
        print(f"Error: {e}")

def main_menu():
    while True:
        print("\nPilih fitur:")
        print("1. Text Summarization")
        print("2. Text Summarization & Text-to-Speech")
        print("3. Speech-to-Text")
        print("4. Text-to-Speech")
        print("5. Keluar")

        choice = input("Masukkan pilihan Anda (1-5): ")

        if choice == "1":
            text_summarization()
        elif choice == "2":
            text_summarization_with_speech()
        elif choice == "3":
            speech_to_text()
        elif choice == "4":
            print("Masukkan teks untuk diubah menjadi suara:")
            text = input("=> ")
            text_to_speech(text)
        elif choice == "5":
            print("Keluar dari program.")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    main_menu()
