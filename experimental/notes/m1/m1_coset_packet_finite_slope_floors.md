# M1 Coset-Packet Finite-Slope Floors

Status: PROVED / FINITE-SLOPE LOWER-BOUND / AUDIT.

This note gives explicit finite-slope support-wise lower floors for

```text
F = F_17[z]/(z^32 - 3),
H = <z>,
|H| = 512,
RS[F,H,256] = {Q|_H : deg Q < 256}.
```

The construction is elementary. It builds large common elementary-prefix
families from unions of full dyadic cosets, turns those support families into
many numerator polynomials for one received word, and then uses a separating
deep anchor to obtain many distinct finite bad slopes on one simple-pole line.
It starts at agreement `a=261`; the lower agreements `a=257..260` are outside
this note's displayed row set and are handled by the random simple-pole entropy
floor package.

The main finite-row consequence is:

```text
a = 261..263: at least binom(63,32) finite bad slopes,
a = 264:      at least binom(64,33) finite bad slopes,
a = 265..271: at least binom(31,16) finite bad slopes,
a = 272:      at least binom(32,17) finite bad slopes,
a = 273..287: at least binom(15,8) finite bad slopes,
a = 288:      at least binom(16,9) finite bad slopes.
```

Numerically, the first row gives

```text
binom(63,32) = 916312070471295267
```

finite bad slopes at agreement `a=261`.

## Predicate

For a line `(f,g)` and agreement `a`, define

```text
Bad_fin(f,g;256,a)
=
{ gamma in F :
  exists Q_gamma in F[X], deg Q_gamma < 256,
  |{x in H : Q_gamma(x)=f(x)+gamma g(x)}| >= a }.
```

This is a finite-slope support-wise line/MCA predicate. It is not an ordinary
list-size statement, not an interleaved-list statement, and not a protocol
soundness statement.

## Theorem 1: Coset-Packet Common Prefix

Let `M` be a dyadic divisor of `512`, and let

```text
K_M = <z^(512/M)> <= H
```

be the subgroup of order `M`. Every coset `C=hK_M` has vanishing polynomial

```text
L_C(X) = product_{x in C} (X-x) = X^M - h^M.
```

Therefore

```text
e_1(C)=e_2(C)=...=e_(M-1)(C)=0.
```

The same holds for any union of full `K_M`-cosets: its vanishing polynomial is
a product of terms `X^M-h_i^M`, hence a polynomial in `X^M`.

Now fix an agreement size

```text
a > 256,
d = a - 257.
```

Assume `d < M`. Write

```text
a = mM + b,        0 <= b < M.
```

If `b=0`, choose any `m` full `K_M`-cosets and let `S` be their union. Then
the family has size

```text
L = binom(512/M, m),
```

and all such `S` have `|S|=a` and

```text
e_1(S)=...=e_d(S)=0.
```

If `b>0`, reserve one coset `C_infty`, choose a fixed subset

```text
B subset C_infty,        |B| = b,
```

and let `S` be `B` together with any `m` full `K_M`-cosets among the remaining
cosets. Then the family has size

```text
L = binom(512/M - 1, m).
```

Since the full-coset part has `e_1=...=e_d=0`, every such `S` has `|S|=a` and
the same prefix

```text
(e_1(S),...,e_d(S)) = (e_1(B),...,e_d(B)).
```

Thus each packet gives a common elementary-prefix family.

## Theorem 2: Common Prefix Simple-Pole Lift

Let

```text
S_1,...,S_L subset H,
|S_i| = a,
```

be distinct supports with common elementary prefix

```text
(e_1(S_i),...,e_d(S_i)) = (c_1,...,c_d),
d = a - 257.
```

If

```text
17^32 - 512 > 256 binom(L,2),
```

then there exists a simple-pole line with at least `L` finite bad slopes at
agreement `a`.

First construct the numerator word and degree-`<=256` polynomials as follows.

For each support, write

