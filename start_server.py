#!/usr/bin/env python3
"""
Simple startup script for ValoRPC API Server
Usage: python3 start_server.py
"""
import sys
import os
import subprocess

def main():
    print("\n🎮 ValoRPC API Server Startup\n")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return 1
    
    # Check if api_server.py exists
    if not os.path.exists('api_server.py'):
        print("❌ api_server.py not found")
        print("   Make sure you're in the ValoRPC directory")
        return 1
    
    # Try to import Flask
    try:
        import flask
    except ImportError:
        print("⚠️  Dependencies not installed")
        print("   Installing requirements...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=False)
    
    # Start the server
    print("✅ Starting API Server on http://localhost:8000")
    print("")
    print("📱 Open your phone and go to: http://<your-pc-ip>:8000")
    print("💻 Local: http://localhost:8000")
    print("")
    print("Press Ctrl+C to stop")
    print("")
    
    try:
        subprocess.run([sys.executable, 'api_server.py'])
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped")
        return 0
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
