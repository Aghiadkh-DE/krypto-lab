"""
SHA-3 (Secure Hash Algorithm 3) Implementation
==============================================

This module implements the SHA3-224 hash function according to FIPS 202 standards.

The implementation includes:
- Keccak-f[1600] permutation function
- Five-step function rounds (θ, ρ, π, χ, ι)
- Padding function for SHA3-224
- Complete SHA3-224 hash algorithm

Usage:
    from sha3.sha3_224 import sha3_224_hash, sha3_224_file
    
    # Hash a message
    hash_value = sha3_224_hash("Hello World")
    
    # Hash from file
    sha3_224_file("input.txt", "output.txt")
"""

__version__ = "1.0.0"
__author__ = "Cryptography Lab"
