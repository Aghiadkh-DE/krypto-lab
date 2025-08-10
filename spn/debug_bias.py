#!/usr/bin/env python3
"""
Debug bias calculation
"""

def calculate_sbox_bias(sbox, input_mask, output_mask):
    """
    Calculate the bias of a linear approximation for a single S-Box.
    
    Returns the absolute bias |ε(U_a ⊕ V_b)|.
    """
    print(f"Calculating bias for input_mask={input_mask:x}, output_mask={output_mask:x}")
    
    if input_mask == 0 and output_mask == 0:
        print("Both masks are 0 - inactive S-Box")
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
        linear_val = u_a ^ v_b
        if linear_val == 0:
            count_zero += 1
            
        if u < 4:  # Print first few for debugging
            print(f"  u={u:x}, v={v:x}, u_a={u_a}, v_b={v_b}, u_a⊕v_b={linear_val}")
    
    # Calculate probability and bias
    probability = count_zero / 16
    bias = abs(probability - 0.5)
    
    print(f"  count_zero={count_zero}, probability={probability}, bias={bias}")
    return bias


def test_bias():
    # S-Box from the SPN implementation
    sbox = {
        0x0: 0xE, 0x1: 0x4, 0x2: 0xD, 0x3: 0x1,
        0x4: 0x2, 0x5: 0xF, 0x6: 0xB, 0x7: 0x8,
        0x8: 0x3, 0x9: 0xA, 0xA: 0x6, 0xB: 0xC,
        0xC: 0x5, 0xD: 0x9, 0xE: 0x0, 0xF: 0x7
    }
    
    print("Testing bias calculation:")
    
    # Test case 1: input_mask=0, output_mask=1
    bias1 = calculate_sbox_bias(sbox, 0, 1)
    print(f"Bias for (0,1): {bias1}\n")
    
    # Test case 2: input_mask=1, output_mask=0
    bias2 = calculate_sbox_bias(sbox, 1, 0)
    print(f"Bias for (1,0): {bias2}\n")
    
    # Test case 3: input_mask=1, output_mask=1
    bias3 = calculate_sbox_bias(sbox, 1, 1)
    print(f"Bias for (1,1): {bias3}\n")


if __name__ == "__main__":
    test_bias()
