import argparse

def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def cipher(text: str, key: int) -> str:
    ...

def decipher(text: str, key: int) -> str:
    ...


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Additive cipher")
    
    parser.add_argument("input_file", type=str, help="Path to the input text file to be processed")
    parser.add_argument("key", type=int, choices=range(0, 26), help="Key for the cipher (0-25)")
    parser.add_argument("output_file", type=str, help="Path to the output file")
    
    args = parser.parse_args()
    
    # Read input text
    input_text = read_file(args.input_file)
    
    # Apply cipher
    encrypted_text = cipher(input_text, args.key)
    
    # Write output
    with open(args.output_file, "w", encoding="utf-8") as output_file:
        output_file.write(encrypted_text)

