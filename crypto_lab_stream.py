# CS 308 
# Lab Assignment: Cryptography in Python
# Lecture 6 — Sections 3.4–3.5
#
# Name: Lorenzo Richardson
# Date: 03/02/2026


# ==============================================================================
# TASK 1: XOR Stream Cipher (5 points) - Expanded Version
# ==============================================================================

def text_to_bits(text):
    """Convert a string to a string of '0' and '1' bits (8 bits per char)."""

    rslt = ""
    
    for char in text:
        ascii_value = ord(char)
        binary_string = format(ascii_value, '08b')
        rslt = rslt + binary_string
        
    return rslt


def bits_to_text(bits):
    """Convert a string of '0' and '1' bits back to a string."""

    rslt = ""
    
    for i in range(0, len(bits), 8):
        byte_string = bits[i : i+8]
        ascii_value = int(byte_string, 2)
        ch = chr(ascii_value)
        
        rslt = rslt + ch
        
    return rslt


def generate_keystream(key, length):
    """
    Generate a keystream of the given bit length by repeating
    the key's bits. Same key + same length = same keystream.
    """
    key_bits = text_to_bits(key)
    
    if len(key_bits) == 0:
        return ""
    
    keystream = ""
    
    while len(keystream) < length:
        keystream = keystream + key_bits
        
    return keystream[:length]


def xor_encrypt(plaintext, key):
    """
    Encrypt plaintext using XOR with a repeating keystream.
    Return the ciphertext as a bit string.
    """

    pt_bits = text_to_bits(plaintext)
    
    ks_bits = generate_keystream(key, len(pt_bits))
    
    ciphertext = ""
    
    for i in range(len(pt_bits)):
        # XOR Logic: If the bits are different, the rslt is '1'
        if pt_bits[i] != ks_bits[i]:
            ciphertext = ciphertext + '1'
        # XOR Logic: If the bits are the same, the rslt is '0'
        else:
            ciphertext = ciphertext + '0'
            
    return ciphertext


def xor_decrypt(ct_bits, key):
    """
    Decrypt a ciphertext bit string using XOR with the same key.
    Return the plaintext string.
    """
    ks_bits = generate_keystream(key, len(ct_bits))
    
    pt_bits = ""
    
    for i in range(len(ct_bits)):

        if ct_bits[i] != ks_bits[i]:
            pt_bits = pt_bits + '1'
        else:
            pt_bits = pt_bits + '0'
            
    return bits_to_text(pt_bits)


# ==============================================================================
# TEST CASES — All must pass
# ==============================================================================

bits = text_to_bits("AB")
assert bits == "0100000101000010"
assert bits_to_text(bits) == "AB"

ct = xor_encrypt("HELLO", "K")
assert xor_decrypt(ct, "K") == "HELLO"

# Demonstrate: wrong key produces wrong plaintext
assert xor_decrypt(ct, "Z") != "HELLO"

print("All tests passed!")


# Task 1 Questions (answer below):
# Q1: Why does XOR decryption use the exact same operation as encryption?
# A1:
#
# Q2: If a 1-bit error occurs in the ciphertext, how many bits of the decrypted
#     plaintext are affected? Why?
# A2: