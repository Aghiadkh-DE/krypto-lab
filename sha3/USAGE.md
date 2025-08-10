# SHA3-224 Usage Examples

## Command Line Usage

```bash
# Hash empty input
python sha3_224.py test_empty.txt output_empty.txt

# Hash "abc" string  
python sha3_224.py test_abc.txt output_abc.txt

# Hash any hexadecimal input
echo "48656C6C6F20576F726C64" > hello_world.txt
python sha3_224.py hello_world.txt output_hello.txt
```

## Python API Usage

```python
from sha3.sha3_224 import sha3_224_hash, sha3_224_hash_bytes, sha3_224_file

# Hash hexadecimal string
hash1 = sha3_224_hash("616263")  # "abc" in hex
print(f"SHA3-224('abc'): {hash1}")

# Hash bytes directly
hash2 = sha3_224_hash_bytes(b"abc")
print(f"SHA3-224(b'abc'): {hash2}")

# Hash from file
sha3_224_file("input.txt", "output.txt")
```

## Expected Results

- **Empty string**: `02C08F43A9FDCC39CB97D5CA256D759B4E4D61B02AD9CF9C21067FA7`
- **"abc"**: `5C75CEB97247B31D77E84988212E7CF12A5E9CF945B50185BDE831E6`
- **"a"**: `07C30A25F16A3FF3DA0B8F19639CD82686F442767755A63D2901B4FC`

## Testing

```bash
# Run all tests
python test_sha3.py

# Run verification
python verify_sha3.py

# Run demo
python demo_sha3.py
```
