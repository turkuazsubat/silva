import aiohttp
CITY_LIST = ["istanbul", "ankara", "izmir", "mersin", "elazığ", "bursa", "adana", "antalya", "konya"]


async def get_weather(city="istanbul"):
    try:
        async with aiohttp.ClientSession() as session:
            url = f"https://wttr.in/{city}?format=3"
            async with session.get(url) as resp:
                if resp.status == 200:
                    return await resp.text()
                else:
                    return "Hava durumu alınamadı."
    except Exception as e:
        return f"Hata oluştu: {e}"

def extract_city_from_message(message):
    # Mesajı küçük harfe çevirip kelimelere ayıralım
    words = message.lower().split()
    
    # Şehir listesinde olan bir kelimeyi arayalım
    for word in words:
        if word in CITY_LIST:
            return word

    # Eğer şehir bulunamazsa, varsayılan olarak 'istanbul' döndür
    return "istanbul"
