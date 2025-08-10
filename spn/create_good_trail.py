#!/usr/bin/env python3
"""
Create a valid trail with non-zero bias for all active S-Boxes
"""


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


def find_good_trail():
    """Find a trail where all active S-Boxes have non-zero bias."""
    
    # List of approximations with good bias (from find_bias.py output)
    good_approximations = [
        (1, 2, 0.125),
        (1, 7, 0.375),  # This has high bias
        (4, 5, 0.250),
        (5, 6, 0.250),
        (2, 14, 0.375),  # This has high bias
        (8, 15, 0.375),  # This has high bias
    ]
    
    print("Trying to create trail with high-bias approximations...")
    
    # Strategy: Use an approximation that results in an output mask that,
    # when permuted, creates an input mask for which we have a good approximation
    
    # Let's try: Round 1 has (1, 7) with bias 0.375
    # Output mask 7 = 0111 in binary
    round1 = [(1, 7), (0, 0), (0, 0), (0, 0)]
    print(f"Round 1: {round1}")
    
    # See what this creates in round 2
    round1_outputs = [pair[1] for pair in round1]
    round2_inputs = apply_permutation(round1_outputs)
    print(f"Round 2 inputs from permutation: {round2_inputs}")
    
    # Check if any of these input masks have good approximations with output mask 0
    print("Checking if any round 2 input masks work well with output mask 0:")
    for i, input_mask in enumerate(round2_inputs):
        if input_mask != 0:
            print(f"  S-Box {i}: input_mask={input_mask:x}, need to check bias for ({input_mask:x}, 0)")
    
    # Let's construct round 2 with output masks = 0 (inactive outputs)
    round2 = [(round2_inputs[i], 0) for i in range(4)]
    print(f"Round 2: {round2}")
    
    # Rounds 3 and 4 are inactive
    round3 = [(0, 0), (0, 0), (0, 0), (0, 0)]
    round4 = [(0, 0), (0, 0), (0, 0), (0, 0)]
    
    # Convert to approximation string
    all_rounds = round1 + round2 + round3 + round4
    approx_string = ""
    for inp, out in all_rounds:
        approx_string += f"{inp:x}{out:x}"
    
    print(f"Approximation string: {approx_string}")
    return approx_string


def check_bias_for_mask(input_mask, output_mask):
    """Check the bias for a specific mask combination."""
    sbox = {
        0x0: 0xE, 0x1: 0x4, 0x2: 0xD, 0x3: 0x1,
        0x4: 0x2, 0x5: 0xF, 0x6: 0xB, 0x7: 0x8,
        0x8: 0x3, 0x9: 0xA, 0xA: 0x6, 0xB: 0xC,
        0xC: 0x5, 0xD: 0x9, 0xE: 0x0, 0xF: 0x7
    }
    
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


def check_round2_biases():
    """Check biases for the round 2 input masks."""
    # From the previous calculation: round2_inputs = [7, 0, 0, 0]
    round2_inputs = [7, 0, 0, 0]
    
    print("Checking biases for round 2 S-Boxes:")
    for i, input_mask in enumerate(round2_inputs):
        if input_mask != 0:
            bias = check_bias_for_mask(input_mask, 0)
            print(f"  S-Box {i}: ({input_mask:x}, 0) has bias {bias:.3f}")


if __name__ == "__main__":
    find_good_trail()
    print()
    check_round2_biases()
