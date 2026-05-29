# utils/voice_handler.py

import streamlit as st
from gtts import gTTS
import speech_recognition as sr
import tempfile
import os
from io import BytesIO

def text_to_speech(text: str) -> bytes:
    """
    Convert text to speech using gTTS
    Returns audio bytes
    """
    try:
        # Create gTTS object
        tts = gTTS(text=text, lang='en', slow=False)
        
        # Save to bytes
        audio_bytes = BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        
        return audio_bytes.read()
    except Exception as e:
        st.error(f"Text-to-speech error: {e}")
        return None

def speech_to_text(audio_file) -> str:
    """
    Convert speech to text using speech_recognition
    """
    try:
        recognizer = sr.Recognizer()
        
        # Read audio file
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            
        # Convert to text
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return f"Speech recognition error: {e}"
    except Exception as e:
        return f"Error: {e}"

def record_audio_from_mic() -> str:
    """
    Record audio from microphone and convert to text
    """
    try:
        recognizer = sr.Recognizer()
        
        with sr.Microphone() as source:
            st.info("🎤 Listening... Speak now!")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=30)
            
        st.success("✅ Audio captured! Processing...")
        
        # Convert to text
        text = recognizer.recognize_google(audio)
        return text
    except sr.WaitTimeoutError:
        return "No speech detected. Please try again."
    except sr.UnknownValueError:
        return "Could not understand audio. Please speak clearly."
    except sr.RequestError as e:
        return f"Speech recognition error: {e}"
    except Exception as e:
        return f"Error: {e}"
