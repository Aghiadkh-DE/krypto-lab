import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List
from util.file_util import read_file


def load_sbox(filename: str) -> List[List[int]]:
    """Load S-Box from file and convert to 16x16 matrix"""
    try:
        content = read_file(filename)
        hex_values = content.replace('\n', ' ').split()
        sbox = []
        for i in range(16):
            row = []
            for j in range(16):
                row.append(int(hex_values[i * 16 + j], 16))
            sbox.append(row)
        return sbox
    except (FileNotFoundError, IOError, ValueError, IndexError) as e:
        print(f"Error loading S-Box from {filename}: {e}")
        return []


def get_sboxes() -> tuple[List[List[int]], List[List[int]]]:
    s_box = load_sbox("SBox.txt")
    inv_s_box = load_sbox("SBoxInvers.txt")
    return s_box, inv_s_box


def parse_hex_string(hex_str: str) -> bytes:
    """Parse hex string from file (ignore spaces and newlines)"""
    hex_str = hex_str.replace(' ', '').replace('\n', '').replace('\r', '')
    return bytes.fromhex(hex_str)


def bytes_to_state(data: bytes) -> List[List[int]]:
    """Convert 16 bytes to 4x4 state matrix (column-major order)"""
    if len(data) != 16:
        raise ValueError("Data must be exactly 16 bytes")
    state = [[0 for _ in range(4)] for _ in range(4)]
    for i in range(16):
        state[i % 4][i // 4] = data[i]
    return state


def state_to_bytes(state: List[List[int]]) -> bytes:
    """Convert 4x4 state matrix to 16 bytes (column-major order)"""
    result = []
    for col in range(4):
        for row in range(4):
            result.append(state[row][col])
    return bytes(result)


def sub_bytes(state: List[List[int]], s_box: List[List[int]]) -> List[List[int]]:
    """Apply S-Box substitution to each byte in the state"""
    for i in range(4):
        for j in range(4):
            byte = state[i][j]
            state[i][j] = s_box[byte >> 4][byte & 0x0F]
    return state


def inv_sub_bytes(state: List[List[int]], inv_s_box: List[List[int]]) -> List[List[int]]:
    """Apply inverse S-Box substitution to each byte in the state"""
    for i in range(4):
        for j in range(4):
            byte = state[i][j]
            state[i][j] = inv_s_box[byte >> 4][byte & 0x0F]
    return state


def shift_rows(state: List[List[int]]) -> List[List[int]]:
    """Shift rows of the state matrix"""
    # Row 0: no shift
    # Row 1: shift left by 1
    state[1] = state[1][1:] + state[1][:1]
    # Row 2: shift left by 2
    state[2] = state[2][2:] + state[2][:2]
    # Row 3: shift left by 3
    state[3] = state[3][3:] + state[3][:3]
    return state


def inv_shift_rows(state: List[List[int]]) -> List[List[int]]:
    """Inverse shift rows of the state matrix"""
    # Row 0: no shift
    # Row 1: shift right by 1
    state[1] = state[1][-1:] + state[1][:-1]
    # Row 2: shift right by 2
    state[2] = state[2][-2:] + state[2][:-2]
    # Row 3: shift right by 3
    state[3] = state[3][-3:] + state[3][:-3]
    return state


def gf_multiply(a: int, b: int) -> int:
    """Multiply two numbers in GF(2^8)"""
    result = 0
    for _ in range(8):
        if b & 1:
            result ^= a
        high_bit = a & 0x80
        a <<= 1
        if high_bit:
            a ^= 0x1B  # AES irreducible polynomial
        b >>= 1
    return result & 0xFF


def mix_columns(state: List[List[int]]) -> List[List[int]]:
    """Mix columns using matrix multiplication in GF(2^8)"""
    for col in range(4):
        temp = [state[row][col] for row in range(4)]
        state[0][col] = (gf_multiply(2, temp[0]) ^ 
                       gf_multiply(3, temp[1]) ^ 
                       temp[2] ^ temp[3])
        state[1][col] = (temp[0] ^ 
                       gf_multiply(2, temp[1]) ^ 
                       gf_multiply(3, temp[2]) ^ 
                       temp[3])
        state[2][col] = (temp[0] ^ temp[1] ^ 
                       gf_multiply(2, temp[2]) ^ 
                       gf_multiply(3, temp[3]))
        state[3][col] = (gf_multiply(3, temp[0]) ^ 
                       temp[1] ^ temp[2] ^ 
                       gf_multiply(2, temp[3]))
    return state


def inv_mix_columns(state: List[List[int]]) -> List[List[int]]:
    """Inverse mix columns using matrix multiplication in GF(2^8)"""
    for col in range(4):
        temp = [state[row][col] for row in range(4)]
        state[0][col] = (gf_multiply(0x0E, temp[0]) ^ 
                       gf_multiply(0x0B, temp[1]) ^ 
                       gf_multiply(0x0D, temp[2]) ^ 
                       gf_multiply(0x09, temp[3]))
        state[1][col] = (gf_multiply(0x09, temp[0]) ^ 
                       gf_multiply(0x0E, temp[1]) ^ 
                       gf_multiply(0x0B, temp[2]) ^ 
                       gf_multiply(0x0D, temp[3]))
        state[2][col] = (gf_multiply(0x0D, temp[0]) ^ 
                       gf_multiply(0x09, temp[1]) ^ 
                       gf_multiply(0x0E, temp[2]) ^ 
                       gf_multiply(0x0B, temp[3]))
        state[3][col] = (gf_multiply(0x0B, temp[0]) ^ 
                       gf_multiply(0x0D, temp[1]) ^ 
                       gf_multiply(0x09, temp[2]) ^ 
                       gf_multiply(0x0E, temp[3]))
    return state


def add_round_key(state: List[List[int]], round_key: bytes) -> List[List[int]]:
    """XOR state with round key"""
    key_state = bytes_to_state(round_key)
    for i in range(4):
        for j in range(4):
            state[i][j] ^= key_state[i][j]
    return state


def encrypt_block(plaintext: bytes, round_keys: List[bytes]) -> bytes:
    """
    Encrypt a 128-bit block using AES
    
    Args:
        plaintext: 16 bytes of plaintext
        round_keys: 11 round keys (each 16 bytes)
        
    Returns:
        16 bytes of ciphertext
    """
    if len(plaintext) != 16:
        raise ValueError("Plaintext must be exactly 16 bytes")
    if len(round_keys) != 11:
        raise ValueError("Must provide exactly 11 round keys")

    s_box, _ = get_sboxes()
    state = bytes_to_state(plaintext)
    state = add_round_key(state, round_keys[0])

    for round_num in range(1, 10):
        state = sub_bytes(state, s_box)
        state = shift_rows(state)
        state = mix_columns(state)
        state = add_round_key(state, round_keys[round_num])

    state = sub_bytes(state, s_box)
    state = shift_rows(state)
    state = add_round_key(state, round_keys[10])

    return state_to_bytes(state)


def decrypt_block(ciphertext: bytes, round_keys: List[bytes]) -> bytes:
    """
    Decrypt a 128-bit block using AES
    
    Args:
        ciphertext: 16 bytes of ciphertext
        round_keys: 11 round keys (each 16 bytes)
        
    Returns:
        16 bytes of plaintext
    """
    if len(ciphertext) != 16:
        raise ValueError("Ciphertext must be exactly 16 bytes")
    if len(round_keys) != 11:
        raise ValueError("Must provide exactly 11 round keys")

    _, inv_s_box = get_sboxes()

    state = bytes_to_state(ciphertext)

    state = add_round_key(state, round_keys[10])

    for round_num in range(9, 0, -1):
        state = inv_shift_rows(state)
        state = inv_sub_bytes(state, inv_s_box)
        state = add_round_key(state, round_keys[round_num])
        state = inv_mix_columns(state)

    state = inv_shift_rows(state)
    state = inv_sub_bytes(state, inv_s_box)
    state = add_round_key(state, round_keys[0])
    
    return state_to_bytes(state)


def load_round_keys_from_file(filename: str) -> List[bytes]:
    """Load 11 round keys from a file"""
    try:
        content = read_file(filename)
        lines = content.strip().split('\n')
        round_keys = []
        
        for line in lines:
            key_bytes = parse_hex_string(line)
            if len(key_bytes) == 16:
                round_keys.append(key_bytes)
        
        if len(round_keys) != 11:
            raise ValueError(f"Expected 11 round keys, got {len(round_keys)}")
        
        return round_keys
    except (FileNotFoundError, IOError, ValueError) as e:
        print(f"Error loading round keys from {filename}: {e}")
        return []


def load_text_from_file(filename: str) -> bytes:
    """Load 128-bit text from a file"""
    try:
        content = read_file(filename)
        text_bytes = parse_hex_string(content)
        
        if len(text_bytes) != 16:
            raise ValueError(f"Expected 16 bytes (128 bits), got {len(text_bytes)}")
        
        return text_bytes
    except (FileNotFoundError, IOError, ValueError) as e:
        print(f"Error loading text from {filename}: {e}")
        return b''


def bytes_to_hex_string(data: bytes, format_output: bool = True) -> str:
    """Convert bytes to hex string"""
    hex_str = ' '.join(f'{byte:02x}' for byte in data)
    if format_output:
        # Format as 4x4 matrix for better readability
        words = hex_str.split()
        result = ""
        for i in range(0, 16, 4):
            result += ' '.join(words[i:i+4]) + '\n'
        return result.strip()
    return hex_str


# Wrapper functions for compatibility with operation modes
def aes_encrypt_wrapper(block: bytes, key: bytes) -> bytes:
    """
    Wrapper function for AES encryption compatible with operation modes
    Note: This implementation uses pre-generated round keys from file
    The 'key' parameter is ignored for this educational implementation
    
    Args:
        block: 16 bytes of plaintext
        key: Ignored - we use round keys from file
        
    Returns:
        16 bytes of ciphertext
    """
    _ = key  # Acknowledge unused parameter
    # Load round keys from file (this is a simplification)
    round_keys = load_round_keys_from_file("Beispiel_key.txt")
    if not round_keys:
        raise ValueError("Failed to load round keys")
    return encrypt_block(block, round_keys)


def aes_decrypt_wrapper(block: bytes, key: bytes) -> bytes:
    """
    Wrapper function for AES decryption compatible with operation modes
    Note: This implementation uses pre-generated round keys from file
    The 'key' parameter is ignored for this educational implementation
    
    Args:
        block: 16 bytes of ciphertext
        key: Ignored - we use round keys from file
        
    Returns:
        16 bytes of plaintext
    """
    _ = key  # Acknowledge unused parameter
    # Load round keys from file (this is a simplification)
    round_keys = load_round_keys_from_file("Beispiel_key.txt")
    if not round_keys:
        raise ValueError("Failed to load round keys")
    return decrypt_block(block, round_keys)

if __name__ == "__main__":
    try:
        plaintext = load_text_from_file("Beispiel_1_Klartext.txt")
        if not plaintext:
            raise ValueError("Failed to load plaintext")
        print(f"Plaintext from file: \n{bytes_to_hex_string(plaintext)}")

        expected_ciphertext = load_text_from_file("Beispiel_1_Kryptotext.txt")
        if not expected_ciphertext:
            raise ValueError("Failed to load expected ciphertext")

        round_keys = load_round_keys_from_file("Beispiel_key.txt")
        if not round_keys:
            raise ValueError("Failed to load round keys")
        print(f"Loaded {len(round_keys)} round keys from file")

        ciphertext = encrypt_block(plaintext, round_keys)
        print(f"\nCiphertext: \n{bytes_to_hex_string(ciphertext)}")
        if ciphertext != expected_ciphertext:
            print("Ciphertext does not match expected value!")
        else:
            print("Ciphertext matches expected value.")

        decrypted = decrypt_block(ciphertext, round_keys)
        print(f"\nDecrypted: \n{bytes_to_hex_string(decrypted)}")

    except (FileNotFoundError, IOError, ValueError) as e:
        print(f"Error with file example: {e}")
