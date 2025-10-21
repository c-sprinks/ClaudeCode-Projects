# 🏭 LBOB AI Production Deployment Guide
## Enterprise-Grade 24/7 Operations with Auto-Restart & Monitoring

**Version:** 1.0
**Date:** 2025-10-20
**Target:** Dell PowerEdge R520 (192.168.1.70)
**Uptime Goal:** 99.9% (8.76 hours downtime/year)

---

## 📋 **DEPLOYMENT OVERVIEW**

### **System Architecture**
```
┌─────────────────────────────────────────────────────────────┐
│                    LBOB AI Production Stack                │
├─────────────────────────────────────────────────────────────┤
│  🌐 Nginx (Port 80) → Load Balancer & Rate Limiting       │
│  ⚡ LBOB API (Port 8000) → FastAPI with Auto-Restart      │
│  🤖 Ollama AI (Port 11434) → LLM Service with Monitoring  │
│  📊 Health Monitor → 24/7 System Monitoring & Recovery    │
│  📝 Centralized Logging → Structured logs with rotation   │
│  🔄 Automated Backups → Daily backups with retention      │
└─────────────────────────────────────────────────────────────┘
```

### **Industry Standards Implemented**
- ✅ **Systemd Services**: Auto-restart, dependency management, resource limits
- ✅ **Health Monitoring**: 30-second checks with automated recovery
- ✅ **Load Balancing**: Nginx reverse proxy with failover
- ✅ **Security**: Firewall, fail2ban, rate limiting, service isolation
- ✅ **Logging**: Structured logs with rotation and centralized collection
- ✅ **Backups**: Automated daily backups with 7-day retention
- ✅ **Monitoring**: Resource utilization, performance metrics, alerting

---

## 🚀 **QUICK DEPLOYMENT**

### **Prerequisites**
- Ubuntu Server 20.04+ or Debian 11+
- Minimum 8GB RAM (for AI model)
- 50GB+ available disk space
- Root or sudo access
- Network connectivity

### **One-Command Deployment**
```bash
# Clone repository and run deployment
git clone https://github.com/c-sprinks/ClaudeCode-Projects.git
cd ClaudeCode-Projects/AIBrainframe-Project
sudo deployment/scripts/install-dependencies.sh
./deployment/scripts/deploy-production.sh
```

### **Verification**
```bash
# Check all services
sudo systemctl status lbob-api ollama lbob-health-monitor

# Test endpoints
curl http://192.168.1.70:8000/health
curl http://192.168.1.70:8000/static/simple_lbob.html

# Monitor logs
sudo journalctl -u lbob-api -f
```

---

## 🔧 **DETAILED DEPLOYMENT STEPS**

### **Step 1: System Preparation**
```bash
# Run dependency installer (as root)
sudo ./deployment/scripts/install-dependencies.sh
```

**What it installs:**
- System packages and security tools
- Python development environment
- Nginx reverse proxy
- Ollama AI service
- Monitoring and logging tools
- Firewall and security configuration

### **Step 2: Deploy Services**
```bash
# Deploy LBOB AI services
./deployment/scripts/deploy-production.sh
```

**What it deploys:**
- Systemd service configurations
- Health monitoring system
- Log rotation and management
- Nginx configuration
- Application files and dependencies

### **Step 3: Verify Deployment**
```bash
# Check service status
sudo systemctl status lbob-api
sudo systemctl status ollama
sudo systemctl status lbob-health-monitor

# Test API endpoints
curl -f http://localhost:8000/health
curl -f http://localhost:11434/api/tags

# Access LBOB interface
curl -f http://localhost:8000/static/simple_lbob.html
```

---

## 🔄 **AUTO-RESTART CONFIGURATION**

### **Systemd Service Features**
Each service includes enterprise-grade restart policies:

**LBOB API Service (`lbob-api.service`):**
- `Restart=always` - Automatic restart on failure
- `RestartSec=10` - 10-second delay between restarts
- `WatchdogSec=30` - Health monitoring every 30 seconds
- Resource limits and security isolation

**Ollama Service (`ollama.service`):**
- `Restart=always` - Automatic restart on failure
- `RestartSec=15` - 15-second delay for AI model loading
- `TimeoutStartSec=120` - Extended startup time for AI models
- Memory limits appropriate for AI workloads

**Health Monitor (`lbob-health-monitor.service`):**
- Monitors both LBOB API and Ollama services
- Automated restart on consecutive failures
- Cooldown periods to prevent restart loops
- Comprehensive logging and alerting

