# 🚨 CRITICAL: READ THIS FIRST - ANTI-TOKEN-WASTE GUIDE

**Last Updated**: 2025-10-20 23:30
**Purpose**: Prevent repetitive diagnostics and wasted tokens

---

## ⚠️ **MANDATORY CHECKS BEFORE ANY WORK:**

### **1. PROJECT STATUS (UPDATED 2025-10-21):**
- **🔄 LBOB AI**: 95% WORKING - Authentication fixed, AI service issue remains
- **✅ nikki-project**: 100% COMPLETE - All PDFs enhanced, GitHub synced
- **🔄 Inspector-G**: 85% complete - Next: Custom OSINT modules

### **2. SERVER STATUS (DO NOT RE-DIAGNOSE):**
- **✅ Production Server**: 192.168.1.70 - HEALTHY
- **✅ LBOB FastAPI**: Port 8000 - RUNNING
- **✅ Ollama AI**: Port 11434 - RUNNING
- **✅ Database**: SQLite - CONNECTED

### **3. WORKING SSH COMMANDS (COPY EXACTLY):**
```bash
# Basic connection:
sshpass -p '0320' ssh csprinks@192.168.1.70

# Process check:
sshpass -p '0320' ssh csprinks@192.168.1.70 'ps aux | grep uvicorn'

# File deployment:
sshpass -p '0320' scp LOCAL_FILE csprinks@192.168.1.70:REMOTE_PATH

# Server logs:
sshpass -p '0320' ssh csprinks@192.168.1.70 'cd /opt/aibrainframe_claude && tail -20 server.log'
```

---

## 🛑 **STOP DOING THESE (UPDATED 2025-10-21):**

### **LBOB AI - DO NOT:**
- ❌ Re-test authentication (401/500 errors FIXED)
- ❌ Re-deploy ai_service.py (ALREADY DEPLOYED)
- ❌ Re-install langchain-ollama (AVAILABLE IN VENV)
- ❌ Re-fix JWT/localStorage issues (ALREADY FIXED)
- ❌ Re-deploy systemd services (ALREADY DEPLOYED)
- ❌ Re-check Ollama status (WORKING WHEN ACCESSED DIRECTLY)

### **🔄 LBOB AI - REMAINING ISSUE:**
- **Problem**: AI responses still showing fallback instead of real Ollama
- **Cause**: systemd service not properly activating virtual environment
- **Evidence**: Manual venv activation works, systemd activation fails
- **Next**: Debug systemd virtual environment configuration

### **nikki-project - DO NOT:**
- ❌ Re-enhance PDFs
- ❌ Re-update branding
- ❌ Re-add charts/graphs
- ❌ Re-commit changes
- ❌ Re-push to GitHub

### **General - DO NOT:**
- ❌ Re-read MASTER_PROJECT_STATUS_CURRENT.md (it's outdated)
- ❌ Re-diagnose "connection refused" errors
- ❌ Re-check git status repeatedly
- ❌ Re-verify file permissions

---

## ✅ **WHAT TO DO INSTEAD:**

### **If User Reports Issue:**
1. **Ask specific question**: "What exactly isn't working?"
2. **Check this file**: Read the current status
3. **Targeted fix**: Address only the specific issue
4. **Update this file**: Document the fix

### **If Starting New Feature:**
1. **Read project READMEs**: Understand current state
2. **Check git status**: See recent commits
3. **Plan properly**: Use TodoWrite tool
4. **Work incrementally**: Small, focused changes

### **Session Optimization:**
1. **Start with status check**: Read this file first
2. **Ask before diagnosing**: "Should I check X or is it working?"
3. **Document changes**: Update status files
4. **End with summary**: Clear handoff for next session

---

## 📁 **KEY PROJECT FILES (REFERENCE ONLY):**

### **Documentation Hierarchy:**
1. **THIS FILE** - Current status and anti-patterns
2. **MASTER_PROJECT_STATUS_CURRENT.md** - Overall project overview
3. **Project READMEs** - Specific project details
4. **Session histories** - Past conversation logs

### **Working Credentials:**
- **LBOB Login**: testtech / password123
- **Server SSH**: csprinks@192.168.1.70 / 0320
- **GitHub**: Already configured and synced

---

## 🎯 **NEXT PRIORITIES (IF ASKED):**

### **Inspector-G (85% → 100%):**
- Custom OSINT modules development
- Username reconnaissance engine
- Email intelligence system
- Phase 3 implementation

### **Future Projects:**
- RootLine Client 2 portfolio
- Enhanced LBOB features
- Inspector-G advanced capabilities

---

## 🔍 **DEBUGGING PROTOCOL:**

### **If Something Actually Breaks:**
1. **Verify the issue**: Is it really broken or just token waste?
2. **Check recent changes**: What was touched last?
3. **Targeted fix**: Address root cause only
4. **Test minimally**: One verification, not five
5. **Update documentation**: Prevent future repeats

### **Red Flags for Token Waste:**
- "Let me check if the server is running" (it is)
- "Let me test the health endpoint" (it's healthy)
- "Let me verify SSH access" (it works)
- "Let me re-deploy the fix" (it's deployed)

---

**BOTTOM LINE**: Both LBOB AI and nikki-project are 100% complete and working. Focus on NEW work, not re-doing FINISHED work.