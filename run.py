#!/usr/bin/env python3
"""
Bu script, scraper.py'yi çalıştırır ve hata oluşması durumunda kullanıcıya bilgi verir.
"""

import os
import sys
import subprocess
import time

def check_requirements():
    """Gerekli kütüphanelerin kurulu olup olmadığını kontrol eder."""
    try:
        import requests
        import bs4
        import dotenv
        import telegram
        return True
    except ImportError as e:
        print(f"HATA: Gerekli kütüphane eksik: {e}")
        print("Lütfen gerekli kütüphaneleri kurun: pip install -r requirements.txt")
        return False

def check_env_file():
    """Telegram token ve chat ID'nin ayarlanıp ayarlanmadığını kontrol eder."""
    if not os.path.exists(".env"):
        print("HATA: .env dosyası bulunamadı.")
        print("Lütfen .env.example dosyasını kopyalayıp .env olarak kaydedin ve Telegram bilgilerinizi girin.")
        return False
    
    from dotenv import load_dotenv
    load_dotenv()
    
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not token or token == "your_telegram_bot_token_here":
        print("HATA: TELEGRAM_TOKEN ayarlanmamış veya varsayılan değerde.")
        print("Lütfen .env dosyasını düzenleyip geçerli bir Telegram token'ı girin.")
        return False
    
    if not chat_id or chat_id == "your_chat_id_here":
        print("HATA: TELEGRAM_CHAT_ID ayarlanmamış veya varsayılan değerde.")
        print("Lütfen .env dosyasını düzenleyip geçerli bir chat ID girin.")
        return False
    
    return True

def run_scraper():
    """scraper.py'yi çalıştırır."""
    try:
        print("Duyuru tarayıcısı başlatılıyor...")
        result = subprocess.run([sys.executable, "scraper.py"], check=True)
        if result.returncode == 0:
            print("İşlem başarıyla tamamlandı.")
            return True
        else:
            print(f"İşlem hata kodu ile sonlandı: {result.returncode}")
            return False
    except subprocess.CalledProcessError as e:
        print(f"HATA: Scraper çalıştırılırken bir hata oluştu: {e}")
        return False
    except Exception as e:
        print(f"BEKLENMEDİK HATA: {e}")
        return False

def main():
    """Ana işlev."""
    print("=" * 50)
    print("ESTÜ ve Anadolu Üniversitesi Duyuru Botu")
    print("=" * 50)
    
    if not check_requirements():
        return
    
    if not check_env_file():
        return
    
    success = run_scraper()
    
    if success:
        print("\nDuyurular kontrol edildi. Detaylar için scraper.log dosyasını inceleyebilirsiniz.")
    else:
        print("\nİşlem sırasında hatalar oluştu. Detaylar için scraper.log dosyasını inceleyebilirsiniz.")
    
    print("\nÇıkmak için Enter'a basın...")
    input()

if __name__ == "__main__":
    main() 