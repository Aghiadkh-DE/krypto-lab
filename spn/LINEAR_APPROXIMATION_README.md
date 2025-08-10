# Linear Approximation Quality Evaluator for SPN

This program evaluates the quality of a given linear approximation trail for a 4-round Substitution-Permutation Network (SPN) cipher, following the specifications provided in the documentation.

## Program Overview

The program implements the complete linear cryptanalysis evaluation process:

1. **Trail Validation**: Verifies that the approximation trail is consistent across rounds through the permutation layer
2. **Bias Calculation**: Computes the bias of each active S-Box linear approximation
3. **Quality Computation**: Uses the Piling-up Lemma to calculate the overall trail quality

## Usage

```bash
python linear_approximation_quality.py [S-Box] [Approximation]
```

### Arguments

- **S-Box**: A string of 16 hexadecimal characters representing the S-Box lookup table
  - Example: `E4D12FB83A6C5907`
  - Character at position `i` represents the output for input `i`

- **Approximation**: A string of 32 hexadecimal characters encoding the linear approximation trail
  - Format: 16 pairs of hex digits `(input_mask, output_mask)` for each S-Box
  - Order: `S₁¹, S₂¹, S₃¹, S₄¹, S₁², S₂², S₃², S₄², S₁³, S₂³, S₃³, S₄³, S₁⁴, S₂⁴, S₃⁴, S₄⁴`
  - `00` indicates an inactive S-Box

### Output

- **Positive number**: The calculated quality of the approximation trail
- **-1**: The approximation trail is invalid
- **0**: The trail is valid but has zero quality (one or more S-Boxes have zero bias)

## SPN Architecture

The program evaluates trails for a 4-round SPN with the following specifications:

- **Block size**: 16 bits (4 S-Boxes × 4 bits each)
- **S-Box**: 4×4-bit substitution boxes (configurable via command line)
- **Permutation**: Fixed bit permutation π_ρ mapping positions:
  ```
  [1,5,9,13, 2,6,10,14, 3,7,11,15, 4,8,12,16]
  ```
- **Rounds**: 4 rounds total
- **Keys**: Round keys are ignored for linear approximation evaluation

## Algorithm Details

### Trail Validation

For rounds 2, 3, and 4, the program validates that:
```
Input_masks[round] = Permutation(Output_masks[round-1])
```

### Bias Calculation

For each active S-Box with masks `(a, b)`:
1. Calculate `U_a ⊕ V_b` for all 16 input values
2. Count occurrences where the result equals 0
3. Compute bias as `|Pr[U_a ⊕ V_b = 0] - 0.5|`

### Quality Computation

Using the Piling-up Lemma:
```
Quality = 2^(|S|-1) × ∏(T_S)
```
where `|S|` is the number of active S-Boxes and `T_S` is the bias of S-Box `S`.

## Examples

### Valid Trail with Zero Quality
```bash
python linear_approximation_quality.py E4D12FB83A6C5907 01000000100000000000000000000000
# Output: 0.0
```

### Invalid Trail
```bash
python linear_approximation_quality.py E4D12FB83A6C5907 17000000000000000000000000000000
# Output: -1
```

### All Inactive S-Boxes
```bash
python linear_approximation_quality.py E4D12FB83A6C5907 00000000000000000000000000000000
# Output: 0.0
```

## Implementation Notes

### Why Many Trails Have Zero Quality

The program correctly identifies that many linear approximation trails have zero quality. This occurs when:

1. **Single-mask approximations**: S-Boxes with only input mask OR only output mask (but not both) always have bias 0
2. **Well-designed S-Boxes**: Cryptographically strong S-Boxes are designed to resist linear cryptanalysis

This is not a bug but reflects the mathematical reality of linear cryptanalysis - finding useful approximations requires careful analysis of the S-Box structure.

### Trail Construction

To create valid trails with non-zero quality:

1. Ensure all active S-Boxes have both input and output masks non-zero
2. Verify consistency through the permutation layer
3. Check that the resulting S-Box approximations have non-zero bias

## Testing

Run the test suite to verify program functionality:

```bash
python test_linear_quality.py
```

The test suite validates:
- Trail validation logic
- Bias calculation accuracy  
- Quality computation using Piling-up Lemma
- Error handling for invalid inputs

## Files

- `linear_approximation_quality.py`: Main program
- `test_linear_quality.py`: Comprehensive test suite
- `debug_quality.py`: Debug version with detailed output
- `find_bias.py`: Utility to find approximations with non-zero bias
- Various other utility scripts for S-Box analysis

## Mathematical Background

This implementation follows standard linear cryptanalysis theory:

1. **Linear Approximation**: `a·x ⊕ b·S(x) = 0` with probability `½ + ε`
2. **Bias**: `ε = |Pr[approximation holds] - ½|`
3. **Piling-up Lemma**: For independent approximations with biases `ε₁, ε₂, ...`, the combined bias is `2^(n-1) × ∏εᵢ`

The program correctly implements these concepts for evaluating SPN linear approximation trails.
