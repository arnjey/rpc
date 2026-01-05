"""
Simple health check HTTP server for Railway deployment.
Runs in the background while the main ValoRPC app runs.
"""
import threading
from flask import Flask, jsonify
import logging

app = Flask(__name__)
logger = logging.getLogger(__name__)

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint for Railway."""
    return jsonify({"status": "ok"}), 200

@app.route('/', methods=['GET'])
def index():
    """Root endpoint for Railway."""
    return jsonify({"app": "ValoRPC", "status": "running"}), 200

def start_health_server():
    """Start the health check server in a background thread."""
    try:
        # Suppress Flask logging
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
        
        app.run(host='0.0.0.0', port=8000, threaded=True)
    except Exception as e:
        logger.error(f"Health server error: {e}")

def run_in_background():
    """Run the health server in a daemon thread."""
    thread = threading.Thread(target=start_health_server, daemon=True)
    thread.start()
    logger.info("Health check server started on port 8000")
