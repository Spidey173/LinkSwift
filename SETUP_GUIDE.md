
# 🛠️ Setup Guide — LinkSwift

Follow these steps to run the project locally.

---

## 📋 Prerequisites

- Python 3.9+
- pip

---

## 📥 Installation

```bash
git clone <your-repo-url>
cd link_shortener


⸻

🧪 Create Virtual Environment

python -m venv venv

Activate:
	•	Windows:

venv\Scripts\activate

	•	Mac/Linux:

source venv/bin/activate


⸻

📦 Install Dependencies

pip install -r requirements.txt


⸻

▶️ Run Server

python app.py

Server runs at:

http://localhost:5001


⸻

🧪 Test API

Create URL

curl -X POST http://localhost:5001/shorten \
-H "Content-Type: application/json" \
-d '{"long_url": "https://google.com"}'


⸻

Redirect

curl -L http://localhost:5001/abc123


⸻

Get Info

curl http://localhost:5001/info/abc123


⸻

🗄️ Database
	•	SQLite DB file: urls.db

⸻

⚠️ Troubleshooting

Issue	Fix
Module not found	Install requirements
Port in use	Change port
App not starting	Restart server


⸻