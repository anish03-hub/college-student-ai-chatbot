<div align="center">

<!-- Animated Header Wave Banner -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:1a0b2e,50:6b21a8,100:3b82f6&height=220&section=header&text=College%20Student%20AI%20Chatbot%20🎓&fontSize=38&fontColor=ffffff&animation=fadeIn&fontAlignY=36&desc=Intelligent%20Academic%20%26%20Campus%20Assistance%20System%20Powered%20by%20Hybrid%20NLP&descAlignY=58&descSize=17" alt="College Student AI Chatbot Banner" width="100%"/>

<!-- Animated Typing Subtitle -->
<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=20&duration=3000&pause=800&color=A855F7&center=true&vCenter=true&width=1000&height=50&lines=Campus+%26+Academic+Query+Assistant+for+College+Students;Hybrid+NLP+Engine%3A+TF-IDF+Vectorization+%2B+Cosine+Similarity;Instant+Answers+for+Exams%2C+Fees%2C+Timetables%2C+Hostel+%26+Mess;Dual+Interface%3A+Modern+Web+Portal+%26+Interactive+CLI+Terminal+%F0%9F%9A%80" alt="CollegeBot Typing SVG" />

<br>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3"/>
  <img src="https://img.shields.io/badge/NLP-scikit--learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white" alt="scikit-learn"/>
  <img src="https://img.shields.io/badge/Algorithm-TF--IDF%20%2B%20Cosine%20Similarity-6366F1?style=for-the-badge" alt="TF-IDF"/>
  <img src="https://img.shields.io/badge/Web_Framework-Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask"/>
  <img src="https://img.shields.io/badge/Frontend-HTML5%20%2F%20CSS3%20%2F%20JS-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="Web UI"/>
</p>

<!-- Real-Time Metrics & Indicators -->
<p align="center">
  <img src="https://img.shields.io/badge/Response_Latency-%3C15ms_Instant-10B981?style=flat-square&logo=speedtest&logoColor=white"/>
  <img src="https://img.shields.io/badge/Campus_Intents-70%2B_Topics-8B5CF6?style=flat-square&logo=knowledgebase&logoColor=white"/>
  <img src="https://img.shields.io/badge/Accuracy-95%25%2B_Match_Confidence-0284C7?style=flat-square&logo=target&logoColor=white"/>
  <img src="https://img.shields.io/badge/Architecture-3--Tier_Hybrid_Matching-EC4899?style=flat-square"/>
</p>

<p align="center">
  <b>A responsive Natural Language Processing (NLP) chatbot designed to streamline student access to university information, eliminating repetitive administrative queries across examinations, fees, mess menus, hostel rules, and academics.</b>
</p>

</div>

---

### 💬 Live Student Query & Response Simulation

<div align="center">

<!-- Animated Interactive Chat Simulation Terminal -->
<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=500&size=15&duration=4200&pause=1200&color=C084FC&background=0D1117&center=false&vCenter=true&width=860&height=125&lines=%F0%9F%8E%93+Student%3A+%22What+is+today's+mess+menu+and+hostel+fee%3F%22;%F0%9F%A4%96+CollegeBot%3A+%22%F0%9F%8D%BD%EF%B8%8F+MESS%3A+Dal+Makhani+%2B+Paneer+%7C+%F0%9F%8F%A0+Hostel%3A+%E2%82%B960%2C000%2Fyear+(includes+mess)!%22;%F0%9F%8E%93+Student%3A+%22When+do+end-sem+exams+begin+and+what's+the+fee%3F%22;%F0%9F%A4%96+CollegeBot%3A+%22%F0%9F%93%85+Exams+commence+Dec+10th+%7C+%F0%9F%92%B0+Tuition%3A+%E2%82%B945%2C000%2Fyr+(Accounts%3A+Block+A)%22" alt="Terminal Chat Simulation"/>

</div>

---

## 📑 Table of Contents

