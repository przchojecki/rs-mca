# F1: Deep-Point List-to-CA/MCA Conversion

Status: PROVED for the simple-pole identity / CONDITIONAL for the quotient-locator
cap application / AUDIT.

This note records a direct simple-pole conversion from large lists for
`RS[F,D,k+1]` into many bad slopes for both no-loss correlated agreement (CA)
and support-wise mutual correlated agreement (MCA) for `RS[F,D,k]`.

For a deep point `alpha notin D`, the simple-pole line

```text
f_alpha(x) = U(x)/(x-alpha),
g_alpha(x) = -1/(x-alpha)
```

has an exact bad-slope identity:

```text
Bad_CA(f_alpha,g_alpha; delta_a)
= Bad_MCA(f_alpha,g_alpha; delta_a)
= {P(alpha) : P in RS-degree < k+1 and P agrees with U on at least a points}.
```

The key observation is simple: `g_alpha` cannot agree with any degree-`<k`
polynomial on more than `k` points. That gives the global far condition needed
for CA, while the same agreement support gives the support-wise MCA witness.

Together with the slack-two quotient-locator list input, this suggests a direct
CA/MCA cap route. The simple-pole identity is self-contained. The cap
application should still be checked against the quotient-locator list mass, the
CA/MCA definitions, and the finite constants in the main papers.
Crites--Stewart remains useful as a broader list-to-agreement conversion and as
an independent comparison route.

## 0. Conventions

Let `F` be a finite field, let `D subset F` have size `n`, and let

```text
C   = RS[F,D,k],
C_+ = RS[F,D,k+1],
1 <= k < n.
```

Codewords of `C` are restrictions to `D` of polynomials in `F[X]_<k`, and
codewords of `C_+` are restrictions to `D` of polynomials in `F[X]_<k+1`.

For an integer `a` with

```text
k < a <= n,
```

write

```text
delta_a = 1 - a/n.
```

Since `a` is an integer, `Delta(W,C) <= 1-a/n` is the same as saying that `W`
agrees with some codeword on at least `a` positions.

The no-loss CA bad-slope set of a line `f + z g` at radius `delta` is

```text
Bad_CA(f,g; delta)
= { z in F : Delta(f+zg,C) <= delta and Delta((f,g),C^2) > delta }.
```

The proximity-loss CA bad-slope set is defined similarly with radii
`delta_fld <= delta_int`:

```text
Bad_CA(f,g; delta_fld, delta_int)
= { z in F : Delta(f+zg,C) <= delta_fld
             and Delta((f,g),C^2) > delta_int }.
```

The support-wise MCA bad-slope set at radius `delta` is

```text
Bad_MCA(f,g; delta)
= { z in F : exists S subset D, |S| >= (1-delta)n,
             f+zg is explained by C on S,
             but (f,g) is not simultaneously explained by C^2 on S }.
```

Here `C^2` denotes the two-fold interleaving of `C` with column distance, and
distances are relative Hamming distances on `D`.

## 1. Exact simple-pole image identity

### Theorem 1.1: exact deep-point image identity for CA and MCA

Let `U : D -> F`, let `alpha in F \ D`, and define

```text
f_alpha(x) = U(x)/(x-alpha),
g_alpha(x) = -1/(x-alpha).
```

For `k < a <= n`, define the deep image of the `C_+` list around `U` at
agreement `a` by

```text
Deep_alpha(U,a)
=
{
    P(alpha) :
    P in F[X]_<k+1 and
    |{x in D : P(x)=U(x)}| >= a
}.
```

Then the no-loss CA-bad slopes and support-wise MCA-bad slopes of the line

```text
f_alpha + z g_alpha
```

at the radius `delta_a = 1-a/n` are exactly the deep image:

```text
Bad_CA(f_alpha,g_alpha; delta_a)
=
Bad_MCA(f_alpha,g_alpha; delta_a)
=
Deep_alpha(U,a).
```

For larger radii the theorem gives persistence, not a new exact description:
every `z in Deep_alpha(U,a)` remains CA-bad for every proximity-loss pair

```text
delta_fld >= delta_a,
delta_int < 1 - k/n,
delta_fld <= delta_int.
```

In particular, for no-loss CA, and also for support-wise MCA, the same slope
remains bad for every

```text
delta in [delta_a, 1-k/n).
```

For MCA alone, the same support-wise witness also persists for larger radii, but
the Proximity Prize cap only needs the subcapacity range `delta < 1-k/n`.

#### Proof

