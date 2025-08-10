
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from spn_cipher import SPNCipher
from util.file_util import read_file


class LinearCryptanalysis:
    def __init__(self):
        self.cipher = SPNCipher()
    
    def extract_bits(self, value, bit_positions):
        """Extract specific bits from a value and return their XOR"""
        result = 0
        for pos in bit_positions:
            if value & (1 << (pos - 1)):  # Convert 1-indexed to 0-indexed
                result ^= 1
        return result
    
    def compute_linear_approximation(self, plaintext, last_round_input):
        """
        Compute the linear approximation:
        T = U1 ⊕ U3 ⊕ U4 ⊕ V2
        
        Where:
        - U1, U3, U4 are plaintext bits at positions 1, 3, 4
        - V2 is the input bit to the last round S-box at position 2
        """
        # Extract plaintext bits U1, U3, U4 (positions 1, 3, 4)
        u_bits = self.extract_bits(plaintext, [1, 3, 4])
        
        # Extract last round input bit V2 (position 2)
        v_bits = self.extract_bits(last_round_input, [2])
        
        # Compute T = U1 ⊕ U3 ⊕ U4 ⊕ V2
        return u_bits ^ v_bits
    
    def partial_decrypt_for_attack(self, ciphertext, partial_key_candidate):
        """
        Partially decrypt the last round to get the input to the last round S-boxes
        For the linear attack, we need to decrypt specific S-boxes
        """
        # The partial key affects specific S-boxes in the last round
        # For this attack, we focus on the S-boxes that affect our linear approximation
        
        # Remove the final key addition for the relevant bits
        # Since we're doing a partial attack, we only consider specific bits
        state = ciphertext ^ partial_key_candidate
        
        # Apply inverse S-box to get the last round input
        return self.cipher.apply_inv_sbox(state)
    
    def linear_attack(self, plaintexts, ciphertexts, target_bits=4):
        """
        Perform linear cryptanalysis attack to recover partial key bits
        
        Args:
            plaintexts: List of plaintext values
            ciphertexts: List of corresponding ciphertext values
            target_bits: Number of key bits to attack (default 4 for one S-box)
        
        Returns:
            List of (partial_key, bias, probability) tuples sorted by |bias|
        """
        num_pairs = len(plaintexts)
        results = []
        
        # Try all possible partial key candidates (2^target_bits possibilities)
        for partial_key in range(1 << target_bits):
            count_zero = 0
            
            # For each plaintext-ciphertext pair
            for i in range(num_pairs):
                plaintext = plaintexts[i]
                ciphertext = ciphertexts[i]
                
                # Partially decrypt to get last round input
                last_round_input = self.partial_decrypt_for_attack(ciphertext, partial_key)
                
                # Compute the linear approximation
                linear_value = self.compute_linear_approximation(plaintext, last_round_input)
                
                # Count when the linear approximation equals 0
                if linear_value == 0:
                    count_zero += 1
            
            # Compute empirical probability and bias
            probability = count_zero / num_pairs
            empirical_bias = probability - 0.5
            
            results.append((partial_key, empirical_bias, probability))
        
        # Sort by absolute bias (descending)
        results.sort(key=lambda x: abs(x[1]), reverse=True)
        
        return results
    
    def extended_linear_attack(self, plaintexts, ciphertexts, key_bits=8):
        """
        Extended attack for more key bits using multiple S-boxes
        """
        num_pairs = len(plaintexts)
        results = []
        
        # Try all possible partial key candidates
        for partial_key in range(1 << key_bits):
            count_zero = 0
            
            # For each plaintext-ciphertext pair
            for i in range(num_pairs):
                plaintext = plaintexts[i]
                ciphertext = ciphertexts[i]
                
                # Partially decrypt the last round
                last_round_input = self.partial_decrypt_for_attack(ciphertext, partial_key)
                
                # Compute linear approximation
                linear_value = self.compute_linear_approximation(plaintext, last_round_input)
                
                if linear_value == 0:
                    count_zero += 1
            
            probability = count_zero / num_pairs
            empirical_bias = probability - 0.5
            
            results.append((partial_key, empirical_bias, probability))
        
        results.sort(key=lambda x: abs(x[1]), reverse=True)
        return results


def parse_hex_data(hex_string):
    """Parse hex string into list of 16-bit blocks"""
    hex_string = hex_string.replace(' ', '').replace('\n', '').strip()
    blocks = []
    
    # Process every 4 hex digits as one 16-bit block
    for i in range(0, len(hex_string), 4):
        block_hex = hex_string[i:i+4]
        if len(block_hex) == 4:
            blocks.append(int(block_hex, 16))
    
    return blocks


def main():
    if len(sys.argv) != 3:
        print("Usage: python linear_attack.py [Klartexte] [Kryptotexte]")
        print("  Klartexte: File containing plaintext hex blocks")
        print("  Kryptotexte: File containing corresponding ciphertext hex blocks")
        sys.exit(1)
    
    plaintext_file = sys.argv[1]
    ciphertext_file = sys.argv[2]
    
    try:
        # Read data files
        plaintext_data = read_file(plaintext_file)
        ciphertext_data = read_file(ciphertext_file)
        
        # Parse hex data into blocks
        plaintexts = parse_hex_data(plaintext_data)
        ciphertexts = parse_hex_data(ciphertext_data)
        
        if len(plaintexts) != len(ciphertexts):
            print("Error: Number of plaintext and ciphertext blocks must match")
            sys.exit(1)
        
        if len(plaintexts) == 0:
            print("Error: No valid data blocks found")
            sys.exit(1)
        
        print(f"Performing linear cryptanalysis with {len(plaintexts)} plaintext-ciphertext pairs")
        
        # Perform linear attack
        cryptanalysis = LinearCryptanalysis()
        
        # Attack 4-bit partial key (one S-box)
        results_4bit = cryptanalysis.linear_attack(plaintexts, ciphertexts, 4)
        
        print("\n4-bit partial key candidates (sorted by |bias|):")
        for key, bias, prob in results_4bit[:8]:  # Top 8 candidates
            print(f"{key:01X}: bias={bias:+.6f}, prob={prob:.6f}")
        
        # Attack 8-bit partial key (two S-boxes)
        if len(plaintexts) >= 100:  # Only if we have enough data
            results_8bit = cryptanalysis.extended_linear_attack(plaintexts, ciphertexts, 8)
            
            print("\n8-bit partial key candidates (sorted by |bias|):")
            for key, bias, prob in results_8bit[:8]:  # Top 8 candidates
                print(f"{key:02X}: bias={bias:+.6f}, prob={prob:.6f}")
        
        # Output most likely partial keys to stdout
        print(f"\nMost likely 4-bit partial key: {results_4bit[0][0]:01X}")
        
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
        sys.exit(1)
    except (IOError, ValueError) as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
