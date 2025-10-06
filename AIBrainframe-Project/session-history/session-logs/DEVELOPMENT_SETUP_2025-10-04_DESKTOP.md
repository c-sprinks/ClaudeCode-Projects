# AIBrainframe Development Setup

## Quick Start Commands

### Start Backend API
```bash
cd /home/csprinks/ClaudeCode-Projects/AIBrainframe-Project
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Start React Native Development
```bash
cd /home/csprinks/ClaudeCode-Projects/AIBrainframe-Project/mobile-app/AIBrainframeMobile

# Install dependencies (first time only)
npm install

# For Android Development
npm run android

# For iOS Development (macOS only)
npm run ios

# Start Metro bundler
npm start
```

## Android Development Setup (Required)

### 1. Install Java JDK ✅ COMPLETED
```bash
sudo apt update
sudo apt install openjdk-21-jdk
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
```

### 2. Install Android Studio
1. Download from: https://developer.android.com/studio
2. Install with default settings
3. Install Android SDK, Build Tools, and Emulator
4. Create virtual device (Pixel 5 API 33 recommended)

### 3. Set Environment Variables
Add to ~/.bashrc:
```bash
export ANDROID_HOME=$HOME/Android/Sdk
export PATH=$PATH:$ANDROID_HOME/emulator
export PATH=$PATH:$ANDROID_HOME/tools
export PATH=$PATH:$ANDROID_HOME/tools/bin
export PATH=$PATH:$ANDROID_HOME/platform-tools
```

Then reload: `source ~/.bashrc`

### 4. Enable Developer Options on Android Device
1. Settings > About Phone > Build Number (tap 7 times)
2. Developer Options > USB Debugging (enable)
3. Connect device via USB

## Live Development Workflow

### Option 1: Android Emulator
```bash
# Start emulator
emulator -avd <your_avd_name>

# In React Native project
npm run android
```

### Option 2: Physical Android Device
```bash
# Check device connection
adb devices

# In React Native project
npm run android
```

### Option 3: Web Development (Testing)
```bash
# Open web interface
http://localhost:8000/
# Use test_api.html for API testing
```

## API Configuration

The mobile app connects to: `http://localhost:8000`

For testing on physical device, update `API_BASE` in App.tsx to your computer's IP address:
```typescript
const API_BASE = 'http://192.168.1.XXX:8000';  // Replace with your IP
```

## Test Credentials
- Username: `testtech`
- Password: `password123`