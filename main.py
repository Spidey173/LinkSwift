import random
import string
from datetime import datetime

import validators
from flask import Flask, request, redirect, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Rate Limiter - corrected initialization
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"  # Explicitly specify in-memory storage (removes warning)
)
limiter.init_app(app)


# Database Model
class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(2048), nullable=False)
    short_code = db.Column(db.String(16), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    clicks = db.Column(db.Integer, default=0)

    def to_dict(self, base_url):
        return {
            "short_code": self.short_code,
            "short_url": base_url + self.short_code,
            "long_url": self.long_url,
            "clicks": self.clicks,
            "created_at": self.created_at.isoformat()
        }


# Create tables (if not exist)
with app.app_context():
    db.create_all()


# Helper functions
def generate_short_code(length=6):
    """Generate a random, collision‑resistant short code (base62)."""
    chars = string.ascii_letters + string.digits
    for _ in range(5):
        code = ''.join(random.choices(chars, k=length))
        if not URLMap.query.filter_by(short_code=code).first():
            return code
    # Fallback: increase length if collisions persist
    return generate_short_code(length + 1)


def is_valid_custom_code(code):
    """Validate custom code: 4‑16 alphanumeric characters."""
    return 4 <= len(code) <= 16 and code.isalnum()


# Root endpoint - shows API information
@app.route('/', methods=['GET'])
def home():
    """API information and available endpoints."""
    return jsonify({
        "service": "LinkSwift URL Shortener",
        "version": "1.0.0",
        "endpoints": {
            "POST /shorten": {
                "description": "Create a short URL",
                "request_body": {
                    "long_url": "string (required)",
                    "custom_code": "string (optional, 4-16 alphanumeric characters)"
                },
                "rate_limit": "10 requests per minute"
            },
            "GET /{short_code}": {
                "description": "Redirect to original URL",
                "example": "http://localhost:5001/abc123"
            },
            "GET /info/{short_code}": {
                "description": "Get metadata and click count",
                "example": "http://localhost:5001/info/abc123"
            }
        },
        "example_usage": {
            "curl_create": "curl -X POST http://localhost:5001/shorten -H 'Content-Type: application/json' -d '{\"long_url\": \"https://www.example.com\"}'",
            "curl_create_custom": "curl -X POST http://localhost:5001/shorten -H 'Content-Type: application/json' -d '{\"long_url\": \"https://www.example.com\", \"custom_code\": \"mycode\"}'",
            "curl_redirect": "curl -L http://localhost:5001/mycode",
            "curl_info": "curl http://localhost:5001/info/mycode"
        }
    }), 200


# API Endpoints
@app.route('/shorten', methods=['POST'])
@limiter.limit("10 per minute")   # Rate limiting for creation
def shorten_url():
    """
    Create a short URL.
    Expects JSON: {"long_url": "...", "custom_code": "optional"}
    """
    data = request.get_json()
    if not data or 'long_url' not in data:
        return jsonify({"error": "Missing long_url"}), 400

    long_url = data['long_url'].strip()
    custom_code = data.get('custom_code', '').strip() or None

    # Validate long URL
    if not validators.url(long_url):
        return jsonify({"error": "Invalid URL format"}), 400

    # --- Custom code provided ---
    if custom_code:
        if not is_valid_custom_code(custom_code):
            return jsonify({"error": "Custom code must be 4-16 alphanumeric characters"}), 400

        existing = URLMap.query.filter_by(short_code=custom_code).first()
        if existing:
            # If same long URL, return existing entry (no conflict)
            if existing.long_url == long_url:
                return jsonify(existing.to_dict(request.host_url)), 200
            else:
                return jsonify({"error": "Custom code already in use"}), 409

        # Create new mapping with custom code
        new_map = URLMap(long_url=long_url, short_code=custom_code)
        db.session.add(new_map)
        db.session.commit()
        return jsonify(new_map.to_dict(request.host_url)), 201

    # --- No custom code: check for duplicate long URL first ---
    existing = URLMap.query.filter_by(long_url=long_url).first()
    if existing:
        return jsonify(existing.to_dict(request.host_url)), 200

    # Generate new short code
    short_code = generate_short_code()
    new_map = URLMap(long_url=long_url, short_code=short_code)
    db.session.add(new_map)
    db.session.commit()
    return jsonify(new_map.to_dict(request.host_url)), 201


@app.route('/<short_code>', methods=['GET'])
def redirect_to_url(short_code):
    """Redirect to the original long URL and increment click count."""
    url_map = URLMap.query.filter_by(short_code=short_code).first()
    if not url_map:
        return jsonify({"error": "Short URL not found"}), 404

    # Increment click count
    url_map.clicks += 1
    db.session.commit()

    # 302 Found (temporary redirect)
    return redirect(url_map.long_url, 302)


@app.route('/info/<short_code>', methods=['GET'])
def get_info(short_code):
    """Retrieve metadata (including click count) for a short URL."""
    url_map = URLMap.query.filter_by(short_code=short_code).first()
    if not url_map:
        return jsonify({"error": "Short URL not found"}), 404
    return jsonify(url_map.to_dict(request.host_url)), 200


# Custom error handler for rate limiting
@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({"error": "Rate limit exceeded. Please try again later."}), 429


# Custom error handler for 404
@app.errorhandler(404)
def not_found_handler(e):
    return jsonify({"error": "Endpoint not found. Please check the API documentation."}), 404


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)