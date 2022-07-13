a = {0, 1, 3, 5, 7, 9}
b = {2, 4, 6, 8, 0}

c = a.union(b)
c = a & b
c.update({-11, 11, 12, -12})
d = a.intersection(b,c)
print(d)
print(c)
