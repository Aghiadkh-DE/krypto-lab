import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from util.file_util import read_file, write_file


def encrypt_vigenere(text: str, key: str) -> str:
    ciphertext = []
    key_length = len(key)

    base, i = ord('A'), 0
    for c in text:
        if c.isalpha() and ord('A') <= ord(c) <= ord('Z'):
            shift = ord(key[i % key_length].upper()) - base
            encrypted_char = chr((ord(c.upper()) - base + shift) % 26 + base)
            ciphertext.append(encrypted_char)
            i += 1
        else:
            ciphertext.append(c)

    return ''.join(ciphertext)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Vigenere Cipher - Encrypt text using Vigenere cipher",
        epilog="Example: python vigenere_cipher.py -i plaintext.txt -k key.txt -o ciphertext.txt"
    )

    parser.add_argument('-i', '--input', type=str, required=True, help='Input plaintext file')
    parser.add_argument('-k', '--key', type=str, required=True, help='Key String for Vigenere cipher')
    parser.add_argument('-o', '--output', type=str, required=True, help='Output ciphertext file')

    args = parser.parse_args()

    if not args.key:
        print("Error: Key file is required.")
        exit(1)

    for char in args.key:
        if ord(char) < ord('A') or ord(char) > ord('Z'):
            print(f"Error: Key must only contain uppercase letters A-Z, found '{char}'")
            exit(1)

    try:
        plaintext = read_file(args.input)
        crypt_text = encrypt_vigenere(plaintext, args.key)
        write_file(args.output, crypt_text)

    except FileNotFoundError:
        print(f"Error: Input file '{args.input}' not found.")
        exit(1)
    except (IOError, OSError) as e:
        print(f"File I/O error: {e}")
        exit(1)