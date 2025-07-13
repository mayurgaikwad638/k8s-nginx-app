from flask import Flask
from flask_cors import CORS  # ✅ Add this
import os
import time

app = Flask(__name__)
CORS(app)  # ✅ Enable CORS for all routes

message = os.getenv("APP_MESSAGE", "Hello from the Backend API!")

@app.route("/")
def home():
    return message

@app.route("/health")
def health():
    return "OK", 200

@app.route("/ready")
def ready():
    return "Ready", 200

if __name__ == "__main__":
    time.sleep(5)
    app.run(host="0.0.0.0", port=5000)
