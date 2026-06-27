# L1 Monomial Dyadic Descent Gate and Survivor Families

- **Status:** PROVED / AUDIT.
- **Agent/model:** Codex.
- **Date:** 2026-06-27.
- **Scope:** Experimental L1 proof note. This note does not edit Papers A-D and does not claim an arbitrary-word list-size theorem, MCA theorem, line-decoding theorem, interleaved-list theorem, or protocol-safety consequence.

## Purpose

This note records a complete admissible-size classification for one monomial-prefix locator toy case:

```text
F = F_17[z] / (z^32 - 3),
H = <z>,
|H| = 512,
deg P <= 256.
```

For `257 < A <= 512`, call a support `S subset H` `A`-admissible if `|S|=A` and the monomial word `x -> x^A` agrees with some polynomial of degree at most `256` on `S`.

The final classification is:

```text
Admissible A:
258, 259, 260, 262, 264, 268, 272, 280,
288, 304, 320, 352, 384, 512.

Impossible A:
all other A with 258 <= A <= 512.
```

The proof has three parts:

```text
1. a local length-16 imbalance lemma over F_17,
2. a dyadic power-sum descent gate,
3. a quotient-complement classification of the remaining rows.
```

The classification is by explicit structural families, not by listing every orbit representative. A literal orbit list is already large in the first rows.

## Field and Subgroup

In `F_17^*`, the element `3` has order `16`. Thus in

```text
F = F_17[z] / (z^32 - 3)
```

we have

```text
z^32 = 3,
z^512 = 1.
```

The element `z` has exact order `512`. Let

```text
H = <z> = {z^i : 0 <= i < 512}.
```

For a finite subset `S subset H`, write

```text
p_j(S) = sum_{x in S} x^j.
```

Also write

```text
L_S(X) = product_{x in S} (X - x)
       = X^A - e_1(S)X^(A-1) + e_2(S)X^(A-2) - ... + (-1)^A e_A(S),
```

where `A=|S|`.

## Agreement and Elementary Vanishing

Let `257 < A <= 512`. A support `S subset H` is `A`-admissible if

```text
|S| = A
```

and there is a polynomial `P in F[X]` such that

```text
deg P <= 256,
P(x) = x^A for every x in S.
```

Equivalently,

```text
L_S(X) divides X^A - P(X)
```

for some `P` of degree at most `256`.

Reducing `X^A` modulo `L_S(X)` gives

```text
X^A == e_1(S)X^(A-1) - e_2(S)X^(A-2) + e_3(S)X^(A-3) - ... mod L_S(X).
```

The remainder has degree at most `256` exactly when

```text
e_1(S) = e_2(S) = ... = e_(A-257)(S) = 0.
```

Newton identities then imply

```text
p_1(S) = p_2(S) = ... = p_(A-257)(S) = 0.
```

This direction uses no division, so there is no characteristic-17 obstruction here.

## Local Length-16 Imbalance Lemma

Let

```text
omega = 3 in F_17.
```

Then `omega` has order `16`.

Let

```text
B(U) = b_0 + b_1 U + ... + b_15 U^15,
b_q in {0,1}.
```

Define

```text
Delta_q = b_q - b_(q+8),        0 <= q < 8,
Delta(U) = sum_{q=0}^7 Delta_q U^q.
```

Since `omega^8=-1`, for odd `j`,

```text
B(omega^j) = Delta(omega^j).
```

The finite local classification is:

```text
Delta(omega)=Delta(omega^3)=0
```

with `Delta_q in {-1,0,1}` has exactly the following solutions:

```text
Delta = 0,
Delta(U) = +/- U^t Delta_0(U) mod U^8+1,        0 <= t < 8,
```

where

```text
Delta_0(U) = U^2 - U^3 - U^4 + U^5 + U^6 + U^7.
```

In particular, the support size of `Delta` is either `0` or `6`.

Also,

```text
Delta_0(omega)=Delta_0(omega^3)=0,
Delta_0(omega^5)=15 != 0.
```

Therefore, if

```text
Delta(omega)=Delta(omega^3)=Delta(omega^5)=0,
```

then `Delta=0`.

Two consequences are used below:

```text
B(omega)=B(omega^3)=0
=> |{q : b_q=1}| is even.

B(omega)=B(omega^3)=B(omega^5)=0
=> b_q=b_(q+8) for every q.
```

