#!/bin/bash
#
# Quick Deploy Script for Live USB Environment
# Git clone and instant setup for BitLocker bypass testing
#

# Colors
GREEN='\033[0;32m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
RESET='\033[0m'

echo -e "${CYAN}╔══════════════════════════════════════════════════════════════╗${RESET}"
echo -e "${CYAN}║${RESET} ${WHITE}BitLocker Bypass - Quick Deploy from GitHub${RESET}             ${CYAN}║${RESET}"
echo -e "${CYAN}╚══════════════════════════════════════════════════════════════╝${RESET}"
echo ""

# Update system and install essential tools
echo -e "${WHITE}Installing essential tools...${RESET}"
apt update && apt install -y git curl wget hexdump python3-volatility

# Clone the project (replace with your actual GitHub repo)
echo -e "${WHITE}Cloning bit-bypass project...${RESET}"
cd /tmp
git clone https://github.com/csprinks/ClaudeCode-Projects.git
cd ClaudeCode-Projects/bit-bypass

# Make scripts executable
chmod +x tools/*.sh

# Quick system check
echo -e "${WHITE}Running quick reconnaissance...${RESET}"
./tools/reconnaissance.sh

echo -e "${GREEN}✅ Deploy complete! Ready for BitLocker bypass testing.${RESET}"
echo -e "${WHITE}Available tools:${RESET}"
echo "  ./tools/reconnaissance.sh     - System analysis"
echo "  ./tools/bitpixie_exploit.sh   - BitPixie CVE-2022-34302"
echo "  docs/                         - Complete documentation"