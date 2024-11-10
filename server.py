import serial
from flask import Flask, jsonify, render_template_string
from threading import Thread

# Setup serial connection to Arduino
arduino = serial.Serial('/dev/cu.usbmodem11101', 9600)  # Replace with your actual serial port
app = Flask(__name__)

# Initialize status variables for Space 1 and Space 2
space1_status = "Loading..."
space2_status = "Loading..."

def update_status():
    global space1_status, space2_status
    while True:
        line = arduino.readline().decode('utf-8').strip()
        
        # Debugging output to see the raw line from Arduino
        print("Received from Arduino:", line)

        # Update the status for Space 1
        if "Space 1" in line:
            if "Occupied" in line:
                space1_status = "Occupied"
            elif "Unoccupied" in line:
                space1_status = "Unoccupied"

        # Update the status for Space 2
        elif "Space 2" in line:
            if "Occupied" in line:
                space2_status = "Occupied"
            elif "Unoccupied" in line:
                space2_status = "Unoccupied"

# Start the status update function in a background thread
thread = Thread(target=update_status)
thread.daemon = True
thread.start()

@app.route('/status')
def get_status():
    # Return the current status of Space 1 and Space 2
    return jsonify(space1=space1_status, space2=space2_status)

@app.route('/')
def index():
    # Serve the HTML page with embedded JavaScript and CSS
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Parking Space Status</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; }
                h1 { color: #333; }
                .space { display: inline-block; padding: 20px; margin: 10px; width: 120px; height: 120px; border-radius: 10px; color: white; font-size: 1.5em; font-weight: bold; }
                .occupied { background-color: red; }
                .unoccupied { background-color: green; }
            </style>
            <script>
                function updateStatus() {
                    fetch('/status')
                        .then(response => response.json())
                        .then(data => {
                            document.getElementById('space1').innerText = data.space1;
                            document.getElementById('space1').className = 'space ' + (data.space1 === 'Occupied' ? 'occupied' : 'unoccupied');
                            
                            document.getElementById('space2').innerText = data.space2;
                            document.getElementById('space2').className = 'space ' + (data.space2 === 'Occupied' ? 'occupied' : 'unoccupied');
                        });
                }
                setInterval(updateStatus, 1000);  // Update every second
            </script>
        </head>
        <body>
            <h1>Parking Space Status</h1>
            <div id="space1" class="space">Loading...</div>
            <div id="space2" class="space">Loading...</div>
        </body>
    </html>
    ''')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5200)  # Listen on all interfaces so your phone can access it
