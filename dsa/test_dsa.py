#!/usr/bin/env python3
"""
DSA Test Script - Automated testing of all three programs
"""

import sys
import os
import subprocess

def run_command(cmd):
    """Run a command and return the output"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr

def main():
    os.chdir("c:/Users/aghyd/PycharmProjects/krypto-lab/dsa")
    python_exe = "C:/Users/aghyd/PycharmProjects/krypto-lab/.venv/Scripts/python.exe"
    
    print("=== DSA Implementation Test ===\n")
    
    # Test 1: Key Generation
    print("1. Testing Key Generation...")
    returncode, stdout, stderr = run_command(f"{python_exe} dsa_keygen.py test_public.key test_private.key")
    if returncode == 0:
        print("✓ Key generation successful")
        print(stdout.strip())
    else:
        print("✗ Key generation failed")
        print(stderr)
        return
    
    print("\n" + "="*50 + "\n")
    
    # Test 2: Signing
    print("2. Testing Message Signing...")
    returncode, stdout, stderr = run_command(f"{python_exe} dsa_sign.py test_private.key test_message.txt")
    if returncode == 0:
        print("✓ Message signing successful")
        print(stdout.strip())
        
        # Extract r and s values from output
        lines = stdout.strip().split('\n')
        r_line = next(line for line in lines if line.startswith('r = '))
        s_line = next(line for line in lines if line.startswith('s = '))
        r_value = r_line.split(' = ')[1]
        s_value = s_line.split(' = ')[1]
        
    else:
        print("✗ Message signing failed")
        print(stderr)
        return
    
    print("\n" + "="*50 + "\n")
    
    # Test 3: Verification (automated)
    print("3. Testing Signature Verification...")
    
    # Create a verification script that provides the r and s values automatically
    verification_script = f"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dsa.dsa_core import read_key_file, read_message_file, dsa_verify

# Read public key file
p, q, g, y = read_key_file('test_public.key')
print('Loaded public key from: test_public.key')

# Read message
message = read_message_file('test_message.txt')
print('Loaded message from: test_message.txt')

# Use the signature values from signing
r = {r_value}
s = {s_value}
print(f'Using signature: r = {{r}}, s = {{s}}')

# Verify the signature
print('Verifying signature...')
is_valid = dsa_verify(message, r, s, p, q, g, y)

if is_valid:
    print('Signature is VALID')
else:
    print('Signature is INVALID')
"""
    
    with open('test_verify.py', 'w', encoding='utf-8') as f:
        f.write(verification_script)
    
    returncode, stdout, stderr = run_command(f"{python_exe} test_verify.py")
    if returncode == 0:
        print("✓ Signature verification completed")
        print(stdout.strip())
    else:
        print("✗ Signature verification failed")
        print(stderr)
    
    print("\n" + "="*50 + "\n")
    
    # Show key file formats
    print("4. Key File Format Verification...")
    print("\nPublic Key File Contents:")
    with open('test_public.key', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i, line in enumerate(lines, 1):
            print(f"Line {i}: {line.strip()}")
    
    print("\nPrivate Key File Contents:")
    with open('test_private.key', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i, line in enumerate(lines, 1):
            print(f"Line {i}: {line.strip()}")
    
    print("\n=== All Tests Completed ===")

if __name__ == "__main__":
    main()
