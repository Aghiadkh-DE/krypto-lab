#!/usr/bin/env python3
"""
Debug version of the linear approximation quality evaluator
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


def calculate_sbox_bias(sbox, input_mask, output_mask):
    """Calculate the bias of a linear approximation for a single S-Box."""
    print(f"  Calculating bias for S-Box with masks ({input_mask:x}, {output_mask:x})")
    
    if input_mask == 0 and output_mask == 0:
        print(f"    Inactive S-Box, bias = 1.0")
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
    
    print(f"    count_zero={count_zero}, probability={probability:.3f}, bias={bias:.3f}")
    return bias


def calculate_approximation_quality(sbox, approximations):
    """Calculate the overall quality of the approximation using the Piling-up Lemma."""
    print("Calculating approximation quality:")
    
    active_sboxes = []
    biases = []
    
    # Identify active S-Boxes and calculate their biases
    for i, (input_mask, output_mask) in enumerate(approximations):
        if input_mask != 0 or output_mask != 0:
            print(f"S-Box {i} is active: ({input_mask:x}, {output_mask:x})")
            active_sboxes.append(i)
            bias = calculate_sbox_bias(sbox, input_mask, output_mask)
            biases.append(bias)
        else:
            print(f"S-Box {i} is inactive: ({input_mask:x}, {output_mask:x})")
    
    print(f"Found {len(active_sboxes)} active S-Boxes with biases: {biases}")
    
    if not active_sboxes:
        print("No active S-Boxes, quality = 0.0")
        return 0.0
    
    # Apply Piling-up Lemma
    num_active = len(active_sboxes)
    quality = (2 ** (num_active - 1))
    
    print(f"Base quality from Piling-up Lemma: 2^({num_active}-1) = {quality}")
    
    for i, bias in enumerate(biases):
        quality *= bias
        print(f"After multiplying by bias {i+1} ({bias:.3f}): quality = {quality:.6f}")
    
    print(f"Final quality: {quality}")
    return quality


def main():
    """Main program entry point."""
    if len(sys.argv) != 3:
        print("Usage: python debug_quality.py [S-Box] [Approximation]", file=sys.stderr)
        sys.exit(1)
    
    sbox_string = sys.argv[1]
    approx_string = sys.argv[2]
    
    print(f"S-Box: {sbox_string}")
    print(f"Approximation: {approx_string}")
    
    # Parse inputs
    sbox = parse_sbox(sbox_string)
    approximations = parse_approximation(approx_string)
    
    print(f"Parsed approximations: {approximations}")
    
    # Calculate quality
    quality = calculate_approximation_quality(sbox, approximations)
    print(f"\nResult: {quality}")


if __name__ == "__main__":
    main()
