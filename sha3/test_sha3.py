"""
Test suite for SHA3-224 implementation.

This module contains comprehensive tests for the SHA3-224 hash function,
including known test vectors and edge cases.
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sha3.sha3_224 import (
    sha3_224_hash, sha3_224_hash_bytes, sha3_pad,
    bytes_to_state, state_to_bytes, keccak_f,
    theta_step, rho_step, pi_step, chi_step, iota_step
)


class TestSHA3Components(unittest.TestCase):
    """Test individual components of the SHA-3 algorithm."""
    
    def test_bytes_to_state_conversion(self):
        """Test conversion between bytes and state matrix."""
        # Test with 200 zero bytes
        zero_bytes = b'\x00' * 200
        state = bytes_to_state(zero_bytes)
        
        # Should be a 5x5 matrix of zeros
        for i in range(5):
            for j in range(5):
                self.assertEqual(state[i][j], 0)
        
        # Convert back to bytes
        converted_bytes = state_to_bytes(state)
        self.assertEqual(zero_bytes, converted_bytes)
    
    def test_bytes_to_state_with_data(self):
        """Test bytes to state conversion with actual data."""
        # Create test data: first 8 bytes = 0x0123456789ABCDEF (little-endian)
        test_bytes = bytearray(200)
        test_bytes[0:8] = b'\xEF\xCD\xAB\x89\x67\x45\x23\x01'  # Little-endian
        
        state = bytes_to_state(bytes(test_bytes))
        
        # First word should be 0x0123456789ABCDEF
        self.assertEqual(state[0][0], 0x0123456789ABCDEF)
        
        # All other words should be 0
        for i in range(5):
            for j in range(5):
                if i == 0 and j == 0:
                    continue
                self.assertEqual(state[i][j], 0)
    
    def test_padding_function(self):
        """Test SHA-3 padding function."""
        rate = 1152  # SHA3-224 rate in bits
        
        # Test empty message
        empty_msg = b''
        padded = sha3_pad(empty_msg, rate)
        self.assertEqual(len(padded) % (rate // 8), 0)
        
        # Test single byte message
        single_byte = b'\x01'
        padded = sha3_pad(single_byte, rate)
        self.assertEqual(len(padded) % (rate // 8), 0)
        
        # Test that padding always adds at least one byte
        for msg_len in range(0, 10):
            msg = b'A' * msg_len
            padded = sha3_pad(msg, rate)
            self.assertGreater(len(padded), len(msg))
    
    def test_keccak_f_permutation(self):
        """Test that Keccak-f permutation is deterministic."""
        # Test with zero state
        zero_state = [[0 for _ in range(5)] for _ in range(5)]
        result1 = keccak_f(zero_state)
        result2 = keccak_f(zero_state)
        
        # Results should be identical
        self.assertEqual(result1, result2)
        
        # Result should be different from input (unless it's a fixed point)
        self.assertNotEqual(result1, zero_state)
    
    def test_step_functions(self):
        """Test individual step functions."""
        # Create a test state with some pattern
        test_state = [[i * 5 + j for j in range(5)] for i in range(5)]
        
        # Test that each step function returns a valid 5x5 matrix
        theta_result = theta_step(test_state)
        rho_result = rho_step(test_state)
        pi_result = pi_step(test_state)
        chi_result = chi_step(test_state)
        iota_result = iota_step(test_state, 0)
        
        for result in [theta_result, rho_result, pi_result, chi_result, iota_result]:
            self.assertEqual(len(result), 5)
            for row in result:
                self.assertEqual(len(row), 5)
                for element in row:
                    self.assertIsInstance(element, int)
                    # Check that values are within 64-bit range
                    self.assertGreaterEqual(element, 0)
                    self.assertLessEqual(element, 0xFFFFFFFFFFFFFFFF)


class TestSHA3KnownVectors(unittest.TestCase):
    """Test SHA3-224 with known test vectors."""
    
    def test_empty_string(self):
        """Test SHA3-224 of empty string."""
        # Known SHA3-224 hash of empty string
        expected = "02C08F43A9FDCC39CB97D5CA256D759B4E4D61B02AD9CF9C21067FA7"
        result = sha3_224_hash("")
        self.assertEqual(result, expected)
    
    def test_single_bit(self):
        """Test SHA3-224 of single bit (0x80)."""
        # Single bit set (0x80 = 10000000 in binary)
        result = sha3_224_hash("80")
        # Check that it produces a valid 224-bit (56 hex char) hash
        self.assertEqual(len(result), 56)
        self.assertTrue(all(c in '0123456789ABCDEF' for c in result))
    
    def test_abc_string(self):
        """Test SHA3-224 of 'abc' string."""
        # Convert "abc" to hex: 616263
        abc_hex = "616263"
        result = sha3_224_hash(abc_hex)
        
        # Check format
        self.assertEqual(len(result), 56)  # 224 bits = 56 hex chars
        self.assertTrue(all(c in '0123456789ABCDEF' for c in result))
    
    def test_longer_message(self):
        """Test SHA3-224 with a longer message."""
        # Test with "abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq"
        long_msg = "abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq"
        hex_msg = long_msg.encode('ascii').hex().upper()
        
        result = sha3_224_hash(hex_msg)
        
        # Check format
        self.assertEqual(len(result), 56)
        self.assertTrue(all(c in '0123456789ABCDEF' for c in result))


class TestSHA3EdgeCases(unittest.TestCase):
    """Test edge cases and error conditions."""
    
    def test_invalid_hex_input(self):
        """Test with invalid hexadecimal input."""
        with self.assertRaises(ValueError):
            sha3_224_hash("ZZ")  # Invalid hex characters
        
        with self.assertRaises(ValueError):
            sha3_224_hash("123")  # Odd length
    
    def test_hex_input_variations(self):
        """Test with various hex input formats."""
        # Test with spaces
        result1 = sha3_224_hash("61 62 63")
        result2 = sha3_224_hash("616263")
        self.assertEqual(result1, result2)
        
        # Test with newlines and tabs
        result3 = sha3_224_hash("61\n62\t63")
        self.assertEqual(result3, result2)
    
    def test_bytes_interface(self):
        """Test the bytes interface."""
        test_bytes = b"abc"
        result1 = sha3_224_hash_bytes(test_bytes)
        result2 = sha3_224_hash("616263")  # "abc" in hex
        self.assertEqual(result1, result2)


def run_tests():
    """Run all tests."""
    print("Running SHA3-224 Test Suite")
    print("=" * 50)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestSHA3Components))
    suite.addTests(loader.loadTestsFromTestCase(TestSHA3KnownVectors))
    suite.addTests(loader.loadTestsFromTestCase(TestSHA3EdgeCases))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("All tests passed successfully!")
    else:
        print(f"Tests failed: {len(result.failures)} failures, {len(result.errors)} errors")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
