def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

# Get user input
a = int(input("Enter the first number: "))
b = int(input("Enter the second number: "))
print(f"The LCM of {a} and {b} is: {lcm(a, b)}")
