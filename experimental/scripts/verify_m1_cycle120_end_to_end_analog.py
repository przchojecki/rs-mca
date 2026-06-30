#!/usr/bin/env python3
"""
PATH B2: faithful pure-stdlib END-TO-END analog of the Cycle120 mechanism.

Real chain (note m1_cycle120_standalone_ldsw_proof.md):
  Cycle84 census #{Phi(T)}=N
   -> (Lemma1 fixed-jet locator transfer)  LD_sw(RS[F_17^16,D0,137],143) >= N
   -> (scalar extension to F_17^32)
   -> (Lemma2 smooth padding)              LD_sw(RS[F_17^32,H,256],262) >= N.

We rebuild EVERY arrow on a small field where D0 is a GENUINE multiplicative
subgroup (so L_D0 = X^m-1, all e_1..e_{m-1}=0, exactly the cyclotomic structure
of the real D0=256th roots of unity), and EVERYTHING is enumerable:

  census (direct {P_J(beta)} enumeration; shell/occ/m_max/doubles/energy)
   -> Lemma1 (build the actual line (f,g); for every J verify f+z_J g agrees
              with a codeword on D0\\J of size n-j, z_J=1/P_J(beta), noncontainment)
   -> scalar extension F_p -> F_p^2 (noncontainment preserved)
   -> Lemma2 (smooth padding lift to RS[F,H,k+|A|], agreement (n-j)+|A|=m+sigma)
   -> confirm LD_sw == measured occ.

Then a STRUCTURAL-TENSION study of the real fiber-size requirement.
"""
import itertools, math
from collections import Counter

# ----------------------------------------------------------------------------
# F_p arithmetic and polynomials
# ----------------------------------------------------------------------------
def factor(n):
    f={}; d=2
    while d*d<=n:
        while n%d==0: f[d]=f.get(d,0)+1; n//=d
        d+=1
    if n>1: f[n]=f.get(n,0)+1
    return f

