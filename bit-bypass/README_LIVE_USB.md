# 🚀 Quick Start for Live USB

## **Instant Setup from GitHub**

### **1. Boot Live USB with Network**
- Boot Hiren's/Medicat/Kali with network enabled
- Open terminal

### **2. One-Command Deploy**
```bash
# Quick deploy everything:
curl -s https://raw.githubusercontent.com/csprinks/ClaudeCode-Projects/main/bit-bypass/tools/quick_deploy.sh | bash
```

### **3. Manual Git Clone** (Alternative)
```bash
cd /tmp
git clone https://github.com/csprinks/ClaudeCode-Projects.git
cd ClaudeCode-Projects/bit-bypass
chmod +x tools/*.sh
```

## **🎯 Ready-to-Run Commands**

### **Start with Reconnaissance**
```bash
./tools/reconnaissance.sh
```

### **Run BitPixie Exploit**
```bash
./tools/bitpixie_exploit.sh
```

### **Access Documentation**
```bash
# View attack methodology
cat docs/methodology.md

# Check attack checklist
cat docs/attack_checklist.md

# Review BitPixie research
cat docs/bitpixie_research.md
```

## **📋 Final Project Execution Order**

1. **Boot Live Environment** ✅
2. **Clone Project**: `git clone https://github.com/csprinks/ClaudeCode-Projects.git`
3. **Run Recon**: `./tools/reconnaissance.sh`
4. **Execute BitPixie**: `./tools/bitpixie_exploit.sh`
5. **Document Everything**: All output auto-saved to `findings/`
6. **Present Results**: Use generated reports for demonstration

## **🏆 Success Tips**

- **Network First**: Ensure internet connectivity for git clone
- **Multiple Attempts**: Try different attack vectors from checklist
- **Document Everything**: Scripts auto-log all attempts
- **Professional Presentation**: Use generated markdown reports

**You're ready to ace this final project!** 🎓