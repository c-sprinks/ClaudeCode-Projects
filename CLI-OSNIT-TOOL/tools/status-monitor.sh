#!/bin/bash
#
# Inspector-G Status Monitor
# System status and target tracking
#

# Colors - Professional cybersecurity theme
RED='\033[0;31m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
GRAY='\033[0;90m'
GREEN='\033[0;32m'
DIM='\033[2m'
RESET='\033[0m'

# Clear screen and show header
clear
echo -e "${GRAY}┌──────────────────────────────────────┐${RESET}"
echo -e "${GRAY}│${RESET} ${RED}[${RESET}${WHITE}STATUS${RESET}${RED}]${RESET} ${CYAN}System Monitor${RESET}          ${GRAY}│${RESET}"
echo -e "${GRAY}└──────────────────────────────────────┘${RESET}"
echo ""

# Function to display status
show_status() {
    local timestamp=$(date '+%H:%M:%S')
    local date=$(date '+%Y-%m-%d')

    echo -e "${RED}[${RESET}${WHITE}SYS${RESET}${RED}]${RESET} ${CYAN}System Status${RESET}"
    echo -e "${GRAY}────────────────────────────────────${RESET}"
    echo -e "Time:    ${WHITE}${timestamp}${RESET}"
    echo -e "Date:    ${WHITE}${date}${RESET}"
    echo -e "Status:  ${GREEN}●${RESET} ${WHITE}OPERATIONAL${RESET}"
    echo ""

    echo -e "${RED}[${RESET}${WHITE}TGT${RESET}${RED}]${RESET} ${CYAN}Current Target${RESET}"
    echo -e "${GRAY}────────────────────────────────────${RESET}"
    if [ -f "/tmp/inspector-g-target" ]; then
        local target=$(cat /tmp/inspector-g-target)
        echo -e "Target:  ${RED}$target${RESET}"
    else
        echo -e "Target:  ${GRAY}NO TARGET SET${RESET}"
    fi
    echo -e "Mode:    ${GREEN}READY${RESET}"
    echo ""

    echo -e "${RED}[${RESET}${WHITE}MOD${RESET}${RED}]${RESET} ${CYAN}Module Status${RESET}"
    echo -e "${GRAY}────────────────────────────────────${RESET}"
    echo -e "Neural AI:       ${GREEN}●${RESET} ${WHITE}ONLINE${RESET}"
    echo -e "Username enum:   ${GREEN}●${RESET} ${WHITE}READY${RESET}"
    echo -e "Email intel:     ${GREEN}●${RESET} ${WHITE}READY${RESET}"
    echo -e "Domain recon:    ${GREEN}●${RESET} ${WHITE}READY${RESET}"
    echo -e "Threat detect:   ${GREEN}●${RESET} ${WHITE}ACTIVE${RESET}"
    echo ""

    echo -e "${RED}[${RESET}${WHITE}STATS${RESET}${RED}]${RESET} ${CYAN}Session Statistics${RESET}"
    echo -e "${GRAY}────────────────────────────────────${RESET}"
    echo -e "Operations:      ${WHITE}0${RESET}"
    echo -e "Targets found:   ${WHITE}0${RESET}"
    echo -e "Success rate:    ${WHITE}0%${RESET}"
    echo -e "Uptime:          ${WHITE}$(uptime -p)${RESET}"
}

# Initial status display
show_status

# Update status every 5 seconds
while true; do
    sleep 5
    clear
    echo -e "${GRAY}┌──────────────────────────────────────┐${RESET}"
    echo -e "${GRAY}│${RESET} ${RED}[${RESET}${WHITE}STATUS${RESET}${RED}]${RESET} ${CYAN}System Monitor${RESET}          ${GRAY}│${RESET}"
    echo -e "${GRAY}└──────────────────────────────────────┘${RESET}"
    echo ""
    show_status
done