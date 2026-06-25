# A0 Deep-Point Cap Dependency Split

## Status

PROVED local fiber-to-MCA cap route under Paper D's finite-field hypotheses /
AUDIT for the original CS25 import.

This note records the A0 dependency split created by the X1 deep-point route.
It does not certify the external Crites--Stewart theorem.  Instead it isolates
which part of Paper D's universal cap no longer needs that import.

## Claim

Under the finite-field, coset, divisibility, and binomial hypotheses of Paper
D's `thm:main`, the headline support-wise MCA cap has a local proof that does
not use the imported CS25/ABF list-to-agreement theorem:

```text
emca(C,delta) > (1/(2k)) (1 - n/q)
```

for every `delta_N <= delta < 1-rho`, where
`q=|F|` and `delta_N = 1-rho-2/N`.  The local proof is:

1. the elementary locator-fiber construction gives a `C+` list of size

```text
L >= binom(N,rho N+2)/|B| >= q/k + 1;
```

2. the simple-pole transfer and deep-point averaging give a line with at least

```text
M >= L / (1 + k(L-1)/(q-n))
```

bad slopes for `C=RS[F,D,k]`;

3. the exact algebra below gives

```text
M/q > (1/(2k)) (1 - n/q).
```

Thus the headline MCA cap has a CS25-free route.  The original CS25/ABF import
still needs source verification for the original CA-to-list proof, the Paper B
import surface, and any statement that explicitly cites the imported theorem.

## Elementary Fiber Lower Bound

We spell out the part of Paper D's `lem:fiber(ii)` used here.  Let
`B subset F` be finite fields, let `D subset B^*` be a multiplicative coset of
order `n`, let `N|n`, set `a=n/N`, and suppose `a|k`.  Put
`rho=k/n`, `ell=rho N+2=k/a+2`, and assume `ell<=N`.  Let
`Q=D^a`; the map `D -> Q`, `x -> x^a`, has fibers `S_b` of size `a`.

For each `ell`-subset `A subset Q`, define

```text
L_A(X) = prod_{b in A}(X^a-b)
       = X^{k+2a} - e_1(A)X^{k+a} + R_A(X),
```

where `deg R_A <= k`.  Set

```text
z_A = -e_1(A) in B,
u_z(x) = x^{k+2a} + z x^{k+a},
c_A(x) = -R_A(x).
```

Then `c_A in RS[B,D,k+1] subset RS[F,D,k+1]`.  On the root set
`S_A = union_{b in A} S_b`, which has size `a ell = k+2a`, one has
`u_{z_A}(x)=c_A(x)`.  Hence `c_A` is in the `C+` list of `u_{z_A}` at radius

```text
delta_N = 1 - (k+2a)/n = 1 - rho - 2/N.
```

For a fixed slope `z`, the map `A -> c_A` is injective on subsets with
`z_A=z`: if `z_A=z_{A'}` and `c_A=c_{A'}`, then `R_A` and `R_{A'}` agree on
all `n` points of `D`; since both have degree at most `k<n`, they are equal.
The top two coefficients also agree, so `L_A=L_{A'}` and therefore `A=A'`.

Since `z_A` takes at most `|B|` values as `A` ranges over the `binom(N,ell)`
subsets, some `z in B` has at least `binom(N,ell)/|B|` distinct listed
codewords.  This proves the local list lower bound consumed by the cap route.

## Simple-Pole Transfer

Let `D subset F`, `|D|=n`, `alpha in F \ D`, `k<m<=n`, and let
`C=RS[F,D,k]`, `C+=RS[F,D,k+1]`, with the convention that `RS[...,k]` means
polynomials of degree `<k`.  Given a received word `U : D -> F`, form the line

```text
f_alpha(x) = U(x)/(x-alpha),
g_alpha(x) = -1/(x-alpha).
```

For radius `delta_m = 1-m/n`, define

```text
List_+(U,m) = { P in F[X]_{<k+1} :
                |{x in D : P(x)=U(x)}| >= m },
Deep_alpha(U,m) = { P(alpha) : P in List_+(U,m) }.
```

Then the slopes `z` for which `f_alpha + z g_alpha` is `delta_m`-close to
`C` are exactly `Deep_alpha(U,m)`.

Indeed, if `P in List_+(U,m)` and `z=P(alpha)`, then

```text
Q(X) = (P(X)-P(alpha))/(X-alpha)
```

has degree `<k`, and on the agreement support of `P` with `U`,

```text
f_alpha(x) + z g_alpha(x) = (U(x)-z)/(x-alpha) = Q(x).
```

Conversely, if `f_alpha + z g_alpha` agrees with a degree-`<k` polynomial
`Q` on a support `S` of size at least `m`, then

```text
P(X) = (X-alpha)Q(X) + z
```

has degree `<k+1`, satisfies `P(alpha)=z`, and agrees with `U` on `S`.  Hence
`z in Deep_alpha(U,m)`.

The support-wise MCA obstruction for this line is automatic in the range
`m>k`.  If `g_alpha` agreed with a degree-`<k` polynomial `G` on any support of
size `>k`, then `(X-alpha)G(X)+1` would be a degree-`<=k` polynomial with more
than `k` roots in `D` but value `1` at `alpha`, impossible.  Therefore, on the
support `S` of size at least `m` supplied above, the endpoints
`f_alpha,g_alpha` cannot be simultaneously explained by two codewords of `C`:
simultaneous explanation would in particular explain `g_alpha` on `S`.  Hence
each slope in `Deep_alpha(U,m)` is MCA-bad in Paper D's support-wise sense.

## Deep-Point Averaging

Let `Omega = F \ D`, so `|Omega| = q-n`, and let
`List_+(U,m) = {P_1,...,P_L}`.  For distinct `i,j`, the polynomial
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

The density supplied by averaging is

```text
L(q-n) / ( q(q-n+k(L-1)) ).
```

The desired strict comparison with Paper D's cap constant is

```text
L(q-n) / ( q(q-n+k(L-1)) ) > (q-n)/(2kq).
```

Since `q>n`, this is equivalent to

```text
2kL > q-n+k(L-1),
```

or

```text
kL - q + n + k > 0.
```

The Paper D fiber hypothesis `L >= q/k+1` gives `kL >= q+k`, so the last
quantity is at least `n+2k`, hence positive.  This proves the local cap
constant strictly at `delta_N`.  Support-wise MCA monotonicity then extends the
same strict lower bound to every `delta_N <= delta < 1-rho`.

## Dependency Consequence

The A0 status should therefore be split:

- **Original CS25 route:** still conditional until the external theorem is
  checked against the Paper D restatement.
- **Headline MCA cap route:** no longer needs CS25 as a load-bearing theorem;
  it uses the elementary fiber lower bound, the simple-pole transfer, the
  deep-point averaging lemma, and the algebra above.
- **Promotion caveat:** Papers A--D should not be edited from this note alone.
  A human review should first check notation compatibility with Paper D.

## Verifier

Run from the repository root:

```sh
python3 experimental/scripts/verify_a0_deep_point_cap_algebra.py
python3 experimental/scripts/verify_a0_deep_point_cap_algebra.py --json
python3 experimental/scripts/verify_x1_lem_fiber.py
python3 experimental/scripts/verify_x1_deep_point_identity.py
```

The verifier checks the exact rational inequality on a grid of finite
parameters and records the symbolic residual
`kL-q+n+k` controlling the comparison.  The fiber verifier brute-checks the
locator-polynomial construction over `F_17`; the X1 identity verifier
independently brute-checks the simple-pole transfer over prime-field toy
models.
