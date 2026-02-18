# Quick Start Guide
## Player Verification and Anti-Cheating System

This guide will get you up and running in 5 minutes!

---

## Prerequisites

✅ Python 3.7 or higher installed  
✅ Webcam connected and working  
✅ Internet connection  

---

## Installation (Choose Your OS)

### 🪟 Windows

1. **Open Command Prompt** in the project directory

2. **Run the setup script:**
   ```cmd
   setup.bat
   ```

3. **Follow the prompts** to create an admin account

### 🐧 Linux / 🍎 macOS

1. **Open Terminal** in the project directory

2. **Make setup script executable:**
   ```bash
   chmod +x setup.sh
   ```

3. **Run the setup script:**
   ```bash
   ./setup.sh
   ```

4. **Follow the prompts** to create an admin account

### 📦 Manual Installation

If the scripts don't work, follow these steps:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Initialize database
cd server
python models.py
cd ..

# 3. Create admin account
cd scripts
python create_admin.py --interactive
cd ..
```

---

## First Run - Testing Everything Works

### Step 1: Start the Server

**Terminal/Command Prompt:**
```bash
cd server
python app.py
```

**You should see:**
```
============================================================
Player Verification System - Server Starting
============================================================
Server URL: http://localhost:5000
Admin Dashboard: http://localhost:5000/admin/login
============================================================
```

**Keep this terminal open!**

---

### Step 2: Register a Test Player

**Open a NEW terminal/command prompt:**

```bash
cd client
python registration_gui.py
```

**What to do:**

1. ✅ Check the consent checkbox
2. 📝 Enter your name (e.g., "Test Player")
3. 🆔 Enter a student ID (e.g., "12345")
4. 📸 Click "Capture Facial Data"
   - Press SPACE when your face is in the green box
   - Do this 5 times from different angles
5. 💻 Click "Get Device Fingerprint"
6. ✅ Click "Complete Registration"

**Save your Player ID!** It's in `player_credentials.txt`

---

### Step 3: Test Verification

**Open another NEW terminal/command prompt:**

```bash
cd client
python player_client.py
```

**What to do:**

1. 🆔 Enter your Player ID when prompted
2. ▶️ Click "Start Verification"
3. 👀 Watch the status - it should show "VERIFIED" in green!

---

### Step 4: Check Admin Dashboard

1. 🌐 Open your browser
2. 📍 Go to: **http://localhost:5000/admin/login**
3. 🔑 Login with the admin credentials you created
4. 📊 You should see your verification appear in real-time!

---

## Common First-Run Issues

### ❌ "Camera not found"
**Solution:** 
- Make sure your webcam is plugged in
- Close other apps using the camera (Zoom, Skype, etc.)
- Try running as administrator

### ❌ "Module not found" errors
**Solution:**
```bash
pip install -r requirements.txt --upgrade
```

### ❌ Face recognition fails
**Solution:**
- Improve lighting - face the light
- Remove glasses if possible
- Keep face centered in camera

### ❌ "Connection refused" when registering
**Solution:**
- Make sure the server is running (Step 1)
- Check the server URL in registration GUI is: `http://localhost:5000`

---

## What to Do Next

### For Your Research/Demo:

1. **Register Multiple Players:**
   - Run `registration_gui.py` for each participant
   - Have them use their own devices for realistic testing

2. **Simulate a Tournament:**
   - Have players run `player_client.py` simultaneously
   - Monitor all of them from the admin dashboard

3. **Test Anti-Cheating:**
   - Have someone try to use another player's account
   - Watch it fail verification!
   - Check the captured images in `logs/images/`

4. **Generate More Admin Accounts:**
   ```bash
   cd scripts
   python create_admin.py --username admin2 --email admin2@test.com --role tournament_admin
   ```

---

## System Architecture Overview

```
┌─────────────────┐
│  Player Client  │  ← Runs on player's computer
│  (player_client)│     - Captures face via webcam
│                 │     - Sends to server every 30s
└────────┬────────┘
         │
         │ HTTP/WebSocket
         ▼
┌─────────────────┐
│  Flask Server   │  ← Central verification service
│  (app.py)       │     - Facial recognition
│                 │     - Device fingerprinting
└────────┬────────┘     - Logs everything
         │
         │ WebSocket Updates
         ▼
┌─────────────────┐
│ Admin Dashboard │  ← Web interface for monitoring
│  (Browser)      │     - Real-time status
│                 │     - Verification history
└─────────────────┘     - Player management
```

---

## File Locations

📁 **Important Files:**
- `player_credentials.txt` - Your player ID (created after registration)
- `database/verification_system.db` - All player and log data
- `logs/images/` - Captured verification images

---

## Getting Help

1. 📖 Read the full `README.md`
2. 🐛 Check the troubleshooting section
3. 📝 Review the system design document
4. 💻 Check server console for error messages

---

## Quick Command Reference

```bash
# Start server
cd server && python app.py

# Register player
cd client && python registration_gui.py

# Run verification
cd client && python player_client.py

# Create admin account
cd scripts && python create_admin.py --interactive

# Reset database
cd database && rm verification_system.db && cd ../server && python models.py
```

---

**You're all set! 🎉**

The system is now running and ready for your research project or tournament!
