def ways(n):
    if n < 0:
        return 0

    if n == 0:
        return 1

    return ways(n - 1) + ways(n - 2) + ways(n - 3)


print("ways(3) =", ways(3))
print("ways(5) =", ways(5))
print("ways(10) =", ways(10))