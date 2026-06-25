# A0 Deep-Point Cap Dependency Split

## Status

PROVED simple-pole transfer and local algebra / CONDITIONAL on the supplied
`C_+` list lower bound.

This note records the A0 dependency split created by the X1 deep-point route.
It does not certify the external Crites--Stewart theorem.  Instead it isolates
which part of Paper D's universal cap no longer needs that import.

## Claim

Assume `lem:fiber(ii)`, or any replacement source, gives a word `U : D -> F`
whose list in `C+ = RS[F,D,k+1]` has size `L` at the Paper D cap radius.  Then
the simple-pole construction below gives a line for `C=RS[F,D,k]` with at least

```text
M >= L / (1 + k(L-1)/(q-n))
```

bad slopes, where `q=|F|` and `n=|D|`.

Then the Paper D hypothesis

```text
L >= q/k + 1
```

implies the same MCA cap constant as `thm:main`:

```text
emca(C,delta) >= M/q >= (1/(2k)) (1 - n/q).
```

Thus the headline MCA cap has a CS25-free route once the local list-lower-bound
input is accepted.  The original CS25/ABF import still needs source
verification for the original CA-to-list proof, the Paper B import surface, and
any statement that explicitly cites the imported theorem.

## Simple-Pole Transfer

Let `D subset F`, `|D|=n`, `alpha in F \ D`, `k<a<=n`, and let
`C=RS[F,D,k]`, `C+=RS[F,D,k+1]`, with the convention that `RS[...,k]` means
polynomials of degree `<k`.  Given a received word `U : D -> F`, form the line

```text
f_alpha(x) = U(x)/(x-alpha),
g_alpha(x) = -1/(x-alpha).
```

For radius `delta_a = 1-a/n`, define

```text
List_+(U,a) = { P in F[X]_{<k+1} :
                |{x in D : P(x)=U(x)}| >= a },
Deep_alpha(U,a) = { P(alpha) : P in List_+(U,a) }.
```

Then the slopes `z` for which `f_alpha + z g_alpha` is `delta_a`-close to
`C` are exactly `Deep_alpha(U,a)`.

Indeed, if `P in List_+(U,a)` and `z=P(alpha)`, then

```text
Q(X) = (P(X)-P(alpha))/(X-alpha)
```

has degree `<k`, and on the agreement support of `P` with `U`,

```text
f_alpha(x) + z g_alpha(x) = (U(x)-z)/(x-alpha) = Q(x).
```

Conversely, if `f_alpha + z g_alpha` agrees with a degree-`<k` polynomial
`Q` on a support `S` of size at least `a`, then

```text
P(X) = (X-alpha)Q(X) + z
```

has degree `<k+1`, satisfies `P(alpha)=z`, and agrees with `U` on `S`.  Hence
`z in Deep_alpha(U,a)`.

The support-wise MCA far condition for this line is automatic in the range
`a>k`: if `g_alpha` agreed with a degree-`<k` polynomial `G` on any support of
size `>k`, then `(X-alpha)G(X)+1` would be a degree-`<=k` polynomial with more
than `k` roots in `D` but value `1` at `alpha`, impossible.  Thus the same
slopes are support-wise MCA-bad slopes.

## Deep-Point Averaging

Let `Omega = F \ D`, so `|Omega| = q-n`, and let
`List_+(U,a) = {P_1,...,P_L}`.  For distinct `i,j`, the polynomial
`P_i-P_j` has degree at most `k`, so

```text
|{alpha in Omega : P_i(alpha)=P_j(alpha)}| <= k.
```

For each `alpha`, let `r_alpha = |{P_i(alpha) : 1<=i<=L}|` and let
`e_alpha` be the number of ordered collisions `(i,j)` with
`P_i(alpha)=P_j(alpha)`.  Then

```text
sum_alpha e_alpha <= L|Omega| + kL(L-1).
```

Some `alpha` has

```text
e_alpha <= L(1 + k(L-1)/|Omega|).
```

Since `L^2 <= r_alpha e_alpha` by Cauchy-Schwarz on the fibers of
`P_i -> P_i(alpha)`, this `alpha` satisfies

```text
r_alpha >= L / (1 + k(L-1)/|Omega|).
```

By the simple-pole transfer, that `alpha` gives a line with at least this many
MCA-bad slopes.

## Algebra

The desired comparison is

```text
L(q-n) / ( q(q-n+k(L-1)) ) >= (q-n)/(2kq).
```

Since `q>n`, this is equivalent to

```text
2kL >= q-n+k(L-1),
```

or

```text
kL - q + n + k >= 0.
```

The Paper D fiber hypothesis `L >= q/k+1` gives `kL >= q+k`, so the last
quantity is at least `n+2k`, hence positive.  This proves the local cap
constant directly from the simple-pole construction.

## Dependency Consequence

The A0 status should therefore be split:

- **Original CS25 route:** still conditional until the external theorem is
  checked against the Paper D restatement.
- **Headline MCA cap route:** no longer needs CS25 as a load-bearing theorem;
  it can use `lem:fiber(ii)`, the simple-pole transfer, the deep-point
  averaging lemma, and the algebra above.
- **Promotion caveat:** Papers A--D should not be edited from this note alone.
  A human review should first check the `lem:fiber(ii)` lower-bound proof and
  notation compatibility with Paper D.

## Verifier

Run from the repository root:

```sh
python3 experimental/scripts/verify_a0_deep_point_cap_algebra.py
python3 experimental/scripts/verify_a0_deep_point_cap_algebra.py --json
python3 experimental/scripts/verify_x1_deep_point_identity.py
```

The verifier checks the exact rational inequality on a grid of finite
parameters and records the symbolic residual
`kL-q+n+k` controlling the comparison.  The X1 identity verifier independently
brute-checks the simple-pole transfer over prime-field toy models.
