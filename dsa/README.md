# Digital Signature Algorithm (DSA) Implementation

This directory contains a complete implementation of the Digital Signature Algorithm (DSA) according to the specified requirements.

## Parameters
- **L = 1024**: Bit length of prime p
- **N = 160**: Bit length of prime q  
- **Hash Function**: SHA-224 (using Python's hashlib library)
- **Encryption**: ElGamal-style approach

## Public Parameters
- **q**: Prime of length N (160 bits)
- **p**: Prime of length L (1024 bits), where p = k·q + 1
- **g**: Group element with order q
- **x**: Secret key with 1 < x < q
- **y**: Public key where y = g^x mod p

## Files

### 1. dsa_keygen.py
Generates DSA parameters and key pairs.

**Usage:**
```
python dsa_keygen.py [public_key_file] [private_key_file]
```

**Output:** Two files with the following format:
```
Line 1: Prime p
Line 2: Prime q  
Line 3: Group element g
Line 4: Key (x for private, y for public)
```

### 2. dsa_sign.py
Creates digital signatures for messages.

**Usage:**
```
python dsa_sign.py [private_key_file] [message_file]
```

**Output:** Creates `[message_file].sig` containing:
```
Line 1: r component
Line 2: s component
```

**Signature Algorithm:**
1. Calculate H(m) using SHA-224
2. Generate random k with 1 < k < q
3. Calculate r = (g^k mod p) mod q
4. Calculate s = k^(-1)(H(m) + r·x) mod q
5. If r = 0 or s = 0, choose different k

### 3. dsa_verify.py
Verifies digital signatures.

**Usage:**
```
python dsa_verify.py [public_key_file] [message_file]
```

**Input:** Reads signature from `[message_file].sig`

**Verification Algorithm:**
1. Calculate w = s^(-1) mod q
2. Calculate u1 = H(m)·w mod q
3. Calculate u2 = r·w mod q  
4. Calculate v = (g^u1 · y^u2 mod p) mod q
5. Signature is valid if v = r

## Example Usage

1. **Generate keys:**
```bash
python dsa_keygen.py public.key private.key
```

2. **Sign a message:**
```bash
python dsa_sign.py private.key message.txt
```

3. **Verify signature:**
```bash
python dsa_verify.py public.key message.txt
```

## Implementation Details

### Prime Generation
- Uses Miller-Rabin primality test with 20 rounds
- Generates q first (160 bits)
- Finds p = k·q + 1 with correct bit length (1024 bits)

### Group Element Generation
- Searches for h where g = h^k mod p ≠ 1
- Verifies g has order q by checking g^q ≡ 1 (mod p)

### Security Features
- Random k generation for each signature
- Proper range checking for signature components
- SHA-224 hash function as specified
- Modular inverse calculation using extended Euclidean algorithm

## Mathematical Background

The DSA algorithm provides:
- **Authentication**: Verifies message sender
- **Non-repudiation**: Sender cannot deny signing
- **Integrity**: Detects message tampering

Security relies on:
- Discrete logarithm problem difficulty
- Cryptographically secure hash function (SHA-224)
- Proper random number generation for k values
