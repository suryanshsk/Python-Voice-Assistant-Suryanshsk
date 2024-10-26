def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

# Get user input
a = int(input("Enter the first number: "))
b = int(input("Enter the second number: "))
print(f"The GCD of {a} and {b} is: {gcd(a, b)}")
