#!/usr/bin/env python3
"""Probe the char-0 list-side sharpness questions of Paper B (slackMCA_v4).

Q1 (2-power, tightness of cor:upstairs-poly): exact max char-0 prefix fiber vs 2^{n/M0}.
Q2 (mixed-radix, fate of thm:upstairs): for n NOT a power of two, are char-0 prefix
    fibers still unions of cosets of a single subgroup mu_M? Is the size bound 2^{n/M0}
    still valid, or is it VIOLATED (=> the 2-power hypothesis is load-bearing, candidate
    sharpness remark / obstruction to the Part-III circle/Chebyshev transfer)?

Exact char-0 keys via a faithful fingerprint prime P == 1 mod n with
P > (2*C(s, s//2))^{phi(n)} (each archimedean conjugate of e_i(S)-e_i(T) has modulus
<= 2*C(s, s//2); its Q(zeta)/Q norm is then < P, so the degree-one prime above P sees
no nonzero char-0 prefix difference). Pure stdlib.
"""
from itertools import combinations
from math import comb, gcd


def is_prime(num):
    if num < 2: return False
    for sp in (2,3,5,7,11,13,17,19,23,29,31,37):
        if num % sp == 0: return num == sp
    d, r = num-1, 0
    while d % 2 == 0: d//=2; r+=1
    for a in (2,3,5,7,11,13,17,19,23,29,31,37):
        x = pow(a,d,num)
        if x in (1,num-1): continue
        for _ in range(r-1):
            x = x*x % num
            if x == num-1: break
        else: return False
    return True

def prime_factors(n):
    f,d,m=set(),2,n
    while d*d<=m:
        while m%d==0: f.add(d); m//=d
        d+=1
    if m>1: f.add(m)
    return f

def prime_1modn_above(n, lo):
    t = max(1,(max(lo,2)-1+n-1)//n)
    while True:
        p = 1+n*t
        if p>=lo and is_prime(p): return p
        t+=1

def order_n_element(p,n):
    pf,cof = prime_factors(n),(p-1)//n
    g=2
    while True:
        h=pow(g,cof,p)
        if h!=1 and all(pow(h,n//q,p)!=1 for q in pf): return h
        g+=1

def prefix_mod(elts,sigma,p):
    c=[0]*(sigma+1); c[0]=1
    for a in elts:
        for j in range(sigma,0,-1):
            c[j]=(c[j]+a*c[j-1])%p
    return tuple(c[1:sigma+1])

def subgroups_of_cyclic(n):
    # return dict M -> the order-M subgroup as a frozenset of exponents (multiples of n//M)
    out={}
    M=1
    for M in range(1,n+1):
        if n%M==0:
            out[M]=frozenset(range(0,n,n//M))
    return out

def coset_union_M(diff_exps, n, M):
    # is the exponent-set diff_exps a union of cosets of the order-M subgroup?
    step=n//M
    sub=set(range(0,n,step))
    ds=set(diff_exps)
    seen=set()
    for e in ds:
        if e in seen: continue
        coset={(e+k)%n for k in sub}
        if not coset<=ds: return False
        seen|=coset
    return True

def quotient_periodic_M(diff_exps,n):
    # largest M>1 with diff a union of order-M cosets (M | n); 1 if none.
    best=1
    for M in range(2,n+1):
        if n%M==0 and coset_union_M(diff_exps,n,M):
            best=M
    return best

def analyze(n, s, sigma):
    phi = sum(1 for a in range(1,n+1) if gcd(a,n)==1)
    P = prime_1modn_above(n, (2*comb(s, s//2))**phi + 1)
    g = order_n_element(P,n)
    powers=[pow(g,a,P) for a in range(n)]
    fibers={}
    for A in combinations(range(n), s):
        key=prefix_mod([powers[a] for a in A], sigma, P)
        fibers.setdefault(key,[]).append(A)
    M0=1
    while M0<=sigma: M0<<=1
    sizes=[len(v) for v in fibers.values()]
    maxsz=max(sizes)
    # examine structure of largest fibers: are pairwise sym-diffs coset-unions?
    nonperiodic=[]
    worstM=None
    for key,sets in fibers.items():
        if len(sets)<2: continue
        S0=set(sets[0])
        for B in sets[1:]:
            diff=S0.symmetric_difference(set(B))
            M=quotient_periodic_M(diff,n)
            if M==1:
                nonperiodic.append((sorted(S0),sorted(B),sorted(diff)))
            if worstM is None or M<worstM:
                worstM=M
    bound=2**(n//M0)
    return {
        "n":n,"s":s,"sigma":sigma,"M0":M0,"phi":phi,"P_bits":P.bit_length(),
        "num_subsets":sum(sizes),"num_fibers":len(fibers),
        "max_char0_fiber":maxsz,"bound_2^(n/M0)":bound,
        "tight?":maxsz==bound,"violates_bound?":maxsz>bound,
        "min_periodicity_M_over_collisions":worstM,
        "num_nonperiodic_pairs":len(nonperiodic),
        "example_nonperiodic":nonperiodic[0] if nonperiodic else None,
        "is_pow2_n": (n&(n-1))==0,
    }

if __name__=="__main__":
    print("== Q1: 2-power n, tightness of cor:upstairs-poly bound 2^(n/M0) ==")
    for (n,s,sigma) in [(8,4,1),(8,4,2),(8,4,3),(16,8,1),(16,8,2),(16,8,3),(16,8,4),
                         (16,4,2),(16,12,2),(16,6,3)]:
        r=analyze(n,s,sigma)
        print(f"  n={n:2d} s={s:2d} sig={sigma} M0={r['M0']:2d} | max char0 fiber={r['max_char0_fiber']:5d} "
              f"vs 2^(n/M0)={r['bound_2^(n/M0)']:5d}  tight={r['tight?']} violate={r['violates_bound?']} "
              f"minM={r['min_periodicity_M_over_collisions']}")
    print("== Q2: mixed-radix n (NOT power of two): does thm:upstairs survive? ==")
    for (n,s,sigma) in [(6,3,1),(12,6,1),(12,6,2),(12,4,1),(12,4,2),(12,8,2),
                         (9,4,1),(9,3,1),(18,9,1),(18,9,2),(24,12,2),(10,5,1),(15,5,1)]:
        r=analyze(n,s,sigma)
        print(f"  n={n:2d} s={s:2d} sig={sigma} M0={r['M0']:2d} | max char0 fiber={r['max_char0_fiber']:5d} "
              f"vs 2^(n/M0)={r['bound_2^(n/M0)']:6d}  violate={r['violates_bound?']} "
              f"nonperiodic_pairs={r['num_nonperiodic_pairs']} minM={r['min_periodicity_M_over_collisions']}")
        if r['example_nonperiodic']:
            S0,B,diff=r['example_nonperiodic']
            print(f"      NONPERIODIC: S0={S0} B={B} symdiff(exps)={diff}")
