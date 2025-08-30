import math
import argparse

def prime_factorization_by_trial_division(integer_to_be_factored):
    '''
    Prime factorization by trial division
    Time complexity: O(sqrt(n))
    The return value is a list of tuples (prime_factor, exponent)
    '''
    prime_factors = []
    # Handle the case when the integer to be factored is even, this can reduce the time complexity
    while integer_to_be_factored % 2 == 0:
        prime_factors.append(2)
        integer_to_be_factored /= 2
    for i in range(3, int(math.sqrt(integer_to_be_factored)) + 1, 2):
        while integer_to_be_factored % i == 0:
            prime_factors.append(i)
            integer_to_be_factored /= i
    if integer_to_be_factored > 2:
        prime_factors.append(int(integer_to_be_factored))
    prime_factors_combined = {}
    for prime_factor in prime_factors:
        if prime_factor in prime_factors_combined:
            prime_factors_combined[prime_factor] += 1
        else:
            prime_factors_combined[prime_factor] = 1
    prime_factors = [[prime_factor, prime_factors_combined[prime_factor]] for prime_factor in prime_factors_combined.keys() if prime_factors_combined[prime_factor] > 0]
    return prime_factors

def pow_mod_p(x, n, p):
    '''
    Exponetiation by squaring
    Calculate x^n mod p
    Time complexity: O(log n)
    '''
    res = 1 # Initialize result
    x = x % p
 
    while (n > 0):
        # If n is odd, multiply x with result
        if (n & 1):
            res = (res * x) % p
        # n must be even now, apply squaring
        n = n >> 1
        x = (x * x) % p
    return res

def baby_step_giant_step(g, h, p, order):
    '''
    Baby-step giant-step algorithm
    Find k such that g^k = h mod p
    'order' is the order of g mod p
    Note: order is not necessarily equal to p - 1
    Time complexity: O(sqrt(order))
    '''
    m = math.ceil(math.sqrt(order))
    table = {}
    # calculate all possible values of g^j mod p for j = 0, 1, ..., m-1
    for j in range(m):
        table[pow_mod_p(g, j, p)] = j
    # calculate the inverse element of g, using the fact that g^{-1} = g^{order - 1} mod p
    g_inverse = pow_mod_p(g, order - 1, p)
    # calculate g_to_the_minus_m = g^(-m) mod p
    g_to_the_minus_m = pow_mod_p(g_inverse, m, p)
    # initialize gamma = h mod p
    gamma = h % p
    # search for a match between gamma and table
    for i in range(m):
        if gamma in table:
            return i * m + table[gamma]
        else:
            gamma = (gamma * g_to_the_minus_m) % p
    return None

def pohlig_hellman_prime_power_order(g, h, q, e, p):
    '''
    Pohlig-Hellman algorithm for groups of prime power order
    Find k such that g^k = h mod p
    'p' is the prime modulus
    'q' is the prime factor of p - 1
    'e' is the exponent of q in the prime factorization of p - 1
    i.e., p - 1 = q^e * m, where m is an integer and gcd(q, m) = 1
    Time complexity: O(e * sqrt(q))
    '''
    g_inverse = pow_mod_p(g, q**e - 1, p)
    gamma = pow_mod_p(g, q**(e - 1), p)
    k_i = 0
    for i in range(e):
        h_i = pow_mod_p(g_inverse, k_i, p) * h % p
        h_i = pow_mod_p(h_i, q**(e-1-i), p)
        d_i = baby_step_giant_step(gamma, h_i, p, q)
        k_i += d_i * q**i
    return k_i

def chinese_remainder_theorem(remainders, moduli, factors):
    '''
    Chinese remainder theorem
    Find k such that k = remainders[i] mod moduli[i] for all i
    'factors' is the prime factorization of the moduli, which is a list of tuples (q, e)
    'factors' is used to calculate the order of each modulus
    '''
    # Compute the product of all moduli, in our case it is equal to p - 1
    M = 1
    for m in moduli:
        M *= m
    # Compute the solution x using the CRT formula
    k = 0
    for i in range(len(moduli)):
        M_i = M // moduli[i]
        # Compute order for each modulus, using the fact that \varphi(q^e) = q^e - q^(e-1)
        order = factors[i][0]**factors[i][1] - factors[i][0]**(factors[i][1] - 1)
        # Calculate the inverse element of Mi mod moduli[i]
        M_i_inverse = pow_mod_p(M_i, order - 1, moduli[i])
        k += remainders[i] * M_i * M_i_inverse
        k = k % M
    return k 

def pohlig_hellman(g, h, p, factors):
    '''
    General Pohlig-Hellman algorithm
    Find k such that g^k = h mod p
    'p' is the prime modulus
    'factors' is the prime factorization of p - 1, which is a list of tuples (q, e)
    Note: q == 2 is solved by brute force
    Time complexity: O(sum_i e_i * (log n + sqrt(q_i)))
    '''
    k = 0
    remainders = []
    moduli = []
    for q, e in factors:
        g_i = pow_mod_p(g, (p - 1) // (q**e), p)
        h_i = pow_mod_p(h, (p - 1) // (q**e), p)
        if q == 2:
            for k_i in range(q**e):
                if pow_mod_p(g_i, k_i, p) == h_i:
                    break
        else:
            k_i = pohlig_hellman_prime_power_order(g_i, h_i, q, e, p)
        remainders.append(k_i)
        moduli.append(q**e)
    k = chinese_remainder_theorem(remainders, moduli, factors)
    return k

if __name__ == '__main__':
    argparse = argparse.ArgumentParser()
    argparse.add_argument('-arg_g', '--generator', type=int, help='The generator of the group')
    argparse.add_argument('-arg_h', '--element', type=int, help='The element of the group')
    argparse.add_argument('-arg_p', '--modulus', type=int, help='The modulus, can be a prime or a composite number')
    args = argparse.parse_args()
    g_test = 2
    h_test = 465161198894784
    p_test = 656100000000001
    g = args.generator
    h = args.element
    p = args.modulus
    # p - 1 = 2^11 * 3^8 * 5^11
    #factors = [(2, 11), (3, 8), (5, 11)]
    factors = prime_factorization_by_trial_division(p - 1)
    k = pohlig_hellman(g, h, p, factors)
    #print("k = ")
    print(k)
    #print('check g^k = h:', pow_mod_p(g, k, p) == h)