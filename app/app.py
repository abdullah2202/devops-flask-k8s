from flask import Flask, request, jsonify
from prometheus_client import Counter, generate_latest, CollectorRegistry, Gauge
import time

app = Flask(__name__)

# Isolate the metrics
REGISTRY = CollectorRegistry(auto_describe=True)

# Counter for tracking total requests
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP Requests',
    ['method', 'endpoint', 'http_status'],
    registry=REGISTRY
)

# Gauge for application uptime
UPTIME_GAUGE = Gauge(
    'app_uptime_seconds',
    'Application uptime in seconds',
    registry=REGISTRY
)
START_TIME = time.time()

@app.route('/')
def home():
    REQUEST_COUNT.labels('GET', '/', 200).inc()
    return "Hello World!\n"

@app.route('/health')
def health():
    REQUEST_COUNT.labels('GET', '/health', 200).inc()
    return jsonify({"status": "healthy"}), 200

@app.route('/metrics') # Prometheus endpoint for metrics
def metrics():
    UPTIME_GAUGE.set(time.time() - START_TIME)
    
    # Return in Prometheus format
    return generate_latest(REGISTRY), 200, {'Content-Type': 'text/plain; version=0.0.4; charset=utf-8'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)