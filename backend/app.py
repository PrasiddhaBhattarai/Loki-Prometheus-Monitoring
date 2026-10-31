from flask import Flask
import random, os, time
from prometheus_client import Counter, Histogram, generate_latest
import logging
import logging_loki

app = Flask(__name__)

# For Metircs --------------
# Counter for application errors
error_counter = Counter(
    "app_errors_total",
    "Total no. of app errors"
)
# latency
request_latency = Histogram(
    "app_request_latency_seconds", 
    "Request latency for P90",
    buckets=[0.05, 0.1, 0.25, 0.5, 1, 2, 5]
)

# For Logging, loki ----------------
logger = logging.getLogger("backend")
logger.setLevel(logging.INFO)

# Prevent duplicate logs
logger.propagate = False

# Console logging (Docker logs)
console_handler = logging.StreamHandler()
console_handler.setFormatter(
    logging.Formatter(
        "%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
)
logger.addHandler(console_handler)  

# Loki logging
loki_handler = logging_loki.LokiHandler(
    url=os.getenv(
        "LOKI_URL",
        "http://loki:3100/loki/api/v1/push"
    ),
    tags={"service": "backend"},
    version="1",
)
loki_handler.setFormatter(
    logging.Formatter(
        "%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
)
logger.addHandler(loki_handler)

# simulate app error
def simulate_application_error():
    # 40% chance to simulate an application error (HTTP 500).
    if random.random() < 0.40:
        error_counter.inc()
        raise Exception("Simulated application error!")

# simulate response delay
SLOW_REQUEST_THRESHOLD = 2.0
def simulate_request_delay():
    # Simulate random request latency between 0 and 3 seconds.
    delay = random.uniform(0.0, 3.0)
    time.sleep(delay)

    if delay > SLOW_REQUEST_THRESHOLD:
        logger.warning("Slow request detected: %.2fs", delay)

    return delay

@app.route("/")
@request_latency.time()
def home():
    try:
        simulate_application_error()
        delay = simulate_request_delay()

        logger.info("GET / ok (%.2fs)", delay)
        return "Backend is healthy!", 200

    except Exception as e:
        logger.error("GET / failed: %s", e)
        return str(e), 500

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": "text/plain; charset=utf-8"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)