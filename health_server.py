"""
Simple health check HTTP server for Railway deployment.
Runs in the background while the main ValoRPC app runs.
"""
import threading
import sys
import json

def health_app(environ, start_response):
    """Simple WSGI app that responds to health checks."""
    path = environ.get('PATH_INFO', '/')
    method = environ.get('REQUEST_METHOD', 'GET')
    
    # Health check endpoints
    if path in ('/', '/health'):
        response_body = json.dumps({
            "status": "ok",
            "app": "ValoRPC",
            "version": "0.2.4-alpha"
        }).encode('utf-8')
        status = '200 OK'
        headers = [
            ('Content-Type', 'application/json'),
            ('Content-Length', str(len(response_body)))
        ]
        start_response(status, headers)
        return [response_body]
    
    # Catch all other routes
    response_body = json.dumps({"status": "ok"}).encode('utf-8')
    status = '200 OK'
    headers = [
        ('Content-Type', 'application/json'),
        ('Content-Length', str(len(response_body)))
    ]
    start_response(status, headers)
    return [response_body]

def start_health_server():
    """Start the health check server in a background thread using waitress."""
    try:
        print("[HealthServer] Importing waitress...", file=sys.stderr)
        from waitress import serve
        
        print("[HealthServer] Starting health check server on port 8000...", file=sys.stderr)
        # This will block, but it's in a daemon thread
        serve(health_app, host='0.0.0.0', port=8000, _quiet=True)
        print("[HealthServer] Health server started successfully", file=sys.stderr)
    except ImportError as e:
        print(f"[HealthServer] IMPORT ERROR: {e}", file=sys.stderr)
        print("[HealthServer] waitress not available, skipping health server", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
    except Exception as e:
        print(f"[HealthServer] ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)

def run_in_background():
    """Run the health server in a daemon thread."""
    try:
        print("[HealthServer] Creating daemon thread...", file=sys.stderr)
        thread = threading.Thread(target=start_health_server, daemon=True)
        thread.daemon = True
        thread.start()
        print("[HealthServer] Daemon thread started", file=sys.stderr)
    except Exception as e:
        print(f"[HealthServer] Failed to start daemon thread: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)




