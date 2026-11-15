"""
chatbot_engine.py — Semantic NLP engine for ARIA chatbot.

HOW IT WORKS (Vector-based understanding):
  1. At startup, every intent pattern is converted into a TF-IDF vector
     (a numeric array where each dimension = a word, value = importance).
  2. When a user sends a message it is ALSO converted into a TF-IDF vector
     in the SAME vector space.
  3. Cosine similarity measures the ANGLE between the user vector and every
     intent vector — the nearest intent (smallest angle / highest similarity)
     is selected. This means semantically similar sentences match even if the
     exact words differ.
  4. A regex pre-pass catches "what is <X>" / "who is <X>" style questions
     and routes them to general_knowledge before the vector step.
  5. Text normalisation expands slang (u→you, thx→thanks, r→are, etc.) so
     informal inputs reach the vector engine in clean form.
"""

import json
import os
import re
import math
import random
from datetime import datetime, timezone

import nltk
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------------------------------------------------------------------
# NLTK bootstrap
# ---------------------------------------------------------------------------
def _ensure_nltk():
    for path, pkg in [
        ("tokenizers/punkt",          "punkt"),
        ("tokenizers/punkt_tab",      "punkt_tab"),
        ("corpora/stopwords",         "stopwords"),
    ]:
        try:
            nltk.data.find(path)
        except LookupError:
            nltk.download(pkg, quiet=True)

_ensure_nltk()

from nltk.corpus import stopwords

# ---------------------------------------------------------------------------
# Slang / abbreviation normalisation table
# ---------------------------------------------------------------------------
_SLANG = {
    r"\bu\b":        "you",
    r"\bur\b":       "your",
    r"\br\b":        "are",
    r"\bwat\b":      "what",
    r"\bwats\b":     "what is",
    r"\bhii+\b":     "hi",
    r"\bheyyy+\b":   "hey",
    r"\bya\b":       "you",
    r"\byep\b":      "yes",
    r"\bnope\b":     "no",
    r"\bgonna\b":    "going to",
    r"\bwanna\b":    "want to",
    r"\bgotta\b":    "got to",
    r"\bthx\b":      "thanks",
    r"\bty\b":       "thank you",
    r"\btysm\b":     "thank you so much",
    r"\bnp\b":       "no problem",
    r"\bpls\b":      "please",
    r"\bplz\b":      "please",
    r"\bok\b":       "okay",
    r"\byup\b":      "yes",
    r"\blol\b":      "",
    r"\blmao\b":     "",
    r"\bomg\b":      "",
    r"\bcant\b":     "cannot",
    r"\bdont\b":     "do not",
    r"\bwont\b":     "will not",
    r"\bim\b":       "i am",
    r"\bive\b":      "i have",
    r"\bill\b":      "i will",
    r"\bcya\b":      "goodbye",
    r"\bttyl\b":     "talk to you later",
    r"\bgn\b":       "good night",
    r"\btc\b":       "take care",
    r"\bbtw\b":      "by the way",
    r"\bfyi\b":      "for your information",
    r"\bimo\b":      "in my opinion",
    r"\bafaik\b":    "as far as i know",
    r"\bw/\b":       "with",
    r"\bw/o\b":      "without",
}

_SLANG_COMPILED = [(re.compile(pat, re.IGNORECASE), rep)
                   for pat, rep in _SLANG.items()]

