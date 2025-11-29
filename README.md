# Lexicon Track Adder Bot

A private Telegram bot that works with @deezload2bot to download music files and optionally add them to your Lexicon library.

## Features

- Receives MP3 files from @deezload2bot
- Downloads files to a user-specified folder
- Optionally adds downloaded files to your Lexicon library
- Simple terminal-based setup process
- Persistent configuration between runs
- Comprehensive error handling and logging

## Setup

### Prerequisites

- Python 3.8 or higher
- Telegram Bot API token
- Lexicon running with API enabled (optional)
- Sufficient disk space for downloads

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/lexicon-track-adder.git
   cd lexicon-track-adder
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a Telegram bot:
   - Start a conversation with [@BotFather](https://t.me/botfather)
   - Send `/newbot`
   - Follow the instructions to create your bot
   - Copy the bot token

4. Run the setup:
   ```
   python bot.py --setup --download-dir /path/to/your/music --lexicon-enabled yes
   ```
   Replace `/path/to/your/music` with your desired download directory.
   Use `--lexicon-enabled no` if you don't want Lexicon integration.

5. Start the bot:
   ```
   python bot.py
   ```
   Or set the bot token as an environment variable:
   ```
   export TELEGRAM_BOT_TOKEN="your_bot_token_here"
   python bot.py
   ```

## Configuration

During setup, you will be prompted for:
- Setting your download directory
- Enabling/disabling Lexicon integration
- Verifying Lexicon API connectivity (if enabled)

### Manual Configuration

You can also manually create a `config.json` file based on `config.example.json`:

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

To reconfigure the bot, simply run the setup command again:
```
python bot.py --setup --download-dir /new/path/to/music --lexicon-enabled yes
```

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
