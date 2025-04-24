import asyncio
from bot_utils import get_weather, extract_city_from_message

# Cevaplar sözlüğü
responses = {
    "selam": "Merhaba!",
    "nasılsın": "İyiyim, sen?",
    "teşekkür ederim": "Rica ederim!",
}

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"{addr} bağlandı.")

    while True:
        data = await reader.read(100)
        if not data:
            break
        message = data.decode().strip()
        print(f"{addr} mesaj gönderdi: {message}")

        response = ""

        if "hava durumu" in message.lower():
            # Şehri mesajdan çek
            city = extract_city_from_message(message)
            writer.write(f"Bot: '{city}' için hava durumu aranıyor...\n".encode())
            await writer.drain()

            weather = await get_weather(city)
            response = f"Bot: {weather}"
        else:
            # dict ile yanıt ver
            response = responses.get(message.lower(), "Üzgünüm, anlamadım.")

        writer.write((response + "\n").encode())
        await writer.drain()

    print(f"{addr} bağlantısı kapandı.")
    writer.close()

async def main():
    server = await asyncio.start_server(handle_client, '127.0.0.1', 8888)
    addr = server.sockets[0].getsockname()
    print(f"Sunucu başlatıldı: {addr}")
    async with server:
        await server.serve_forever()

asyncio.run(main())
