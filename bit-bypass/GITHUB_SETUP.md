# GitHub Setup Instructions

## Create New Repository on GitHub

1. **Go to**: https://github.com/new
2. **Repository name**: `bit-bypass`
3. **Description**: `BitLocker Bypass - Cybersecurity Final Project`
4. **Set to**: Public or Private (your choice)
5. **Don't initialize** with README (we already have one)
6. **Click**: "Create repository"

## Push Local Project to GitHub

After creating the repository, run these commands:

```bash
# Add your GitHub repository as remote origin
git remote add origin https://github.com/YOUR_USERNAME/bit-bypass.git

# Push to GitHub
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

## Alternative: Add to Existing Repository

If you want to add this to your existing ClaudeCode-Projects repository:

```bash
# Copy bit-bypass folder to existing repo
cp -r /home/csprinks/ClaudeCode-Projects/bit-bypass /path/to/existing/ClaudeCode-Projects/

# Then commit and push from there
```

## Quick Deploy Command Update

Once uploaded, your quick deploy command will be:

```bash
# From live USB:
git clone https://github.com/YOUR_USERNAME/bit-bypass.git
cd bit-bypass
chmod +x tools/*.sh
./tools/reconnaissance.sh
```

## Verification

After pushing, check that these files are visible on GitHub:
- README.md
- docs/methodology.md
- docs/attack_checklist.md
- docs/bitpixie_research.md
- tools/reconnaissance.sh
- tools/bitpixie_exploit.sh