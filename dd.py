import math
import time
import matplotlib.pyplot as plt

def cube_root_integer_positive(n):
    """
    Finds the integer cube root of a non-negative integer.

    Args:
        n: A non-negative integer.

    Returns:
        A tuple containing:
        - The integer cube root of n.
        - The number of steps taken.
    """
    if n < 0:
        raise ValueError("Input must be a non-negative integer.")
    steps = 0
    if n == 0:
        return 0, steps
    low = 0
    high = n
    ans = -1
    while low <= high:
        steps += 1
        mid = (low + high) // 2
        cube = mid ** 3
        if cube == n:
            ans = mid
            break
        elif cube < n:
            ans = mid
            low = mid + 1
        else:
            high = mid - 1
    return ans, steps

def primality_test(n):
    """
    Checks if a number is prime.

    Args:
        n: An integer.

    Returns:
        A tuple containing:
        - True if n is prime, False otherwise.
        - The number of steps taken.
    """
    steps = 0
    if n <= 1:
        return False, steps + 1
    if n <= 3:
        return True, steps + 2
    if n % 2 == 0 or n % 3 == 0:
        return False, steps + 3
    i = 5
    while i * i <= n:
        steps += 1
        if n % i == 0 or n % (i + 2) == 0:
            return False, steps + 1
        i += 6
    return True, steps

def sum_primes_up_to(limit):
    """
    Calculates the sum of prime numbers between 3 and a given limit.

    Args:
        limit: An integer representing the upper limit.

    Returns:
        The sum of prime numbers between 3 and limit, and the total steps.
    """
    steps = 0
    if limit < 3:
        return 0, steps
    primes = [True] * (limit + 1)
    primes[0] = primes[1] = False
    for p in range(2, int(math.sqrt(limit)) + 1):
        steps += 1
        if primes[p]:
            for i in range(p * p, limit + 1, p):
                primes[i] = False
                steps += 1
    prime_sum = 0
    for i in range(3, limit + 1, 2): # Optimized to check only odd numbers after 2
        steps += 1
        if primes[i]:
            prime_sum += i
    return prime_sum, steps

def egg_drop(floors, eggs):
    """
    Calculates the minimum number of trials needed to find the critical floor
    using dynamic programming.

    Args:
        floors: The number of floors in the building.
        eggs: The number of eggs available.

    Returns:
        The minimum number of trials in the worst case.
    """
    dp = [[0 for _ in range(eggs + 1)] for _ in range(floors + 1)]

    # Base cases
    for i in range(1, floors + 1):
        dp[i][1] = i
    for j in range(1, eggs + 1):
        dp[1][j] = 1

    # Fill the DP table
    for i in range(2, floors + 1):
        for j in range(2, eggs + 1):
            dp[i][j] = float('inf')
            for x in range(1, i + 1):
                # Worst case of egg breaking or not breaking
                res = 1 + max(dp[x - 1][j - 1], dp[i - x][j])
                if res < dp[i][j]:
                    dp[i][j] = res
    return dp[floors][eggs]

def egg_drop_optimized(floors, eggs):
    """
    Calculates the minimum number of trials needed to find the critical floor
    using a more optimized approach for a fixed number of eggs.
    This version is tailored for the 7-egg scenario.

    Args:
        floors: The number of floors in the building.
        eggs: The number of eggs available.

    Returns:
        The minimum number of trials in the worst case.
    """
    if eggs == 1:
        return floors
    if floors <= 1:
        return floors

    dp = [[0 for _ in range(floors + 1)] for _ in range(eggs + 1)]

    for j in range(1, floors + 1):
        dp[1][j] = j

    for i in range(2, eggs + 1):
        m = 1
        for j in range(1, floors + 1):
            while m < j and max(dp[i - 1][m - 1], dp[i][j - m]) > max(dp[i - 1][m], dp[i][j - m - 1]):
                m += 1
            dp[i][j] = 1 + max(dp[i - 1][m - 1], dp[i][j - m])

    return dp[eggs][floors]

