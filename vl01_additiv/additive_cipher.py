import argparse

def read_file(path: str) -> str:
    with open(path, mode="r", encoding="utf-8") as file:
        return file.read()

def write_file(path: str, content: str) -> None:
    with open(path, mode="w", encoding="utf-8") as file:
        file.write(content)


def cipher(text: str, key: int) -> str:
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
        description="Additive cipher",
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