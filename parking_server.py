import asyncio
import websockets
import serial

# Serial connection setup (adjust the port to your Arduino's connection)
try:
    ser = serial.Serial('/dev/cu.usbmodem11101', 9600)  # Adjust this port accordingly
except serial.SerialException as e:
    print(f"Error connecting to serial port: {e}")
    exit(1)

# WebSocket server to send data to mobile devices
connected_clients = set()

# WebSocket handler to handle incoming connections from mobile devices
async def websocket_handler(websocket, path):
    connected_clients.add(websocket)
    try:
        while True:
            data = await websocket.recv()  # Receive any incoming message from the client (if needed)
            print(f"Received from mobile: {data}")
    except websockets.exceptions.ConnectionClosed as e:
        print(f"Connection closed: {e}")
    finally:
        connected_clients.remove(websocket)

# Start the WebSocket servers
async def start_websocket_server():
    server = await websockets.serve(websocket_handler, "0.0.0.0", 8766)
    await server.wait_closed()

# Function to read serial data and broadcast to mobile devices
async def read_serial_and_broadcast():
    while True:
        if ser.in_waiting > 0:  # Check if there's data in the serial buffer
            line = ser.readline().decode('utf-8').strip()  # Read a line from the serial input
            print(f"Serial Data Received: {line}")  # Debugging: Check what data is received
            
            # Only broadcast data for Space 1 and Space 2
            if "Space 1" in line or "Space 2" in line:
                for client in connected_clients:
                    await client.send(line)  # Send the message to the mobile device
        await asyncio.sleep(0.1)  # Avoid overloading the CPU

# Start both tasks in the same event loop
loop = asyncio.get_event_loop()
loop.create_task(start_websocket_server())
loop.create_task(read_serial_and_broadcast())
loop.run_forever()
