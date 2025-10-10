import os
import logging
from flask import Flask, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter, Histogram

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ecommerce.db"
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize the app with the extension
db.init_app(app)

@app.template_filter('currency')
def currency_format(amount):
    """Format currency for Kenyan Shillings with commas"""
    return f"KES {amount:,.0f}"

with app.app_context():
    # Import models to ensure tables are created
    import models
    db.create_all()
    
    # Initialize sample data if needed
    from utils import init_sample_data
    init_sample_data()

# Import routes after app initialization
import routes
import admin

# ------------------------------
# ✅ Prometheus metrics section
# ------------------------------
REQUEST_COUNT = Counter(
    'app_requests_total', 
    'Total number of HTTP requests handled by the app'
)

REQUEST_LATENCY = Histogram(
    'app_request_latency_seconds', 
    'Request latency (seconds)'
)

@app.before_request
def before_request():
    REQUEST_COUNT.inc()

@app.route('/metrics')
def metrics():
    """Expose Prometheus metrics"""
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