The only finite case split in the note is the displayed ternary imbalance classification. It has `3^8` cases and is isolated for review.

## Local Coordinates in Dyadic Quotients

Let `G_N=<alpha>` be cyclic of order

```text
N in {512, 256, 128, 64, 32, 16}.
```

Set

```text
h = N/16.
```

Then

```text
alpha^h = omega = 3.
```

For each listed `h`, the polynomial `X^h-3` is irreducible over `F_17`, so

```text
1, alpha, alpha^2, ..., alpha^(h-1)
```

is an `F_17`-basis of `F_17(alpha)`.

Here is the irreducibility check. The case `h=1` is trivial. For
`h in {2,4,8,16,32}`, the binomial criterion applies to `X^h-3`: the only
prime divisor of `h` is `2`, and `2` divides `ord_{F_17^*}(3)=16`; also

```text
gcd(h, (17-1)/16) = gcd(h,1) = 1.
```

When `4 | h`, the final binomial-criterion condition is also satisfied because

```text
17 == 1 mod 4.
```

Thus `X^h-3` is irreducible over `F_17` for the listed `h`.

Every exponent has a unique form

```text
i = a + hq,
0 <= a < h,
0 <= q < 16.
```

For `C subset G_N`, define

```text
B_a(U) = sum_{q : alpha^(a+hq) in C} U^q.
```

For odd `j`, multiplication by `j` permutes the residue classes modulo `h`, and coefficient comparison in the basis above gives:

```text
p_j(C)=0
if and only if
B_a(omega^j)=0 for every a.
```

For `j=2` and `h>=2`, coefficient comparison gives:

```text
p_2(C)=0
if and only if
B_a(omega^2) + omega B_(a+h/2)(omega^2) = 0
for 0 <= a < h/2.
```

When `h=1`, the condition is simply `B_0(omega^2)=0`.

## Dyadic Power-Sum Descent

For a dyadic integer `Q` dividing `512`, let

```text
K_Q = <z^(512/Q)>.
```

The key descent statement is:

```text
p_1(S)=p_2(S)=...=p_m(S)=0
and
m >= 5 * 2^r
=> S is a union of K_(2^(r+1))-cosets.
```

Here `0 <= r <= 5`.

The proof is by induction. Suppose `S` is already a union of `K_q`-cosets, where `q=2^t`. Let

```text
phi_q : H -> <z^q>,
phi_q(x)=x^q.
```

The kernel is `K_q`. Let `T` be the quotient image of the `K_q`-cosets contained in `S`. For `ell in {1,3,5}`,

```text
p_(q ell)(S) = q p_ell(T).
```

Since `q` is nonzero in characteristic `17`, the vanishings of `p_q(S)`, `p_(3q)(S)`, and `p_(5q)(S)` force

```text
p_1(T)=p_3(T)=p_5(T)=0.
```

The local length-16 lemma gives `T=-T`, so the quotient image is antipodal. Lifting antipodality through `phi_q` says that every occupied `K_q`-coset is paired with its adjacent coset inside a `K_(2q)`-coset. Hence `S` is a union of `K_(2q)`-cosets.

Iterating gives the descent theorem.

## Divisibility Gate

If `S` is `A`-admissible, then

```text
p_1(S)=...=p_(A-257)(S)=0.
```

By dyadic descent,

```text
5 * 2^r <= A - 257
=> S is a union of K_(2^(r+1))-cosets
=> 2^(r+1) divides A.
```

Thus:

```text
A >= 262 => 2 divides A,
A >= 267 => 4 divides A,
A >= 277 => 8 divides A,
A >= 297 => 16 divides A,
A >= 337 => 32 divides A,
A >= 417 => 64 divides A.
```

This gate leaves only the following candidate sizes:

```text
258, 259, 260, 261, 262, 264, 266, 268,
272, 276, 280, 288, 296, 304, 320, 336,
352, 384, 416, 448, 512.
```

## Quotient-Complement Reduction

For each survivor `A`, let `Q=Q(A)` be the largest dyadic order forced by the divisibility gate. Put

```text
G = G_Q = <z^Q>,
N = |G| = 512/Q,
B = A/Q,
D = 256/Q.
```

