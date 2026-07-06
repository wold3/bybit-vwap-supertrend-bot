import asyncio
import websockets
import json

clients = set()


# ================================
# CLIENT REGISTER
# ================================
async def register(ws):
    clients.add(ws)


async def unregister(ws):
    clients.remove(ws)


# ================================
# BROADCAST (PnL push)
# ================================
async def broadcast(data):

    if clients:

        msg = json.dumps(data)

        await asyncio.wait([
            client.send(msg)
            for client in clients
        ])


# ================================
# WS HANDLER
# ================================
async def handler(ws):

    await register(ws)

    try:
        async for msg in ws:
            pass
    finally:
        await unregister(ws)


# ================================
# START SERVER
# ================================
def start_ws_server():

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    server = websockets.serve(handler, "0.0.0.0", 6789)

    loop.run_until_complete(server)
    loop.run_forever()
