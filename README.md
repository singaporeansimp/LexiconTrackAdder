# Lexicon Track Adder Bot

A private Telegram bot that works with @deezload2bot to download music files and optionally add them to your Lexicon library.

## Features

- Receives MP3 files from @deezload2bot
- Downloads files to a user-specified folder
- Optionally adds downloaded files to your Lexicon library
- Simple terminal-based setup process
- Persistent configuration between runs
- Comprehensive error handling and logging

## 📖 Table of Contents

- [Setup Instructions](#setup-instructions)
  - [Prerequisites](#-prerequisites)
  - [macOS Setup](#-setup-for-macos)
  - [Windows Setup](#-setup-for-windows)
  - [Advanced Configuration](#%EF%B8%8F-advanced-configuration)
- [Usage](#usage)
- [Lexicon Integration](#lexicon-integration)
- [Troubleshooting](#troubleshooting)
- [Development](#development)

## Setup Instructions

This guide provides detailed, step-by-step instructions for setting up the Lexicon Track Adder Bot on both **macOS** and **Windows**.

---

## 📋 Prerequisites

Before you begin, ensure you have:
- A Telegram account
- Internet connection
- Sufficient disk space for music downloads (recommended: 10GB+)
- (Optional) Lexicon music player installed with API enabled

---

## 🍎 Setup for macOS

### Step 1: Install Python

1. **Check if Python is already installed:**
   - Open Terminal (press `Cmd + Space`, type "Terminal", and press Enter)
   - Run: `python3 --version`
   - If you see Python 3.8 or higher, skip to Step 2

2. **Install Python using Homebrew (recommended):**
   - Install Homebrew if you don't have it:
     ```bash
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
     ```
   - Install Python:
     ```bash
     brew install python
     ```

3. **Alternative: Download from python.org:**
   - Visit https://www.python.org/downloads/
   - Download the latest Python 3.x installer for macOS
   - Run the installer and follow the prompts

### Step 2: Install Git (if not already installed)

```bash
# Check if Git is installed
git --version

# If not installed, install via Homebrew
brew install git
```

### Step 3: Clone the Repository

```bash
# Navigate to your desired location (e.g., Documents)
cd ~/Documents

# Clone the repository
git clone https://github.com/yourusername/lexicon-track-adder.git

# Navigate into the project directory
cd lexicon-track-adder
```

### Step 4: Install Python Dependencies

```bash
# Install required packages
pip3 install -r requirements.txt
```

### Step 5: Create Your Telegram Bot

1. Open Telegram on your phone or computer
2. Search for and start a conversation with [@BotFather](https://t.me/botfather)
3. Send the command: `/newbot`
4. Follow the prompts:
   - Enter a name for your bot (e.g., "My Music Bot")
   - Enter a unique username ending in 'bot' (e.g., "my_music_downloader_bot")
5. **Copy the bot token** (it looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)
6. Keep this token safe - you'll need it in the next step

### Step 6: Configure the Bot

Run the setup command with your preferred settings:

```bash
# Example: Setup with Lexicon integration
python3 bot.py --setup --download-dir ~/Music/Downloads --lexicon-enabled yes

# Example: Setup without Lexicon integration
python3 bot.py --setup --download-dir ~/Music/Downloads --lexicon-enabled no
```

When prompted, paste your bot token from Step 5.

**Notes:**
- Replace `~/Music/Downloads` with your preferred download directory
- The directory will be created if it doesn't exist
- Use absolute paths for best results (e.g., `/Users/yourusername/Music/Downloads`)

### Step 7: Start the Bot

```bash
python3 bot.py
```

You should see: `Bot started successfully! Send music files from @deezload2bot`

**To run the bot in the background:**
```bash
# Using nohup
nohup python3 bot.py > bot.log 2>&1 &

# To stop the bot later
pkill -f "python3 bot.py"
```

---

## 🪟 Setup for Windows

### Step 1: Install Python

1. **Check if Python is already installed:**
   - Open Command Prompt (press `Win + R`, type "cmd", press Enter)
   - Run: `python --version`
   - If you see Python 3.8 or higher, skip to Step 2

2. **Download and install Python:**
   - Visit https://www.python.org/downloads/
   - Click "Download Python 3.x.x" (latest version)
   - Run the installer
   - **IMPORTANT:** Check the box "Add Python to PATH" at the bottom
   - Click "Install Now"
   - Wait for installation to complete
   - Click "Close"

3. **Verify installation:**
   - Open a new Command Prompt
   - Run: `python --version`
   - You should see the Python version number

### Step 2: Install Git

1. **Download Git:**
   - Visit https://git-scm.com/download/win
   - Download the installer
   - Run the installer with default settings

2. **Verify installation:**
   - Open a new Command Prompt
   - Run: `git --version`

### Step 3: Clone the Repository

```cmd
# Navigate to your desired location (e.g., Documents)
cd %USERPROFILE%\Documents

# Clone the repository
git clone https://github.com/yourusername/lexicon-track-adder.git

# Navigate into the project directory
cd lexicon-track-adder
```

### Step 4: Install Python Dependencies

```cmd
# Install required packages
pip install -r requirements.txt
```

If you encounter "pip is not recognized", try:
```cmd
python -m pip install -r requirements.txt
```

### Step 5: Create Your Telegram Bot

1. Open Telegram on your phone or computer
2. Search for and start a conversation with [@BotFather](https://t.me/botfather)
3. Send the command: `/newbot`
4. Follow the prompts:
   - Enter a name for your bot (e.g., "My Music Bot")
   - Enter a unique username ending in 'bot' (e.g., "my_music_downloader_bot")
5. **Copy the bot token** (it looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)
6. Keep this token safe - you'll need it in the next step

### Step 6: Configure the Bot

Run the setup command with your preferred settings:

```cmd
# Example: Setup with Lexicon integration
python bot.py --setup --download-dir C:\Users\YourUsername\Music\Downloads --lexicon-enabled yes

# Example: Setup without Lexicon integration
python bot.py --setup --download-dir C:\Users\YourUsername\Music\Downloads --lexicon-enabled no
```

When prompted, paste your bot token from Step 5.

**Notes:**
- Replace `C:\Users\YourUsername\Music\Downloads` with your preferred download directory
- Replace `YourUsername` with your actual Windows username
- The directory will be created if it doesn't exist
- Use full paths (e.g., `C:\Music\Downloads` or `D:\Downloads`)

### Step 7: Start the Bot

```cmd
python bot.py
```

You should see: `Bot started successfully! Send music files from @deezload2bot`

**To run the bot in the background:**
1. Create a file named `start_bot.bat` with this content:
   ```batch
   @echo off
   cd %~dp0
   python bot.py
   ```
2. Double-click `start_bot.bat` to start the bot
3. To stop: Close the Command Prompt window

**To run as a startup program:**
1. Press `Win + R`, type `shell:startup`, press Enter
2. Create a shortcut to `start_bot.bat` in this folder
3. The bot will start automatically when Windows starts

---

## ⚙️ Advanced Configuration

### Setting Bot Token as Environment Variable

**macOS/Linux:**
```bash
# Add to ~/.bash_profile or ~/.zshrc
export TELEGRAM_BOT_TOKEN="your_bot_token_here"

# Reload your profile
source ~/.bash_profile  # or source ~/.zshrc

# Run bot without being prompted for token
python3 bot.py
```

**Windows:**
```cmd
# Set for current session
set TELEGRAM_BOT_TOKEN=your_bot_token_here

# Set permanently (requires admin privileges)
setx TELEGRAM_BOT_TOKEN "your_bot_token_here"
```

### Manual Configuration

You can manually create a `config.json` file:

```json
{
  "bot_token": "YOUR_TELEGRAM_BOT_TOKEN_HERE",
  "admin_user_id": 123456789,
  "download_dir": "/path/to/your/music/downloads",
  "lexicon_enabled": true,
  "lexicon_api_url": "http://localhost:48624/v1"
}
```

### Reconfiguration

To change settings later, run setup again:

**macOS:**
```bash
python3 bot.py --setup --download-dir /new/path --lexicon-enabled yes
```

**Windows:**
```cmd
python bot.py --setup --download-dir C:\new\path --lexicon-enabled yes
```

---

## Usage

1. Get an MP3 file from @deezload2bot
2. Forward that file to your private bot
3. The bot will download the file to your specified directory
4. If Lexicon integration is enabled, it will automatically add the file to your library

## Commands

- `/start` - Start the bot
- `/help` - Show help message

## Lexicon Integration

To enable Lexicon integration:

1. Make sure Lexicon is running
2. Enable the API in Lexicon settings under Integrations
3. During bot setup, enable Lexicon integration
4. The bot will test the connection and confirm if successful

## Troubleshooting

### Bot doesn't respond
- Check your bot token is correct
- Ensure the bot is running without errors
- Check the logs for any error messages

### Lexicon integration fails
- Ensure Lexicon is running with API enabled
- Verify the API URL is correct (default: http://localhost:48624/v1)
- Check if Lexicon API is accessible from your network

### File download issues
- Check file permissions for your download directory
- Ensure sufficient disk space
- Verify internet connection

### Configuration issues
- Check `config.json` for syntax errors
- Ensure all required fields are filled
- Verify paths are correct and accessible

## Development

### Running Tests

Run the test suite:
```
python test_bot.py
```

### Project Structure

```
lexicon-track-adder/
├── bot.py              # Main bot implementation
├── config.py           # Configuration management
├── lexicon_client.py   # Lexicon API client
├── utils.py            # Utility functions
├── download_manager.py  # File download management
├── error_handler.py    # Error handling
├── test_bot.py         # Test suite
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── config.example.json # Example configuration
└── .gitignore         # Git ignore file
```

## Privacy

This is a private bot that only responds to the administrator user (the first user to interact with it). No data is shared with third parties.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## Support

If you encounter any issues, please:
1. Check the troubleshooting section
2. Search existing issues
3. Create a new issue with details about your problem
