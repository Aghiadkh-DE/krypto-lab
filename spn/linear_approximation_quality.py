#!/usr/bin/env python3
"""
Linear Approximation Quality Evaluator for SPN

This program evaluates the quality of a given linear approximation for a 4-round
Substitution-Permutation Network (SPN). It validates the approximation trail and
calculates its quality using the Piling-up Lemma.

Usage: python linear_approximation_quality.py [S-Box] [Approximation]

Args:
    S-Box: 16 hexadecimal characters defining the S-Box lookup table
    Approximation: 32 hexadecimal characters encoding input/output masks for 16 S-Boxes
"""

import sys


def parse_sbox(sbox_string):
    """Parse S-Box string into lookup table."""
    if len(sbox_string) != 16:
        raise ValueError("S-Box must be exactly 16 hexadecimal characters")
    
    sbox = {}
    for i, char in enumerate(sbox_string):
        try:
            sbox[i] = int(char, 16)
        except ValueError:
            raise ValueError(f"Invalid hexadecimal character in S-Box: {char}")
    
    return sbox


def parse_approximation(approx_string):
    """Parse approximation string into (input_mask, output_mask) pairs for each S-Box."""
    if len(approx_string) != 32:
        raise ValueError("Approximation must be exactly 32 hexadecimal characters")
    
    approximations = []
    for i in range(0, 32, 2):
        try:
            input_mask = int(approx_string[i], 16)
            output_mask = int(approx_string[i + 1], 16)
            approximations.append((input_mask, output_mask))
        except ValueError:
            raise ValueError(f"Invalid hexadecimal character in approximation: {approx_string[i:i+2]}")
    
    return approximations


def apply_permutation(output_masks):
    """
    Apply the SPN permutation to output masks from previous round.
    
    Permutation: [1,5,9,13, 2,6,10,14, 3,7,11,15, 4,8,12,16]
    This maps input bit position to output bit position.
    """
    # Convert 1-indexed to 0-indexed
    permutation = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]
    
    # Combine all output masks from the 4 S-Boxes in the previous round
    combined_mask = 0
    for i, mask in enumerate(output_masks):
        combined_mask |= mask << (i * 4)
    
    # Apply permutation
    permuted_mask = 0
    for i in range(16):
        if combined_mask & (1 << i):
            permuted_mask |= 1 << permutation[i]
    
    # Split back into 4 S-Box input masks
    input_masks = []
    for i in range(4):
        input_masks.append((permuted_mask >> (i * 4)) & 0xF)
    
    return input_masks


def validate_approximation_trail(approximations):
    """
    Validate the approximation trail by checking consistency between rounds.
    
    Returns True if valid, False otherwise.
    """
    # Split approximations by rounds (4 S-Boxes per round, 4 rounds)
    rounds = []
    for round_num in range(4):
        start_idx = round_num * 4
        rounds.append(approximations[start_idx:start_idx + 4])
    
    # Check trail validity for rounds 2, 3, and 4
    for round_num in range(1, 4):  # Rounds 2, 3, 4 (0-indexed: 1, 2, 3)
        # Get output masks from previous round
        prev_round_output_masks = [pair[1] for pair in rounds[round_num - 1]]
        
        # Calculate expected input masks for current round
        expected_input_masks = apply_permutation(prev_round_output_masks)
        
        # Get actual input masks from current round
        actual_input_masks = [pair[0] for pair in rounds[round_num]]
        
        # Check if they match
        if expected_input_masks != actual_input_masks:
            return False
    
    return True


def calculate_sbox_bias(sbox, input_mask, output_mask):
    """
    Calculate the bias of a linear approximation for a single S-Box.
    
    Returns the absolute bias |ε(U_a ⊕ V_b)|.
    """
    if input_mask == 0 and output_mask == 0:
        return 1.0  # Inactive S-Box has bias 1
    
    count_zero = 0
    
    # Iterate through all 16 possible inputs
    for u in range(16):
        v = sbox[u]  # S-Box output
        
        # Calculate U_a (XOR of input bits selected by input_mask)
        u_a = 0
        for bit_pos in range(4):
            if input_mask & (1 << bit_pos):
                u_a ^= (u >> bit_pos) & 1
        
        # Calculate V_b (XOR of output bits selected by output_mask)
        v_b = 0
        for bit_pos in range(4):
            if output_mask & (1 << bit_pos):
                v_b ^= (v >> bit_pos) & 1
        
        # Count when U_a ⊕ V_b = 0
        if u_a ^ v_b == 0:
            count_zero += 1
    
    # Calculate probability and bias
    probability = count_zero / 16
    bias = abs(probability - 0.5)
    
    return bias


def calculate_approximation_quality(sbox, approximations):
    """
    Calculate the overall quality of the approximation using the Piling-up Lemma.
    
    Quality = 2^(|S|-1) * ∏(T_S) for all active S-Boxes S
    """
    active_sboxes = []
    biases = []
    
    # Identify active S-Boxes and calculate their biases
    for i, (input_mask, output_mask) in enumerate(approximations):
        if input_mask != 0 or output_mask != 0:
            active_sboxes.append(i)
            bias = calculate_sbox_bias(sbox, input_mask, output_mask)
            biases.append(bias)
    
    if not active_sboxes:
        return 0.0  # No active S-Boxes
    
    # Apply Piling-up Lemma
    num_active = len(active_sboxes)
    quality = (2 ** (num_active - 1))
    
    for bias in biases:
        quality *= bias
    
    return quality


def main():
    """Main program entry point."""
    if len(sys.argv) != 3:
        print("Usage: python linear_approximation_quality.py [S-Box] [Approximation]", file=sys.stderr)
        sys.exit(1)
    
    sbox_string = sys.argv[1]
    approx_string = sys.argv[2]
    
    try:
        # Parse inputs
        sbox = parse_sbox(sbox_string)
        approximations = parse_approximation(approx_string)
        
        # Validate approximation trail
        if not validate_approximation_trail(approximations):
            print(-1)
            return
        
        # Calculate quality
        quality = calculate_approximation_quality(sbox, approximations)
        print(quality)
        
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
