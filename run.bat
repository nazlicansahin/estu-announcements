@echo off
echo ESTU Duyuru Botu
echo ======================================
echo.

python run.py

if %errorlevel% neq 0 (
    echo.
    echo Hata olustu! Lutfen yonetici izniyle calistirmayi deneyin.
    echo Gerekli paketlerin yuklu oldugundan emin olun: pip install -r requirements.txt
    echo.
    pause
    exit /b %errorlevel%
) 