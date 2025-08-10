#!/usr/bin/env python3
"""
Calculate correct permutation for output mask 2
"""

def apply_permutation(output_masks):
    """Apply the SPN permutation to output masks from previous round."""
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


# Test output mask 2 from first S-Box
print("Testing output mask 2 from first S-Box:")
round1_outputs = [2, 0, 0, 0]
round2_inputs = apply_permutation(round1_outputs)
print(f"Round 2 input masks: {round2_inputs}")

# Create the trail
round1 = [(1, 2), (0, 0), (0, 0), (0, 0)]
round2 = [(round2_inputs[i], 0) for i in range(4)]
round3 = [(0, 0), (0, 0), (0, 0), (0, 0)]
round4 = [(0, 0), (0, 0), (0, 0), (0, 0)]

all_rounds = round1 + round2 + round3 + round4
approx_string = ""
for inp, out in all_rounds:
    approx_string += f"{inp:x}{out:x}"

print(f"Correct trail: {approx_string}")