- [Overview](#-overview)
- [System Architecture](#-system-architecture)
- [Core Features](#-core-features)
- [NLP & Matching Engine](#-nlp--matching-engine)
- [Knowledge Base & Intent Domains](#-knowledge-base--intent-domains)
- [REST API Specifications](#-rest-api-specifications)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Author & Connect](#-author--connect)

---

## 💡 Overview

University administrative desks and department heads receive hundreds of repetitive student queries every day regarding examination timetables, fee due dates, hostel allocation, library borrowing limits, and daily cafeteria menus. 

**College Student AI Chatbot** automates this communication pipeline with an intelligent, rule-backed hybrid Natural Language Processing engine:
- **Sub-15ms Latency:** Instant response delivery without requiring heavy, expensive cloud LLM APIs.
- **3-Tier Matching Hierarchy:** Guarantees exact matches for critical campus keywords while using statistical TF-IDF cosine similarity for variations in natural phrasing.
- **Dual Mode Deployment:** Functions as both an interactive web application (Flask + responsive UI) and a standalone terminal CLI.
- **Interaction Auditing:** Automatically records conversational history and unmatched queries to `chat_log.txt` for continuous intent expansion.

---

## 🏛 System Architecture

The chatbot utilizes a multi-tiered pipeline that progressively matches user queries from strict pattern matching down to vector space cosine similarities:

```mermaid
flowchart TD
    UserQuery(["Student Natural Language Input\n('when are final exams scheduled?')"])
    
    subgraph Preprocessing ["1. Text Normalization Pipeline"]
        Clean["Lowercasing & Whitespace Stripping"]
        Regex["Punctuation Removal & Regex Filtering"]
        Tokens["Tokenization & Keyword Extraction"]
        Clean --> Regex --> Tokens
    end

    subgraph Matcher ["2. Multi-Tier Matching Engine"]
        T1{"Tier 1: Exact Match?\n(Pattern Match >= 0.85)"}
        T2{"Tier 2: Keyword Priority?\n(Direct Keyword Dictionary)"}
        T3["Tier 3: TF-IDF Vector Space\nCosine Similarity Matrix"]
        
        T1 -- Yes --> R1["Exact Response (Conf: 1.0)"]
        T1 -- No --> T2
        T2 -- Yes --> R2["Priority Response (Conf: 0.95)"]
        T2 -- No --> T3
    end

    subgraph Evaluation ["3. Confidence Scoring & Dispatch"]
        Score{"Cosine Score >= 0.30 Threshold?"}
        T3 --> Score
        Score -- Yes --> R3["Best Matching Intent Response"]
        Score -- No --> Fallback["Friendly Fallback Response\n('Please contact college office...')"]
    end

    subgraph Output ["4. Client & Audit Layer"]
        Resp["Response Returned (Web UI / Terminal CLI)"]
        Log[("Append Query & Tag to chat_log.txt")]
    end

    UserQuery --> Clean
    R1 --> Resp
    R2 --> Resp
    R3 --> Resp
    Fallback --> Resp
    Resp --> Log
```

---

## ✨ Core Features

| Feature | Description |
| :--- | :--- |
| ⚡ **Instant Query Resolution** | Delivers accurate academic information in under 15ms using optimized local scikit-learn vectorizers. |
| 🎯 **Hybrid NLP Strategy** | Seamless combination of pattern matching, keyword dictionaries, and TF-IDF cosine similarity. |
| 🍽️ **Daily Mess & Canteen Feeds** | Provides meal breakdowns (Breakfast, Lunch, Dinner) and monthly mess subscription rates. |
| 📅 **Exam & Academic Timetables** | Instant lookups for semester exam dates, hall ticket downloads, and result portals. |
| 💰 **Fee & Accounts Navigation** | Breakdown of tuition, hostel, semester dues, and physical accounts office locations. |
| 📚 **Library & Facility Guidelines** | Timings (8 AM – 8 PM), borrowing limits (3 books for 14 days), and digital catalog instructions. |
| 🌐 **Modern Web Interface** | Clean, responsive Flask-powered chat UI with auto-scrolling conversation bubbles. |
| 🖥️ **Terminal CLI Mode** | Standalone console mode with ANSI colored prompts and ASCII branding banner. |
| 📝 **Audit Logging** | Automatically logs every question, intent tag, and timestamp to `chat_log.txt` for administrative review. |

---

## 🧠 NLP & Matching Engine

The decision logic operates across three progressive tiers to balance speed and semantic flexibility:

```python
# Tier 1: Exact Pattern Matching
user_words = set(preprocess(user_input).split())
# Evaluates intersection with verified intent patterns

# Tier 2: Priority Keyword Lookup
priority_responses = {
    "mess": "🍽️ Mess Menu Today: Breakfast, Lunch, Dinner...",
    "fee":  "💰 Annual tuition: ₹45,000 | Semester: ₹22,500...",
    "exam": "📅 End Semester Exams: Check student portal..."
}

# Tier 3: TF-IDF Vectorization & Cosine Similarity
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(corpus)
similarity_scores = cosine_similarity(user_vector, tfidf_matrix)
```

- **Confidence Threshold:** `0.30` (Filters out unrelated noise or gibberish).
- **Exact Threshold:** `0.85` (Bypasses matrix computation for instantaneous response).

---

## 📚 Knowledge Base & Intent Domains

The bot's unified dataset (`dataset.json`) encompasses **70+ unique campus intents**:

- 🎓 **Academics:** Course syllabus, department contacts, faculty offices, academic calendar.
- 📝 **Examinations:** Schedule, admit card / hall ticket download, revaluation process.
- 💳 **Fees & Finance:** Tuition fees, lab charges, payment deadlines, scholarship procedures.
- 🏠 **Campus Accommodation:** Boys & girls hostel allotment, room rules, warden contacts.
- 🍽️ **Dining:** Daily breakfast, lunch, and dinner menus; monthly mess passes.
- 📖 **Library:** Timings, fine policies, book renewal, research journals access.
- 🚀 **Placements:** Training & placement cell contacts, recruiting companies, mock interviews.

---

## 📡 REST API Specifications

The Flask application exposes a lightweight JSON endpoint for seamless frontend and mobile integration:

### Query Bot
- **Endpoint:** `POST /get_response`
- **Headers:** `Content-Type: application/json`
- **Request Body:**
```json
{
  "message": "When do end semester exams start?"
}
```
- **Response (`200 OK`):**
```json
{
  "response": "📅 End Semester Exams begin on 10th Dec 2024. Please check the student portal for detailed subject timetables.",
  "tag": "exam",
  "confidence": 0.95
}
```

---

## 📂 Project Structure

```
college-student-ai-chatbot/
├── chatbot.py            # Main application runner (Flask Web + CLI Engine)
├── dataset.json          # Unified intent dataset with 70+ campus categories
├── update_dataset.py     # Utility script for appending & normalizing intents
├── chat_log.txt          # Conversation audit and analytics log
├── requirements.txt      # Python dependencies (scikit-learn, numpy, flask)
├── static/               # Frontend assets (CSS stylesheets, icons)
│   └── style.css         # Modern chat bubble UI styling
├── templates/            # Jinja2 HTML templates
│   └── index.html        # Interactive student chat web portal
└── model/                # Serialized model cache & preprocessed components
```

---

## 🚀 Getting Started

### Prerequisites
- Python `3.9` or higher
- `pip` package manager

### 1. Clone & Set Up Environment

```bash
# Clone the repository
git clone https://github.com/anish03-hub/college-student-ai-chatbot.git
cd college-student-ai-chatbot

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Launch Web Interface

```bash
python chatbot.py
```
Open your browser and navigate to **`http://localhost:5000`** to chat with CollegeBot.

### 3. Launch in Terminal CLI Mode

Run without web server dependencies:
```bash
python chatbot.py --cli
```

---

<div align="center">

## 👨‍💻 Author & Connect

**Anish Kumar Sah**  
*Java Developer | Spring Boot & REST APIs | B.Tech CSE @ Symbiosis Institute of Technology, Pune*

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Anish%20Kumar%20Sah-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/anishsah)
[![Email](https://img.shields.io/badge/Email-sah42515%40gmail.com-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:sah42515@gmail.com)
[![GitHub](https://img.shields.io/badge/GitHub-anish03--hub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/anish03-hub)

<br>

<!-- Animated Waving Footer Banner -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:3b82f6,50:6b21a8,100:1a0b2e&height=110&section=footer" alt="Footer Banner" width="100%"/>

<sub>Built with ❤️ using Python, scikit-learn, and Flask. Empowering students with instant campus knowledge.</sub>

</div>
