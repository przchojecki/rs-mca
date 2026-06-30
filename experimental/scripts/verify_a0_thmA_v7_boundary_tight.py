# Verify the deep-point internals of thm:A and the TIGHTNESS of the f<=n-k-1 admissibility,
# i.e. that the C->C+ degree drop is exactly 1 and the radius cutoff 1-rho-1/n is exactly right.
p=41
def powmod(a,e): return pow(a%p,e,p)
def inv(a): return pow(a%p,p-2,p)

# pick D as subgroup order n=8, k arbitrary <=  ; F=GF(41), 41-1=40, n=8|40
g=None
def order(x):
    o=1;y=x%p
    while y!=1: y=(y*x)%p;o+=1
    return o
for c in range(2,p):
    if order(c)==40: g=c;break
g8=powmod(g,40//8)
D=sorted({powmod(g8,i) for i in range(8)}); n=8
Omega=[a for a in range(p) if a not in set(D)]   # F\D

# (3) deep-point degree drop: for P of degree exactly k, (P(X)-P(alpha))/(X-alpha) has degree exactly k-1
def poly_eval(coeffs,x): return sum(c*powmod(x,i) for i,c in enumerate(coeffs))%p
def deflate(coeffs, alpha):
    # divide P(X)-P(alpha) by (X-alpha); return quotient coeffs (synthetic division)
    Pa=poly_eval(coeffs,alpha)
    num=coeffs[:]; num[0]=(num[0]-Pa)%p
    # synthetic division of num by (X-alpha): root=alpha
    q=[0]*(len(num)-1); rem=0; carry=0
    # do it from top degree down
    deg=len(num)-1
    c=[0]*deg
    acc=0
    coef=num[:]  # ascending
    # convert to descending
    desc=coef[::-1]
    out=[]; cur=0
    for d in desc:
        cur=(cur*alpha + d)%p
        out.append(cur)
    # out[-1] should be remainder = num(alpha)=0
    rem=out[-1]
    quot_desc=out[:-1]
    quot=quot_desc[::-1]
    return quot, rem

import random
random.seed(1)
for k in [3,4,5]:
    # random P of degree exactly k
    coeffs=[random.randrange(p) for _ in range(k+1)]
    if coeffs[k]==0: coeffs[k]=1
    alpha=Omega[0]
    quot,rem=deflate(coeffs,alpha)
    assert rem==0
    qdeg=max([i for i,c in enumerate(quot) if c!=0],default=-1)
    assert qdeg==k-1, (k,qdeg)
print("(3) deep-point degree drop is EXACTLY 1 (deg k -> deg k-1) : OK  (line-point lands in C=deg<k)")

# (4)&(5) far-condition tightness: g_alpha(x) = -1/(x-alpha).
# Claim: no G in F[X]_{<k} agrees with g_alpha on > k points; and =k IS achievable.
# So common-support must be <= k; admissibility needs support a=n-f >= k+1 (f<=n-k-1).
# Show at the ALLOWED endpoint f=n-k-1 (support k+1) the far-cond holds (matching impossible),
# and at the FORBIDDEN f=n-k (support k) a degree-<k poly CAN match g_alpha on k pts (far-cond breaks).
def gval(x,alpha): return (-inv((x-alpha)%p))%p

# Lagrange interpolation through k points (degree <= k-1) over GF(p)
def interp(points):  # points: list of (x,y); returns coeff list ascending, degree<=len-1
    xs=[x for x,_ in points]; ys=[y for _,y in points]
    m=len(points)
    # build via Newton/Lagrange straightforwardly
    coeffs=[0]*m
    for i in range(m):
        # basis poly L_i(X)=prod_{j!=i}(X-xj)/(xi-xj)
        num=[1]  # ascending
        den=1
        for j in range(m):
            if j==i: continue
            # multiply num by (X - xs[j])
            new=[0]*(len(num)+1)
            for t,c in enumerate(num):
                new[t]=(new[t]-c*xs[j])%p
                new[t+1]=(new[t+1]+c)%p
            num=new
            den=(den*((xs[i]-xs[j])%p))%p
        f=(ys[i]*inv(den))%p
        for t in range(len(num)):
            if t<len(coeffs): coeffs[t]=(coeffs[t]+f*num[t])%p
    return coeffs

for k in [3,4,5]:
    alpha=Omega[0]
    Dl=list(D)
    # ALLOWED endpoint: support size k+1 -> try to find G deg<k matching g_alpha on k+1 pts of D
    # Theory says impossible. Brute: interpolate through any k pts (deg<=k-1) then check if a (k+1)th matches.
    found_kplus1=False
    from itertools import combinations
    for S in combinations(Dl, k+1):
        # a deg<=k-1 poly is determined by k points; check if it can pass through all k+1 with values g_alpha
        pts=[(x,gval(x,alpha)) for x in S[:k]]
        G=interp(pts)              # deg<=k-1
        gdeg=max([i for i,c in enumerate(G) if c!=0],default=-1)
        if gdeg>k-1: continue
        if poly_eval(G,S[k])==gval(S[k],alpha):
            found_kplus1=True;break
    assert not found_kplus1, f"k={k}: a deg<k poly matched g_alpha on k+1 points -> far-cond would BREAK at allowed endpoint!"
    # FORBIDDEN: support size k -> matching on k points IS achievable (interp k pts, deg<=k-1<k)
    S=tuple(Dl[:k])
    pts=[(x,gval(x,alpha)) for x in S]
    G=interp(pts); gdeg=max([i for i,c in enumerate(G) if c!=0],default=-1)
    ok=all(poly_eval(G,x)==gval(x,alpha) for x in S) and gdeg<=k-1
    assert ok
    print(f"  k={k}: support k+1 (f=n-k-1) -> NO degree-<k match (far-cond HOLDS, allowed); "
          f"support k (f=n-k) -> degree-<k match EXISTS (far-cond BREAKS, correctly excluded)")
print("(4)&(5) admissibility cutoff f<=n-k-1  i.e. delta<=1-rho-1/n is EXACTLY tight : OK")
