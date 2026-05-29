# 🎤 Voice Interview Mode - Complete Setup Guide

## What is Voice Interview Mode?

A **real voice interview** where:
- ✅ **AI speaks to you** (text-to-speech)
- ✅ **You speak your answers** (speech-to-text)
- ✅ **AI responds with voice** (audio feedback)
- ✅ **Greets you by name**
- ✅ **Natural conversation flow**

---

## 🚀 Setup Instructions

### Step 1: Install Voice Libraries (2 minutes)

```bash
pip install gTTS SpeechRecognition pyaudio audio-recorder-streamlit
```

**Or install all requirements:**
```bash
pip install -r requirements.txt
```

### Step 2: Install PyAudio (Windows)

PyAudio might need special installation on Windows:

**Option A: Using pip**
```bash
pip install pipwin
pipwin install pyaudio
```

**Option B: Download wheel file**
1. Go to: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
2. Download the `.whl` file for Python 3.12 (64-bit)
3. Install: `pip install PyAudio‑0.2.13‑cp312‑cp312‑win_amd64.whl`

### Step 3: Test Microphone Access

```python
# Test if microphone works
python -c "import speech_recognition as sr; print('Microphone OK!')"
```

### Step 4: Run the App

```bash
streamlit run ui\app.py
```

---

## 🎤 How Voice Interview Works

### Flow:

```
1. Select "Voice Interview" mode
   ↓
2. AI greets you: "Hello [Your Name]!"
   (AI speaks with voice)
   ↓
3. AI asks first question
   (AI speaks the question)
   ↓
4. You speak your answer
   (Microphone records your voice)
   ↓
5. AI processes your answer
   (Speech converted to text)
   ↓
6. AI gives feedback
   (AI speaks the feedback)
   ↓
7. Repeat for 5 questions
   ↓
8. Final score announced
   (AI speaks your score)
```

---

## 🎯 Features

### AI Voice Output:
- ✅ Greets you by username
- ✅ Speaks all questions
- ✅ Speaks all feedback
- ✅ Announces your score
- ✅ Natural, clear voice

### Voice Input Options:
1. **Audio Recorder** - Click to record, click to stop
2. **Microphone** - One-click recording
3. **Text Fallback** - Type if voice doesn't work

### Smart Features:
- ✅ Automatic speech-to-text
- ✅ Automatic text-to-speech
- ✅ Audio playback in browser
- ✅ Visual feedback
- ✅ Error handling

---

## 📱 Using Voice Interview

### Step 1: Start Interview
1. Sign in to your account
2. Select **"Voice Interview"** in sidebar
3. Choose topic and difficulty
4. Interview starts automatically

### Step 2: Listen to AI
- AI greets you with voice
- AI asks question with voice
- Listen carefully

### Step 3: Respond with Voice

**Option 1: Audio Recorder**
1. Click "Click to record" button
2. Speak your answer
3. Click to stop recording
4. Click "Submit Audio"

**Option 2: Microphone**
1. Click "Start Recording"
2. Speak your answer (up to 30 seconds)
3. Answer automatically submitted

**Option 3: Text (Fallback)**
1. Type your answer
2. Click "Submit Text"

### Step 4: Get Feedback
- AI speaks the feedback
- Feedback also shown as text
- Next question asked automatically

### Step 5: Complete Interview
- Answer 5 questions
- Get final score
- AI announces score with voice

---

## 🎙️ Voice Input Tips

### For Best Results:
1. **Speak clearly** - Enunciate words
2. **Normal pace** - Not too fast or slow
3. **Quiet environment** - Minimize background noise
4. **Good microphone** - Use quality mic if possible
5. **Close to mic** - Speak 6-12 inches away
6. **Complete sentences** - Finish your thought

### What to Say:
- **Be concise** - 1-2 sentences per answer
- **Stay on topic** - Answer the question asked
- **Use keywords** - Technical terms are recognized
- **Natural language** - Speak conversationally

### If Voice Fails:
- Use the text fallback option
- Check microphone permissions
- Try different browser (Chrome works best)
- Restart the app

---

## 🔧 Troubleshooting

### Issue 1: "Microphone not found"
**Fix:**
- Check microphone is plugged in
- Allow browser microphone access
- Restart browser
- Try different browser (Chrome recommended)

### Issue 2: "Could not understand audio"
**Fix:**
- Speak more clearly
- Reduce background noise
- Speak closer to microphone
- Try again with slower speech

