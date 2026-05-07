import tkinter as tk
from tkinter import messagebox


# -------- Generate Matrix --------
def generate_matrix(key):
    key = key.upper().replace("J", "I")
    matrix = []
    used = set()

    for ch in key:
        if ch.isalpha() and ch not in used:
            matrix.append(ch)
            used.add(ch)

    for ch in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if ch not in used:
            matrix.append(ch)

    return [matrix[i:i+5] for i in range(0, 25, 5)]


# -------- Prepare Text --------
def prepare_text(text):
    text = text.upper().replace("J", "I")
    text = "".join(c for c in text if c.isalpha())

    result = ""
    i = 0
    while i < len(text):
        a = text[i]
        if i+1 < len(text):
            b = text[i+1]
            if a == b:
                result += a + "X"
                i += 1
            else:
                result += a + b
                i += 2
        else:
            result += a + "X"
            i += 1
    return result


# -------- Find Position --------
def find_pos(matrix, ch):
    for r in range(5):
        for c in range(5):
            if matrix[r][c] == ch:
                return r, c


# -------- Cipher --------
def playfair(text, key, mode):
    matrix = generate_matrix(key)

    if mode == "Encrypt":
        text = prepare_text(text)
    else:
        text = text.upper().replace("J", "I")
        text = "".join(c for c in text if c.isalpha())

    result = ""

    for i in range(0, len(text), 2):
        a, b = text[i], text[i+1]
        r1, c1 = find_pos(matrix, a)
        r2, c2 = find_pos(matrix, b)

        if r1 == r2:
            if mode == "Encrypt":
                result += matrix[r1][(c1+1)%5] + matrix[r2][(c2+1)%5]
            else:
                result += matrix[r1][(c1-1)%5] + matrix[r2][(c2-1)%5]

        elif c1 == c2:
            if mode == "Encrypt":
                result += matrix[(r1+1)%5][c1] + matrix[(r2+1)%5][c2]
            else:
                result += matrix[(r1-1)%5][c1] + matrix[(r2-1)%5][c2]

        else:
            result += matrix[r1][c2] + matrix[r2][c1]

    return result


# -------- Process --------
def process():
    text = input_text.get("1.0", tk.END).strip()
    key = key_entry.get().strip()

    if not key:
        messagebox.showerror("Error", "Enter key!")
        return

    result = playfair(text, key, mode.get())

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, result)


def clear_all():
    input_text.delete("1.0", tk.END)
    output_text.delete("1.0", tk.END)
    key_entry.delete(0, tk.END)
    mode.set("Encrypt")


# -------- GUI --------

root = tk.Tk()
root.title("Playfair Cipher Tool")
root.geometry("650x500")
root.configure(bg="#f0f4ff")   # Light background color

tk.Label(root,
         text="Playfair Cipher",
         font=("Arial", 18, "bold"),
         bg="#f0f4ff",
         fg="#1a237e").pack(pady=15)

tk.Label(root, text="Enter Key:",
         bg="#f0f4ff").pack()

key_entry = tk.Entry(root, width=40)
key_entry.pack(pady=5)

tk.Label(root, text="Enter Message:",
         bg="#f0f4ff").pack()

input_text = tk.Text(root, height=4, width=60)
input_text.pack(pady=5)

mode = tk.StringVar(value="Encrypt")

tk.Radiobutton(root, text="Encrypt",
               variable=mode, value="Encrypt",
               bg="#f0f4ff").pack()

tk.Radiobutton(root, text="Decrypt",
               variable=mode, value="Decrypt",
               bg="#f0f4ff").pack()

btn_frame = tk.Frame(root, bg="#f0f4ff")
btn_frame.pack(pady=10)

tk.Button(btn_frame,
          text="Submit",
          command=process,
          bg="#4caf50",
          fg="white",
          width=12).grid(row=0, column=0, padx=10)

tk.Button(btn_frame,
          text="Clear",
          command=clear_all,
          bg="#f44336",
          fg="white",
          width=12).grid(row=0, column=1, padx=10)

tk.Label(root,
         text="Output Message:",
         bg="#f0f4ff").pack()

output_text = tk.Text(root, height=4, width=60)
output_text.pack(pady=5)

root.mainloop()
