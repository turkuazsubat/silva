import aiohttp
import ssl

CURRENCY_LIST = ["usd", "eur", "try", "gbp", "jpy", "chf", "cad", "aud", "nzd"]

async def get_exchange_rate(base_currency="usd", target_currency="try"):
    try:
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        async with aiohttp.ClientSession() as session:
            url = f"https://api.frankfurter.app/latest?amount=1&from={base_currency.lower()}&to={target_currency.lower()}"

            async with session.get(url, ssl=ssl_context) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    rates = data.get("rates", {})

                    # Dikkat: Frankfurter sadece EUR bazlı tam çalışır
                    # Başka bir base_currency kullanıldığında "404" hatası verebilir
                    if target_currency.upper() in rates:
                        rate = rates[target_currency.upper()]
                        return f"1 {base_currency.upper()} = {rate:.3f} {target_currency.upper()}"
                    else:
                        return f"{base_currency.upper()} -> {target_currency.upper()} kuru bulunamadı."
                else:
                    return f"Döviz kuru alınamadı. HTTP kodu: {resp.status}"
    except Exception as e:
        return f"Hata oluştu: {e}"

def extract_currency_from_message(message):
    words = message.lower().split()
    found = []
    for word in words:
        if word in CURRENCY_LIST:
            found.append(word)
    return found if found else ["usd", "try"]  # Varsayılan usd→try
