# 🤖 ARIA — Intelligent AI Chatbot

A modern, responsive, and context-aware conversational AI assistant powered by **Python, Flask, and NLP Vector Embeddings (TF-IDF + Cosine Similarity)**. ARIA handles customer support workflows, general knowledge questions, and multi-turn conversations with a clean, distraction-free interface.

---

## ⚡ Quick Start (Run in 3 Steps)

### 1. Open your terminal and navigate to the project folder
```bash
cd "AI Chatbot"
```

### 2. Install the required dependencies
```bash
pip install -r requirements.txt
```

### 3. Start the application
```bash
python app.py
```

### 4. Open in your browser
Open your browser and visit:
👉 **[http://localhost:5000](http://localhost:5000)** (or `http://127.0.0.1:5000`)

*That's it! ARIA is online and ready to chat.*

---

## ✨ Features

- **🧠 Semantic Vector NLP**: Uses TF-IDF vector embeddings and cosine similarity to understand the *meaning* behind user questions, not just exact keyword matches.
- **💬 Slang & Abbreviation Handling**: Intelligently parses informal text like `"who are u"`, `"hii"`, `"thx"`, `"what can u do"`, and questions with typos.
- **💡 Built-in Knowledge Base**: Accurately explains tech & factual concepts like `"what is java"`, `"what is python"`, `"what is google"`, `"what is AI"`, and `"who is elon musk"`.
- **🎨 Modern Dark / Light Mode UI**: Clean, responsive design inspired by modern conversational AI with ambient background gradients, glassmorphism cards, and quick-reply chips.
- **🔄 Context-Aware Dialogue**: Maintains session memory across conversation turns to deliver natural multi-turn interactions.
- **🛡️ Intelligent Fallback**: Smoothly guides the user when an unrecognized query is encountered rather than failing or giving unrelated answers.
- **📥 Export Transcript**: Download complete conversation logs with one click.
- **🔌 RESTful API**: Clean JSON endpoints ready for integration with mobile apps or external frontends.

---

## 🎯 Supported Capabilities (21 Categories)

ARIA is trained across 21 diverse intent categories:

| Category | Description | Example Query |
| :--- | :--- | :--- |
| **Greeting** | Friendly welcoming | *"Hi", "Hello", "Good morning", "Yo"* |
| **Identity** | Bot identity and background | *"Who are you?", "What's your name?", "Are you a bot?"* |
| **Capabilities** | What ARIA can do | *"What can you do?", "How can you help me?"* |
| **General Knowledge** | Tech and factual definitions | *"What is Java?", "What is Google?", "What is AI?"* |
| **Products & Catalog** | Inquiring about offerings | *"What products do you offer?", "Show me your catalog"* |
| **Pricing** | Rates, costs, and plans | *"How much does it cost?", "Pricing details"* |
| **Order Tracking** | Package status updates | *"Where is my order?", "My order is late"* |
| **Shipping** | Delivery timelines & policies | *"How long does shipping take?", "Do you offer free shipping?"* |
| **Returns & Refunds** | Policy details | *"What is your return policy?", "Can I get a refund?"* |
| **Complaints** | Customer dissatisfaction support | *"I have a complaint", "Bad service", "Item arrived broken"* |
| **Contact Support** | Reaching human agents | *"How can I contact you?", "Customer support phone number"* |
| **Hours** | Availability | *"What are your business hours?", "Are you open 24/7?"* |
| **Entertainment** | Jokes and humor | *"Tell me a joke", "Make me laugh"* |
| **Weather & News** | Daily updates guidance | *"What's the weather today?", "Latest news"* |
| **Assistance** | Help and guidance | *"I need help", "Can you assist me?"* |
| **Gratitude & Farewell** | Courtesies | *"Thank you!", "Thanks a lot", "Goodbye", "See you later"* |

---

## 📁 Project Structure

```text
AI Chatbot/
│
├── app.py                    # Flask server & REST API routes
├── chatbot_engine.py         # Vector NLP engine, intent matcher & knowledge base
├── intents.json              # Structured dataset with 21 intents and patterns
├── requirements.txt          # Python package dependencies
├── README.md                 # Project documentation
│
├── templates/
│   └── index.html            # Responsive chat web interface
│
└── static/
    ├── css/
    │   └── style.css         # Modern dark/light theme styling & animations
    └── js/
        └── chat.js           # Client-side chat logic, session & API integration
```

---

## 🔌 REST API Reference

| Method | Endpoint | Request Body | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | None | Serves the web chat interface |
| `POST` | `/api/chat` | `{"message": "...", "session_id": "..."}` | Sends user message, returns AI response & intent |
| `GET` | `/api/history/<session_id>` | None | Returns conversation transcript for a session |
| `GET` | `/api/intents` | None | Lists all supported intent tags |
| `GET` | `/api/health` | None | Service health status & loaded intents count |

---

## 🛠️ Tech Stack

- **Backend**: Python 3.8+ / Flask / Flask-CORS
- **Natural Language Processing**: NLTK / Scikit-Learn (TF-IDF Vectorizer) / NumPy
- **Frontend**: HTML5 / CSS3 (Custom Variables, Flexbox, Keyframes) / Vanilla JavaScript (ES6+)
- **Typography**: Inter (Google Fonts)

---

## 👤 Author

Developed by **[Vikas](https://github.com/Vikas1267)**.
Feel free to star ⭐ the repository if you found this project helpful!
