#!/usr/bin/env python3
"""
Create an S-Box with known good linear properties and test it
"""


def create_simple_sbox():
    """Create a simple S-Box with predictable linear properties."""
    # S-Box where output bit 0 = input bit 0 XOR input bit 1
    # This should give good bias for certain approximations
    sbox = {}
    for i in range(16):
        # Extract input bits
        bit0 = i & 1
        bit1 = (i >> 1) & 1
        bit2 = (i >> 2) & 1
        bit3 = (i >> 3) & 1
        
        # Output bit 0 = input bit 0 XOR input bit 1
        out_bit0 = bit0 ^ bit1
        # Other output bits = corresponding input bits
        out_bit1 = bit1
        out_bit2 = bit2
        out_bit3 = bit3
        
        output = out_bit0 | (out_bit1 << 1) | (out_bit2 << 2) | (out_bit3 << 3)
        sbox[i] = output
    
    # Convert to hex string
    sbox_string = ""
    for i in range(16):
        sbox_string += f"{sbox[i]:X}"
    
    return sbox_string, sbox


def test_sbox_bias(sbox, input_mask, output_mask):
    """Test the bias of a specific approximation."""
    count_zero = 0
    
    for u in range(16):
        v = sbox[u]
        
        # Calculate U_a
        u_a = 0
        for bit_pos in range(4):
            if input_mask & (1 << bit_pos):
                u_a ^= (u >> bit_pos) & 1
        
        # Calculate V_b
        v_b = 0
        for bit_pos in range(4):
            if output_mask & (1 << bit_pos):
                v_b ^= (v >> bit_pos) & 1
        
        if u_a ^ v_b == 0:
            count_zero += 1
    
    probability = count_zero / 16
    bias = abs(probability - 0.5)
    return bias


def main():
    """Test the custom S-Box."""
    sbox_string, sbox_dict = create_simple_sbox()
    print(f"Custom S-Box: {sbox_string}")
    
    # Test approximation (3, 1): input bits 0,1 XOR output bit 0
    # Since output bit 0 = input bit 0 XOR input bit 1,
    # we have: (input bit 0 XOR input bit 1) XOR (input bit 0 XOR input bit 1) = 0
    # This should always be 0, giving bias 0.5
    
    bias = test_sbox_bias(sbox_dict, 3, 1)  # input mask 3 = bits 0,1; output mask 1 = bit 0
    print(f"Bias for approximation (3, 1): {bias}")
    
    # Test this with the quality program manually
    import subprocess
    import sys
    import os
    
    script_path = os.path.join(os.path.dirname(__file__), 'linear_approximation_quality.py')
    
    try:
        result = subprocess.run(
            [sys.executable, script_path, sbox_string, "31000000000000000000000000000000"],
            capture_output=True,
            text=True,
            timeout=30,
            check=False
        )
        
        if result.returncode == 0:
            quality = float(result.stdout.strip())
            print(f"Quality for single approximation (3,1): {quality}")
            
            if quality > 0:
                print(f"Got positive quality: {quality}")
            else:
                print("Quality is 0 (may be expected due to trail validation)")
        else:
            print(f"Program returned error or -1: {result.stdout.strip()}")
            
    except Exception as e:
        print(f"Error running program: {e}")


if __name__ == "__main__":
    main()
