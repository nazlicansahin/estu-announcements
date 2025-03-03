@echo off
echo ESTU Duyuru Botu - Günlük Çalıştırma
echo ======================================
echo %date% %time% - Bot çalıştırılıyor... >> bot_schedule.log

cd /d "%~dp0"
python scraper.py >> bot_schedule.log 2>&1

echo %date% %time% - Bot çalışması tamamlandı. >> bot_schedule.log
echo. >> bot_schedule.log 