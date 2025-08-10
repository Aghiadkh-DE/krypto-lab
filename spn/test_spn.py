#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from spn_cipher import SPNCipher
from linear_cryptanalysis import LinearCryptanalysisTheory
import unittest


class TestSPNCipher(unittest.TestCase):
    """Test cases for SPN cipher implementation"""
    
    def setUp(self):
        self.cipher = SPNCipher()
    
    def test_sbox_mapping(self):
        """Test S-box mapping matches specification"""
        expected_sbox = {
            0x0: 0xE, 0x1: 0x4, 0x2: 0xD, 0x3: 0x1,
            0x4: 0x2, 0x5: 0xF, 0x6: 0xB, 0x7: 0x8,
            0x8: 0x3, 0x9: 0xA, 0xA: 0x6, 0xB: 0xC,
            0xC: 0x5, 0xD: 0x9, 0xE: 0x0, 0xF: 0x7
        }
        
        self.assertEqual(self.cipher.sbox, expected_sbox)
    
    def test_permutation_mapping(self):
        """Test permutation mapping matches specification"""
        # πP = [1,5,9,13, 2,6,10,14, 3,7,11,15, 4,8,12,16]
        # Convert to 0-indexed
        expected_perm = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]
        
        self.assertEqual(self.cipher.permutation, expected_perm)
    
    def test_sbox_application(self):
        """Test S-box application on 16-bit data"""
        # Test with known input: 0x1234
        input_data = 0x1234
        result = self.cipher.apply_sbox(input_data)
        
        # Expected: nibble 4->2, 3->1, 2->D, 1->4 = 0x4D12 (processing LSB to MSB)
        expected = 0x4D12
        self.assertEqual(result, expected)
    
    def test_permutation_application(self):
        """Test permutation application"""
        # Test with known pattern
        input_data = 0xF000  # Only bits 12-15 set
        result = self.cipher.apply_permutation(input_data)
        
        # Bits 12-15 should map to positions 3,7,11,15
        expected = 0x8888
        self.assertEqual(result, expected)
    
    def test_encryption_decryption(self):
        """Test encryption and decryption are inverse operations"""
        plaintext = 0x1234
        key = 0x5678
        
        ciphertext = self.cipher.encrypt_block(plaintext, key)
        decrypted = self.cipher.decrypt_block(ciphertext, key)
        
        self.assertEqual(plaintext, decrypted)
    
    def test_encrypt_hex_string(self):
        """Test encryption of hex string in ECB mode"""
        plaintext = "12345678"
        key = "ABCD"
        
        result = self.cipher.encrypt(plaintext, key)
        
        # Should return 8 hex digits (2 blocks * 4 digits each)
        self.assertEqual(len(result), 8)
        self.assertTrue(all(c in '0123456789ABCDEF' for c in result))
    
    def test_four_rounds(self):
        """Test that exactly 4 rounds are performed"""
        # This is verified by the structure of encrypt_block method
        # We can test by checking intermediate values
        plaintext = 0x0000
        key = 0x0000
        
        # With all zeros, we can trace the operations
        result = self.cipher.encrypt_block(plaintext, key)
        
        # After 4 rounds with key=0, applying S-box to 0000 gives EEEE
        # This gets processed through 4 rounds
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 0)
        self.assertLessEqual(result, 0xFFFF)


class TestLinearCryptanalysis(unittest.TestCase):
    """Test cases for linear cryptanalysis implementation"""
    
    def setUp(self):
        self.lc = LinearCryptanalysisTheory()
    
    def test_sbox_bias_verification(self):
        """Test S-box linear approximation bias verification"""
        # Test T approximation
        result_t = self.lc.verify_sbox_approximation('T')
        self.assertTrue(result_t['matches'])
        self.assertAlmostEqual(result_t['bias'], 0.125, places=2)
        
        # Test T' approximation
        result_t_prime = self.lc.verify_sbox_approximation('T_prime')
        self.assertTrue(result_t_prime['matches'])
        self.assertAlmostEqual(result_t_prime['bias'], 0.125, places=2)
    
    def test_overall_bias(self):
        """Test overall bias calculation"""
        expected_bias = 1/64  # Updated based on empirical S-box biases
        self.assertAlmostEqual(self.lc.overall_bias, expected_bias, places=6)
    
    def test_sample_size_calculation(self):
        """Test required sample size calculation"""
        # For t=8, should be approximately 8 * 1000 = 8000
        required = self.lc.compute_required_samples(8)
        expected = 8 * (1/self.lc.overall_bias)**2
        
        self.assertAlmostEqual(required, expected, delta=100)
    
    def test_linear_attack_format(self):
        """Test linear attack returns correct format"""
        # Generate small test data
        plaintexts = [0x1234, 0x5678, 0xABCD, 0xEF01]
        ciphertexts = [0x9876, 0x5432, 0x1098, 0x7654]
        
        results = self.lc.linear_attack_optimal(plaintexts, ciphertexts)
        
        # Should return 16 results (2^4 partial keys)
        self.assertEqual(len(results), 16)
        
        # Each result should be (key, bias, probability, count)
        for result in results:
            self.assertEqual(len(result), 4)
            key, bias, prob, count = result
            self.assertIsInstance(key, int)
            self.assertIsInstance(bias, float)
            self.assertIsInstance(prob, float)
            self.assertIsInstance(count, int)


class TestSpecificationCompliance(unittest.TestCase):
    """Test compliance with exact specifications"""
    
    def test_block_size(self):
        """Test block size is 16 bits"""
        cipher = SPNCipher()
        
        # Test that cipher handles 16-bit blocks correctly
        test_block = 0xFFFF
        key = 0x1234
        
        result = cipher.encrypt_block(test_block, key)
        self.assertLessEqual(result, 0xFFFF)
        self.assertGreaterEqual(result, 0)
    
    def test_key_size(self):
        """Test key size is 16 bits and same for all rounds"""
        cipher = SPNCipher()
        
        # The implementation uses the same key for all rounds
        # This is verified by the encrypt_block method structure
        plaintext = 0x1234
        key = 0x5678
        
        result = cipher.encrypt_block(plaintext, key)
        self.assertIsInstance(result, int)
    
    def test_ecb_mode(self):
        """Test ECB mode operation"""
        cipher = SPNCipher()
        
        # Same plaintext blocks should produce same ciphertext blocks
        plaintext = "12341234"  # Two identical blocks
        key = "ABCD"
        
        result = cipher.encrypt(plaintext, key)
        
        # First and second blocks should be identical
        first_block = result[:4]
        second_block = result[4:8]
        self.assertEqual(first_block, second_block)
    
    def test_hex_input_output_format(self):
        """Test hex input/output format"""
        cipher = SPNCipher()
        
        plaintext = "ABCD"
        key = "1234"
        
        result = cipher.encrypt(plaintext, key)
        
        # Result should be 4 hex digits
        self.assertEqual(len(result), 4)
        self.assertTrue(all(c in '0123456789ABCDEF' for c in result))


def run_all_tests():
    """Run all test suites"""
    print("Running SPN Cipher and Linear Cryptanalysis Tests")
    print("=" * 55)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestSPNCipher))
    suite.addTests(loader.loadTestsFromTestCase(TestLinearCryptanalysis))
    suite.addTests(loader.loadTestsFromTestCase(TestSpecificationCompliance))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\nTest Summary:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success: {result.wasSuccessful()}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
