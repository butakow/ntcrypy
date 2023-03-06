"""
Nic Butakow
2 March 2023
Algorithms in number theory.
"""

def lbolt_coeffs(integer_0, integer_1):
    """The greatest common divisor of a pair of integers and their Bezout coefficients. I store
    Bezout coefficients individually to avoid iterating over a pair of integers, which in my
    opinion would make this code look significantly prettier but be significantly sillier."""
    swap = False
    if integer_0 < integer_1:
        swap = True
        (integer_0, integer_1) = (integer_1, integer_0)
    dividend = integer_0
    divisor = integer_1
    dividend_coeff_0 = 1
    dividend_coeff_1 = 0
    divisor_coeff_0 = 0
    divisor_coeff_1 = 1
    while True:
        quotient = dividend // divisor
        remainder = dividend - quotient * divisor
        if remainder == 0:
            if swap:
                (divisor_coeff_0, divisor_coeff_1) = (divisor_coeff_1, divisor_coeff_0)
            return divisor, divisor_coeff_0, divisor_coeff_1
        remainder_coeff_0 = dividend_coeff_0 - quotient * divisor_coeff_0
        remainder_coeff_1 = dividend_coeff_1 - quotient * divisor_coeff_1
        dividend = divisor
        divisor = remainder
        dividend_coeff_0 = divisor_coeff_0
        dividend_coeff_1 = divisor_coeff_1
        divisor_coeff_0 = remainder_coeff_0
        divisor_coeff_1 = remainder_coeff_1

def gcd(integers):
    """The greatest common divisor of a container of integers."""
    divisor, coeff_0, coeff_1 = lbolt_coeffs(integers[0], integers[1])
    coeffs = [coeff_0, coeff_1]
    for i in range(2, len(integers)):
        divisor, coeff_0, coeff_1 = lbolt_coeffs(divisor, integers[i])
        coeffs = [coeff_0 * coeff for coeff in coeffs]
        coeffs.append(coeff_1)
    return divisor, coeffs

def reduced_products(moduli):
    """The reduced products for a container of moduli."""
    product = 1
    for modulus in moduli:
        product *= modulus
    return [product // modulus for modulus in moduli]

def magic_iterative(moduli):
    """The magic tuple for a container of moduli, computed iteratively."""
    products = reduced_products(moduli)
    _, coeffs = gcd(products)
    return [products[i] * coeffs[i] for i in range(len(moduli))]

def magic_complicated(moduli):
    """The magic tuple for a container of moduli, computed iteratively and pulling out the common
    factors of reduced products before calling the lightning bolt algorithm."""
    products = reduced_products(moduli)
    coeffs = [1]
    product = 1
    for i in range(1, len(moduli)):
        product *= moduli[i - 1]
        _, coeff_modulus, coeff_product = lbolt_coeffs(moduli[i], product)
        coeffs = [coeff_modulus * coeff for coeff in coeffs] + [coeff_product]
    return [products[i] * coeffs[i] for i in range(len(moduli))]

def magic_parallel(moduli):
    """The magic tuple for a container of moduli, computed in parallel."""
    products = reduced_products(moduli)
    magic = []
    for i, modulus in enumerate(moduli):
        product = products[i]
        magic.append(product * lbolt_coeffs(product, modulus)[1])
    return magic

def solve_congruence(modulus, coefficient, target):
    """The solutions to a linear congruence."""
    if coefficient < modulus:
        dividend = modulus
        divisor = coefficient
    else:
        dividend = coefficient
        divisor = modulus
    quotients = []
    while True:
        quotient = dividend // divisor
        quotients.append(quotient)
        remainder = dividend - quotient * divisor
        if remainder == 0:
            break
        dividend = divisor
        divisor = remainder
    if target != (target // divisor) * divisor:
        return []
    modulus //= divisor
    modulus_coeff = 0
    coeff_coeff = 1
    for quotient in quotients[:-1]:
        remainder_coeff = modulus_coeff - quotient * coeff_coeff
        modulus_coeff = coeff_coeff
        coeff_coeff = remainder_coeff
    solution = (coeff_coeff * target // divisor) % modulus
    return [solution + k * modulus for k in range(divisor)]

def fuse_two_congruences(mtar_1, mtar_2):
    """The fusion of two congruences."""
    modulus_1, target_1 = mtar_1
    modulus_2, target_2 = mtar_2
    greater = modulus_1 < modulus_2
    if greater:
        dividend = modulus_2
        divisor = modulus_1
        coeff_0 = 0
        coeff_1 = 1
    else:
        dividend = modulus_1
        divisor = modulus_2
        coeff_0 = 1
        coeff_1 = 0
    quotients = []
    while True:
        quotient = dividend // divisor
        quotients.append(quotient)
        remainder = dividend - quotient * divisor
        if remainder == 0:
            break
        dividend = divisor
        divisor = remainder
    difference = target_1 - target_2
    ratio = difference // divisor
    if difference != ratio * divisor:
        return -1, -1
    for quotient in quotients[:-1]:
        remainder_coeff = coeff_0 - quotient * coeff_1
        coeff_0 = coeff_1
        coeff_1 = remainder_coeff
    modulus = modulus_1 * (modulus_2 // divisor) if greater else modulus_2 * (modulus_1 // divisor)
    return modulus, (target_1 - ratio * coeff_1 * modulus_1) % modulus

def fuse_congruences(mtars):
    """The fusion of many congruences."""
    fusion = fuse_two_congruences(mtars[0], mtars[1])
    for i in range(2, len(mtars)):
        fusion = fuse_two_congruences(fusion, mtars[i])
    return fusion
