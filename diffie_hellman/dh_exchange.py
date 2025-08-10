import sys
import secrets
import os

# Add parent directory to path to import utility functions
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import custom modular exponentiation
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from modular_arithmetic import mod_exp


def generate_private_key(p):
    """
    Generate a cryptographically secure random private key.
    
    Args:
        p (int): The prime modulus
        
    Returns:
        int: A random integer a where 2 ≤ a < p-1
    """
    if p <= 3:
        raise ValueError("Prime p must be greater than 3")
    
    # Generate a random integer in the range [2, p-2]
    # We use secrets for cryptographically secure randomness
    while True:
        a = secrets.randbelow(p - 3) + 2  # Range [2, p-2]
        if 2 <= a <= p - 2:
            return a


def compute_public_value(g, a, p):
    """
    Compute the public value A = g^a mod p.
    
    Args:
        g (int): The generator
        a (int): The private key
        p (int): The prime modulus
        
    Returns:
        int: The public value A
    """
    return mod_exp(g, a, p)


def compute_shared_secret(B, a, p):
    """
    Compute the shared secret S = B^a mod p.
    
    Args:
        B (int): The other party's public value
        a (int): This party's private key
        p (int): The prime modulus
        
    Returns:
        int: The shared secret S
    """
    return mod_exp(B, a, p)


def read_parameters():
    """
    Read the DH parameters p and g from standard input.
    
    Returns:
        tuple: (p, g) where p is the prime and g is the generator
    """
    try:
        p_line = input().strip()
        g_line = input().strip()
        
        p = int(p_line)
        g = int(g_line)
        
        if p <= 1:
            raise ValueError("Prime p must be greater than 1")
        if g <= 1 or g >= p:
            raise ValueError("Generator g must be in range [2, p-1]")
            
        return p, g
        
    except EOFError as exc:
        raise ValueError("Could not read parameters from stdin") from exc
    except ValueError as e:
        if "invalid literal" in str(e):
            raise ValueError("Parameters must be valid integers") from e
        raise


def read_public_value():
    """
    Read the other party's public value B from standard input.
    
    Returns:
        int: The other party's public value B
    """
    try:
        B_line = input().strip()
        B = int(B_line)
        
        if B <= 0:
            raise ValueError("Public value B must be positive")
            
        return B
        
    except EOFError as exc:
        raise ValueError("Could not read public value from stdin") from exc
    except ValueError as e:
        if "invalid literal" in str(e):
            raise ValueError("Public value must be a valid integer") from e
        raise


def main():
    """
    Main function that orchestrates the Diffie-Hellman key exchange.
    """
    try:
        # Step 1: Read the prime p and generator g from stdin
        p, g = read_parameters()
        
        # Step 2: Generate private key and compute public value
        a = generate_private_key(p)
        A = compute_public_value(g, a, p)
        
        # Step 3: Output our public value A to stdout
        print(A)
        sys.stdout.flush()  # Ensure immediate output for piping
        
        # Step 4: Read the other party's public value B from stdin
        B = read_public_value()
        
        # Step 5: Compute the shared secret S = B^a mod p
        S = compute_shared_secret(B, a, p)
        
        # Step 6: Output the shared secret S to stdout
        print(S)
        
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
