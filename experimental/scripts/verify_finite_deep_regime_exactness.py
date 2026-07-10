#!/usr/bin/env python3
"""Exact verifier for cap25_finite_deep_regime_exactness.md.
stdlib only; ~60 s; deterministic."""
import math

fails = []
def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name)
    if not ok:
        fails.append(name)

def pf(x):
    out, d = [], 2
    while d*d <= x:
        while x % d == 0: out.append(d); x //= d
        d += 1
    if x > 1: out.append(x)
    return out

def is_prime(m):
    if m < 2: return False
    i = 2
    while i*i <= m:
        if m % i == 0: return False
        i += 1
    return True

def mu(q, N):
    g = next(c for c in range(2, q) if all(pow(c, (q-1)//r, q) != 1 for r in set(pf(q-1))))
    h = pow(g, (q-1)//N, q)
    return [pow(h, i, q) for i in range(N)]

# (a) N=8, j=2 sweep: exact dichotomy at every prime = 1 mod 8 in [257, 4000)
N = 8
bad = 0; tested = 0
for q in range(257, 4000):
    if q % N != 1 or not is_prime(q):
        continue
    D = mu(q, N)
    cnt = 0
    for mask in range(1 << N):
        s1 = s2 = 0; m = mask; i = 0
        while m:
            if m & 1:
                s1 += D[i]; s2 += D[i]*D[i]
            m >>= 1; i += 1
        if s1 % q == 0 and s2 % q == 0:
            cnt += 1
    tested += 1
    if cnt != 2 ** (N // 4):   # struct at N=8, j=2: the two mu_4-cosets -> 2^2 = 4 unions
        bad += 1
print(f"  swept {tested} primes")
check("N=8 sweep: census = struct (4) at EVERY prime", bad == 0 and tested > 100)

# (b) level-dependent struct: j=4 census = 2^{N/8} (mu_8-unions) at (12289, 16)
q, N4 = 12289, 16
D = mu(q, N4)
cnt4 = 0
for mask in range(1 << N4):
    s1 = s2 = s3 = s4 = 0; m = mask; i = 0
    while m:
        if m & 1:
            x = D[i]; x2 = x*x % q
            s1 += x; s2 += x2; s3 += x2*x % q; s4 += x2*x2 % q
        m >>= 1; i += 1
    if s1 % q == 0 and s2 % q == 0 and s3 % q == 0 and s4 % q == 0:
        cnt4 += 1
check("j=4 census at (12289,16) = 2^{N/8} = 4 (NOT 2^{N/4} = 16)", cnt4 == 4)

# (c) mini N=32 MTM transition: shallow primes have extras, deep have zero
def census32(q):
    D = mu(q, 32)
    A, B = D[:16], D[16:]
    def vecs(H):
        pw = [(x % q, x*x % q, pow(x, 3, q)) for x in H]
        out = [(0, 0, 0)] * (1 << 16)
        for m in range(1, 1 << 16):
            lb = m & (-m); i = lb.bit_length() - 1
            p0 = out[m ^ lb]; e = pw[i]
            out[m] = ((p0[0]+e[0]) % q, (p0[1]+e[1]) % q, (p0[2]+e[2]) % q)
        return out
    va, vb = vecs(A), vecs(B)
    from collections import defaultdict
    cnt = defaultdict(int)
    for v in va:
        cnt[v] += 1
    tot = 0
    for v in vb:
        tot += cnt.get(((q-v[0]) % q, (q-v[1]) % q, (q-v[2]) % q), 0)
    return tot
shallow = census32(257)          # occupancy 2^32/257^3 ~ 253: flat-dominated
deep1, deep2 = census32(3041), census32(4001)
print(f"  N=32 j=3 census: q=257 -> {shallow}; q=3041 -> {deep1}; q=4001 -> {deep2}")
check("N=32 transition: shallow prime has extras (census > struct 256)", shallow > 256)
check("N=32 transition: deep primes exact (census = struct 256)", deep1 == 256 and deep2 == 256)

print()
if fails:
    raise SystemExit("FAIL: " + ", ".join(fails))
print("FINITE_DEEP_REGIME_EXACTNESS_PASS")
