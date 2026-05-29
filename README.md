# InterviewAI - AI-Powered Interview Assistant 💬

A clean, modern interview chatbot with RAG (Retrieval-Augmented Generation) capabilities, featuring both conversational interviews and MCQ tests.

## ✨ Features

- 🤖 **AI-Powered Interviews** - Intelligent question generation and evaluation
- 🔐 **Email Verification** - Secure registration with 6-digit codes
- 📝 **Two Interview Modes**:
  - Text Interview (Conversational Q&A)
  - MCQ Test (Multiple Choice with scoring)
- 📄 **RAG Mode** - Questions based on your documents (Python, Java, SQL)
- 🧠 **LLM Mode** - AI knowledge-based questions (other topics)
- 📊 **Real-Time Scoring** - Track your performance (MCQ mode)
- 🎯 **Multiple Topics** - Python, Java, JavaScript, C++, SQL, ML, System Design, etc.
- 🎚️ **Difficulty Levels** - Beginner, Intermediate, Advanced
- 👤 **User Authentication** - Secure login/signup with email verification
- 💾 **Session History** - Track your interview progress

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up API Key & Email
Create a `.env` file in the project root:
```env
# Required: Groq API Key
GROQ_API_KEY=your_groq_api_key_here

# Optional: Email Verification (for secure registration)
SENDER_EMAIL=your.email@gmail.com
SENDER_PASSWORD=your_gmail_app_password
```

**Get your Groq API key**: https://console.groq.com

**Setup Email Verification** (Optional but recommended):
- Follow `QUICK_START.md` for 5-minute setup
- See `EMAIL_SETUP_GUIDE.md` for detailed instructions
- Get Gmail App Password: https://myaccount.google.com/apppasswords

### 3. Run the Application
```bash
streamlit run ui/app.py
```

Or using Python module:
```bash
python -m streamlit run ui/app.py
```

The app will open at: **http://localhost:8501**

## 📖 Detailed Guides

### Setup & Configuration
- **[QUICK_START.md](QUICK_START.md)** - 5-minute email verification setup
- **[EMAIL_SETUP_GUIDE.md](EMAIL_SETUP_GUIDE.md)** - Complete email configuration guide
- **[EMAIL_VERIFICATION_FLOW.md](EMAIL_VERIFICATION_FLOW.md)** - Visual flow diagrams
- **[SETUP_SUMMARY.md](SETUP_SUMMARY.md)** - Complete feature overview
- **[HOW_TO_RUN.md](HOW_TO_RUN.md)** - Complete setup and troubleshooting guide

### Features & Usage
- **[MCQ_FEATURE_GUIDE.md](MCQ_FEATURE_GUIDE.md)** - MCQ test documentation
- **[SIDEBAR_GUIDE.md](SIDEBAR_GUIDE.md)** - UI navigation guide

## 🎮 How to Use

1. **Sign Up/Login** - Create an account or login
2. **Choose Mode** - Select Text Interview or MCQ Test
3. **Select Topic** - Pick from 8+ technical topics
4. **Set Difficulty** - Choose your level
5. **Start Interview** - Answer questions and get feedback!

### Interview Modes

**Text Interview:**
- Conversational Q&A format
- Detailed feedback on answers
- Type `pass` to skip questions
- Type `quit` to end interview

**MCQ Test:**
- Multiple choice questions (A, B, C, D)
- Instant scoring and feedback
- Real-time accuracy tracking
- Progress bar visualization

## 📁 Project Structure

```
RAG-CHATBOT/
├── ui/
│   └── app.py              # Main Streamlit application
├── bot/
│   ├── interviewer.py      # Interview logic
│   ├── evaluator.py        # Answer evaluation
│   └── prompt_builder.py   # Prompt templates
├── retrieval/
│   ├── retriever.py        # RAG retrieval logic
│   └── vector_store.py     # Vector database management
├── ingestion/
│   ├── loader.py           # Document loading
│   ├── chunker.py          # Text chunking
│   └── embedder.py         # Text embeddings
├── data/
│   ├── sample.pdf          # Sample documents
│   └── urls.txt            # URLs for ingestion
├── chroma_db/              # Vector database storage
├── .env                    # API keys (create this)
├── requirements.txt        # Python dependencies
└── users.json             # User data (auto-created)
```

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **AI Model**: Groq (Llama 3.3 70B)
- **Vector DB**: ChromaDB
- **Embeddings**: Sentence Transformers
- **RAG**: LangChain
- **PDF Processing**: PyPDF2

## 📊 Adding Your Documents (RAG Mode)

1. Place PDF files in `data/` folder
2. Add URLs to `data/urls.txt`
3. Run ingestion:
```bash
python ingestion/loader.py
```

This enables RAG mode for Python, Java, and SQL topics.

## 🎨 UI Design

Clean, minimal interface inspired by ChatGPT, Claude, and Gemini:
- White background with subtle grays
- Collapsible sidebar for settings
- Native chat interface
- Real-time score tracking (MCQ mode)
- Responsive design

## 🔧 Configuration

### Change Port
```bash
streamlit run ui/app.py --server.port 8080
```

### Enable Debug Mode
```bash
streamlit run ui/app.py --logger.level=debug
```

### Clear Cache
```bash
streamlit cache clear
```

## 📝 Requirements

- Python 3.8+
- GROQ API Key
- Internet connection
- 2GB RAM minimum

## 🐛 Troubleshooting

**App won't start?**
```bash
# Check Python version
python --version

# Reinstall dependencies
pip install -r requirements.txt

# Try alternative command
python -m streamlit run ui/app.py
```

**"streamlit: command not found"?**
```bash
pip install streamlit
```

**"GROQ_API_KEY not found"?**
- Check if `.env` file exists
- Verify API key is correct
- Restart the application

**Slow responses?**
- Check internet connection
- GROQ API might be experiencing delays
- Try again in a few moments

For more help, see **[HOW_TO_RUN.md](HOW_TO_RUN.md)**

## 🎯 Supported Topics

- 🐍 **Python** (RAG Mode)
- ☕ **Java** (RAG Mode)
- 🗄️ **SQL** (RAG Mode)
- ⚡ JavaScript (LLM Mode)
- ⚙️ C++ (LLM Mode)
- 📊 Data Science (LLM Mode)
- 🤖 Machine Learning (LLM Mode)
- 🏗️ System Design (LLM Mode)

## 📈 Features Roadmap

- [ ] Voice interview mode
- [ ] Code execution for programming questions
- [ ] Interview analytics dashboard
- [ ] Export interview transcripts
- [ ] Custom topic creation
- [ ] Multi-language support

## 🎓 Use Cases

- **Job Interview Prep** - Practice technical interviews
- **Exam Preparation** - Test your knowledge with MCQs
- **Skill Assessment** - Evaluate your technical skills
- **Learning Tool** - Learn from detailed feedback
- **Recruitment** - Screen candidates efficiently

## 📄 License

MIT License - feel free to use and modify!

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## 📞 Support

For issues or questions:
1. Check **[HOW_TO_RUN.md](HOW_TO_RUN.md)** for detailed setup
2. Review error messages in terminal
3. Verify API key is valid
4. Try clearing cache: `streamlit cache clear`

## 🌟 Quick Command Reference

```bash
# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run ui/app.py

# Run on different port
streamlit run ui/app.py --server.port 8080

# Stop application
Ctrl + C

# Clear cache
streamlit cache clear

# Update dependencies
pip install -r requirements.txt --upgrade
```

---

**Made with ❤️ using Streamlit and Groq AI**

**Start your interview journey today!** 🚀

**Current Status**: ✅ Running at http://localhost:8501
