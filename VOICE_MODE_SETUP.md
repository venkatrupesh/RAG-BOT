# Voice Mode - Automatic Speech Processing

## Current Status
The voice mode feature needs to be re-implemented with automatic speech processing.

## Expected Flow

### 1. **User Enters Voice Mode**
- Bot greets user by name: "Hi [Username], ready to start your [Topic] interview at [Difficulty] level?"
- Uses Text-to-Speech (TTS) to speak the greeting

### 2. **Automatic Interview Flow**
```
Bot speaks question → User speaks answer → Bot processes speech → Bot gives feedback → Next question
```

### 3. **Key Features Needed**
- ✅ Automatic speech recognition (no manual buttons)
- ✅ Automatic answer submission after user stops speaking
- ✅ Bot speaks all questions and feedback
- ✅ Seamless conversation flow
- ✅ Visual feedback (listening indicator, processing status)

## Implementation Requirements

### JavaScript Components
```javascript
// Auto-detect when user stops speaking (silence detection)
// Auto-submit answer to Streamlit
// Show visual indicators (listening, processing, speaking)
```

### Python Backend
```python
# Process voice answer automatically
# Generate feedback with TTS
# Continue to next question
# Track conversation history
```

### UI Elements
- 🎤 Microphone indicator (active/inactive)
- 🔊 Speaker indicator (bot speaking)
- 👂 Listening indicator (recording user)
- ⚙️ Processing indicator (analyzing answer)
- 📝 Live transcript display

## Technical Approach

### Option 1: Web Speech API (Current)
- Browser-based speech recognition
- Works in Chrome/Edge
- No server costs
- Limited accuracy

### Option 2: External API (Recommended)
- Use Groq Whisper API for speech-to-text
- Better accuracy
- More reliable
- Requires API calls

## Next Steps

1. Re-implement voice component with auto-submission
2. Add silence detection (2-3 seconds of silence = answer complete)
3. Remove manual "Send" button
4. Add visual state indicators
5. Test end-to-end flow

## Configuration

Add to `.env`:
```env
# Voice Mode Settings
VOICE_SILENCE_THRESHOLD=2.5  # seconds
VOICE_AUTO_SUBMIT=true
VOICE_SHOW_TRANSCRIPT=true
```

## User Experience

**Perfect Flow:**
1. User clicks "Voice Interview"
2. Bot: "Hi John, ready to start Python interview at Intermediate level?"
3. User: "Yes, I'm ready"
4. Bot: "Great! What is a decorator in Python?"
5. User: "A decorator is a function that modifies another function..."
6. Bot: "Correct! Decorators use the @ symbol. Next question..."

**No manual clicks needed - fully automatic conversation!**
