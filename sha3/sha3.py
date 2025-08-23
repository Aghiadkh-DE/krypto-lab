"""
SHA3 (Keccak) Implementation
===========================

This module implements the SHA3 cryptographic hash function based on the Keccak algorithm.
SHA3 uses the sponge construction with the Keccak-f[1600] permutation.

Author: Krypto Lab
Date: 2025
"""

import os


class SHA3:
    """
    SHA3 (Keccak) hash function implementation.
    
    Supports SHA3-224, SHA3-256, SHA3-384, and SHA3-512 variants.
    """
    
    # Keccak round constants (24 rounds)
    ROUND_CONSTANTS = [
        0x0000000000000001, 0x0000000000008082, 0x800000000000808A, 0x8000000080008000,
        0x000000000000808B, 0x0000000080000001, 0x8000000080008081, 0x8000000000008009,
        0x000000000000008A, 0x0000000000000088, 0x0000000080008009, 0x000000008000000A,
        0x000000008000808B, 0x800000000000008B, 0x8000000000008089, 0x8000000000008003,
        0x8000000000008002, 0x8000000000000080, 0x000000000000800A, 0x800000008000000A,
        0x8000000080008081, 0x8000000000008080, 0x0000000080000001, 0x8000000080008008
    ]
    
    # Rotation offsets for the ρ (rho) step
    RHO_OFFSETS = [
        0, 1, 62, 28, 27, 36, 44, 6, 55, 20, 3, 10, 43, 25, 39, 41,
        45, 15, 21, 8, 18, 2, 61, 56, 14
    ]
    
    # Standard SHA3 variants configuration
    SHA3_VARIANTS = {
        224: {'rate': 1152, 'capacity': 448, 'output_length': 224},
        256: {'rate': 1088, 'capacity': 512, 'output_length': 256},
        384: {'rate': 832, 'capacity': 768, 'output_length': 384},
        512: {'rate': 576, 'capacity': 1024, 'output_length': 512}
    }
    
    def __init__(self, variant: int = 256):
        """
        Initialize SHA3 with specified variant.
        
        Args:
            variant: SHA3 variant (224, 256, 384, or 512)
        """
        if variant not in self.SHA3_VARIANTS:
            raise ValueError(f"Unsupported SHA3 variant: {variant}. Supported: {list(self.SHA3_VARIANTS.keys())}")
        
        self.variant = variant
        self.rate = self.SHA3_VARIANTS[variant]['rate']
        self.capacity = self.SHA3_VARIANTS[variant]['capacity']
        self.output_length = self.SHA3_VARIANTS[variant]['output_length']
        
        # State array: 5x5 matrix of 64-bit words
        self.state = [[0 for _ in range(5)] for _ in range(5)]
        
        # Buffer for partial blocks
        self.buffer = bytearray()
        self.finalized = False
    
    def _rotate_left(self, value: int, amount: int) -> int:
        """Rotate a 64-bit value left by specified amount."""
        return ((value << amount) | (value >> (64 - amount))) & 0xFFFFFFFFFFFFFFFF
    
    def _theta(self) -> None:
        """θ (theta) step: Column parity computation and XOR."""
        # Compute column parities
        C = [0] * 5
        for x in range(5):
            C[x] = self.state[x][0] ^ self.state[x][1] ^ self.state[x][2] ^ self.state[x][3] ^ self.state[x][4]
        
        # Compute D values
        D = [0] * 5
        for x in range(5):
            D[x] = C[(x + 4) % 5] ^ self._rotate_left(C[(x + 1) % 5], 1)
        
        # Apply theta transformation
        for x in range(5):
            for y in range(5):
                self.state[x][y] ^= D[x]
    
    def _rho(self) -> None:
        """ρ (rho) step: Bit rotation."""
        for x in range(5):
            for y in range(5):
                offset = self.RHO_OFFSETS[5 * y + x]
                self.state[x][y] = self._rotate_left(self.state[x][y], offset)
    
    def _pi(self) -> None:
        """π (pi) step: Lane permutation."""
        temp_state = [[0 for _ in range(5)] for _ in range(5)]
        for x in range(5):
            for y in range(5):
                temp_state[y][(2 * x + 3 * y) % 5] = self.state[x][y]
        self.state = temp_state
    
    def _chi(self) -> None:
        """χ (chi) step: Non-linear transformation."""
        temp_state = [[0 for _ in range(5)] for _ in range(5)]
        for x in range(5):
            for y in range(5):
                temp_state[x][y] = self.state[x][y] ^ ((~self.state[(x + 1) % 5][y]) & self.state[(x + 2) % 5][y])
        self.state = temp_state
    
    def _iota(self, round_index: int) -> None:
        """ι (iota) step: Add round constant."""
        self.state[0][0] ^= self.ROUND_CONSTANTS[round_index]
    
    def _keccak_f(self) -> None:
        """Keccak-f[1600] permutation: 24 rounds of transformations."""
        for round_index in range(24):
            self._theta()
            self._rho()
            self._pi()
            self._chi()
            self._iota(round_index)
    
    def _absorb_block(self, block: bytes) -> None:
        """Absorb a block of data into the state."""
        # Convert block to 64-bit words and XOR with state
        for i in range(0, len(block), 8):
            if i + 8 <= len(block):
                # Full 8-byte word
                word = int.from_bytes(block[i:i+8], byteorder='little')
                lane_x = (i // 8) % 5
                lane_y = (i // 8) // 5
                self.state[lane_x][lane_y] ^= word
            else:
                # Partial word (should not happen with proper padding)
                partial = block[i:] + b'\x00' * (8 - (len(block) - i))
                word = int.from_bytes(partial, byteorder='little')
                lane_x = (i // 8) % 5
                lane_y = (i // 8) // 5
                self.state[lane_x][lane_y] ^= word
    
    def _squeeze(self, output_length: int) -> bytes:
        """Squeeze output from the state."""
        output = bytearray()
        
        while len(output) < output_length // 8:
            # Extract rate bytes from state
            for y in range(5):
                for x in range(5):
                    if len(output) >= output_length // 8:
                        break
                    word_bytes = self.state[x][y].to_bytes(8, byteorder='little')
                    for byte in word_bytes:
                        if len(output) >= output_length // 8:
                            break
                        output.append(byte)
                if len(output) >= output_length // 8:
                    break
            
            # If we need more output, apply permutation
            if len(output) < output_length // 8:
                self._keccak_f()
        
        return bytes(output[:output_length // 8])
    
    def update(self, data: bytes) -> None:
        """
        Update the hash with new data.
        
        Args:
            data: Input data to hash
        """
        if self.finalized:
            raise ValueError("Cannot update after finalization")
        
        self.buffer.extend(data)
        rate_bytes = self.rate // 8
        
        # Process complete blocks
        while len(self.buffer) >= rate_bytes:
            block = bytes(self.buffer[:rate_bytes])
            self.buffer = self.buffer[rate_bytes:]
            self._absorb_block(block)
            self._keccak_f()
    
    def digest(self) -> bytes:
        """
        Finalize the hash and return the digest.
        
        Returns:
            Hash digest as bytes
        """
        if not self.finalized:
            self._finalize()
        
        return self._squeeze(self.output_length)
    
    def hexdigest(self) -> str:
        """
        Finalize the hash and return the digest as hexadecimal string.
        
        Returns:
            Hash digest as hexadecimal string
        """
        return self.digest().hex()
    
    def _finalize(self) -> None:
        """Apply padding and finalize the hash."""
        if self.finalized:
            return
        
        rate_bytes = self.rate // 8
        
        # SHA3 padding: append 0x06 followed by zeros, then 0x80 at the end
        self.buffer.append(0x06)
        
        # Pad to rate boundary
        while len(self.buffer) % rate_bytes != 0:
            self.buffer.append(0x00)
        
        # Set the last bit
        self.buffer[-1] |= 0x80
        
        # Process the final block
        if len(self.buffer) == rate_bytes:
            block = bytes(self.buffer)
            self._absorb_block(block)
            self._keccak_f()
        
        self.finalized = True
    
    def copy(self) -> 'SHA3':
        """Create a copy of the current hash state."""
        new_hash = SHA3(self.variant)
        new_hash.state = [row[:] for row in self.state]
        new_hash.buffer = self.buffer[:]
        new_hash.finalized = self.finalized
        return new_hash


def sha3_224(data: bytes) -> bytes:
    """Compute SHA3-224 hash of data."""
    hasher = SHA3(224)
    hasher.update(data)
    return hasher.digest()


def sha3_256(data: bytes) -> bytes:
    """Compute SHA3-256 hash of data."""
    hasher = SHA3(256)
    hasher.update(data)
    return hasher.digest()


def sha3_384(data: bytes) -> bytes:
    """Compute SHA3-384 hash of data."""
    hasher = SHA3(384)
    hasher.update(data)
    return hasher.digest()


def sha3_512(data: bytes) -> bytes:
    """Compute SHA3-512 hash of data."""
    hasher = SHA3(512)
    hasher.update(data)
    return hasher.digest()


def hash_file(filepath: str, variant: int = 256) -> str:
    """
    Compute SHA3 hash of a file.
    
    Args:
        filepath: Path to the file to hash
        variant: SHA3 variant (224, 256, 384, or 512)
    
    Returns:
        Hexadecimal hash string
    """
    hasher = SHA3(variant)
    
    try:
        with open(filepath, 'rb') as f:
            while True:
                chunk = f.read(8192)  # Read in 8KB chunks
                if not chunk:
                    break
                hasher.update(chunk)
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"File not found: {filepath}") from exc
    except PermissionError as exc:
        raise PermissionError(f"Permission denied: {filepath}") from exc
    
    return hasher.hexdigest()


def process_hex_file(input_file: str, output_file: str, hash_size: int = 224) -> None:
    """
    Process hexadecimal input file and write SHA3 hash to output file.
    
    Args:
        input_file: Path to input file containing hexadecimal data
        output_file: Path to output file for hash result
        hash_size: SHA3 variant (224, 256, 384, or 512), default is 224
    """
    try:
        # Read hexadecimal data from input file
        with open(input_file, 'r', encoding='utf-8') as f:
            hex_data = f.read().strip()
        
        # Remove any whitespace or newlines
        hex_data = ''.join(hex_data.split())
        
        # Validate hexadecimal input
        if not all(c in '0123456789ABCDEFabcdef' for c in hex_data):
            raise ValueError("Input file contains non-hexadecimal characters")
        
        # Convert hexadecimal string to bytes
        if len(hex_data) % 2 != 0:
            hex_data = '0' + hex_data  # Pad with leading zero if odd length
        
        input_bytes = bytes.fromhex(hex_data)
        
        # Compute SHA3 hash
        hasher = SHA3(hash_size)
        hasher.update(input_bytes)
        hash_result = hasher.hexdigest()
        
        # Write hash result to output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(hash_result.upper())
        
        print(f"SHA3-{hash_size} hash computed successfully")
        print(f"Input file: {input_file}")
        print(f"Output file: {output_file}")
        print(f"Hash: {hash_result.upper()}")
        
    except FileNotFoundError as exc:
        print(f"Error: Input file '{input_file}' not found")
        raise FileNotFoundError(f"Input file not found: {input_file}") from exc
    except PermissionError as exc:
        print("Error: Permission denied accessing files")
        raise PermissionError("Permission denied") from exc
    except ValueError as exc:
        print(f"Error: {exc}")
        raise
    except Exception as exc:
        print(f"Unexpected error: {exc}")
        raise


def demo():
    """Demonstration of SHA3 functionality."""
    print("SHA3 Hash Function Demo")
    print("=" * 50)
    
    # Test vectors
    test_cases = [
        ("", "empty string"),
        (b"abc", "simple test"),
        (b"The quick brown fox jumps over the lazy dog", "pangram"),
        (b"a" * 1000, "1000 'a' characters")
    ]
    
    for data, description in test_cases:
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        print(f"\nTest: {description}")
        print(f"Input: {data[:50]}{'...' if len(data) > 50 else ''}")
        
        for variant in [224, 256, 384, 512]:
            hasher = SHA3(variant)
            hasher.update(data)
            hash_value = hasher.hexdigest()
            print(f"SHA3-{variant}: {hash_value}")
    
    # File hashing example
    print(f"\n{'='*50}")
    print("File Hashing Example")
    
    # Create a test file
    test_file = "test_sha3.txt"
    test_content = b"This is a test file for SHA3 hashing."
    
    try:
        with open(test_file, 'wb') as f:
            f.write(test_content)
        
        print(f"Created test file: {test_file}")
        hash_result = hash_file(test_file, 256)
        print(f"SHA3-256 of file: {hash_result}")
        
        # Clean up
        os.remove(test_file)
        print("Test file removed.")
        
    except (OSError, IOError) as e:
        print(f"File operation error: {e}")


def main():
    """
    Main function for SHA3 implementation.
    
    Implements SHA3 hash function:
    - Input file: Hexadecimal digits of arbitrary length
    - Output: Hash value (Hexadecimal)
    - Filename format: [Input.txt] [Output.txt]
    - Optional parameter for hash size (224, 256, 384, 512), default is 224
    """
    import sys
    
    # Default values
    input_file = "Input.txt"
    output_file = "Output.txt"
    hash_size = 224
    
    # Parse command line arguments
    if len(sys.argv) >= 3:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
    
    if len(sys.argv) >= 4:
        try:
            hash_size = int(sys.argv[3])
            if hash_size not in [224, 256, 384, 512]:
                print(f"Error: Unsupported hash size {hash_size}. Supported sizes: 224, 256, 384, 512")
                print("Using default hash size: 224")
                hash_size = 224
        except ValueError:
            print(f"Error: Invalid hash size '{sys.argv[3]}'. Using default: 224")
            hash_size = 224
    
    # Display usage information
    print("SHA3 Hash Function")
    print("=" * 30)
    print("Usage: python sha3.py [input_file] [output_file] [hash_size]")
    print(f"Input file: {input_file}")
    print(f"Output file: {output_file}")
    print(f"Hash size: SHA3-{hash_size}")
    print()
    
    try:
        process_hex_file(input_file, output_file, hash_size)
    except (FileNotFoundError, PermissionError, ValueError) as e:
        print(f"Failed to process files: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()