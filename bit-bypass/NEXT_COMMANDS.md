# Quick Reference - Next Commands to Execute

**Last Updated:** 2025-10-24 21:00
**Status:** Ready to swap USB and restart imaging

---

## 🔄 **Step 1: Swap USB Connections**

### **Physical Action Required:**
1. Unmount drive first (see command below)
2. Unplug Parrot Live USB from laptop USB port
3. Unplug 4TB HDD from USB hub
4. Plug Parrot Live USB into USB hub (connected to USB-C)
5. Plug 4TB HDD directly into laptop USB port
6. Wait 10 seconds

### **Commands:**
```bash
# Unmount before swapping
sudo umount /mnt/backup

# NOW do the physical swap (see above)

# After swap, verify detection
lsblk

# Check USB speed (should see "5000M" for USB 3.0, not "480M")
dmesg | grep -i "usb.*5000\|usb.*480" | tail -5

# Find the 4TB drive (look for "BitLocker-Eviden" label)
sudo blkid | grep "BitLocker-Eviden"

# It should still be /dev/sdd1, but might change
# Mount it (adjust device if needed)
sudo mount /dev/sdd1 /mnt/backup

# Verify mount succeeded
df -h | grep backup
```

---

## 🚀 **Step 2: Start Forensic Imaging**

### **COPY-PASTE THIS COMMAND:**
```bash
sudo dc3dd if=/dev/nvme0n1 of=/mnt/backup/laptop_backup.img \
  hash=md5 hash=sha256 \
  log=/mnt/backup/imaging.log \
  progress=on verb=on
```

### **What You'll See:**
- Scrolling data/text (this is normal!)
- Progress updates
- Transfer speed indicators
- Should complete in 2-3 hours

---

## 📊 **Step 3: Monitor Progress (Optional)**

### **Open a second terminal and run:**
```bash
# Check current file size
ls -lh /mnt/backup/laptop_backup.img

# Watch it grow (updates every 10 seconds)
watch -n 10 'ls -lh /mnt/backup/laptop_backup.img'

# Press Ctrl+C to stop watching
```

### **Calculate Progress:**
- Target size: 477 GB
- Current size: (from ls command)
- Progress: (Current ÷ 477) × 100 = %

---

## ✅ **Step 4: When Imaging Completes**

### **You'll know it's done when:**
- Scrolling stops
- You see "MD5 hash:" and "SHA256 hash:" printed
- Terminal prompt returns

### **Verify completion:**
```bash
# Check final file size (should be ~477 GB)
ls -lh /mnt/backup/laptop_backup.img

# View the imaging log with hashes
cat /mnt/backup/imaging.log

# You should see something like:
# Total bytes: 512110190592
# MD5: [hash]
# SHA256: [hash]
```

---

## 📋 **After Imaging - Next Phase**

When imaging is complete, we'll proceed to BitLocker analysis:
1. Mount the image as loop device
2. Run reconnaissance on BitLocker partition
3. Attempt BitPixie exploit (CVE-2022-34302)
4. Extract encryption keys
5. Mount BitLocker volume
6. Find target .txt file

**See `CURRENT_SESSION_LOG.md` for full details**

---

## 🚨 **Troubleshooting**

### **If drive not detected after swap:**
```bash
# List all USB devices
lsusb

# Check kernel messages
dmesg | tail -30

# List all block devices
lsblk
```

### **If mount fails:**
```bash
# Create mount point if needed
sudo mkdir -p /mnt/backup

# Try mounting with explicit filesystem type
sudo mount -t ext4 /dev/sdd1 /mnt/backup
```

### **If still slow after swap:**
```bash
# Check actual USB connection speed
lsusb -t

# Should show "5000M" for USB 3.0
# If shows "480M" you're still on USB 2.0
```

---

## ⏱️ **Time Estimates**

- **USB swap:** 2-3 minutes
- **Imaging:** 2-3 hours (if USB 3.0 is working properly)
- **Verification:** 1-2 minutes

**Total:** ~2-3 hours for complete forensic backup

---

**Ready to proceed? Start with Step 1 above!**
