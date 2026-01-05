"""
Simple health check HTTP server for Railway deployment.
Runs in the background while the main ValoRPC app runs.
"""
import threading
import sys
import time
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint for Railway."""
    return jsonify({"status": "ok", "app": "ValoRPC"}), 200

@app.route('/', methods=['GET'])
def index():
    """Root endpoint for Railway."""
    return jsonify({"app": "ValoRPC", "status": "running", "version": "0.2.4-alpha"}), 200

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors."""
    return jsonify({"status": "ok", "app": "ValoRPC"}), 200

def start_health_server():
    """Start the health check server in a background thread."""
    try:
        # Suppress Flask request logging
        import logging
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
        
        # Use Flask's built-in server but with threading
        # This will run in the background thread
        app.run(
            host='0.0.0.0',
            port=8000,
            debug=False,
            use_reloader=False,
            threaded=True
        )
    except Exception as e:
        print(f"Health server error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()

def run_in_background():
    """Run the health server in a daemon thread."""
    thread = threading.Thread(target=start_health_server, daemon=True)
    thread.daemon = True
    thread.start()
    # Give server a moment to start
    time.sleep(0.5)
    print("Health check server started on port 8000", file=sys.stderr)


