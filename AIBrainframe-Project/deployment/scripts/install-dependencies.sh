#!/bin/bash
# LBOB AI Production Dependencies Installation
# Enterprise-grade system preparation for 24/7 operations

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

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

echo -e "${BLUE}🏭 LBOB AI Production Dependencies Installation${NC}"
echo "=============================================="

# Check if running as root or with sudo
if [[ $EUID -eq 0 ]]; then
    warn "Running as root. Consider using a non-root user for application services."
fi

# Update system packages
log "Updating system packages..."
apt-get update
apt-get upgrade -y

# Install essential packages
log "Installing essential packages..."
apt-get install -y \
    curl \
    wget \
    git \
    software-properties-common \
    apt-transport-https \
    ca-certificates \
    gnupg \
    lsb-release \
    htop \
    iotop \
    nethogs \
    fail2ban \
    ufw \
    logrotate \
    rsyslog \
    cron

# Install Python and development tools
log "Installing Python development environment..."
apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    build-essential \
    libssl-dev \
    libffi-dev \
    libpq-dev

# Install Nginx for reverse proxy
log "Installing Nginx..."
apt-get install -y nginx
systemctl enable nginx

# Install monitoring tools
log "Installing monitoring tools..."
apt-get install -y \
    htop \
    iotop \
    nethogs \
    iftop \
    ncdu \
    tree \
    jq \
    sysstat

# Create LBOB user if it doesn't exist
if ! id "csprinks" &>/dev/null; then
    log "Creating csprinks user for LBOB AI..."
    useradd -m -s /bin/bash csprinks
    usermod -aG sudo csprinks
else
    log "User csprinks already exists"
fi

# Create Ollama user if it doesn't exist
if ! id "ollama" &>/dev/null; then
    log "Creating ollama user for AI service..."
    useradd -r -s /bin/false ollama
    mkdir -p /var/lib/ollama
    chown ollama:ollama /var/lib/ollama
else
    log "User ollama already exists"
fi

# Install Ollama if not present
if ! command -v ollama &> /dev/null; then
    log "Installing Ollama AI service..."
    curl -fsSL https://ollama.ai/install.sh | sh

    # Configure Ollama
    mkdir -p /etc/systemd/system/ollama.service.d
    cat > /etc/systemd/system/ollama.service.d/override.conf << EOF
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
Environment="OLLAMA_MODELS=/var/lib/ollama/models"
EOF

    systemctl daemon-reload
else
    log "Ollama already installed"
fi

# Create necessary directories
log "Creating application directories..."
mkdir -p /opt/aibrainframe_claude
mkdir -p /opt/backups
mkdir -p /var/log/lbob
mkdir -p /var/log/ollama

# Set permissions
chown -R csprinks:csprinks /opt/aibrainframe_claude
chown -R csprinks:csprinks /var/log/lbob
chown -R ollama:ollama /var/log/ollama
chown -R csprinks:csprinks /opt/backups

# Configure firewall
log "Configuring firewall..."
ufw --force enable
ufw default deny incoming
ufw default allow outgoing

# Allow essential services
ufw allow ssh
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw allow 8000/tcp  # LBOB API
ufw allow from 192.168.1.0/24 to any port 11434  # Ollama (internal network only)

log "Firewall rules applied"

# Configure fail2ban
log "Configuring fail2ban..."
cat > /etc/fail2ban/jail.local << EOF
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[sshd]
enabled = true
port = ssh
logpath = /var/log/auth.log

[nginx-http-auth]
enabled = true
port = http,https
logpath = /var/log/nginx/error.log

[nginx-noscript]
enabled = true
port = http,https
logpath = /var/log/nginx/access.log
maxretry = 6

[nginx-badbots]
enabled = true
port = http,https
logpath = /var/log/nginx/access.log
maxretry = 2
EOF

systemctl enable fail2ban
systemctl restart fail2ban

# Configure log rotation
log "Configuring log rotation..."
cat > /etc/logrotate.d/lbob << 'EOF'
/var/log/lbob/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 644 csprinks csprinks
    copytruncate
}

