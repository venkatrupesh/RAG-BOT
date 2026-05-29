# 🚀 Install Voice Mode - Quick Guide

## Error: ModuleNotFoundError: No module named 'gtts'

This means voice libraries are not installed yet.

---

## ✅ Solution (Choose One):

### Option 1: Automatic Installation (Easiest)

**Double-click this file:**
```
install_voice.bat
```

It will install everything automatically.

### Option 2: Manual Installation

**Open terminal and run:**
```bash
pip install gTTS SpeechRecognition pyaudio audio-recorder-streamlit
```

### Option 3: Install All Requirements

```bash
pip install -r requirements.txt
```

---

## 🎯 After Installation:

1. **Restart the app**:
   ```bash
   streamlit run ui\app.py
   ```

2. **Voice mode will appear** in the sidebar

3. **Select "Voice Interview"** and start!

---

## ⚠️ PyAudio Installation Issues?

If PyAudio fails to install:

```bash
# Install pipwin first
pip install pipwin

# Then install PyAudio
pipwin install pyaudio
```

---

## 💡 App Works Without Voice Mode

The app now works even without voice libraries:
- ✅ **Text Interview** - Available
- ✅ **MCQ Test** - Available
- ⚠️ **Voice Interview** - Requires installation

You can use Text and MCQ modes now, and install voice libraries later!

---

## 🚀 Quick Commands:

```bash
# Install voice libraries
pip install gTTS SpeechRecognition pyaudio audio-recorder-streamlit

# Restart app
streamlit run ui\app.py
```

---

**Install the libraries and voice mode will work!** 🎤
