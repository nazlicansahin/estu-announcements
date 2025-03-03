# ESTÜ Announcement Bot

This project is a bot application that fetches announcements from the following Eskişehir Technical University websites and sends them via Telegram:

- Eskişehir Technical University (ESTÜ) Main Page  
- ESTÜ Department of Computer Engineering  
- ESTÜ International Relations Office  

## Features

- Automatically fetches announcements from specified websites  
- Detects new announcements and prevents resending  
- Sends announcements to your desired Telegram chat/channel  
- Sends an info message if no new announcements are found  
- Runs automatically every day  
- User-friendly and informative message format  
- Comprehensive error handling and logging  

## Installation

1. Clone this repository:  
```bash
git clone https://github.com/username/estu-announcements.git
cd estu-announcements
```

2. Install the required Python packages:  
```bash
pip install -r requirements.txt
```

3. Copy the `.env.example` file as `.env` and edit it:  
```bash
cp .env.example .env
```

4. Open the `.env` file with a text editor and add the required values:  
   - `TELEGRAM_TOKEN`: Your bot token obtained from Telegram BotFather  
   - `TELEGRAM_CHAT_ID`: The chat or channel ID where messages will be sent  

## Creating a Telegram Bot  

1. Start a chat with [@BotFather](https://t.me/botfather) on Telegram  
2. Send the `/newbot` command and follow the instructions  
3. After creating the bot, BotFather will provide you with a token. Add this token to the `.env` file.  

## Finding Chat ID  

- **For personal chats:** Start a conversation with [@userinfobot](https://t.me/userinfobot), and it will give you your ID.  
- **For channels:** If you know your channel username (e.g., @mychannel), add your bot as an admin and send a message to the channel. Then, visit:  
  `https://api.telegram.org/bot<BOT_TOKEN>/getUpdates`  
  This will provide you with the channel ID.  

## Usage  

To run the script manually:  

```bash
python scraper.py
```

- The script will fetch new announcements and send them via Telegram  
- Previously sent announcements will not be resent  
- If no new announcements are found, an info message will be sent for each source  
- Logs will be saved in the `scraper.log` file  

## Automated Daily Execution  

The bot can be configured to run automatically every day.  

### For Windows Users  

To schedule automatic execution using Task Scheduler:  

1. Use the `daily_run.bat` file in the project's root directory  
2. Create a daily task in Windows Task Scheduler  
3. Check the `TASK_SCHEDULER_SETUP.md` file in the project for detailed instructions  

### For Linux/Mac Users  

To schedule automatic execution using Cron:  

```bash
# Runs every day at 08:00 AM
0 8 * * * cd /path/to/estu-announcements && python scraper.py
```

## Testing  

To test the setup:  

1. Run the script manually: `python scraper.py`  
2. Check if you receive messages on Telegram  
3. On Windows, run `daily_run.bat` directly to test the scheduler setup  

## Contributing  

We welcome contributions! Please open a pull request or share your suggestions.  

## License  

This project is licensed under the MIT License. For more details, check the `LICENSE` file.

