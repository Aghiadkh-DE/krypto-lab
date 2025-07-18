"""
Additive Cipher Module

This module implements an additive cipher (also known as Caesar cipher) for encrypting
and decrypting text. The cipher shifts each letter in the alphabet by a fixed number
of positions (the key).

The module supports:
- Encryption and decryption of uppercase letters (A-Z)
- Non-alphabetic characters are preserved unchanged
- Command-line interface for file-based operations
- Key validation (0-25)

Author: Aghiad Khertabeel
Date: July 2025
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from util.file_util import read_file, write_file


def cipher(text: str, key: int) -> str:
    """
    Encrypt text using an additive cipher (Caesar cipher).
    
    Each uppercase letter (A-Z) is shifted forward in the alphabet by the key value.
    Non-alphabetic characters and characters outside A-Z are left unchanged.
    
    Args:
        text (str): The plaintext to encrypt
        key (int): The shift value (0-25)
        
    Returns:
        str: The encrypted text
        
    Example:
        >>> cipher("HELLO", 3)
        'KHOOR'
    """
    encrypted_chars = []

    base = ord('A')
    for char in text:
        if char.isalpha() and ord('A') <= ord(char) <= ord('Z'):
            encrypted_char = chr((ord(char) - base + key) % 26 + base)
            encrypted_chars.append(encrypted_char)
        else:
            encrypted_chars.append(char)

    return ''.join(encrypted_chars)


def decipher(text: str, key: int) -> str:
    """
    Decrypt text using an additive cipher (Caesar cipher).
    
    Each uppercase letter (A-Z) is shifted backward in the alphabet by the key value.
    Non-alphabetic characters and characters outside A-Z are left unchanged.
    
    Args:
        text (str): The ciphertext to decrypt
        key (int): The shift value (0-25)
        
    Returns:
        str: The decrypted text
        
    Example:
        >>> decipher("KHOOR", 3)
        'HELLO'
    """
    decrypted_chars = []

    base = ord('A')
    for char in text:
        if char.isalpha() and ord('A') <= ord(char) <= ord('Z'):
            decrypted_char = chr((ord(char) - base - key) % 26 + base)
            decrypted_chars.append(decrypted_char)
        else:
            decrypted_chars.append(char)

    return ''.join(decrypted_chars)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Additive cipher - Encrypt or decrypt text using Caesar cipher",
        epilog="Example: python additive_cipher.py -i plaintext.txt -k 7 -o ciphertext.txt -e"
    )

    parser.add_argument("-i", "--input", type=str, required=True, help="Path to the input text file to be processed")
    parser.add_argument("-k", "--key", type=int, required=True, help="Key for the cipher (0-25)")
    parser.add_argument("-o", "--output", type=str, required=True, help="Path to the output file")
    parser.add_argument("-d", "--decrypt", action="store_true", help="Decrypt the input text")
    parser.add_argument("-e", "--encrypt", action="store_true", help="Encrypt the input text (default)")

    args = parser.parse_args()
    if args.key < 0 or args.key > 25:
        raise ValueError("Key must be between 0 and 25")

    if not args.encrypt and not args.decrypt:
        args.encrypt = True
    if args.decrypt and args.encrypt:
        raise ValueError("Cannot specify both encrypt and decrypt options")

    if args.decrypt:
        operation = decipher
    else:
        operation = cipher

    input_text = read_file(args.input)
    output_text = operation(input_text, args.key)
    write_file(args.output, output_text)