import argparse

def read_file(path: str) -> str:
    with open(path, mode="r", encoding="utf-8") as file:
        return file.read()

def write_file(path: str, content: str) -> None:
    with open(path, mode="w", encoding="utf-8") as file:
        file.write(content)


def cipher(text: str, key: int) -> str:
    encrypted_chars = []

    for char in text:
        print(f"Processing character: {char}")


def decipher(text: str, key: int) -> str:
    ...


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Additive cipher",
        epilog="Example usage: python additive_cipher.py input.txt -k 10 output.txt"
    )

    parser.add_argument("-i", "--input", type=str, required=True, help="Path to the input text file to be processed")
    parser.add_argument("-k", "--key", type=int, required=True, help="Key for the cipher (0-25)")
    parser.add_argument("-o", "--output", type=str, required=True, help="Path to the output file")
    
    args = parser.parse_args()

    print(f"Input file: {args.input}")
    print(f"Key: {args.key}")
    print(f"Output file: {args.output}")

