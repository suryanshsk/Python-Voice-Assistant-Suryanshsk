def binary_exponentiation(base, exp):
    result = 1
    while exp > 0:
        if exp % 2 == 1:
            result *= base
        base *= base
        exp //= 2
    return result

# Get user input
base = float(input("Enter the base: "))
exp = int(input("Enter the exponent: "))
print(f"{base} raised to the power {exp} is: {binary_exponentiation(base, exp)}")
