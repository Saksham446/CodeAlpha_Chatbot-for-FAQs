from flask import Flask, request, jsonify
from flask_cors import CORS

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from nltk.tokenize import wordpunct_tokenize
from nltk.stem import PorterStemmer

import re


# =========================================================
# FLASK APPLICATION
# =========================================================

app = Flask(__name__)
CORS(app)


# =========================================================
# FAQ KNOWLEDGE BASE
# =========================================================

FAQS = [
    {
        "question": "What is your name?",
        "answer": "I am FAQBot AI, an intelligent FAQ chatbot."
    },
    {
        "question": "What is FAQBot AI?",
        "answer": "FAQBot AI is an NLP-based chatbot that finds the most relevant answer from a predefined FAQ knowledge base."
    },
    {
        "question": "What can you help me with?",
        "answer": "I can answer common questions about admissions, courses, fees, exams, placements, library, hostel, timings, and technical support."
    },
    {
        "question": "How can I contact support?",
        "answer": "You can contact support through the official support desk or the help section of the application."
    },
    {
        "question": "What are the admission requirements?",
        "answer": "Admission requirements depend on the course. Generally, students need to satisfy the required academic eligibility criteria and complete the application process."
    },
    {
        "question": "How can I apply for admission?",
        "answer": "You can apply by completing the admission application form and submitting the required documents."
    },
    {
        "question": "What courses are available?",
        "answer": "The available courses depend on the institution. FAQBot AI can be configured with course information for a specific organization."
    },
    {
        "question": "How can I check my course details?",
        "answer": "You can check your course details through the academic or student information section."
    },
    {
        "question": "What is the fee structure?",
        "answer": "The fee structure varies by course and program. Please check the official fee details provided by your institution."
    },
    {
        "question": "How can I pay my fees?",
        "answer": "Fees can generally be paid through the available online payment methods or through the institution's designated fee counter."
    },
    {
        "question": "When are exams conducted?",
        "answer": "Examination dates are announced according to the academic calendar. Check the examination section for the latest schedule."
    },
    {
        "question": "How can I check my exam schedule?",
        "answer": "You can check your examination schedule through the student portal or examination section."
    },
    {
        "question": "How can I check my results?",
        "answer": "Results can generally be checked through the official student portal after they are published."
    },
    {
        "question": "Is hostel accommodation available?",
        "answer": "Hostel availability depends on the institution. Please contact the administration or hostel office for accommodation details."
    },
    {
        "question": "How can I apply for hostel accommodation?",
        "answer": "You can apply for hostel accommodation by submitting the required hostel application form and documents."
    },
    {
        "question": "What are the library timings?",
        "answer": "Library timings depend on the institution. Please check the library notice or official schedule for current timings."
    },
    {
        "question": "How can I borrow a book?",
        "answer": "You can borrow books using your valid student or library identification card."
    },
    {
        "question": "What are the library rules?",
        "answer": "Library users are expected to maintain silence, handle books carefully, return resources on time, and follow the library's borrowing policies."
    },
    {
        "question": "Is WiFi available?",
        "answer": "WiFi availability depends on the institution. If available, students can usually connect using their authorized credentials."
    },
    {
        "question": "How can I reset my password?",
        "answer": "Use the password reset option on the login page. If you still cannot access your account, contact technical support."
    },
    {
        "question": "I forgot my password.",
        "answer": "You can reset your password using the Forgot Password option on the login page."
    },
    {
        "question": "How can I create an account?",
        "answer": "Click the registration or sign-up option and provide the required information to create your account."
    },
    {
        "question": "How can I login?",
        "answer": "Enter your registered email or username and password on the login page."
    },
    {
        "question": "What should I do if I cannot login?",
        "answer": "Check your username and password first. If the problem continues, use password recovery or contact technical support."
    },
    {
        "question": "What is the placement process?",
        "answer": "The placement process generally includes eligibility screening, registration, company assessments, interviews, and selection."
    },
    {
        "question": "How can I register for placements?",
        "answer": "Students can register through the official placement portal or by contacting the placement department."
    },
    {
        "question": "What is the attendance requirement?",
        "answer": "Attendance requirements depend on the institution and academic regulations. Students should maintain the required attendance percentage."
    },
    {
        "question": "How can I check my attendance?",
        "answer": "Attendance can generally be viewed through the student portal or academic management system."
    },
    {
        "question": "How can I contact the administration?",
        "answer": "You can contact the administration through the official office, email, phone number, or student support portal."
    },
    {
        "question": "Where can I find important announcements?",
        "answer": "Important announcements are usually published on the official website, student portal, notice board, or communication channels."
    },
    {
        "question": "Thank you",
        "answer": "You're welcome! I'm happy to help."
    },
    {
        "question": "Hello",
        "answer": "Hello! 👋 How can I help you today?"
    },
    {
        "question": "Hi",
        "answer": "Hi! 👋 Ask me anything related to the available FAQs."
    }
]


# =========================================================
# NLTK NLP PROCESSING
# =========================================================

stemmer = PorterStemmer()