def primitive_root(p):
    fac=list(factor(p-1))
    for g in range(2,p):
        if all(pow(g,(p-1)//q,p)!=1 for q in fac): return g
    raise RuntimeError

def subgroup(p,m):
    g=primitive_root(p); h=pow(g,(p-1)//m,p)
    return sorted({pow(h,i,p) for i in range(m)})

def inv(a,p): return pow(a%p,p-2,p)

def pmul(a,b,p):
    if not a or not b: return []
    out=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b): out[i+j]=(out[i+j]+x*y)%p
    return ptrim(out,p)
def ptrim(a,p):
    a=[x%p for x in a]
    while a and a[-1]==0: a.pop()
    return a
def padd(a,b,p):
    out=[0]*max(len(a),len(b))
    for i in range(len(out)): out[i]=((a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0))%p
    return ptrim(out,p)
def psub(a,b,p):
    out=[0]*max(len(a),len(b))
    for i in range(len(out)): out[i]=((a[i] if i<len(a) else 0)-(b[i] if i<len(b) else 0))%p
    return ptrim(out,p)
def peval(f,x,p):
    acc=0
    for c in reversed(f): acc=(acc*x+c)%p
    return acc
def deriv(f,p): return ptrim([(i*f[i])%p for i in range(1,len(f))],p)
def from_roots(roots,p):
    poly=[1]
    for r in roots: poly=pmul(poly,[(-r)%p,1],p)
    return poly
def divmod_monic(num,div,p):
    top=ptrim(num,p); bot=ptrim(div,p)
    assert bot and bot[-1]==1
    q=[0]*max(0,len(top)-len(bot)+1)
    while top and len(top)>=len(bot):
        s=len(top)-len(bot); c=top[-1]%p; q[s]=c
        for i,bc in enumerate(bot): top[s+i]=(top[s+i]-c*bc)%p
        top=ptrim(top,p)
    return ptrim(q,p),top
def interp(xs,ys,p):
    out=[]
    for i,xi in enumerate(xs):
        basis=[1]; den=1
        for jx,xj in enumerate(xs):
            if i==jx: continue
            basis=pmul(basis,[(-xj)%p,1],p); den=den*((xi-xj)%p)%p
        out=padd(out,[ (c*ys[i]*inv(den,p))%p for c in basis ],p)
    return ptrim(out,p)
def is_low_degree_Fp(xs,ys,k,p):
    """does some poly of degree<k pass through all (xs,ys)?  (over F_p)"""
    if k<=0: return all(y%p==0 for y in ys)
    if len(xs)<=k: return True
    cand=interp(xs[:k],ys[:k],p)
    if len(cand)-1>=k: return False
    return all(peval(cand,x,p)==y%p for x,y in zip(xs,ys))

# ----------------------------------------------------------------------------
# F_p^2 arithmetic (for the scalar-extension step)
# ----------------------------------------------------------------------------
def nonresidue(p):
    for a in range(2,p):
        if pow(a,(p-1)//2,p)==p-1: return a
    raise RuntimeError
class F2:
    """element a+b*t, t^2 = NR.  Carries its own p, NR via closure factory."""
    __slots__=("a","b")
    def __init__(s,a,b): s.a=a; s.b=b
def make_F2(p):
    NR=nonresidue(p)
    def add(x,y): return F2((x.a+y.a)%p,(x.b+y.b)%p)
    def sub(x,y): return F2((x.a-y.a)%p,(x.b-y.b)%p)
    def mul(x,y): return F2((x.a*y.a+NR*x.b*y.b)%p,(x.a*y.b+x.b*y.a)%p)
    def eq(x,y): return x.a%p==y.a%p and x.b%p==y.b%p
    def inv2(x):
        d=(x.a*x.a-NR*x.b*x.b)%p; di=inv(d,p)
        return F2((x.a*di)%p,((-x.b)*di)%p)
    def emb(c): return F2(c%p,0)
    return dict(add=add,sub=sub,mul=mul,eq=eq,inv=inv2,emb=emb,zero=F2(0,0),one=F2(1,0))
def is_low_degree_generic(xs,ys,k,F):
    """field-agnostic: does poly deg<k pass through (xs,ys)?  xs,ys are F-elems."""
    if k<=0: return all(F["eq"](y,F["zero"]) for y in ys)
    if len(xs)<=k: return True
    # Lagrange interpolate first k nodes, test the rest
    def lagrange(nodes,vals):
        acc=[F["zero"]]
        for i,xi in enumerate(nodes):
            basis=[F["one"]]; den=F["one"]
            for m,xm in enumerate(nodes):
                if m==i: continue
                nb=[F["zero"]]*(len(basis)+1)          # basis*(X-xm)
                for d,c in enumerate(basis):
                    nb[d]=F["sub"](nb[d],F["mul"](c,xm))
                    nb[d+1]=F["add"](nb[d+1],c)
                basis=nb; den=F["mul"](den,F["sub"](xi,xm))
            scale=F["mul"](vals[i],F["inv"](den))
            basis=[F["mul"](c,scale) for c in basis]
            for d in range(len(basis)):
                if d<len(acc): acc[d]=F["add"](acc[d],basis[d])
                else: acc.append(basis[d])
        return acc
    cand=lagrange(xs[:k],ys[:k])
    # degree check
    deg=len(cand)-1
    while deg>0 and F["eq"](cand[deg],F["zero"]): deg-=1
    if deg>=k: return False
    def ev(poly,x):
        acc=F["zero"]
        for c in reversed(poly): acc=F["add"](F["mul"](acc,x),c)
        return acc
    return all(F["eq"](ev(cand,x),y) for x,y in zip(xs,ys))

# ----------------------------------------------------------------------------
# fixed-jet family + census
# ----------------------------------------------------------------------------
def topkey(J,j,sigma,p):
    poly=from_roots(J,p)            # degree j, poly[j]=1
    return tuple(poly[j-t] for t in range(1,sigma+1))
def largest_fixed_jet_family(D0,j,sigma,p):
    buckets={}
    for J in itertools.combinations(D0,j):
        buckets.setdefault(topkey(J,j,sigma,p),[]).append(J)
    return max(buckets.values(),key=len)
def pjbeta(J,beta,p):
    v=1
    for a in J: v=(v*((beta-a)%p))%p
    return v

def census(family,beta,p):
    vals=[pjbeta(J,beta,p) for J in family]
    c=Counter(vals)
    shell=len(family); occ=len(c)
    mmax=max(c.values())
    hist={s:sum(1 for v in c.values() if v==s) for s in range(1,mmax+1)}
    doubles=hist.get(2,0)
    energy=sum(s*(s-1) for s in c.values())          # ordered off-diagonal
    collisions=shell-occ                              # sum (c_v - 1)
    return dict(vals=vals,counter=c,shell=shell,occ=occ,mmax=mmax,hist=hist,
                doubles=doubles,energy=energy,collisions=collisions,
                zero_value=(0 in c))

# ----------------------------------------------------------------------------
# Lemma 1 : build the actual line (f,g) and verify all four conclusions
# ----------------------------------------------------------------------------
def syndrome(word,D,red,p,LDp_at):
    return [ sum( (pow(x,m,p)*word[idx]%p)*inv(LDp_at[x],p) for idx,x in enumerate(D))%p
             for m in range(red) ]

def lemma1(D0,beta,j,sigma,family,p):
    n=len(D0); k=n-j-sigma; red=j+sigma; agree=n-j
    LD=from_roots(D0,p); LDp=deriv(LD,p)
    LDp_at={x:peval(LDp,x,p) for x in D0}
    LD_beta=peval(LD,beta,p)
    # B=(beta^m), A=-Q_m(beta), independence of Q_m across family
    locs={J:from_roots(J,p) for J in family}
    Avec=[]; Bvec=[pow(beta,m,p) for m in range(red)]
    for m in range(red):
        mono=[0]*m+[1]; qs=set()
        for J in family:
            q,_=divmod_monic(mono,locs[J],p); qs.add(peval(q,beta,p))
        assert len(qs)==1, ("Q_m depends on J", m)
        Avec.append((-qs.pop())%p)
    g={x:(LD_beta*inv((beta-x)%p,p))%p for x in D0}
    gw=[g[x] for x in D0]
    assert syndrome(gw,D0,red,p,LDp_at)==Bvec, "Hg!=B"
    def err(J):
        PJp=deriv(locs[J],p); w={x:0 for x in D0}
        for x in J:
            w[x]=(LDp_at[x]*inv((beta-x)%p,p)%p)*inv(peval(PJp,x,p),p)%p
        return w
    J0=family[0]; e0=err(J0); z0=inv(peval(locs[J0],beta,p),p)
    f={x:(e0[x]-z0*g[x])%p for x in D0}
    assert syndrome([f[x] for x in D0],D0,red,p,LDp_at)==Avec, "Hf!=A"
    zset=set(); ok_line=ok_nc=ok_slope=True; codewords={}
    for J in family:
        eJ=err(J); PJb=peval(locs[J],beta,p); zJ=inv(PJb,p); zset.add(zJ)
        # He_J == A+zB
        exp=[(a+zJ*b)%p for a,b in zip(Avec,Bvec)]
        if syndrome([eJ[x] for x in D0],D0,red,p,LDp_at)!=exp: ok_line=False
        # residual f+zg-e in ker H
        resid=[(f[x]+zJ*g[x]-eJ[x])%p for x in D0]
        if any(c!=0 for c in syndrome(resid,D0,red,p,LDp_at)): ok_line=False
        # line point on D0\J equals a degree<k codeword
        comp=[x for x in D0 if x not in set(J)]
        cwvals=[(f[x]+zJ*g[x])%p for x in comp]
        cpoly=interp(comp,cwvals,p)
        if len(cpoly)-1>=k: ok_line=False
        if len(comp)!=agree: ok_line=False
        codewords[J]=(comp,cpoly)
        # noncontainment: g on D0\J is NOT degree<k
        if is_low_degree_Fp(comp,[g[x] for x in comp],k,p): ok_nc=False
        if zJ!=inv(PJb,p): ok_slope=False
    return dict(n=n,k=k,sigma=sigma,agree=agree,family=family,f=f,g=g,
                z_distinct=len(zset),codewords=codewords,
                ok_line=ok_line,ok_noncontain=ok_nc,ok_slope=ok_slope,
                LDp_at=LDp_at)

# ----------------------------------------------------------------------------
# scalar extension F_p -> F_p^2 : noncontainment preserved
# ----------------------------------------------------------------------------
def scalar_extension_check(D0,L1,p,ntest=6):
    F=make_F2(p); g=L1["g"]; k=L1["k"]
    same=True; checked=0
    for J in L1["family"][:ntest]:
        comp=[x for x in D0 if x not in set(J)]
        over_p=is_low_degree_Fp(comp,[g[x] for x in comp],k,p)
        xs=[F["emb"](x) for x in comp]; ys=[F["emb"](g[x]) for x in comp]
        over_p2=is_low_degree_generic(xs,ys,k,F)
        if over_p!=over_p2: same=False
        checked+=1
    return dict(checked=checked,both_noncontain=same and not over_p2)

# ----------------------------------------------------------------------------
# Lemma 2 : smooth padding lift  (D0 -> H = D0 u A u R)
# ----------------------------------------------------------------------------
def lemma2(D0,H,L1,p):
    k=L1["k"]; n=L1["n"]; f=L1["f"]; g=L1["g"]
    other=[x for x in H if x not in set(D0)]          # the odd coset, size m
    A=other[:n-k]; R=other[n-k:]                      # |A|=n-k, |R|=k  (real:119,137)
    LA=from_roots(A,p)
    full=list(D0)+A+R
    lift_dim=k+len(A); lift_agree=L1["agree"]+len(A)
    fp={}; gp={}
    for x in D0: fp[x]=peval(LA,x,p)*f[x]%p; gp[x]=peval(LA,x,p)*g[x]%p
    for x in A: fp[x]=0; gp[x]=0
    for x in R: fp[x]=0; gp[x]=0
    ok_line=ok_nc=True
    for J in L1["family"]:
        comp,cpoly=L1["codewords"][J]
        lift_supp=comp+A
        lifted_cw=pmul(LA,cpoly,p)
        if len(lifted_cw)-1>=lift_dim: ok_line=False
        # lifted line point on (D0\J) u A must equal lifted_cw evaluated there
        # (f_+ + z g_+) = L_A*(f+zg) = L_A*codeword on D0\J ; =0=L_A*cw? on A (L_A=0)
        for x in comp:
            zJ=inv(pjbeta(J,L1_betaval[0],p),p)
            lhs=(fp[x]+zJ*gp[x])%p; rhs=peval(lifted_cw,x,p)
            if lhs!=rhs: ok_line=False
        for x in A:
            if peval(LA,x,p)!=0: ok_line=False
        if len(lift_supp)!=lift_agree: ok_line=False
        # noncontainment of g_+ on (D0\J) u A
        xs=lift_supp; ys=[gp[x] for x in lift_supp]
        if is_low_degree_Fp(xs,ys,lift_dim,p): ok_nc=False
    return dict(A=len(A),R=len(R),lift_n=len(full),lift_dim=lift_dim,
                lift_agree=lift_agree,ok_line=ok_line,ok_noncontain=ok_nc)

# ----------------------------------------------------------------------------
# RUN one faithful instance
# ----------------------------------------------------------------------------
def run_instance(p,m,j,sigma,beta,label):
    global L1_betaval
    L1_betaval=[beta]
    D0=subgroup(p,m); H=subgroup(p,2*m)
    assert set(D0)<=set(H), "D0 must be subgroup of H"
    assert beta not in D0
    # cyclotomic check: L_D0 = X^m - 1
    LD=from_roots(D0,p); expect=[(-1)%p]+[0]*(m-1)+[1]
    cyclo = (LD==expect)
    family=largest_fixed_jet_family(D0,j,sigma,p)
    cs=census(family,beta,p)
    L1=lemma1(D0,beta,j,sigma,family,p)
    se=scalar_extension_check(D0,L1,p)
    L2=lemma2(D0,H,L1,p)
    out=dict(label=label,p=p,m=m,j=j,sigma=sigma,beta=beta,k=L1["k"],
             cyclotomic_LD0_is_Xm_minus_1=cyclo,
             shell=cs["shell"],occ=cs["occ"],mmax=cs["mmax"],
             doubles=cs["doubles"],energy=cs["energy"],collisions=cs["collisions"],
             hist=cs["hist"],
             bookkeeping_occ_eq_shell_minus_collisions=(cs["occ"]==cs["shell"]-cs["collisions"]),
             bookkeeping_mmax2_occ_eq_shell_minus_doubles=
                 (cs["mmax"]<=2 and cs["occ"]==cs["shell"]-cs["doubles"]),
             bookkeeping_energy_eq_2doubles_if_mmax2=
                 (cs["mmax"]>2 or cs["energy"]==2*cs["doubles"]),
             L1_distinct_z=L1["z_distinct"],
             L1_distinct_z_eq_occ=(L1["z_distinct"]==cs["occ"]),
             L1_ok_line=L1["ok_line"],L1_ok_noncontain=L1["ok_noncontain"],
             L1_ok_slope=L1["ok_slope"],
             L1_native_code="RS[F_%d,D0(|%d|),k=%d] agree=%d"%(p,m,L1["k"],L1["agree"]),
             scalarext_checked=se["checked"],scalarext_preserved=se["both_noncontain"],
             L2_A=L2["A"],L2_R=L2["R"],L2_lift_n=L2["lift_n"],
             L2_lift_dim=L2["lift_dim"],L2_lift_agree=L2["lift_agree"],
             L2_ok_line=L2["ok_line"],L2_ok_noncontain=L2["ok_noncontain"],
             L2_lift_code="RS[F_%d,H(|%d|),k=%d] agree=%d"%(p,2*m,L2["lift_dim"],L2["lift_agree"]),
             padding_agree_eq_m_plus_sigma=(L2["lift_agree"]==m+sigma),
             LDsw_lower_bound=cs["occ"],
             LDsw_equals_occ=(L1["z_distinct"]==cs["occ"]
                              and L1["ok_line"] and L1["ok_noncontain"]
                              and L2["ok_line"] and L2["ok_noncontain"]))
    return out

if __name__=="__main__":
    insts=[
        run_instance(193,16,8,1,10,"primary-rich (sigma=1, m_max=2, 20 doubles)"),
        run_instance(97,16,8,2,95,"secondary (sigma=2, multi-coeff jet fixed)"),
        run_instance(73,12,6,1,5,"tertiary (smaller, sigma=1)"),
    ]
    for o in insts:
        print("="*78)
        print("INSTANCE:",o["label"])
        print(" F_%d  D0=<g> order %d (mult. subgroup)  beta=%d  j=%d sigma=%d k=%d"
              %(o["p"],o["m"],o["beta"],o["j"],o["sigma"],o["k"]))
        print(" cyclotomic L_D0 = X^%d - 1 :"%o["m"],o["cyclotomic_LD0_is_Xm_minus_1"])
        print(" CENSUS  shell=%d  occ=%d  m_max=%d  doubles=%d  energy=%d  collisions=%d  hist=%s"
              %(o["shell"],o["occ"],o["mmax"],o["doubles"],o["energy"],o["collisions"],o["hist"]))
        print("   [%s] occ = shell - collisions"%("OK" if o["bookkeeping_occ_eq_shell_minus_collisions"] else "FAIL"))
        print("   [%s] (m_max<=2) occ = shell - doubles"%("OK" if o["bookkeeping_mmax2_occ_eq_shell_minus_doubles"] else "n/a"))
        print("   [%s] energy = 2*doubles"%("OK" if o["bookkeeping_energy_eq_2doubles_if_mmax2"] else "FAIL"))
        print(" LEMMA1  %s"%o["L1_native_code"])
        print("   distinct z_J=%d  (== occ: %s)"%(o["L1_distinct_z"],o["L1_distinct_z_eq_occ"]))
        print("   [%s] line: f+z_J g = codeword on D0\\J (size n-j), all J"%("OK" if o["L1_ok_line"] else "FAIL"))
        print("   [%s] slopes z_J = 1/P_J(beta)"%("OK" if o["L1_ok_slope"] else "FAIL"))
        print("   [%s] noncontainment: g not explained on D0\\J, all J"%("OK" if o["L1_ok_noncontain"] else "FAIL"))
        print(" SCALAR-EXT F_%d -> F_%d^2 : noncontainment preserved on %d supports : %s"
              %(o["p"],o["p"],o["scalarext_checked"],o["scalarext_preserved"]))
        print(" LEMMA2  %s"%o["L2_lift_code"])
        print("   |A|=%d |R|=%d  lift_n=%d lift_dim=%d lift_agree=%d  (= m+sigma: %s)"
              %(o["L2_A"],o["L2_R"],o["L2_lift_n"],o["L2_lift_dim"],o["L2_lift_agree"],
                o["padding_agree_eq_m_plus_sigma"]))
        print("   [%s] lifted line agrees with L_A*codeword on (D0\\J) u A, all J"%("OK" if o["L2_ok_line"] else "FAIL"))
        print("   [%s] lifted noncontainment of g_+ on (D0\\J) u A, all J"%("OK" if o["L2_ok_noncontain"] else "FAIL"))
        print(" >>> LD_sw(%s) >= %d   and construction realizes exactly occ=%d distinct params"
              %(o["L2_lift_code"],o["LDsw_lower_bound"],o["occ"]))
        print(" >>> END-TO-END LD_sw == measured occ : %s"%o["LDsw_equals_occ"])
    print("="*78)
    allok=all(o["LDsw_equals_occ"] and o["L1_ok_line"] and o["L1_ok_noncontain"]
              and o["L2_ok_line"] and o["L2_ok_noncontain"] and o["scalarext_preserved"]
              and o["cyclotomic_LD0_is_Xm_minus_1"] for o in insts)
    print("ALL INSTANCES PASS:",allok)
