#!/usr/bin/env python3
"""
Work backwards from a good approximation in the last round
"""

def reverse_permutation(input_masks):
    """Apply the inverse SPN permutation."""
    # Original permutation: [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]
    # Inverse permutation
    inv_permutation = [0] * 16
    permutation = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]
    for i, p in enumerate(permutation):
        inv_permutation[p] = i
    
    # Combine input masks from the 4 S-Boxes
    combined_mask = 0
    for i, mask in enumerate(input_masks):
        combined_mask |= mask << (i * 4)
    
    print(f"Combined input mask: {combined_mask:04x}")
    
    # Apply inverse permutation
    inv_permuted_mask = 0
    for i in range(16):
        if combined_mask & (1 << i):
            inv_permuted_mask |= 1 << inv_permutation[i]
    
    print(f"Inverse permuted mask: {inv_permuted_mask:04x}")
    
    # Split back into 4 S-Box output masks
    output_masks = []
    for i in range(4):
        output_masks.append((inv_permuted_mask >> (i * 4)) & 0xF)
    
    return output_masks


def create_backwards_trail():
    """Create a trail working backwards from round 4."""
    print("Working backwards from a good approximation in round 4...")
    
    # Round 4: Use approximation (1, 7) which has bias 0.375
    round4 = [(1, 7), (0, 0), (0, 0), (0, 0)]
    print(f"Round 4: {round4}")
    
    # What should round 3 output masks be?
    round4_inputs = [pair[0] for pair in round4]
    round3_outputs = reverse_permutation(round4_inputs)
    round3 = [(0, round3_outputs[i]) for i in range(4)]
    print(f"Round 3: {round3}")
    
    # Continue backwards
    round3_inputs = [pair[0] for pair in round3]
    round2_outputs = reverse_permutation(round3_inputs)
    round2 = [(0, round2_outputs[i]) for i in range(4)]
    print(f"Round 2: {round2}")
    
    # Continue backwards
    round2_inputs = [pair[0] for pair in round2]
    round1_outputs = reverse_permutation(round2_inputs)
    round1 = [(0, round1_outputs[i]) for i in range(4)]
    print(f"Round 1: {round1}")
    
    # Convert to approximation string
    all_rounds = round1 + round2 + round3 + round4
    approx_string = ""
    for inp, out in all_rounds:
        approx_string += f"{inp:x}{out:x}"
    
    print(f"Backwards trail: {approx_string}")
    return approx_string


if __name__ == "__main__":
    create_backwards_trail()
