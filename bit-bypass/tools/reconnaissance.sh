#!/bin/bash
#
# BitLocker Bypass - Reconnaissance Toolkit
# Educational cybersecurity project - authorized use only
#

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
GRAY='\033[0;90m'
RESET='\033[0m'

# Create output directory
OUTPUT_DIR="findings/reconnaissance_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$OUTPUT_DIR"

echo -e "${CYAN}╔══════════════════════════════════════════════════════════════╗${RESET}"
echo -e "${CYAN}║${RESET} ${WHITE}BitLocker Bypass - System Reconnaissance Tool${RESET}            ${CYAN}║${RESET}"
echo -e "${CYAN}║${RESET} ${GRAY}Educational Project - Authorized Use Only${RESET}                ${CYAN}║${RESET}"
echo -e "${CYAN}╚══════════════════════════════════════════════════════════════╝${RESET}"
echo ""

log_finding() {
    local message="$1"
    local level="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')

    case $level in
        "SUCCESS")
            echo -e "${GREEN}[✓]${RESET} $message"
            echo "[$timestamp] SUCCESS: $message" >> "$OUTPUT_DIR/reconnaissance.log"
            ;;
        "WARNING")
            echo -e "${YELLOW}[!]${RESET} $message"
            echo "[$timestamp] WARNING: $message" >> "$OUTPUT_DIR/reconnaissance.log"
            ;;
        "ERROR")
            echo -e "${RED}[✗]${RESET} $message"
            echo "[$timestamp] ERROR: $message" >> "$OUTPUT_DIR/reconnaissance.log"
            ;;
        "INFO")
            echo -e "${BLUE}[i]${RESET} $message"
            echo "[$timestamp] INFO: $message" >> "$OUTPUT_DIR/reconnaissance.log"
            ;;
    esac
}

# Function to check hardware information
check_hardware() {
    echo -e "${WHITE}═══ Hardware Information ═══${RESET}"

    log_finding "Collecting hardware information..." "INFO"

    if command -v dmidecode &> /dev/null; then
        log_finding "DMI decode available" "SUCCESS"
        sudo dmidecode -t system > "$OUTPUT_DIR/system_info.txt" 2>/dev/null
        sudo dmidecode -t bios > "$OUTPUT_DIR/bios_info.txt" 2>/dev/null
        sudo dmidecode -t memory > "$OUTPUT_DIR/memory_info.txt" 2>/dev/null
    else
        log_finding "DMI decode not available" "WARNING"
    fi

    # CPU information
    log_finding "Collecting CPU information..." "INFO"
    cat /proc/cpuinfo > "$OUTPUT_DIR/cpu_info.txt"

    # Memory information
    log_finding "Collecting memory information..." "INFO"
    cat /proc/meminfo > "$OUTPUT_DIR/memory_details.txt"
    free -h > "$OUTPUT_DIR/memory_usage.txt"

    # Storage devices
    log_finding "Identifying storage devices..." "INFO"
    lsblk > "$OUTPUT_DIR/block_devices.txt"
    sudo fdisk -l > "$OUTPUT_DIR/disk_layout.txt" 2>/dev/null

    echo ""
}

# Function to check for encryption
check_encryption() {
    echo -e "${WHITE}═══ Encryption Detection ═══${RESET}"

    log_finding "Scanning for encrypted volumes..." "INFO"

    # Check for LUKS volumes
    if command -v cryptsetup &> /dev/null; then
        log_finding "Cryptsetup available - checking for LUKS volumes" "INFO"
        sudo blkid | grep -i luks > "$OUTPUT_DIR/luks_volumes.txt"
    fi

    # Check for BitLocker signatures
    log_finding "Checking for BitLocker signatures..." "INFO"
    sudo hexdump -C /dev/sda | head -20 > "$OUTPUT_DIR/disk_header.txt" 2>/dev/null

    # Mount point analysis
    log_finding "Analyzing current mount points..." "INFO"
    mount > "$OUTPUT_DIR/mount_points.txt"
    df -h > "$OUTPUT_DIR/filesystem_usage.txt"

    echo ""
}