First prove

```text
Deep_alpha(U,a) subset Bad_CA cap Bad_MCA.
```

Take `z in Deep_alpha(U,a)`. Then there is `P in F[X]_<k+1` and a support

```text
S = {x in D : P(x)=U(x)}
```

with `|S| >= a > k` and `z = P(alpha)`.

On `S`,

```text
f_alpha(x) + z g_alpha(x)
= U(x)/(x-alpha) - P(alpha)/(x-alpha)
= (P(x)-P(alpha))/(x-alpha).
```

The polynomial

```text
Q(X) = (P(X)-P(alpha))/(X-alpha)
```

has degree `< k`, since `deg P < k+1`. Hence `f_alpha + z g_alpha` is explained
by `C` on `S`.

Now show that `(f_alpha,g_alpha)` is not close to `C^2` on any support of size
`> k`. It is enough to show that `g_alpha` alone has no degree-`<k` explanation
on such a support.

Suppose some `T subset D`, `|T| > k`, and some `G in F[X]_<k` satisfy

```text
G(x) = -1/(x-alpha)       for all x in T.
```

Then

```text
H(X) = (X-alpha)G(X) + 1
```

has degree at most `k` and vanishes on more than `k` points. Thus `H=0`. But

```text
H(alpha) = 1,
```

a contradiction.

Therefore `g_alpha` is not explained by `C` on any support of size `> k`, so
`(f_alpha,g_alpha)` is not `delta_int`-close to `C^2` for any
`delta_int < 1-k/n`. This proves CA-badness at `delta_a`, and it also proves
support-wise MCA-badness on the specific support `S`.

Now prove the reverse inclusion.

Suppose `z` is MCA-bad at radius `delta_a`. Then there is a support `S subset D`,
`|S| >= a`, and a polynomial `Q in F[X]_<k` such that

```text
f_alpha(x) + z g_alpha(x) = Q(x)       for all x in S.
```

Multiplying by `x-alpha` gives

```text
U(x) - z = (x-alpha)Q(x)       for all x in S.
```

Define

```text
P(X) = (X-alpha)Q(X) + z.
```

Then `deg P < k+1`, `P(alpha)=z`, and `P(x)=U(x)` for all `x in S`. Hence
`z in Deep_alpha(U,a)`.

The same reverse implication applies if `z` is CA-bad, because CA-badness
includes the condition that `f_alpha+z g_alpha` is `delta_a`-close to `C`.

Thus the bad-slope set is exactly the deep image. The persistence statement
follows because closeness of `f_alpha+z g_alpha` at radius `delta_a` implies
closeness at every larger `delta_fld`, while the pair `(f_alpha,g_alpha)` is far
from `C^2` at every `delta_int < 1-k/n`.

QED.

## 2. Averaging over deep points

The exact identity converts deep images into bad-slope counts. The next lemma
lower-bounds the size of a deep image for some `alpha`.

### Lemma 2.1: deep-point evaluation expansion

Let

```text
P_1, ..., P_L in F[X]_<k+1
```

be pairwise distinct polynomials. Let `Omega subset F` be any nonempty candidate
set of deep points. For `alpha in Omega`, write

```text
M(alpha) = |{P_i(alpha) : 1 <= i <= L}|.
```

Then there exists `alpha in Omega` such that

```text
M(alpha) >= L / (1 + k(L-1)/|Omega|).
```

#### Proof

For each unordered pair `{i,j}` with `i != j`, the polynomial `P_i-P_j` is
nonzero and has degree at most `k`. Therefore

```text
|{alpha in Omega : P_i(alpha)=P_j(alpha)}| <= k.
```

Let `C_alpha` be the number of unordered colliding pairs at `alpha`. Averaging
over `Omega` gives

```text
E_alpha C_alpha <= k * binom(L,2) / |Omega|.
```

Choose `alpha` satisfying this bound. If the fiber sizes of the map
`i -> P_i(alpha)` are `m_1,...,m_M`, then

```text
sum_r m_r = L,
sum_r binom(m_r,2) = C_alpha,
sum_r m_r^2 = L + 2C_alpha.
```

By Cauchy-Schwarz,

```text
L^2 <= M * sum_r m_r^2 = M(L + 2C_alpha).
```

Substituting the averaged collision bound gives

```text
M >= L/(1 + k(L-1)/|Omega|).
```

QED.

### Theorem 2.2: list-to-CA/MCA transfer through a deep point

Let `U : D -> F` be a received word. Suppose there are pairwise distinct
polynomials

