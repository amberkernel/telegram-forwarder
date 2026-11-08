# Telegram Forwarder

**Languages:** [🇬🇧 English](#-english) | [🇹🇷 Türkçe](#-türkçe)

---

## 🇬🇧 English

A message forwarding tool that runs on your own Telegram user account (userbot). It listens to the source channels you choose and **copies** every new message to the users or chats you choose.

Messages are copied, not forwarded. So the "Forwarded from" label does not appear and the source channel stays hidden. The source channel's name is added to the start of each message.

### Features

- Multiple source channels and multiple targets
- Media (photos, videos, files) is sent along with its caption
- If media cannot be sent (polls, etc.), only the text is sent
- Only live messages are handled: messages older than 60 seconds are skipped, so old messages are not sent again when the bot restarts
- The same message is never sent twice
- Waits 1.5 seconds between targets and respects Telegram's rate limit (`FloodWait`)
- `SESSION_STRING` support and a small keep-alive web server for cloud platforms such as Render.com

### Requirements

- Python 3.8+
- Telegram API credentials (`API_ID` and `API_HASH`): [my.telegram.org](https://my.telegram.org) → *API development tools*

### Installation

```bash
git clone <repo-url>
cd telegram-forwarder

python -m venv venv
# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt
```

### Configuration

Copy `.env.example` to `.env` and fill in your values:

```bash
# Windows
copy .env.example .env
# Linux / macOS
cp .env.example .env
```

Example `.env`:

```env
API_ID=1234567
API_HASH=0123456789abcdef0123456789abcdef

# Channels to listen to (comma-separated). Username or numeric ID.
SOURCE_CHANNEL=@channel1,-1001234567890

# Targets to send messages to (comma-separated)
TARGET_USER=@user1,me

# Optional: session string for cloud deployments (see "Running in the Cloud")
SESSION_STRING=
```

| Variable | Required | Description |
|---|---|---|
| `API_ID` | Yes | API ID from my.telegram.org |
| `API_HASH` | Yes | API Hash from my.telegram.org |
| `SOURCE_CHANNEL` | Yes | Channels or chats to listen to, comma-separated |
| `TARGET_USER` | Yes | Targets to send messages to, comma-separated (`me` = Saved Messages) |
| `SESSION_STRING` | No | If set, this session is used instead of the local `.session` file |
| `PORT` | No | Web server port (default `8080`) |

> Numeric IDs (`-100...`) are converted to numbers automatically.

### Usage

#### 1. Log in (once)

```bash
python qr_login.py
```

A QR code appears in the terminal. Scan it in the Telegram app via **Settings → Devices → Link Desktop Device** (you have 120 seconds). The session is saved to `user_session.session`.

#### 2. Start the bot

```bash
python main.py
```

The bot starts listening to the source channels. Press `Ctrl+C` to stop it.

### Running in the Cloud (Render.com)

1. Log in locally with `qr_login.py`.
2. Convert the session to a string:
   ```bash
   python export_session.py
   ```
3. Copy the long string from the output.
4. Create a **Web Service** on Render:
   - Build command: `pip install -r requirements.txt`
   - Start command: `python main.py`
5. Add `API_ID`, `API_HASH`, `SOURCE_CHANNEL`, `TARGET_USER` and `SESSION_STRING` under *Environment Variables*.

The bot runs a small web server that answers on `/` at the port Render expects. On the free plan, you can ping this URL regularly with an uptime service (e.g. UptimeRobot) to keep the service from sleeping.

### Project Structure

```
telegram-forwarder/
├── main.py              # Main bot: listens to channels, copies messages
├── config.py            # Reads .env and parses settings
├── qr_login.py          # Telegram login with QR code
├── export_session.py    # Converts the local session to SESSION_STRING
├── .env.example         # Example environment file
└── requirements.txt     # Dependencies
```

### Security

- `SESSION_STRING` and the `.session` file give **full access to your account**. Do not share them or commit them to Git (`.gitignore` already excludes them).
- Using a userbot is subject to Telegram's Terms of Service. Excessive or spam-like use may get your account restricted.

### Known Limitations

- Albums (grouped media) are sent as separate messages.
- Messages edited or deleted in the source are not reflected in the target.
- After a `FloodWait`, the message for that target is not retried.

---

## 🇹🇷 Türkçe

Kendi Telegram kullanıcı hesabınızla (userbot) çalışan bir mesaj aktarma aracı. Belirlediğiniz kaynak kanalları dinler ve gelen her yeni mesajı belirlediğiniz kişilere veya sohbetlere **kopyalar**.

Mesajlar iletilmez (forward), kopyalanır. Bu yüzden "iletildi" etiketi görünmez ve kaynak kanal gizli kalır. Her mesajın başına kaynak kanalın adı eklenir.

### Özellikler

- Birden fazla kaynak kanal ve birden fazla hedef desteği
- Medya (fotoğraf, video, dosya) açıklamasıyla birlikte aktarılır
- Gönderilemeyen medyada (anket vb.) yalnızca metin gönderilir
- Yalnızca canlı mesajlar işlenir: 60 saniyeden eski mesajlar atlanır, bot yeniden başladığında eski mesajlar tekrar gönderilmez
- Aynı mesajın iki kez gönderilmesi engellenir
- Hedefler arasında 1,5 saniye beklenir; Telegram'ın hız sınırına (`FloodWait`) uyulur
- Render.com gibi bulut ortamlarında çalışmak için `SESSION_STRING` desteği ve uyanık tutma amaçlı küçük bir web sunucusu

### Gereksinimler

- Python 3.8+
- Telegram API bilgileri (`API_ID` ve `API_HASH`): [my.telegram.org](https://my.telegram.org) → *API development tools*

### Kurulum

```bash
git clone <repo-adresi>
cd telegram-forwarder

python -m venv venv
# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt
```

### Yapılandırma

`.env.example` dosyasını `.env` olarak kopyalayın ve kendi bilgilerinizle doldurun:

```bash
# Windows
copy .env.example .env
# Linux / macOS
cp .env.example .env
```

Örnek `.env`:

```env
API_ID=1234567
API_HASH=0123456789abcdef0123456789abcdef

# Dinlenecek kanallar (virgülle ayırın). Kullanıcı adı veya sayısal ID olabilir.
SOURCE_CHANNEL=@kanal1,-1001234567890

# Mesajların gönderileceği hedefler (virgülle ayırın)
TARGET_USER=@kullanici1,me

# İsteğe bağlı: bulut ortamı için oturum metni (bkz. "Bulutta Çalıştırma")
SESSION_STRING=
```

| Değişken | Zorunlu | Açıklama |
|---|---|---|
| `API_ID` | Evet | my.telegram.org'dan alınan API ID |
| `API_HASH` | Evet | my.telegram.org'dan alınan API Hash |
| `SOURCE_CHANNEL` | Evet | Dinlenecek kanal veya sohbetler, virgülle ayrılmış |
| `TARGET_USER` | Evet | Mesajların gönderileceği hedefler, virgülle ayrılmış (`me` = Kayıtlı Mesajlar) |
| `SESSION_STRING` | Hayır | Doluysa yerel `.session` dosyası yerine bu oturum kullanılır |
| `PORT` | Hayır | Web sunucusunun portu (varsayılan `8080`) |

> Sayısal ID'ler (`-100...`) otomatik olarak sayıya çevrilir.

### Kullanım

#### 1. Giriş yapın (bir kez)

```bash
python qr_login.py
```

Terminalde bir QR kod görünür. Telegram uygulamasında **Ayarlar → Cihazlar → Masaüstü Cihazı Bağla** adımlarıyla okutun (120 saniye süreniz var). Oturum `user_session.session` dosyasına kaydedilir.

#### 2. Botu başlatın

```bash
python main.py
```

Bot kaynak kanalları dinlemeye başlar. Durdurmak için `Ctrl+C`'ye basın.

### Bulutta Çalıştırma (Render.com)

1. Yerelde `qr_login.py` ile giriş yapın.
2. Oturumu metne dönüştürün:
   ```bash
   python export_session.py
   ```
3. Çıktıdaki uzun metni kopyalayın.
4. Render'da bir **Web Service** oluşturun:
   - Build komutu: `pip install -r requirements.txt`
   - Start komutu: `python main.py`
5. *Environment Variables* bölümüne `API_ID`, `API_HASH`, `SOURCE_CHANNEL`, `TARGET_USER` ve `SESSION_STRING` değişkenlerini ekleyin.

Bot, Render'ın beklediği porttan `/` adresine yanıt veren küçük bir web sunucusu çalıştırır. Ücretsiz planda servisin uykuya geçmemesi için bu adresi bir uptime servisiyle (ör. UptimeRobot) düzenli olarak yoklayabilirsiniz.

### Proje Yapısı

```
telegram-forwarder/
├── main.py              # Ana bot: kanalları dinler, mesajları kopyalar
├── config.py            # .env okuma ve ayarların ayrıştırılması
├── qr_login.py          # QR kod ile Telegram girişi
├── export_session.py    # Yerel oturumu SESSION_STRING'e dönüştürür
├── .env.example         # Örnek ortam değişkenleri dosyası
└── requirements.txt     # Bağımlılıklar
```

### Güvenlik

- `SESSION_STRING` ve `.session` dosyası **hesabınıza tam erişim** sağlar. Kimseyle paylaşmayın, Git'e eklemeyin (`.gitignore` bunları zaten hariç tutar).
- Userbot kullanımı Telegram kullanım koşullarına tabidir. Aşırı veya spam niteliğinde kullanım hesabınızın kısıtlanmasına yol açabilir.

### Bilinen Sınırlamalar

- Albümler (gruplu medya) tek tek ayrı mesajlar olarak gönderilir.
- Kaynakta düzenlenen veya silinen mesajlar hedefe yansıtılmaz.
- `FloodWait` sonrası o hedefe giden mesaj tekrar denenmez.
