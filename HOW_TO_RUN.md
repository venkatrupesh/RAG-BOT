# How to Run InterviewAI - Complete Guide

## 📋 Prerequisites

Before running the project, make sure you have:
- **Python 3.8+** installed
- **pip** (Python package manager)
- **GROQ API Key** (for AI responses)

## 🚀 Quick Start (3 Steps)

### **Step 1: Install Dependencies**
Open terminal/command prompt in the project folder and run:

```bash
pip install -r requirements.txt
```

This will install all required packages:
- streamlit (UI framework)
- groq (AI model)
- chromadb (vector database)
- sentence-transformers (embeddings)
- langchain (RAG framework)
- python-dotenv (environment variables)
- PyPDF2 (PDF processing)

### **Step 2: Set Up Environment Variables**
Create or edit the `.env` file in the project root:

```bash
GROQ_API_KEY=your_groq_api_key_here
```

**How to get GROQ API Key:**
1. Go to https://console.groq.com
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy and paste it in the `.env` file

### **Step 3: Run the Application**
```bash
streamlit run ui/app.py
```

Or using Python module:
```bash
python -m streamlit run ui/app.py
```

The app will open automatically in your browser at:
- **Local URL**: http://localhost:8501
- **Network URL**: http://YOUR_IP:8501

## 📁 Project Structure

```
RAG-CHATBOT/
├── ui/
│   └── app.py              # Main application (Streamlit UI)
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
├── .env                    # Environment variables (API keys)
├── requirements.txt        # Python dependencies
└── users.json             # User data (auto-created)
```

## 🎯 First Time Setup

### **1. Install Python**
If you don't have Python installed:
- **Windows**: Download from https://python.org
- **Mac**: `brew install python3`
- **Linux**: `sudo apt install python3 python3-pip`

### **2. Verify Installation**
```bash
python --version
pip --version
```

### **3. Create Virtual Environment (Optional but Recommended)**
```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

### **4. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **5. Set Up API Key**
Edit `.env` file:
```
GROQ_API_KEY=gsk_your_actual_api_key_here
```

### **6. Run the App**
```bash
streamlit run ui/app.py
```

## 🔧 Troubleshooting

### **Problem: "streamlit: command not found"**
**Solution:**
```bash
# Install streamlit
pip install streamlit

# Or use Python module
python -m streamlit run ui/app.py
```

### **Problem: "ModuleNotFoundError: No module named 'groq'"**
**Solution:**
```bash
pip install groq
```

### **Problem: "GROQ_API_KEY not found"**
**Solution:**
1. Check if `.env` file exists in project root
2. Make sure it contains: `GROQ_API_KEY=your_key`
3. Restart the application

### **Problem: Port 8501 already in use**
**Solution:**
```bash
# Use a different port
streamlit run ui/app.py --server.port 8502
```

### **Problem: Dependencies conflict**
**Solution:**
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

## 📱 Using the Application

### **1. First Login**
- Open http://localhost:8501
- Click "Sign Up" tab
- Create an account with:
  - Username
  - Email
  - Password (min 6 characters)

### **2. Start Interview**
- Login with your credentials
- Select **Interview Mode** (Text or MCQ)
- Choose **Topic** (Python, Java, etc.)
- Select **Difficulty** (Beginner/Intermediate/Advanced)
- Start chatting!

### **3. Interview Modes**

**Text Interview:**
- Conversational Q&A
- Type your answers
- Get detailed feedback
- Use `pass` to skip questions
- Use `quit` to end

**MCQ Test:**
- Multiple choice questions
- Type A, B, C, or D
- Instant scoring
- Real-time accuracy tracking
- Progress bar in sidebar

## 🛠️ Advanced Configuration

### **Change Port**
```bash
streamlit run ui/app.py --server.port 8080
```

### **Run in Background**
```bash
# Windows
start /B streamlit run ui/app.py

# Mac/Linux
nohup streamlit run ui/app.py &
```

### **Enable Debug Mode**
```bash
streamlit run ui/app.py --logger.level=debug
```

### **Custom Configuration**
Create `.streamlit/config.toml`:
```toml
[server]
port = 8501
headless = true

[theme]
primaryColor = "#6366f1"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f7f7f8"
textColor = "#1a1a1a"
```

## 📊 Adding Your Own Documents (RAG Mode)

### **1. Add PDF Documents**
Place your PDF files in the `data/` folder:
```
data/
├── sample.pdf
├── your_document.pdf
└── another_doc.pdf
```

### **2. Add URLs**
Edit `data/urls.txt` and add URLs (one per line):
```
https://docs.python.org/3/tutorial/
https://www.example.com/article
```

### **3. Ingest Documents**
Run the ingestion script:
```bash
python ingestion/loader.py
```

This will:
- Load all PDFs from `data/` folder
- Fetch content from URLs
- Create embeddings
- Store in ChromaDB

### **4. Use RAG Mode**
- Select topics: Python, Java, or SQL
- These topics will automatically use RAG mode
- Questions will be based on your documents

## 🔄 Updating the Project

### **Pull Latest Changes**
```bash
git pull origin main
```

### **Update Dependencies**
```bash
pip install -r requirements.txt --upgrade
```

### **Clear Cache**
```bash
streamlit cache clear
```

## 🐛 Common Issues

### **Issue: Slow Response**
- Check your internet connection
- GROQ API might be slow
- Try reducing context length

### **Issue: Out of Memory**
- Reduce batch size in embeddings
- Clear ChromaDB: delete `chroma_db/` folder
- Restart the application

### **Issue: Login Not Working**
- Check if `users.json` exists
- Delete `users.json` to reset users
- Create a new account

## 📞 Support

If you encounter issues:
1. Check the error message in terminal
2. Verify all dependencies are installed
3. Ensure `.env` file has valid API key
4. Try restarting the application

## 🎉 Success!

If everything is working, you should see:
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://10.x.x.x:8501
```

Open the URL in your browser and start interviewing! 🚀

## 📝 Quick Command Reference

```bash
# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run ui/app.py

# Run on different port
streamlit run ui/app.py --server.port 8080

# Stop application
Ctrl + C (in terminal)

# Clear cache
streamlit cache clear

# Update dependencies
pip install -r requirements.txt --upgrade
```

Happy Interviewing! 💬✨
