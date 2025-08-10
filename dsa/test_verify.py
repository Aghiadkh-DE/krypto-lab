
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
r = 13296216272177932449805685288345330332763423366
s = 673435344691044881606974868105501898606995561091
print(f'Using signature: r = {r}, s = {s}')

# Verify the signature
print('Verifying signature...')
is_valid = dsa_verify(message, r, s, p, q, g, y)

if is_valid:
    print('Signature is VALID')
else:
    print('Signature is INVALID')
