# NeoTrace OSINT Suite - CLI-OSNIT-TOOL

> **Ultimate OSINT Desktop Application** - A comprehensive Open Source Intelligence toolkit with AI integration and sleek terminal interface.

## 🎯 Project Vision

NeoTrace is a state-of-the-art OSINT desktop application that combines the power of traditional terminal-based reconnaissance tools with modern AI analysis and an intuitive desktop interface. Designed as an advanced school project demonstrating OSINT mastery, Python proficiency, and AI integration.

### Key Innovation
- **Terminal-Style UI**: Professional hacker terminal aesthetics with fade/recall functionality
- **AI-Powered Analysis**: Local LLM integration for intelligent data interpretation
- **Desktop Interactivity**: Borderless window that fades gracefully and recalls on hotkeys
- **Ethical Framework**: Built-in safeguards and mock data modes for educational demonstration

## 🚀 Features

### Core OSINT Modules
- **Username Enumeration** (Sherlock-style): Scan 400+ sites with AI risk scoring
- **Email Harvesting** (theHarvester): Domain reconnaissance with phishing risk analysis
- **Phone Intelligence** (PhoneInfoga): Carrier, location, and social media footprints
- **Domain/IP Scanning** (SpiderFoot/Recon-ng): Comprehensive network reconnaissance
- **Social Media Analysis** (Osintgram): Deep social profiling with sentiment analysis
- **Breach Detection** (HaveIBeenPwned): Data leak verification with impact prediction
- **AI Query Engine**: Natural language OSINT requests with automated routing

### Desktop Experience
- **Sleek Terminal UI**: Borderless, full-screen optional, matrix-style aesthetics
- **Smart Fade/Recall**: Auto-fades on external app focus, recalls on shortcuts
- **Keyboard Shortcuts**: Ctrl+Alt+O (toggle), Ctrl+R (run), Ctrl+C (copy)
- **Clickable Output**: Direct browser integration and export capabilities

### AI Integration
- **Local LLM** (Ollama): Privacy-focused analysis with fine-tuned OSINT prompts
- **Natural Language Queries**: "Find connections between username and company"
- **Threat Prediction**: Risk scoring and impact analysis
- **Automated Synthesis**: Convert raw data into actionable intelligence

## 🛠️ Technology Stack

### Core Framework
- **Python 3.12+**: Primary development language
- **Textual/Urwid**: Advanced terminal UI framework
- **PyQt6**: Desktop window management and global hotkeys
- **Ollama**: Local LLM for AI processing
- **LangChain**: AI tool chaining and query routing

### OSINT Libraries
- **Sherlock**: Username reconnaissance across platforms
- **theHarvester**: Email and domain intelligence gathering
- **PhoneInfoga**: Phone number OSINT analysis
- **SpiderFoot**: Automated reconnaissance framework
- **Recon-ng**: Modular reconnaissance framework
- **HaveIBeenPwned API**: Data breach verification

### Additional Components
- **Rich**: Advanced terminal formatting and styling
- **Requests/BeautifulSoup**: Web scraping and API integration
- **Vosk/PyAudio**: Voice command integration (optional)
- **PyInstaller**: Cross-platform executable packaging

## 📋 Development Roadmap

### Phase 1: Core Infrastructure (Week 1)
- [ ] Project setup and environment configuration
- [ ] Borderless PyQt window with Textual integration
- [ ] Basic command prompt and output display
- [ ] Fade/recall functionality with global hotkeys

### Phase 2: OSINT Module Integration (Weeks 2-3)
- [ ] Sherlock username enumeration integration
- [ ] theHarvester email reconnaissance
- [ ] PhoneInfoga phone intelligence
- [ ] Basic output formatting and link handling

### Phase 3: AI Integration (Week 4)
- [ ] Ollama LLM setup and configuration
- [ ] LangChain query routing implementation
- [ ] Natural language command processing
- [ ] Automated analysis and risk scoring

### Phase 4: Polish and Features (Week 5)
- [ ] Advanced UI effects and animations
- [ ] Voice command integration
- [ ] Export functionality (PDF/CSV)
- [ ] Comprehensive testing and documentation

