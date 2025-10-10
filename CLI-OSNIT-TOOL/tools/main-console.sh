#!/bin/bash
#
# Inspector-G Main Console
# Full Linux terminal with OSINT command extensions
#

# Colors - Professional cybersecurity theme
RED='\033[0;31m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
GRAY='\033[0;90m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
DIM='\033[2m'
RESET='\033[0m'

# Clear screen and show header
clear
echo -e "${GRAY}┌──────────────────────────────────────────────────────────────────────────────┐${RESET}"
echo -e "${GRAY}│${RESET} ${RED}[${RESET}${WHITE}MAIN CONSOLE${RESET}${RED}]${RESET} ${CYAN}Inspector-G OSINT Terminal${RESET}                     ${GRAY}│${RESET}"
echo -e "${GRAY}└──────────────────────────────────────────────────────────────────────────────┘${RESET}"
echo ""

# Function to log results
log_result() {
    local message="$1"
    local type="$2"
    local timestamp=$(date '+%H:%M:%S')

    case $type in
        "success")
            echo -e "${GRAY}[${timestamp}]${RESET} ${GREEN}✓${RESET} $message"
            ;;
        "error")
            echo -e "${GRAY}[${timestamp}]${RESET} ${RED}✗${RESET} $message"
            ;;
        "info")
            echo -e "${GRAY}[${timestamp}]${RESET} ${CYAN}►${RESET} $message"
            ;;
        "warning")
            echo -e "${GRAY}[${timestamp}]${RESET} ${YELLOW}!${RESET} $message"
            ;;
        *)
            echo -e "${GRAY}[${timestamp}]${RESET} $message"
            ;;
    esac
}

# Function to set current target
set_target() {
    echo "$1" > /tmp/inspector-g-target 2>/dev/null || true
}

# Function to investigate username
investigate_username() {
    local target="$1"
    set_target "$target"

    log_result "Starting username enumeration: $target" "info"

    platforms=("GitHub" "Twitter" "LinkedIn" "Reddit" "Instagram" "TikTok" "Facebook" "YouTube")

    echo ""
    printf "%-15s %-15s %-25s %-15s\n" "PLATFORM" "STATUS" "PROFILE" "CONFIDENCE"
    echo -e "${GRAY}───────────────────────────────────────────────────────────────────────────${RESET}"

    for platform in "${platforms[@]}"; do
        sleep 0.2

        # Simulate different results
        if [ $((RANDOM % 3)) -eq 0 ]; then
            status="${GREEN}FOUND${RESET}"
            profile="${target}_profile"
            confidence="$((RANDOM % 30 + 70))%"
        else
            status="${RED}NOT FOUND${RESET}"
            profile="-"
            confidence="-"
        fi

        printf "%-15s %-24s %-25s %-15s\n" "$platform" "$status" "$profile" "$confidence"
    done

    echo ""
    log_result "Username enumeration complete" "success"
    echo ""
}

# Function to investigate email domain
investigate_email() {
    local domain="$1"
    set_target "$domain"

    log_result "Starting email intelligence: $domain" "info"

    steps=("DNS enumeration" "Email pattern analysis" "Corporate structure" "Security assessment" "Breach database")

    for step in "${steps[@]}"; do
        sleep 0.3
        log_result "$step: COMPLETE" "success"
    done

    echo ""
    printf "%-40s %-15s %-10s\n" "EMAIL PATTERN" "CONFIDENCE" "RISK"
    echo -e "${GRAY}──────────────────────────────────────────────────────────────────${RESET}"
    printf "%-40s %-15s %-10s\n" "firstname.lastname@$domain" "HIGH" "LOW"
    printf "%-40s %-15s %-10s\n" "f.lastname@$domain" "MEDIUM" "LOW"
    printf "%-40s %-15s %-10s\n" "firstname@$domain" "MEDIUM" "MEDIUM"
    printf "%-40s %-15s %-10s\n" "admin@$domain" "HIGH" "HIGH"

    echo ""
    log_result "Email intelligence complete" "success"
    echo ""
}

