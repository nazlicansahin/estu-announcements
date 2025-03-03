# Windows Task Scheduler Setup Instructions

This document explains how to configure Windows Task Scheduler to run the ESTU Announcement Bot automatically every day.

## Prerequisites

1. Ensure that Python is installed on your computer
2. Make sure the bot files are fully configured (especially the `.env` file)
3. Confirm that the required dependencies are installed: `pip install -r requirements.txt`

## Task Scheduler Setup

1. Type "Task Scheduler" in the Windows search bar and open the application
2. Click on "Create Basic Task..." in the right panel
3. Follow the steps:
   - **Name**: Enter a descriptive name like "ESTU Announcement Bot"
   - **Description**: Optionally, add a description
   - **Trigger**: Select "Daily"
   - **Start Time**: Choose the time you want the bot to run (e.g., 8:00 AM)
   - **Action**: Select "Start a Program"
   - **Program/script**: Specify the full path to the `daily_run.bat` file in your project directory
   - **Start in (optional)**: Enter the full path of your project’s root directory (e.g., `C:\Users\username\estu-announcements`)

4. Click "Finish" to create the task

## Advanced Settings (Optional)

For more control, open the properties of the created task and adjust the following settings:

1. **Conditions** tab:
   - "Start the task only if the computer is idle" → Disable
   - "Start only if the computer is on AC power" → Enable

2. **Settings** tab:
   - "Run the task as soon as possible after a scheduled start is missed" → Enable
   - "If the task fails, restart every" → Enable and set to 5 minutes
   - "Stop the task if it runs longer than 3 days" → Disable

## Testing

Select the created task in Task Scheduler and click "Run" to execute it immediately.
Check the `bot_schedule.log` file to ensure the process was successful and verify that messages were sent to Telegram.

## Troubleshooting

If the task does not run as expected:

1. Ensure the `.env` file is correctly configured
2. Check the `bot_schedule.log` file for error messages
3. Review the task history in Task Scheduler
4. Confirm that the bot runs manually: `python scraper.py`

