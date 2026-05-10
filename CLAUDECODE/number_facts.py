import sys
import math

def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def is_perfect_square(n):
    if n < 0:
        return False
    root = int(math.sqrt(n))
    return root * root == n

def is_fibonacci(n):
    if n < 0:
        return False
    a, b = 0, 1
    while a < n:
        a, b = b, a + b
    return a == n

if len(sys.argv) < 2:
    print("Error: Please provide a number as an argument.")
    print("Usage: python number_facts.py <number>")
    sys.exit(1)

try:
    num = int(sys.argv[1])
except ValueError:
    print(f"Error: '{sys.argv[1]}' is not a valid integer.")
    sys.exit(1)

print(f"\nNumber Facts for {num}:")
print("-" * 40)
print(f"Prime:          {is_prime(num)}")
print(f"Perfect Square: {is_perfect_square(num)}")
print(f"Fibonacci:      {is_fibonacci(num)}")
print("-" * 40)