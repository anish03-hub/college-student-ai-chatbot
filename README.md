# College Student Assistant Chatbot
### AI Mini Project | Rule-Based Chatbot using Python

---

## Project Overview
An AI-powered chatbot that provides instant answers to student queries
about academics, schedules, fees, and college information.

---

## Files
| File | Description |
|------|-------------|
| `chatbot.py` | Main chatbot program |
| `dataset.json` | FAQ dataset (20 topics) |
| `requirements.txt` | Python dependencies |
| `chat_log.txt` | Auto-generated conversation log |

---

## How to Run

### Step 1 – Install dependencies
```
pip install -r requirements.txt
```

### Step 2 – Run the chatbot
```
python chatbot.py
```

---

## Topics Covered
- Fees & Payments
- Exam Dates & Timetable
- Library Hours
- Hostel & Canteen
- Admissions & Scholarships
- Attendance Rules
- Results & Grade Cards
- Placement & Internships
- Sports & Wi-Fi
- College Contact Info

---

## Model Used
- **Algorithm**: TF-IDF Vectorizer + Cosine Similarity
- **Library**: scikit-learn
- **Dataset**: 20 topics, 100+ patterns (dataset.json)
- **Threshold**: 0.25 similarity score

---

## Architecture
```
User Input → Preprocessing → TF-IDF Matching → Response → Output
                                   ↓
                          dataset.json (FAQ)
```
