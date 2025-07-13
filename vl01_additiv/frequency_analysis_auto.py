"""
Frequency Analysis Module for Automatic Decryption

This module implements frequency analysis to automatically decrypt German texts
that have been encrypted using additive ciphers (Caesar cipher). The method
is based on the fact that letters do not appear with equal frequency in natural
languages, with 'E' being the most common letter in German.

The module supports:
- Automatic key detection through frequency analysis
- Decryption of German texts
- Command-line interface for file-based operations
- Ignoring special German characters (Ä, Ö, Ü, ß)

Author: Aghiad Khertabeel
Date: July 2025
"""

import argparse
from collections import Counter
from typing import Dict, Tuple
import sys
import os


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import additive_cipher
from util.file_util import read_file, write_file


def count_letter_frequencies(text: str) -> Dict[str, int]:
    """
    Count the frequency of each letter in the text.
    
    Only counts uppercase letters A-Z, ignoring special German characters
    (Ä, Ö, Ü, ß) and non-alphabetic characters.
    
    Args:
        text (str): The text to analyze
        
    Returns:
        Dict[str, int]: Dictionary mapping letters to their frequencies
    """
    # Convert to uppercase and filter only A-Z letters
    filtered_text = ''.join(char for char in text.upper() if char.isalpha() and 'A' <= char <= 'Z')
    
    return dict(Counter(filtered_text))


def get_most_frequent_letter(text: str) -> str:
    """
    Find the most frequent letter in the text.
    
    Args:
        text (str): The text to analyze
        
    Returns:
        str: The most frequent letter (A-Z)
        
    Raises:
        ValueError: If no valid letters are found in the text
    """
    frequencies = count_letter_frequencies(text)
    
    if not frequencies:
        raise ValueError("No valid letters found in the text")
    
    # Find the letter with maximum frequency
    most_frequent_letter = max(frequencies.keys(), key=lambda k: frequencies[k])
    return most_frequent_letter


def calculate_key_from_frequency(most_frequent_letter: str, expected_letter: str = 'E') -> int:
    """
    Calculate the cipher key based on frequency analysis.
    
    Assumes that the most frequent letter in the ciphertext corresponds
    to the expected most frequent letter in German (default: 'E').
    
    Args:
        most_frequent_letter (str): The most frequent letter in ciphertext
        expected_letter (str): The expected most frequent letter (default: 'E')
        
    Returns:
        int: The calculated key (0-25)
    """
    # Calculate the shift from expected letter to most frequent letter
    key = (ord(most_frequent_letter) - ord(expected_letter)) % 26
    return key


def analyze_and_decrypt(ciphertext: str) -> Tuple[int, str]:
    """
    Perform frequency analysis and decrypt the text automatically.
    
    Args:
        ciphertext (str): The encrypted text to decrypt
        
    Returns:
        Tuple[int, str]: A tuple containing (key, decrypted_text)
        
    Raises:
        ValueError: If no valid letters are found in the text
    """
    # Find the most frequent letter
    most_frequent = get_most_frequent_letter(ciphertext)
    
    # Calculate the key assuming 'E' is the most frequent letter in German
    key = calculate_key_from_frequency(most_frequent, 'E')
    
    # Decrypt the text using the calculated key
    decrypted_text = additive_cipher.decipher(ciphertext, key)
    
    return key, decrypted_text


def print_frequency_statistics(text: str) -> None:
    """
    Print frequency statistics for the text.
    
    Args:
        text (str): The text to analyze
    """
    frequencies = count_letter_frequencies(text)
    total_letters = sum(frequencies.values())
    
    if total_letters == 0:
        print("No valid letters found in the text.")
        return
    
    print("Letter frequency analysis:")
    print("-" * 40)
    
    # Sort by frequency (descending)
    sorted_frequencies = sorted(frequencies.items(), 
                               key=lambda x: x[1], reverse=True)
    
    for letter, count in sorted_frequencies[:10]:  # Show top 10
        percentage = (count / total_letters) * 100
        print(f"{letter}: {count:3d} ({percentage:5.1f}%)")
    
    print(f"\nTotal letters analyzed: {total_letters}")
    print(f"Most frequent letter: {sorted_frequencies[0][0]}")


def main():
    """
    Command-line interface for automatic frequency analysis decryption.
    
    Usage:
        python frequency_analysis_auto.py input.txt output.txt
    
    Arguments:
        input.txt: Path to the encrypted text file
        output.txt: Path to save the decrypted text
    
    The program will:
    1. Read the encrypted text from the input file
    2. Perform frequency analysis to determine the key
    3. Decrypt the text using the calculated key
    4. Save the decrypted text to the output file
    5. Print the key to standard output
    """
    parser = argparse.ArgumentParser(
        description="Automatic decryption of German texts using frequency analysis",
        epilog="Example: python frequency_analysis_auto.py encrypted.txt decrypted.txt"
    )
    
    parser.add_argument("input", type=str, 
                       help="Path to the input encrypted text file")
    parser.add_argument("output", type=str, 
                       help="Path to the output decrypted text file")
    parser.add_argument("-v", "--verbose", action="store_true",
                       help="Show detailed frequency statistics")
    
    args = parser.parse_args()
    
    try:
        ciphertext = read_file(args.input)
        
        if args.verbose:
            print("Analyzing frequency distribution...")
            print_frequency_statistics(ciphertext)
            print()
        
        key, decrypted_text = analyze_and_decrypt(ciphertext)
        
        write_file(args.output, decrypted_text)
        
        print(f"Detected key: {key}")
        
        if args.verbose:
            print(f"Decrypted text saved to: {args.output}")
            print("\nFirst 200 characters of decrypted text:")
            print(decrypted_text[:200] + "..." if len(decrypted_text) > 200 else decrypted_text)
        
    except FileNotFoundError:
        print(f"Error: Input file '{args.input}' not found.")
        exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)
    except (IOError, OSError) as e:
        print(f"File I/O error: {e}")
        exit(1)


if __name__ == "__main__":
    main()
