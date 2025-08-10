#!/usr/bin/env python3
"""
DSA Verification Program
Usage: python dsa_verify.py [key_file] [message_file]

Verifies a DSA signature for a message using the public key from key_file.
The message is read from message_file as a string.
The signature (r, s) values are prompted from user input.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dsa.dsa_core import read_key_file, read_message_file, dsa_verify


def main():
    if len(sys.argv) != 3:
        print("Usage: python dsa_verify.py [key_file] [message_file]")
        sys.exit(1)
    
    key_file = sys.argv[1]
    message_file = sys.argv[2]
    
    try:
        # Read public key file
        p, q, g, y = read_key_file(key_file)
        print(f"Loaded public key from: {key_file}")
        
        # Read message
        message = read_message_file(message_file)
        print(f"Loaded message from: {message_file}")
        
        # Get signature from user
        print("\nPlease enter the signature values:")
        try:
            r = int(input("r = "))
            s = int(input("s = "))
        except ValueError:
            print("Error: Invalid signature values. Please enter integers.")
            sys.exit(1)
        
        # Verify the signature
        print("Verifying signature...")
        is_valid = dsa_verify(message, r, s, p, q, g, y)
        
        if is_valid:
            print("✓ Signature is VALID")
        else:
            print("✗ Signature is INVALID")
        
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: Invalid file format - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
