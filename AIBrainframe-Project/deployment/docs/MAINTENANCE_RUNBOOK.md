# 🔧 LBOB AI Maintenance Runbook
## 24/7 Operations Support & Troubleshooting

**Version:** 1.0
**Last Updated:** 2025-10-20
**Audience:** System Administrators, DevOps Engineers, Technical Support

---

## 🚨 **EMERGENCY PROCEDURES**

### **Service Down - Critical**
**Symptoms:** LBOB AI not responding, 500/502 errors
**Impact:** Complete service outage

**Immediate Actions:**
```bash
# 1. Check service status (30 seconds)
sudo systemctl status lbob-api ollama lbob-health-monitor

# 2. Restart services (2 minutes)
sudo systemctl restart lbob-api ollama lbob-health-monitor

# 3. Verify recovery (1 minute)
curl http://192.168.1.70:8000/health
curl http://192.168.1.70:8000/static/simple_lbob.html

# 4. If still down - nuclear restart (5 minutes)
sudo reboot
```

**Post-Recovery:**
1. Check logs for root cause: `sudo journalctl -u lbob-api -n 100`
2. Document incident in `/var/log/lbob/incidents.log`
3. Monitor for 30 minutes to ensure stability

### **AI Responses Failing - High Priority**
**Symptoms:** LBOB responds but no AI answers, timeout errors
**Impact:** Degraded user experience

**Immediate Actions:**
```bash
# 1. Check Ollama service
sudo systemctl status ollama
curl http://localhost:11434/api/tags

# 2. Restart Ollama if needed
sudo systemctl restart ollama
sleep 60  # Allow model loading

# 3. Test AI functionality
curl -X POST http://localhost:8000/conversations/1/messages \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer [token]" \
  -d '{"message_text": "Test message"}'
```

### **High Resource Usage - Medium Priority**
**Symptoms:** Slow responses, high CPU/memory alerts
**Impact:** Performance degradation

**Immediate Actions:**
```bash
# 1. Identify resource consumers
htop
iotop
ps aux --sort=-%cpu | head -10
ps aux --sort=-%mem | head -10

# 2. Check disk space
df -h
du -sh /var/log/* | sort -hr

# 3. Clean up if needed
sudo journalctl --vacuum-time=7d
sudo find /tmp -type f -mtime +7 -delete

# 4. Restart services if resource leak suspected
sudo systemctl restart lbob-api
```

---

## 📊 **DAILY MONITORING CHECKLIST**

### **Service Health (5 minutes)**
```bash
# Run daily health check script
cat > /tmp/daily_health_check.sh << 'EOF'
#!/bin/bash
echo "=== LBOB AI Daily Health Check $(date) ==="

# Service status
echo "## Service Status"
systemctl is-active lbob-api && echo "✅ LBOB API: Running" || echo "❌ LBOB API: Down"
systemctl is-active ollama && echo "✅ Ollama: Running" || echo "❌ Ollama: Down"
systemctl is-active lbob-health-monitor && echo "✅ Health Monitor: Running" || echo "❌ Health Monitor: Down"

# API health
echo "## API Health"
if curl -s -f http://localhost:8000/health > /dev/null; then
    echo "✅ LBOB API: Responding"
else
    echo "❌ LBOB API: Not responding"
fi

if curl -s -f http://localhost:11434/api/tags > /dev/null; then
    echo "✅ Ollama: Responding"
else
    echo "❌ Ollama: Not responding"
fi

# Resource usage
echo "## Resource Usage"
echo "CPU: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | awk -F'%' '{print $1}')%"
echo "Memory: $(free | grep Mem | awk '{printf("%.1f"), $3/$2 * 100.0}')%"
echo "Disk: $(df / | tail -1 | awk '{print $5}')"

# Log errors
echo "## Recent Errors (last 24h)"
ERROR_COUNT=$(journalctl -u lbob-api --since "24 hours ago" | grep -i error | wc -l)
echo "LBOB API errors: $ERROR_COUNT"

OLLAMA_ERROR_COUNT=$(journalctl -u ollama --since "24 hours ago" | grep -i error | wc -l)
echo "Ollama errors: $OLLAMA_ERROR_COUNT"

echo "=== Health Check Complete ==="
EOF

chmod +x /tmp/daily_health_check.sh
/tmp/daily_health_check.sh
```

### **Backup Verification (2 minutes)**
```bash
# Check last backup
ls -la /opt/backups/lbob_backup_*.tar.gz | tail -1

# Verify backup age (should be < 24 hours)
find /opt/backups -name "lbob_backup_*.tar.gz" -mtime -1 | wc -l
```

### **Log Review (3 minutes)**
```bash
# Check for critical errors
sudo journalctl -u lbob-api --since "24 hours ago" | grep -i "critical\|fatal\|error" | tail -10

# Check health monitor alerts
sudo tail -20 /var/log/lbob/health-monitor.log | grep -i "error\|restart\|failure"

# Check security events
sudo tail -20 /var/log/fail2ban.log | grep -i "banned\|found"
```

