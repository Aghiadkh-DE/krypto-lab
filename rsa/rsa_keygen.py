
import sys
import random


def miller_rabin_test(n, k=10):
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    
    # Write n-1 as d * 2^r
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1
    
    # Perform k rounds of testing
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)  # a^d mod n
        
        if x == 1 or x == n - 1:
            continue
        
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    
    return True


def is_prime(n, k=10):
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False
    
    # Check for small prime factors first (optimization)
    small_primes = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    for p in small_primes:
        if n == p:
            return True
        if n % p == 0:
            return False
    
    return miller_rabin_test(n, k)


def generate_prime(bit_length, k=10):
    if bit_length < 2:
        raise ValueError("Bit length must be at least 2")
    
    while True:
        # Generate a random odd number with the specified bit length
        # Ensure the number has exactly bit_length bits by setting MSB and LSB
        candidate = random.getrandbits(bit_length)
        
        # Set the most significant bit to ensure bit_length bits
        candidate |= (1 << (bit_length - 1))
        
        # Set the least significant bit to ensure it's odd
        candidate |= 1
        
        if is_prime(candidate, k):
            return candidate


def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    
    gcd_val, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    
    return gcd_val, x, y


def mod_inverse(a, m):
    gcd_val, x, _ = extended_gcd(a, m)
    
    if gcd_val != 1:
        raise ValueError(f"Modular inverse of {a} modulo {m} does not exist")
    
    # Make sure the result is positive
    return (x % m + m) % m


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def generate_rsa_keypair(bit_length):
    """
    Generate an RSA key pair with the specified bit length.
    
    Args:
        bit_length (int): Desired bit length for the modulus n
        
    Returns:
        tuple: (e, d, n, p, q) where:
            e: public exponent
            d: private exponent
            n: modulus (p * q)
            p, q: the two prime factors
    """
    print(f"Generating RSA key pair with {bit_length}-bit modulus...")
    
    # Calculate bit length for individual primes
    # We want p and q such that p*q has approximately bit_length bits
    prime_bit_length = bit_length // 2
    
    print(f"Generating first prime with ~{prime_bit_length} bits...")
    p = generate_prime(prime_bit_length)
    print(f"First prime generated: {p.bit_length()} bits")
    
    print(f"Generating second prime with ~{prime_bit_length} bits...")
    while True:
        q = generate_prime(prime_bit_length)
        
        # Ensure p and q are different and not too close to each other
        if p != q and abs(p - q) > (1 << (prime_bit_length - 10)):
            break
    
    print(f"Second prime generated: {q.bit_length()} bits")
    
    # Ensure p > q for consistency
    if p < q:
        p, q = q, p
    
    # Calculate n and φ(n)
    n = p * q
    phi_n = (p - 1) * (q - 1)
    
    print(f"Modulus n has {n.bit_length()} bits")
    
    # Choose public exponent e
    # Start with the commonly used value 65537 = 2^16 + 1
    e = 65537
    
    # Ensure e is coprime to φ(n)
    while gcd(e, phi_n) != 1:
        e += 2  # Try next odd number
        if e >= phi_n:
            raise ValueError("Cannot find suitable public exponent")
    
    print(f"Public exponent e = {e}")
    
    # Calculate private exponent d
    print("Calculating private exponent...")
    d = mod_inverse(e, phi_n)
    
    # Verify the key pair
    test_message = 42
    encrypted = pow(test_message, e, n)
    decrypted = pow(encrypted, d, n)
    
    if decrypted != test_message:
        raise ValueError("Key pair verification failed")
    
    print("Key pair generated and verified successfully!")
    
    return e, d, n, p, q


def write_key_files(e, d, n, p, q, private_key_file, public_key_file, primes_file):
    try:
        # Write private key file (d, n)
        with open(private_key_file, 'w', encoding='utf-8') as f:
            f.write(f"{d}\n{n}\n")
        print(f"Private key written to: {private_key_file}")
        
        # Write public key file (e, n)
        with open(public_key_file, 'w', encoding='utf-8') as f:
            f.write(f"{e}\n{n}\n")
        print(f"Public key written to: {public_key_file}")
        
        # Write primes file (p, q)
        with open(primes_file, 'w', encoding='utf-8') as f:
            f.write(f"{p}\n{q}\n")
        print(f"Primes written to: {primes_file}")
        
    except IOError as err:
        raise IOError(f"Error writing key files: {err}") from err


def main():
    """
    Main function that handles command line arguments and orchestrates key generation.
    """
    if len(sys.argv) != 5:
        print("Usage: python rsa_keygen.py <bit_length> <private_key_file> <public_key_file> <primes_file>")
        print("\nDescription:")
        print("  bit_length:        Desired bit length for the RSA modulus")
        print("  private_key_file:  Output file for private key (d, n)")
        print("  public_key_file:   Output file for public key (e, n)")
        print("  primes_file:       Output file for prime factors (p, q)")
        print("\nExample:")
        print("  python rsa_keygen.py 1024 private.key public.key primes.txt")
        sys.exit(1)
    
    try:
        bit_length = int(sys.argv[1])
        private_key_file = sys.argv[2]
        public_key_file = sys.argv[3]
        primes_file = sys.argv[4]
        
        if bit_length < 8:
            raise ValueError("Bit length must be at least 8")
        
        print("RSA Key Generation")
        print("==================")
        print(f"Bit length: {bit_length}")
        print(f"Private key file: {private_key_file}")
        print(f"Public key file: {public_key_file}")
        print(f"Primes file: {primes_file}")
        print()
        
        # Generate RSA key pair
        e, d, n, p, q = generate_rsa_keypair(bit_length)
        
        # Write keys to files
        write_key_files(e, d, n, p, q, private_key_file, public_key_file, primes_file)
        
        print("\nKey generation completed successfully!")
        print(f"Modulus bit length: {n.bit_length()}")
        print(f"Public exponent: {e}")
        
    except (ValueError, IOError, KeyboardInterrupt) as e:
        if isinstance(e, KeyboardInterrupt):
            print("\nKey generation interrupted by user.")
        else:
            print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
