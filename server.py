import asyncio
from bot_utils import get_weather, extract_city_from_message
from response import responses

#day4
from aiohttp import web

async def web_index(request):
    return web.Response(text="""
    <html>
    <body>
        <h1>Bot ile Chat</h1>
        <form action="/send" method="post">
            <input type="text" name="message" autofocus required>
            <button type="submit">Gönder</button>
        </form>
    </body>
    </html>
    """, content_type='text/html')

async def web_send(request):
    data = await request.post()
    message = data.get('message', '')

    # Burada TCP sunucusuna bağlanarak gerçek cevap alınmalı
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888)
    writer.write(message.encode())
    await writer.drain()

    # Sunucudan gelen cevabı al
    response_data = await reader.read(1024)
    response_text = response_data.decode()

    # Bağlantıyı kapat
    writer.close()
    await writer.wait_closed()
    
    return web.Response(text=f"""
    <html>
    <body>
        <h1>Bot ile Chat</h1>
        <p><b>Sen:</b> {message}</p>
        <p><b>{response_text[:4]}</b> {response_text[5:]}</p> 
        <form action="/send" method="post">
            <input type="text" name="message" autofocus required>
            <button type="submit">Gönder</button>
        </form>
    </body>
    </html>
    """, content_type='text/html')

async def start_web_server():
    app = web.Application()
    app.add_routes([
        web.get('/', web_index),
        web.post('/send', web_send),
    ])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '127.0.0.1', 8080)
    await site.start()
    print("Web sunucusu başlatıldı: http://127.0.0.1:8080")



#day4end

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

#day4after
'''
async def main():
    server = await asyncio.start_server(handle_client, '127.0.0.1', 8888)
    addr = server.sockets[0].getsockname()
    print(f"Sunucu başlatıldı: {addr}")
    async with server:
        await server.serve_forever()
'''

async def main():
    server = await asyncio.start_server(handle_client, '127.0.0.1', 8888)
    addr = server.sockets[0].getsockname()
    print(f"TCP Sunucu başlatıldı: {addr}")

    await asyncio.gather(
        server.serve_forever(),
        start_web_server()
    )


if __name__ == "__main__":
    asyncio.run(main())