---

## 📈 **WEEKLY MAINTENANCE TASKS**

### **Performance Analysis (15 minutes)**
```bash
# CPU and memory trends
echo "=== Weekly Performance Report $(date) ==="

# Service uptime
systemctl show lbob-api --property=ActiveEnterTimestamp
systemctl show ollama --property=ActiveEnterTimestamp

# Resource utilization
echo "## Resource Usage Trends"
sar -u 1 1  # CPU usage
sar -r 1 1  # Memory usage
sar -d 1 1  # Disk I/O

# Network statistics
ss -s  # Socket statistics
netstat -i  # Interface statistics

# Log growth
du -sh /var/log/lbob/
du -sh /var/log/ollama/
```

### **Security Review (10 minutes)**
```bash
# Failed login attempts
sudo grep "Failed password" /var/log/auth.log | tail -10

# Fail2ban activity
sudo fail2ban-client status
sudo fail2ban-client status sshd

# Firewall status
sudo ufw status numbered

# System updates available
apt list --upgradable 2>/dev/null | wc -l
```

### **Log Rotation & Cleanup (5 minutes)**
```bash
# Force log rotation
sudo logrotate -f /etc/logrotate.d/lbob

# Clean old logs manually if needed
sudo find /var/log/lbob -name "*.log.*" -mtime +30 -delete

# Clean temporary files
sudo find /tmp -type f -mtime +7 -delete
sudo find /var/tmp -type f -mtime +7 -delete
```

---

## 🔧 **MONTHLY MAINTENANCE TASKS**

### **System Updates (30 minutes)**
```bash
# Create maintenance window announcement
echo "MAINTENANCE: LBOB AI system updates in progress" > /opt/aibrainframe_claude/assets/maintenance.html

# Stop services gracefully
sudo systemctl stop lbob-health-monitor
sudo systemctl stop lbob-api
sudo systemctl stop ollama

# Update system packages
sudo apt update
sudo apt list --upgradable
sudo apt upgrade -y

# Update Python packages
cd /opt/aibrainframe_claude
source venv/bin/activate
pip list --outdated
pip install --upgrade pip
# pip install --upgrade package_name  # Only if needed

# Restart services
sudo systemctl start ollama
sleep 30  # Allow model loading
sudo systemctl start lbob-api
sleep 15
sudo systemctl start lbob-health-monitor

# Verify functionality
curl http://localhost:8000/health
rm /opt/aibrainframe_claude/assets/maintenance.html
```

### **Backup Testing (20 minutes)**
```bash
# Create test backup
sudo /opt/backups/backup-lbob.sh

# Test backup restoration (in test directory)
mkdir -p /tmp/backup_test
cd /tmp/backup_test
sudo tar -xzf /opt/backups/lbob_backup_$(date +%Y%m%d)*.tar.gz

# Verify critical files exist
test -f aibrainframe_claude/app/main.py && echo "✅ Main app file exists"
test -f aibrainframe_claude/app/ai_service.py && echo "✅ AI service file exists"
test -f aibrainframe_claude/aibrainframe.db && echo "✅ Database file exists"

# Cleanup test
rm -rf /tmp/backup_test
```

### **Performance Optimization Review (15 minutes)**
```bash
# Database size and performance
ls -lh /opt/aibrainframe_claude/aibrainframe.db

# Log file sizes
du -sh /var/log/lbob/*
du -sh /var/log/ollama/*

# Service memory usage over time
ps aux | grep uvicorn | awk '{print $6}' | head -1  # RSS memory
ps aux | grep ollama | awk '{print $6}' | head -1   # RSS memory

# Disk space analysis
df -h
du -sh /opt/aibrainframe_claude/*
ncdu /opt/aibrainframe_claude  # Interactive disk usage
```

---

## 🚨 **TROUBLESHOOTING GUIDE**

### **Common Issues & Solutions**

#### **Issue: "Connection Refused" on Port 8000**
**Diagnosis:**
```bash
sudo systemctl status lbob-api
sudo netstat -tlnp | grep :8000
sudo journalctl -u lbob-api -n 20
```

**Solutions:**
1. Service not running: `sudo systemctl start lbob-api`
2. Port conflict: Check if another process is using port 8000
3. Firewall blocking: `sudo ufw allow 8000/tcp`
4. Configuration error: Check `/opt/aibrainframe_claude/app/main.py`

#### **Issue: AI Responses Taking Too Long**
**Diagnosis:**
```bash
curl -w "@curl-format.txt" http://localhost:11434/api/tags
top -p $(pgrep ollama)
nvidia-smi  # If using GPU
```

**Solutions:**
1. Restart Ollama: `sudo systemctl restart ollama`
2. Check model loading: `curl http://localhost:11434/api/tags`
3. Resource constraints: Increase memory limits in service file
4. Model corruption: Re-download model with `ollama pull llama3.1:8b`

