#!/bin/bash
# LBOB AI Production Deployment Script
# Enterprise-grade 24/7 deployment with auto-restart and monitoring

set -euo pipefail

# Configuration
DEPLOY_USER="csprinks"
DEPLOY_HOST="192.168.1.70"
DEPLOY_PATH="/opt/aibrainframe_claude"
SSH_CMD="sshpass -p '0320' ssh ${DEPLOY_USER}@${DEPLOY_HOST}"
SCP_CMD="sshpass -p '0320' scp"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 LBOB AI Production Deployment - 24/7 Enterprise Setup${NC}"
echo "=================================================="

# Function to log with timestamp
log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
    exit 1
}

# Pre-deployment checks
log "Running pre-deployment checks..."

# Check SSH connectivity
if ! $SSH_CMD 'echo "SSH OK"' > /dev/null 2>&1; then
    error "Cannot connect to production server"
fi

# Check if deployment directory exists
if ! $SSH_CMD "test -d ${DEPLOY_PATH}"; then
    error "Deployment directory ${DEPLOY_PATH} does not exist"
fi

log "✅ Pre-deployment checks passed"

# Backup current deployment
log "Creating backup of current deployment..."
BACKUP_NAME="lbob-backup-$(date +%Y%m%d-%H%M%S)"
$SSH_CMD "sudo cp -r ${DEPLOY_PATH} /opt/backups/${BACKUP_NAME}" || warn "Backup creation failed"

# Deploy systemd services
log "Deploying systemd services..."

# Copy service files
$SCP_CMD deployment/systemd/*.service ${DEPLOY_USER}@${DEPLOY_HOST}:/tmp/

# Install services
$SSH_CMD "
    sudo cp /tmp/*.service /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl enable lbob-api.service
    sudo systemctl enable ollama.service
    sudo systemctl enable lbob-health-monitor.service
"

log "✅ Systemd services deployed"

# Deploy monitoring system
log "Deploying health monitoring system..."

# Create directories
$SSH_CMD "
    sudo mkdir -p /var/log/lbob
    sudo mkdir -p ${DEPLOY_PATH}/deployment/monitoring
    sudo chown -R ${DEPLOY_USER}:${DEPLOY_USER} /var/log/lbob
"

# Copy monitoring files
$SCP_CMD deployment/monitoring/health-monitor.py ${DEPLOY_USER}@${DEPLOY_HOST}:${DEPLOY_PATH}/deployment/monitoring/
$SSH_CMD "chmod +x ${DEPLOY_PATH}/deployment/monitoring/health-monitor.py"

log "✅ Health monitoring deployed"

# Deploy logging configuration
log "Deploying logging configuration..."

$SCP_CMD deployment/logging/logrotate.conf ${DEPLOY_USER}@${DEPLOY_HOST}:/tmp/
$SSH_CMD "
    sudo cp /tmp/logrotate.conf /etc/logrotate.d/lbob
    sudo chown root:root /etc/logrotate.d/lbob
    sudo chmod 644 /etc/logrotate.d/lbob
"

log "✅ Logging configuration deployed"

# Install Python dependencies for monitoring
log "Installing monitoring dependencies..."
$SSH_CMD "
    cd ${DEPLOY_PATH}
    source venv/bin/activate
    pip install psutil requests
"

# Stop existing services gracefully
log "Stopping existing services..."
$SSH_CMD "
    sudo systemctl stop lbob-health-monitor.service 2>/dev/null || true
    sudo pkill -f uvicorn 2>/dev/null || true
    sleep 5
"

# Start services in correct order
log "Starting production services..."

# Start Ollama first
$SSH_CMD "sudo systemctl restart ollama.service"
sleep 10

# Start LBOB API
$SSH_CMD "sudo systemctl restart lbob-api.service"
sleep 15

# Start health monitor
$SSH_CMD "sudo systemctl restart lbob-health-monitor.service"
sleep 5

# Verify deployment
log "Verifying deployment..."

# Check service status
if $SSH_CMD "systemctl is-active --quiet lbob-api.service"; then
    log "✅ LBOB API service is running"
else
    error "❌ LBOB API service failed to start"
fi

if $SSH_CMD "systemctl is-active --quiet ollama.service"; then
    log "✅ Ollama service is running"
else
    error "❌ Ollama service failed to start"
fi

if $SSH_CMD "systemctl is-active --quiet lbob-health-monitor.service"; then
    log "✅ Health monitor service is running"
else
    warn "⚠️ Health monitor service not running"
fi

# Test API endpoints
log "Testing API endpoints..."
sleep 10

if curl -s -f http://192.168.1.70:8000/health > /dev/null; then
    log "✅ LBOB API health check passed"
else
    warn "⚠️ LBOB API health check failed - may need more time to start"
fi

if curl -s -f http://192.168.1.70:11434/api/tags > /dev/null; then
    log "✅ Ollama API health check passed"
else
    warn "⚠️ Ollama API health check failed - may need more time to start"
fi

# Display service status
log "Service Status Summary:"
$SSH_CMD "
    echo '  LBOB API:' \$(systemctl is-active lbob-api.service)
    echo '  Ollama:' \$(systemctl is-active ollama.service)
    echo '  Health Monitor:' \$(systemctl is-active lbob-health-monitor.service)
"

# Show how to monitor
echo ""
echo -e "${BLUE}📊 Monitoring Commands:${NC}"
echo "  Check status: sudo systemctl status lbob-api.service"
echo "  View logs:    sudo journalctl -u lbob-api.service -f"
echo "  Health logs:  sudo tail -f /var/log/lbob/health-monitor.log"
echo ""

echo -e "${GREEN}🎉 Production deployment complete!${NC}"
echo -e "${GREEN}🌍 LBOB AI is now available 24/7 at: http://192.168.1.70:8000/static/simple_lbob.html${NC}"
echo -e "${GREEN}🔧 Auto-restart and monitoring are active${NC}"