### Phase 5: Future Enhancements
- [ ] 3D visualization integration
- [ ] Dark web reconnaissance modules
- [ ] Mobile companion application
- [ ] Advanced threat intelligence feeds

## ⚖️ Ethical Considerations

### Educational Framework
- **Mock Data Modes**: Safe demonstration environments for academic review
- **Consent Prompts**: User acknowledgment for all reconnaissance activities
- **Rate Limiting**: Respectful API usage to prevent service disruption
- **Audit Logging**: Comprehensive activity tracking for academic evaluation

### Security Best Practices
- **Local Processing**: AI analysis performed locally for privacy
- **No Data Persistence**: Optional data storage with explicit user consent
- **Proxy Support**: Anonymous reconnaissance capabilities
- **Legal Compliance**: Built-in warnings for jurisdictional considerations

## 🚀 Quick Start

### Installation
```bash
# Clone repository
git clone [repository-url]
cd CLI-OSNIT-TOOL

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install system dependencies (Debian/Ubuntu)
sudo apt install recon-ng theharvester tesseract-ocr portaudio19-dev

# Setup Ollama for AI features
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama3
```

### Basic Usage
```bash
# Launch NeoTrace OSINT Suite
python neotrace.py

# Username reconnaissance
neo username john.doe

# Email harvesting
neo email target.com

# AI-powered analysis
neo ai "Analyze threat level for user data"

# Phone intelligence
neo phone +1-555-1234

# Domain reconnaissance
neo domain example.com
```

### Keyboard Shortcuts
- **Ctrl+Alt+O**: Toggle window visibility
- **Ctrl+R**: Execute command
- **Ctrl+C**: Copy output to clipboard
- **Esc**: Clear current command
- **F1**: Help and command reference

## 📚 Project Structure

```
CLI-OSNIT-TOOL/
├── neotrace.py              # Main application entry point
├── requirements.txt         # Python dependencies
├── README.md               # Project documentation
├── src/
│   ├── core/               # Core application framework
│   ├── modules/            # OSINT reconnaissance modules
│   ├── ai/                 # AI integration and analysis
│   ├── ui/                 # Terminal and desktop UI components
│   └── utils/              # Shared utilities and helpers
├── tests/                  # Unit and integration tests
├── docs/                   # Additional documentation
└── assets/                 # Resources and configuration files
```

## 🎓 Academic Value

### Learning Objectives
- **OSINT Mastery**: Comprehensive understanding of reconnaissance techniques
- **Python Proficiency**: Advanced application development and library integration
- **AI Integration**: Practical implementation of local LLM processing
- **Security Awareness**: Ethical hacking and privacy considerations
- **Software Engineering**: Modular design, testing, and documentation

### Demonstration Features
- **Live OSINT**: Real-time reconnaissance on approved targets
- **AI Analysis**: Intelligent data interpretation and risk assessment
- **Technical Depth**: Advanced Python programming and framework integration
- **Ethical Framework**: Responsible disclosure and educational safeguards

## 🔮 Future Vision

NeoTrace represents the evolution of OSINT tooling - combining the analytical power of traditional reconnaissance with the intelligence of modern AI and the usability of contemporary desktop applications. This project demonstrates not just technical capability, but a thoughtful approach to ethical intelligence gathering in an educational context.

### Innovation Highlights
- **Seamless Integration**: Traditional OSINT tools unified under intelligent interface
- **AI-Enhanced Analysis**: Raw data transformed into actionable intelligence
- **Privacy-First Design**: Local processing ensures sensitive data protection
- **Educational Focus**: Designed specifically for academic demonstration and learning

---

**Status**: 📋 Project Specification Complete - Ready for Implementation
**Next Phase**: Core Infrastructure Development (Phase 1)
**Timeline**: 4-6 weeks to MVP, additional polish as desired

*This project combines inspiration from leading OSINT tools (Sherlock, Maltego, SpiderFoot) with modern AI capabilities and innovative desktop interaction patterns to create something truly unique in the OSINT landscape.*