#### **Issue: High Memory Usage**
**Diagnosis:**
```bash
ps aux --sort=-%mem | head -10
cat /proc/meminfo
sudo systemctl show lbob-api | grep -i memory
```

**Solutions:**
1. Restart services to clear memory leaks
2. Adjust service memory limits
3. Enable swap if needed: `sudo swapon -a`
4. Monitor for memory leaks: `valgrind` on development

#### **Issue: Disk Space Full**
**Diagnosis:**
```bash
df -h
du -sh /var/log/* | sort -hr
du -sh /opt/aibrainframe_claude/* | sort -hr
```

**Solutions:**
1. Clean logs: `sudo journalctl --vacuum-time=7d`
2. Remove old backups: `find /opt/backups -mtime +14 -delete`
3. Clean temporary files: `sudo find /tmp -mtime +7 -delete`
4. Archive old conversation data if needed

#### **Issue: SSL/TLS Certificate Errors**
**Diagnosis:**
```bash
openssl s_client -connect 192.168.1.70:443 -servername lbob.local
sudo nginx -t
```

**Solutions:**
1. Renew certificates: `sudo certbot renew`
2. Check Nginx config: `sudo nginx -t && sudo systemctl reload nginx`
3. Verify certificate paths in configuration

### **Advanced Diagnostics**

#### **Performance Profiling**
```bash
# Profile Python application
pip install py-spy
sudo py-spy top --pid $(pgrep -f uvicorn)

# System call tracing
sudo strace -p $(pgrep -f uvicorn) -c

# Network analysis
sudo tcpdump -i any port 8000 -c 100

# Database performance
sqlite3 /opt/aibrainframe_claude/aibrainframe.db ".schema"
sqlite3 /opt/aibrainframe_claude/aibrainframe.db "PRAGMA optimize;"
```

#### **Security Analysis**
```bash
# Active connections
sudo netstat -tuln
sudo ss -tuln

# Process tree
pstree -p

# Open files
sudo lsof +L1  # Check for deleted files still open
sudo lsof -u csprinks

# Security scan
sudo chkrootkit
sudo rkhunter --check
```

---

## 📞 **ESCALATION PROCEDURES**

### **Level 1: Self-Service (Tech/User)**
- Check service status dashboard
- Restart browser/clear cache
- Try different network connection
- Wait 5 minutes for auto-recovery

### **Level 2: System Administrator**
- Run daily health checks
- Restart services if needed
- Check logs for obvious issues
- Verify system resources

### **Level 3: DevOps Engineer**
- Deep log analysis
- Performance profiling
- Configuration debugging
- Infrastructure changes

### **Level 4: Development Team**
- Code-level debugging
- Database schema issues
- AI model problems
- Application architecture changes

### **Contact Information**
```
Level 1 Support: [Internal Help Desk]
Level 2 Support: csprinks@domain.com
Level 3 Support: [DevOps Team Lead]
Level 4 Support: [Development Team Lead]

Emergency Contact: [24/7 Phone Number]
Vendor Support: Ollama Community / FastAPI Documentation
```

---

## 📚 **REFERENCE DOCUMENTATION**

### **Configuration Files**
- `/etc/systemd/system/lbob-api.service` - Main API service
- `/etc/systemd/system/ollama.service` - AI service
- `/etc/systemd/system/lbob-health-monitor.service` - Monitoring
- `/etc/nginx/sites-available/lbob` - Web server config
- `/etc/logrotate.d/lbob` - Log rotation
- `/opt/aibrainframe_claude/.env` - Environment variables

### **Log Locations**
- `/var/log/lbob/` - Application logs
- `/var/log/ollama/` - AI service logs
- `/var/log/nginx/` - Web server logs
- `/var/log/syslog` - System logs
- `journalctl -u lbob-api` - Service logs

### **Important Commands Reference**
```bash
# Service Management
sudo systemctl {start|stop|restart|status} lbob-api
sudo systemctl {start|stop|restart|status} ollama
sudo systemctl {start|stop|restart|status} lbob-health-monitor

# Log Viewing
sudo journalctl -u lbob-api -f                    # Follow API logs
sudo tail -f /var/log/lbob/health-monitor.log     # Follow health logs
sudo tail -f /var/log/nginx/access.log            # Follow web logs

# Health Checks
curl http://localhost:8000/health                 # API health
curl http://localhost:11434/api/tags              # AI service
systemctl is-active lbob-api                      # Service status

# Performance Monitoring
htop                                               # Interactive process viewer
iotop                                              # I/O monitoring
nethogs                                            # Network usage
df -h                                              # Disk usage
free -h                                            # Memory usage

# Security
sudo ufw status                                    # Firewall status
sudo fail2ban-client status                       # Intrusion prevention
sudo journalctl -u ssh -f                         # SSH access logs
```

---

**📋 This runbook should be reviewed and updated quarterly or after any major system changes.**