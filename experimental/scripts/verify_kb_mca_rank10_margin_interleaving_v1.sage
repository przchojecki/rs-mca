#!/usr/bin/env sage
"""Independent Sage replay of decisive rank-ten numbers and GF(11) fixture."""

from math import comb, prod

n, K, m, w = 2097152, 1048576, 1116048, 67472
p, extension_degree = 2130706433, 6
budget, near, s, T = 274980728111395087, 134944, 9, 667

fall = lambda x, j: prod(x-i for i in range(j))
rise = lambda x, j: prod(x+i for i in range(j))
A = m-T+1
M = comb(n-K+s, s) // comb(A-K+s, s)
caps = [n//T]
for r in range(1, s+1):
    caps.append(floor(max(
        QQ(fall(n,r+1))/(m*T*rise(w+1,r-1)),
        QQ(fall(n-K+r,r+1))/(T*rise(w+1,r)),
    )))
high = max(caps)
low = (n-A)*M
total = near+high+low
assert (A,M,high,low,total,budget-total) == (
    1115382,57781140652,5143522968716559,56727790457914040,
    61871313426765543,213109414684629544)
assert M^2 < p^extension_degree and M^2 >= p

F = GF(11)
slopes = list(map(F, range(8)))
r0 = [F(0),F(0)] + [-g for g in slopes]
r1 = [F(0),F(0)] + [F(1)]*8
for j,g in enumerate(slopes):
    S = [i for i in range(10) if r0[i]+g*r1[i] == 0]
    assert S == [0,1,j+2]
    assert len(set(r0[i] for i in S)) > 1 or len(set(r1[i] for i in S)) > 1
toy_A = 2
assert len(slopes) == 10-toy_A
print("KB_MCA_RANK10_MARGIN_INTERLEAVING_SAGE_PASS")
