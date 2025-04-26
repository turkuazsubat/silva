import asyncio
from bot_utils import get_weather, extract_city_from_message
from response import responses

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"{addr} bağlandı.")
    
    while True:
        data = await reader.read(1024)
        if not data:
            break
        message = data.decode().strip()
        print(f"{addr} mesaj gönderdi: {message}")
        
        if not message:
            continue
        
        parts = [part.strip() for part in message.lower().split("ve")]
        tasks = []
        
        for part in parts:
            if "hava durumu" in part:
                city = extract_city_from_message(part)
                tasks.append(get_weather(city))
            elif part in responses:
                async def fake_response(resp=responses[part]):
                    await asyncio.sleep(0)
                    return resp
                tasks.append(fake_response())
        
        if not tasks:
            writer.write("Bot: Üzgünüm, buraya çalışmadım.\n".encode())
            await writer.drain()
            continue

        try:
            results = await asyncio.gather(*tasks)
            combined_response = "\n".join(results) 
            writer.write(f"Bot: {combined_response}".encode())
            await writer.drain()
        except Exception as e:
            writer.write(f"Bot: Bir hata oluştu: {str(e)}\n".encode())
            await writer.drain()
    
    print(f"{addr} bağlantısı kapandı.")
    writer.close()

async def main():
    server = await asyncio.start_server(handle_client, '127.0.0.1', 8888)
    addr = server.sockets[0].getsockname()
    print(f"Sunucu başlatıldı: {addr}")
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
