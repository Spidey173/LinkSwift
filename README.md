# 🚀 LinkSwift — URL Shortener API

A lightweight and production-ready URL shortening service built with Flask.  
Supports custom short links, click tracking, and rate limiting.

---

## ✨ Features

- 🔗 Shorten long URLs
- ✏️ Custom short codes (user-defined)
- 📊 Click tracking (analytics)
- ⚡ Rate limiting (10 requests/min)
- 🧠 Clean REST API design
- 🗄️ SQLite database (via SQLAlchemy)
- ❌ Proper error handling

---

## 🧱 Tech Stack

- Python (Flask)
- SQLAlchemy (SQLite)
- Flask-Limiter
- validators

---

## ⚡ Quick Start

```bash
git clone <your-repo-url>
cd link_shortener
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py

Server runs at:

http://localhost:5001


⸻

📡 API Endpoints

Method	Endpoint	Description
GET	/	API info
POST	/shorten	Create short URL
GET	/{code}	Redirect
GET	/info/{code}	Get metadata

👉 Detailed API: API_Documentation.md￼

⸻

🧪 Example

curl -X POST http://localhost:5001/shorten \
-H "Content-Type: application/json" \
-d '{"long_url": "https://google.com"}'


⸻

📂 Project Structure

link_shortener/
├── app.py
├── requirements.txt
├── README.md
├── API_Documentation.md
└── SETUP_GUIDE.md
