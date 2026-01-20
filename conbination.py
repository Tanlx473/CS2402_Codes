import math

N = int(input("input N: "))
k = int(input("input k: "))

com = math.comb(N, k)
print(f"The combination (N, k) is: {com}")