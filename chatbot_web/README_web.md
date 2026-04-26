# PAST Engineering College Web Chatbot - Run Guide

## 🚀 Quick Start (Windows/VSCode Terminal)

### Step 1: Open new terminal in `c:/Users/Prati/Downloads/files`

### Step 2: Install & Run (one command)
```powershell
pip install flask scikit-learn numpy && python chatbot_web/app.py
```

### Step 3: Open Browser
```
http://127.0.0.1:5000
```

## 📱 Features
- **60 topics** (fees, exams, hostel, library, transport, medical...)
- **Nice UI** - responsive chat interface
- **TF-IDF matching** - intelligent responses
- **Real-time** AJAX chat

## 🧪 Test Queries
```
what is the fee structure?
when is the exam?
library hours
hostel fee
college timing
help
```

## 🔧 Troubleshooting
**Flask error:** `pip install flask --upgrade`
**Model load error:** Ensure `dataset.json` in `chatbot_web/`
**Port busy:** `taskkill /f /im python.exe`

## 🛑 Stop Server
Ctrl+C in terminal

**Ready! 🎓 PAST Engineering College**

