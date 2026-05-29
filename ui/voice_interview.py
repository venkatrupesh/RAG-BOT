# ui/voice_interview.py

import streamlit as st
import streamlit.components.v1 as components

def show_voice_interview(username, topic, difficulty, get_system_prompt_func, ask_groq_func):
    """
    Fully automatic voice interview without page reloads
    """
    
    # Initialize voice state
    if 'voice_history' not in st.session_state:
        st.session_state.voice_history = []
    if 'voice_started' not in st.session_state:
        st.session_state.voice_started = False
    if 'voice_question_count' not in st.session_state:
        st.session_state.voice_question_count = 0
    if 'pending_voice_answer' not in st.session_state:
        st.session_state.pending_voice_answer = None
    
    # Start interview with greeting
    if not st.session_state.voice_started:
        greeting = f"Hi {username}, welcome to your {topic} interview at {difficulty} level. Are you ready to begin?"
        st.session_state.voice_history = [{"role": "assistant", "content": greeting}]
        st.session_state.voice_started = True
    
    # Display conversation history
    st.markdown("### 🎙️ Voice Interview")
    st.markdown(f"**Topic:** {topic} | **Difficulty:** {difficulty}")
    st.markdown("---")
    
    # Render voice component first
    last_bot_message = ""
    if st.session_state.voice_history:
        for msg in reversed(st.session_state.voice_history):
            if msg["role"] == "assistant":
                last_bot_message = msg["content"]
                break
    
    # Clean text for TTS
    clean_text = last_bot_message.replace("*", "").replace("#", "").replace("✅", "Correct").replace("❌", "Incorrect").replace("⚠️", "Partially correct")
    
    # Render voice component
    render_auto_voice_component(clean_text, st.session_state.voice_question_count)
    
    # Voice input and submit button
    st.markdown("**Your Answer:**")
    col1, col2 = st.columns([5, 1])
    with col1:
        voice_input = st.text_input(
            "voice_answer_input", 
            key=f"voice_input_{st.session_state.voice_question_count}", 
            label_visibility="collapsed", 
            placeholder="Your voice answer will appear here..."
        )
    with col2:
        voice_submit = st.button(
            "📤 Send", 
            key=f"voice_submit_{st.session_state.voice_question_count}", 
            use_container_width=True,
            type="primary"
        )
    
    # Process voice answer when button clicked
    if voice_submit and voice_input and voice_input.strip():
        # Add user answer to conversation
        st.session_state.voice_history.append({"role": "user", "content": voice_input})
        
        try:
            if st.session_state.voice_question_count == 0:
                start_msg = f"Start a {difficulty} level {topic} voice interview. Ask the first question. Keep it short and conversational."
                system_prompt, _ = get_system_prompt_func(start_msg, topic, difficulty, "Voice")
            else:
                system_prompt, _ = get_system_prompt_func(voice_input, topic, difficulty, "Voice")
            
            # Build proper message history
            messages = [{"role": m["role"], "content": str(m["content"])} for m in st.session_state.voice_history]
            
            # Get bot response
            response = ask_groq_func(system_prompt, messages)
            st.session_state.voice_history.append({"role": "assistant", "content": response})
            st.session_state.voice_question_count += 1
            
            st.rerun()
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    st.markdown("---")
    
    # Show conversation history
    for msg in st.session_state.voice_history:
        role = msg["role"]
        avatar = "🤖" if role == "assistant" else "👤"
        with st.chat_message(role, avatar=avatar):
            st.markdown(msg["content"])
    
    # Manual fallback
    with st.expander("💬 Type answer manually (if voice fails)"):
        manual_input = st.text_input("Your answer:", key=f"manual_{st.session_state.voice_question_count}")
        if st.button("Submit", key=f"submit_{st.session_state.voice_question_count}"):
            if manual_input:
                st.session_state.voice_history.append({"role": "user", "content": manual_input})
                
                try:
                    if st.session_state.voice_question_count == 0:
                        start_msg = f"Start a {difficulty} level {topic} voice interview. Ask the first question. Keep it short and conversational."
                        system_prompt, _ = get_system_prompt_func(start_msg, topic, difficulty, "Voice")
                    else:
                        system_prompt, _ = get_system_prompt_func(manual_input, topic, difficulty, "Voice")
                    
                    messages = [{"role": m["role"], "content": str(m["content"])} for m in st.session_state.voice_history]
                    
                    response = ask_groq_func(system_prompt, messages)
                    st.session_state.voice_history.append({"role": "assistant", "content": response})
                    st.session_state.voice_question_count += 1
                    
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")


