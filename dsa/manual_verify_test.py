#!/usr/bin/env python3
"""
Manual DSA Verification Test
This script demonstrates the verification program by providing sample signature values.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dsa.dsa_core import read_key_file, read_message_file, dsa_verify

def main():
    # Read public key and message
    p, q, g, y = read_key_file('test_public.key')
    message = read_message_file('test_message.txt')
    
    print("DSA Verification Example")
    print("========================")
    print(f"Message: {message}")
    print(f"Public key loaded from: test_public.key")
    print()
    
    # Test with known good signature (generated from signing)
    print("Test 1: Valid signature")
    r = 13296216272177932449805685288345330332763423366
    s = 673435344691044881606974868105501898606995561091
    
    print(f"r = {r}")
    print(f"s = {s}")
    
    is_valid = dsa_verify(message, r, s, p, q, g, y)
    print(f"Result: {'VALID' if is_valid else 'INVALID'}")
    print()
    
    # Test with invalid signature
    print("Test 2: Invalid signature")
    r_bad = 12345
    s_bad = 67890
    
    print(f"r = {r_bad}")
    print(f"s = {s_bad}")
    
    is_valid = dsa_verify(message, r_bad, s_bad, p, q, g, y)
    print(f"Result: {'VALID' if is_valid else 'INVALID'}")

if __name__ == "__main__":
    main()
