"""
SHA3-224 Implementation
======================

Implementation of the SHA3-224 hash function with Keccak-f[1600] permutation.

Parameters for SHA3-224:
- Hash size (d): 224 bits
- Block size (rate r): 1152 bits = 144 bytes
- Capacity (c): 448 bits = 56 bytes
- Block width (b = c + r): 1600 bits = 200 bytes

The Keccak state is represented as a 5×5 array of 64-bit words (lanes).
"""

import sys
from typing import List


# Rotation offsets for the ρ (rho) step
RHO_OFFSETS = [
    0, 1, 62, 28, 27,
    36, 44, 6, 55, 20,
    3, 10, 43, 25, 39,
    41, 45, 15, 21, 8,
    18, 2, 61, 56, 14
]

# Round constants for the ι (iota) step (24 rounds)
ROUND_CONSTANTS = [
    0x0000000000000001,
    0x0000000000008082,
    0x800000000000808A,
    0x8000000080008000,
    0x000000000000808B,
    0x0000000080000001,
    0x8000000080008081,
    0x8000000000008009,
    0x000000000000008A,
    0x0000000000000088,
    0x0000000080008009,
    0x000000008000000A,
    0x000000008000808B,
    0x800000000000008B,
    0x8000000000008089,
    0x8000000000008003,
    0x8000000000008002,
    0x8000000000000080,
    0x000000000000800A,
    0x800000008000000A,
    0x8000000080008081,
    0x8000000000008080,
    0x0000000080000001,
    0x8000000080008008
]


def bytes_to_state(data: bytes) -> List[List[int]]:
    """
    Convert 200 bytes to a 5×5 state matrix of 64-bit words.
    
    Args:
        data: 200 bytes of input data
        
    Returns:
        5×5 list of 64-bit integers representing the Keccak state
    """
    if len(data) != 200:
        raise ValueError("Data must be exactly 200 bytes for Keccak state")
    
    state = [[0 for _ in range(5)] for _ in range(5)]
    
    for i in range(5):
        for j in range(5):
            offset = 8 * (5 * i + j)
            # Convert 8 bytes to 64-bit word (little-endian)
            word = int.from_bytes(data[offset:offset+8], byteorder='little')
            state[i][j] = word
    
    return state


def state_to_bytes(state: List[List[int]]) -> bytes:
    """
    Convert a 5×5 state matrix to 200 bytes.
    
    Args:
        state: 5×5 list of 64-bit integers
        
    Returns:
        200 bytes representing the state
    """
    data = bytearray(200)
    
    for i in range(5):
        for j in range(5):
            offset = 8 * (5 * i + j)
            word = state[i][j] & 0xFFFFFFFFFFFFFFFF  # Ensure 64-bit
            word_bytes = word.to_bytes(8, byteorder='little')
            data[offset:offset+8] = word_bytes
    
    return bytes(data)


def theta_step(state: List[List[int]]) -> List[List[int]]:
    """
    θ (theta) step: Column parity calculations.
    
    For each column, compute the XOR of all elements, then XOR each element
    with the parities of the adjacent columns (with rotation).
    
    Args:
        state: 5×5 state matrix
        
    Returns:
        Modified state after theta step
    """
    # Compute column parities
    C = [0] * 5
    for x in range(5):
        C[x] = state[x][0] ^ state[x][1] ^ state[x][2] ^ state[x][3] ^ state[x][4]
    
    # Compute D values
    D = [0] * 5
    for x in range(5):
        D[x] = C[(x-1) % 5] ^ _rotl64(C[(x+1) % 5], 1)
    
    # Apply theta transformation
    new_state = [[0 for _ in range(5)] for _ in range(5)]
    for x in range(5):
        for y in range(5):
            new_state[x][y] = state[x][y] ^ D[x]
    
    return new_state


