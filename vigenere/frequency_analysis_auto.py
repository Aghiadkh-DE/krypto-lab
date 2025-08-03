import argparse
import os
import sys
from collections import Counter


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from util.file_util import read_file, write_file

# German letter frequencies (approximate)
GERMAN_FREQUENCIES = {
    'E': 17.4, 'N': 9.78, 'I': 7.55, 'R': 7.00, 'S': 7.27, 'A': 6.51,
    'T': 6.15, 'D': 5.08, 'H': 4.76, 'U': 4.35, 'L': 3.44, 'C': 3.06,
    'G': 3.01, 'M': 2.53, 'O': 2.51, 'B': 1.89, 'W': 1.89, 'F': 1.66,
    'K': 1.21, 'Z': 1.13, 'P': 0.79, 'V': 0.67, 'J': 0.27, 'Y': 0.04,
    'X': 0.03, 'Q': 0.02
}

def sanitize_text(text: str) -> str:
    return ''.join(ch for ch in text.upper() if ch.isalpha() and 'A' <= ch <= 'Z')

def index_of_coincidence(text: str) -> float:
    # Convert text to uppercase and filter out non-alphabetic characters
    text = sanitize_text(text)
    n = len(text)

    if n == 0:
        return 0.0

    # Get absolute frequencies of each letter
    frequencies = Counter(text).values()

    # Calculate the index of coincidence, non-existing letters are ignored
    return sum(frequency * (frequency - 1) for frequency in frequencies) / (n * (n - 1))


def determine_key_length(cipher_text: str, max_key_length: int = 100) -> list[tuple[int, float]]:
    # Clean the ciphertext
    clean_text = sanitize_text(cipher_text)
    
    results = []
    
    for key_length in range(1, min(max_key_length + 1, len(clean_text) + 1)):
        # Split text into subtexts based on key length
        subtexts = [''] * key_length
        
        for i, char in enumerate(clean_text):
            subtexts[i % key_length] += char
        
        # Calculate IoC for each subtext
        ioc_values = []
        for subtext in subtexts:
            if len(subtext) > 1:  # Need at least 2 characters for IoC calculation
                ioc = index_of_coincidence(subtext)
                ioc_values.append(ioc)
        
        # Calculate average IoC for this key length
        if ioc_values:
            avg_ioc = sum(ioc_values) / len(ioc_values)
            results.append((key_length, avg_ioc))
    
    # Sort by average IoC in descending order
    results.sort(key=lambda x: x[1], reverse=True)
    return results


def find_most_likely_key_length(cipher_text: str, max_key_length: int = 100) -> int:
    results = determine_key_length(cipher_text, max_key_length)
    
    if not results:
        return 1
    
    # IC_german is around 0.076 for German texts
    threshold = 0.076
    
    # Get all key lengths with high IoC
    high_ioc_keys = [(key_length, avg_ioc) for key_length, avg_ioc in results if avg_ioc > threshold]
    
    if not high_ioc_keys:
        # If no high IoC found, return the one with highest IoC
        return results[0][0]
    
    # Find the most likely original key length by looking for the smallest key that has multiple high IoC multiples
    candidate_scores = {}
    
    for key_length, avg_ioc in high_ioc_keys:
        # Count how many multiples of this key length also have high IoC
        multiples_count = 0
        for other_key, _ in high_ioc_keys:
            if other_key > key_length and other_key % key_length == 0:
                multiples_count += 1

        score = avg_ioc + (multiples_count * 0.01)  # Bias for having multiples
        candidate_scores[key_length] = score
    
    # Return the key length with the highest score
    # In case of ties, prefer the smallest key length
    best_key = min(candidate_scores.keys(), key=lambda k: (-candidate_scores[k], k))
    return best_key


def chi_squared_test(observed_frequencies: dict, expected_frequencies: dict, text_length: int) -> float:
    chi_squared = 0.0
    
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        observed = observed_frequencies.get(letter, 0)
        expected = (expected_frequencies.get(letter, 0) / 100.0) * text_length
        
        if expected > 0:
            chi_squared += ((observed - expected) ** 2) / expected
    
    return chi_squared


def find_best_shift_for_subtext(subtext: str) -> int:
    if len(subtext) == 0:
        return 0
    
    best_shift = 0
    best_score = float('inf')
    
    for shift in range(26):
        # Decrypt the subtext with this shift
        decrypted = ''
        for char in subtext:
            if char.isalpha():
                shifted_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
                decrypted += shifted_char
        
        # Calculate frequency distribution
        freq_count = Counter(decrypted)
        
        # Calculate chi-squared score against German frequencies
        chi_squared = chi_squared_test(freq_count, GERMAN_FREQUENCIES, len(decrypted))
        
        if chi_squared < best_score:
            best_score = chi_squared
            best_shift = shift
    
    return best_shift


def determine_vigenere_key(cipher_text: str, key_length: int | None = None) -> str:
    # Clean the ciphertext
    clean_text = sanitize_text(cipher_text)
    
    if key_length is None:
        key_length = find_most_likely_key_length(cipher_text)
    
    # Split text into subtexts based on key length
    subtexts = [''] * key_length
    
    for i, char in enumerate(clean_text):
        subtexts[i % key_length] += char
    
    # Find the best shift for each subtext
    key_chars = []
    for subtext in subtexts:
        if len(subtext) > 0:
            shift = find_best_shift_for_subtext(subtext)
            key_char = chr(shift + ord('A'))
            key_chars.append(key_char)
        else:
            key_chars.append('A')  # Default to 'A' if subtext is empty
    
    return ''.join(key_chars)


def analyze_vigenere_cipher(cipher_text: str, max_key_length: int = 20) -> tuple[str, int]:
    key_length = find_most_likely_key_length(cipher_text, max_key_length)

    key = determine_vigenere_key(cipher_text, key_length)
    
    return key, key_length


def decrypt_vigenere(text: str, key: str) -> str:
    plaintext = []
    key_length = len(key)

    base, i = ord('A'), 0
    for c in text:
        if c.isalpha() and ord('A') <= ord(c) <= ord('Z'):
            shift = ord(key[i % key_length].upper()) - base
            decrypted_char = chr((ord(c.upper()) - base - shift + 26) % 26 + base)
            plaintext.append(decrypted_char)
            i += 1
        else:
            plaintext.append(c)

    return ''.join(plaintext)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Vigenère Cipher Frequency Analysis Tool",
        epilog="Example usage: python frequency_analysis_auto.py -i input.txt -o output.txt"
    )

    parser.add_argument('-i', '--input', type=str, required=True, help='Input ciphertext file')
    parser.add_argument('-o', '--output', type=str, required=True, help='Output results file')

    args = parser.parse_args()

    if not args.input or not args.output:
        print("Error: Input and output files are required.")
        exit(1)

    try:
        crypto_text = read_file(args.input)
        recovered_key, recovered_key_length = analyze_vigenere_cipher(crypto_text, max_key_length=20)
        print(f"Recovered Key: {recovered_key}")
        print(f"Key Length: {recovered_key_length}")

        write_file(args.output, decrypt_vigenere(crypto_text, recovered_key))


    except FileNotFoundError:
        print(f"Error: Input file '{args.input}' not found.")
        exit(1)