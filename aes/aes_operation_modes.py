from typing import Callable

from bitstring import Bits

def mode_ecb_encrypt(block_size :int, aes_encrypt: Callable[[bytes, bytes], bytes], plain_text: bytes):
    """
    Encrypts the plain text using AES in ECB mode.

    :param block_size: The block size in integer.
    :param aes_encrypt: The AES encryption function.
    :param plain_text: The plain text to encrypt.
    :return: The encrypted text.
    """
    # Pad the plain text to a multiple of the block size
    padding_length = (block_size - len(plain_text) % block_size) % block_size
    padded_plain_text = plain_text + bytes([padding_length] * padding_length)

    # Encrypt each block
    encrypted_blocks = []
    for i in range(0, len(padded_plain_text), block_size):
        block = padded_plain_text[i:i + block_size]
        print(block)
        encrypted_block = aes_encrypt(block, b'')
        encrypted_blocks.append(encrypted_block)

    return b''.join(encrypted_blocks)

if __name__ == "__main__":
    # Example AES encryption function (dummy implementation)
    def dummy_aes_encrypt(block: bytes, key: bytes) -> bytes:
        return block

    # Example usage
    block_size = 1  # AES block size in bytes
    plain_text = b'AB'
    print(len(plain_text))
    encrypted_text = mode_ecb_encrypt(block_size, dummy_aes_encrypt, plain_text)
    print("Encrypted text:", Bits(bytes=encrypted_text).bytes)