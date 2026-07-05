import asyncio
import logging
import os
from aiohttp import web
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from config import API_ID, API_HASH, SOURCE_CHANNELS, TARGET_USERS, SESSION_STRING
from qr_login import SESSION_NAME

# Loglama ayarları
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# --- Sahte Web Sunucusu (Render'ı Kandırmak İçin) ---
async def handle_web(request):
    return web.Response(text="Bot aktif ve calisiyor! (Render Uptime)")

async def web_server():
    app = web.Application()
    app.router.add_get('/', handle_web)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    logging.info(f"Sahte web sunucusu {port} portunda baslatildi.")
# ----------------------------------------------------

def main():
    if not SOURCE_CHANNELS or not TARGET_USERS:
        print("HATA: .env dosyasında SOURCE_CHANNEL veya TARGET_USER belirtilmemiş!")
        return

    # İstemciyi oturumla başlat
    if SESSION_STRING:
        client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
        logging.info("Bulut oturumu (StringSession) kullanılıyor...")
    else:
        # İstemciyi mevcut yerel oturumla başlat (qr_login.py ile oluşturulmuş olmalı)
        client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
        logging.info("Yerel oturum (.session) kullanılıyor...")
    
    @client.on(events.NewMessage(chats=SOURCE_CHANNELS))
    async def handler(event):
        try:
            logging.info("Yeni mesaj yakalandı, kopyalanıyor...")
            
            # Mesajı kopyalayarak tüm hedeflere gönderir (ileti etiketi olmaz, orijinal kanal gizli kalır)
            # Medya varsa medyayı da destekler
            for target in TARGET_USERS:
                try:
                    if event.message.media:
                        await client.send_file(target, file=event.message.media, caption=event.message.text)
                    else:
                        await client.send_message(target, event.message.text)
                except Exception as e:
                    logging.error(f"Hedefe ({target}) gönderilemedi: {e}")
                
            logging.info("Mesaj başarıyla kopyalandı!")
        except Exception as e:
            logging.error(f"Mesaj gönderilirken hata oluştu: {e}")

    logging.info(f"{SOURCE_CHANNELS} kanalları dinleniyor...")
    logging.info("Çıkmak için Ctrl+C'ye basın.")
    
    with client:
        # Web sunucusunu Telegram döngüsüyle birlikte çalıştır
        client.loop.create_task(web_server())
        # Mesaj dinleme döngüsünü başlat
        client.run_until_disconnected()

if __name__ == '__main__':
    main()
