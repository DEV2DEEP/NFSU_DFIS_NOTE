# -------- Helper Functions --------
def char_to_num(c):
    return ord(c) - ord('A')

def num_to_char(n):
    return chr(n % 26 + ord('A'))

def prepare_text(text):
    text = text.upper()
    text = "".join(c for c in text if c.isalpha())
    if len(text) % 2 != 0:
        text += "X"
    return text


# -------- Matrix Operations --------
def multiply(key, vec):
    return [
        (key[0][0]*vec[0] + key[0][1]*vec[1]) % 26,
        (key[1][0]*vec[0] + key[1][1]*vec[1]) % 26
    ]

def det(key):
    return (key[0][0]*key[1][1] - key[0][1]*key[1][0]) % 26

def mod_inv(d):
    for i in range(1, 26):
        if (d * i) % 26 == 1:
            return i
    return None

def inverse(key):
    d = det(key)
    inv_d = mod_inv(d)
    if inv_d is None:
        return None

    return [
        [ key[1][1]*inv_d % 26, (-key[0][1]*inv_d) % 26],
        [(-key[1][0]*inv_d) % 26, key[0][0]*inv_d % 26]
    ]


# -------- Hill Cipher --------
def encrypt(text, key):
    text = prepare_text(text)
    res = ""
    for i in range(0, len(text), 2):
        v = [char_to_num(text[i]), char_to_num(text[i+1])]
        r = multiply(key, v)
        res += num_to_char(r[0]) + num_to_char(r[1])
    return res

def decrypt(text, key):
    inv = inverse(key)
    if inv is None:
        return None

    text = prepare_text(text)
    res = ""
    for i in range(0, len(text), 2):
        v = [char_to_num(text[i]), char_to_num(text[i+1])]
        r = multiply(inv, v)
        res += num_to_char(r[0]) + num_to_char(r[1])
    return res


# -------- CLI --------
print("\n=== Hill Cipher CLI ===")

text = input("Enter message: ")

print("Enter 2x2 key matrix:")
k1 = int(input("k1: "))
k2 = int(input("k2: "))
k3 = int(input("k3: "))
k4 = int(input("k4: "))

key = [[k1, k2], [k3, k4]]

mode = input("Encrypt (e) / Decrypt (d): ").lower()

if mode == "e":
    print("Result:", encrypt(text, key))
elif mode == "d":
    result = decrypt(text, key)
    if result is None:
        print("Error: Key matrix not invertible!")
    else:
        print("Result:", result)
else:
    print("Invalid choice!")