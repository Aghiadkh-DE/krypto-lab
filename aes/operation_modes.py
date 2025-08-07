from typing import Callable

def mode_ecb_encrypt(block_size: int, aes_operation: Callable[[bytes, bytes], bytes], plain_text: bytes, key: bytes) -> bytes:
    padding_length = (block_size - len(plain_text) % block_size) % block_size
    padded_plain_text = plain_text + bytes([0] * padding_length)

    encrypted_blocks = []
    for i in range(0, len(padded_plain_text), block_size):
        block = padded_plain_text[i:i + block_size]
        encrypted_block = aes_operation(block, key)
        encrypted_blocks.append(encrypted_block)

    return b''.join(encrypted_blocks)

def mode_ecb_decrypt(block_size: int, aes_operation: Callable[[bytes, bytes], bytes], cipher_text: bytes, key: bytes) -> bytes:
    decrypted_blocks = []
    for i in range(0, len(cipher_text), block_size):
        block = cipher_text[i:i + block_size]
        decrypted_block = aes_operation(block, key)
        decrypted_blocks.append(decrypted_block)

    return b''.join(decrypted_blocks).rstrip(b'\x00')

def mode_cbc_encrypt(block_size: int, aes_operation: Callable[[bytes, bytes], bytes], plain_text: bytes, key: bytes, initialization_vector: bytes) -> bytes:
    if block_size != len(initialization_vector):
        raise ValueError("Initialization vector must match block size.")

    padding_length = (block_size - len(plain_text) % block_size) % block_size
    padded_plain_text = plain_text + bytes([0] * padding_length)

    encrypted_blocks = []
    cipher_block_xi = initialization_vector
    for i in range(0, len(padded_plain_text), block_size):
        plain_text_block = padded_plain_text[i:i + block_size]
        xor_block = bytes([b ^ c for b, c in zip(plain_text_block, cipher_block_xi)])
        cipher_block_xi = aes_operation(xor_block, key)
        encrypted_blocks.append(cipher_block_xi)

    return b''.join(encrypted_blocks)

def mode_cbc_decrypt(block_size: int, aes_operation: Callable[[bytes, bytes], bytes], cipher_text: bytes, key: bytes, initialization_vector: bytes) -> bytes:
    if block_size != len(initialization_vector):
        raise ValueError("Initialization vector must match block size.")

    decrypted_blocks = []
    cipher_block_xi = initialization_vector
    for i in range(0, len(cipher_text), block_size):
        cipher_text_block = cipher_text[i:i + block_size]
        decrypted_block = aes_operation(cipher_text_block, key)
        plain_text_block = bytes([b ^ c for b, c in zip(decrypted_block, cipher_block_xi)])
        cipher_block_xi = cipher_text_block
        decrypted_blocks.append(plain_text_block)

    return b''.join(decrypted_blocks).rstrip(b'\x00')

def mode_ofb(block_size: int, aes_operation: Callable[[bytes, bytes], bytes], plain_text: bytes, key: bytes, initialization_vector: bytes) -> bytes:
    encrypted_blocks = []
    cipher_block_xi = initialization_vector
    for i in range(0, len(plain_text), block_size):
        cipher_block_xi = aes_operation(cipher_block_xi, key)
        plain_text_block = plain_text[i:i + block_size]
        encrypted_block = bytes([b ^ c for b, c in zip(plain_text_block, cipher_block_xi)])
        encrypted_blocks.append(encrypted_block)

    return b''.join(encrypted_blocks)

def mode_ctr(block_size: int, aes_operation: Callable[[bytes, bytes], bytes], plain_text: bytes, key: bytes, nonce: bytes) -> bytes:
    if len(nonce) > block_size:
        raise ValueError("Nonce cannot be longer than block size.")
    
    encrypted_blocks = []
    ctr = int.from_bytes(nonce + b'\x00' * (block_size - len(nonce)), 'big')
    
    m_bits = block_size * 8
    mod_value = 2 ** m_bits
    block_count = (len(plain_text) + block_size - 1) // block_size
    
    for i in range(1, block_count + 1):
        Ti = (ctr + i - 1) % mod_value
        Ti_bytes = Ti.to_bytes(block_size, 'big')
        encrypted_counter = aes_operation(Ti_bytes, key)
        
        start_idx = (i - 1) * block_size
        end_idx = min(start_idx + block_size, len(plain_text))
        plain_text_block = plain_text[start_idx:end_idx]
        
        encrypted_block = bytes([b ^ c for b, c in zip(plain_text_block, encrypted_counter)])
        encrypted_blocks.append(encrypted_block)
    
    return b''.join(encrypted_blocks)

if __name__ == "__main__":
    ...
