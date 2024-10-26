def exponentiation_by_squaring(base, exp):
    if exp < 0:
        return 1 / exponentiation_by_squaring(base, -exp)
    if exp == 0:
        return 1
    half = exponentiation_by_squaring(base, exp // 2)
    return half * half if exp % 2 == 0 else base * half * half

# Get user input
base = float(input("Enter the base: "))
exp = int(input("Enter the exponent: "))
print(f"{base} raised to the power {exp} is: {exponentiation_by_squaring(base, exp)}")
