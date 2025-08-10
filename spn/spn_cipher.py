import sys

from util.file_util import write_file, read_file


class SPNCipher:
    def __init__(self):
        # S-box mapping (4-bit → 4-bit)
        self.sbox = {
            0x0: 0xE, 0x1: 0x4, 0x2: 0xD, 0x3: 0x1,
            0x4: 0x2, 0x5: 0xF, 0x6: 0xB, 0x7: 0x8,
            0x8: 0x3, 0x9: 0xA, 0xA: 0x6, 0xB: 0xC,
            0xC: 0x5, 0xD: 0x9, 0xE: 0x0, 0xF: 0x7
        }
        
        # Inverse S-box for decryption
        self.inv_sbox = {v: k for k, v in self.sbox.items()}
        
        # Permutation πP on 16 bit positions (1-indexed to 0-indexed)
        # πP = [1,5,9,13, 2,6,10,14, 3,7,11,15, 4,8,12,16]
        self.permutation = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]
        
        # Inverse permutation for decryption
        self.inv_permutation = [0] * 16
        for i, p in enumerate(self.permutation):
            self.inv_permutation[p] = i
    
    def apply_sbox(self, data):
        """Apply S-box substitution to 16-bit data (4 nibbles)"""
        result = 0
        for i in range(4):
            nibble = (data >> (i * 4)) & 0xF
            result |= self.sbox[nibble] << (i * 4)
        return result
    
    def apply_inv_sbox(self, data):
        """Apply inverse S-box substitution to 16-bit data (4 nibbles)"""
        result = 0
        for i in range(4):
            nibble = (data >> (i * 4)) & 0xF
            result |= self.inv_sbox[nibble] << (i * 4)
        return result
    
    def apply_permutation(self, data):
        """Apply bit permutation to 16-bit data"""
        result = 0
        for i in range(16):
            if data & (1 << i):
                result |= 1 << self.permutation[i]
        return result
    
    def apply_inv_permutation(self, data):
        """Apply inverse bit permutation to 16-bit data"""
        result = 0
        for i in range(16):
            if data & (1 << i):
                result |= 1 << self.inv_permutation[i]
        return result
    
    def encrypt_block(self, plaintext, key):
        """Encrypt a single 16-bit block"""
        state = plaintext
        
        # 4 rounds
        for round_num in range(4):
            # Add round key (XOR with key)
            state ^= key
            
            # Apply S-box substitution
            state = self.apply_sbox(state)
            
            # Apply permutation (except in the last round)
            if round_num < 3:
                state = self.apply_permutation(state)
        
        # Final key addition
        state ^= key
        
        return state
    
    def decrypt_block(self, ciphertext, key):
        """Decrypt a single 16-bit block"""
        state = ciphertext
        
        # Remove final key
        state ^= key
        
        # 4 rounds (in reverse)
        for round_num in range(3, -1, -1):
            # Apply inverse permutation (except in the first reverse round)
            if round_num < 3:
                state = self.apply_inv_permutation(state)
            
            # Apply inverse S-box substitution
            state = self.apply_inv_sbox(state)
            
            # Remove round key (XOR with key)
            state ^= key
        
        return state
    
    def encrypt(self, plaintext_hex, key_hex):
        """Encrypt hex string in ECB mode"""
        # Convert hex strings to integers
        key = int(key_hex, 16)
        
        # Remove any whitespace and ensure even length
        plaintext_hex = plaintext_hex.replace(' ', '').replace('\n', '')
        if len(plaintext_hex) % 4 != 0:
            # Pad with zeros if necessary
            plaintext_hex = plaintext_hex.ljust((len(plaintext_hex) + 3) // 4 * 4, '0')
        
        result = ""
        
        # Process each 16-bit block (4 hex digits)
        for i in range(0, len(plaintext_hex), 4):
            block_hex = plaintext_hex[i:i+4]
            block = int(block_hex, 16)
            encrypted_block = self.encrypt_block(block, key)
            result += f"{encrypted_block:04X}"
        
        return result
    
    def decrypt(self, ciphertext_hex, key_hex):
        """Decrypt hex string in ECB mode"""
        # Convert hex strings to integers
        key = int(key_hex, 16)
        
        # Remove any whitespace and ensure even length
        ciphertext_hex = ciphertext_hex.replace(' ', '').replace('\n', '')
        if len(ciphertext_hex) % 4 != 0:
            raise ValueError("Ciphertext length must be multiple of 4 hex digits")
        
        result = ""
        
        # Process each 16-bit block (4 hex digits)
        for i in range(0, len(ciphertext_hex), 4):
            block_hex = ciphertext_hex[i:i+4]
            block = int(block_hex, 16)
            decrypted_block = self.decrypt_block(block, key)
            result += f"{decrypted_block:04X}"
        
        return result
    
    def partial_decrypt_last_round(self, ciphertext_block, partial_key):
        """
        Partially decrypt the last round for linear cryptanalysis
        This function decrypts only specific S-boxes affected by the partial key
        """
        # Remove the final key addition
        state = ciphertext_block ^ partial_key
        
        # Apply inverse S-box to get the input to the last round S-boxes
        # For linear attack, we're interested in specific S-box inputs
        return self.apply_inv_sbox(state)


def main():
    if len(sys.argv) != 4:
        print("Usage: python spn_encrypt.py [Input] [Schlüssel] [Output]")
        print("  Input: File containing hex digits to encrypt")
        print("  Schlüssel: 16-bit key (4 hex digits)")
        print("  Output: Output file for encrypted hex digits")
        sys.exit(1)

    input_file = sys.argv[1]
    key = sys.argv[2]
    output_file = sys.argv[3]

    # Validate key format
    if len(key) != 4:
        print("Error: Key must be exactly 4 hex digits (16 bits)")
        sys.exit(1)

    try:
        int(key, 16)
    except ValueError:
        print("Error: Key must be valid hex digits")
        sys.exit(1)

    try:
        # Read input data
        plaintext = read_file(input_file).strip()

        # Create cipher instance and encrypt
        cipher = SPNCipher()
        ciphertext = cipher.encrypt(plaintext, key)

        # Write output
        write_file(output_file, ciphertext)

        print("Encryption completed successfully")
        print(f"Input: {plaintext}")
        print(f"Key: {key}")
        print(f"Output: {ciphertext}")

    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found")
        sys.exit(1)
    except (IOError, ValueError) as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()