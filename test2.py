# Enter your code here. Read input from STDIN. Print output to STDOUT
n = raw_input("how many years?")
print n
prices = [int(x) for x in raw_input("prices?").split()]

min_cost = 0

for i in range(len(prices)):
    for j in range(i + 1, len(prices)):
        if prices[i] > prices[j]:
            if min_cost is 0:
                min_cost = prices[i] - prices[j]
            min_cost = min(min_cost, prices[i] - prices[j])

print min_cost