import asyncio
import websockets

async def handle_client(websocket, path):
    async for message in websocket:
        print(f"Received message: {message}")
        # Example: echo the message back to the client
        await websocket.send(f"Server received: {message}")

async def main():
    async with websockets.serve(handle_client, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
