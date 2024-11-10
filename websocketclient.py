import asyncio
import websockets

async def connect():
    uri = "ws://localhost:8766"  # WebSocket server URL
    async with websockets.connect(uri) as websocket:
        print("Connected to WebSocket server")

        # Send a test message to the WebSocket server
        await websocket.send("Hello Server!")

        # Receive the response from the server
        response = await websocket.recv()
        print(f"Received from server: {response}")

# Run the client
asyncio.get_event_loop().run_until_complete(connect())