```text
L_{S_i}(X) = product_{x in S_i}(X-x).
```

Choose the monic degree-`a` polynomial

```text
R(X)
= X^a - c_1 X^(a-1) + c_2 X^(a-2) - ... + (-1)^d c_d X^(a-d),
```

with all lower coefficients set to zero, and define

```text
P_i(X) = R(X) - L_{S_i}(X).
```

The top coefficients through degree `a-d = 257` cancel, so

```text
deg P_i <= 256.
```

Define a received numerator word

```text
U(x)=R(x)        for x in H.
```

For `x in S_i`, one has `L_{S_i}(x)=0`, hence

```text
P_i(x)=R(x)=U(x).
```

So every `P_i` agrees with `U` on the `a` points of `S_i`. The polynomials
`P_i` are distinct because equality `P_i=P_j` would imply
`L_{S_i}=L_{S_j}`, hence `S_i=S_j`.

Now choose the deep anchor. There is a point `beta in F \ H` such that all
values `P_i(beta)` are pairwise distinct. Indeed, each pairwise difference
`P_i-P_j` is a nonzero polynomial of degree at most `256`, so it has at most
`256` roots, and the assumed anchor inequality leaves an available point in
`F \ H`.

For such a `beta`, set

```text
gamma_i = P_i(beta),
f(x) = U(x)/(x-beta),
g(x) = -1/(x-beta).
```

Then

```text
Q_i(X) = (P_i(X)-gamma_i)/(X-beta)
```

is a polynomial of degree `<256`. On every `x in S_i`,

```text
Q_i(x)
= (U(x)-gamma_i)/(x-beta)
= f(x)+gamma_i g(x).
```

Thus every distinct `gamma_i` lies in `Bad_fin(f,g;256,a)`, and

```text
|Bad_fin(f,g;256,a)| >= L.
```

The simple-pole direction is genuine: `g(x)=-1/(x-beta)` is not equal to any
degree-`<256` polynomial on more than `256` points of `H`. Otherwise
`(X-beta)G(X)+1` would have degree at most `256`, vanish on more than `256`
points of `H`, and still equal `1` at `X=beta`.

## Certified Rows

The exact certified rows are:

| agreement `a` | prefix depth `d=a-257` | coset size `M` | packet | finite bad-slope floor |
| ------------: | ---------------------: | -------------: | ------ | ---------------------: |
| `261..263` | `4..6` | `8` | fixed base of size `a mod 8`, choose `32` of `63` full cosets | `binom(63,32)` |
| `264` | `7` | `8` | choose `33` of all `64` full cosets | `binom(64,33)` |
| `265..271` | `8..14` | `16` | fixed base of size `a mod 16`, choose `16` of `31` full cosets | `binom(31,16)` |
| `272` | `15` | `16` | choose `17` of all `32` full cosets | `binom(32,17)` |
| `273..287` | `16..30` | `32` | fixed base of size `a mod 32`, choose `8` of `15` full cosets | `binom(15,8)` |
| `288` | `31` | `32` | choose `9` of all `16` full cosets | `binom(16,9)` |

The numerical floors are:

```text
binom(63,32) = 916312070471295267,
binom(64,33) = 1777090076065542336,
binom(31,16) = 300540195,
binom(32,17) = 565722720,
binom(15,8)  = 6435,
binom(16,9)  = 11440.
```

For every row in the table, the anchor-separation condition

```text
17^32 - 512 > 256 binom(L,2)
```

holds. Each listed floor is also larger than the moving-root tangent floor
`513-a` at the same agreement.

## Scope

This is a lower-bound construction for finite support-wise bad slopes. It does
not claim a safe-side upper bound, an ordinary list-decoding theorem, an
interleaved-list theorem, protocol soundness failure, or exactness of
`Bad_fin`.

The displayed agreement rows are separate existence statements. The note does
not claim one received line realizes all agreement rows simultaneously. The
rows `a=257..260` are intentionally left to the random simple-pole entropy
floor package.
