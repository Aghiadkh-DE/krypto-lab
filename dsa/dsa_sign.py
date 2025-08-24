#!/usr/bin/env python3
"""
Digital Signature Algorithm (DSA) Signature Generation
Creates a digital signature for a message using DSA.

Usage: python dsa_sign.py [private_key_file] [message_file]

The signature will be saved as [message_file].sig
"""

import sys
import random
import hashlib
from math import gcd

def mod_inverse(a, m):
    """Calculate modular inverse using extended Euclidean algorithm"""
    if gcd(a, m) != 1:
        return None
    
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd_val, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd_val, x, y
    
    _, x, _ = extended_gcd(a % m, m)
    return (x % m + m) % m

def load_key_file(filename):
    """Load DSA parameters from key file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if len(lines) != 4:
                raise ValueError("Invalid key file format")
            
            p = int(lines[0].strip())
            q = int(lines[1].strip())
            g = int(lines[2].strip())
            key = int(lines[3].strip())
            
            return p, q, g, key
    except (IOError, ValueError) as e:
        raise ValueError(f"Error reading key file: {e}")

def load_message(filename):
    """Load message from file as string"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except IOError as e:
        raise ValueError(f"Error reading message file: {e}")

def sha224_hash(message):
    """Calculate SHA-224 hash of message"""
    return hashlib.sha224(message.encode('utf-8')).digest()

def bytes_to_int(byte_data):
    """Convert bytes to integer"""
    return int.from_bytes(byte_data, byteorder='big')

def dsa_sign(message, p, q, g, x):
    """
    Generate DSA signature for message
    
    Args:
        message: Message to sign (string)
        p, q, g: DSA parameters
        x: Private key
        
    Returns:
        (r, s): Signature tuple
    """
    # Calculate hash of message using SHA-224
    hash_bytes = sha224_hash(message)
    h = bytes_to_int(hash_bytes)
    
    # Reduce hash modulo q if necessary
    h = h % q
    
    while True:
        # Generate random k (1 < k < q)
        k = random.randint(2, q - 1)
        
        # Calculate r = (g^k mod p) mod q
        r = pow(g, k, p) % q
        
        if r == 0:
            continue  # Try again with different k
        
        # Calculate k^(-1) mod q
        k_inv = mod_inverse(k, q)
        if k_inv is None:
            continue  # Try again with different k
        
        # Calculate s = k^(-1) * (H(m) + r * x) mod q
        s = (k_inv * (h + r * x)) % q
        
        if s == 0:
            continue  # Try again with different k
        
        return r, s

def save_signature(filename, r, s):
    """Save signature to file"""
    sig_filename = filename + ".sig"
    with open(sig_filename, 'w', encoding='utf-8') as f:
        f.write(f"{r}\n")
        f.write(f"{s}\n")
    return sig_filename

def main():
    if len(sys.argv) != 3:
        print("Usage: python dsa_sign.py [private_key_file] [message_file]")
        sys.exit(1)
    
    private_key_file = sys.argv[1]
    message_file = sys.argv[2]
    
    try:
        # Load private key and parameters
        print(f"Loading private key from {private_key_file}")
        p, q, g, x = load_key_file(private_key_file)
        
        print("DSA Parameters:")
        print(f"p = {p}")
        print(f"q = {q}")
        print(f"g = {g}")
        print(f"Private key x = {x}")
        
        # Load message
        print(f"Loading message from {message_file}")
        message = load_message(message_file)
        print(f"Message: {repr(message[:100])}{'...' if len(message) > 100 else ''}")
        
        # Generate signature
        print("Generating DSA signature...")
        r, s = dsa_sign(message, p, q, g, x)
        
        print("Signature components:")
        print(f"r = {r}")
        print(f"s = {s}")
        
        # Save signature
        sig_file = save_signature(message_file, r, s)
        print(f"Signature saved to {sig_file}")
        
    except (ValueError, IOError) as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
