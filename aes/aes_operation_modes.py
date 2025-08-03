from typing import Callable

def mode_ecb_encrypt(block_size: int, aes_encrypt: Callable[[bytes, bytes], bytes], plain_text: bytes, key: bytes) -> bytes:
    """
    Encrypts the plain text using AES in ECB mode.

    :param key: AES key in bytes.
    :param block_size: The block size in integer.
    :param aes_encrypt: The AES encryption function.
    :param plain_text: The plain text to encrypt.
    :return: The encrypted text.
    """
    padding_length = (block_size - len(plain_text) % block_size) % block_size
    padded_plain_text = plain_text + bytes([0] * padding_length)

    encrypted_blocks = []
    for i in range(0, len(padded_plain_text), block_size):
        block = padded_plain_text[i:i + block_size]
        encrypted_block = aes_encrypt(block, key)
        encrypted_blocks.append(encrypted_block)

    return b''.join(encrypted_blocks)

def mode_ecb_decrypt(block_size: int, aes_decrypt_func: Callable[[bytes, bytes], bytes], cipher_text: bytes, key: bytes) -> bytes:
    """
    Decrypts the cipher text using AES in ECB mode.

    :param key: AES key in bytes.
    :param block_size: The block size in integer.
    :param aes_decrypt_func: The AES decryption function.
    :param cipher_text: The cipher text to decrypt.
    :return: The decrypted text.
    """
    decrypted_blocks = []
    for i in range(0, len(cipher_text), block_size):
        block = cipher_text[i:i + block_size]
        decrypted_block = aes_decrypt_func(block, key)
        decrypted_blocks.append(decrypted_block)

    return b''.join(decrypted_blocks).rstrip(b'\x00')

def aes_encrypt(plain_text: bytes, key: bytes) -> bytes:
    """
    Placeholder for AES encryption function.
    This should be replaced with an actual AES encryption implementation.
    """
    # Extend key to match the length of plain_text by repeating it
    extended_key = (key * ((len(plain_text) // len(key)) + 1))[:len(plain_text)]
    print(f"Needed repeating key: {(key * ((len(plain_text) // len(key)) + 1))}")
    return bytes([b ^ k for b, k in zip(plain_text, extended_key)])

def aes_decrypt(cipher_text: bytes, key: bytes) -> bytes:
    """
    Placeholder for AES decryption function.
    For XOR encryption, decryption is the same as encryption.
    """
    # Extend key to match the length of cipher_text by repeating it
    extended_key = (key * ((len(cipher_text) // len(key)) + 1))[:len(cipher_text)]
    return bytes([b ^ k for b, k in zip(cipher_text, extended_key)])

if __name__ == "__main__":
    cipher = mode_ecb_encrypt(16, aes_encrypt, b'This is a test text.', b'SixteenByteKey!')
    print(f"Cipher: {cipher}")
    plain = mode_ecb_decrypt(16, aes_decrypt, cipher, b'SixteenByteKey!')
    print(f"Plain: {plain.decode()}")
