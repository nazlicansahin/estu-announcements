# Windows Görev Zamanlayıcısı Kurulum Talimatları

Bu doküman, ESTU Duyuru Botunun her gün otomatik olarak çalıştırılması için Windows Görev Zamanlayıcısı'nın nasıl yapılandırılacağını açıklar.

## Ön Gereksinimler

1. Python'un bilgisayarınızda kurulu olduğundan emin olun
2. Bot dosyalarının tam olarak yapılandırıldığından emin olun (özellikle `.env` dosyası)
3. Gereksinimlerin yüklü olduğundan emin olun: `pip install -r requirements.txt`

## Görev Zamanlayıcı Kurulumu

1. Windows arama çubuğuna "Görev Zamanlayıcısı" veya "Task Scheduler" yazın ve uygulamayı açın
2. Sağ paneldeki "Temel Görev Oluştur..." veya "Create Basic Task..." seçeneğine tıklayın
3. Adımları takip edin:
   - **İsim**: "ESTU Duyuru Botu" gibi tanımlayıcı bir isim girin
   - **Açıklama**: İsteğe bağlı olarak bir açıklama ekleyin
   - **Tetikleyici**: "Günlük" (Daily) seçeneğini seçin
   - **Başlangıç**: Botun çalışmasını istediğiniz saati seçin (örneğin sabah 8:00)
   - **Eylem**: "Bir program başlat" (Start a program) seçeneğini seçin
   - **Program/script**: Projenizin dizinindeki `daily_run.bat` dosyasının tam yolunu belirtin
   - **Başlangıç dizini**: Projenizin ana dizininin tam yolunu belirtin (örn: `C:\Users\username\estu-announcements`)

4. "Son" düğmesine tıklayarak görevi oluşturun

## Gelişmiş Ayarlar (İsteğe Bağlı)

Daha fazla kontrol için, oluşturulan görevin özelliklerini açabilir ve şu ayarları yapabilirsiniz:

1. **Koşullar** sekmesi:
   - Bilgisayar boşta ise çalıştır: Devre dışı bırakın
   - Ağ bağlantısı varsa çalıştır: Etkinleştirin

2. **Ayarlar** sekmesi:
   - Görevin zamanlanandan sonra mümkün olan en kısa sürede çalıştırılmasına izin ver: Etkinleştirin
   - Görev çalışmaya başlamazsa, yeniden başlat: Etkinleştirin ve 5 dakika olarak ayarlayın
   - Görev 3 günden uzun süredir çalışmıyorsa durdur: Devre dışı bırakın

## Test Etme

Görev Zamanlayıcısı'nda oluşturulan görevi seçin ve "Çalıştır" (Run) düğmesine tıklayarak hemen çalıştırın. 
İşlemin başarılı olduğundan emin olmak için `bot_schedule.log` dosyasını kontrol edin ve Telegram'a mesajların gelip gelmediğini doğrulayın.

## Sorun Giderme

Eğer görev beklendiği gibi çalışmıyorsa:

1. `.env` dosyasının doğru yapılandırıldığından emin olun
2. `bot_schedule.log` dosyasını inceleyerek hata mesajlarını kontrol edin
3. Görev Zamanlayıcısı'nda görevin geçmişini kontrol edin
4. Botun manuel olarak çalıştığından emin olun: `python scraper.py` 