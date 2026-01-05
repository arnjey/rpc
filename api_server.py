"""
ValoRPC Status API Server for Railway deployment.
Receives game status updates from local ValoRPC and displays them on a web dashboard.
"""
from flask import Flask, jsonify, request, render_template_string
import json
import os
from datetime import datetime
from threading import Lock

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Get port from environment (Railway sets this)
PORT = int(os.environ.get('PORT', 8000))
HOST = os.environ.get('HOST', '0.0.0.0')

# In-memory status storage (persists while container is running)
status_lock = Lock()
current_status = {
    "status": "offline",
    "game": "Valorant",
    "details": "Not running",
    "state": "Waiting for connection...",
    "last_updated": None,
    "user": "Unknown"
}

# HTML Dashboard Template
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ValoRPC Status Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 500px;
            width: 100%;
            padding: 40px;
            text-align: center;
        }
        .header {
            margin-bottom: 30px;
        }
        .header h1 {
            font-size: 28px;
            color: #333;
            margin-bottom: 10px;
        }
        .header p {
            color: #666;
            font-size: 14px;
        }
        .status-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 25px;
        }
        .status-indicator {
            width: 20px;
            height: 20px;
            border-radius: 50%;
            display: inline-block;
            margin-right: 10px;
            animation: pulse 2s infinite;
        }
        .status-indicator.online {
            background-color: #4ade80;
            box-shadow: 0 0 10px #4ade80;
        }
        .status-indicator.offline {
            background-color: #ef4444;
        }
        .status-indicator.idle {
            background-color: #f59e0b;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        .status-text {
            font-size: 18px;
            font-weight: 600;
            margin-top: 15px;
        }
        .game-info {
            background: #f5f5f5;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            text-align: left;
        }
        .info-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid #e0e0e0;
        }
        .info-row:last-child {
            border-bottom: none;
        }
        .info-label {
            color: #666;
            font-size: 14px;
            font-weight: 500;
        }
        .info-value {
            color: #333;
            font-size: 15px;
            font-weight: 600;
            word-break: break-word;
            text-align: right;
            flex: 1;
            margin-left: 10px;
        }
        .timestamp {
            font-size: 12px;
            color: #999;
            margin-top: 15px;
        }
        .refresh-btn {
            background: #667eea;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.3s;
        }
        .refresh-btn:hover {
            background: #764ba2;
        }
        .api-info {
            background: #f0f0f0;
            border-radius: 10px;
            padding: 15px;
            margin-top: 20px;
            font-size: 12px;
            color: #666;
            text-align: left;
        }
        .api-info code {
            background: white;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            color: #d63031;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎮 ValoRPC Status</h1>
            <p>Check your Valorant game status anytime</p>
        </div>

        <div class="status-card" id="statusCard">
            <div>
                <span class="status-indicator" id="statusIndicator"></span>
                <strong id="statusLabel">Loading...</strong>
            </div>
            <div class="status-text" id="statusText"></div>
        </div>

        <div class="game-info" id="gameInfo">
            <div class="info-row">
                <span class="info-label">Game</span>
                <span class="info-value" id="gameValue">-</span>
            </div>
            <div class="info-row">
                <span class="info-label">Status</span>
                <span class="info-value" id="detailsValue">-</span>
            </div>
            <div class="info-row">
                <span class="info-label">Details</span>
                <span class="info-value" id="stateValue">-</span>
            </div>
            <div class="timestamp" id="timestamp">Last updated: never</div>
        </div>

        <button class="refresh-btn" onclick="loadStatus()">Refresh Status</button>

        <div class="api-info">
            <strong>📱 How to use:</strong><br>
            • Open this link on your phone<br>
            • Check your Valorant status anytime<br>
            • Auto-refreshes every 10 seconds<br>
            <code>/api/status</code> for JSON data
        </div>
    </div>

    <script>
        async function loadStatus() {
            try {
                const response = await fetch('/api/status');
                const data = await response.json();
                
                // Update status indicator and label
                const statusCard = document.getElementById('statusCard');
                const indicator = document.getElementById('statusIndicator');
                const label = document.getElementById('statusLabel');
                const text = document.getElementById('statusText');
                
                // Remove all classes
                statusCard.className = 'status-card';
                indicator.className = 'status-indicator';
                
                // Update based on status
                if (data.status === 'online') {
                    statusCard.style.background = 'linear-gradient(135deg, #4ade80 0%, #22c55e 100%)';
                    indicator.classList.add('online');
                    label.textContent = 'PLAYING';
                    text.textContent = data.details || 'Valorant';
                } else if (data.status === 'idle') {
                    statusCard.style.background = 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)';
                    indicator.classList.add('idle');
                    label.textContent = 'IDLE';
                    text.textContent = data.details || 'Away from game';
                } else {
                    statusCard.style.background = 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)';
                    indicator.classList.add('offline');
                    label.textContent = 'OFFLINE';
                    text.textContent = data.details || 'Not playing';
                }
                
                // Update info
                document.getElementById('gameValue').textContent = data.game || 'Valorant';
                document.getElementById('detailsValue').textContent = data.details || 'N/A';
                document.getElementById('stateValue').textContent = data.state || 'N/A';
                
                // Update timestamp
                if (data.last_updated) {
                    const time = new Date(data.last_updated);
                    document.getElementById('timestamp').textContent = `Last updated: ${time.toLocaleTimeString()}`;
                } else {
                    document.getElementById('timestamp').textContent = 'Last updated: never';
                }
            } catch (error) {
                console.error('Error loading status:', error);
                document.getElementById('statusText').textContent = 'Connection error';
            }
        }
        
        // Load on page load
        loadStatus();
        
        // Auto-refresh every 10 seconds
        setInterval(loadStatus, 10000);
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def dashboard():
    """Serve the web dashboard."""
    return render_template_string(DASHBOARD_HTML)

@app.route('/api/status', methods=['GET'])
def get_status():
    """API endpoint to get current status."""
    with status_lock:
        return jsonify(current_status)

@app.route('/api/update', methods=['POST'])
def update_status():
    """API endpoint for ValoRPC to send updates."""
    global current_status
    
    try:
        data = request.get_json()
        
        with status_lock:
            current_status.update({
                "status": data.get("status", current_status["status"]),
                "game": data.get("game", current_status["game"]),
                "details": data.get("details", current_status["details"]),
                "state": data.get("state", current_status["state"]),
                "user": data.get("user", current_status["user"]),
                "last_updated": datetime.now().isoformat()
            })
        
        return jsonify({
            "success": True,
            "message": "Status updated",
            "current_status": current_status
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok", "service": "ValoRPC API"}), 200

@app.route('/', methods=['POST'])
def root_post():
    """Catch-all for POST requests."""
    return get_status()

if __name__ == '__main__':
    # Production: use waitress with environment PORT
    try:
        from waitress import serve
        print(f"[ValoRPC API] Starting server on {HOST}:{PORT}")
        serve(app, host=HOST, port=PORT, _quiet=False)
    except ImportError as e:
        print(f"[ValoRPC API] Warning: waitress not available ({e})")
        print(f"[ValoRPC API] Using Flask development server")
        app.run(host=HOST, port=PORT, debug=False, threaded=True)
    except Exception as e:
        print(f"[ValoRPC API] CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
