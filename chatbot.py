"""
============================================================
  College Student Assistant Chatbot - FIXED VERSION
  Model  : Rule-Based (TF-IDF + Cosine Similarity + Exact Match)
  Web + Console Support
============================================================
"""

import json
import re
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime
import random

# Flask Web Support
try:
    from flask import Flask, render_template, request, jsonify
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    print("Flask not available - Console mode only")

# ─────────────────────────────────────────────────────────
#  CONFIG
# ─────────────────────────────────────────────────────────
DATASET_PATH  = "dataset.json"
THRESHOLD     = 0.3
EXACT_THRESHOLD = 0.85
LOG_FILE      = "chat_log.txt"
COLLEGE_NAME  = "ABC Engineering College"
BOT_NAME      = "CollegeBot"

BANNER = f"""
╔══════════════════════════════════════════════════════════╗
║         🎓  {COLLEGE_NAME}  🎓         ║
║                  Student Assistant Bot                   ║
╚══════════════════════════════════════════════════════════╝
  Type your question and press Enter.
  Type 'help' to see all topics.
  Type 'quit' or 'exit' to stop.
──────────────────────────────────────────────────────────
"""

# ─────────────────────────────────────────────────────────
#  GLOBAL MODEL (Shared between console/web)
# ─────────────────────────────────────────────────────────
data = None
vectorizer = None
tfidf_matrix = None
tag_map = None

def load_dataset(path: str):
    """Fixed: Handles both list and dict formats"""
    if not os.path.exists(path):
        print(f"[ERROR] Dataset file '{path}' not found!")
        return []
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
            if isinstance(raw_data, list):
                print("  📄 Direct list format detected")
                return raw_data
            elif isinstance(raw_data, dict) and 'intents' in raw_data:
                print("  📄 'intents' wrapper format detected")
                return raw_data['intents']
            else:
                print(f"[ERROR] Invalid JSON format!")
                return []
    except Exception as e:
        print(f"[ERROR] Loading dataset: {e}")
        return []

def preprocess(text: str) -> str:
    """Fixed preprocessing - preserve key phrases"""
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    words = [w for w in text.split() if len(w) > 1]  # lower min len to keep 'menu'
    return " ".join(words)

def exact_match(user_input: str, data: list) -> tuple:
    """Priority 1: Exact pattern matching"""
    user_words = set(preprocess(user_input).split())
    for item in data:
        for pattern in item["patterns"]:
            pattern_words = set(preprocess(pattern).split())
            if user_words.issuperset(pattern_words) or len(user_words.intersection(pattern_words)) >= 2:
                return item["response"], item.get("tag", item.get("intent", "unknown")), 1.0
    return None, None, 0.0

def keyword_priority_match(user_input: str, data: list) -> tuple:
    """Priority 2: Keyword → Tag mapping"""
    user_lower = user_input.lower()
    
    # FIXED: Direct keyword-to-response mapping for speed
    priority_responses = {
        "mess": """🍽️ **MESS MENU TODAY**
Breakfast: Poha + Tea
Lunch: Dal Makhani + Paneer + Rice + Roti
Dinner: Chicken Biryani + Raita
💰 Monthly: ₹3,500""",
        "menu": """🍽️ **MESS MENU TODAY**
Breakfast: Poha + Tea
Lunch: Dal Makhani + Paneer + Rice + Roti  
Dinner: Chicken Biryani + Raita
💰 Monthly: ₹3,500""",
        "food": """🍽️ **MESS MENU TODAY**
Breakfast: Poha + Tea
Lunch: Dal Makhani + Paneer + Rice + Roti
Dinner: Chicken Biryani + Raita
💰 Monthly: ₹3,500""",
        "hostel": "🏠 Separate hostels for boys & girls. Annual fee: ₹60,000 (includes mess). Contact: hostel@college.edu",
        "fee": "💰 Annual tuition: ₹45,000 | Semester: ₹22,500 | Lab: ₹5,000/year. Accounts Office: Block A, Room 101",
        "fees": "💰 Annual tuition: ₹45,000 | Semester: ₹22,500 | Lab: ₹5,000/year. Accounts Office: Block A, Room 101",
        "exam": "📅 End Semester Exams: 10th Dec 2024. Check notice board/student portal",
        "library": "📚 Library: Mon-Sat 8AM-8PM. Borrow 3 books for 14 days"
    }
    
    for keyword, response in priority_responses.items():
        if keyword in user_lower:
            return response, keyword, 0.95
    
    return None, None, 0.0