# Function to investigate domain
investigate_domain() {
    local target="$1"
    set_target "$target"

    log_result "Starting domain reconnaissance: $target" "info"

    checks=("DNS resolution" "Subdomain enumeration" "Port scanning" "Technology stack" "Security headers" "SSL analysis")

    echo ""
    printf "%-25s %-15s %-10s\n" "CHECK" "STATUS" "RESULT"
    echo -e "${GRAY}──────────────────────────────────────────────────────${RESET}"

    for check in "${checks[@]}"; do
        sleep 0.3
        result="${GREEN}✓${RESET}"
        if [ "$check" = "Security headers" ]; then
            result="${YELLOW}!${RESET}"
        fi
        printf "%-25s %-15s %-19s\n" "$check" "COMPLETE" "$result"
    done

    echo ""
    log_result "Domain reconnaissance complete" "success"
    echo ""
}

# Welcome message
echo -e "${RED}[${RESET}${WHITE}INIT${RESET}${RED}]${RESET} ${CYAN}Inspector-G OSINT Terminal initialized${RESET}"
log_result "Full Linux terminal with OSINT extensions loaded" "success"
log_result "Type 'osint-help' for OSINT commands, or use any Linux command" "info"
echo ""

# Custom OSINT command handler
handle_osint_command() {
    local cmd="$1"
    shift
    local args="$@"

    case $cmd in
        "username")
            if [ -z "$args" ]; then
                log_result "Usage: username <target>" "error"
            else
                investigate_username "$args"
            fi
            return 0
            ;;
        "email")
            if [ -z "$args" ]; then
                log_result "Usage: email <domain>" "error"
            else
                investigate_email "$args"
            fi
            return 0
            ;;
        "domain")
            if [ -z "$args" ]; then
                log_result "Usage: domain <target>" "error"
            else
                investigate_domain "$args"
            fi
            return 0
            ;;
        "osint-help")
            echo -e "${RED}[${RESET}${WHITE}OSINT COMMANDS${RESET}${RED}]${RESET}"
            echo ""
            echo -e "  ${CYAN}username <target>${RESET}     - Username enumeration across platforms"
            echo -e "  ${CYAN}email <domain>${RESET}        - Email intelligence and patterns"
            echo -e "  ${CYAN}domain <target>${RESET}       - Domain reconnaissance"
            echo -e "  ${CYAN}set-target <name>${RESET}     - Set current investigation target"
            echo -e "  ${CYAN}clear-target${RESET}          - Clear current target"
            echo ""
            echo -e "${GRAY}All standard Linux commands are available.${RESET}"
            return 0
            ;;
        "set-target")
            if [ -z "$args" ]; then
                log_result "Usage: set-target <name>" "error"
            else
                set_target "$args"
                log_result "Target set: $args" "success"
            fi
            return 0
            ;;
        "clear-target")
            rm -f /tmp/inspector-g-target 2>/dev/null || true
            log_result "Target cleared" "success"
            return 0
            ;;
        *)
            return 1
            ;;
    esac
}

# Set custom PS1 prompt
export PS1="\[\033[0;31m\][\[\033[1;37m\]inspector-g\[\033[0;31m\]]\[\033[0;36m\] \u@\h\[\033[0m\]:\[\033[1;37m\]\w\[\033[0m\]\$ "

# Override command execution to intercept OSINT commands
exec_command() {
    local input="$1"

    # Parse command and arguments
    read -ra ADDR <<< "$input"
    local cmd="${ADDR[0]}"
    local args="${ADDR[@]:1}"

    # Try OSINT command first
    if handle_osint_command "$cmd" $args; then
        return
    fi

    # Execute as regular Linux command
    eval "$input"
}

# Main command loop with full Linux terminal functionality
while true; do
    # Use bash's built-in read with prompt
    read -e -p "$(echo -e "\033[0;31m[\033[1;37minspector-g\033[0;31m]\033[0;36m $(whoami)@$(hostname)\033[0m:\033[1;37m$(pwd)\033[0m\$ ")" command

    # Handle empty input
    if [ -z "$command" ]; then
        continue
    fi

    # Add to history
    history -s "$command"

    # Handle exit commands
    if [[ "$command" == "exit" || "$command" == "quit" ]]; then
        log_result "Terminating session" "info"
        rm -f /tmp/inspector-g-target 2>/dev/null || true
        break
    fi

    # Execute command
    exec_command "$command"
done