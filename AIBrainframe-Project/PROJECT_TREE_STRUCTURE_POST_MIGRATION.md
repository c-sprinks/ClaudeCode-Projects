# AIBrainframe Project - Complete Directory Structure (Post Migration)
**Updated**: October 6, 2025 - Repository Migration Complete
**Status**: Production Ready with Unified Monorepo Architecture

---

## 🏗️ **NEW UNIFIED PROJECT STRUCTURE**

### **Multi-Environment Monorepo**
```
ClaudeCode-Projects/
└── AIBrainframe-Project/                    # Main unified project
    ├── 📱 Mobile Development
    │   └── mobile-app/AIBrainframeMobile/    # React Native TypeScript
    │
    ├── 🖥️ Backend API (FastAPI + AI Integration)
    │   ├── app/
    │   │   ├── main.py                       # Main application entry
    │   │   ├── ai_service.py                 # 🚀 AI integration with Ollama
    │   │   ├── auth.py                       # JWT authentication
    │   │   ├── models.py                     # SQLAlchemy database models
    │   │   ├── schemas.py                    # Pydantic schemas
    │   │   └── routes/
    │   │       ├── conversations.py          # 🎯 AI chat endpoints (READY)
    │   │       ├── users.py                  # User management
    │   │       └── [other routes...]
    │   └── config/database.py                # Database configuration
    │
    ├── 🌐 Web Interfaces (Production Ready)
    │   ├── static/
    │   │   ├── simple_lbob.html              # 🎨 Neural network theme
    │   │   └── aibrainframe_web_app.html     # Immersive character
    │   └── dev-tools/test_api.html           # API testing
    │
    ├── 🎭 LBOB Character Assets
    │   ├── assets/images/characters/
    │   │   ├── LBOBAICharacter_ai.png        # ✨ AI-processed transparent
    │   │   └── [character variations...]
    │   └── assets/models/model.glb           # 3D LBOB model
    │
    ├── 📚 Documentation & Session History
    │   ├── session-history/
    │   │   ├── MASTER_PROJECT_STATUS.md      # 📊 Central status
    │   │   ├── SESSION_HANDOFF_NEXT_AI_INTEGRATION.md # 🚀 Next session
    │   │   ├── session-logs/                 # Chronological sessions
    │   │   └── archives/                     # Historical docs + PDFs
    │   └── [other docs...]
    │
    ├── 🗄️ Data & Environment
    │   ├── data/aibrainframe.db              # SQLite database
    │   ├── venv/                             # Python virtual environment
    │   ├── .env                              # Environment variables
    │   └── requirements.txt                  # Python dependencies
```

---

## 🖥️ **ENVIRONMENT DEPLOYMENTS (NOW UNIFIED)**

### **🆕 Server Production (MIGRATED)**
```
Server: 192.168.1.70
└── /opt/aibrainframe_claude/AIBrainframe-Project/
    ├── ✅ AI Infrastructure Ready
    │   ├── Ollama Service (Process 57502)
    │   ├── Llama 3.1:8b Model (4.9GB)
    │   └── API: http://localhost:11434
    │
    ├── ✅ Supporting Services
    │   ├── PostgreSQL (Process 1280)
    │   ├── Nginx (24 workers)
    │   ├── Redis (Process 1111)
    │   └── Security (UFW + fail2ban)
    │
    └── 🚀 READY FOR: AI Integration
```

### **Development Environments**
- **TBL1 (Current)**: `/home/csprinks/ClaudeCode-Projects/AIBrainframe-Project/`
- **Desktop**: Same path, synced via git
- **All environments now use same repository structure** ✅

---

## 📋 **CRITICAL FILES FOR NEXT SESSION**

### **🎯 Primary Target**
```
/opt/aibrainframe_claude/AIBrainframe-Project/
└── app/routes/conversations.py               # Line 111-112 needs update
    # FROM: ai_response_text = f"I understand..."
    # TO:   ai_response_text = ai_service.generate_ai_response(...)
```

### **🔧 Supporting Files**
- `app/ai_service.py` - Ready for integration
- `static/simple_lbob.html` - Frontend interface
- `data/aibrainframe.db` - Database with test users

---

## 🎊 **MIGRATION SUCCESS**

### **✅ Completed Actions**
1. **Repository Migration**: Server now uses ClaudeCode-Projects monorepo
2. **Safety Backup**: Original preserved at `/opt/aibrainframe_backup_20251007_0149`
3. **Industry Standards**: Implemented 2025 best practices
4. **Documentation**: All guides updated for new structure

### **🚀 Ready for AI Integration**
- All infrastructure operational
- Code synchronized across environments
- Documentation comprehensive and current
- Next session can focus purely on AI connection

---

**Status**: ✅ **Migration Complete - Ready for AI Phase**