if __name__ == "__main__":
    # Cube Root Testing (Positive Numbers Only)
    print("--- Cube Root Testing (Positive Numbers Only) ---")
    numbers_cube_positive = [8, 27, 125, 216, 1000]
    steps_cube_positive = []
    digits_cube_positive = []
    for num in numbers_cube_positive:
        root, steps = cube_root_integer_positive(num)
        print(f"Cube root of {num} is {root}, steps: {steps}")
        steps_cube_positive.append(steps)
        digits_cube_positive.append(len(str(num)))

    plt.figure(figsize=(8, 5))
    plt.plot(digits_cube_positive, steps_cube_positive, marker='o')
    plt.title("Cube Root (Positive): Steps vs Number of Digits")
    plt.xlabel("Number of Digits")
    plt.ylabel("Number of Steps")
    plt.grid(True)
    plt.show()

    # Primality Testing
    print("\n--- Primality Testing ---")
    numbers_prime = [2, 3, 4, 11, 15, 23, 100]
    steps_prime = []
    digits_prime = []
    for num in numbers_prime:
        is_prime, steps = primality_test(num)
        print(f"{num} is prime: {is_prime}, steps: {steps}")
        steps_prime.append(steps)
        digits_prime.append(len(str(abs(num))))

    plt.figure(figsize=(8, 5))
    plt.plot(digits_prime, steps_prime, marker='o')
    plt.title("Primality Test: Steps vs Number of Digits")
    plt.xlabel("Number of Digits")
    plt.ylabel("Number of Steps")
    plt.grid(True)
    plt.show()

    # Sum of Primes
    print("\n--- Sum of Primes ---")
    limit = 1000
    sum_of_primes, steps_sum_primes = sum_primes_up_to(limit)
    print(f"Sum of prime numbers between 3 and {limit}: {sum_of_primes}, steps: {steps_sum_primes}")

    # Egg Dropping Puzzle
    print("\n--- Egg Dropping Puzzle ---")
    num_floors = 102
    num_eggs = 7
    min_trials = egg_drop_optimized(num_floors, num_eggs)
    print(f"Minimum number of trials for {num_floors} floors and {num_eggs} eggs: {min_trials}")

    # Explanation of the 7-egg use case
    print("\n--- Explanation of 7-Egg Use Case ---")
    print("""
    The standard dynamic programming solution for the egg dropping puzzle (egg_drop function)
    has a time complexity that depends on both the number of floors and the number of eggs.
    For a small number of eggs, like 7, we can potentially optimize the DP approach.

    The egg_drop_optimized function attempts a slight optimization by trying to find the
    optimal dropping floor 'm' more efficiently within the DP calculation. However, for a
    fixed small number of eggs, the core complexity still relates to the number of floors.

    How this use case can be used in other scenarios:
    The fundamental principle of the egg dropping puzzle is to find the minimum number of
    experiments needed to determine a threshold (the critical floor in this case) in a
    system where the outcome of an experiment (egg breaks or doesn't break) provides
    information.

    Other scenarios where this logic can be applied:
    1. Software Testing: Finding the minimum number of test cases to identify a bug threshold
       (e.g., the maximum load a system can handle before crashing).
    2. Quality Control: Determining the minimum number of trials to find the failure point of a
       product under stress.
    3. Binary Search Variations: While binary search assumes a sorted space, the egg dropping
       puzzle deals with a more complex scenario where the 'cost' of failure (a broken egg)
       is significant. The strategies learned can inform how to probe a search space more
       effectively when there are constraints on the number of failures.
    4. Decision Making under Uncertainty: The problem explores the trade-off between the number
       of experiments and the certainty of the result, which is a common theme in various
       decision-making processes.

    The provided 'egg_drop_optimized' function with 7 eggs aims to find a balance between
    the number of trials and the number of eggs, which is crucial in scenarios where tests
    are costly or resources (like eggs) are limited.
    """)

    # Example with a different number of eggs for the Empire State Building
    num_eggs_other = 3
    min_trials_other = egg_drop(num_floors, num_eggs_other)
    print(f"\nMinimum number of trials for {num_floors} floors and {num_eggs_other} eggs: {min_trials_other}")
