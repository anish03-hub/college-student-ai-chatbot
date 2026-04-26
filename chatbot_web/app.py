"""
============================================================
  College Student Assistant — FULL AI CHATBOT
  100% Gemini-powered | Streaming | Multi-turn memory
============================================================
"""

from flask import Flask, render_template, request, jsonify, Response, stream_with_context
from flask_cors import CORS
import google.generativeai as genai
import os, json, datetime

app = Flask(__name__)
CORS(app)

# ─────────────────────────────────────────────────────────
#  CONFIG — replace with your key
# ─────────────────────────────────────────────────────────
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyC2hA0zTgulcOcsKtx2FK3gQ1bDXKxpECQ")

COLLEGE_SYSTEM_PROMPT = """
You are CampusAI — a smart, friendly, and knowledgeable AI assistant for ABC Engineering College.

COLLEGE FACTS (always use these when relevant):
- College Name: ABC Engineering College
- Location: Mumbai, Maharashtra, India
- Courses: B.Tech (CS, IT, EC, ME, CE), M.Tech, MBA
- Total Students: ~4,000 | Founded: 1998
- Principal: Dr. Ramesh Kumar | Dean: Dr. Priya Sharma

FEES:
- B.Tech Tuition: ₹45,000/year
- Hostel: ₹60,000/year (meals included)
- Exam Fee: ₹2,500/semester

HOSTEL:
- Boys Hostel: Block H1, H2 (capacity 800)
- Girls Hostel: Block G1, G2 (capacity 600)
- Warden: Mr. Suresh (Boys), Ms. Kavitha (Girls)
- Curfew: 10 PM weekdays, 11 PM weekends

MESS MENU (Weekly):
- Breakfast (8–9 AM): Poha/Upma/Idli + Tea/Coffee
- Lunch (1–2 PM): Dal + Sabji + Rice + 4 Rotis + Salad + Curd
- Snacks (4–5 PM): Samosa / Pakoda / Sandwich + Juice
- Dinner (7:30–8:30 PM): Varies daily
  Monday: Rajma Chawal | Wednesday: Pasta | Friday: Chole Bhature | Sunday: Biryani + Ice Cream
- Monthly Mess Fee: ₹3,500

EXAMS:
- Mid Sem: March & September | End Sem: November–December & May
- Results: Student portal within 3 weeks
- Revaluation: Apply within 7 days, fee ₹500/subject

LIBRARY:
- Hours: 8 AM–8 PM (Mon–Sat), 10 AM–4 PM (Sunday)
- 50,000+ books | E-resources: IEEE, Springer, JSTOR
- Borrow: 3 books for 14 days | Fine: ₹2/day

PLACEMENTS:
- Head: Mr. Anil Joshi, Block D Room 101
- Recruiters: TCS, Infosys, Wipro, Cognizant, HCL, Amazon, Deloitte
- Average: 4.5 LPA | Highest: 18 LPA (Amazon 2024) | Rate: 87%

ADMISSIONS:
- 12th Science 60%+ | MHT-CET / JEE Main
- admissions@abccollege.edu.in | +91-22-1234-5678

TRANSPORT:
- Buses from: Dadar, Andheri, Thane, Navi Mumbai, Kalyan
- Fee: ₹8,000/year

CONTACTS:
- Admin: Block A, 9 AM–5 PM | +91-22-1234-5678
- Medical: 24/7, Block M
- Counselor: Block C, Room 12
- Helpdesk: helpdesk@abccollege.edu.in

YOUR RULES:
1. Be helpful, friendly, warm — like a knowledgeable senior student.
2. Answer ANY question — college info, academics, coding, science, weather, career, general knowledge, etc.
3. Use the college facts above when relevant. For everything else, use your broad knowledge.
4. Use bullet points and emojis for clarity where appropriate.
5. If unsure about a very specific college detail, admit it and suggest contacting admin.
6. NEVER refuse general knowledge questions. You know a lot — use it!
7. For mental health/stress, be empathetic and mention the counselor (Block C, Room 12).
8. Keep responses concise but complete.
"""

# ─────────────────────────────────────────────────────────
#  GEMINI INIT
# ─────────────────────────────────────────────────────────
gemini_model  = None
chat_sessions = {}
AI_READY      = False


