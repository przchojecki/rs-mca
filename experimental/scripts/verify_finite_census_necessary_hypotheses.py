#!/usr/bin/env python3
"""Exact replays for cap25_finite_census_necessary_hypotheses.md.
stdlib only; < 10 s; deterministic."""
import math

fails = []
def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name)
    if not ok:
        fails.append(name)

# ---- Trap 1: char-3 eta block (F_81 = F_3[X]/(X^4+X^2-1)) ----
P = 3
def mul3(a, b):
    r = [0]*7
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            r[i+j] = (r[i+j] + ai*bj) % P
    for d in range(6, 3, -1):     # X^4 = -X^2+1 = 2X^2+1
        c = r[d]
        if c:
            r[d] = 0
            r[d-2] = (r[d-2] + 2*c) % P
            r[d-4] = (r[d-4] + c) % P
    return r[:4]
def pow3(a, e):
    r = [1,0,0,0]; b = a[:]
    while e:
        if e & 1: r = mul3(r, b)
        b = mul3(b, b); e >>= 1
    return r
eta = [0,1,0,0]
check("char3: eta has order 16", pow3(eta,16) == [1,0,0,0] and pow3(eta,8) == [2,0,0,0])
E3 = [0,1,2,8,10,11,13]
for k in (1, 2):
    s = [0,0,0,0]
    for e in E3:
        v = pow3(eta, (k*e) % 16)
        s = [(x+y) % P for x, y in zip(s, v)]
    check(f"char3: p_{k}(B) = 0", s == [0,0,0,0])
check("char3: |B| = 7 distinct", len({tuple(pow3(eta,e)) for e in E3}) == 7)
# p-free exclusion arithmetic: ord_512(3) = 128, t*_eff = 2
o = 1; v = 3
while v != 1:
    v = (v*3) % 512; o += 1
check("char3: ord_512(3) = 128", o == 128)
check("char3: p-free balance fails (2*128*log2(3) < 512)",
      2*128*math.log2(3) < 512 < 3*128*math.log2(3))

# ---- Trap 2: char-7 seed + aspect table (F_{7^4} = F_7[X]/(X^4-X^2-1)) ----
Q7 = 7
def mul7(a, b):
    r = [0]*7
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            r[i+j] = (r[i+j] + ai*bj) % Q7
    for d in range(6, 3, -1):     # X^4 = X^2 + 1
        c = r[d]
        if c:
            r[d] = 0
            r[d-2] = (r[d-2] + c) % Q7
            r[d-4] = (r[d-4] + c) % Q7
    return r[:4]
def pow7(a, e):
    r = [1,0,0,0]; b = a[:]
    while e:
        if e & 1: r = mul7(r, b)
        b = mul7(b, b); e >>= 1
    return r
om = [0,1,0,0]
check("char7: omega has order 32", pow7(om,32) == [1,0,0,0] and pow7(om,16) != [1,0,0,0])
E7 = [0,1,2,3,5,9,11,15,16,18,23]
for k in range(1, 6):
    s = [0,0,0,0]
    for e in E7:
        v = pow7(om, (k*e) % 32)
        s = [(x+y) % Q7 for x, y in zip(s, v)]
    check(f"char7: p_{k}(seed) = 0", s == [0,0,0,0])
# aspect table: super-budget iff aspect-violating
rows_ok = True
for N in (64, 128, 256, 512):
    aspect = (N // 8) * math.log2(7) / math.log2(N)
    super_budget = 2 ** (3 * N // 16) > N ** 3
    violating = aspect > 256 / 41
    print(f"  N={N}: aspect={aspect:.3f} superbudget={super_budget} violating={violating}")
    rows_ok = rows_ok and (super_budget == violating)
check("char7: super-budget iff aspect-violating (all four scales)", rows_ok)

# ---- Trap 3: the M_0 lift identity at (q=97, N=32, M=8) ----
q, N, M = 97, 32, 8
def pf(x):
    out, d = [], 2
    while d*d <= x:
        while x % d == 0: out.append(d); x //= d
        d += 1
    if x > 1: out.append(x)
    return out
g = next(c for c in range(2, q) if all(pow(c, (q-1)//r, q) != 1 for r in set(pf(q-1))))
h = pow(g, (q-1)//N, q)
D = [pow(h, i, q) for i in range(N)]
mu4 = sorted({pow(x, M, q) for x in D})
A = {mu4[0], q - mu4[0]} & set(mu4)      # a zero-sum quotient pair
BA = [x for x in D if pow(x, M, q) in A]
lift_ok = len(A) == 2 and len(BA) == 16
for i in range(1, 2*M):
    s = sum(pow(x, i, q) for x in BA) % q
    expect = (M * sum(A)) % q if i == M else 0
    lift_ok = lift_ok and (s == expect)
check("lift: p_i(B_A) = 0 (i != M), = M*sum(A) (i = M), all i < 2M", lift_ok)

print()
if fails:
    raise SystemExit("FAIL: " + ", ".join(fails))
print("FINITE_CENSUS_NECESSARY_HYPOTHESES_PASS")
