from flask import Flask
from prometheus_client import Counter, generate_latest
import random, os

app = Flask(__name__)
error_counter = Counter("app_errors_total", "Total frontend errors")

@app.route("/")
def home():
    if random.random() < 0.1:
        error_counter.inc()
        return "Frontend error!", 500
    return "Frontend OK!"

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": "text/plain; charset=utf-8"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)