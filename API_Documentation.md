# 📡 LinkSwift API Documentation

Base URL:

http://localhost:5001

---

## 🏠 1. API Info

**GET** `/`

Returns available endpoints and usage examples.

---

## 🔗 2. Create Short URL

**POST** `/shorten`

### Request
```json
{
  "long_url": "https://example.com",
  "custom_code": "optional123"
}


⸻

Responses

✅ 201 Created

{
  "short_code": "abc123",
  "short_url": "http://localhost:5001/abc123",
  "long_url": "https://example.com",
  "clicks": 0,
  "created_at": "2026-04-06T12:00:00"
}

✅ 200 OK
Returns existing mapping.

❌ 400 Bad Request

{ "error": "Invalid URL format" }

❌ 409 Conflict

{ "error": "Custom code already in use" }

❌ 429 Too Many Requests

{ "error": "Rate limit exceeded. Please try again later." }


⸻

🔄 3. Redirect

GET /{short_code}
	•	Redirects to original URL
	•	Increments click count
	•	Returns 302 Found

❌ 404 Not Found

{ "error": "Short URL not found" }


⸻

📊 4. Get URL Info

GET /info/{short_code}

Response

{
  "short_code": "abc123",
  "short_url": "http://localhost:5001/abc123",
  "long_url": "https://example.com",
  "clicks": 10,
  "created_at": "2026-04-06T12:00:00"
}


⸻

⚙️ Rate Limiting
	•	Endpoint: /shorten
	•	Limit: 10 requests per minute per IP

⸻

⚠️ Error Codes

Code	Meaning
400	Invalid input
404	Not found
409	Conflict
429	Rate limit exceeded


⸻

🧪 Example

curl -X POST http://localhost:5001/shorten \
-H "Content-Type: application/json" \
-d '{"long_url": "https://google.com"}'

---