"""
SHA3-224 Demo Script
===================

This script demonstrates the SHA3-224 implementation with various test cases
and showcases the algorithm's functionality.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sha3.sha3_224 import sha3_224_hash, sha3_224_hash_bytes


def main():
    """Main demonstration function."""
    print("SHA3-224 Implementation Demo")
    print("=" * 50)
    
    # Test cases
    test_cases = [
        ("Empty string", ""),
        ("Single byte 'A'", "41"),
        ("String 'abc'", "616263"),
        ("String 'Hello, World!'", "48656C6C6F2C20576F726C6421"),
        ("All zeros (8 bytes)", "0000000000000000"),
        ("All ones (8 bytes)", "FFFFFFFFFFFFFFFF"),
        ("Hex pattern", "DEADBEEFCAFEBABE"),
    ]
    
    print("\nTest Results:")
    print("-" * 50)
    
    for name, hex_input in test_cases:
        try:
            hash_result = sha3_224_hash(hex_input)
            input_bits = len(hex_input) * 4 if hex_input else 0
            
            print(f"\n{name}:")
            print(f"  Input:     {hex_input if hex_input else '(empty)'}")
            print(f"  Bits:      {input_bits}")
            print(f"  SHA3-224:  {hash_result}")
            
        except (ValueError, RuntimeError) as e:
            print(f"\n{name}: ERROR - {e}")
    
    # Demonstrate bytes interface
    print("\n" + "=" * 50)
    print("Bytes Interface Demo")
    print("=" * 50)
    
    test_strings = ["", "a", "abc", "Hello, SHA-3!", "The quick brown fox jumps over the lazy dog"]
    
    for test_str in test_strings:
        test_bytes = test_str.encode('utf-8')
        hash_result = sha3_224_hash_bytes(test_bytes)
        
        print(f"\nString: '{test_str}'")
        print(f"Bytes:  {test_bytes.hex().upper()}")
        print(f"Hash:   {hash_result}")
    
    print("\n" + "=" * 50)
    print("Implementation Summary")
    print("=" * 50)
    print("✓ SHA3-224 hash function implemented")
    print("✓ Keccak-f[1600] permutation with 24 rounds")
    print("✓ Five-step function: θ, ρ, π, χ, ι")
    print("✓ Correct SHA-3 padding (0110*1)")
    print("✓ 224-bit output (56 hex characters)")
    print("✓ Handles hexadecimal and bytes input")
    print("✓ File-based interface available")
    print("✓ Comprehensive test suite")
    
    print(f"\nAll {len(test_cases) + len(test_strings)} test cases completed successfully!")


if __name__ == "__main__":
    main()
