import sys


def square_and_multiply(base, exponent, modulus):
    if modulus == 1:
        return 0
    
    result = 1
    base = base % modulus
    
    while exponent > 0:
        # If exponent is odd (current bit is 1)
        if exponent % 2 == 1:
            result = (result * base) % modulus
        
        # Square the base for the next iteration
        base = (base * base) % modulus
        
        # Move to the next bit (divide exponent by 2)
        exponent = exponent >> 1
    
    return result


def read_input_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            return int(content)
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Input file not found: {file_path}") from exc
    except ValueError as exc:
        raise ValueError(f"Invalid integer in input file: {file_path}") from exc


def read_key_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.read().strip().split('\n')
            if len(lines) != 2:
                raise ValueError("Key file must contain exactly two lines")
            
            exponent = int(lines[0].strip())
            modulus = int(lines[1].strip())
            
            return exponent, modulus
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Key file not found: {file_path}") from exc
    except ValueError as e:
        raise ValueError(f"Invalid key file format: {e}") from e


def write_output_file(file_path, result):
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(result))
    except IOError as e:
        raise IOError(f"Error writing to output file {file_path}: {e}") from e


def rsa_operation(message, exponent, modulus):
    """
    Performs the RSA operation: message^exponent mod modulus.
    
    Args:
        message (int): The input message
        exponent (int): The exponent (e for encryption, d for decryption)
        modulus (int): The modulus n
        
    Returns:
        int: The result of the RSA operation
    """
    return square_and_multiply(message, exponent, modulus)


def main():
    """
    Main function that handles command line arguments and orchestrates the RSA operation.
    """
    # Check command line arguments
    if len(sys.argv) != 4:
        print("Usage: python rsa.py <input_file> <key_file> <output_file>")
        print("\nDescription:")
        print("  input_file:  File containing a single decimal number (message)")
        print("  key_file:    File with two lines - exponent and modulus in decimal")
        print("  output_file: File where the result will be written")
        sys.exit(1)
    
    input_file = sys.argv[1]
    key_file = sys.argv[2]
    output_file = sys.argv[3]
    
    try:
        # Read input message
        message = read_input_file(input_file)
        print(f"Read message: {message}")
        
        # Read key (exponent and modulus)
        exponent, modulus = read_key_file(key_file)
        print(f"Read exponent: {exponent}")
        print(f"Read modulus: {modulus}")
        
        # Perform RSA operation using Square and Multiply
        print("Performing RSA operation using Square and Multiply method...")
        result = rsa_operation(message, exponent, modulus)
        print(f"Result: {result}")
        
        # Write result to output file
        write_output_file(output_file, result)
        print(f"Result written to: {output_file}")
        
    except (FileNotFoundError, ValueError, IOError) as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
