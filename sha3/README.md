# SHA-3 (SHA3-224) Implementation

This directory contains a complete implementation of the SHA3-224 hash function according to FIPS 202 standards.

## Files

- `sha3_224.py` - Main SHA3-224 implementation
- `test_sha3.py` - Comprehensive test suite
- `test_*.txt` - Test input files
- `README.md` - This documentation

## Algorithm Overview

SHA3-224 is part of the SHA-3 family of cryptographic hash functions based on the Keccak algorithm. It produces a 224-bit (28-byte) hash value.

### Parameters for SHA3-224

- **Hash size (d)**: 224 bits (28 bytes)
- **Block size (rate r)**: 1152 bits (144 bytes)
- **Capacity (c)**: 448 bits (56 bytes)
- **Block width (b = c + r)**: 1600 bits (200 bytes)

### Algorithm Components

#### 1. Keccak-f[1600] Permutation
The core permutation function operates on a 5×5 array of 64-bit words through 24 rounds.

#### 2. Five Step Functions (per round)
- **θ (theta)**: Column parity calculations
- **ρ (rho)**: Cyclic rotation of individual lanes
- **π (pi)**: Lane position permutation
- **χ (chi)**: Nonlinear component (only nonlinear operation)
- **ι (iota)**: Round constant addition

#### 3. Padding Function
Appends the padding pattern `0110*1` to make the message length divisible by the rate.

## Usage

### Command Line Interface

```bash
python sha3_224.py <input_file> <output_file>
```

**Example:**
```bash
python sha3_224.py test_abc.txt output.txt
```

### Python API

```python
from sha3.sha3_224 import sha3_224_hash, sha3_224_hash_bytes, sha3_224_file

# Hash a hexadecimal string
hash_value = sha3_224_hash("616263")  # "abc" in hex

# Hash bytes directly
hash_value = sha3_224_hash_bytes(b"abc")

# Hash from file
sha3_224_file("input.txt", "output.txt")
```

### Input Format

The input should be hexadecimal digits. Spaces, newlines, and tabs are automatically removed.

**Valid input examples:**
- `616263` (hex for "abc")
- `61 62 63` (with spaces)
- `` (empty string)
- `80` (single bit)

### Output Format

The output is a 56-character hexadecimal string representing the 224-bit hash value.

## Implementation Details

### State Representation
The Keccak state is represented as a 5×5 array of 64-bit words (lanes), totaling 1600 bits.

### Byte Ordering
- Little-endian byte ordering is used for converting between bytes and 64-bit words
- This follows the official Keccak specification

### Round Constants
The implementation includes all 24 round constants for the ι (iota) step as specified in the Keccak standard.

### Rotation Offsets
The ρ (rho) step uses the official rotation offsets for each of the 25 lanes.

## Testing

Run the comprehensive test suite:

```bash
python test_sha3.py
```

The test suite includes:
- Component tests for individual functions
- Known test vectors
- Edge cases and error conditions
- Format validation

### Test Files

- `test_empty.txt` - Empty input
- `test_abc.txt` - "abc" in hexadecimal (616263)
- `test_single_bit.txt` - Single bit (80)
- `test_long.txt` - Longer test message

## Examples

### Example 1: Empty String
```bash
python sha3_224.py test_empty.txt output_empty.txt
```
**Expected output:** `6B4E03423667DBB73B6E15454F0EB1ABD4597F9A1B078E3F5B5A6BC7`

### Example 2: "abc"
```bash
python sha3_224.py test_abc.txt output_abc.txt
```

### Example 3: Long Message
```bash
python sha3_224.py test_long.txt output_long.txt
```

## Mathematical Background

SHA-3 is based on the sponge construction:

1. **Absorption Phase**: Message blocks are XORed with the state and processed through the permutation
2. **Squeezing Phase**: The desired number of output bits are extracted from the state

The security of SHA-3 relies on the cryptographic properties of the Keccak-f permutation, which provides:
- Collision resistance
- Pre-image resistance
- Second pre-image resistance

## Verification

To verify the implementation against reference values:

1. Use the NIST test vectors for SHA3-224
2. Compare with other standard implementations
3. Run the provided test suite

## Performance Notes

This implementation prioritizes clarity and correctness over performance. For production use, consider:
- Using optimized bit manipulation operations
- Implementing lane-wise operations more efficiently
- Using platform-specific optimizations

## References

- FIPS 202: SHA-3 Standard
- The Keccak SHA-3 submission
- NIST Special Publication 800-185
