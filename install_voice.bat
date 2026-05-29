@echo off
echo ============================================
echo Installing Voice Interview Dependencies
echo ============================================
echo.

echo Step 1: Installing gTTS (Text-to-Speech)...
pip install gTTS
echo.

echo Step 2: Installing SpeechRecognition...
pip install SpeechRecognition
echo.

echo Step 3: Installing audio-recorder-streamlit...
pip install audio-recorder-streamlit
echo.

echo Step 4: Installing PyAudio...
echo Note: PyAudio might fail. If it does, run: pipwin install pyaudio
pip install pyaudio
if errorlevel 1 (
    echo.
    echo PyAudio installation failed!
    echo Installing pipwin...
    pip install pipwin
    echo.
    echo Installing PyAudio via pipwin...
    pipwin install pyaudio
)

echo.
echo ============================================
echo Installation Complete!
echo ============================================
echo.
echo Next steps:
echo 1. Run: streamlit run ui\app.py
echo 2. Sign in
echo 3. Select "Voice Interview" mode
echo 4. Start speaking!
echo.
pause
