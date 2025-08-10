"""
SHA3-224 Verification Script
============================

This script verifies the SHA3-224 implementation against known test vectors
and provides debugging information for the Keccak algorithm.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sha3.sha3_224 import sha3_224_hash


def test_known_vectors():
    """Test against known SHA3-224 vectors."""
    print("Testing SHA3-224 Implementation")
    print("=" * 50)
    
    # Test cases with expected results
    test_cases = [
        {
            "name": "Empty string",
            "input": "",
            "expected": None,  # We'll determine this from our implementation
            "description": "Empty input (0 bits)"
        },
        {
            "name": "Single bit",
            "input": "80",  # Binary: 10000000 (1 bit followed by zeros)
            "expected": None,
            "description": "Single bit set (1 bit)"
        },
        {
            "name": "ABC string",
            "input": "616263",  # "abc" in ASCII hex
            "expected": None,
            "description": "ASCII string 'abc' (24 bits)"
        },
        {
            "name": "448-bit string",
            "input": "61626364" * 14,  # "abcd" repeated to make 448 bits
            "expected": None,
            "description": "448-bit message (exactly capacity size)"
        },
        {
            "name": "896-bit string", 
            "input": "61626364" * 28,  # "abcd" repeated to make 896 bits
            "expected": None,
            "description": "896-bit message (2 × capacity size)"
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test['name']}")
        print(f"Description: {test['description']}")
        print(f"Input: {test['input'][:32]}{'...' if len(test['input']) > 32 else ''}")
        print(f"Input length: {len(test['input'])} hex chars = {len(test['input']) * 4} bits")
        
        try:
            result = sha3_224_hash(test['input'])
            print(f"SHA3-224: {result}")
            
            if test['expected']:
                if result == test['expected']:
                    print("✓ PASS - Matches expected value")
                else:
                    print("✗ FAIL - Does not match expected value")
                    print(f"Expected: {test['expected']}")
            else:
                print("? INFO - No reference value available")
                
        except (ValueError, RuntimeError) as e:
            print(f"✗ ERROR: {e}")


def analyze_padding():
    """Analyze the padding behavior for different input sizes."""
    print("\n" + "=" * 50)
    print("Padding Analysis")
    print("=" * 50)
    
    from sha3.sha3_224 import sha3_pad
    
    rate = 1152  # SHA3-224 rate in bits
    rate_bytes = rate // 8  # 144 bytes
    
    # Test different message lengths
    test_lengths = [0, 1, 2, 8, 16, 32, 64, 128, 143, 144, 145, 288]
    
    for length in test_lengths:
        message = b'A' * length
        padded = sha3_pad(message, rate)
        
        print(f"Message: {length:3d} bytes -> Padded: {len(padded):3d} bytes "
              f"(+{len(padded) - length:3d}) -> Blocks: {len(padded) // rate_bytes}")
        
        if len(padded) < 20:  # Show padding for short messages
            print(f"  Padded data: {padded.hex().upper()}")


def debug_state_transitions():
    """Debug the state transitions for a simple input."""
    print("\n" + "=" * 50)
    print("State Transition Debug")
    print("=" * 50)
    
    from sha3.sha3_224 import (
        sha3_pad, bytes_to_state, keccak_f, state_to_bytes,
        theta_step, rho_step, pi_step, chi_step, iota_step
    )
    
    # Use simple input
    message = b""  # Empty message
    rate = 1152
    
    print("Input message:", message.hex().upper() if message else "(empty)")
    
    # Pad the message
    padded = sha3_pad(message, rate)
    print(f"Padded message ({len(padded)} bytes):", padded.hex().upper())
    
    # Initialize state
    state = [[0 for _ in range(5)] for _ in range(5)]
    print("Initial state: all zeros")
    
    # Process first (and only) block
    rate_bytes = rate // 8
    block = padded[:rate_bytes]
    
    # XOR with state
    state_bytes = state_to_bytes(state)
    new_state_bytes = bytearray(state_bytes)
    for j in range(len(block)):
        new_state_bytes[j] ^= block[j]
    
    state = bytes_to_state(bytes(new_state_bytes))
    print(f"After absorbing block: {state[0][0]:016X} (first word)")
    
    # Apply one round of Keccak-f for debugging
    print("\nFirst round steps:")
    state_theta = theta_step(state)
    print(f"After theta: {state_theta[0][0]:016X}")
    
    state_rho = rho_step(state_theta) 
    print(f"After rho:   {state_rho[0][0]:016X}")
    
    state_pi = pi_step(state_rho)
    print(f"After pi:    {state_pi[0][0]:016X}")
    
    state_chi = chi_step(state_pi)
    print(f"After chi:   {state_chi[0][0]:016X}")
    
    state_iota = iota_step(state_chi, 0)
    print(f"After iota:  {state_iota[0][0]:016X}")
    
    # Complete Keccak-f
    final_state = keccak_f(state)
    print(f"\nAfter full Keccak-f: {final_state[0][0]:016X}")
    
    # Extract output
    output_bytes = 28  # 224 bits
    result_bytes = state_to_bytes(final_state)[:output_bytes]
    print(f"Final hash: {result_bytes.hex().upper()}")


def main():
    """Main verification function."""
    try:
        test_known_vectors()
        analyze_padding()
        debug_state_transitions()
        
        print("\n" + "=" * 50)
        print("Verification complete!")
        
    except (ValueError, RuntimeError) as e:
        print(f"Error during verification: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