```text
P_1, ..., P_L in F[X]_<k+1
```

such that each `P_i` agrees with `U` on at least `a` points of `D`, where

```text
k < a <= n.
```

Let `Omega subset F \ D` be nonempty. Then there exists `alpha in Omega` and a
simple-pole line

```text
f_alpha(x) = U(x)/(x-alpha),
g_alpha(x) = -1/(x-alpha)
```

with at least

```text
M >= L / (1 + k(L-1)/|Omega|)
```

bad slopes for both CA and support-wise MCA at radius `delta_a = 1-a/n`.
Consequently,

```text
epsilon_ca(C, delta_a)  >= (1/|F|) * L / (1 + k(L-1)/|Omega|),
epsilon_mca(C, delta_a) >= (1/|F|) * L / (1 + k(L-1)/|Omega|).
```

More generally, the same lower bound holds for proximity-loss CA:

```text
epsilon_ca(C, delta_fld, delta_int)
    >= (1/|F|) * L / (1 + k(L-1)/|Omega|)
```

whenever

```text
delta_fld in [delta_a, 1-k/n),
delta_fld <= delta_int < 1-k/n.
```

The same lower bound also holds for `epsilon_mca(C,delta)` for every
`delta in [delta_a,1-k/n)`.

#### Proof

Apply Lemma 2.1 to choose `alpha in Omega` with at least the displayed number of
distinct values among `P_i(alpha)`. Theorem 1.1 identifies those distinct values
with CA-bad and MCA-bad slopes for the simple-pole line. Dividing the number of
bad slopes by `|F|` gives the claimed error lower bounds.

QED.

### Corollary 2.3: saturated form

In the setting of Theorem 2.2, if

```text
L >= |Omega|/k,
```

then

```text
epsilon_ca(C, delta_a)  >= |Omega|/(2k|F|),
epsilon_mca(C, delta_a) >= |Omega|/(2k|F|).
```

The same bound persists for the proximity-loss CA and no-loss CA/MCA ranges in
Theorem 2.2.

More generally, if

```text
R = kL/|Omega|,
```

then the lower-bound numerator is

```text
L/(1 + k(L-1)/|Omega|)
= (|Omega|/k) * R/(1 + R - k/|Omega|).
```

For `R >> 1`, this is essentially `|Omega|/k`.

## 3. Extension-field form and subfield confinement

Assume now that

```text
B <= F,
D subset B.
```

Taking `Omega = F \ B` in Theorem 2.2 gives a genuinely extension-valued line.
If `F != B`, then

```text
|Omega| = |F| - |B|.
```

Thus

```text
epsilon_ca(RS[F,D,k], 1-a/n)
>=
(1/|F|) * L / (1 + k(L-1)/(|F|-|B|)),

epsilon_mca(RS[F,D,k], 1-a/n)
>=
(1/|F|) * L / (1 + k(L-1)/(|F|-|B|)).
```

If

```text
L >= (|F|-|B|)/k,
```

then

```text
epsilon_ca(RS[F,D,k], 1-a/n)
>= (1 - |B|/|F|)/(2k),

epsilon_mca(RS[F,D,k], 1-a/n)
>= (1 - |B|/|F|)/(2k),
```

with the same proximity-loss and no-loss persistence range from Theorem 2.2.

This does not contradict subfield confinement for `B`-valued lines. For
`alpha in F \ B`, the words

```text
f_alpha(x)=U(x)/(x-alpha),
g_alpha(x)=-1/(x-alpha)
```

are generally not `B`-valued on `D`.

### Lemma 3.1: simple pole is not scalar-`B`-valued

Let `B < F`, let `D subset B` contain at least two distinct points, and let
`alpha in F \ B`. Define

```text
g_alpha(x) = -1/(x-alpha),  x in D.
```

Then there is no `lambda in F^*` such that `lambda^{-1} g_alpha(x) in B` for all
`x in D`.

#### Proof

Suppose such `lambda` exists. Then for every distinct `x,y in D`,

```text
g_alpha(x)/g_alpha(y) = (y-alpha)/(x-alpha)
```

lies in `B`.

Fix distinct `x,y in D` and put

```text
r = (y-alpha)/(x-alpha) in B.
```

If `r=1`, then `x=y`, contradiction. Hence `r != 1`. Rearranging,

```text
r(x-alpha) = y-alpha,
(r-1) alpha = rx-y.
```

The right side lies in `B`, and `r-1` is nonzero in `B`, so `alpha in B`, a
contradiction.

