# Fixed-endpoint owner router for rank-eleven pair anticodes

## 1. Setup

Use the KoalaBear row

```text
n=2097152,  K=1048576,  m=1116048,  w=m-K=67472,
B*=274980728111395087,  2w=134944.
```

After the parent gauge, let the explanation direction code `C'` have
dimension `s<=10`.  For each low-margin selected slope, fix the actual
minimizing pair from #1168.  In an affine basis of `C'`, write its pair
coefficient matrix as `M_e in F^(2 x s)`.

The parent nonuniform resource is

```text
sum_gamma theta_gamma <= C_10
C_10=106618568137036225644.
```

Fix an integer cutoff `1<=tau<w`, put

```text
A=m-tau,  d=A-K=w-tau,
L={gamma:theta_gamma<=tau},
H={gamma:theta_gamma>=tau+1}.
```

Then

```text
|H| <= floor(C_10/(tau+1)).                              (1)
```

For a low record assigned to pair `e=(a_e,b_e)`, its complete pair core

```text
H_e={x:r_0(x)=a_e(x), r_1(x)=b_e(x)}
```

has size at least `m-theta_gamma>=A`.

## 2. Fixed-left geometry produces a fixed endpoint

Assume the low pair types form the fixed-left branch of #1171:

```text
M_e=M_0+u v_e^T,  u=(alpha,beta)!=0.                    (2)
```

Choose row functionals `ell,t in (F^2)^*` with

```text
ell(u)=0,  t(u)=1.
```

Apply the invertible row operation `(ell,t)` simultaneously to the received
pair and every codeword pair.  Write

```text
(R,S)=(ell(r_0,r_1),t(r_0,r_1)),
(c,d_e)=(ell(a_e,b_e),t(a_e,b_e)).
```

Equation (2) gives

```text
c independent of e,
d_e=d_0+P_e,
```

where the distinct `P_e` lie in an affine Reed--Solomon direction space of
dimension `r<=s`.

Put

```text
G={x in D:R(x)=c(x)},  g=|G|.                            (3)
```

Since `H_e subset G`, every low pair gives `g>=A` and `d_e` agrees with `S`
on at least `A` coordinates of `G`.

## 3. Ordinary affine-list count on G

Restriction to `G` is injective because `g>=A>K`.  Apply the ordinary
affine-span Reed--Solomon list theorem on the punctured evaluation domain
`G`.  The number `N_g` of distinct varying endpoints satisfies

```text
N_g <= floor( C(g-K+r,r) / C(A-K+r,r) )
    <= floor( C(g-K+s,s) / C(A-K+s,s) ).                 (4)
```

The second inequality follows from

```text
C(x+r,r)/C(d+r,r)=prod_(j=1)^r (x+j)/(d+j),  x>=d,
```

which is nondecreasing in `r`.

## 4. Outside-G owner injection

The original finite affine slopes map injectively under the row operation to
a subset of the projective line.  At most one image has zero coefficient on
the varying endpoint `S`; reserve that slope.

Consider every other selected slope assigned to pair `e`, and let `T_gamma`
be its exact size-`m` bad support.  If `T_gamma subset G`, then on all of
`T_gamma` the fixed endpoint satisfies `R=c`.  The transformed affine
combination and its explanation by `(c,d_e)` then force `S=d_e` on the same
support.  This is simultaneous pair containment, contrary to the actual
same-support badness.  Hence

```text
T_gamma meets D\\G.                                      (5)
```

At `x notin G`, the fixed-endpoint error `R(x)-c(x)` is nonzero.  For fixed
pair type `e`, the transformed two-endpoint affine equation at `x` determines
one projective slope.  Choosing one outside coordinate in (5) therefore
injects the slopes owned by `e` into `D\\G`.  Thus

```text
one pair type owns at most n-g nonexceptional slopes.     (6)
```

Combining (4)--(6),

```text
|L| <= 1+(n-g) floor(C(g-K+s,s)/C(A-K+s,s)).              (7)
```

## 5. Closed deployed envelope

Write `x=g-K` and `d=A-K=w-tau`.  Since `n=2K`, equation (7) gives

```text
|L| <= 1+ floor(
 max_(d<=x<=K) (K-x) C(x+s,s)/C(d+s,s)
).                                                        (8)
```

For fixed `x>=d`, the ratio is largest at `s=10`.  Put

```text
F(x)=(K-x) C(x+10,10).
```

Its successive ratio satisfies

```text
F(x+1)>F(x)
iff (K-x-1)(x+11)>(K-x)(x+1)
iff x<(10K-11)/11.
```

Therefore the unique integer maximizer is

```text
x*=953250,
g*=K+x*=2001826,
n-g*=95326.                                               (9)
```

The theorem-level low envelope is

```text
L_left(tau)=1+floor(
 95326 C(953260,10)/C(67472-tau+10,10)
).                                                        (10)
```

No numerical maximization over `g` is load-bearing.

## 6. First payment and exact optimum

At the first paying cutoff `tau=439`,

```text
A=1115609,
d=67033,
L_left(439)=32215263489919749,
floor(C_10/440)=242314927584173240.
```

Adding the disjoint near charge gives

```text
134944
+242314927584173240
+32215263489919749
=274530191074227933
<B*,                                                       (11)
```

with slack

```text
450537037167154.
```

The adjacent cutoff `tau=438` gives

```text
275077356203816531>B*
```

by `96628092421444`; hence `439` is the first paying cutoff of the declared
envelope.  The complete exact scan has unique minimum at `tau=3608`:

```text
81826485385525648,
```

with slack `193154242725869439`.  The minimum is calibration only; (11) is
the stronger structural cutoff.

The exact floor scan beneath the analytic envelope at `tau=439` is

```text
max_x (K-x) floor(C(x+10,10)/C(67043,10))
=32215263489916276
```

at the same `x*=953250`.  The theorem deliberately uses the larger analytic
envelope in (10).

## 7. Complete rank-one anticode payment

If the low pair types are pairwise rank one, #1171 gives fixed-right or
fixed-left geometry.

- Fixed right: #1171 gives `|L|<=8147918`, so at `tau=439` the full total is
  `242314927592456102`, with slack `32665800518938985`.
- Fixed left: equation (11) pays the branch.

Thus an over-budget rank-eleven line has two low pair types `e,f` with

```text
rank(M_e-M_f)=2.                                          (12)
```

## 8. Rank-two large-common-factor terminal

Both complete cores have size at least `A=1115609`, so

```text
|H_e intersect H_f|
>=|H_e|+|H_f|-n
>=2A-n
=134066.                                                   (13)
```

At every coordinate in this intersection, both degree-`<K` differences

```text
a_e-a_f,  b_e-b_f
```

vanish.  Their coefficient rows are independent by (12), but the squarefree
locator of the intersection divides both.  Hence their polynomial gcd has
degree at least `134066`.

This is the exact successor terminal.  The packet does not choose a factor
owner, sum edgewise cancellations, or assert that multiple rank-two edges
share the same factor.
