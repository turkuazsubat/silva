import aiohttp
import ssl


CITY_LIST = ["istanbul", "ankara", "izmir", "mersin", "elazığ", "bursa", "adana", "antalya", "konya"]


async def get_weather(city="istanbul"):
    try:
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False  # Sertifika doğrulamasını kapat
        ssl_context.verify_mode = ssl.CERT_NONE  # Sertifika doğrulamasını kapat

        async with aiohttp.ClientSession() as session:
            url = f"https://wttr.in/{city}?format=3"
            async with session.get(url, ssl=ssl_context) as resp:
                if resp.status == 200:
                    return await resp.text()
                else:
                    return "Hava durumu alınamadı."
    except Exception as e:
        return f"Hata oluştu: {e}"

def extract_city_from_message(message):
    words = message.lower().split()
    for word in words:
        if word in CITY_LIST:
            return word
    return "istanbul"