QED.

## 4. Slack-two quotient-locator list input

The universal-cap application uses the following list input.

### Lemma 4.1: slack-two quotient-locator list fiber

Let `B <= F` be finite fields. Let `D subset B^*` be a multiplicative coset of
order `n`. Let `N | n` and set

```text
a0 = n/N,
Q  = D^a0 = {x^a0 : x in D} subset B^*.
```

Then `Q` is a multiplicative coset of order `N`, and the map `x -> x^a0` maps
`D` onto `Q` with fibers of size `a0`.

Let `k` satisfy `a0 | k`, and set `rho = k/n`. Put

```text
ell = rho N + 2 = k/a0 + 2.
```

Assume `ell <= N`. Then there is a `B`-valued received word `U_z : D -> B` such
that

```text
|Lambda(RS[F,D,k+1], 1-rho-2/N, U_z)|
    >= ceil( binom(N,ell) / |B| ).
```

Moreover, all listed codewords are `B`-valued and are represented by polynomials
of degree `<= k`.

#### Proof

For `A subset Q` with `|A|=ell`, define

```text
L_A(X) = prod_{b in A} (X^a0 - b).
```

Since `a0 ell = k + 2a0`, this expands as

```text
L_A(X) = X^(k+2a0) - e_1(A) X^(k+a0) + R_A(X),
```

where `deg R_A <= k`.

Set

```text
z_A = -e_1(A) in B,
U_{z_A}(x) = x^(k+2a0) + z_A x^(k+a0),
c_A(x) = -R_A(x).
```

Then `c_A` is a codeword of `RS[B,D,k+1]`, because `deg R_A <= k`. The
polynomial `L_A` vanishes exactly on

```text
S_A = {x in D : x^a0 in A},
```

and `|S_A| = a0 ell = k + 2a0`. On `S_A`,

```text
U_{z_A}(x) = c_A(x).
```

Thus `c_A` is within radius

```text
1 - (k+2a0)/n = 1 - rho - 2/N
```

of `U_{z_A}`.

As `A` ranges over the `binom(N,ell)` subsets of `Q`, the value `z_A` lies in
`B`, so some `z in B` occurs for at least `ceil(binom(N,ell)/|B|)` choices of
`A`.

For this fixed `z`, the corresponding `c_A` are distinct. Indeed, if
`c_A=c_A'` as functions on `D`, then `R_A=R_A'` as polynomials because
`deg(R_A-R_A') <= k < n`. Since `z_A=z_A'=z`, this gives `L_A=L_A'`. Hence the
root sets `S_A` and `S_A'` are equal, and therefore

```text
A = {x^a0 : x in S_A} = {x^a0 : x in S_A'} = A'.
```

So the fixed word `U_z` has at least `ceil(binom(N,ell)/|B|)` distinct nearby
codewords in `RS[F,D,k+1]`.

QED.

## 5. Direct CA/MCA lower bound from quotient-locator lists

### Theorem 5.1: deep-point quotient-locator CA/MCA obstruction

In the setting of Lemma 4.1, let

```text
q  = |F|,
b  = |B|,
L0 = ceil( binom(N,rho N + 2) / b ).
```

Let `Omega subset F \ D` be nonempty. Then

```text
epsilon_ca(RS[F,D,k], 1-rho-2/N)
>=
(1/q) * L0 / (1 + k(L0-1)/|Omega|),

epsilon_mca(RS[F,D,k], 1-rho-2/N)
>=
(1/q) * L0 / (1 + k(L0-1)/|Omega|).
```

The same lower bound holds for proximity-loss CA whenever

```text
delta_fld in [1-rho-2/N, 1-rho),
delta_fld <= delta_int < 1-rho,
```

and for no-loss CA/MCA throughout

```text
delta in [1-rho-2/N, 1-rho).
```

In particular:

1. Taking `Omega = F \ D` gives

   ```text
   epsilon_ca(RS[F,D,k], delta)  >= (q-n)/(2kq),
   epsilon_mca(RS[F,D,k], delta) >= (q-n)/(2kq)
   ```

   throughout the above range whenever

   ```text
   L0 >= (q-n)/k.
   ```

2. If `D subset B subsetneq F`, taking `Omega = F \ B` gives the genuinely
   extension-valued lower bound

   ```text
   epsilon_ca(RS[F,D,k], delta)  >= (q-b)/(2kq),
   epsilon_mca(RS[F,D,k], delta) >= (q-b)/(2kq)
   ```

   throughout the above range whenever

   ```text
   L0 >= (q-b)/k.
   ```

