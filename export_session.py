import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from config import API_ID, API_HASH
from qr_login import SESSION_NAME

async def main():
    print("Mevcut oturum okunuyor...")
    # Mevcut SQLite oturumu ile bağlan
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    await client.connect()
    
    if not await client.is_user_authorized():
        print("HATA: Oturum bulunamadı! Önce qr_login.py ile giriş yapmalısınız.")
        return
        
    # Mevcut oturumu StringSession'a dönüştür
    string_session = StringSession.save(client.session)
    
    print("\n" + "="*50)
    print("AŞAĞIDAKİ UZUN METİN SİZİN OTURUM ŞİFRENİZDİR (SESSION_STRING):")
    print("Bunu kopyalayıp Render.com panelindeki Environment Variables kısmına")
    print("SESSION_STRING anahtarıyla yapıştıracaksınız. LÜTFEN KİMSEYLE PAYLAŞMAYIN!\n")
    print(string_session)
    print("="*50 + "\n")
    
    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
