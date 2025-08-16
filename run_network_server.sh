#!/bin/bash

# Sami Deutsch - Network Server Runner
# This script helps you run the Django server accessible from network devices.

echo "🌐 Sami Deutsch - Network Server Runner"
echo "=================================================="
echo

# Check if manage.py exists
if [ ! -f "manage.py" ]; then
    echo "❌ Error: manage.py not found. Please run this script from the Django project root."
    exit 1
fi

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python3 not found. Please install Python3 first."
    exit 1
fi

# Check if Django is installed
if ! python3 -c "import django" &> /dev/null; then
    echo "❌ Error: Django not found. Please install Django first."
    exit 1
fi

echo "✅ Django project found"
echo "✅ Python environment ready"
echo

# Get server configuration
echo "📋 Server Configuration:"
echo "1. Local only (localhost:8000)"
echo "2. Network access (0.0.0.0:8000)"
echo "3. Custom configuration"
echo

read -p "Select option (1-3): " choice

case $choice in
    1)
        host="127.0.0.1"
        port=8000
        echo
        echo "🚀 Starting local server..."
        echo "📍 Access: http://localhost:8000"
        ;;
    2)
        host="0.0.0.0"
        port=8000
        echo
        echo "🚀 Starting network server..."
        echo "📍 Local access: http://localhost:8000"
        echo "🌐 Network access: http://$(hostname -I | awk '{print $1}'):8000"
        echo "🔧 Server binding: 0.0.0.0:8000"
        ;;
    3)
        read -p "Enter host (default: 0.0.0.0): " host
        host=${host:-"0.0.0.0"}
        
        read -p "Enter port (default: 8000): " port_input
        port=${port_input:-8000}
        
        # Validate port number
        if ! [[ "$port" =~ ^[0-9]+$ ]] || [ "$port" -lt 1 ] || [ "$port" -gt 65535 ]; then
            echo "❌ Invalid port number. Using default port 8000."
            port=8000
        fi
        
        echo
        echo "🚀 Starting custom server..."
        echo "🔧 Server binding: $host:$port"
        ;;
    *)
        echo "❌ Invalid choice. Using default network configuration."
        host="0.0.0.0"
        port=8000
        echo
        echo "🚀 Starting network server..."
        ;;
esac

echo
echo "⏹️  Press Ctrl+C to stop the server"
echo

# Run migrations
echo "🔄 Running migrations..."
if python3 manage.py migrate; then
    echo "✅ Migrations completed successfully"
else
    echo "⚠️  Warning: Migrations failed, but continuing..."
fi

echo

# Collect static files
echo "🔄 Collecting static files..."
if python3 manage.py collectstatic --noinput; then
    echo "✅ Static files collected successfully"
else
    echo "⚠️  Warning: Static files collection failed, but continuing..."
fi

echo

# Start Django server
echo "🚀 Starting Django server..."
python3 manage.py runserver "$host:$port"

echo
echo "🛑 Server stopped"
