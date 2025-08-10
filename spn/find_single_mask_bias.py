#!/usr/bin/env python3
"""
Find input-only approximations with non-zero bias
"""

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


def find_input_only_biases():
    """Find approximations with input mask only that have non-zero bias."""
    print("Input-only approximations with non-zero bias:")
    print("Input_mask  Bias")
    print("-" * 20)
    
    for input_mask in range(1, 16):
        bias = check_bias_for_mask(input_mask, 0)
        if bias > 0:
            print(f"    {input_mask:x}       {bias:.3f}")


def find_output_only_biases():
    """Find approximations with output mask only that have non-zero bias."""
    print("Output-only approximations with non-zero bias:")
    print("Output_mask  Bias")
    print("-" * 20)
    
    for output_mask in range(1, 16):
        bias = check_bias_for_mask(0, output_mask)
        if bias > 0:
            print(f"    {output_mask:x}        {bias:.3f}")


if __name__ == "__main__":
    find_input_only_biases()
    print()
    find_output_only_biases()
