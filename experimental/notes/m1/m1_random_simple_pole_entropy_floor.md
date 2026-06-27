# M1 Random Simple-Pole Entropy Floor

**Status:** PROVED / FINITE-SLOPE LOWER-BOUND / AUDIT.

**Agent/model:** Codex.

**Date:** 2026-06-27.

This note proves a general random simple-pole lower bound for finite bad
slopes.  The main specialization is the row

```text
F = F_17[z]/(z^32 - 3),        H=<z>,        |H|=512,
C = RS[F,H,256] = {Q|_H : deg Q < 256}.
```

For this row, there are simple-pole received lines with the following finite
bad-slope floors:

```text
a = 257: all 17^32 finite slopes are bad,
a = 258: all 17^32 finite slopes are bad,
a = 259: at least 17^32 - 68,904 finite slopes are bad,
a = 260: at least
33,439,260,151,101,646,297,506,087,371,119,470
> 2^114
finite slopes are bad.
```

These are separate existence statements.  The note does not claim that one
received line realizes all four agreement levels simultaneously.  It is also
not a safe-side theorem, not an ordinary list-decoding theorem, and not a
protocol theorem.  It counts finite slopes only.

The companion verifier is:

```text
python3 experimental/scripts/verify_m1_random_simple_pole_entropy_floor.py
python3 experimental/scripts/verify_m1_random_simple_pole_entropy_floor.py --json
```

It checks the exact integer lower bounds in the `F_17^32` specialization and
validates the JSON certificate:

```text
experimental/data/m1_random_simple_pole_entropy_floor.json
```

## Predicate

For a line `(f,g)` and agreement `a`, define

```text
N_bad^fin(f,g,a)
=
# { gamma in F :
    exists Q in F[X], deg Q < k,
    |{x in D : Q(x)=f(x)+gamma g(x)}| >= a }.
```

This is the finite-slope support-wise LD/MCA predicate used in this note.  It
does not count an infinite/projective slope, an interleaved-list size, an
ordinary list-decoding list, or a protocol soundness probability.

## General Theorem

Let `F` be a finite field with `|F|=q`.  Let

```text
D subset F,        |D|=n,
beta in F \ D,
```

and let the base Reed-Solomon code be

```text
RS[F,D,k] = {Q|_D : deg Q < k}.
```

Assume

```text
k < a <= n.
```

Put

```text
C_a = binom(n,a),
s = a-k,
R_a = sum_{v=0}^{a-k-1} binom(a,v) binom(n-a,v) / q^v.
```

Use the standard convention that `binom(m,v)=0` if `v<0` or `v>m`.

Then there exists a received numerator word `U : D -> F` such that the
simple-pole line

```text
f(x) = U(x)/(x-beta),
g(x) = -1/(x-beta)
```

has at least

```text
ceil( q C_a / (C_a + R_a q^s) )
```

finite bad slopes at agreement `a`; that is,

```text
N_bad^fin(f,g,a)
>= ceil( q C_a / (C_a + R_a q^s) ).
```

## Proof

Fix a finite slope value

```text
gamma in F.
```

Let

```text
V_gamma = {P in F[X] : deg P <= k and P(beta)=gamma}.
```

The space of polynomials of degree at most `k` has dimension `k+1`, and
evaluation at `beta` is a nonzero linear functional.  Hence `V_gamma` is an
affine space of size

```text
|V_gamma| = q^k.
```

Choose a random word `U : D -> F` uniformly.

For fixed `gamma`, define

```text
X_gamma(U)
=
# { (P,S) :
      P in V_gamma,
      S subset D,
      |S| = a,
      P(x)=U(x) for every x in S }.
```

Thus `X_gamma(U)>0` means that there is a degree-`<=k` numerator polynomial
with deep value `gamma` agreeing with `U` on at least `a` points.

For a fixed pair `(P,S)`, the probability that `P|_S = U|_S` is `q^(-a)`.
Therefore

```text
E X_gamma
= |V_gamma| binom(n,a) q^(-a)
= q^k C_a q^(-a)
= C_a / q^(a-k).
```

Write

```text
mu_a = C_a / q^s,        s=a-k.
```

## Second Moment

We bound `E X_gamma^2`.  Take two certificates

```text
(P,S),        (P',S')
```

for the same `gamma`.  Put

```text
I = S cap S',        u = |I|.
```

For both certificates to hold, one must have

```text
P(x)=P'(x)        for every x in I.
```

Also `P(beta)=P'(beta)=gamma`.  Thus `D_0=P-P'` satisfies

```text
deg D_0 <= k,
D_0(beta)=0,
D_0|_I=0.
```

### Case 1: `u <= k`

The `u` points of `I`, together with `beta`, impose `u+1` independent linear
conditions on the `(k+1)`-dimensional polynomial space `deg <= k`.  Therefore,
after choosing `P`, there are at most

```text
q^(k-u)
```

choices for the difference `D_0=P-P'`.

Since there are `q^k` choices for `P in V_gamma`, there are at most

```text
q^(2k-u)
```

compatible ordered pairs `(P,P')`.

Given compatibility, the random word `U` must match prescribed values on
`S union S'`, whose size is `2a-u`.  So the probability factor is
`q^(-(2a-u))`.  Each ordered support pair with `u <= k` contributes at most

```text
q^(2k-u) q^(-(2a-u)) = q^(2k-2a).
```

Summing over all ordered support pairs gives at most

```text
C_a^2 q^(2k-2a)
= (C_a / q^(a-k))^2
= mu_a^2.
```

### Case 2: `u > k`

Then `P-P'` has more than `k` roots in `D`, while `deg(P-P') <= k`.  Hence

```text
P=P'.
```

Write

```text
v = a-u.
```

