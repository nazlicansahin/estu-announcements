import os
import time
import hashlib
import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional, Set
import re

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import telebot

# Logging ayarları
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scraper.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# .env dosyasını yükle
load_dotenv()

# Telegram Bot API token'ı
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Duyuru kaynakları
SOURCES = {
    "estu": {
        "name": "Eskişehir Teknik Üniversitesi",
        "url": "https://www.eskisehir.edu.tr/tr/Duyuru",
        "selector": "h3"
    },
    "estu_ceng": {
        "name": "ESTÜ Bilgisayar Mühendisliği Bölümü",
        "url": "https://ceng.eskisehir.edu.tr/tr/Duyuru",
        "selector": "h3"
    },
    "estu_uib": {
        "name": "ESTÜ Uluslararası İlişkiler Birimi",
        "url": "https://uib.eskisehir.edu.tr/tr/Duyuru",
        "selector": "h3"
    }
}

# Daha önce gönderilen duyuruları saklamak için dosya
HISTORY_FILE = "announcement_history.json"

class AnnouncementScraper:
    def __init__(self, telegram_token: str, chat_id: str):
        self.telegram_token = telegram_token
        self.chat_id = chat_id
        self.bot = self._setup_telegram_bot()
        self.sent_announcements = self._load_history()
        
    def _setup_telegram_bot(self) -> telebot.TeleBot:
        """Telegram botunu ayarla."""
        if not self.telegram_token:
            logger.error("Telegram token bulunamadı! .env dosyasını kontrol edin.")
            return None
        
        return telebot.TeleBot(token=self.telegram_token)
    
    def _load_history(self) -> Set[str]:
        """Daha önce gönderilen duyuruların hash'lerini yükle."""
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    return set(json.load(f))
            except Exception as e:
                logger.error(f"Geçmiş dosyası yüklenirken hata oluştu: {e}")
                return set()
        return set()
    
    def _save_history(self) -> None:
        """Gönderilen duyuruların hash'lerini kaydet."""
        try:
            with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump(list(self.sent_announcements), f)
        except Exception as e:
            logger.error(f"Geçmiş dosyası kaydedilirken hata oluştu: {e}")
    
    def _generate_hash(self, announcement: Dict[str, Any]) -> str:
        """Duyuru için benzersiz bir hash oluştur."""
        content = f"{announcement['title']}{announcement['link']}{announcement['date']}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _is_new_announcement(self, announcement_hash: str) -> bool:
        """Duyurunun daha önce gönderilip gönderilmediğini kontrol et."""
        return announcement_hash not in self.sent_announcements
    
    def fetch_announcements(self, source_id: str) -> List[Dict[str, Any]]:
        """Belirtilen kaynaktan duyuruları çeker."""
        source = SOURCES.get(source_id)
        if not source:
            logger.error(f"Kaynak bulunamadı: {source_id}")
            return []
            
        try:
            logger.info(f"{source['name']} sitesinden duyurular çekiliyor...")
            response = requests.get(source['url'], timeout=10)
            response.raise_for_status()
            
            # HTML içeriğini parse et
            soup = BeautifulSoup(response.text, 'html5lib')
            
            # Duyuru öğelerini bul
            items = soup.select(source['selector'])
            
            announcements = []
            for item in items:
                announcement = self._parse_estu_announcement(item, source)
                
                if announcement:
                    announcements.append(announcement)
            
            logger.info(f"{source['name']} sitesinden {len(announcements)} duyuru çekildi.")
            return announcements
            
        except Exception as e:
            logger.error(f"{source['name']} sitesinden duyurular çekilirken hata oluştu: {e}")
            return []
    
    def _parse_estu_announcement(self, item, source) -> Dict[str, Any]:
        """Eskişehir Teknik Üniversitesi duyurularını ayrıştır."""
        try:
            # Artık item doğrudan h3 elementi
            title = item.text.strip()
            
            # Ebeveyn elementlerden a etiketini bulmaya çalış
            link_elem = item.find_parent('a')
            if not link_elem:
                # Kardeş elementlerden a etiketini aramayı dene
                link_elem = item.find_next_sibling('a') or item.find_previous_sibling('a')
                
                # a etiketi bulunamadıysa, parent div'in içindeki a etiketini kontrol et
                if not link_elem:
                    parent_div = item.find_parent('div')
                    if parent_div:
                        link_elem = parent_div.find('a')
            
            # Hala bulunamadıysa, h3'e en yakın a etiketini bul
            if not link_elem:
                # Tüm a etiketlerini bul ve h3'e en yakın olanı seç
                all_links = item.find_all_next('a')
                if all_links:
                    link_elem = all_links[0]
            
            link = link_elem.get("href", "") if link_elem else ""
            
            # Eğer link göreceli ise mutlak URL'ye çevir
            if link and not link.startswith(("http://", "https://")):
                base_url = "/".join(source["url"].split("/")[:3])
                link = f"{base_url}{link if link.startswith('/') else '/' + link}"
            
            # Bugünün tarihini al
            today = datetime.now().strftime("%d.%m.%Y")
            
            # Duyurunun yayın tarihini bugün olarak işaretle
            announcement_date = today
            
            # Duyurunun bugüne ait olduğunu işaretle (tüm duyuruları bugünün duyurusu olarak kabul ediyoruz)
            # Gerçek senaryoda, web sayfasından duyuru tarihi çekilebilir ve karşılaştırma yapılabilir
            is_today = True
            
            # Sadece bugünün duyurularını döndür
            if is_today:
                return {
                    "source": source["name"],
                    "title": title,
                    "date": announcement_date,
                    "link": link
                }
            else:
                return None
                
        except Exception as e:
            logger.error(f"Duyuru ayrıştırılırken hata oluştu: {e}")
            return None
    
    def send_telegram_message(self, announcement):
        """Duyuruyu Telegram üzerinden gönderir."""
        try:
            message = (
                f"📢 *{announcement['source']}*\n\n"
                f"*{announcement['title']}*\n\n"
                f"📅 {announcement['date']}\n\n"
                f"🔗 [Detaylar için tıklayın]({announcement['link']})"
            )
            
            # pyTelegramBotAPI ile mesaj gönderme
            self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode='Markdown',
                disable_web_page_preview=False
            )
            
            # Başarıyla gönderilen duyurunun hash'ini kaydet
            announcement_hash = self._generate_hash(announcement)
            self.sent_announcements.add(announcement_hash)
            
            logger.info(f"Duyuru başarıyla gönderildi: {announcement['title']}")
            return True
            
        except Exception as e:
            logger.error(f"Telegram mesajı gönderilirken hata oluştu: {e}")
            return False
    
    def run(self) -> None:
        """Tüm kaynaklardan duyuruları çek ve yeni olanları gönder."""
        new_announcements_sent = False
        
        for source_id in SOURCES:
            announcements = self.fetch_announcements(source_id)
            source_name = SOURCES[source_id]["name"]
            source_has_new = False
            
            for announcement in announcements:
                announcement_hash = self._generate_hash(announcement)
                
                if self._is_new_announcement(announcement_hash):
                    success = self.send_telegram_message(announcement)
                    if success:
                        new_announcements_sent = True
                        source_has_new = True
                        # Her mesaj arasında kısa bir bekleme yap (rate limit'i aşmamak için)
                        time.sleep(1)
            
            # Bu kaynaktan hiç yeni duyuru yoksa veya hiç duyuru çekilmediyse, bildirim gönder
            if not source_has_new:
                try:
                    message = f"📢 *{source_name}*\n\n Bugün için yeni duyuru bulunmamaktadır."
                    self.bot.send_message(
                        chat_id=self.chat_id,
                        text=message,
                        parse_mode='Markdown'
                    )
                    logger.info(f"{source_name} için 'bugün yeni duyuru yok' bildirimi gönderildi.")
                    time.sleep(1)
                except Exception as e:
                    logger.error(f"Bildirim gönderilirken hata oluştu: {e}")
        
        # Geçmişi kaydet
        if new_announcements_sent:
            self._save_history()
            logger.info("Yeni duyurular gönderildi ve geçmiş güncellendi.")
        else:
            logger.info("Bugün için yeni duyuru bulunamadı.")

def main():
    """Ana program."""
    logger.info("Duyuru tarama işlemi başlatılıyor...")
    
    # Gerekli ortam değişkenlerini kontrol et
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        logger.error("TELEGRAM_TOKEN ve TELEGRAM_CHAT_ID .env dosyasında tanımlanmalıdır!")
        return
    
    try:
        scraper = AnnouncementScraper(TELEGRAM_TOKEN, TELEGRAM_CHAT_ID)
        scraper.run()
        logger.info("İşlem tamamlandı.")
    except Exception as e:
        logger.error(f"İşlem sırasında beklenmeyen bir hata oluştu: {e}")

if __name__ == "__main__":
    main() 