/opt/aibrainframe_claude/logs/*.log {
    daily
    rotate 14
    compress
    delaycompress
    missingok
    notifempty
    create 644 csprinks csprinks
    copytruncate
}
EOF

# Install monitoring dependencies via pip
log "Installing Python monitoring packages..."
pip3 install --upgrade pip
pip3 install psutil requests

# Configure system limits
log "Configuring system limits..."
cat >> /etc/security/limits.conf << EOF

# LBOB AI System Limits
csprinks soft nofile 65536
csprinks hard nofile 65536
csprinks soft nproc 4096
csprinks hard nproc 4096

ollama soft nofile 65536
ollama hard nofile 65536
ollama soft nproc 8192
ollama hard nproc 8192
EOF

# Configure kernel parameters
log "Optimizing kernel parameters..."
cat >> /etc/sysctl.conf << EOF

# LBOB AI Optimizations
net.core.somaxconn = 1024
net.core.netdev_max_backlog = 2000
net.ipv4.tcp_max_syn_backlog = 2048
net.ipv4.tcp_keepalive_time = 600
net.ipv4.tcp_keepalive_intvl = 60
net.ipv4.tcp_keepalive_probes = 3
vm.swappiness = 10
EOF

sysctl -p

# Create backup script
log "Creating backup automation..."
cat > /opt/backups/backup-lbob.sh << 'EOF'
#!/bin/bash
# LBOB AI Automated Backup Script

BACKUP_DIR="/opt/backups"
SOURCE_DIR="/opt/aibrainframe_claude"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="lbob_backup_${TIMESTAMP}"

# Create backup
tar -czf "${BACKUP_DIR}/${BACKUP_NAME}.tar.gz" \
    --exclude="${SOURCE_DIR}/venv" \
    --exclude="${SOURCE_DIR}/.git" \
    --exclude="${SOURCE_DIR}/logs" \
    "${SOURCE_DIR}"

# Keep only last 7 backups
find "${BACKUP_DIR}" -name "lbob_backup_*.tar.gz" -mtime +7 -delete

echo "Backup completed: ${BACKUP_NAME}.tar.gz"
EOF

chmod +x /opt/backups/backup-lbob.sh

# Add backup to crontab
log "Scheduling automated backups..."
(crontab -l 2>/dev/null; echo "0 2 * * * /opt/backups/backup-lbob.sh >> /var/log/lbob/backup.log 2>&1") | crontab -

# Configure rsyslog for centralized logging
log "Configuring centralized logging..."
cat > /etc/rsyslog.d/49-lbob.conf << 'EOF'
# LBOB AI Logging Configuration

# LBOB API logs
:programname, isequal, "lbob-api"          /var/log/lbob/api.log
& stop

# Health Monitor logs
:programname, isequal, "lbob-health-monitor"  /var/log/lbob/health-monitor.log
& stop

# Ollama logs
:programname, isequal, "ollama"            /var/log/ollama/ollama.log
& stop
EOF

systemctl restart rsyslog

# Display installation summary
echo ""
echo -e "${GREEN}🎉 Production dependencies installation complete!${NC}"
echo ""
echo -e "${BLUE}📋 Installation Summary:${NC}"
echo "  ✅ System packages updated"
echo "  ✅ Python development environment"
echo "  ✅ Nginx reverse proxy"
echo "  ✅ Ollama AI service"
echo "  ✅ Monitoring tools"
echo "  ✅ Security configuration (UFW, fail2ban)"
echo "  ✅ Log rotation and centralized logging"
echo "  ✅ Automated backups scheduled"
echo "  ✅ System optimization"
echo ""
echo -e "${BLUE}🔧 Next Steps:${NC}"
echo "  1. Deploy LBOB AI application"
echo "  2. Configure systemd services"
echo "  3. Start health monitoring"
echo "  4. Verify 24/7 operations"
echo ""
echo -e "${YELLOW}⚠️  System Reboot Recommended${NC}"
echo "  Run: sudo reboot"