def init_gemini():
    global gemini_model, AI_READY
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        gemini_model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=COLLEGE_SYSTEM_PROMPT,
            generation_config=genai.GenerationConfig(
                temperature=0.7,
                max_output_tokens=1024,
                top_p=0.9,
            ),
            safety_settings=[
                {"category": "HARM_CATEGORY_HARASSMENT",        "threshold": "BLOCK_ONLY_HIGH"},
                {"category": "HARM_CATEGORY_HATE_SPEECH",       "threshold": "BLOCK_ONLY_HIGH"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_ONLY_HIGH"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_ONLY_HIGH"},
            ]
        )
        AI_READY = True
        print("✅ Gemini 2.0 Flash initialized and ready!")
    except Exception as e:
        print(f"❌ Gemini init failed: {e}")
        AI_READY = False


def get_or_create_session(session_id: str):
    if session_id not in chat_sessions:
        chat_sessions[session_id] = gemini_model.start_chat(history=[])
    return chat_sessions[session_id]


def ask_gemini(message: str, session_id: str = "default") -> str:
    if not AI_READY or gemini_model is None:
        return "⚠️ AI is not available. Check GEMINI_API_KEY and server logs."
    try:
        chat     = get_or_create_session(session_id)
        response = chat.send_message(message)
        return response.text.strip()
    except Exception as e:
        print(f"❌ Gemini error: {e}")
        # Retry with fresh session
        try:
            chat_sessions.pop(session_id, None)
            chat     = get_or_create_session(session_id)
            response = chat.send_message(message)
            return response.text.strip()
        except Exception as e2:
            return f"⚠️ Couldn't get a response: {str(e2)}. Please try again."


# ─────────────────────────────────────────────────────────
#  ROUTES
# ─────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        body       = request.get_json(force=True) or {}
        message    = (body.get("message") or "").strip()
        session_id = body.get("session_id", "default")

        if not message:
            return jsonify({"response": "Please type a message!", "ok": False})

        response = ask_gemini(message, session_id)
        return jsonify({"response": response, "ok": True, "source": "gemini-2.0-flash"})

    except Exception as e:
        print(f"❌ /chat error: {e}")
        return jsonify({"response": f"Server error: {str(e)}", "ok": False}), 500


@app.route("/chat/stream", methods=["POST"])
def chat_stream():
    """Server-Sent Events streaming — tokens arrive in real time."""
    body       = request.get_json(force=True) or {}
    message    = (body.get("message") or "").strip()
    session_id = body.get("session_id", "default")

    if not message:
        return jsonify({"error": "Empty message"}), 400

    def generate():
        try:
            if not AI_READY or gemini_model is None:
                yield f"data: {json.dumps({'text': '⚠️ AI not ready. Check API key.'})}\n\n"
                yield f"data: {json.dumps({'done': True})}\n\n"
                return

            chat     = get_or_create_session(session_id)
            response = chat.send_message(message, stream=True)

            for chunk in response:
                if chunk.text:
                    yield f"data: {json.dumps({'text': chunk.text})}\n\n"

            yield f"data: {json.dumps({'done': True})}\n\n"

        except Exception as e:
            print(f"❌ Stream error: {e}")
            yield f"data: {json.dumps({'error': str(e), 'done': True})}\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",   # Important for Nginx
        }
    )


@app.route("/clear", methods=["POST"])
def clear_session():
    body       = request.get_json(force=True) or {}
    session_id = body.get("session_id", "default")
    chat_sessions.pop(session_id, None)
    return jsonify({"ok": True, "message": "Conversation cleared!"})


@app.route("/status")
def status():
    return jsonify({
        "ai_ready"       : AI_READY,
        "model"          : "gemini-2.0-flash",
        "active_sessions": len(chat_sessions),
        "college"        : "ABC Engineering College",
        "timestamp"      : datetime.datetime.now().isoformat()
    })


# ─────────────────────────────────────────────────────────
#  STARTUP — runs always, not just when __name__ == '__main__'
# ─────────────────────────────────────────────────────────
init_gemini()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080, use_reloader=False)