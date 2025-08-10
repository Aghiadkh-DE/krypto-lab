import sys
import random
import os

# Add parent directory to path to import from rsa module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rsa.rsa_keygen import is_prime

# Import custom modular exponentiation
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from modular_arithmetic import mod_exp


def generate_safe_prime(bit_length, k=10):
    """
    Generate a safe prime p of the form p = 2q + 1 where both p and q are prime.
    
    Args:
        bit_length (int): Desired bit length for the prime p
        k (int): Number of Miller-Rabin rounds for primality testing
        
    Returns:
        tuple: (p, q) where p = 2q + 1 and both are prime
    """
    if bit_length < 3:
        raise ValueError("Bit length must be at least 3 for safe primes")
    
    while True:
        # Generate a prime q with bit_length - 1 bits
        q_bit_length = bit_length - 1
        
        # Generate random number with q_bit_length bits
        q = random.getrandbits(q_bit_length)
        
        # Set MSB to ensure exactly q_bit_length bits
        q |= (1 << (q_bit_length - 1))
        
        # Make it odd
        q |= 1
        
        # Check if q is prime
        if is_prime(q, k):
            # Calculate p = 2q + 1
            p = 2 * q + 1
            
            # Check if p is also prime (making it a safe prime)
            if is_prime(p, k):
                return p, q


def find_generator(p, q):
    """
    Find a generator g for the group Z*_p.
    
    For a safe prime p = 2q + 1, a generator g must satisfy:
    - g^1 ≢ 1 (mod p)
    - g^2 ≢ 1 (mod p)  
    - g^q ≢ 1 (mod p)
    - g^(p-1) ≡ 1 (mod p) [this is always true by Fermat's Little Theorem]
    
    Args:
        p (int): The safe prime
        q (int): The Sophie Germain prime where p = 2q + 1
        
    Returns:
        int: A generator g for Z*_p
    """
    # Try small integers starting from 2
    for g in range(2, min(100, p)):
        # Check if g is a generator
        # For safe primes, we only need to check g^2 and g^q
        if mod_exp(g, 2, p) != 1 and mod_exp(g, q, p) != 1:
            return g
    
    # If no small generator found, try random values
    for _ in range(1000):
        g = random.randrange(2, p)
        if mod_exp(g, 2, p) != 1 and mod_exp(g, q, p) != 1:
            return g
    
    raise ValueError("Could not find a generator")


def main():
    """
    Main function that handles command line arguments and generates DH parameters.
    """
    if len(sys.argv) != 2:
        print("Usage: python dh_params.py [bit_length]", file=sys.stderr)
        print("  bit_length: Approximate desired bit length for the prime p", file=sys.stderr)
        sys.exit(1)
    
    try:
        bit_length = int(sys.argv[1])
        if bit_length < 8:
            raise ValueError("Bit length must be at least 8")
    except ValueError as e:
        print(f"Error: Invalid bit length - {e}", file=sys.stderr)
        sys.exit(1)
    
    try:
        print(f"Generating safe prime with approximately {bit_length} bits...", file=sys.stderr)
        
        # Generate safe prime p and corresponding q
        p, q = generate_safe_prime(bit_length)
        
        print(f"Safe prime p generated: {p.bit_length()} bits", file=sys.stderr)
        print(f"Sophie Germain prime q: {q.bit_length()} bits", file=sys.stderr)
        
        # Find a generator
        print("Finding generator...", file=sys.stderr)
        g = find_generator(p, q)
        
        print(f"Generator g = {g}", file=sys.stderr)
        print("DH parameters generated successfully!", file=sys.stderr)
        
        # Output the results to stdout
        print(p)
        print(g)
        
    except (ValueError, RuntimeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
