#!/usr/bin/env python3
"""
Test identity S-Box properties
"""

def calculate_sbox_bias(sbox, input_mask, output_mask):
    """Calculate the bias of a linear approximation for a single S-Box."""
    if input_mask == 0 and output_mask == 0:
        return 1.0
    
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


def test_identity_sbox():
    """Test linear properties of identity S-Box."""
    # Identity S-Box: f(x) = x
    sbox = {i: i for i in range(16)}
    
    print("Testing identity S-Box linear approximations:")
    print("Input_mask Output_mask  Bias")
    print("-" * 30)
    
    for input_mask in range(1, 16):
        for output_mask in range(1, 16):
            bias = calculate_sbox_bias(sbox, input_mask, output_mask)
            if bias > 0:
                print(f"    {input_mask:x}           {output_mask:x}      {bias:.3f}")


def apply_permutation(output_masks):
    """Apply the SPN permutation to output masks from previous round."""
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


def create_identity_trail():
    """Create a valid trail for identity S-Box."""
    print("\nCreating trail for identity S-Box...")
    
    # For identity S-Box, input_mask == output_mask should have bias 0.5 (always true)
    # Let's use input_mask=1, output_mask=1 for first S-Box
    round1 = [(1, 1), (0, 0), (0, 0), (0, 0)]
    print(f"Round 1: {round1}")
    
    # Calculate what round 2 should be
    round1_outputs = [pair[1] for pair in round1]
    round2_inputs = apply_permutation(round1_outputs)
    round2 = [(round2_inputs[i], 0) for i in range(4)]  # No outputs in round 2
    print(f"Round 2: {round2}")
    
    # Rounds 3 and 4 are inactive
    round3 = [(0, 0), (0, 0), (0, 0), (0, 0)]
    round4 = [(0, 0), (0, 0), (0, 0), (0, 0)]
    
    # Convert to approximation string
    all_rounds = round1 + round2 + round3 + round4
    approx_string = ""
    for inp, out in all_rounds:
        approx_string += f"{inp:x}{out:x}"
    
    print(f"Identity trail: {approx_string}")
    return approx_string


if __name__ == "__main__":
    test_identity_sbox()
    create_identity_trail()
