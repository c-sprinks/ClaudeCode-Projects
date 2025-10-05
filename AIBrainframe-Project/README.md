# AIBrainframe Project - Complete Documentation

## 🏗️ Project Overview

**AIBrainframe** is a revolutionary AI-powered assistant specifically designed for building safety professionals. The project combines modern web technologies with an immersive character-driven interface featuring **LBOB** (Large Brain, Open-source Behavior) - a virtual assistant inspired by classic desktop companions like Microsoft Clippy and BonziBuddy.

### 🎯 Key Features
- **FastAPI Backend** with JWT authentication and SQLite/PostgreSQL support
- **React Native Mobile App** with TypeScript for iOS/Android
- **Immersive Web Interface** with LBOB character interactions
- **Multi-platform Development** across Desktop, Laptop, and Server environments
- **Professional Branding** with CertaSite integration

---

## 📁 Project Structure

```
AIBrainframe-Project/
├── 📱 Mobile App
│   └── mobile-app/AIBrainframeMobile/     # React Native TypeScript app
├── 🖥️ Backend API
│   ├── app/                               # FastAPI application
│   │   ├── main.py                        # Main application entry
│   │   ├── models.py                      # Database models
│   │   ├── auth.py                        # Authentication logic
│   │   └── routes/                        # API endpoints
│   └── config/                            # Configuration files
├── 🌐 Web Interface
│   ├── aibrainframe_web_app.html          # Main immersive web app
│   ├── simple_lbob.html                   # Simplified interface
│   └── test_api.html                      # API testing tool
├── 🎨 Assets
│   ├── assets/images/characters/          # LBOB character variations
│   ├── assets/images/logos/               # Branding and logos
│   ├── assets/images/3d-models/          # 3D character models
│   ├── assets/images/ui-screenshots/     # Interface screenshots
│   └── assets/styles/                     # Brand guidelines
├── 📚 Documentation
│   ├── docs/session-history/              # Claude Code session logs
│   ├── docs/project-specs/               # Requirements and specifications
│   ├── docs/setup-guides/                # Environment setup guides
│   └── docs/api-docs/                    # API documentation
├── 🗄️ Database
│   └── aibrainframe.db                   # SQLite database
└── 🔧 Environment
    ├── venv/                             # Python virtual environment
    ├── .env                              # Environment variables
    └── requirements.txt                  # Python dependencies
```

---

## 🚀 Quick Start

### **Prerequisites**
- Python 3.13+
- Node.js 18.20.8+
- Java JDK 21 (for mobile development)
- Git

### **Setup Commands**
```bash
# Clone and navigate
git clone https://github.com/c-sprinks/ClaudeCode-Projects.git
cd ClaudeCode-Projects/AIBrainframe-Project

# Backend setup
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt

# Create .env file (see Environment Variables section)
cp .env.example .env  # Edit with your values

# Start FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Mobile app setup (separate terminal)
cd mobile-app/AIBrainframeMobile
npm install
npx react-native doctor  # Verify environment
```

---

## 🖥️ Multi-Machine Architecture

### **Desktop (Main-Station) - Debian 13**
- **Role:** Primary development machine
- **IP:** 192.168.1.247
- **Status:** Complete environment with latest code
- **Features:** Full stack development, testing, immersive interface

### **Laptop (TBL1) - Ubuntu**
- **Role:** Secondary development machine
- **Status:** Synced via git, environment configured
- **Features:** Portable development, testing capabilities

### **Server (192.168.1.70) - Ubuntu**
- **Role:** Production deployment target
- **Status:** Needs sync with latest desktop code
- **Access:** `sshpass -p '0320' ssh csprinks@192.168.1.70`

---

## 🔧 Technology Stack

### **Backend**
- **Framework:** FastAPI 0.104+
- **Database:** SQLite (development) / PostgreSQL (production)
- **Authentication:** JWT with Argon2 password hashing
- **ORM:** SQLAlchemy 2.0+
- **API Docs:** Swagger UI / ReDoc

### **Mobile**
- **Framework:** React Native 0.74+
- **Language:** TypeScript
- **Navigation:** React Navigation 6
- **State:** React Hooks + Context
- **Platform:** iOS & Android

### **Web**
- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **Styling:** Custom CSS with animations
- **Character:** LBOB interactive system
- **Experience:** Full-screen immersive interface

### **Development Tools**
- **Version Control:** Git + GitHub
- **Environment:** Python venv, npm
- **Testing:** Jest (mobile), FastAPI TestClient
- **Documentation:** Claude Code session tracking

---

## 🌐 API Endpoints

### **Authentication**
- `POST /users/register` - User registration
- `POST /users/login` - User authentication

### **Conversations**
- `GET /conversations/` - List user conversations
- `POST /conversations/` - Create new conversation
- `GET /conversations/{id}/messages` - Get conversation messages
- `POST /conversations/{id}/messages` - Send message

### **Documentation**
- `GET /docs` - Swagger UI documentation
- `GET /redoc` - ReDoc documentation
- `GET /` - API status and information

