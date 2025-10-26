from flask import Flask
from flask_cors import CORS
from config import Config
from models import db
from routes.auth import auth_bp
from routes.leads import leads_bp

app = Flask(__name__)
app.config.from_object(Config)

# Proper CORS config for local frontend
CORS(app, supports_credentials=True)

db.init_app(app)
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(leads_bp, url_prefix="/api/leads")

@app.route("/")
def home():
    return "Flask backend is running!"

if __name__ == "__main__":
    app.run(debug=True)