Since `Q` divides `256` in every survivor row, `D` is integral.

The map

```text
phi_Q : H -> G,
phi_Q(x)=x^Q
```

has kernel `K_Q`. If `S` is a union of `K_Q`-cosets, then

```text
S = phi_Q^(-1)(T)
```

for a unique `T subset G` with `|T|=B`.

For a coset with quotient element `y=x^Q`,

```text
product_{u in xK_Q} (X-u) = X^Q - y.
```

Therefore

```text
L_S(X) = product_{y in T} (X^Q-y) = L_T(X^Q).
```

It follows that `S` is `A`-admissible if and only if

```text
e_1(T)=e_2(T)=...=e_d(T)=0,
d = B-D-1.
```

Indeed, the coefficient `e_i(T)` in `L_T(X^Q)` appears at degree

```text
Q(B-i).
```

The terms above degree `256` are exactly those with

```text
Q(B-i) > 256.
```

Since `D=256/Q`, this is equivalent to

```text
i <= B-D-1.
```

Let

```text
C = G \ T.
```

For `1 <= j < N`, the full group sum over `G` is zero, so

```text
p_j(T) = -p_j(C).
```

In every survivor row, `d <= 4 < 17`, so Newton identities are reversible in the quotient problem. Thus the quotient condition is equivalent to

```text
|C| = c = N-B,
p_1(C)=p_2(C)=...=p_d(C)=0.
```

## Survivor Table

| A | Q | N=512/Q | B=A/Q | D=256/Q | d=B-D-1 | c=N-B |
|---:|---:|---:|---:|---:|---:|---:|
| 258 | 1 | 512 | 258 | 256 | 1 | 254 |
| 259 | 1 | 512 | 259 | 256 | 2 | 253 |
| 260 | 1 | 512 | 260 | 256 | 3 | 252 |
| 261 | 1 | 512 | 261 | 256 | 4 | 251 |
| 262 | 2 | 256 | 131 | 128 | 2 | 125 |
| 264 | 2 | 256 | 132 | 128 | 3 | 124 |
| 266 | 2 | 256 | 133 | 128 | 4 | 123 |
| 268 | 4 | 128 | 67 | 64 | 2 | 61 |
| 272 | 4 | 128 | 68 | 64 | 3 | 60 |
| 276 | 4 | 128 | 69 | 64 | 4 | 59 |
| 280 | 8 | 64 | 35 | 32 | 2 | 29 |
| 288 | 8 | 64 | 36 | 32 | 3 | 28 |
| 296 | 8 | 64 | 37 | 32 | 4 | 27 |
| 304 | 16 | 32 | 19 | 16 | 2 | 13 |
| 320 | 16 | 32 | 20 | 16 | 3 | 12 |
| 336 | 16 | 32 | 21 | 16 | 4 | 11 |
| 352 | 32 | 16 | 11 | 8 | 2 | 5 |
| 384 | 32 | 16 | 12 | 8 | 3 | 4 |
| 416 | 32 | 16 | 13 | 8 | 4 | 3 |
| 448 | 64 | 8 | 7 | 4 | 2 | 1 |
| 512 | 64 | 8 | 8 | 4 | 3 | 0 |

## Impossible Rows

The `d=4` rows are impossible:

```text
261, 266, 276, 296, 336, 416.
```

Indeed, their complement sizes are odd. But `p_1(C)=p_3(C)=0`, and the local length-16 lemma says every local fiber has even size. Hence `|C|` must be even, a contradiction.

The row `A=448` is also impossible. There, `N=8`, `d=2`, and `c=1`. A one-point complement cannot satisfy `p_1(C)=0`, since its only element is nonzero.

All sizes outside the survivor table are impossible by the divisibility gate. Combining these exclusions leaves exactly the admissible list stated at the start.

## Structural Families for Existing Rows

For `N >= 16`, define:

```text
Z_1(N,c) = {C subset G_N : |C|=c and p_1(C)=0}.

Z_2(N,c) = {C subset G_N : |C|=c and p_1(C)=p_2(C)=0}.

Z_3(N,c) = {C subset G_N : |C|=c and p_1(C)=p_2(C)=p_3(C)=0}.
```

For the `d=3` rows, the local description of `Z_3` is:

