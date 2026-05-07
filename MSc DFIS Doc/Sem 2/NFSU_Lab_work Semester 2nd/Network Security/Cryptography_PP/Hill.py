import tkinter as tk
from tkinter import messagebox


# -------- Helper Functions --------

def char_to_num(c):
    return ord(c) - ord('A')

def num_to_char(n):
    return chr(n % 26 + ord('A'))

def prepare_text(text):
    text = text.upper()
    text = "".join([c for c in text if c.isalpha()])
    if len(text) % 2 != 0:
        text += "X"
    return text


# -------- Matrix Operations --------

def multiply_matrix(key, vector):
    return [
        (key[0][0]*vector[0] + key[0][1]*vector[1]) % 26,
        (key[1][0]*vector[0] + key[1][1]*vector[1]) % 26
    ]

def determinant(key):
    return (key[0][0]*key[1][1] - key[0][1]*key[1][0]) % 26

def mod_inverse(det):
    for i in range(1, 26):
        if (det * i) % 26 == 1:
            return i
    return None

def inverse_matrix(key):
    det = determinant(key)
    inv_det = mod_inverse(det)
    if inv_det is None:
        return None

    return [
        [ key[1][1]*inv_det % 26, (-key[0][1]*inv_det) % 26],
        [(-key[1][0]*inv_det) % 26, key[0][0]*inv_det % 26]
    ]


# -------- Hill Cipher --------

def hill_encrypt(text, key):
    text = prepare_text(text)
    result = ""
    for i in range(0, len(text), 2):
        vector = [char_to_num(text[i]), char_to_num(text[i+1])]
        encrypted = multiply_matrix(key, vector)
        result += num_to_char(encrypted[0]) + num_to_char(encrypted[1])
    return result

def hill_decrypt(text, key):
    inv_key = inverse_matrix(key)
    if inv_key is None:
        return None

    text = prepare_text(text)
    result = ""
    for i in range(0, len(text), 2):
        vector = [char_to_num(text[i]), char_to_num(text[i+1])]
        decrypted = multiply_matrix(inv_key, vector)
        result += num_to_char(decrypted[0]) + num_to_char(decrypted[1])
    return result


# -------- GUI Functions --------

def process_text():
    text = input_text.get("1.0", tk.END).strip()

    try:
        key = [
            [int(k1.get()), int(k2.get())],
            [int(k3.get()), int(k4.get())]
        ]
    except:
        messagebox.showerror("Error", "Enter valid key numbers!")
        return

    if mode.get() == "Encrypt":
        result = hill_encrypt(text, key)
    else:
        result = hill_decrypt(text, key)
        if result is None:
            messagebox.showerror("Error", "Key matrix not invertible!")
            return

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, result)


def clear_all():
    input_text.delete("1.0", tk.END)
    output_text.delete("1.0", tk.END)
    k1.delete(0, tk.END)
    k2.delete(0, tk.END)
    k3.delete(0, tk.END)
    k4.delete(0, tk.END)
    mode.set("Encrypt")


# -------- GUI Design --------

root = tk.Tk()
root.title("Hill Cipher Tool (2x2)")
root.geometry("700x550")
root.configure(bg="#f2f6ff")  # Light background color

title = tk.Label(root,
                 text="Hill Cipher (2x2 Matrix)",
                 font=("Arial", 18, "bold"),
                 bg="#f2f6ff",
                 fg="#1a237e")
title.pack(pady=15)

# Input Section
tk.Label(root, text="Enter Message:",
         bg="#f2f6ff", font=("Arial", 12)).pack()

input_text = tk.Text(root, height=4, width=60)
input_text.pack(pady=5)

# Key Frame (Colored)
key_frame = tk.LabelFrame(root,
                          text="Enter 2x2 Key Matrix",
                          font=("Arial", 12, "bold"),
                          bg="#dfe9ff",
                          fg="#0d47a1",
                          padx=10, pady=10)
key_frame.pack(pady=10)

k1 = tk.Entry(key_frame, width=5)
k2 = tk.Entry(key_frame, width=5)
k3 = tk.Entry(key_frame, width=5)
k4 = tk.Entry(key_frame, width=5)

k1.grid(row=0, column=0, padx=5, pady=5)
k2.grid(row=0, column=1, padx=5, pady=5)
k3.grid(row=1, column=0, padx=5, pady=5)
k4.grid(row=1, column=1, padx=5, pady=5)

# Mode
mode = tk.StringVar(value="Encrypt")

tk.Radiobutton(root, text="Encrypt",
               variable=mode, value="Encrypt",
               bg="#f2f6ff").pack()

tk.Radiobutton(root, text="Decrypt",
               variable=mode, value="Decrypt",
               bg="#f2f6ff").pack()

# Buttons (Colored)
btn_frame = tk.Frame(root, bg="#f2f6ff")
btn_frame.pack(pady=15)

submit_btn = tk.Button(btn_frame,
                       text="Submit",
                       command=process_text,
                       bg="#4caf50",
                       fg="white",
                       font=("Arial", 11, "bold"),
                       width=12)
submit_btn.grid(row=0, column=0, padx=10)

clear_btn = tk.Button(btn_frame,
                      text="Clear",
                      command=clear_all,
                      bg="#e53935",
                      fg="white",
                      font=("Arial", 11, "bold"),
                      width=12)
clear_btn.grid(row=0, column=1, padx=10)

# Output
tk.Label(root, text="Output Message:",
         bg="#f2f6ff", font=("Arial", 12)).pack()

output_text = tk.Text(root, height=4, width=60)
output_text.pack(pady=5)

root.mainloop()
