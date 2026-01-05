# ValoRPC with Web Dashboard

This setup allows you to check your Valorant game status on your phone anytime, even when your PC is off!

## Architecture

```
Your Gaming PC (Local)          Railway (Cloud)              Your Phone
       ↓                              ↓                           ↓
  ValoRPC detects game  ----→  Flask API Server  ----→   Web Dashboard
  (sends updates every 10s)   (stores game status)   (check anytime, anywhere)
```

## Setup Instructions

### Step 1: Deploy API Server to Railway

1. Go to https://railway.app and create a new project
2. Connect your GitHub repo (already deployed!)
3. The API server will start automatically on Railway
4. Get your Railway URL: `https://web-production-xxxxx.up.railway.app`

### Step 2: Run Local ValoRPC with API Updates

On your gaming PC, create a file `run_valorpc.py`:

```python
import os
from api_client import ValoRPCAPIClient
from vrpc import VRPCMaster

# Set your Railway API URL
os.environ['VALORPC_API_URL'] = 'https://web-production-xxxxx.up.railway.app'

# Initialize API client
api_client = ValoRPCAPIClient()

# Start ValoRPC
vrpc = VRPCMaster()

# Send initial status to API
api_client.set_idle("Your Username")

try:
    vrpc.start_main_thread()
    vrpc.system_tray_app.loop()
except KeyboardInterrupt:
    api_client.set_offline("Your Username")
    print("ValoRPC stopped")
```

Then run:
```bash
python3 run_valorpc.py --always-show
```

### Step 3: Check Status on Your Phone

Simply open your Railway URL on your phone:
```
https://web-production-xxxxx.up.railway.app
```

You'll see:
- ✅ PLAYING (when in game)
- ⏸️ IDLE (when AFK)
- ❌ OFFLINE (when not playing)
- Last updated timestamp
- Game details and state

## API Endpoints

- **`GET /`** - Web dashboard (open on phone)
- **`GET /api/status`** - Get current status (JSON)
- **`POST /api/update`** - Update status (used by local ValoRPC)
- **`GET /health`** - Health check

## Status JSON Format

```json
{
  "status": "online",           // "online", "idle", or "offline"
  "game": "Valorant",
  "details": "In Match - Ascent",
  "state": "Round 5 - 8/8 players",
  "last_updated": "2026-01-06T16:30:45.123456",
  "user": "YourUsername"
}
```

## Example API Usage

```bash
# Send playing update
curl -X POST https://web-production-xxxxx.up.railway.app/api/update \
  -H "Content-Type: application/json" \
  -d '{
    "status": "online",
    "details": "In Match - Ascent",
    "state": "Round 3",
    "user": "YourUsername"
  }'

# Get current status
curl https://web-production-xxxxx.up.railway.app/api/status
```

## Features

✅ Beautiful mobile-friendly dashboard
✅ Real-time status updates
✅ Auto-refresh every 10 seconds  
✅ Works even when PC is off (shows last status)
✅ Simple REST API for custom integrations
✅ No external dependencies beyond Flask

## Customization

You can modify `api_server.py` to:
- Change the color scheme
- Add more status details
- Store updates in a database
- Add authentication
- Send notifications

Enjoy! 🎮
