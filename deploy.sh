#!/bin/bash
# Deployment script for Sami Deutsch
# Usage: ./deploy.sh

set -e  # Exit on error

echo "🚀 Starting deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
PROJECT_DIR="/home/sami/sami_deutsch"
VENV_DIR="$PROJECT_DIR/venv"
SERVICE_NAME="samideutsch"

# Functions
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Check if running as correct user
if [ "$USER" != "sami" ]; then
    print_error "This script should be run as 'sami' user"
    exit 1
fi

# Navigate to project directory
cd $PROJECT_DIR || exit 1

# Activate virtual environment
print_warning "Activating virtual environment..."
source $VENV_DIR/bin/activate

# Pull latest code
print_warning "Pulling latest code..."
git pull origin main || {
    print_error "Failed to pull code"
    exit 1
}
print_success "Code updated"

# Install/update dependencies
print_warning "Installing dependencies..."
pip install -r requirements.txt --quiet || {
    print_error "Failed to install dependencies"
    exit 1
}
print_success "Dependencies installed"

# Run migrations
print_warning "Running migrations..."
python manage.py migrate --noinput || {
    print_error "Migrations failed"
    exit 1
}
print_success "Migrations completed"

# Collect static files
print_warning "Collecting static files..."
python manage.py collectstatic --noinput --clear || {
    print_error "Failed to collect static files"
    exit 1
}
print_success "Static files collected"

# Check .env file exists
if [ ! -f "$PROJECT_DIR/.env" ]; then
    print_error ".env file not found!"
    print_warning "Please create .env file with required settings"
    exit 1
fi

# Test Django configuration
print_warning "Testing Django configuration..."
python manage.py check --deploy || {
    print_error "Django check failed"
    exit 1
}
print_success "Django configuration OK"

# Restart Gunicorn service
print_warning "Restarting Gunicorn service..."
sudo systemctl restart $SERVICE_NAME || {
    print_error "Failed to restart service"
    exit 1
}

# Wait a moment for service to start
sleep 2

# Check service status
if sudo systemctl is-active --quiet $SERVICE_NAME; then
    print_success "Service is running"
else
    print_error "Service is not running"
    sudo systemctl status $SERVICE_NAME
    exit 1
fi

# Reload Nginx (if needed)
print_warning "Reloading Nginx..."
sudo nginx -t && sudo systemctl reload nginx || {
    print_error "Nginx reload failed"
    exit 1
}
print_success "Nginx reloaded"

# Final checks
print_warning "Running final checks..."

# Check if site is responding
if curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000 | grep -q "200\|301\|302"; then
    print_success "Site is responding"
else
    print_warning "Site might not be responding correctly"
fi

# Display service status
echo ""
print_success "Deployment completed!"
echo ""
echo "Service status:"
sudo systemctl status $SERVICE_NAME --no-pager -l
echo ""
echo "Recent logs:"
tail -n 10 $PROJECT_DIR/logs/django.log 2>/dev/null || echo "No logs found"
echo ""
print_warning "Don't forget to:"
echo "  - Check logs: tail -f $PROJECT_DIR/logs/django.log"
echo "  - Check security logs: tail -f $PROJECT_DIR/logs/security.log"
echo "  - Test the website: https://yourdomain.com"