def render_auto_voice_component(text_to_speak, question_num):
    """
    Renders voice component that auto-fills hidden input
    """
    
    safe_text = text_to_speak.replace("\\", "\\\\").replace("`", "\\`").replace("$", "\\$").replace("\n", " ").replace('"', '\\"')
    
    html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
  body {{
    font-family: 'Inter', sans-serif;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    background: #f9fafb;
    margin: 0;
  }}
  
  .voice-container {{
    background: white;
    border-radius: 16px;
    padding: 30px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    max-width: 500px;
    width: 100%;
  }}
  
  .status {{
    text-align: center;
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 20px;
    color: #374151;
  }}
  
  .status.speaking {{ color: #3b82f6; }}
  .status.listening {{ color: #10b981; }}
  .status.processing {{ color: #f59e0b; }}
  
  .mic-button {{
    width: 80px;
    height: 80px;
    border-radius: 50%;
    border: none;
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    color: white;
    font-size: 32px;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    transition: all 0.3s;
    margin: 0 auto;
    display: block;
  }}
  
  .mic-button:hover {{
    transform: scale(1.05);
    box-shadow: 0 6px 16px rgba(59, 130, 246, 0.4);
  }}
  
  .mic-button.listening {{
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    animation: pulse 1.5s infinite;
  }}
  
  @keyframes pulse {{
    0%, 100% {{ box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); }}
    50% {{ box-shadow: 0 0 0 15px rgba(16, 185, 129, 0); }}
  }}
  
  .transcript {{
    margin-top: 20px;
    padding: 15px;
    background: #f3f4f6;
    border-radius: 12px;
    min-height: 60px;
    font-size: 14px;
    color: #1f2937;
    text-align: center;
  }}
  
  .waveform {{
    display: flex;
    justify-content: center;
    gap: 4px;
    height: 40px;
    align-items: center;
    margin: 15px 0;
    opacity: 0;
    transition: opacity 0.3s;
  }}
  
  .waveform.active {{ opacity: 1; }}
  
  .waveform span {{
    width: 4px;
    background: #3b82f6;
    border-radius: 2px;
    animation: wave 1s ease-in-out infinite;
  }}
  
  .waveform span:nth-child(1) {{ height: 10px; animation-delay: 0s; }}
  .waveform span:nth-child(2) {{ height: 20px; animation-delay: 0.1s; }}
  .waveform span:nth-child(3) {{ height: 30px; animation-delay: 0.2s; }}
  .waveform span:nth-child(4) {{ height: 20px; animation-delay: 0.3s; }}
  .waveform span:nth-child(5) {{ height: 10px; animation-delay: 0.4s; }}
  
  @keyframes wave {{
    0%, 100% {{ transform: scaleY(0.5); }}
    50% {{ transform: scaleY(1); }}
  }}
</style>
</head>
<body>

<div class="voice-container">
  <div class="status" id="status">Initializing...</div>
  
  <div class="waveform" id="waveform">
    <span></span><span></span><span></span><span></span><span></span>
  </div>
  
  <button class="mic-button" id="micBtn" onclick="toggleListening()">🎤</button>
  
  <div class="transcript" id="transcript">Waiting...</div>
</div>

<script>
const TEXT_TO_SPEAK = `{safe_text}`;
const QUESTION_NUM = {question_num};
let recognition = null;
let isListening = false;
let finalTranscript = "";
let silenceTimer = null;
const SILENCE_THRESHOLD = 2000;

window.onload = function() {{
  speakText(TEXT_TO_SPEAK);
  initSpeechRecognition();
}};

function speakText(text) {{
  if (!text || !window.speechSynthesis) return;
  
  window.speechSynthesis.cancel();
  
  setTimeout(() => {{
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 0.95;
    utterance.pitch = 1.0;
    utterance.volume = 1.0;
    utterance.lang = 'en-US';
    
    const voices = window.speechSynthesis.getVoices();
    if (voices.length > 0) {{
      const preferredVoice = voices.find(v => v.lang.startsWith("en") && v.name.includes("Google")) || voices[0];
      utterance.voice = preferredVoice;
    }}
    
    utterance.onstart = () => {{
      document.getElementById('status').textContent = '🔊 AI Speaking...';
      document.getElementById('status').className = 'status speaking';
      document.getElementById('waveform').classList.add('active');
      document.getElementById('micBtn').disabled = true;
    }};
    
    utterance.onend = () => {{
      document.getElementById('status').textContent = '🎤 Your Turn - Click Mic';
      document.getElementById('status').className = 'status';
      document.getElementById('waveform').classList.remove('active');
      document.getElementById('micBtn').disabled = false;
      
      setTimeout(() => {{
        if (!isListening) {{
          startListening();
        }}
      }}, 500);
    }};
    
    utterance.onerror = (e) => {{
      console.error('TTS Error:', e);
      document.getElementById('status').textContent = 'Ready';
      document.getElementById('micBtn').disabled = false;
    }};
    
    window.speechSynthesis.speak(utterance);
  }}, 100);
}}

function initSpeechRecognition() {{
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {{
    document.getElementById('status').textContent = '❌ Speech recognition not supported';
    return;
  }}
  
  recognition = new SpeechRecognition();
  recognition.continuous = true;
  recognition.interimResults = true;
  recognition.lang = 'en-US';
  
  recognition.onstart = () => {{
    isListening = true;
    document.getElementById('micBtn').classList.add('listening');
    document.getElementById('status').textContent = '👂 Listening...';
    document.getElementById('status').className = 'status listening';
    document.getElementById('transcript').textContent = 'Speak now...';
  }};
  
  recognition.onresult = (event) => {{
    let interim = "";
    finalTranscript = "";
    
    for (let i = event.resultIndex; i < event.results.length; i++) {{
      const transcript = event.results[i][0].transcript;
      if (event.results[i].isFinal) {{
        finalTranscript += transcript + " ";
      }} else {{
        interim += transcript;
      }}
    }}
    
    document.getElementById('transcript').textContent = finalTranscript + interim;
    
    clearTimeout(silenceTimer);
    
    if (finalTranscript.trim()) {{
      silenceTimer = setTimeout(() => {{
        stopListening();
        submitAnswer();
      }}, SILENCE_THRESHOLD);
    }}
  }};
  
  recognition.onerror = (e) => {{
    console.error('Recognition error:', e.error);
    if (e.error === 'not-allowed') {{
      document.getElementById('status').textContent = '❌ Microphone access denied';
    }} else {{
      document.getElementById('status').textContent = '❌ Error: ' + e.error;
    }}
    stopListening();
  }};
  
  recognition.onend = () => {{
    if (isListening) {{
      try {{
        recognition.start();
      }} catch (e) {{
        console.log('Recognition restart failed:', e);
      }}
    }}
  }};
}}

function toggleListening() {{
  if (isListening) {{
    stopListening();
  }} else {{
    startListening();
  }}
}}

function startListening() {{
  if (!recognition) return;
  
  finalTranscript = "";
  document.getElementById('transcript').textContent = 'Speak now...';
  
  try {{
    recognition.start();
  }} catch (e) {{
    console.log('Recognition already started');
  }}
}}

function stopListening() {{
  isListening = false;
  if (recognition) {{
    recognition.onend = null;
    recognition.stop();
  }}
  
  document.getElementById('micBtn').classList.remove('listening');
  document.getElementById('status').textContent = '⚙️ Processing...';
  document.getElementById('status').className = 'status processing';
  
  clearTimeout(silenceTimer);
}}

function submitAnswer() {{
  const answer = finalTranscript.trim();
  if (!answer) {{
    document.getElementById('status').textContent = '❌ No speech detected';
    return;
  }}
  
  document.getElementById('transcript').textContent = '✅ Answer: ' + answer;
  document.getElementById('status').textContent = '✅ Ready to submit!';
  
  // Find the input field and fill it (but DON'T auto-click)
  setTimeout(() => {{
    try {{
      const parentDoc = window.parent.document;
      
      // Find input field by placeholder text
      let inputField = null;
      const allInputs = parentDoc.querySelectorAll('input[type="text"]');
      
      for (let input of allInputs) {{
        if (input.placeholder && input.placeholder.includes('voice answer')) {{
          inputField = input;
          break;
        }}
      }}
      
      if (!inputField) {{
        console.error('Could not find voice input field');
        return;
      }}
      
      console.log('Found input field, setting value...');
      
      // Set the value using native setter
      const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.parent.HTMLInputElement.prototype, 'value').set;
      nativeInputValueSetter.call(inputField, answer);
      
      // Trigger input event
      const inputEvent = new Event('input', {{ bubbles: true, cancelable: true }});
      inputField.dispatchEvent(inputEvent);
      
      // Focus the input to show the value
      inputField.focus();
      
      console.log('Input value set successfully:', inputField.value);
      
      // Change status to prompt user to click Send
      document.getElementById('status').textContent = '✅ Click Send button!';
      document.getElementById('status').className = 'status';
      
    }} catch (e) {{
      console.error('Error filling input:', e);
    }}
  }}, 500);
}}
</script>

</body>
</html>
"""
    
    components.html(html, height=400, scrolling=False)
