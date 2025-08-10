#!/usr/bin/env python3
"""
DSA Signing Program
Usage: python dsa_sign.py [key_file] [message_file]

Signs a message using the private key from key_file.
The message is read from message_file as a string.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dsa.dsa_core import read_key_file, read_message_file, dsa_sign


def main():
    if len(sys.argv) != 3:
        print("Usage: python dsa_sign.py [key_file] [message_file]")
        sys.exit(1)
    
    key_file = sys.argv[1]
    message_file = sys.argv[2]
    
    try:
        # Read private key file
        p, q, g, x = read_key_file(key_file)
        print(f"Loaded private key from: {key_file}")
        
        # Read message
        message = read_message_file(message_file)
        print(f"Loaded message from: {message_file}")
        
        # Sign the message
        print("Signing message...")
        r, s = dsa_sign(message, p, q, g, x)
        
        # Output signature
        print(f"Signature (r, s):")
        print(f"r = {r}")
        print(f"s = {s}")
        
        print("Message signed successfully!")
        
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
