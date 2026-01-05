"""
API Client for sending ValoRPC status updates to Railway API server.
Used by local ValoRPC instance to report game status to the cloud dashboard.
"""
import requests
import json
import os
from datetime import datetime

class ValoRPCAPIClient:
    """Client for communicating with the remote ValoRPC API server."""
    
    def __init__(self, api_url=None):
        """
        Initialize the API client.
        
        Args:
            api_url: Base URL of the ValoRPC API server (e.g., https://web-production-xxxxx.up.railway.app)
                    If not provided, will try to read from VALORPC_API_URL env var
        """
        self.api_url = api_url or os.getenv('VALORPC_API_URL', '').rstrip('/')
        self.enabled = bool(self.api_url)
        
        if self.enabled:
            print(f"[ValoRPC API Client] Initialized with API URL: {self.api_url}")
        else:
            print("[ValoRPC API Client] API URL not configured, status updates disabled")
    
    def update_status(self, status, game="Valorant", details="", state="", user="Unknown"):
        """
        Send a status update to the Railway API server.
        
        Args:
            status: One of 'online', 'idle', 'offline'
            game: Game name (default: Valorant)
            details: What the user is doing (e.g., "In Match - Ascent")
            state: Additional state info
            user: Username
        
        Returns:
            bool: True if update was successful, False otherwise
        """
        if not self.enabled:
            return False
        
        try:
            payload = {
                "status": status,
                "game": game,
                "details": details,
                "state": state,
                "user": user
            }
            
            response = requests.post(
                f"{self.api_url}/api/update",
                json=payload,
                timeout=5
            )
            
            if response.status_code == 200:
                return True
            else:
                print(f"[ValoRPC API Client] Update failed: {response.status_code} - {response.text}")
                return False
        except requests.exceptions.ConnectionError:
            print("[ValoRPC API Client] Connection error: Cannot reach API server")
            return False
        except requests.exceptions.Timeout:
            print("[ValoRPC API Client] Timeout: API server took too long to respond")
            return False
        except Exception as e:
            print(f"[ValoRPC API Client] Error: {e}")
            return False
    
    def set_offline(self, user="Unknown"):
        """Mark user as offline."""
        return self.update_status("offline", details="Not playing", user=user)
    
    def set_idle(self, user="Unknown"):
        """Mark user as idle/away."""
        return self.update_status("idle", details="Away from game", user=user)
    
    def set_playing(self, game_details="In Match", user="Unknown"):
        """Mark user as playing."""
        return self.update_status("online", details=game_details, user=user)

# Example usage:
if __name__ == "__main__":
    # Test the client
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python api_client.py <API_URL> [status] [details]")
        print("Example: python api_client.py https://example.up.railway.app online 'In Match - Ascent'")
        sys.exit(1)
    
    api_url = sys.argv[1]
    status = sys.argv[2] if len(sys.argv) > 2 else "online"
    details = sys.argv[3] if len(sys.argv) > 3 else "Testing"
    
    client = ValoRPCAPIClient(api_url)
    success = client.update_status(status, details=details)
    
    if success:
        print("✓ Status update sent successfully")
    else:
        print("✗ Status update failed")
        sys.exit(1)
