#!/usr/bin/env python3
"""
Debug script to understand the permutation and trail validation
"""

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
    
    print(f"Combined output mask: {combined_mask:04x}")
    
    # Apply permutation
    permuted_mask = 0
    for i in range(16):
        if combined_mask & (1 << i):
            permuted_mask |= 1 << permutation[i]
    
    print(f"Permuted mask: {permuted_mask:04x}")
    
    # Split back into 4 S-Box input masks
    input_masks = []
    for i in range(4):
        input_masks.append((permuted_mask >> (i * 4)) & 0xF)
    
    return input_masks


def test_simple_case():
    """Test a simple case where first S-Box has output mask 1."""
    print("Testing: First S-Box output mask = 1, others = 0")
    output_masks = [1, 0, 0, 0]
    result = apply_permutation(output_masks)
    print(f"Input masks for next round: {result}")
    print(f"As hex: {[f'{x:x}' for x in result]}")
    print()


def create_valid_trail():
    """Create a valid approximation trail."""
    print("Creating valid trail...")
    
    # Start with first round: only S-Box 1 active with output mask 1
    round1 = [(0, 1), (0, 0), (0, 0), (0, 0)]
    print(f"Round 1: {round1}")
    
    # Calculate what round 2 should be
    round1_outputs = [pair[1] for pair in round1]
    round2_inputs = apply_permutation(round1_outputs)
    round2 = [(round2_inputs[i], 0) for i in range(4)]
    print(f"Round 2: {round2}")
    
    # Rounds 3 and 4 should be all inactive if round 2 has no outputs
    round3 = [(0, 0), (0, 0), (0, 0), (0, 0)]
    round4 = [(0, 0), (0, 0), (0, 0), (0, 0)]
    
    # Convert to approximation string
    all_rounds = round1 + round2 + round3 + round4
    approx_string = ""
    for input_mask, output_mask in all_rounds:
        approx_string += f"{input_mask:x}{output_mask:x}"
    
    print(f"Valid approximation string: {approx_string}")
    return approx_string


if __name__ == "__main__":
    test_simple_case()
    valid_trail = create_valid_trail()