def build_model(data: list):
    """Build TF-IDF model"""
    if not data:
        return None, None, None
    
    patterns = []
    tag_map = []
    for idx, item in enumerate(data):
        for pattern in item["patterns"]:
            patterns.append(preprocess(pattern))
            tag_map.append(idx)

    vectorizer = TfidfVectorizer(
        min_df=1, max_df=0.9,
        ngram_range=(1, 2),
        stop_words='english'
    )
    tfidf_matrix = vectorizer.fit_transform(patterns)
    return vectorizer, tfidf_matrix, tag_map

def get_response(user_input: str) -> tuple:
    """Bulletproof 4-stage matching - MESS MENU ALWAYS FIRST"""
    global data, vectorizer, tfidf_matrix, tag_map
    
    user_lower = user_input.lower().strip()
    
    # ========================================
    # STAGE 0: HARDCODED MESS MENU (ALWAYS MATCHES)
    # ========================================
    mess_triggers = [
        'mess', 'menu', 'food', 'lunch', 'dinner', 'canteen', 
        'breakfast', 'messmenu', 'mess menu', 'food menu', 'college food', 
        'what food', 'food today', 'weekly menu', 'mess food'
    ]
    
    if any(trigger in user_lower for trigger in mess_triggers):
        mess_response = """🍽️ **TODAY'S MESS MENU** (Dec 15, 2024)

🥣 **Breakfast (8-9 AM):** Poha + Upma + Tea/Coffee
🍛 **Lunch (1-2 PM):** Dal Makhani, Paneer Butter Masala, Jeera Rice, 4 Rotis, Salad, Curd
🍕 **Snacks (4-5 PM):** Samosa + Bread Pakoda + Cold Drink
🍗 **Dinner (7:30-8:30 PM):** Chicken Biryani, Veg Raita, Papad, Gulab Jamun

**Weekly Specials:**
- Mon: Rajma-Chawal
- Wed: Pasta Day  
- Fri: Chole Bhature
- Sun: Biryani Feast + Ice Cream!

💰 Monthly Mess: ₹3,500 | Veg/Non-Veg available"""
        return mess_response, "mess_menu", 1.00
    
    # ========================================
    # STAGE 0.5: WEATHER CHECK
    # ========================================
    weather_triggers = ['weather', 'temperature', 'how hot', 'how cold', 'raining']
    if any(trigger in user_lower for trigger in weather_triggers):
        try:
            import urllib.request
            req = urllib.request.Request("https://wttr.in/Mumbai?format=3", headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                weather_data = response.read().decode('utf-8').strip()
            return f"🌤️ **Live Weather Update:**\n{weather_data}", "weather", 1.00
        except Exception as e:
            return "🌤️ I couldn't fetch the live weather right now, but it's usually pleasant in Mumbai!", "weather", 1.00
    # ========================================
    # STAGE 1: Other High Priority Keywords
    # ========================================
    priority_map = {
        'hostel': "🏠 **HOSTEL INFO**\nBoys & Girls hostels available. Annual fee: ₹60,000 (includes mess). Contact: hostel@college.edu",
        'fee': "💰 **FEES**\nAnnual tuition: ₹45,000 | Semester: ₹22,500 | Lab: ₹5,000/year\nAccounts Office: Block A, Room 101",
        'fees': "💰 **FEES**\nAnnual tuition: ₹45,000 | Semester: ₹22,500 | Lab: ₹5,000/year\nAccounts Office: Block A, Room 101", 
        'exam': "📅 **EXAMS**\nEnd Semester: 10th Dec 2024. Internal: October. Check notice board.",
        'library': "📚 **LIBRARY**\nMon-Sat: 8AM-8PM. Borrow 3 books (14 days). Closed Sundays.",
        'placement': "💼 **PLACEMENTS**\nTCS, Infosys, Wipro. Avg package: ₹4.5 LPA. Contact: placement@college.edu"
    }
    
    for keyword, response in priority_map.items():
        if keyword in user_lower:
            return response, keyword, 0.98
    
    # ========================================
    # STAGE 2: Your existing exact_match
    # ========================================
    if data:
        response, tag, score = exact_match(user_input, data)
        if score >= EXACT_THRESHOLD:
            return response, tag, score
    
    # ========================================
    # STAGE 3: Keyword priority from dataset
    # ========================================
    if data:
        response, tag, score = keyword_priority_match(user_input, data)
        if score >= 0.9:
            return response, tag, score
    
    # ========================================
    # STAGE 4: TF-IDF Fallback
    # ========================================
    if vectorizer is not None:
        cleaned = preprocess(user_input)
        query_vec = vectorizer.transform([cleaned])
        scores = cosine_similarity(query_vec, tfidf_matrix).flatten()
        best_idx = int(np.argmax(scores))
        confidence = round(float(scores[best_idx]), 2)

        if confidence >= THRESHOLD:
            matched_tag = data[tag_map[best_idx]].get("tag", data[tag_map[best_idx]].get("intent", "unknown"))
            matched_response = data[tag_map[best_idx]]["response"]
            return matched_response, matched_tag, confidence
    
    # ========================================
    # FINAL FALLBACK
    # ========================================
    return """🤖 **QUICK HELP:**
- `mess menu` / `food` 🍽️ - Today's menu
- `fee structure` 💰 - Tuition fees
- `hostel fees` 🏠 - Hostel details  
- `exam schedule` 📅 - Exam dates
- `library timing` 📚 - Library hours

**Type one of these!**""", "help", 0.5

# ─────────────────────────────────────────────────────────
#  CONSOLE MODE
# ─────────────────────────────────────────────────────────
def console_chat():
    global data, vectorizer, tfidf_matrix, tag_map
    
    print(BANNER)
    data = load_dataset(DATASET_PATH)
    vectorizer, tfidf_matrix, tag_map = build_model(data)
    
    if not data:
        print("❌ No data loaded. Exiting.")
        return
    
    print(f"✅ Loaded {len(data)} topics | Model ready!\n")
    
    total, matched, unknown = 0, 0, 0
    
    while True:
        try:
            user_input = input("💬 You: ").strip()
        except (KeyboardInterrupt, EOFError):
            break

        if not user_input:
            continue

        total += 1
        
        if user_input.lower() in ("help", "menu", "?"):
            print("\n📋 TOPICS: mess menu, hostel, fees, exams, library...")
            continue
            
        if user_input.lower() in ("quit", "exit", "q", "bye"):
            print("👋 Goodbye!")
            break

        response, tag, score = get_response(user_input)
        
        conf_emoji = "🟢" if score > 0.8 else "🟡" if score > 0.5 else "🔴"
        print(f"\n🤖 {BOT_NAME}: {response}")
        print(f"  ({conf_emoji} {score:.0%})\n{'─'*60}")

# ─────────────────────────────────────────────────────────
#  FLASK WEB MODE
# ─────────────────────────────────────────────────────────
if FLASK_AVAILABLE:
    app = Flask(__name__)
    
    @app.route('/')
    def home():
        return render_template("index.html")
    
    @app.route('/chat', methods=['POST'])
    def flask_chat():
        msg = request.json['message']
        response, tag, confidence = get_response(msg)
        return jsonify({'response': response, 'confidence': confidence, 'ok': True})
    
    def web_chat():
        global data, vectorizer, tfidf_matrix, tag_map
        data = load_dataset(DATASET_PATH)
        vectorizer, tfidf_matrix, tag_map = build_model(data)
        print("🌐 Web server starting on http://localhost:5002")
        app.run(debug=True, host='0.0.0.0', port=5002)

# ─────────────────────────────────────────────────────────
#  MAIN ENTRY POINT
# ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "web":
        if FLASK_AVAILABLE:
            web_chat()
        else:
            print("❌ Install Flask: pip install flask")
    else:
        console_chat()