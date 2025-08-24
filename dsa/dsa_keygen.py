#!/usr/bin/env python3
"""
Digital Signature Algorithm (DSA) Key Generation
Generates public and private key files with DSA parameters.

Usage: python dsa_keygen.py [public_key_file] [private_key_file]

Parameters:
- L = 1024 (bit length of p)
- N = 160 (bit length of q)
- Hash function: SHA-224
"""

import sys
import random
from math import gcd

def is_prime(n, k=20):
    """Miller-Rabin primality test"""
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    
    # Write n-1 as d * 2^r
    r = 0
    d = n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    
    # Witness loop
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime(bits):
    """Generate a prime number with specified bit length"""
    while True:
        # Generate random number with specified bit length
        p = random.getrandbits(bits)
        # Ensure it has the right bit length (MSB = 1)
        p |= (1 << (bits - 1))
        # Ensure it's odd
        p |= 1
        
        if is_prime(p):
            return p

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

def generate_dsa_parameters():
    """Generate DSA parameters (p, q, g) according to specifications"""
    N = 160  # bit length of q
    L = 1024  # bit length of p
    
    print("Generating DSA parameters...")
    print(f"L = {L}, N = {N}")
    
    # Step 1: Generate prime q of length N (160 bits)
    print("Generating prime q...")
    q = generate_prime(N)
    print(f"Generated q: {q}")
    
    # Step 2: Generate prime p = k*q + 1 of length L (1024 bits)
    print("Generating prime p...")
    target_bits = L
    min_k = (1 << (target_bits - 1)) // q
    max_k = (1 << target_bits) // q
    
    p = None
    k = None
    
    for _ in range(10000):  # Limit attempts
        k = random.randint(min_k, max_k)
        p_candidate = k * q + 1
        
        # Check if p has the right bit length
        if p_candidate.bit_length() == target_bits and is_prime(p_candidate):
            p = p_candidate
            break
    
    if p is None:
        raise ValueError("Could not generate suitable prime p")
    
    print(f"Generated p: {p}")
    print(f"k = {k}")
    
    # Step 3: Find generator g with order q
    print("Finding generator g...")
    for _ in range(1000):
        h = random.randint(2, p - 1)
        g = pow(h, k, p)
        if g != 1:
            # Verify that g has order q
            if pow(g, q, p) == 1:
                print(f"Generated g: {g}")
                break
    else:
        raise ValueError("Could not generate suitable generator g")
    
    return p, q, g

def generate_keypair(p, q, g):
    """Generate DSA key pair"""
    # Generate private key x (1 < x < q)
    x = random.randint(2, q - 1)
    
    # Calculate public key y = g^x mod p
    y = pow(g, x, p)
    
    return x, y

def save_key_file(filename, p, q, g, key):
    """Save key to file with specified format"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"{p}\n")
        f.write(f"{q}\n")
        f.write(f"{g}\n")
        f.write(f"{key}\n")

def main():
    if len(sys.argv) != 3:
        print("Usage: python dsa_keygen.py [public_key_file] [private_key_file]")
        sys.exit(1)
    
    public_key_file = sys.argv[1]
    private_key_file = sys.argv[2]
    
    try:
        # Generate DSA parameters
        p, q, g = generate_dsa_parameters()
        
        # Generate key pair
        print("Generating key pair...")
        x, y = generate_keypair(p, q, g)
        
        # Save keys to files
        print(f"Saving public key to {public_key_file}")
        save_key_file(public_key_file, p, q, g, y)
        
        print(f"Saving private key to {private_key_file}")
        save_key_file(private_key_file, p, q, g, x)
        
        print("DSA key generation completed successfully!")
        print(f"Public key (y): {y}")
        print(f"Private key (x): {x}")
        
    except (ValueError, IOError) as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