#### Proof

Apply Lemma 4.1 to get a received word `U_z` with at least `L0` listed codewords
for `C_+ = RS[F,D,k+1]` at agreement

```text
k + 2a0 > k.
```

Then apply Theorem 2.2 with `a = k + 2a0`. This gives the main displayed
bounds. The two half-bounds are Corollary 2.3 with `Omega = F\D` and
`Omega = F\B`.

QED.

## 6. Direct CA/MCA cap for the Proximity Prize envelope

### Corollary 6.1: proposed direct CA/MCA universal cap

Let

```text
rho in {1/2, 1/4, 1/8, 1/16}.
```

Set

```text
N_rho = 1024   for rho in {1/2, 1/4, 1/8},
N_rho = 2048   for rho = 1/16.
```

Let `F` be any finite field with `q=|F| < 2^256`. Let `B <= F` be a subfield, and
let `D subset B^*` be a multiplicative coset of order `n` with `N_rho | n`. Let

```text
C = RS[F,D,k],
k = rho n <= 2^40.
```

Then, for every no-loss radius

```text
delta in [1-rho-2/N_rho, 1-rho),
```

we have

```text
epsilon_ca(C, delta)  >= (1/(2k))*(1 - n/q) >= 2^-86,
epsilon_mca(C, delta) >= (1/(2k))*(1 - n/q) >= 2^-86.
```

More generally, for proximity-loss CA,

```text
epsilon_ca(C, delta_fld, delta_int)
    >= (1/(2k))*(1 - n/q)
```

whenever

```text
delta_fld in [1-rho-2/N_rho, 1-rho),
delta_fld <= delta_int < 1-rho.
```

If `q >= 2n`, then the same lower bound improves to

```text
(1/(2k))*(1 - n/q) >= 2^-42.
```

Consequently,

```text
delta^*_C(2^-128) <= 1-rho-2^-9       for rho in {1/2,1/4,1/8},
delta^*_C(2^-128) <= 1-rho-2^-10      for rho = 1/16.
```

#### Proof

Apply Theorem 5.1 with `N=N_rho` and `Omega=F\D`. We verify the saturation
condition

```text
L0 >= (q-n)/k.
```

Here

```text
L0 >= binom(N_rho, rho N_rho + 2)/|B|.
```

It is enough that

```text
binom(N_rho, rho N_rho + 2) >= |B|*(q/k + 1).
```

Since `|B| <= q < 2^256` and `k >= 1`,

```text
|B|*(q/k + 1) <= q*(q+1) < 2^513.
```

The elementary entropy estimates are:

```text
rho     N_rho   ell=rho*N_rho+2   log2 binom(N_rho,ell) lower bound
1/2     1024    514               1013
1/4     1024    258                823
1/8     1024    130                552
1/16    2048    130                687
```

All four lower bounds exceed `513`, so the saturation condition holds.

Therefore Theorem 5.1 gives

```text
epsilon_ca(C, delta)  >= (q-n)/(2kq),
epsilon_mca(C, delta) >= (q-n)/(2kq)
```

throughout the stated no-loss and proximity-loss ranges.

It remains only to check the numerical `2^-86` lower bound. Since `D subset F^*`,
we have `n <= q-1`, and hence

```text
1 - n/q >= 1/(n+1).
```

Also `rho >= 1/16` and `k <= 2^40`, so

```text
n = k/rho <= 16k <= 2^44.
```

Thus

```text
(1/(2k))*(1 - n/q)
>= 1/(2k(n+1))
> 2^-86.
```

If `q >= 2n`, then `1-n/q >= 1/2`, so

```text
(1/(2k))*(1 - n/q) >= 1/(4k) >= 2^-42.
```

The stated gaps are `2/N_rho`, namely `2^-9` for `N_rho=1024` and `2^-10` for
`N_rho=2048`.

QED.

### Remark 6.2: relation to CS25

If the quotient-locator list input and the CA/MCA predicates match the statements
used here, the simple-pole route gives the displayed CA and MCA lower bounds
without invoking CS25 for this particular cap mechanism.

CS25 remains useful for:

1. a general theorem converting arbitrary list mass into CA without constructing
   the special simple-pole line;
2. comparison with the prior universal-cap paper and independent redundancy;
3. protocol arguments that use a CA variant outside the range `delta_int < 1-rho`;
4. historical continuity with the previous proof route.