def rho_step(state: List[List[int]]) -> List[List[int]]:
    """
    ρ (rho) step: Cyclic rotation of individual lanes.
    
    Each lane is rotated by a different amount according to the rho offsets.
    
    Args:
        state: 5×5 state matrix
        
    Returns:
        Modified state after rho step
    """
    new_state = [[0 for _ in range(5)] for _ in range(5)]
    
    for x in range(5):
        for y in range(5):
            offset_index = 5 * y + x
            rotation = RHO_OFFSETS[offset_index]
            new_state[x][y] = _rotl64(state[x][y], rotation)
    
    return new_state


def pi_step(state: List[List[int]]) -> List[List[int]]:
    """
    π (pi) step: Lane position permutation.
    
    Rearranges the positions of the lanes according to the formula:
    state[x][y] → state[y][(2x + 3y) mod 5]
    
    Args:
        state: 5×5 state matrix
        
    Returns:
        Modified state after pi step
    """
    new_state = [[0 for _ in range(5)] for _ in range(5)]
    
    for x in range(5):
        for y in range(5):
            new_x = y
            new_y = (2 * x + 3 * y) % 5
            new_state[new_x][new_y] = state[x][y]
    
    return new_state


def chi_step(state: List[List[int]]) -> List[List[int]]:
    """
    χ (chi) step: Nonlinear transformation.
    
    This is the only nonlinear operation in Keccak. For each lane:
    state[x][y] = state[x][y] ⊕ ((~state[(x+1)%5][y]) & state[(x+2)%5][y])
    
    Args:
        state: 5×5 state matrix
        
    Returns:
        Modified state after chi step
    """
    new_state = [[0 for _ in range(5)] for _ in range(5)]
    
    for x in range(5):
        for y in range(5):
            new_state[x][y] = (
                state[x][y] ^ 
                ((~state[(x+1) % 5][y]) & state[(x+2) % 5][y])
            ) & 0xFFFFFFFFFFFFFFFF  # Ensure 64-bit
    
    return new_state


def iota_step(state: List[List[int]], round_index: int) -> List[List[int]]:
    """
    ι (iota) step: Round constant addition.
    
    XORs the round constant with the lane at position [0][0].
    
    Args:
        state: 5×5 state matrix
        round_index: Current round number (0-23)
        
    Returns:
        Modified state after iota step
    """
    new_state = [row[:] for row in state]  # Deep copy
    new_state[0][0] ^= ROUND_CONSTANTS[round_index]
    new_state[0][0] &= 0xFFFFFFFFFFFFFFFF  # Ensure 64-bit
    
    return new_state


def keccak_f(state: List[List[int]]) -> List[List[int]]:
    """
    Keccak-f[1600] permutation function.
    
    Applies 24 rounds of the five-step function (θ, ρ, π, χ, ι).
    
    Args:
        state: 5×5 state matrix
        
    Returns:
        Permuted state after 24 rounds
    """
    current_state = [row[:] for row in state]  # Deep copy
    
    for round_index in range(24):
        current_state = theta_step(current_state)
        current_state = rho_step(current_state)
        current_state = pi_step(current_state)
        current_state = chi_step(current_state)
        current_state = iota_step(current_state, round_index)
    
    return current_state


def sha3_pad(message: bytes, rate: int) -> bytes:
    """
    SHA-3 padding function.
    
    Appends the padding suffix '0110*1' to make the message length
    a multiple of the rate (in bits).
    
    For SHA3-224: rate = 1152 bits = 144 bytes
    
    Args:
        message: Input message bytes
        rate: Rate in bits (1152 for SHA3-224)
        
    Returns:
        Padded message
    """
    rate_bytes = rate // 8  # Convert rate from bits to bytes
    
    # Calculate padding length
    msg_len = len(message)
    pad_len = rate_bytes - (msg_len % rate_bytes)
    
    # SHA-3 suffix is '01' followed by padding '10*1'
    if pad_len == 1:
        # Only one byte needed: combine '01' and '1' -> '011' + padding + '1' = '0110 0001' = 0x61
        padding = b'\x86'  # 0x86 = 10000110 (reversed bit order)
    else:
        # Multiple bytes: '01' + zeros + '1'
        padding = b'\x06'  # 0x06 = 00000110 (reversed bit order)
        padding += b'\x00' * (pad_len - 2)
        padding += b'\x80'  # 0x80 = 10000000 (reversed bit order)
    
    return message + padding


