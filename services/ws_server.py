import asyncio
import websockets
import json
import threading

clients = set()


# ================================
# CLIENT HANDLING
# ================================
async def handler(ws):

    clients.add(ws)
    try:
        async for _ in ws:
            pass
    finally:
        clients.remove(ws)


# ================================
# BROADCAST (PnL / event push)
# ================================
async def _broadcast(data):

    if clients:
        msg = json.dumps(data)

        await asyncio.gather(
            *[c.send(msg) for c in clients],
            return_exceptions=True
        )


def broadcast(data):

    try:
        loop = asyncio.get_event_loop()
        loop.create_task(_broadcast(data))
    except RuntimeError:
        # fallback (thread safe)
        asyncio.run(_broadcast(data))


# ================================
# START SERVER
# ================================
def start_ws_server():

    async def main():
        async with websockets.serve(handler, "0.0.0.0", 6789):
            await asyncio.Future()

    asyncio.run(main())
