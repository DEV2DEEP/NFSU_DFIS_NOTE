import tkinter as tk
from tkinter import messagebox

# Caesar Cipher Function
def caesar_cipher(text, shift, mode):
    result = ""
    for char in text:
        if char.isalpha():
            ascii_base = ord('A') if char.isupper() else ord('a')     
            if mode == "encrypt":
                shifted = (ord(char) - ascii_base + shift) % 26
            else:  # decrypt
                shifted = (ord(char) - ascii_base - shift) % 26
            
            result += chr(shifted + ascii_base)
        else:
            result += char
    return result

# Process Button Function
def process_text():
    text = input_text.get("1.0", tk.END).strip()
    shift = shift_entry.get()
    if not shift.isdigit():
        messagebox.showerror("Error", "Shift must be a number!")
        return
    shift = int(shift)
    if mode.get() == "Encrypt":
        result = caesar_cipher(text, shift, "encrypt")
    else:
        result = caesar_cipher(text, shift, "decrypt")
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, result)

def clear_all():
    input_text.delete("1.0", tk.END)
    output_text.delete("1.0", tk.END)
    shift_entry.delete(0, tk.END)
    mode.set("Encrypt")  # Reset to default

# -----------------------
# GUI Design
# -----------------------

root = tk.Tk()
root.title("Caesar Cipher - Encryption & Decryption")
root.geometry("500x480")
root.configure(bg="lightblue")
title_label = tk.Label(root, text="Caesar Cipher Tool", font=("Arial", 16, "bold"), bg="lightblue")
title_label.pack(pady=10)

# Input Text
tk.Label(root, text="Enter Message:", bg="lightblue").pack()
input_text = tk.Text(root, height=5, width=50)
input_text.pack(pady=5)

# Shift Value
tk.Label(root, text="Enter Shift Value:", bg="lightblue").pack()
shift_entry = tk.Entry(root)
shift_entry.pack(pady=5)

# Mode Selection
mode = tk.StringVar(value="Encrypt")
tk.Radiobutton(root, text="Encrypt", variable=mode, value="Encrypt", bg="lightblue").pack()
tk.Radiobutton(root, text="Decrypt", variable=mode, value="Decrypt", bg="lightblue").pack()

# Buttons Frame
button_frame = tk.Frame(root, bg="lightblue")
button_frame.pack(pady=10)
process_button = tk.Button(button_frame, text="Submit", command=process_text, bg="green", fg="white", width=10)
process_button.grid(row=0, column=0, padx=10)
clear_button = tk.Button(button_frame, text="Clear", command=clear_all, bg="red", fg="white", width=10)
clear_button.grid(row=0, column=1, padx=10)

# Output Text
tk.Label(root, text="Output Message:", bg="lightblue").pack()
output_text = tk.Text(root, height=5, width=50)
output_text.pack(pady=5)
root.mainloop()