# Function to check boot environment
check_boot_environment() {
    echo -e "${WHITE}═══ Boot Environment Analysis ═══${RESET}"

    log_finding "Analyzing boot configuration..." "INFO"

    # EFI variables (if available)
    if [ -d "/sys/firmware/efi" ]; then
        log_finding "EFI system detected" "SUCCESS"
        efibootmgr > "$OUTPUT_DIR/efi_boot_entries.txt" 2>/dev/null
        ls -la /sys/firmware/efi/efivars/ > "$OUTPUT_DIR/efi_variables.txt" 2>/dev/null
    else
        log_finding "Legacy BIOS system" "INFO"
    fi

    # Kernel modules
    log_finding "Checking loaded kernel modules..." "INFO"
    lsmod > "$OUTPUT_DIR/kernel_modules.txt"

    # TPM detection
    if [ -d "/sys/class/tpm" ]; then
        log_finding "TPM detected" "SUCCESS"
        ls -la /sys/class/tpm/ > "$OUTPUT_DIR/tpm_info.txt"
        cat /sys/class/tpm/tpm*/device/description > "$OUTPUT_DIR/tpm_description.txt" 2>/dev/null
    else
        log_finding "No TPM detected" "WARNING"
    fi

    echo ""
}

# Function to check network and USB devices
check_peripherals() {
    echo -e "${WHITE}═══ Peripheral Device Analysis ═══${RESET}"

    log_finding "Scanning USB devices..." "INFO"
    lsusb > "$OUTPUT_DIR/usb_devices.txt"

    log_finding "Checking PCI devices..." "INFO"
    lspci > "$OUTPUT_DIR/pci_devices.txt"

    log_finding "Network interface analysis..." "INFO"
    ip addr show > "$OUTPUT_DIR/network_interfaces.txt"

    echo ""
}

# Function to generate summary report
generate_summary() {
    echo -e "${WHITE}═══ Generating Summary Report ═══${RESET}"

    local summary_file="$OUTPUT_DIR/RECONNAISSANCE_SUMMARY.md"

    cat > "$summary_file" << EOF
# System Reconnaissance Summary
**Generated**: $(date)
**Target**: $(hostname)
**Operator**: $(whoami)

## Key Findings

### Hardware Configuration
- **System**: $(dmidecode -s system-product-name 2>/dev/null || echo "Unknown")
- **Manufacturer**: $(dmidecode -s system-manufacturer 2>/dev/null || echo "Unknown")
- **BIOS**: $(dmidecode -s bios-version 2>/dev/null || echo "Unknown")
- **Memory**: $(free -h | awk '/^Mem:/ {print $2}')

### Storage Analysis
$(lsblk | while read line; do echo "- $line"; done)

### Security Features Detected
EOF

    if [ -d "/sys/firmware/efi" ]; then
        echo "- ✅ UEFI Secure Boot capability" >> "$summary_file"
    else
        echo "- ❌ Legacy BIOS (no Secure Boot)" >> "$summary_file"
    fi

    if [ -d "/sys/class/tpm" ]; then
        echo "- ✅ TPM detected" >> "$summary_file"
    else
        echo "- ❌ No TPM detected" >> "$summary_file"
    fi

    cat >> "$summary_file" << EOF

### Recommended Attack Vectors
Based on reconnaissance findings:

1. **Boot Environment Manipulation**
   - Target identified boot configuration
   - Test alternative boot methods

2. **Hardware-Based Attacks**
   - Physical access opportunities identified
   - Memory analysis potential

3. **Software-Based Bypass**
   - Recovery environment testing
   - Live boot analysis

### Next Steps
1. Attempt non-destructive software methods first
2. Progress to hardware analysis if needed
3. Document all attempts thoroughly
4. Maintain evidence chain of custody

---
*This reconnaissance was conducted as part of an authorized educational cybersecurity exercise.*
EOF

    log_finding "Summary report generated: $summary_file" "SUCCESS"
    echo ""
}

# Main execution
main() {
    log_finding "Starting system reconnaissance..." "INFO"
    log_finding "Output directory: $OUTPUT_DIR" "INFO"
    echo ""

    check_hardware
    check_encryption
    check_boot_environment
    check_peripherals
    generate_summary

    echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${RESET}"
    echo -e "${GREEN}║${RESET} ${WHITE}Reconnaissance Complete${RESET}                                  ${GREEN}║${RESET}"
    echo -e "${GREEN}║${RESET} ${GRAY}Results saved to: $OUTPUT_DIR${RESET}"
    echo -e "${GREEN}║${RESET} ${GRAY}Review findings before proceeding to active testing${RESET}     ${GREEN}║${RESET}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${RESET}"
}

# Check for proper authorization
echo -e "${YELLOW}⚠️  AUTHORIZATION CHECK ⚠️${RESET}"
echo "This tool is for authorized educational cybersecurity testing only."
echo "Ensure you have explicit permission to test the target system."
echo ""
read -p "Do you have authorization to test this system? (yes/no): " auth_check

if [[ $auth_check == "yes" ]]; then
    main
else
    echo -e "${RED}❌ Authorization not confirmed. Exiting.${RESET}"
    exit 1
fi