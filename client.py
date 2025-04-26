import asyncio

async def tcp_client():
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888)

    print("Sunucuya bağlandı. Çıkmak için boş mesaj bırak.")
    while True:
        msg = input("Sen: ")
        if not msg:
            break

        writer.write(msg.encode())
        await writer.drain()

        data = await reader.read(1024)
        print(data.decode())

    writer.close()
    await writer.wait_closed()

asyncio.run(tcp_client())
