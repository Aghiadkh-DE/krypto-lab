# DSA (Digital Signature Algorithm) Implementation

This directory contains a complete implementation of the Digital Signature Algorithm (DSA) with three command-line programs as specified.

## Programs

### 1. Parameter & Key Generation (`dsa_keygen.py`)

**Usage:**
```
python dsa_keygen.py [public_key_output] [private_key_output]
```

**Description:**
- Generates DSA parameters (p, q, g) and a key pair (x, y)
- Writes two files with exactly four lines each:
  - Line 1: prime p (1024-bit)
  - Line 2: prime q (160-bit)  
  - Line 3: group element g
  - Line 4: the respective key (x for private key file, y for public key file)

**Example:**
```bash
python dsa_keygen.py public.key private.key
```

### 2. Signing (`dsa_sign.py`)

**Usage:**
```
python dsa_sign.py [key_file] [message_file]
```

**Description:**
- Signs a message using the private key from the key file
- The message file is interpreted as a string
- Outputs the signature values (r, s) to the console

**Example:**
```bash
python dsa_sign.py private.key test_message.txt
```

### 3. Verification (`dsa_verify.py`)

**Usage:**
```
python dsa_verify.py [key_file] [message_file]
```

**Description:**
- Verifies a DSA signature for a message using the public key
- The message file is interpreted as a string
- Prompts for signature values (r, s) from user input
- Outputs whether the signature is valid or invalid

**Example:**
```bash
python dsa_verify.py public.key test_message.txt
```
Then enter the r and s values when prompted.

## Key File Format

Both public and private key files have exactly 4 lines:
```
<prime p>
<prime q>
<group element g>
<key value (x for private, y for public)>
```

## Implementation Details

### DSA Parameters
- **p**: 1024-bit prime
- **q**: 160-bit prime where q divides (p-1)
- **g**: Generator element of order q in the multiplicative group mod p

### Security Features
- Uses SHA-1 for message hashing (as per DSA standard)
- Implements Miller-Rabin primality testing for parameter generation
- Proper random number generation for keys and signatures
- Validates signature parameters during verification

### Core Functions

The implementation includes:
- `generate_dsa_parameters()`: Generates p, q, g parameters
- `generate_dsa_keypair()`: Generates private/public key pair
- `dsa_sign()`: Creates DSA signature
- `dsa_verify()`: Verifies DSA signature
- Miller-Rabin primality testing
- File I/O utilities for key management

## Testing

Run the comprehensive test suite:
```bash
python test_dsa.py
```

This will test all three programs and verify the complete signing/verification process.

## Files

- `dsa_core.py`: Core DSA implementation
- `dsa_keygen.py`: Key generation program
- `dsa_sign.py`: Signing program  
- `dsa_verify.py`: Verification program
- `test_dsa.py`: Comprehensive test suite
- `test_message.txt`: Sample message file for testing
- `manual_verify_test.py`: Manual verification demonstration

## Dependencies

- Python 3.6+ (uses built-in libraries only)
- No external dependencies required

## Mathematical Background

The DSA signature algorithm works as follows:

**Key Generation:**
1. Choose primes p (1024-bit) and q (160-bit) where q divides (p-1)
2. Find generator g of order q in Z*p
3. Choose random private key x ∈ [1, q-1]
4. Compute public key y = g^x mod p

**Signing:**
1. Choose random k ∈ [1, q-1]
2. Compute r = (g^k mod p) mod q
3. Compute s = k^(-1) * (H(m) + x*r) mod q
4. Signature is (r, s)

**Verification:**
1. Check 0 < r < q and 0 < s < q
2. Compute w = s^(-1) mod q
3. Compute u1 = H(m) * w mod q
4. Compute u2 = r * w mod q  
5. Compute v = ((g^u1 * y^u2) mod p) mod q
6. Signature is valid if v = r
