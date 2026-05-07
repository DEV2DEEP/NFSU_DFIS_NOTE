# Generate matrix
def gen_matrix(key):
    key = key.upper().replace("J", "I")
    seen = []
    
    for c in key:
        if c.isalpha() and c not in seen:
            seen.append(c)
    
    for c in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if c not in seen:
            seen.append(c)
    
    return [seen[i:i+5] for i in range(0, 25, 5)]


# Prepare text
def prep(text):
    text = text.upper().replace("J", "I")
    text = "".join(c for c in text if c.isalpha())
    
    res, i = "", 0
    while i < len(text):
        a = text[i]
        b = text[i+1] if i+1 < len(text) else "X"
        
        if a == b:
            res += a + "X"
            i += 1
        else:
            res += a + b
            i += 2
    
    return res


# Find position
def pos(m, ch):
    for i in range(5):
        for j in range(5):
            if m[i][j] == ch:
                return i, j


# Cipher
def playfair(text, key, enc=True):
    m = gen_matrix(key)
    text = prep(text) if enc else "".join(c for c in text.upper() if c.isalpha())
    
    out = ""
    for i in range(0, len(text), 2):
        a, b = text[i], text[i+1]
        r1, c1 = pos(m, a)
        r2, c2 = pos(m, b)
        
        if r1 == r2:
            shift = 1 if enc else -1
            out += m[r1][(c1+shift)%5] + m[r2][(c2+shift)%5]
        
        elif c1 == c2:
            shift = 1 if enc else -1
            out += m[(r1+shift)%5][c1] + m[(r2+shift)%5][c2]
        
        else:
            out += m[r1][c2] + m[r2][c1]
    
    return out


# -------- MAIN --------
key = input("Key: ")
text = input("Message: ")
mode = input("Encrypt (e) / Decrypt (d): ").lower()

result = playfair(text, key, enc=(mode == "e"))

print("Result:", result)