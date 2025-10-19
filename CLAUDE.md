# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Structure

This is a multi-project repository containing three main projects:

### 1. AIBrainframe-Project
- **Type**: FastAPI backend + React Native mobile app + Web interface
- **Purpose**: AI-powered building safety assistant with LBOB character
- **Location**: `AIBrainframe-Project/`
- **Technologies**: Python 3.13+, FastAPI, React Native, TypeScript

### 2. CLI-OSNIT-TOOL
- **Type**: Terminal-based OSINT toolkit (Inspector-G)
- **Purpose**: Educational OSINT reconnaissance tools
- **Location**: `CLI-OSNIT-TOOL/`
- **Technologies**: Native terminal applications, shell scripts

### 3. nikki-project
- **Type**: Professional competitive research and intelligence solutions
- **Purpose**: Business intelligence analysis with interactive presentations
- **Location**: `nikki-project/`
- **Technologies**: HTML5, CSS3, JavaScript, Chart.js, GSAP

## Essential Commands

### AIBrainframe-Project Development

#### Backend (FastAPI)
```bash
cd AIBrainframe-Project
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Mobile App (React Native)
```bash
cd AIBrainframe-Project/mobile-app/AIBrainframeMobile
npm start                    # Start Metro bundler
npm run android             # Run on Android
npm run ios                 # Run on iOS
npm test                    # Run tests
npm run lint                # Run ESLint
npm run build:android       # Build Android APK
npm run build:ios           # Build iOS archive
```

#### Testing and Development
```bash
# Test API endpoints
curl http://localhost:8000/
curl http://localhost:8000/docs

# Test with credentials: testtech / password123
curl -X POST http://localhost:8000/users/login \
  -H "Content-Type: application/json" \
  -d '{"username": "testtech", "password": "password123"}'

# Python testing (when available)
cd AIBrainframe-Project
pytest
```

### CLI-OSNIT-TOOL Development

#### Launch Inspector-G
```bash
cd CLI-OSNIT-TOOL
./launch-inspector-g.sh      # Launch 3-window terminal suite
./inspector-g               # Direct launcher
```

### nikki-project Development

#### View Interactive Presentations
```bash
cd nikki-project/client-portfolios/client1-fire-alarm-systems
# Open Client1_Professional_Presentation.html in browser
python3 -m http.server 8080  # Serve locally if needed
```

#### Access Deliverables
- Interactive Presentation: `Client1_Professional_Presentation.html`
- Executive Dashboard: `Client1_FireAlarm_Dashboard.csv`
- PowerPoint Format: `Client1_FireAlarm_Presentation.pptx`
- Comprehensive Report: `Client1_FireAlarm_Report.pdf`

## Project Architecture

### AIBrainframe-Project Architecture

**Backend (FastAPI)**
- `app/main.py` - Main application entry point
- `app/models.py` - SQLAlchemy database models
- `app/auth.py` - JWT authentication system
- `app/ai_service.py` - AI integration (Ollama/LangChain)
- `app/routes/` - API endpoint definitions
- `app/schemas.py` - Pydantic data models

**Database**
- Development: SQLite (`aibrainframe.db`)
- Production: PostgreSQL (configured via environment)

**Mobile App Structure**
- TypeScript React Native 0.72.6
- Navigation: React Navigation 6
- Authentication: JWT with AsyncStorage
- Network: Configurable API base URL

**Character System (LBOB)**
- Interactive AI assistant character
- Multiple visual variations in `assets/images/characters/`
- Integrated across web and mobile interfaces

### Multi-Environment Setup

**Development Machines**
- Desktop (192.168.1.247): Primary development
- Laptop: Secondary/testing environment
- Server (192.168.1.70): Production deployment

**Environment Variables** (`.env` file required)
```bash
DB_HOST=localhost
DB_NAME=aibrainframe_db
DB_USER=aibrainframe_user
DB_PASSWORD=0320
USE_POSTGRES=false
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Development Workflow

### Starting Development Session
1. Check current machine: `uname -a`
2. Check git status: `git status`
3. Activate environment: `source venv/bin/activate` (for Python projects)
4. Start services as needed

### Testing Interfaces
- Web App: `http://localhost:8000/simple_lbob.html`
- API Docs: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

### Remote Server Access
```bash
# SSH to production server
sshpass -p '0320' ssh csprinks@192.168.1.70

# Server has Ollama + Llama 3.1:8b for AI integration
```

## Key Technologies & Dependencies

### Python Stack (AIBrainframe)
- FastAPI 0.116.1 with Uvicorn
- SQLAlchemy 2.0.43 + Alembic migrations
- JWT auth with Argon2 password hashing
- LangChain + Ollama integration
- ChromaDB for vector storage
- Pytest for testing

### Mobile Stack
- React Native 0.72.6 with TypeScript 4.8.4
- React Navigation 6
- AsyncStorage for local data
- Vector icons and animations

### CLI-OSNIT-TOOL Stack
- Native terminal applications
- Shell scripts for window management
- Simple, reliable approach without TUI libraries

## Common Development Tasks

### Adding New API Endpoints
1. Define route in `app/routes/`
2. Add schema in `app/schemas.py`
3. Update models if database changes needed
4. Test via `/docs` interface

### Mobile Development
1. Ensure Metro bundler is running (`npm start`)
2. Use `npx react-native doctor` to verify environment
3. Test on device or emulator
4. Update API base URL for different environments

### Database Changes
1. Modify models in `app/models.py`
2. Generate migration: `alembic revision --autogenerate -m "description"`
3. Apply migration: `alembic upgrade head`

## Credentials & Access

### Test User
- Username: `testtech`
- Password: `password123`

### Server Access
- SSH: `csprinks@192.168.1.70`
- Password: `0320`
- Sudo password: `0320`

## Git Workflow

Repository uses main branch as primary. Standard workflow:
```bash
git add .
git commit -m "Description"
git push origin main
```

Session documentation stored in:
- `AIBrainframe-Project/docs/session-history/`
- `nikki-project/docs/session-history/`