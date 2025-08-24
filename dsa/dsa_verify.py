#!/usr/bin/env python3
"""
Digital Signature Algorithm (DSA) Signature Verification
Verifies a digital signature using DSA.

Usage: python dsa_verify.py [public_key_file] [message_file]

The signature is expected to be in [message_file].sig
"""

import sys
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
        raise ValueError(f"Error reading key file: {e}") from e

def load_message(filename):
    """Load message from file as string"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except IOError as e:
        raise ValueError(f"Error reading message file: {e}") from e

def load_signature(filename):
    """Load signature from file"""
    sig_filename = filename + ".sig"
    try:
        with open(sig_filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if len(lines) != 2:
                raise ValueError("Invalid signature file format")
            
            r = int(lines[0].strip())
            s = int(lines[1].strip())
            
            return r, s
    except (IOError, ValueError) as e:
        raise ValueError(f"Error reading signature file: {e}") from e

def sha224_hash(message):
    """Calculate SHA-224 hash of message"""
    return hashlib.sha224(message.encode('utf-8')).digest()

def bytes_to_int(byte_data):
    """Convert bytes to integer"""
    return int.from_bytes(byte_data, byteorder='big')

def dsa_verify(message, r, s, p, q, g, y):
    """
    Verify DSA signature for message
    
    Args:
        message: Original message (string)
        r, s: Signature components
        p, q, g: DSA parameters
        y: Public key
        
    Returns:
        bool: True if signature is valid, False otherwise
    """
    # Check signature components are in valid range
    if not (0 < r < q) or not (0 < s < q):
        return False
    
    # Calculate hash of message using SHA-224
    hash_bytes = sha224_hash(message)
    h = bytes_to_int(hash_bytes)
    
    # Reduce hash modulo q if necessary
    h = h % q
    
    # Calculate w = s^(-1) mod q
    w = mod_inverse(s, q)
    if w is None:
        return False
    
    # Calculate u1 = H(m) * w mod q
    u1 = (h * w) % q
    
    # Calculate u2 = r * w mod q
    u2 = (r * w) % q
    
    # Calculate v = (g^u1 * y^u2 mod p) mod q
    v = (pow(g, u1, p) * pow(y, u2, p)) % p % q
    
    # Signature is valid if v == r
    return v == r

def main():
    if len(sys.argv) != 3:
        print("Usage: python dsa_verify.py [public_key_file] [message_file]")
        sys.exit(1)
    
    public_key_file = sys.argv[1]
    message_file = sys.argv[2]
    
    try:
        # Load public key and parameters
        print(f"Loading public key from {public_key_file}")
        p, q, g, y = load_key_file(public_key_file)
        
        print("DSA Parameters:")
        print(f"p = {p}")
        print(f"q = {q}")
        print(f"g = {g}")
        print(f"Public key y = {y}")
        
        # Load message
        print(f"Loading message from {message_file}")
        message = load_message(message_file)
        print(f"Message: {repr(message[:100])}{'...' if len(message) > 100 else ''}")
        
        # Load signature
        print(f"Loading signature from {message_file}.sig")
        r, s = load_signature(message_file)
        
        print("Signature components:")
        print(f"r = {r}")
        print(f"s = {s}")
        
        # Verify signature
        print("Verifying DSA signature...")
        is_valid = dsa_verify(message, r, s, p, q, g, y)
        
        if is_valid:
            print("Signature is VALID")
        else:
            print("Signature is INVALID")
        
        return 0 if is_valid else 1
        
    except (ValueError, IOError) as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
