"""
Simple health check HTTP server for Railway deployment.
Runs in the background while the main ValoRPC app runs.
"""
import threading
import logging
from flask import Flask, jsonify
from werkzeug.serving import make_server

# Set up logging
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Suppress Flask request logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint for Railway."""
    return jsonify({"status": "ok", "app": "ValoRPC"}), 200

@app.route('/', methods=['GET'])
def index():
    """Root endpoint for Railway."""
    return jsonify({"app": "ValoRPC", "status": "running", "version": "0.2.4-alpha"}), 200

def start_health_server():
    """Start the health check server in a background thread."""
    try:
        # Use werkzeug server instead of Flask's development server
        server = make_server('0.0.0.0', 8000, app, threaded=True)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        logger.info("Health check server started on port 8000")
    except Exception as e:
        logger.error(f"Health server failed to start: {e}")
        import traceback
        logger.error(traceback.format_exc())

def run_in_background():
    """Run the health server in a daemon thread."""
    start_health_server()

