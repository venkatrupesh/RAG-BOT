# Voice Interview Component - Auto Submit with Voice Feedback

import streamlit as st
import streamlit.components.v1 as components

def voice_interview_component(bot_text: str, key: str = "voice"):
    """Voice component with auto-submit"""
    
    clean_text = bot_text.replace("*", "").replace("#", "").replace("✅", "Correct").replace("❌", "Incorrect").replace("⚠️", "")
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {{
            font-family: 'Inter', sans-serif;
            padding: 20px;
            background: #f9fafb;
        }}
        .voice-container {{
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            padding: 24px;
            max-width: 600px;
            margin: 0 auto;
        }}
        .status {{
            text-align: center;
            font-size: 0.9rem;
            color: #6b7280;
            margin-bottom: 20px;
            min-height: 24px;
        }}
        .status.speaking {{ color: #3b82f6; font-weight: 600; }}
        .status.listening {{ color: #10b981; font-weight: 600; }}
        .mic-button {{
            width: 80px;
            height: 80px;
            border-radius: 50%;
            border: 3px solid #e5e7eb;
            background: white;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 20px;
            transition: all 0.3s;
        }}
        .mic-button:hover {{ border-color: #3b82f6; transform: scale(1.05); }}
        .mic-button.listening {{
            border-color: #10b981;
            background: #ecfdf5;
            animation: pulse 1.5s infinite;
        }}
        @keyframes pulse {{
            0%, 100% {{ box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); }}
            50% {{ box-shadow: 0 0 0 15px rgba(16, 185, 129, 0); }}
        }}
        .transcript {{
            background: #f9fafb;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 16px;
            min-height: 60px;
            text-align: center;
            color: #374151;
            margin-bottom: 16px;
        }}
        .hint {{
            text-align: center;
            font-size: 0.85rem;
            color: #9ca3af;
        }}
    </style>
    </head>
    <body>
        <div class="voice-container">
            <div class="status" id="status">Ready to speak</div>
            
            <button class="mic-button" id="micBtn" onclick="toggleMic()">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none">
                    <rect x="9" y="2" width="6" height="12" rx="3" fill="#374151"/>
                    <path d="M5 11a7 7 0 0 0 14 0" stroke="#374151" stroke-width="2" stroke-linecap="round"/>
                    <line x1="12" y1="18" x2="12" y2="22" stroke="#374151" stroke-width="2" stroke-linecap="round"/>
                    <line x1="8" y1="22" x2="16" y2="22" stroke="#374151" stroke-width="2" stroke-linecap="round"/>
                </svg>
            </button>
            
            <div class="transcript" id="transcript">Your answer will appear here...</div>
            <div class="hint" id="hint">Click the microphone to start speaking</div>
        </div>

        <script>
            const BOT_TEXT = `{clean_text}`;
            let recognition = null;
            let isListening = false;
            let finalTranscript = "";
            let hasSpoken = false;

            const micBtn = document.getElementById("micBtn");
            const statusEl = document.getElementById("status");
            const transcriptEl = document.getElementById("transcript");
            const hintEl = document.getElementById("hint");

            function speak(text) {{
                if (!text || !window.speechSynthesis || hasSpoken) return;
                
                window.speechSynthesis.cancel();
                
                setTimeout(() => {{
                    const utterance = new SpeechSynthesisUtterance(text);
                    utterance.rate = 0.9;
                    utterance.pitch = 1.0;
                    utterance.volume = 1.0;
                    utterance.lang = 'en-US';

                    const voices = window.speechSynthesis.getVoices();
                    const englishVoice = voices.find(v => v.lang.startsWith('en')) || voices[0];
                    if (englishVoice) utterance.voice = englishVoice;

                    utterance.onstart = () => {{
                        statusEl.textContent = "🤖 AI is speaking...";
                        statusEl.className = "status speaking";
                        micBtn.disabled = true;
                        hintEl.textContent = "Please wait...";
                    }};

                    utterance.onend = () => {{
                        statusEl.textContent = "Your turn - click mic to answer";
                        statusEl.className = "status";
                        micBtn.disabled = false;
                        hintEl.textContent = "Click the microphone to start speaking";
                        hasSpoken = true;
                    }};

                    utterance.onerror = () => {{
                        statusEl.textContent = "Ready to speak";
                        statusEl.className = "status";
                        micBtn.disabled = false;
                        hasSpoken = true;
                    }};

                    window.speechSynthesis.speak(utterance);
                }}, 100);
            }}

            function initRecognition() {{
                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                if (!SpeechRecognition) {{
                    statusEl.textContent = "Speech recognition not supported";
                    return null;
                }}

                const rec = new SpeechRecognition();
                rec.continuous = true;
                rec.interimResults = true;
                rec.lang = 'en-US';

                rec.onstart = () => {{
                    isListening = true;
                    micBtn.classList.add("listening");
                    statusEl.textContent = "🎤 Listening...";
                    statusEl.className = "status listening";
                    hintEl.textContent = "Speak now, click mic when done";
                    transcriptEl.textContent = "...";
                }};

                rec.onresult = (event) => {{
                    let interim = "";
                    for (let i = 0; i < event.results.length; i++) {{
                        const transcript = event.results[i][0].transcript;
                        if (event.results[i].isFinal) {{
                            finalTranscript += transcript + " ";
                        }} else {{
                            interim += transcript;
                        }}
                    }}
                    transcriptEl.textContent = (finalTranscript + interim).trim();
                }};

                rec.onerror = () => {{
                    stopListening();
                }};

                rec.onend = () => {{
                    if (isListening) {{
                        try {{ rec.start(); }} catch(e) {{}}
                    }}
                }};

                return rec;
            }}

            function toggleMic() {{
                if (isListening) {{
                    stopListening();
                }} else {{
                    startListening();
                }}
            }}

            function startListening() {{
                finalTranscript = "";
                transcriptEl.textContent = "...";
                recognition = initRecognition();
                if (recognition) {{
                    try {{ recognition.start(); }} catch(e) {{}}
                }}
            }}

            function stopListening() {{
                isListening = false;
                if (recognition) {{
                    recognition.onend = null;
                    try {{ recognition.stop(); }} catch(e) {{}}
                }}
                micBtn.classList.remove("listening");
                
                const answer = finalTranscript.trim();
                if (answer) {{
                    transcriptEl.textContent = answer;
                    statusEl.textContent = "✓ Submitting...";
                    statusEl.className = "status";
                    hintEl.textContent = "Processing your answer...";
                    
                    // Send to Streamlit
                    window.parent.postMessage({{
                        type: 'streamlit:setComponentValue',
                        value: answer
                    }}, '*');
                }} else {{
                    transcriptEl.textContent = "Nothing heard. Try again.";
                    statusEl.textContent = "Ready to speak";
                    statusEl.className = "status";
                    hintEl.textContent = "Click the microphone to start speaking";
                }}
            }}

            // Auto-speak bot response once
            window.addEventListener('load', () => {{
                setTimeout(() => {{
                    if (BOT_TEXT && !hasSpoken) {{
                        const voices = window.speechSynthesis.getVoices();
                        if (voices.length > 0) speak(BOT_TEXT);
                    }}
                }}, 500);
            }});

            if (window.speechSynthesis.onvoiceschanged !== undefined) {{
                window.speechSynthesis.onvoiceschanged = () => {{
                    if (BOT_TEXT && !hasSpoken) speak(BOT_TEXT);
                }};
            }}
        </script>
    </body>
    </html>
    """
    
    return components.html(html, height=350, scrolling=False)


def render_voice_interview(topic, difficulty, get_system_prompt_fn, ask_groq_fn):
    """Render voice interview mode"""
    
    # Show conversation history
    if st.session_state.history:
        st.markdown("### Conversation")
        for msg in st.session_state.history[-4:]:
            with st.chat_message(msg["role"], avatar="🤖" if msg["role"] == "assistant" else "👤"):
                st.markdown(msg["content"])
        st.markdown("---")
    
    # Get last bot message for voice playback
    last_bot_text = ""
    if st.session_state.history:
        last_msg = st.session_state.history[-1]
        if last_msg["role"] == "assistant":
            last_bot_text = last_msg["content"]
    
    # Render voice component
    voice_answer = voice_interview_component(last_bot_text, key=f"voice_{st.session_state.question_count}")
    
    # Process voice answer when received
    if voice_answer:
        answer_str = str(voice_answer).strip()
        
        if answer_str and answer_str.lower() not in ["quit", "exit", "bye"]:
            # Add user answer to history
            st.session_state.history.append({"role": "user", "content": answer_str})
            
            # Get AI response
            with st.spinner("Evaluating..."):
                system, _ = get_system_prompt_fn(answer_str, topic, difficulty, "Voice")
                response = ask_groq_fn(system, st.session_state.history)
                st.session_state.history.append({"role": "assistant", "content": response})
                st.session_state.question_count += 1
            
            st.rerun()
        elif answer_str.lower() in ["quit", "exit", "bye"]:
            st.success("Voice interview ended!")
