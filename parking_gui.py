import serial
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk  # Requires Pillow library for icons

# Set up serial communication (adjust port and baud rate)
ser = serial.Serial('/dev/cu.usbmodem11101', 9600)  # Adjust the port accordingly

# Initialize the Tkinter window
root = tk.Tk()
root.title("Parking Space Occupancy")
root.geometry("400x200")  # Set window size
root.config(bg="#f0f4f8")  # Light background color

# Load icons for occupied and unoccupied status
occupied_img = Image.open("occupied_icon.png").resize((300, 300))
unoccupied_img = Image.open("unoccupied_icon.png").resize((300, 300))
occupied_icon = ImageTk.PhotoImage(occupied_img)
unoccupied_icon = ImageTk.PhotoImage(unoccupied_img) 

# Define labels for Space 1 and Space 2 with icons
spaces = {}
for i in range(1, 3):  # Only for Space 1 and 2
    frame = tk.Frame(root, bg="#ffffff", relief="solid", bd=1, padx=10, pady=10)
    frame.pack(pady=10, fill="x", padx=20)
    
    label_text = Label(frame, text=f"Space {i}: Checking...", font=("Helvetica", 16), fg="#333")
    label_text.grid(row=0, column=1, padx=10)
    label_icon = Label(frame, image=unoccupied_icon, bg="#ffffff")  # Start with unoccupied icon
    label_icon.grid(row=0, column=0)
    spaces[i] = (label_text, label_icon)

# Update the GUI based on serial data
def update_spaces():
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()
        if "Occupied" in line:
            space_num = int(line.split()[1])
            if space_num in spaces:  # Only update if space 1 or 2
                spaces[space_num][0].config(text=f"Space {space_num}: Occupied", fg="red")
                spaces[space_num][1].config(image=occupied_icon)
        elif "Unoccupied" in line:
            space_num = int(line.split()[1])
            if space_num in spaces:  # Only update if space 1 or 2
                spaces[space_num][0].config(text=f"Space {space_num}: Unoccupied", fg="green")
                spaces[space_num][1].config(image=unoccupied_icon)
    root.after(100, update_spaces)

# Schedule the GUI updates
root.after(100, update_spaces)
root.mainloop()