### Issue 3: "PyAudio not installed"
**Fix:**
```bash
pip install pipwin
pipwin install pyaudio
```

### Issue 4: "No audio output"
**Fix:**
- Check system volume
- Check browser audio permissions
- Try different browser
- Restart the app

### Issue 5: "Speech recognition error"
**Fix:**
- Check internet connection (Google Speech API needs internet)
- Wait a moment and try again
- Use text fallback option

---

## 🌐 Browser Compatibility

### Best Support:
- ✅ **Google Chrome** (Recommended)
- ✅ **Microsoft Edge**
- ✅ **Firefox**

### Limited Support:
- ⚠️ Safari (may have audio issues)
- ⚠️ Opera (may have mic issues)

**Recommendation**: Use Google Chrome for best experience

---

## 🎨 Voice Interview UI

### What You'll See:

```
┌─────────────────────────────────────────┐
│ 🎤 Voice Interview Mode                 │
│ AI will speak to you and listen to      │
│ your voice responses                     │
└─────────────────────────────────────────┘

🤖 AI: Hello Rushi! Welcome to your 
       Intermediate level Python voice 
       interview...

🤖 AI: What is a list comprehension?

┌─────────────────────────────────────────┐
│ 🎤 Your Response                        │
│                                         │
│ Option 1: Record Audio                  │
│ [🎤 Click to record]                    │
│                                         │
│ Option 2: Use Microphone                │
│ [🎤 Start Recording]                    │
│                                         │
│ Option 3: Type Your Answer              │
│ [Text input field]                      │
└─────────────────────────────────────────┘
```

---

## 📊 Voice vs Text vs MCQ

| Feature | Voice | Text | MCQ |
|---------|-------|------|-----|
| **Input** | Voice | Text | Click |
| **Output** | Voice | Text | Text |
| **Questions** | 5 | 5 | 10 |
| **Feedback** | Voice | Text | Text |
| **Best For** | Interview prep | Learning | Testing |
| **Requires** | Microphone | Keyboard | Mouse |

---

## 🎯 When to Use Voice Mode

### Use Voice Interview For:
- ✅ Phone interview practice
- ✅ Verbal communication skills
- ✅ Real interview simulation
- ✅ Speaking confidence
- ✅ Quick thinking practice

### Use Text Interview For:
- ✅ Detailed explanations
- ✅ Complex answers
- ✅ Learning mode
- ✅ No microphone available

### Use MCQ Test For:
- ✅ Quick knowledge check
- ✅ Multiple choice practice
- ✅ Timed tests
- ✅ Self-assessment

---

## 🔒 Privacy & Security

### Voice Data:
- ✅ Processed in real-time
- ✅ Not stored permanently
- ✅ Uses Google Speech API
- ✅ Temporary audio files deleted

### Microphone Access:
- ✅ Only when you click record
- ✅ Browser asks permission
- ✅ You control when to record
- ✅ Can revoke anytime

---

## 📝 Example Voice Interview

```
🤖 AI (speaking): "Hello Rushi! Welcome to your 
                  Intermediate level Python voice 
                  interview. Let's begin with the 
                  first question."

🤖 AI (speaking): "What is a decorator in Python?"

👤 You (speaking): "A decorator is a function that 
                    modifies another function's behavior"

🤖 AI (speaking): "Good! That's correct. Decorators 
                  wrap functions to extend their 
                  behavior. Next question..."

[... 4 more questions ...]

🤖 AI (speaking): "Great job! Your final score is 
                  8 out of 10. Well done!"
```

---

## ✅ Installation Checklist

- [ ] Installed gTTS: `pip install gTTS`
- [ ] Installed SpeechRecognition: `pip install SpeechRecognition`
- [ ] Installed PyAudio: `pip install pyaudio` or `pipwin install pyaudio`
- [ ] Installed audio-recorder: `pip install audio-recorder-streamlit`
- [ ] Tested microphone access
- [ ] Allowed browser microphone permissions
- [ ] Using Chrome or Edge browser
- [ ] Internet connection active (for speech recognition)

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Install PyAudio (Windows)
pip install pipwin
pipwin install pyaudio

# 3. Run the app
streamlit run ui\app.py

# 4. Sign in

# 5. Select "Voice Interview"

# 6. Start speaking!
```

---

**Voice Interview Mode is now ready! Install the dependencies and start practicing with voice.** 🎤🎉
