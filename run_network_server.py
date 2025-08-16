#!/usr/bin/env python3
"""
Network Server Runner for Sami Deutsch
This script helps you run the Django server accessible from network devices.
"""

import os
import sys
import socket
import subprocess
from pathlib import Path

def get_local_ip():
    """Get local IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "127.0.0.1"

def check_django_project():
    """Check if we're in a Django project directory"""
    if not Path("manage.py").exists():
        print("❌ Error: manage.py not found. Please run this script from the Django project root.")
        return False
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import django
        print(f"✅ Django {django.get_version()} found")
        return True
    except ImportError:
        print("❌ Error: Django not found. Please install Django first.")
        return False

def run_migrations():
    """Run Django migrations"""
    print("🔄 Running migrations...")
    try:
        subprocess.run([sys.executable, "manage.py", "migrate"], check=True)
        print("✅ Migrations completed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Error: Failed to run migrations")
        return False

def collect_static():
    """Collect static files"""
    print("🔄 Collecting static files...")
    try:
        subprocess.run([sys.executable, "manage.py", "collectstatic", "--noinput"], check=True)
        print("✅ Static files collected successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Error: Failed to collect static files")
        return False

def start_server(host="0.0.0.0", port=8000):
    """Start Django development server"""
    local_ip = get_local_ip()
    
    print(f"\n🚀 Starting Django server...")
    print(f"📍 Local access: http://localhost:{port}")
    print(f"🌐 Network access: http://{local_ip}:{port}")
    print(f"🔧 Server binding: {host}:{port}")
    print(f"⏹️  Press Ctrl+C to stop the server\n")
    
    try:
        # Start Django server
        subprocess.run([
            sys.executable, "manage.py", "runserver", f"{host}:{port}"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

def main():
    """Main function"""
    print("🌐 Sami Deutsch - Network Server Runner")
    print("=" * 50)
    
    # Check if we're in a Django project
    if not check_django_project():
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Get server configuration
    print("\n📋 Server Configuration:")
    print("1. Local only (localhost:8000)")
    print("2. Network access (0.0.0.0:8000)")
    print("3. Custom configuration")
    
    choice = input("\nSelect option (1-3): ").strip()
    
    if choice == "1":
        host = "127.0.0.1"
        port = 8000
    elif choice == "2":
        host = "0.0.0.0"
        port = 8000
    elif choice == "3":
        host = input("Enter host (default: 0.0.0.0): ").strip() or "0.0.0.0"
        port_input = input("Enter port (default: 8000): ").strip() or "8000"
        try:
            port = int(port_input)
        except ValueError:
            print("❌ Invalid port number. Using default port 8000.")
            port = 8000
    else:
        print("❌ Invalid choice. Using default network configuration.")
        host = "0.0.0.0"
        port = 8000
    
    # Run migrations
    if not run_migrations():
        print("⚠️  Warning: Migrations failed, but continuing...")
    
    # Collect static files
    if not collect_static():
        print("⚠️  Warning: Static files collection failed, but continuing...")
    
    # Start server
    start_server(host, port)

if __name__ == "__main__":
    main()