## 7. Deployed Extension-Field Estimate

Take the deployed extension-field parameters

```text
B = F_p,
p = 2^31 - 2^24 + 1,
F = B^6,
n = 2^21,
k = 2^20,
rho = 1/2,
N = 256,
a0 = n/N = 2^13,
ell = rho N + 2 = 130.
```

The quotient-locator list input gives

```text
L0 >= binom(256,130) / p.
```

Using

```text
log2 binom(256,130) > 247,
log2 p < 31,
```

we get

```text
log2 L0 > 216.
```

For `Omega = F \ B`,

```text
|Omega| = p^6 - p,
log2 |Omega| < 186,
```

and

```text
k L0 / |Omega| > 2^(20 + 216 - 186) = 2^50.
```

Therefore the sharper `R`-form of Corollary 2.3 gives

```text
epsilon_ca(RS[F,D,2^20], 1/2 - 2^-7)
  > (1-p^-5)(1-2^-49) / 2^20,

epsilon_mca(RS[F,D,2^20], 1/2 - 2^-7)
  > (1-p^-5)(1-2^-49) / 2^20.
```

In particular,

```text
epsilon_ca  > 2^-21,
epsilon_mca > 2^-21
```

in the stated no-loss and subcapacity proximity-loss ranges. The conservative
half-bound already gives `> 2^-22`.

The witness line has the explicit rational shape

```text
f_alpha(x) = U_z0(x)/(x-alpha),
g_alpha(x) = -1/(x-alpha),
alpha in F \ B,
```

and the bad slopes are the distinct values

```text
lambda = P_i(alpha)
```

coming from the heavy `RS[F,D,k+1]` list around `U_z0`.

The proof above is existential in `z0` and `alpha`. It proves that such a heavy
quotient-locator fiber and such a deep point exist. It does not yet enumerate the
deployed-size certificate.

## 8. Audit Checklist

The proof is short, but these are the points that should be checked before
anything is promoted out of `experimental/`.

1. CA definition.
   Check that the no-loss and proximity-loss CA events are exactly: the folded
   point is close to `C`, while the pair `(f,g)` is farther than the internal
   radius from `C^2`.

2. MCA definition.
   Check that support-wise MCA only requires one support `S` such that
   `f+zg` is explained on `S`, while `(f,g)` is not simultaneously explained on
   that same `S`.

3. Global far condition.
   The CA step rests on the fact that `g_alpha=-1/(X-alpha)` has no degree-`<k`
   explanation on any support of size `>k`.

4. Strict support size.
   The argument requires `a>k`. At `a=k`, the global far statement for supports
   of size `>k` would not force badness at the corresponding radius.

5. Degree drop.
   Since `P in F[X]_<k+1`, the quotient

   ```text
   (P(X)-P(alpha))/(X-alpha)
   ```

   has degree `<k`.

6. Denominator.
   We require `alpha notin D`, so `x-alpha` is nonzero on every evaluation point.

7. Reverse inclusion.
   If `f_alpha+z g_alpha` is close on support `S`, multiplying by `X-alpha`
   gives `P(X)=(X-alpha)Q(X)+z`, so `P(alpha)=z` and `P` is a listed `C_+`
   polynomial. This proves exactness of the image identity.

8. Evaluation expansion.
   For distinct `P_i,P_j in F[X]_<k+1`, the difference `P_i-P_j` has degree at
   most `k`, hence has at most `k` roots. This is the only input in Lemma 2.1.

9. Extension-valued line.
   For the extension-field application, choose `alpha in F\B`. Then `f_alpha`
   and `g_alpha` are generally `F`-valued but not `B`-valued, so this route is
   outside the `B`-valued subfield-confinement class.

10. Imported list mass.
    The slack-two quotient-locator list mass should be checked separately:
    `N|n`, `a0=n/N`, `a0|k`, `ell=rho N+2<=N`, and pigeonhole denominator
    `|B|`.

11. Cap statement.
    Check the quotient-locator list mass, constants, and threshold notation
    before moving the direct CA/MCA cap statement into any main paper.

12. Exactness versus persistence.
    `Bad_CA = Bad_MCA = Deep_alpha(U,a)` is exact at `delta_a`. At larger
    radii, the construction gives persistent bad slopes and lower bounds; it
    does not claim that no additional bad slopes appear.

## 9. Reproducibility

The finite toy check for the exact identity is:

```bash
python experimental/scripts/f1_deep_point_list_to_ca_mca_sanity.py
```
