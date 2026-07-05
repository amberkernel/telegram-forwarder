import asyncio
import logging
import os
from aiohttp import web
from telethon import TelegramClient, events, errors
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
    
    # Mesajların sırasını korumak ve çakışmaları önlemek için kilit (Lock)
    send_lock = asyncio.Lock()
    processed_messages = set()
    
    @client.on(events.NewMessage(chats=SOURCE_CHANNELS))
    async def handler(event):
        # Aynı mesajın (örn: bağlantı kopmalarında) tekrar gelmesini engellemek için cache kontrolü
        msg_unique_id = f"{event.chat_id}_{event.message.id}"
        if msg_unique_id in processed_messages:
            return
        processed_messages.add(msg_unique_id)
        if len(processed_messages) > 1000:
            processed_messages.clear()
            
        async with send_lock:
            try:
                logging.info("Yeni mesaj yakalandı, kopyalanıyor...")
                
                # Kanal adını al
                channel_name = "Bilinmeyen Kanal"
                if event.chat and hasattr(event.chat, 'title'):
                    channel_name = event.chat.title
                
                # Mesaj metninin başına kanal adını ekle
                original_text = event.message.text or ""
                formatted_text = f"📢 **{channel_name}**\n\n{original_text}" if original_text else f"📢 **{channel_name}**"
                
                # Mesajı kopyalayarak tüm hedeflere gönderir (ileti etiketi olmaz, orijinal kanal gizli kalır)
                # Medya varsa medyayı da destekler
                for target in TARGET_USERS:
                    try:
                        if event.message.media:
                            await client.send_file(target, file=event.message.media, caption=formatted_text)
                        else:
                            await client.send_message(target, formatted_text)
                        
                        # Telegram spam filtresine takılmamak için hedefler arası 1.5 saniye bekle
                        await asyncio.sleep(1.5)
                        
                    except errors.FloodWaitError as e:
                        logging.warning(f"Telegram spam siniri! {e.seconds} saniye bekleniyor...")
                        await asyncio.sleep(e.seconds)
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