STOP_WORDS = {
    "a",
    "an",
    "the",
    "is",
    "are",
    "am",
    "was",
    "were",
    "be",
    "been",
    "being",
    "to",
    "of",
    "in",
    "on",
    "at",
    "for",
    "from",
    "with",
    "and",
    "or",
    "but",
    "can",
    "could",
    "would",
    "should",
    "do",
    "does",
    "did",
    "how",
    "what",
    "when",
    "where",
    "who",
    "why",
    "which",
    "my",
    "your",
    "our",
    "their",
    "i",
    "me",
    "we",
    "you"
}


def preprocess_text(text):
    """
    NLP preprocessing using NLTK.

    Steps:
    1. Convert text to lowercase
    2. Tokenize using NLTK
    3. Remove punctuation
    4. Remove stop words
    5. Apply stemming using PorterStemmer
    """

    text = text.lower()

    # NLTK tokenization
    tokens = wordpunct_tokenize(text)

    processed_tokens = []

    for token in tokens:

        # Keep alphabetic words only
        if not token.isalpha():
            continue

        # Remove stop words
        if token in STOP_WORDS:
            continue

        # NLTK stemming
        stemmed_word = stemmer.stem(token)

        processed_tokens.append(stemmed_word)

    return " ".join(processed_tokens)


# =========================================================
# PREPROCESS FAQ QUESTIONS
# =========================================================

faq_questions = [
    preprocess_text(faq["question"])
    for faq in FAQS
]


# =========================================================
# TF-IDF VECTORIZATION
# =========================================================

vectorizer = TfidfVectorizer(
    ngram_range=(1, 2)
)

faq_vectors = vectorizer.fit_transform(
    faq_questions
)


# =========================================================
# COSINE SIMILARITY MATCHING
# =========================================================

def find_best_answer(user_question):

    cleaned_question = preprocess_text(
        user_question
    )

    if not cleaned_question:
        return {
            "answer": "Please enter a valid question.",
            "confidence": 0,
            "matched_question": ""
        }

    # Convert user question into TF-IDF vector
    user_vector = vectorizer.transform(
        [cleaned_question]
    )

    # Calculate cosine similarity
    similarity_scores = cosine_similarity(
        user_vector,
        faq_vectors
    )[0]

    # Find highest similarity score
    best_index = similarity_scores.argmax()

    best_score = float(
        similarity_scores[best_index]
    )

    # Convert score to percentage
    confidence = round(
        best_score * 100,
        2
    )

    # Minimum matching threshold
    if best_score < 0.18:

        return {
            "answer": (
                "Sorry, I couldn't find a relevant answer "
                "to your question. Please try asking in a different way."
            ),
            "confidence": confidence,
            "matched_question": ""
        }

    return {
        "answer": FAQS[best_index]["answer"],
        "confidence": confidence,
        "matched_question": FAQS[best_index]["question"]
    }


# =========================================================
# HOME ROUTE
# =========================================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "success": True,
        "message": "FAQBot AI Backend is running!"
    })


# =========================================================
# HEALTH CHECK
# =========================================================

@app.route("/api/health", methods=["GET"])
def health():

    return jsonify({
        "success": True,
        "message": "FAQBot AI API is working",
        "nlp": "NLTK",
        "matching": "TF-IDF + Cosine Similarity",
        "faq_count": len(FAQS)
    })


# =========================================================
# CHAT API
# =========================================================

@app.route("/api/chat", methods=["POST"])
def chat():

    try:

        data = request.get_json()

        if not data:

            return jsonify({
                "success": False,
                "message": "Request body is required."
            }), 400

        user_message = data.get(
            "message",
            ""
        )

        if not isinstance(
            user_message,
            str
        ):

            return jsonify({
                "success": False,
                "message": "Message must be a string."
            }), 400

        user_message = user_message.strip()

        if not user_message:

            return jsonify({
                "success": False,
                "message": "Please enter a question."
            }), 400

        result = find_best_answer(
            user_message
        )

        return jsonify({

            "success": True,

            "question": user_message,

            "answer": result["answer"],

            "confidence": result["confidence"],

            "matched_question": result["matched_question"]

        })

    except Exception as error:

        print(
            "Chat Error:",
            error
        )

        return jsonify({

            "success": False,

            "message":
                "Something went wrong while processing your question."

        }), 500


# =========================================================
# START SERVER
# =========================================================

if __name__ == "__main__":

    print("")
    print("======================================")
    print("🤖 FAQBot AI Backend")
    print("======================================")
    print("🧠 NLP: NLTK Enabled")
    print("🔤 Tokenization: NLTK wordpunct_tokenize")
    print("🌱 Stemming: NLTK PorterStemmer")
    print("📊 TF-IDF: Enabled")
    print("📐 Cosine Similarity: Enabled")
    print(
        "📚 FAQ Knowledge Base:",
        len(FAQS),
        "questions"
    )
    print(
        "🌐 Server: http://127.0.0.1:5002"
    )
    print("======================================")
    print("")

    app.run(
        host="127.0.0.1",
        port=5002,
        debug=True
    )