```text
B_a(omega)=B_a(omega^3)=0 for every local fiber a,
```

together with the `p_2` equations from the local-coordinate section. By the local length-16 lemma, each local imbalance vector is either zero or a signed skew shift of `Delta_0`.

The structural normal forms for the existing rows are:

| A | Q | N | d | c | complement family |
|---:|---:|---:|---:|---:|---|
| 258 | 1 | 512 | 1 | 254 | `C in Z_1(512,254)` |
| 259 | 1 | 512 | 2 | 253 | `C in Z_2(512,253)` |
| 260 | 1 | 512 | 3 | 252 | `C in Z_3(512,252)` |
| 262 | 2 | 256 | 2 | 125 | `C in Z_2(256,125)` |
| 264 | 2 | 256 | 3 | 124 | `C in Z_3(256,124)` |
| 268 | 4 | 128 | 2 | 61 | `C in Z_2(128,61)` |
| 272 | 4 | 128 | 3 | 60 | `C in Z_3(128,60)` |
| 280 | 8 | 64 | 2 | 29 | `C in Z_2(64,29)` |
| 288 | 8 | 64 | 3 | 28 | `C in Z_3(64,28)` |
| 304 | 16 | 32 | 2 | 13 | `C in Z_2(32,13)` |
| 320 | 16 | 32 | 3 | 12 | `C in Z_3(32,12)` |
| 352 | 32 | 16 | 2 | 5 | `C in Z_2(16,5)` |
| 384 | 32 | 16 | 3 | 4 | one coset of the order-4 subgroup of `G_16` |
| 512 | 64 | 8 | 3 | 0 | `C=emptyset` |

For every listed row,

```text
T = G_N \ C,
S = phi_Q^(-1)(T).
```

Conversely, every `A`-admissible support arises this way.

## Nonemptiness of the Existing Families

The `d=1` row `A=258` is nonempty: take `C` to be any union of `127` antipodal pairs in `G_512`.

For the `d=2` rows, use

```text
E_0 = {1, 2, 3, 13, 15} subset F_17^*.
```

Then

```text
sum_{x in E_0} x = 0,
sum_{x in E_0} x^2 = 0.
```

For `N=16`, this gives the `A=352` complement directly. For larger `N`, take

```text
C = E_0 union U,
```

where `U` is a union of enough complete order-4 cosets in `G_N` disjoint from `E_0`. Each order-4 coset contributes zero to `p_1` and `p_2`.

There are enough such cosets. At most five order-4 cosets meet `E_0`. In the rows

```text
N = 32, 64, 128, 256, 512,
```

the required numbers of extra order-4 cosets are

```text
2, 6, 14, 30, 62,
```

respectively, while at least

```text
N/4 - 5
```

order-4 cosets are disjoint from `E_0`.

For the `d=3` rows, take `C` to be a union of `c/4` complete order-4 cosets. Since `4` divides none of `1,2,3`, each such coset contributes zero to `p_1`, `p_2`, and `p_3`.

For `A=384`, the same argument also gives the full classification: a four-point complement with `p_1=p_2=p_3=0` has vanishing polynomial `X^4-c`, so it is exactly a coset of the unique order-4 subgroup of `G_16`.

For `A=512`, take `S=H`; then `x^512=1` for every `x in H`, so the agreeing polynomial is the constant `P(X)=1`.

## Final Theorem

For the field and subgroup above, with degree bound `deg P <= 256`, the `A`-admissible sizes in the full range

```text
258 <= A <= 512
```

are exactly

```text
258, 259, 260, 262, 264, 268, 272, 280,
288, 304, 320, 352, 384, 512.
```

For each admissible `A`, every admissible support is the full preimage of one of the quotient packets described in the structural family table. For every other `A`, either the dyadic divisibility gate rules it out or the quotient complement row is impossible.

## Review Points

The main points to audit are:

```text
1. The degree convention is deg P <= 256.
2. The local length-16 imbalance classification has exactly 17 ternary solutions.
3. The dyadic descent threshold is 5 * 2^r, using p_1,p_3,p_5.
4. The quotient identity L_S(X)=L_T(X^Q) matches the forced K_Q-periodicity.
5. The structural families Z_1, Z_2, and Z_3 are normal forms, not explicit orbit-representative lists.
```