def _normalize(text: str) -> str:
    """Lowercase, expand slang, remove punctuation, collapse whitespace."""
    text = text.lower().strip()
    for pat, rep in _SLANG_COMPILED:
        text = pat.sub(rep, text)
    text = re.sub(r"[?!.,;:\"]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# ---------------------------------------------------------------------------
# "What is X" / "Who is X" regex pre-classifier
# ---------------------------------------------------------------------------
_GENERAL_KNOWLEDGE_RE = re.compile(
    r"^(what|who|where|when|why|how|define|explain|describe|tell me about|"
    r"meaning of|definition of|what does|what do you know about)\s+.{2,}",
    re.IGNORECASE,
)

# These ARE about ARIA/the bot itself — keep them routed to name intent
_SELF_REFERENCE_RE = re.compile(
    r"\b(aria|you|your name|yourself|bot|robot|ai|assistant|chatbot|"
    r"who made you|who built you|who created you)\b",
    re.IGNORECASE,
)

# Support-domain keywords — if present, don't redirect to general knowledge
_SUPPORT_KEYWORDS_RE = re.compile(
    r"\b(order|orders|price|prices|pricing|cost|costs|rate|rates|fee|fees|charge|charges|"
    r"product|products|item|items|goods|catalog|merchandise|sell|buy|purchase|"
    r"shipping|ship|delivery|deliver|package|track|tracking|"
    r"return|returns|refund|refunds|exchange|policy|"
    r"complaint|complaints|issue|problem|broken|damaged|"
    r"contact|call|phone|email|support|reach|agent|human|"
    r"hour|hours|time|open|close|available|online|"
    r"help|assist|assistance|guide|stuck|"
    r"joke|jokes|funny|laugh|smile|"
    r"reminder|remind|alarm|schedule|"
    r"weather|rain|temperature|forecast|"
    r"news|headline|headlines)\b",
    re.IGNORECASE,
)

# Knowledge dictionary for instant, accurate, logical answers to popular topics
_KNOWLEDGE_BASE = {
    "java": "Java is a popular, class-based, object-oriented programming language designed with 'write once, run anywhere' portability across platforms, widely used in enterprise backends and Android development.",
    "python": "Python is a high-level, interpreted programming language famous for its clean readability and vast ecosystem in AI, machine learning, data science, and web development.",
    "javascript": "JavaScript is the versatile programming language that powers the interactive and dynamic behavior of modern websites, web applications, and backend services (via Node.js).",
    "c++": "C++ is a high-performance, compiled programming language with low-level memory manipulation, widely used in game engines, operating systems, and high-frequency trading.",
    "html": "HTML (HyperText Markup Language) is the standard markup language used to structure web pages and their content on the World Wide Web.",
    "css": "CSS (Cascading Style Sheets) is the style sheet language used to describe the presentation, layout, and visual design of HTML documents.",
    "react": "React is an open-source JavaScript front-end library created by Meta for building dynamic user interfaces based on reusable components.",
    "flask": "Flask is a lightweight Python web framework designed to make getting started quick and easy, with the ability to scale up to complex applications.",
    "django": "Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design with built-in admin, ORM, and auth.",
    "node": "Node.js is an open-source, cross-platform JavaScript runtime environment that allows developers to run JavaScript code outside of a web browser on servers.",
    "api": "An API (Application Programming Interface) is a set of rules and protocols that allows different software applications to communicate and exchange data with each other.",
    "git": "Git is a distributed version control system designed to track changes in source code during software development, enabling collaboration among developers.",
    "github": "GitHub is a cloud-based hosting service and collaboration platform for software development and version control using Git.",
    "google": "Google is a leading global technology company specializing in internet-related services, including search, cloud computing (GCP), online advertising, Android, and artificial intelligence.",
    "amazon": "Amazon is an American multinational technology and e-commerce giant focusing on online retail, cloud computing (AWS), digital streaming, and artificial intelligence.",
    "microsoft": "Microsoft is a global tech leader known for Windows, the Office productivity suite, Azure cloud computing, Xbox gaming, and its investments in AI (OpenAI partnership).",
    "apple": "Apple is a technology company renowned for designing consumer electronics such as the iPhone, Mac, iPad, Apple Watch, and running proprietary operating systems like iOS and macOS.",
    "meta": "Meta (formerly Facebook) is a technology conglomerate that owns Facebook, Instagram, WhatsApp, and focuses on social networking, AI, and immersive VR/AR platforms.",
    "facebook": "Facebook is one of the world's largest social media platforms, connecting billions of people globally, owned by parent company Meta.",
    "twitter": "Twitter (now X) is a microblogging and social networking platform where users post, share, and interact with short messages and multimedia.",
    "openai": "OpenAI is an AI research and deployment organization renowned for creating cutting-edge artificial intelligence models such as GPT-4, ChatGPT, and DALL-E.",
    "chatgpt": "ChatGPT is an advanced conversational AI chatbot developed by OpenAI, trained on vast textual data to understand and generate human-like text.",
    "ai": "Artificial Intelligence (AI) is the simulation of human intelligence processes by computer systems, encompassing learning, reasoning, problem solving, perception, and language understanding.",
    "artificial intelligence": "Artificial Intelligence (AI) is the field of computer science dedicated to creating systems capable of performing tasks that typically require human cognition.",
    "machine learning": "Machine Learning (ML) is a subset of AI focused on developing algorithms that learn from data and improve their performance over time without explicit programming.",
    "deep learning": "Deep Learning is a specialized branch of machine learning based on multi-layered artificial neural networks, enabling breakthroughs in computer vision and natural language processing.",
    "data science": "Data Science is an interdisciplinary field that uses scientific methods, processes, algorithms, and systems to extract actionable knowledge and insights from structured and unstructured data.",
    "cloud computing": "Cloud computing is the on-demand delivery of IT resources over the Internet with pay-as-you-go pricing, including compute power, storage, databases, and networking.",
    "blockchain": "Blockchain is a decentralized, cryptographically secured distributed ledger that immutably records transactions across a network of computers.",
    "bitcoin": "Bitcoin is the first decentralized cryptocurrency, created in 2009 by the pseudonymous Satoshi Nakamoto, operating on a peer-to-peer blockchain without central authority.",
    "cryptocurrency": "Cryptocurrency is a digital or virtual currency that is secured by cryptography, making it nearly impossible to counterfeit or double-spend, often built on blockchain networks.",
    "cybersecurity": "Cybersecurity is the practice of protecting systems, networks, devices, and programs from digital attacks, unauthorized access, and data breaches.",
    "algorithm": "An algorithm is a finite sequence of well-defined, computer-implementable instructions used to solve a specific class of problems or perform computations.",
    "database": "A database is an organized collection of structured information or data, typically stored electronically in a computer system and managed by a DBMS (e.g. PostgreSQL, MySQL, MongoDB).",
    "elon musk": "Elon Musk is a visionary entrepreneur, engineer, and CEO of Tesla, founder and CEO of SpaceX, owner of X (Twitter), and founder of xAI and Neuralink.",
    "bill gates": "Bill Gates is an American business magnate, software developer, and philanthropist who co-founded Microsoft and later established the Bill & Melinda Gates Foundation.",
    "steve jobs": "Steve Jobs was the iconic co-founder and former CEO of Apple Inc., celebrated for revolutionizing personal computing, animated movies (Pixar), and mobile devices (iPhone).",
    "mark zuckerberg": "Mark Zuckerberg is the co-founder, chairman, and CEO of Meta (originally Facebook), which he started while a student at Harvard University.",
    "jeff bezos": "Jeff Bezos is an American entrepreneur and investor who founded Amazon in 1994 and aerospace company Blue Origin.",
}

def _extract_topic(text: str) -> str:
    """Extract candidate topic from questions like 'what is java' or 'explain AI'."""
    text = re.sub(r"[?!.,]", "", text.lower()).strip()
    patterns = [
        r"^(?:what|who|where|when|which)\s+(?:is|are|was|were)\s+(?:\b(?:a|an|the)\b\s*)?(.+)$",
        r"^(?:define|explain|describe|tell me about|meaning of|definition of)\s+(?:\b(?:a|an|the)\b\s*)?(.+)$",
        r"^what\s+does\s+(.+?)\s+mean$",
    ]
    for p in patterns:
        m = re.match(p, text)
        if m:
            return m.group(1).strip()
    return ""


def _is_general_knowledge(raw: str, normalized: str) -> bool:
    """
    Return True if the query looks like a factual/knowledge question that
    isn't about the bot itself or our support domain.
    """
    # If it contains domain keywords, it belongs to customer support
    if _SUPPORT_KEYWORDS_RE.search(normalized):
        return False
    # If it is self-referential, it belongs to the bot
    if _SELF_REFERENCE_RE.search(normalized):
        return False
    # Check if it matches knowledge pattern
    if not _GENERAL_KNOWLEDGE_RE.match(normalized):
        return False
    return True


# ---------------------------------------------------------------------------
# Load intents
# ---------------------------------------------------------------------------
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_INTENTS_PATH = os.path.join(_BASE_DIR, "intents.json")

with open(_INTENTS_PATH, "r", encoding="utf-8") as _f:
    _INTENTS_DATA: list[dict] = json.load(_f)["intents"]

_TAG_TO_INTENT: dict[str, dict] = {i["tag"]: i for i in _INTENTS_DATA}

# ---------------------------------------------------------------------------
# Build TF-IDF vector index
# ---------------------------------------------------------------------------
# Each intent is represented by a DOCUMENT = all its patterns joined together.
# The TF-IDF vectorizer converts every document and every future query into
# the same high-dimensional vector space.  Cosine similarity then finds which
# intent document is geometrically closest to the user's query vector.

_stemmer = PorterStemmer()
_stop_en  = set(stopwords.words("english"))

# Keep question words and personal pronouns — they carry intent signal
_KEEP_WORDS = {
    "what", "who", "where", "when", "why", "how", "which",
    "you", "your", "me", "my", "i", "we", "our",
}

def _stem_tokenise(text: str) -> str:
    """Stem + filter, used as the analyser for TfidfVectorizer."""
    tokens = re.findall(r"[a-z]+", text.lower())
    result = []
    for t in tokens:
        if t in _KEEP_WORDS or t not in _stop_en:
            result.append(_stemmer.stem(t))
    return " ".join(result) if result else text.lower()


# Build corpus: one document per intent (all patterns merged)
_intent_tags: list[str] = []
_corpus:      list[str] = []

for _intent in _INTENTS_DATA:
    if _intent["tag"] == "fallback":
        continue
    _intent_tags.append(_intent["tag"])
    # Combine all patterns into one rich document, then stem
    merged = " ".join(_intent["patterns"])
    _corpus.append(_stem_tokenise(merged))

# Fit the vectorizer on the full corpus
_vectorizer = TfidfVectorizer(
    analyzer="word",
    ngram_range=(1, 2),   # unigrams + bigrams for phrase awareness
    min_df=1,
    sublinear_tf=True,    # log-scaling prevents frequency flooding
)
_intent_matrix = _vectorizer.fit_transform(_corpus)   # shape: (n_intents, vocab)

# ---------------------------------------------------------------------------
# Session storage
# ---------------------------------------------------------------------------
_sessions: dict[str, dict] = {}

def _get_session(session_id: str) -> dict:
    if session_id not in _sessions:
        _sessions[session_id] = {"history": [], "last_intent": None}
    return _sessions[session_id]


# ---------------------------------------------------------------------------
# Core recognition
# ---------------------------------------------------------------------------
FALLBACK_THRESHOLD = 0.08   # below this cosine similarity → fallback

def _recognise(user_message: str) -> tuple[str, float, str]:
    """
    Parse the user message, find nearest intent vector, return
    (tag, confidence, response).
    """
    normalized = _normalize(user_message)

    # --- Pre-pass 1: very short single-word greetings ---
    _greetings = {"hi", "hey", "hello", "yo", "sup", "howdy", "hiya", "hai"}
    if normalized.strip() in _greetings:
        intent = _TAG_TO_INTENT["greeting"]
        return "greeting", 1.0, random.choice(intent["responses"])

    # --- Pre-pass 2: exact match against known intent patterns ---
    for intent in _INTENTS_DATA:
        if intent["tag"] == "fallback":
            continue
        for pattern in intent["patterns"]:
            norm_pattern = _normalize(pattern)
            if normalized == norm_pattern:
                tag = intent["tag"]
                if tag == "general_knowledge":
                    topic = _extract_topic(normalized)
                    if topic in _KNOWLEDGE_BASE:
                        ans = _KNOWLEDGE_BASE[topic] + " 😊 Feel free to ask if you need help with our products, orders, or services!"
                        return "general_knowledge", 1.0, ans
                    for k in sorted(_KNOWLEDGE_BASE.keys(), key=len, reverse=True):
                        if re.search(r"\b" + re.escape(k) + r"\b", topic):
                            ans = _KNOWLEDGE_BASE[k] + " 😊 Let me know if you need any assistance with our support services or products!"
                            return "general_knowledge", 1.0, ans
                return intent["tag"], 1.0, random.choice(intent["responses"])

    # --- Pre-pass 3: general knowledge / educational questions ---
    if _is_general_knowledge(user_message, normalized):
        topic = _extract_topic(normalized)
        if topic in _KNOWLEDGE_BASE:
            ans = _KNOWLEDGE_BASE[topic] + " 😊 Feel free to ask if you need help with our products, orders, or services!"
            return "general_knowledge", 0.98, ans
        
        # Check whole-word topic match in knowledge base (longest keys first)
        for k in sorted(_KNOWLEDGE_BASE.keys(), key=len, reverse=True):
            if re.search(r"\b" + re.escape(k) + r"\b", topic):
                ans = _KNOWLEDGE_BASE[k] + " 😊 Let me know if you need any assistance with our support services or products!"
                return "general_knowledge", 0.96, ans

        # Thoughtful fallback for general knowledge queries
        generic_responses = [
            f"Great question! '{topic or user_message}' is an interesting topic. For detailed technical articles and research, Wikipedia or Google is best. In the meantime, I'm right here if you need help with orders, products, or pricing! 🤖",
            f"I appreciate your curiosity about '{topic or user_message}'! For in-depth encyclopedia knowledge, checking official resources or Wikipedia works best. I'm also here 24/7 for our customer support and product questions. How can I help? 🌟",
        ]
        return "general_knowledge", 0.90, random.choice(generic_responses)

    # --- Vector similarity (TF-IDF + Cosine Distance) ---
    stemmed_query = _stem_tokenise(normalized)
    query_vec = _vectorizer.transform([stemmed_query])
    similarities = cosine_similarity(query_vec, _intent_matrix).flatten()

    best_idx   = int(similarities.argmax())
    best_score = float(similarities[best_idx])
    best_tag   = _intent_tags[best_idx]

    # --- Substring pattern match (boost if clear phrase overlap with word boundary) ---
    for intent in _INTENTS_DATA:
        if intent["tag"] == "fallback":
            continue
        for pattern in intent["patterns"]:
            norm_pattern = _normalize(pattern)
            if len(norm_pattern) >= 4 and re.search(r"\b" + re.escape(norm_pattern) + r"\b", normalized):
                score = 0.90
                if score > best_score:
                    best_score = score
                    best_tag   = intent["tag"]

    # --- Fallback threshold ---
    if best_score < FALLBACK_THRESHOLD:
        fb = _TAG_TO_INTENT.get("fallback", {})
        fb_responses = fb.get("responses", [
            "I'm not sure I understood that fully. Could you rephrase? You can type 'help' or ask about products, orders, shipping, and pricing!"
        ])
        return "fallback", best_score, random.choice(fb_responses)

    intent = _TAG_TO_INTENT[best_tag]
    return best_tag, best_score, random.choice(intent["responses"])


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_response(user_message: str, session_id: str) -> dict:
    """
    Understand the user message and return a response dict.

    Returns:
        {
            "response":   str,
            "intent":     str,
            "confidence": float   (0.0 – 1.0)
        }
    """
    session = _get_session(session_id)
    tag, confidence, response = _recognise(user_message)

    # Context: same intent back-to-back → rotate response to avoid repetition
    if tag == session["last_intent"] and tag not in ("fallback", "general_knowledge"):
        intent = _TAG_TO_INTENT.get(tag, {})
        responses = intent.get("responses", [response])
        if len(responses) > 1:
            response = random.choice(responses)

    session["last_intent"] = tag
    session["history"].append({
        "user":      user_message,
        "bot":       response,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "intent":    tag,
    })

    return {
        "response":   response,
        "intent":     tag,
        "confidence": round(min(confidence, 1.0), 4),
    }


def get_conversation_log(session_id: str) -> list:
    """Return full conversation history for the session."""
    return list(_get_session(session_id)["history"])


def get_all_intents() -> list:
    """Return list of all intent tag strings."""
    return [i["tag"] for i in _INTENTS_DATA]
