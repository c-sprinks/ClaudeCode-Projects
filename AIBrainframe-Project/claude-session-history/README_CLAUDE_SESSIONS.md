# Claude Code Session History System

## 📁 Purpose
This directory contains timestamped documentation for all Claude Code sessions to maintain continuity across different machines and sessions.

## 📋 Quick Start for New Sessions

### **Step 1: Read Session History**
```bash
cd /home/csprinks/ClaudeCode-Projects/claude-session-history/
ls -la  # See all available session files
```

### **Step 2: Get Latest Context**
```bash
# Read the most recent session file
cat ADMIN_CONVO_2025-10-04_EVENING_TBL1.md
cat PROJECT_STATUS_2025-10-04_EVENING_TBL1.md
```

### **Step 3: Verify Current Machine**
```bash
uname -a  # Check which machine you're on
cd /home/csprinks/ClaudeCode-Projects/AIBrainframe-Project/
git status && git log --oneline -3
```

## 📝 File Naming Convention

### **Session Files**
- **Format:** `ADMIN_CONVO_YYYY-MM-DD_TIME_MACHINE.md`
- **Example:** `ADMIN_CONVO_2025-10-04_EVENING_TBL1.md`

### **Status Files**
- **Format:** `PROJECT_STATUS_YYYY-MM-DD_TIME_MACHINE.md`
- **Example:** `PROJECT_STATUS_2025-10-04_EVENING_TBL1.md`

### **Machine Codes**
- **TBL1:** Laptop (Ubuntu/Linux Surface)
- **DESKTOP:** Main-Station (Debian 13)
- **SERVER:** Ubuntu Server (192.168.1.70)

## 🎯 How to Use

### **Starting a New Claude Code Session**
1. **Navigate to this folder first**
2. **Read the latest session files**
3. **Check current machine with `uname -a`**
4. **Review project status and next steps**
5. **Continue from where previous session left off**

### **Ending a Claude Code Session**
1. **Create new timestamped session file**
2. **Update project status file**
3. **Document current state and next steps**
4. **Commit changes to git if significant progress made**

## 📚 Session History Index

### **October 4, 2025**
- **Morning/Day:** Desktop session (Main-Station) - Complete development
- **Evening:** Laptop session (TBL1) - Environment preparation

### **Session Content**
- **ADMIN_CONVO files:** Detailed conversation history, decisions, accomplishments
- **PROJECT_STATUS files:** Current state, checklist, next steps, technical status

## 🔧 Key Information Always Include

### **Every Session File Should Document**
- Current machine and location
- Git status and latest commits
- Environment state (running services, setup status)
- Immediate next steps and priorities
- Any blocking issues or decisions needed

### **Quick Status Commands**
```bash
# Machine identification
uname -a

# Git status
git status && git log --oneline -3

# Running services
ps aux | grep uvicorn

# Network check
ip addr show | grep inet
```

## 🚨 Critical Reminders

### **Multi-Machine Setup**
- **Desktop (Main-Station):** Primary development, has latest complete environment
- **Laptop (TBL1):** Secondary development, needs environment setup
- **Server (192.168.1.70):** Production target, needs sync strategy

### **Always Check Before Starting**
1. Which machine am I on?
2. What was accomplished in the last session?
3. What are the immediate next steps?
4. Are there any blocking issues or decisions needed?
5. Is the git repository up to date?

## 📞 Emergency Recovery

### **If Session History is Lost**
- **Latest Code:** Always in GitHub repository
- **Desktop Backup:** Main-Station has complete working environment
- **Server Backup:** `/opt/aibrainframe` has older but functional version

### **Key Project Info**
- **Repository:** https://github.com/c-sprinks/ClaudeCode-Projects.git
- **Test User:** `testtech` / `password123`
- **API Port:** 8000
- **Server SSH:** `sshpass -p '0320' ssh csprinks@192.168.1.70`

---

**Created:** October 4, 2025 (Evening)
**Purpose:** Maintain Claude Code session continuity across machines and time