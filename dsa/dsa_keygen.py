#!/usr/bin/env python3
"""
DSA Parameter & Key Generation Program
Usage: python dsa_keygen.py [public_key_output] [private_key_output]

Generates DSA parameters and keys, writing two files with exactly four lines each:
Line 1: prime p
Line 2: prime q  
Line 3: group element g
Line 4: the respective key (x for private key file, y for public key file)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dsa.dsa_core import generate_dsa_parameters, generate_dsa_keypair, write_key_file


def main():
    if len(sys.argv) != 3:
        print("Usage: python dsa_keygen.py [public_key_output] [private_key_output]")
        sys.exit(1)
    
    public_key_file = sys.argv[1]
    private_key_file = sys.argv[2]
    
    try:
        # Generate DSA parameters
        print("Generating DSA parameters...")
        p, q, g = generate_dsa_parameters()
        
        # Generate key pair
        print("Generating key pair...")
        x, y = generate_dsa_keypair(p, q, g)
        
        # Write public key file (p, q, g, y)
        write_key_file(public_key_file, p, q, g, y)
        print(f"Public key written to: {public_key_file}")
        
        # Write private key file (p, q, g, x)
        write_key_file(private_key_file, p, q, g, x)
        print(f"Private key written to: {private_key_file}")
        
        print("DSA parameter and key generation completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
