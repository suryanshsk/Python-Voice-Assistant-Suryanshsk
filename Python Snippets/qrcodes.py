import tkinter as tk
from tkinter import filedialog, messagebox, StringVar, OptionMenu, simpledialog
import cv2
from pyzbar.pyzbar import decode
import qrcode
import os
import json
import datetime

# File to store the QR code history
HISTORY_FILE = "qr_code_history.json"

# Load QR code history from file
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as file:
            return json.load(file)
    return []

# Save QR code history to file
def save_history(data):
    with open(HISTORY_FILE, 'w') as file:
        json.dump(data, file)

# Function to scan QR code
def scan_qr_code():
    file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        img = cv2.imread(file_path)
        qr_codes = decode(img)
        
        if qr_codes:
            qr_data = qr_codes[0].data.decode('utf-8')
            messagebox.showinfo("QR Code Data", f"Data: {qr_data}")
            history.append({"data": qr_data, "timestamp": str(datetime.datetime.now())})
            save_history(history)
        else:
            messagebox.showwarning("No QR Code", "No QR code found in the image.")

# Function to generate QR code
def generate_qr_code():
    data = entry.get().strip()
    format_choice = format_var.get()

    if not data:
        messagebox.showwarning("Input Error", "Please enter data to generate QR code.")
        return

    if not is_valid_data(data):
        messagebox.showwarning("Validation Error", "Invalid data format. Please enter a valid URL or text.")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=f".{format_choice.lower()}", filetypes=[(f"{format_choice} files", f"*.{format_choice.lower()}")])
    
    if file_path:
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)

            img = qr.make_image(fill='black', back_color='white')
            img.save(file_path)
            messagebox.showinfo("Success", f"QR code generated and saved as {file_path}.")
            history.append({"data": data, "timestamp": str(datetime.datetime.now()), "file_path": file_path})
            save_history(history)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the QR code: {e}")

# Function to validate data
def is_valid_data(data):
    # Simple URL validation for demonstration (improve as needed)
    return data.startswith("http://") or data.startswith("https://") or data

# Set up the main application window
app = tk.Tk()
app.title("QR Code Generator and Scanner")

# Initialize history
history = load_history()

# Entry field for QR code data
entry_label = tk.Label(app, text="Enter Data for QR Code:")
entry_label.pack(pady=10)

entry = tk.Entry(app, width=40)
entry.pack(pady=5)

# Dropdown for file format selection
format_var = StringVar(app)
format_var.set("PNG")  # Default value
format_choices = ["PNG", "JPEG", "SVG"]
format_menu = OptionMenu(app, format_var, *format_choices)
format_menu.pack(pady=10)

# Generate button
generate_button = tk.Button(app, text="Generate QR Code", command=generate_qr_code)
generate_button.pack(pady=10)

# Scan button
scan_button = tk.Button(app, text="Scan QR Code", command=scan_qr_code)
scan_button.pack(pady=10)

# History button
def show_history():
    history_window = tk.Toplevel(app)
    history_window.title("QR Code History")
    history_list = tk.Listbox(history_window, width=50, height=10)
    history_list.pack(pady=10)
    
    for entry in history:
        display_text = f"Data: {entry['data']} | Timestamp: {entry['timestamp']}"
        history_list.insert(tk.END, display_text)
    
    close_button = tk.Button(history_window, text="Close", command=history_window.destroy)
    close_button.pack(pady=5)

history_button = tk.Button(app, text="Show QR Code History", command=show_history)
history_button.pack(pady=10)

# Run the application
app.mainloop()