### **Restart Triggers**
Services automatically restart on:
- Process crashes or exits
- Memory exhaustion
- Network connectivity issues
- Health check failures (3 consecutive failures)
- System reboot (services auto-start)

### **Manual Service Management**
```bash
# Start services
sudo systemctl start lbob-api
sudo systemctl start ollama
sudo systemctl start lbob-health-monitor

# Stop services
sudo systemctl stop lbob-api
sudo systemctl stop ollama
sudo systemctl stop lbob-health-monitor

# Restart services
sudo systemctl restart lbob-api
sudo systemctl restart ollama

# Check status
sudo systemctl status lbob-api
sudo systemctl is-active lbob-api
sudo systemctl is-enabled lbob-api
```

---

## 📊 **MONITORING & LOGGING**

### **Health Monitoring**
The health monitor (`health-monitor.py`) provides:

**Features:**
- 30-second health checks for all services
- Automated restart on failure (3-strike rule)
- Resource utilization monitoring
- Comprehensive status logging
- JSON status reports

**Monitoring Targets:**
- LBOB API response time and health
- Ollama AI service availability
- System resources (CPU, memory, disk)
- Database connectivity
- Network connectivity

**Health Check Endpoints:**
```bash
# LBOB API health
curl http://localhost:8000/health

# Ollama service status
curl http://localhost:11434/api/tags

# System resource status
htop
iotop
nethogs
```

### **Centralized Logging**

**Log Locations:**
```
/var/log/lbob/
├── health-monitor.log     # Health monitoring events
├── api.log               # LBOB API requests and responses
├── backup.log            # Backup operation logs
└── status.json           # Latest system status

/var/log/ollama/
└── ollama.log            # AI service logs

System Logs:
/var/log/nginx/           # Nginx access and error logs
/var/log/fail2ban.log     # Security events
/var/log/ufw.log          # Firewall events
```

**Log Management:**
- **Rotation**: Daily rotation with 30-day retention
- **Compression**: Automatic compression of old logs
- **Centralization**: Structured logging via rsyslog
- **Monitoring**: Real-time log monitoring available

**Viewing Logs:**
```bash
# Real-time API logs
sudo journalctl -u lbob-api -f

# Health monitor logs
sudo tail -f /var/log/lbob/health-monitor.log

# Nginx access logs
sudo tail -f /var/log/nginx/access.log

# All LBOB logs
sudo tail -f /var/log/lbob/*.log
```

### **Performance Monitoring**
```bash
# System performance
htop                      # CPU and memory usage
iotop                     # Disk I/O monitoring
nethogs                   # Network usage by process
ss -tulpn                 # Network connections

# Service-specific monitoring
sudo systemctl status lbob-api
sudo journalctl -u lbob-api --since "1 hour ago"
curl http://localhost:8000/health | jq
```

---

## 🔐 **SECURITY CONFIGURATION**

### **Firewall (UFW)**
```bash
# Current rules
sudo ufw status verbose

# Allow additional services
sudo ufw allow from 192.168.1.0/24 to any port 8080  # Monitoring dashboard
```

### **Fail2ban Protection**
- SSH brute force protection
- Nginx DoS protection
- Bad bot detection
- Automatic IP banning

### **Service Isolation**
- Each service runs with minimal privileges
- Private temporary directories
- Read-only system files
- Resource limits enforced

### **Rate Limiting**
- API: 10 requests/second per IP
- AI endpoints: 2 requests/second per IP
- Burst allowance for legitimate traffic

---

## 📦 **BACKUP & RECOVERY**

### **Automated Backups**
**Schedule:** Daily at 2:00 AM
**Retention:** 7 days
**Location:** `/opt/backups/`

**Backup Contents:**
- Application code and configuration
- Database files
- Logs (recent)
- Custom configuration files

**Manual Backup:**
```bash
# Create immediate backup
sudo /opt/backups/backup-lbob.sh

# Verify backups
ls -la /opt/backups/lbob_backup_*.tar.gz
```

### **Recovery Procedures**

**Quick Recovery (Service Issues):**
```bash
# Restart all services
sudo systemctl restart lbob-api ollama lbob-health-monitor

# Check service status
sudo systemctl status lbob-api ollama lbob-health-monitor
```

