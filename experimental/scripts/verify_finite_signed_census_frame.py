#!/usr/bin/env python3
"""Exact verifier for cap25_finite_signed_census_frame.md.
stdlib only; ~30 s; deterministic."""
import cmath, math

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

def mu(q, N):
    g = next(c for c in range(2, q) if all(pow(c, (q-1)//r, q) != 1 for r in set(pf(q-1))))
    h = pow(g, (q-1)//N, q)
    return [pow(h, i, q) for i in range(N)]

# --- Theorems 1+2 at (q, N, j) = (97, 32, 2): quantization + census identity
q, N, j = 97, 32, 2
D = mu(q, N)
xb = [(x, x*x % q) for x in D]
# integer census by DP over (p1, p2)
cen = {(0, 0): 1}
for (x1, x2) in xb:
    new = dict(cen)
    for (a, b), cnt in cen.items():
        k = ((a + x1) % q, (b + x2) % q)
        new[k] = new.get(k, 0) + cnt
    cen = new
N_total = cen.get((0, 0), 0)
signed_exact = q**j * N_total - 2**N
# frequency side: quantization + signed sum
tot = 0.0
quant_ok = True
for c1 in range(q):
    for c2 in range(q):
        if c1 == 0 and c2 == 0:
            continue
        ssum = U = 0
        S = 0.0
        for (x1, x2) in xb:
            s = (c1*x1 + c2*x2) % q
            ssum += s
            U += s > q//2
            S += math.log(abs(2*math.cos(math.pi*s/q))) if s else math.log(2.0)
        if ssum % q:
            quant_ok = False
        eps = 1 - 2*((ssum//q + U) % 2)
        tot += eps * math.exp(S)
check("T1: quantization (sum s_x = 0 mod q at every c)", quant_ok)
check("T2: census identity (rel err < 1e-9)",
      abs(tot - signed_exact) <= 1e-9 * max(1.0, abs(signed_exact)))

# --- Theorem 3 at (113, 16, 2): ladder identity, integer-exact
q2, N2 = 113, 16
D2 = mu(q2, N2)
xb2 = [(x, x*x % q2) for x in D2]
lad = {(0, 0): 1}
for (x1, x2) in xb2:
    new = {}
    for (a, b), cnt in lad.items():
        for (m1, m2, w) in ((0, 0, 2), (x1, x2, 1), (q2-x1, q2-x2, 1)):
            k = ((a+m1) % q2, (b+m2) % q2)
            new[k] = new.get(k, 0) + cnt*w
    lad = new
Cpp = lad.get((0, 0), 0)
lhs = q2**2 * Cpp - 4**N2
tot2 = 0.0
for c1 in range(q2):
    for c2 in range(q2):
        if c1 == 0 and c2 == 0:
            continue
        S2 = 0.0
        for (x1, x2) in xb2:
            s = (c1*x1 + c2*x2) % q2
            S2 += 2*math.log(abs(2*math.cos(math.pi*s/q2))) if s else 2*math.log(2.0)
        tot2 += math.exp(S2)
check("T3: ladder identity (rel err < 1e-9)",
      abs(tot2 - lhs) <= 1e-9 * max(1.0, abs(lhs)))

# --- Theorem 4: tower row F_49 (p=7, k=2), N=16, j=2
p, k, Nt = 7, 2, 16
def mul49(a, b):  # F_7[X]/(X^2 - 3): X^2 = 3 (3 is a QNR mod 7)
    return ((a[0]*b[0] + 3*a[1]*b[1]) % p, (a[0]*b[1] + a[1]*b[0]) % p)
def pow49(a, e):
    r = (1, 0); b = a
    while e:
        if e & 1: r = mul49(r, b)
        b = mul49(b, b); e >>= 1
    return r
gen = None
for a0 in range(p):
    for a1 in range(p):
        cand = (a0, a1)
        if cand == (0, 0):
            continue
        if all(pow49(cand, 48//r) != (1, 0) for r in (2, 3)):
            gen = cand
            break
    if gen:
        break
hh = pow49(gen, 48 // Nt)
Dt = []
v = (1, 0)
for _ in range(Nt):
    Dt.append(v)
    v = mul49(v, hh)
tr = lambda a: (2*a[0]) % p           # Tr(a0 + a1 X) = 2 a0
add49 = lambda a, b: ((a[0]+b[0]) % p, (a[1]+b[1]) % p)
xbt = [(x, mul49(x, x)) for x in Dt]
cen_t = {}
for T in range(1 << Nt):
    a = (0, 0); b = (0, 0); m = T; i = 0
    while m:
        if m & 1:
            a = add49(a, xbt[i][0]); b = add49(b, xbt[i][1])
        m >>= 1; i += 1
    if a == (0, 0) and b == (0, 0):
        cen_t[T] = 1
Nt_total = len(cen_t)
tot_t = 0.0
quant_t = True
for e1 in range(49):
    for e2 in range(49):
        if e1 == 0 and e2 == 0:
            continue
        c1 = (e1 % p, e1 // p); c2 = (e2 % p, e2 // p)
        S = 0.0; ph = 0.0; trs = 0
        for (xx, x2) in xbt:
            y = add49(mul49(c1, xx), mul49(c2, x2))
            t = tr(y)
            trs += t
            w = 1 + cmath.exp(2j*math.pi*t/p)
            S += math.log(abs(w))
            ph += cmath.phase(w)
        if trs % p:
            quant_t = False
        tot_t += math.exp(S) * math.cos(ph)
signed_t = 49**2 * Nt_total - 2**Nt
check("T4: tower quantization (trace sums vanish)", quant_t)
check("T4: tower census identity (rel err < 1e-9)",
      abs(tot_t - signed_t) <= 1e-9 * max(1.0, abs(signed_t)))

# --- Theorem 5: diagonalization at (q=97, G = index-3 subgroup)
q5, m5 = 97, 3
g5 = next(c for c in range(2, q5) if all(pow(c, (q5-1)//r, q5) != 1 for r in set(pf(q5-1))))
dl = [0]*q5
v = 1
for i in range(q5-1):
    dl[v] = i; v = v*g5 % q5
f5 = (q5-1)//m5
L = [0.0]*q5
for s in range(1, q5):
    L[s] = math.log(abs(2*math.cos(math.pi*s/q5)))
w5 = cmath.exp(2j*math.pi/m5)
aL = [sum(w5**(-jj*dl[s]) * L[s] for s in range(1, q5)) / (q5-1) for jj in range(m5)]
G5 = [pow(g5, m5*i, q5) for i in range(f5)]
worst = 0.0
for t in range(1, q5):
    T = sum(L[t*g % q5] for g in G5)
    rec = f5 * sum(aL[jj] * w5**(jj*dl[t]) for jj in range(1, m5))
    worst = max(worst, abs(T - rec.real) + abs(rec.imag))
check("T5: pointwise diagonalization (max err < 1e-9)", worst < 1e-9)
# doubling law at (q=7, G=<2>)
q6 = 7
G6, v = [], 1
while True:
    G6.append(v); v = v*2 % q6
    if v == 1:
        break
mx = max(abs(sum(math.log(abs(2*math.cos(math.pi*((t*g) % q6)/q6))) for g in G6))
         for t in range(1, q6))
check("T5: doubling law (2 in G => field == 0)", mx < 1e-12)

print()
if fails:
    raise SystemExit("FAIL: " + ", ".join(fails))
print("FINITE_SIGNED_CENSUS_FRAME_PASS")
