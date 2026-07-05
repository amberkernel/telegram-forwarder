import sys
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

import asyncio
import qrcode
from telethon import TelegramClient

from config import API_ID, API_HASH

# Oturum dosyası adı
SESSION_NAME = 'user_session'

def generate_qr_code(url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=1,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    qr.print_ascii(invert=True)

async def login():
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    await client.connect()

    if not await client.is_user_authorized():
        qr_login = await client.qr_login()
        print("\n" + "="*50)
        print("LÜTFEN AŞAĞIDAKİ KAREKODU TELEGRAM UYGULAMASINDAN OKUTUN")
        print("Ayarlar -> Cihazlar -> Masaüstü Cihazı Bağla")
        print("="*50 + "\n")
        
        generate_qr_code(qr_login.url)
        
        try:
            print("\nQR Kodun okutulması bekleniyor...")
            await qr_login.wait(120)  # 120 saniye bekle
            print("Giriş başarılı! Artık main.py dosyasını çalıştırabilirsiniz.")
        except Exception as e:
            print("\nGiriş yapılamadı veya süre doldu. Hata:", str(e))
    else:
        print("Zaten giriş yapılmış! main.py dosyasını çalıştırabilirsiniz.")
        
    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(login())
