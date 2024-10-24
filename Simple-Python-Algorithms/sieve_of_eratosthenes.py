def sieve_of_eratosthenes(n):
    primes = []
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False

    for i in range(2, n + 1):
        if is_prime[i]:
            primes.append(i)
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    return primes

# Get user input
n = int(input("Enter the upper limit to find prime numbers: "))
print(f"Prime numbers up to {n} are: {sieve_of_eratosthenes(n)}")
