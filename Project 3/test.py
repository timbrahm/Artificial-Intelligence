from decimal import *

test = ['2 2', '1 1 0 1', '0 1 1 1', '0 0 1 1', '1 0 1 0']
new = [i.split() for i in test]

# print(test)
# print(new)

r, c = 10, 10
r1, r2, c1, c2 = r - 1, r + 1, c - 1, c + 1


print(r1, r2)
print(c1, c2)