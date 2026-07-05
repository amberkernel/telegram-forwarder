import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')

# Telethon, ID numaralarını (örn: -100123) integer (sayı) olarak bekler, string olarak hata verir.
# Bu yüzden girilen değer sayıysa integer'a çeviren bir yardımcı fonksiyon yazıyoruz.
def parse_entity(entity_str):
    entity_str = entity_str.strip()
    if entity_str.lstrip('-').isdigit():
        return int(entity_str)
    return entity_str

# Birden fazla kanal/kullanıcı desteklemek için virgülle ayırıp listeye çeviriyoruz
_source_str = os.getenv('SOURCE_CHANNEL')
SOURCE_CHANNELS = [parse_entity(ch) for ch in _source_str.split(',')] if _source_str else []

_target_str = os.getenv('TARGET_USER')
TARGET_USERS = [parse_entity(t) for t in _target_str.split(',')] if _target_str else []

SESSION_STRING = os.getenv('SESSION_STRING')

# Gerekli bilgilerin kontrolü
if not API_ID or not API_HASH:
    print('HATA: Lütfen .env dosyasındaki API_ID ve API_HASH bilgilerini doldurun!')
    exit(1)
