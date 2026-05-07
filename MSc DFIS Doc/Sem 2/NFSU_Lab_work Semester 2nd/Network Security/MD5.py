# Function for left rotation
def left_rotate(x, c):
    return ((x << c) | (x >> (32 - c))) & 0xFFFFFFFF

def md5(message):
    # Initialize variables
    A = 0x67452301
    B = 0xefcdab89
    C = 0x98badcfe
    D = 0x10325476

    # Convert message to bytes
    msg = bytearray(message, 'utf-8')
    orig_len = (8 * len(msg)) & 0xffffffffffffffff

    # Append '1' bit (0x80)
    msg.append(0x80)

    # Pad with zeros until length ≡ 56 mod 64
    while len(msg) % 64 != 56:
        msg.append(0)

    # Append original length (64-bit little endian)
    msg += orig_len.to_bytes(8, byteorder='little')

    # Predefined shift amounts
    s = [7,12,17,22]*4 + [5,9,14,20]*4 + \
        [4,11,16,23]*4 + [6,10,15,21]*4

    # Generate constants using sine function manually
    K = [int((abs(__import__('math').sin(i + 1)) * (2**32))) & 0xFFFFFFFF for i in range(64)]

    # Process each 512-bit chunk
    for chunk_offset in range(0, len(msg), 64):
        chunk = msg[chunk_offset:chunk_offset+64]
        M = [int.from_bytes(chunk[i:i+4], 'little') for i in range(0, 64, 4)]

        a, b, c, d = A, B, C, D

        for i in range(64):
            if i < 16:
                f = (b & c) | (~b & d)
                g = i
            elif i < 32:
                f = (d & b) | (~d & c)
                g = (5*i + 1) % 16
            elif i < 48:
                f = b ^ c ^ d
                g = (3*i + 5) % 16
            else:
                f = c ^ (b | ~d)
                g = (7*i) % 16

            temp = d
            d = c
            c = b
            b = (b + left_rotate((a + f + K[i] + M[g]) & 0xFFFFFFFF, s[i])) & 0xFFFFFFFF
            a = temp

        # Add result to current hash
        A = (A + a) & 0xFFFFFFFF
        B = (B + b) & 0xFFFFFFFF
        C = (C + c) & 0xFFFFFFFF
        D = (D + d) & 0xFFFFFFFF

    # Produce final hash (128-bit)
    result = A.to_bytes(4, 'little') + B.to_bytes(4, 'little') + \
             C.to_bytes(4, 'little') + D.to_bytes(4, 'little')

    return ''.join(f'{byte:02x}' for byte in result)


# Main program
message = input("Enter message: ")
print("MD5 Hash:", md5(message))