"""
Digital Signature Algorithm (DSA) Core Implementation
"""

import hashlib
import random
from typing import Tuple


def miller_rabin_test(n: int, k: int = 5) -> bool:
    """Miller-Rabin primality test"""
    if n == 2 or n == 3:
        return True
    if n < 2 or n % 2 == 0:
        return False
    
    # Write n-1 as d * 2^r
    r = 0
    d = n - 1
    while d % 2 == 0:
        d //= 2
        r += 1
    
    # Perform k rounds of testing
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


def generate_prime(bits: int) -> int:
    """Generate a prime number with specified bit length"""
    while True:
        candidate = random.getrandbits(bits)
        # Ensure it's odd and has the right bit length
        candidate |= (1 << bits - 1) | 1
        
        if miller_rabin_test(candidate):
            return candidate


def generate_dsa_parameters(L: int = 1024, N: int = 160) -> Tuple[int, int, int]:
    """
    Generate DSA parameters (p, q, g)
    L: bit length of prime p (default 1024)
    N: bit length of prime q (default 160)
    """
    # Generate q (N-bit prime)
    q = generate_prime(N)
    
    # Generate p (L-bit prime such that q divides p-1)
    while True:
        # Generate a random number and adjust to make p-1 divisible by q
        p_candidate = random.getrandbits(L)
        p_candidate |= (1 << L - 1) | 1  # Ensure L bits and odd
        
        # Make p ≡ 1 (mod q)
        p = p_candidate - (p_candidate % q) + 1
        
        if p.bit_length() == L and miller_rabin_test(p):
            break
    
    # Generate g
    h = 2
    while True:
        g = pow(h, (p - 1) // q, p)
        if g > 1:
            break
        h += 1
    
    return p, q, g


def generate_dsa_keypair(p: int, q: int, g: int) -> Tuple[int, int]:
    """
    Generate DSA key pair
    Returns (private_key, public_key)
    """
    # Private key x: random integer in [1, q-1]
    x = random.randrange(1, q)
    
    # Public key y = g^x mod p
    y = pow(g, x, p)
    
    return x, y


def dsa_sign(message: str, p: int, q: int, g: int, x: int) -> Tuple[int, int]:
    """
    Sign a message using DSA
    Returns (r, s) signature pair
    """
    # Hash the message
    hash_obj = hashlib.sha1()
    hash_obj.update(message.encode('utf-8'))
    message_hash = int.from_bytes(hash_obj.digest(), byteorder='big')
    
    while True:
        # Generate random k in [1, q-1]
        k = random.randrange(1, q)
        
        # Calculate r = (g^k mod p) mod q
        r = pow(g, k, p) % q
        
        if r == 0:
            continue
        
        # Calculate k^(-1) mod q
        k_inv = pow(k, -1, q)
        
        # Calculate s = k^(-1) * (H(m) + x*r) mod q
        s = (k_inv * (message_hash + x * r)) % q
        
        if s == 0:
            continue
        
        return r, s


def dsa_verify(message: str, r: int, s: int, p: int, q: int, g: int, y: int) -> bool:
    """
    Verify a DSA signature
    Returns True if signature is valid, False otherwise
    """
    # Check that 0 < r < q and 0 < s < q
    if not (0 < r < q and 0 < s < q):
        return False
    
    # Hash the message
    hash_obj = hashlib.sha1()
    hash_obj.update(message.encode('utf-8'))
    message_hash = int.from_bytes(hash_obj.digest(), byteorder='big')
    
    # Calculate w = s^(-1) mod q
    try:
        w = pow(s, -1, q)
    except ValueError:
        return False
    
    # Calculate u1 = H(m) * w mod q
    u1 = (message_hash * w) % q
    
    # Calculate u2 = r * w mod q
    u2 = (r * w) % q
    
    # Calculate v = ((g^u1 * y^u2) mod p) mod q
    v = (pow(g, u1, p) * pow(y, u2, p)) % p % q
    
    # Signature is valid if v == r
    return v == r


def write_key_file(filename: str, p: int, q: int, g: int, key: int) -> None:
    """Write key file with p, q, g, and key value"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"{p}\n")
        f.write(f"{q}\n")
        f.write(f"{g}\n")
        f.write(f"{key}\n")


def read_key_file(filename: str) -> Tuple[int, int, int, int]:
    """Read key file and return p, q, g, and key value"""
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.read().strip().split('\n')
        p = int(lines[0])
        q = int(lines[1])
        g = int(lines[2])
        key = int(lines[3])
        return p, q, g, key


def read_message_file(filename: str) -> str:
    """Read message from file as string"""
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()