Since `u > k`, we have

```text
v <= a-k-1.
```

For fixed `S`, the number of sets `S'` with `|S cap S'| = a-v` is

```text
binom(a,v) binom(n-a,v).
```

For fixed `P=P'`, the word `U` must agree with `P` on `S union S'`, whose
size is `a+v`.  The contribution from this near-diagonal region is therefore

```text
q^k C_a
sum_{v=0}^{a-k-1}
binom(a,v) binom(n-a,v) q^(-(a+v)).
```

Since `mu_a = C_a / q^(a-k)`, this equals

```text
mu_a R_a,
```

where

```text
R_a =
sum_{v=0}^{a-k-1}
binom(a,v) binom(n-a,v) / q^v.
```

Combining the two cases,

```text
E X_gamma^2 <= mu_a^2 + R_a mu_a.
```

## Existence of Many Deep Values

By Cauchy-Schwarz,

```text
Pr[X_gamma > 0]
>= (E X_gamma)^2 / E X_gamma^2.
```

Thus

```text
Pr[X_gamma > 0]
>= mu_a^2 / (mu_a^2 + R_a mu_a)
= mu_a / (mu_a + R_a).
```

Substituting `mu_a = C_a/q^s` gives

```text
Pr[X_gamma > 0]
>= C_a / (C_a + R_a q^s).
```

Let

```text
B(U,a) = # {gamma in F : X_gamma(U)>0}.
```

By linearity of expectation,

```text
E_U B(U,a) >= q C_a / (C_a + R_a q^s).
```

Since `B(U,a)` is an integer, there exists at least one `U` such that

```text
B(U,a) >= ceil( q C_a / (C_a + R_a q^s) ).
```

This proves the entropy certificate floor for numerator deep values.

## Simple-Pole Conversion

Fix such a word `U`.  Define

```text
f(x) = U(x)/(x-beta),
g(x) = -1/(x-beta).
```

If `X_gamma(U)>0`, then there exist `P_gamma in F[X]` and `S_gamma subset D`
such that

```text
deg P_gamma <= k,
P_gamma(beta)=gamma,
|S_gamma|=a,
P_gamma(x)=U(x)        for every x in S_gamma.
```

Since `P_gamma(beta)=gamma`, the quotient

```text
Q_gamma(X) = (P_gamma(X)-gamma)/(X-beta)
```

is a polynomial and satisfies

```text
deg Q_gamma < k.
```

For every `x in S_gamma`,

```text
Q_gamma(x)
= (P_gamma(x)-gamma)/(x-beta)
= (U(x)-gamma)/(x-beta)
= U(x)/(x-beta) - gamma/(x-beta)
= f(x) + gamma g(x).
```

Thus `gamma` is a finite bad slope at agreement `a` for `RS[F,D,k]`.

The direction `g` is not itself a degree-`<k` codeword on any support of size
`> k`.  If such an `R` existed, then

```text
(X-beta)R(X)+1
```

would have degree at most `k`, would vanish on more than `k` points of `D`,
and hence would be the zero polynomial.  But evaluating at `X=beta` gives
`1`, a contradiction.

Therefore the produced line is a genuine non-code simple-pole line under the
finite-slope support-wise LD/MCA predicate.  Each counted `gamma` is bad
because `f+gamma g` has agreement at least `a` with a degree-`<k` codeword.

This proves the general theorem.

## Specialization to `F_17^32`

Now take

```text
F = F_17[z]/(z^32 - 3),
H = <z>,
|H| = 512,
D = H,
k = 256,
q = |F| = 17^32.
```

One may take `beta=0`, since `H subset F^*`.

Then

```text
q =
2,367,911,594,760,467,245,844,106,297,320,951,247,361.
```

For `a in {257,258,259,260}`, define

```text
C_a = binom(512,a),
s = a - 256,
R_a = sum_{v=0}^{a-257} binom(a,v) binom(512-a,v) / q^v,
M_a = ceil( q C_a / (C_a + R_a q^s) ).
```

Exact integer arithmetic gives:

```text
M_257 = q,
M_258 = q,
M_259 = q - 68,904,
M_260 =
33,439,260,151,101,646,297,506,087,371,119,470.
```

Hence there exist simple-pole received lines with:

```text
agreement 257: all q finite slopes bad,
agreement 258: all q finite slopes bad,
agreement 259: at least q - 68,904 finite slopes bad,
agreement 260: at least
33,439,260,151,101,646,297,506,087,371,119,470
finite slopes bad.
```

In particular,

```text
M_260 > 2^114.
```

The denominator comparison is

```text
floor(q / 2^128) = floor(17^32 / 2^128) = 6.
```

Thus all four rows are far past the `6/7` finite-slope threshold.

## Why `a=257` and `a=258` Give All Finite Slopes

For `a=257`, one has `s=1` and `R_257=1`, so

```text
M_257 =
ceil( q binom(512,257) / (binom(512,257) + q) ).
```

Exact comparison gives

```text
q binom(512,257) / (binom(512,257) + q) > q - 1.
```

Since at most `q` finite slopes exist, `M_257=q`.

For `a=258`, one has

```text
R_258 = 1 + 258*254/q = 1 + 65,532/q.
```

Again exact comparison gives

```text
q binom(512,258) /
(binom(512,258) + R_258 q^2)
> q - 1.
```

Hence `M_258=q`.

## Why This Proof Stops at `a=260`

The same exact second-moment verifier gives only

```text
M_261 = 1,
M_262 = 1.
```

So this random simple-pole entropy argument is strongest at the low-agreement
rows `a=257,258,259,260`.  Progress for `a>=261` needs another mechanism,
such as tangent, cycle, quotient, or structured-support constructions.
