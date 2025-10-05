# AIBrainframe Project - Complete Directory Structure

## 📁 Final Organized Project Tree

```
AIBrainframe-Project/
├── 📋 README.md                          # Main project documentation
├── 📋 .gitignore                         # Git ignore rules
├── 📋 .env                               # Environment variables (not in git)
├── 📋 requirements.txt                   # Python dependencies
├── 📋 PROJECT_STATUS_CHECKPOINT.md       # Current status tracking
│
├── 🖥️ Backend Application/
│   ├── app/                              # FastAPI application
│   │   ├── __init__.py
│   │   ├── main.py                       # Application entry point
│   │   ├── models.py                     # Database models
│   │   ├── auth.py                       # Authentication logic
│   │   ├── schemas.py                    # Pydantic schemas
│   │   └── routes/                       # API endpoint modules
│   │       ├── __init__.py
│   │       ├── users.py                  # User management
│   │       ├── conversations.py          # Chat functionality
│   │       ├── companies.py              # Company management
│   │       ├── equipment.py              # Equipment tracking
│   │       ├── jobs.py                   # Job management
│   │       └── solutions.py              # Solution database
│   └── config/                           # Configuration files
│       ├── __init__.py
│       └── database.py                   # Database configuration
│
├── 🌐 Web Interface/
│   ├── aibrainframe_web_app.html         # Main immersive web application
│   ├── simple_lbob.html                  # Simplified LBOB interface
│   └── test_api.html                     # API testing interface
│
├── 📱 Mobile Application/
│   └── mobile-app/AIBrainframeMobile/    # Complete React Native app
│       ├── App.tsx                       # Main TypeScript application
│       ├── package.json                  # Dependencies and scripts
│       ├── android/                      # Android configuration
│       ├── ios/                          # iOS configuration
│       └── node_modules/                 # Node.js dependencies
│
├── 🎨 Assets & Media/
│   └── assets/
│       ├── images/
│       │   ├── characters/               # LBOB character variations
│       │   │   ├── LBOB3.png
│       │   │   ├── LBOBAICharacter*.png  # Multiple character versions
│       │   │   └── Gemini_Generated_*.png
│       │   ├── logos/                    # Branding and logos
│       │   │   ├── CertaSite_Primary_*.webp
│       │   │   ├── certasite-logo.webp
│       │   │   └── certasite-website-screenshot.png
│       │   ├── 3d-models/               # 3D character models
│       │   │   ├── model.fbx
│       │   │   ├── model.glb
│       │   │   └── model.obj
│       │   ├── ui-screenshots/          # Interface screenshots
│       │   │   └── Screenshot*.png
│       │   ├── screenshots/             # Additional screenshots
│       │   └── people/                  # Team/reference photos
│       └── styles/
│           └── certasite-brand-guide.md # Brand guidelines
│
├── 📚 Documentation/
│   └── docs/
│       ├── session-history/             # Claude Code session logs
│       │   ├── README_CLAUDE_SESSIONS.md
│       │   ├── ADMIN_CONVO_*.md         # Conversation histories
│       │   ├── PROJECT_STATUS_*.md      # Status checkpoints
│       │   ├── DEVELOPMENT_SETUP_*.md   # Setup guides
│       │   └── 2025-10-05_*.md         # Recent session logs
│       ├── project-specs/              # Requirements and specifications
│       │   └── Complete*.pdf           # PDF documentation
│       ├── setup-guides/               # Environment setup guides
│       │   ├── migrate_to_postgres.py
│       │   ├── setup_postgres.py
│       │   ├── postgres_setup_instructions.txt
│       │   ├── mobile_platform_configs*.js
│       │   ├── react_native_setup.json
│       │   └── ios_android_config.txt
│       └── api-docs/                   # API documentation (auto-generated)
│
├── 🗄️ Database/
│   └── aibrainframe.db                  # SQLite database file
│
├── 🧪 Testing/
│   └── tests/                           # Test files and test data
│
├── 📊 Data/
│   └── data/                            # Data files and exports
│
└── 🔧 Environment/
    ├── venv/                            # Python virtual environment
    └── .claude/                         # Claude Code settings (local)
```

## 📁 Directory Descriptions

### **Root Level**
- **README.md**: Complete project documentation and quick start guide
- **.gitignore**: Comprehensive ignore rules for all environments
- **.env**: Environment variables (database, API keys, configurations)
- **requirements.txt**: Python package dependencies

### **Backend Application (`app/`)**
- **main.py**: FastAPI application entry point with CORS and routing
- **models.py**: SQLAlchemy database models for all entities
- **auth.py**: JWT authentication and user management
- **routes/**: Modular API endpoints organized by functionality

### **Web Interface**
- **aibrainframe_web_app.html**: Revolutionary immersive LBOB experience
- **simple_lbob.html**: Simplified character interface for testing
- **test_api.html**: Comprehensive API testing tool

### **Mobile Application**
- **Complete React Native TypeScript application**
- **Cross-platform support**: iOS and Android
- **Professional UI/UX**: Integrated LBOB character system

### **Assets Organization**
- **characters/**: All LBOB character images and variations
- **logos/**: Corporate branding and CertaSite integration
- **3d-models/**: FBX, GLB, OBJ files for advanced character rendering
- **ui-screenshots/**: Interface documentation and progress tracking
- **people/**: Team reference photos

### **Documentation System**
- **session-history/**: Complete Claude Code session tracking
- **project-specs/**: Requirements, specifications, and project planning
- **setup-guides/**: Environment setup for all machines and platforms
- **api-docs/**: Auto-generated API documentation

## 🔧 Environment Setup by Machine

### **Desktop (Main-Station) - Debian 13**
```bash
cd /home/csprinks/ClaudeCode-Projects/AIBrainframe-Project
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### **Laptop (TBL1) - Ubuntu**
```bash
git pull origin main
cd AIBrainframe-Project
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Create .env file manually
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### **Server (192.168.1.70) - Ubuntu**
```bash
sshpass -p '0320' ssh csprinks@192.168.1.70
# Sync latest code and deploy
```

## 📊 File Count Summary

### **Assets**
- **Character Images**: 10+ LBOB variations
- **3D Models**: 3 formats (FBX, GLB, OBJ)
- **Logos & Branding**: CertaSite integration
- **Screenshots**: UI documentation

### **Documentation**
- **Session History**: Complete tracking system
- **Setup Guides**: Multi-platform instructions
- **Project Specifications**: Requirements and planning
- **API Documentation**: Auto-generated from FastAPI

### **Code Files**
- **Backend**: FastAPI with modular routing
- **Mobile**: React Native TypeScript
- **Web**: Immersive character interface
- **Configuration**: Multi-environment support

## 🎯 Organization Benefits

### **Developer Experience**
- **Clear Structure**: Easy navigation and file location
- **Modular Design**: Separation of concerns and responsibilities
- **Documentation**: Complete session history and setup guides
- **Multi-platform**: Consistent development across machines

### **Maintenance**
- **Version Control**: Proper gitignore and organization
- **Asset Management**: Categorized and accessible media files
- **Configuration**: Environment-specific settings
- **Testing**: Organized test files and API tools

### **Scalability**
- **Modular Backend**: Easy to extend API functionality
- **Asset Organization**: Simple to add new character variations
- **Documentation**: Trackable progress and decisions
- **Multi-environment**: Seamless deployment across platforms

---

**Last Updated**: October 5, 2025
**Organization Status**: Complete
**Structure Version**: 2.0.0 - Fully Organized