**Full Recovery (System Issues):**
```bash
# Stop services
sudo systemctl stop lbob-api ollama lbob-health-monitor

# Restore from backup
cd /opt
sudo tar -xzf /opt/backups/lbob_backup_YYYYMMDD_HHMMSS.tar.gz

# Restart services
sudo systemctl start lbob-api ollama lbob-health-monitor
```

---

## 🎯 **PERFORMANCE OPTIMIZATION**

### **Resource Allocation**
**LBOB API:**
- Workers: 2 (adjustable based on traffic)
- Memory: ~500MB per worker
- CPU: Low usage except during AI calls

**Ollama AI:**
- Memory: 4-6GB for Llama 3.1:8b model
- CPU: High during inference
- Storage: ~5GB for model files

### **Performance Tuning**
```bash
# Monitor resource usage
htop
sudo systemctl status lbob-api ollama

# Adjust worker count (if needed)
sudo systemctl edit lbob-api
# Add: ExecStart override with --workers N

# Monitor AI response times
curl -w "@curl-format.txt" http://localhost:8000/health
```

### **Optimization Settings**
- Nginx: Connection pooling, caching
- Systemd: Resource limits, watchdog timers
- Python: uvicorn workers, async processing
- AI: Model preloading, response caching

---

## 🚨 **TROUBLESHOOTING**

### **Common Issues**

**Service Won't Start:**
```bash
# Check service status
sudo systemctl status lbob-api

# View detailed logs
sudo journalctl -u lbob-api -n 50

# Check port conflicts
sudo ss -tulpn | grep :8000
```

**AI Responses Slow/Failing:**
```bash
# Check Ollama status
sudo systemctl status ollama
curl http://localhost:11434/api/tags

# Monitor AI service resources
htop
iotop
```

**High Resource Usage:**
```bash
# Identify resource consumers
htop
iotop
nethogs

# Check service limits
sudo systemctl show lbob-api | grep -i limit
```

**Network Connectivity Issues:**
```bash
# Check firewall
sudo ufw status

# Test internal connectivity
curl http://localhost:8000/health
curl http://localhost:11434/api/tags

# Check external access
curl http://192.168.1.70:8000/health
```

### **Emergency Procedures**

**Service Recovery:**
```bash
# Full service restart
sudo systemctl restart lbob-api ollama lbob-health-monitor

# Nuclear option - full system restart
sudo reboot
```

**Resource Recovery:**
```bash
# Clear logs if disk full
sudo journalctl --vacuum-time=7d
sudo find /var/log -name "*.log" -mtime +7 -delete

# Kill resource-heavy processes
sudo pkill -f uvicorn
sudo systemctl restart lbob-api
```

---

## 📞 **MAINTENANCE & SUPPORT**

### **Regular Maintenance Tasks**

**Daily:**
- Monitor service status via health checks
- Review error logs for issues
- Verify backup completion

**Weekly:**
- Review performance metrics
- Check disk space and resource usage
- Update security patches (if available)

**Monthly:**
- Review and clean old logs
- Verify backup restoration procedures
- Performance optimization review

### **Maintenance Commands**
```bash
# System updates
sudo apt update && sudo apt upgrade

# Log cleanup
sudo journalctl --vacuum-time=30d
sudo find /var/log/lbob -name "*.log" -mtime +30 -delete

# Performance review
df -h                     # Disk usage
free -h                   # Memory usage
uptime                    # System load
```

### **Health Dashboard**
Access monitoring dashboard at: `http://192.168.1.70:8080/health-dashboard`
(Internal network only)

### **Contact Information**
- **System Administrator**: csprinks@domain.com
- **Emergency Contact**: [Emergency phone/email]
- **Documentation**: This guide + system README files
- **Repository**: https://github.com/c-sprinks/ClaudeCode-Projects

---

## 📈 **SUCCESS METRICS**

### **Uptime Targets**
- **Target Uptime**: 99.9% (8.76 hours downtime/year)
- **Maximum Downtime**: 43 minutes/month
- **Recovery Time**: < 5 minutes for service issues

### **Performance Targets**
- **API Response Time**: < 200ms (health checks)
- **AI Response Time**: < 30 seconds (typical queries)
- **Page Load Time**: < 2 seconds (web interface)

### **Monitoring KPIs**
- Service availability percentage
- Average response times
- Error rates
- Resource utilization trends
- Backup success rates

---

**🎉 Congratulations! LBOB AI is now deployed for 24/7 enterprise operations with industry-standard reliability, monitoring, and maintenance procedures.**