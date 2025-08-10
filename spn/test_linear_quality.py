#!/usr/bin/env python3
"""
Test script for the Linear Approximation Quality Evaluator

This script tests the linear_approximation_quality.py program with various
test cases to ensure it works correctly.
"""

import subprocess
import sys
import os


def run_quality_program(sbox, approximation):
    """Run the linear approximation quality program and return the output."""
    script_path = os.path.join(os.path.dirname(__file__), 'linear_approximation_quality.py')
    
    try:
        result = subprocess.run(
            [sys.executable, script_path, sbox, approximation],
            capture_output=True,
            text=True,
            timeout=30,
            check=False
        )
        
        if result.returncode == 0:
            return float(result.stdout.strip())
        else:
            return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "TIMEOUT"
    except (ValueError, subprocess.SubprocessError) as e:
        return f"ERROR: {e}"


def test_valid_approximation():
    """Test with a valid approximation trail."""
    print("Testing valid approximation trail...")
    
    # Use the default S-Box from the SPN implementation
    sbox = "E4D12FB83A6C5907"
    
    # Create a valid trail with good approximation: Round 4 has (1,7) with bias 0.375
    # Work backwards: Round 3 needs output mask 1 to create input mask 1 in round 4
    approximation = "00000000000000000100000017000000"
    
    result = run_quality_program(sbox, approximation)
    print(f"S-Box: {sbox}")
    print(f"Approximation: {approximation}")
    print(f"Result: {result}")
    print()


def test_invalid_approximation():
    """Test with an invalid approximation trail."""
    print("Testing invalid approximation trail...")
    
    sbox = "E4D12FB83A6C5907"
    
    # Create an invalid approximation (only one S-Box active but with output mask)
    approximation = "17000000000000000000000000000000"
    
    result = run_quality_program(sbox, approximation)
    print(f"S-Box: {sbox}")
    print(f"Approximation: {approximation}")
    print(f"Result: {result}")
    print()


def test_all_inactive():
    """Test with all S-Boxes inactive."""
    print("Testing all S-Boxes inactive...")
    
    sbox = "E4D12FB83A6C5907"
    approximation = "00" * 16  # All S-Boxes inactive
    
    result = run_quality_program(sbox, approximation)
    print(f"S-Box: {sbox}")
    print(f"Approximation: {approximation}")
    print(f"Result: {result}")
    print()


def test_single_active_sbox():
    """Test with a single active S-Box that has good bias."""
    print("Testing single active S-Box with good bias...")
    
    sbox = "E4D12FB83A6C5907"
    
    # Use a known good approximation (1,7) in the last round only
    # This should be valid because it doesn't require propagation
    approximation = "00000000000000000000000017000000"
    
    result = run_quality_program(sbox, approximation)
    print(f"S-Box: {sbox}")
    print(f"Approximation: {approximation}")
    print(f"Result: {result}")
    print()


def test_simple_demonstrations():
    """Test simple cases to demonstrate the program works."""
    print("Testing simple demonstration cases...")
    
    # Test 1: All inactive should give quality 0
    result = run_quality_program("0123456789ABCDEF", "00000000000000000000000000000000")
    print(f"All inactive: {result} (expected: 0.0)")
    
    # Test 2: Invalid trail should give -1
    result = run_quality_program("0123456789ABCDEF", "11000000000000000000000000000000")
    print(f"Invalid trail: {result} (expected: -1)")
    
    # Test 3: Use identity S-Box with trail that only has input masks (no outputs)
    # This should be valid and have quality > 0
    result = run_quality_program("0123456789ABCDEF", "10000000000000000000000000000000")
    print(f"Identity S-Box, input-only: {result}")
    
    # Test 4: Use a custom S-Box designed to have good linear properties
    # Simple S-Box where bit 0 is always flipped: f(x) = x XOR 1
    custom_sbox = "1032547698BADCFE"  # Each nibble XORed with 1
    result = run_quality_program(custom_sbox, "10000000000000000000000000000000")
    print(f"Custom S-Box, input-only: {result}")
    
    print()


def test_error_cases():
    """Test various error cases."""
    print("Testing error cases...")
    
    # Invalid S-Box length
    result = run_quality_program("E4D12F", "00" * 16)
    print(f"Short S-Box result: {result}")
    
    # Invalid approximation length
    result = run_quality_program("E4D12FB83A6C5907", "00" * 10)
    print(f"Short approximation result: {result}")
    
    # Invalid hex characters
    result = run_quality_program("E4D12FB83A6C590G", "00" * 16)
    print(f"Invalid hex in S-Box result: {result}")
    
    print()


def main():
    """Run all tests."""
    print("=== Linear Approximation Quality Evaluator Tests ===\n")
    
    test_valid_approximation()
    test_invalid_approximation()
    test_all_inactive()
    test_single_active_sbox()
    test_simple_demonstrations()
    test_error_cases()
    
    print("=== Tests completed ===")


if __name__ == "__main__":
    main()
