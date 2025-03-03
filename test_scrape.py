import requests
from bs4 import BeautifulSoup
import json

def inspect_site(url, name):
    """Web sitesinin yapısını incelemek için test fonksiyonu"""
    print(f"\n{'-'*50}")
    print(f"İnceleniyor: {name} ({url})")
    print(f"{'-'*50}")
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # HTML içeriğini parse et
        soup = BeautifulSoup(response.text, 'html5lib')
        
        # Olası duyuru konteynerları için seçicileri test et
        selectors = [
            "div.event-content", 
            "div.announcement-list-item",
            "div.announcement", 
            "div.duyuru", 
            ".duyuru-liste", 
            ".duyurular", 
            "div.news-list",
            "article.announcement"
        ]
        
        print("\nMuhtemel duyuru konteynerları:")
        for selector in selectors:
            items = soup.select(selector)
            print(f"  {selector}: {len(items)} öğe bulundu")
        
        # Tüm h2, h3 ve div.date elementlerini kontrol et
        h2s = soup.find_all('h2')
        h3s = soup.find_all('h3')
        dates = soup.select('div.date, span.date')
        
        print(f"\nBulunan başlık etiketleri: H2: {len(h2s)}, H3: {len(h3s)}")
        print(f"Bulunan tarih etiketleri: {len(dates)}")
        
        # İlk birkaç h2 ve h3 içeriğini göster
        if h2s:
            print("\nÖrnek H2 içerikleri:")
            for i, h in enumerate(h2s[:3]):
                print(f"  {i+1}. {h.text.strip()}")
        
        if h3s:
            print("\nÖrnek H3 içerikleri:")
            for i, h in enumerate(h3s[:3]):
                print(f"  {i+1}. {h.text.strip()}")
        
        # Sayfa yapısını analiz ederek duyuru olabilecek öğeleri bul
        articles = soup.find_all('article')
        divs_with_class = [div for div in soup.find_all('div', class_=True)]
        
        print(f"\nToplam <article> sayısı: {len(articles)}")
        print(f"Class'a sahip <div> sayısı: {len(divs_with_class)}")
        
        # En sık kullanılan div sınıflarını göster
        class_counter = {}
        for div in divs_with_class:
            for cls in div['class']:
                class_counter[cls] = class_counter.get(cls, 0) + 1
        
        sorted_classes = sorted(class_counter.items(), key=lambda x: x[1], reverse=True)
        
        print("\nEn yaygın div sınıfları:")
        for cls, count in sorted_classes[:10]:
            print(f"  {cls}: {count}")
        
        # Sayfa içindeki tüm bağlantıları analiz et
        links = soup.find_all('a', href=True)
        duyuru_links = [a for a in links if 'duyuru' in a['href'].lower()]
        
        print(f"\nDuyuru içerebilecek bağlantı sayısı: {len(duyuru_links)}")
        if duyuru_links:
            print("Örnek bağlantılar:")
            for i, link in enumerate(duyuru_links[:3]):
                print(f"  {i+1}. {link.get('href')}: {link.text.strip()}")
                
    except Exception as e:
        print(f"HATA: {e}")

# Test edilecek URL'ler
urls = [
    ("https://www.eskisehir.edu.tr/tr/Duyuru", "ESTÜ Ana Sayfa"),
    ("https://ceng.eskisehir.edu.tr/tr/Duyuru", "ESTÜ Bilgisayar Mühendisliği"),
    ("https://uib.eskisehir.edu.tr/tr/Duyuru", "ESTÜ Uluslararası İlişkiler")
]

for url, name in urls:
    inspect_site(url, name)

print("\nTest tamamlandı.") 