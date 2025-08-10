def mod_exp(base, exponent, modulus):
    if exponent < 0:
        raise ValueError("Exponent must be non-negative")
    if modulus <= 0:
        raise ValueError("Modulus must be positive")
    
    # Handle edge cases
    if modulus == 1:
        return 0
    if exponent == 0:
        return 1
    
    base = base % modulus
    
    if base == 0:
        return 0
    
    result = 1
    current_base = base
    
    while exponent > 0:
        if exponent & 1:
            result = (result * current_base) % modulus
        
        current_base = (current_base * current_base) % modulus

        exponent >>= 1
    
    return result