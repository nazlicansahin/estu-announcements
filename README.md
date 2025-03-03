# ESTÜ Duyuru Botu

Bu proje, aşağıdaki Eskişehir Teknik Üniversitesi web sitelerinden duyuruları çeken ve bunları Telegram üzerinden gönderen bir bot uygulamasıdır:

- Eskişehir Teknik Üniversitesi (ESTÜ) Ana Sayfa
- ESTÜ Bilgisayar Mühendisliği Bölümü
- ESTÜ Uluslararası İlişkiler Birimi

## Özellikler

- Belirtilen web sitelerinden duyuruları otomatik olarak çeker
- Yeni duyuruları algılar ve tekrar göndermeyi önler
- Duyuruları Telegram üzerinden istediğiniz sohbete/kanala gönderir
- Yeni duyuru yoksa bilgilendirme mesajı gönderir
- Her gün otomatik çalışma özelliği
- Kullanıcı dostu ve bilgilendirici mesaj formatı
- Kapsamlı hata yönetimi ve loglama

## Kurulum

1. Bu repository'yi klonlayın:
```bash
git clone https://github.com/username/estu-announcements.git
cd estu-announcements
```

2. Gerekli Python paketlerini yükleyin:
```bash
pip install -r requirements.txt
```

3. `.env.example` dosyasını `.env` olarak kopyalayın ve düzenleyin:
```bash
cp .env.example .env
```

4. `.env` dosyasını bir metin editörü ile açın ve gerekli değerleri ekleyin:
   - `TELEGRAM_TOKEN`: Telegram BotFather'dan aldığınız bot token'ı
   - `TELEGRAM_CHAT_ID`: Mesajların gönderileceği sohbet veya kanal ID'si

## Telegram Bot Oluşturma

1. Telegram'da [@BotFather](https://t.me/botfather) ile konuşma başlatın
2. `/newbot` komutunu gönderin ve talimatları izleyin
3. Bot oluşturulduktan sonra, BotFather size bir token verecektir. Bu token'ı `.env` dosyasına ekleyin.

## Chat ID Bulma

- **Kişisel sohbet için:** [@userinfobot](https://t.me/userinfobot) ile konuşma başlatın, size ID'nizi verecektir.
- **Kanal için:** Kanalınızın kullanıcı adını (örn: @mychannel) biliyorsanız, botunuzu kanala yönetici olarak ekleyin ve kanalınıza bir mesaj gönderin. Ardından şu URL'yi ziyaret edin: `https://api.telegram.org/bot<BOT_TOKEN>/getUpdates`. Bu size kanal ID'sini verecektir.

## Kullanım

Scripti manuel olarak çalıştırmak için:

```bash
python scraper.py
```

- Script yeni duyuruları çekecek ve Telegram üzerinden gönderecektir
- Daha önce gönderilen duyurular tekrar gönderilmeyecektir
- Yeni duyuru yoksa, her bir kaynak için bilgilendirme mesajı gönderilecektir
- İşlem logları `scraper.log` dosyasında saklanacaktır

## Otomatik Günlük Çalıştırma

Bot, her gün otomatik olarak çalışacak şekilde yapılandırılabilir:

### Windows Kullanıcıları İçin

Windows Görev Zamanlayıcısı ile otomatik çalıştırmak için:

1. Projenin ana dizinindeki `daily_run.bat` dosyasını kullanın
2. Windows Görev Zamanlayıcısı'nda günlük bir görev oluşturun
3. Detaylı talimatlar için projedeki `TASK_SCHEDULER_SETUP.md` dosyasını inceleyin

### Linux/Mac Kullanıcıları İçin

Cron ile otomatik çalıştırmak için:

```bash
# Her gün saat 08:00'de çalıştırmak için
0 8 * * * cd /path/to/estu-announcements && python scraper.py
```

## Test Etme

Yapılandırmayı test etmek için:

1. Scripti manuel olarak çalıştırın: `python scraper.py`
2. Telegram'da mesajları alıp almadığınızı kontrol edin
3. Windows'ta `daily_run.bat` dosyasını doğrudan çalıştırarak zamanlayıcı ayarlarını test edin

## Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen bir pull request açın veya önerilerinizi iletişime geçin.

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Daha fazla bilgi için `LICENSE` dosyasına bakın.