def sha3_224_hash(message: str) -> str:
    """
    Compute SHA3-224 hash of a hexadecimal message string.
    
    Args:
        message: Hexadecimal string (without spaces or prefixes)
        
    Returns:
        SHA3-224 hash as hexadecimal string (56 hex characters)
    """
    # Convert hex string to bytes
    # Remove any whitespace and convert
    hex_str = message.replace(' ', '').replace('\n', '').replace('\t', '')
    if len(hex_str) % 2 != 0:
        raise ValueError("Hexadecimal string must have even length")
    
    try:
        message_bytes = bytes.fromhex(hex_str)
    except ValueError as exc:
        raise ValueError("Invalid hexadecimal string") from exc
    
    return sha3_224_hash_bytes(message_bytes)


def sha3_224_hash_bytes(message_bytes: bytes) -> str:
    """
    Compute SHA3-224 hash of message bytes.
    
    Args:
        message_bytes: Input message as bytes
        
    Returns:
        SHA3-224 hash as hexadecimal string (56 hex characters)
    """
    # SHA3-224 parameters
    rate = 1152  # bits
    output_length = 224  # bits = 28 bytes
    
    # Pad the message
    padded_message = sha3_pad(message_bytes, rate)
    
    # Initialize state (200 bytes = 1600 bits)
    state = [[0 for _ in range(5)] for _ in range(5)]
    
    # Process message blocks
    rate_bytes = rate // 8  # 144 bytes
    for i in range(0, len(padded_message), rate_bytes):
        block = padded_message[i:i + rate_bytes]
        
        # Pad block if necessary (should not be needed due to padding)
        if len(block) < rate_bytes:
            block += b'\x00' * (rate_bytes - len(block))
        
        # XOR block with state (only first rate_bytes of the 200-byte state)
        state_bytes = state_to_bytes(state)
        new_state_bytes = bytearray(state_bytes)
        
        for j in range(rate_bytes):
            new_state_bytes[j] ^= block[j]
        
        # Convert back to state and apply permutation
        state = bytes_to_state(bytes(new_state_bytes))
        state = keccak_f(state)
    
    # Extract output (squeeze phase)
    output_bytes = output_length // 8  # 28 bytes
    result = state_to_bytes(state)[:output_bytes]
    
    return result.hex().upper()


def sha3_224_file(input_file: str, output_file: str) -> None:
    """
    Compute SHA3-224 hash from input file and write to output file.
    
    Args:
        input_file: Path to input file containing hexadecimal data
        output_file: Path to output file for hash result
    """
    try:
        # Read input file
        with open(input_file, 'r', encoding='utf-8') as f:
            hex_data = f.read().strip()
        
        # Compute hash
        hash_result = sha3_224_hash(hex_data)
        
        # Write output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(hash_result + '\n')
        
        print("SHA3-224 hash computed successfully:")
        print(f"Input: {input_file}")
        print(f"Output: {output_file}")
        print(f"Hash: {hash_result}")
        
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except (IOError, OSError) as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


def _rotl64(value: int, amount: int) -> int:
    """
    Rotate a 64-bit value left by the specified amount.
    
    Args:
        value: 64-bit integer
        amount: Number of positions to rotate left
        
    Returns:
        Rotated 64-bit integer
    """
    value &= 0xFFFFFFFFFFFFFFFF  # Ensure 64-bit
    amount %= 64  # Normalize rotation amount
    return ((value << amount) | (value >> (64 - amount))) & 0xFFFFFFFFFFFFFFFF


def main():
    """
    Command-line interface for SHA3-224 hashing.
    
    Usage: python sha3_224.py <input_file> <output_file>
    """
    if len(sys.argv) != 3:
        print("Usage: python sha3_224.py <input_file> <output_file>")
        print("  input_file: File containing hexadecimal data to hash")
        print("  output_file: File to write the SHA3-224 hash result")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    sha3_224_file(input_file, output_file)


if __name__ == "__main__":
    main()