---

## ⚙️ Environment Variables

Create `.env` file in project root:

```bash
# Database Configuration
DB_HOST=localhost
DB_NAME=aibrainframe_db
DB_USER=aibrainframe_user
DB_PASSWORD=0320
USE_POSTGRES=false

# Security
SECRET_KEY=your_secret_key_here_change_this_in_production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Environment
ENVIRONMENT=development
DEBUG=True
```

---

## 🧪 Testing

### **Test User Credentials**
- **Username:** `testtech`
- **Password:** `password123`

### **API Testing**
```bash
# Test API status
curl http://localhost:8000/

# Test authentication
curl -X POST http://localhost:8000/users/login \
  -H "Content-Type: application/json" \
  -d '{"username": "testtech", "password": "password123"}'
```

### **Web Interface Testing**
1. Start FastAPI server: `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
2. Open `aibrainframe_web_app.html` in browser
3. Experience immersive LBOB interface

### **Mobile Testing**
```bash
cd mobile-app/AIBrainframeMobile
npm start
# Use Android Studio or Expo Go for device testing
```

---

## 🎨 LBOB Character System

### **Character Variations**
- **LBOB3.png** - Primary character design
- **LBOBAICharacter_transparent.png** - Transparent background
- **LBOBAICharacter_smart.png** - Professional mode
- **LBOBAICharacter_clean.png** - Minimalist design

### **Interactive Features**
- **Speech Bubbles** - Context-aware responses
- **Mood Changes** - Happy, thinking, excited, confused
- **Animations** - Floating, bobbing, click responses
- **3D Models** - FBX, GLB, OBJ formats available

### **Integration**
- Character positioned at bottom-right of interface
- Size: 150px (optimized for user experience)
- Clippy-style assistance for building safety professionals

---

## 📱 Mobile App Features

### **Authentication System**
- Secure login/logout functionality
- JWT token management
- User session persistence

### **Chat Interface**
- Real-time conversation with LBOB
- Message history and threading
- Professional UI/UX design

### **Network Configuration**
- API Base URL: `http://192.168.1.247:8000` (desktop)
- Configurable endpoints for different environments
- CORS support for cross-platform access

---

## 🔄 Development Workflow

### **Starting New Session**
1. **Check Machine:** `uname -a`
2. **Read Session History:** `docs/session-history/README_CLAUDE_SESSIONS.md`
3. **Git Status:** `git status && git log --oneline -3`
4. **Start Services:** `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`

### **Sync Between Machines**
```bash
# Push changes (Desktop)
git add . && git commit -m "Description" && git push origin main

# Pull changes (Laptop/Server)
git pull origin main
```

### **Session Documentation**
- Create timestamped session files in `docs/session-history/`
- Follow naming convention: `ADMIN_CONVO_YYYY-MM-DD_TIME_MACHINE.md`
- Document decisions, progress, and next steps

---

## 🚀 Deployment Guide

### **Development Deployment**
```bash
# Local development
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### **Production Deployment (Server)**
```bash
# Connect to server
sshpass -p '0320' ssh csprinks@192.168.1.70

# Sync latest code and deploy
git pull origin main
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### **Mobile Deployment**
```bash
# Android
cd mobile-app/AIBrainframeMobile
npx react-native run-android

# iOS
npx react-native run-ios
```

---

## 🔍 Troubleshooting

### **Common Issues**
- **FastAPI Import Error:** Check virtual environment activation
- **Database Connection:** Verify .env file exists and has correct settings
- **Mobile API Connection:** Check IP address in mobile app configuration
- **Git SSH Issues:** Use HTTPS clone URLs, cache credentials

### **Debug Commands**
```bash
# Check running services
ps aux | grep uvicorn

# Test API connectivity
curl http://localhost:8000/

# Check logs
tail -f logs/app.log  # If logging configured

# Verify environment
source venv/bin/activate && python -c "import fastapi; print('FastAPI OK')"
```

---

## 📧 Support & Contact

### **Project Repository**
- **GitHub:** https://github.com/c-sprinks/ClaudeCode-Projects.git
- **Session Tracking:** `docs/session-history/`
- **Issues:** Document in session history files

### **Key Credentials**
- **Test User:** testtech / password123
- **Server SSH:** csprinks@192.168.1.70 (password: 0320)
- **Sudo Password:** 0320

---

## 📝 Recent Updates

### **October 5, 2025**
- ✅ **Immersive Interface:** Revolutionary LBOB character experience
- ✅ **Project Cleanup:** Organized assets and documentation
- ✅ **Mobile App:** Complete TypeScript React Native implementation
- ✅ **Multi-Machine Sync:** Seamless development across environments

### **Next Development Goals**
- 🔄 Server sync and production deployment
- 📱 Mobile app store distribution
- 🎨 Enhanced LBOB character animations
- 🔒 Production security hardening

---

**Last Updated:** October 5, 2025
**Version:** 2.0.0 - Immersive LBOB Experience
**Documentation Status:** Complete and Current