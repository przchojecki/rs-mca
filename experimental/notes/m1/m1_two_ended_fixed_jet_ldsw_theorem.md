# M1 Two-Ended Fixed-Jet LDsw Transfer Theorem

Status: PROVED / AUDIT / TWO-ENDED-FIXED-JET-LDSW-THEOREM.

Date: 2026-06-24.

This note isolates the generic proof behind the Cycle119 strict-ball addendum.
Cycle116 uses a fixed top jet. Cycle119 trades one top coefficient for a fixed
endpoint coefficient: the locators have a common nonzero constant term and a
common top jet that is one coefficient shorter.

The companion verifier is:

```text
python3 experimental/scripts/verify_m1_two_ended_fixed_jet_ldsw_theorem.py
```

It checks exact finite-field toy instances for `sigma=2,...,6`, then checks
that the current Cycle119 row instantiates the theorem.

## Theorem

Let `D` be an `n`-point subset of a field `F`, with `0 notin D`, and let
`beta` be outside `D`. Let `J` range over `j`-subsets of `D`, and write

```text
P_J(X)=prod_{a in J}(X-a).
```

Assume:

```text
P_J(0)=c != 0                 independent of J,
deg(P_J-P_J') <= j-sigma+1   for every pair J,J',
sigma >= 2,
k = n-j-sigma,
P_J(beta) != 0               for every J.
```

Let `C=RS[F,D,k]`. Then one affine line `f+z g` has at least

```text
#{P_J(beta): J}
```

support-wise bad parameters at agreement `n-j`. In particular,

```text
LD_sw(C,n-j) >= #{P_J(beta): J}.
```

## Proof

Use the usual weighted Vandermonde parity check

```text
(Hw)_m = sum_{x in D} x^m w(x)/L_D'(x),  0<=m<j+sigma,
L_D(X)=prod_{x in D}(X-x).
```

Its kernel is `RS[F,D,k]`.

The annihilator of the syndrome span supported on `J` consists exactly of the
coefficient vectors of

```text
P_J(X) A(X),   deg A < sigma.
```

Indeed, such a polynomial has degree `<j+sigma` and vanishes on `J`, and the
dimension is `sigma`.

Now inspect the selected coefficients of `P_J A` in degrees

```text
0, j+1, j+2, ..., j+sigma-1.
```

The degree-zero coefficient is `c A(0)`. The high selected coefficients form a
triangular system in the remaining coefficients of `A`; they use only the
common top coefficients of `P_J` and have monic diagonal entries. Hence the map

```text
A -> selected coefficients of P_J A
```

is independent of `J` and invertible. Therefore there is one common linear
functional on those selected syndrome coordinates whose value on `P_J A` is
`A(beta)` for every `J`.

Let `A0` be the negative of that common functional, embedded as a syndrome
vector in the selected coordinates, and let

```text
B=(1,beta,beta^2,...,beta^{j+sigma-1}).
```

For each `J`, set

```text
z_J = 1/P_J(beta).
```

For every polynomial `A` with `deg A < sigma`, the annihilator pairing gives

```text
<P_J A, A0 + z_J B>
  = -A(beta) + P_J(beta)^(-1) P_J(beta) A(beta)
  = 0.
```

Thus `A0+z_J B` lies in the syndrome span supported on `J`; choose an error
word `e_J` supported on `J` with this syndrome.

As in the fixed-jet theorem, the word

```text
g(x)=L_D(beta)/(beta-x)
```

has syndrome `B`. Fix one `J0` and set `f=e_J0-z_J0 g`. Then for every `J`,

```text
H(f+z_J g-e_J)=0,
```

so `f+z_J g` agrees with a codeword on `D\J`, of size `n-j`.

For noncontainment, if `g` were explained by a codeword on `D\J`, then the
Vandermonde column at `beta` would lie in the span of the columns indexed by
`J`. This is impossible because `J union {beta}` has `j+1` distinct points and
`j+1 <= j+sigma`. Distinct values of `P_J(beta)` give distinct bad parameters.

## Cycle119 Instantiation

The Cycle119 strict-ball row takes

```text
K = F_17^32,
H = <theta>, |H|=512,
k = 256,
j = 249,
sigma = 7,
agreement = 263.
```

It uses the same native Cycle116 co-supports `J_T` of size `113`, plus a fixed
odd-coset block `R*` of size `136`. The complement odd-coset block `A*` has
size `120`, so

```text
143 + 120 = 263,
113 + 136 = 249,
256 + 249 + 7 = 512.
```

The two-ended hypotheses come from:

```text
P_T(X)=X^113-X^112+O(X^107),
color(T)=4 mod 16,
R*={theta eta^i:120<=i<=255}.
```

Multiplying by the fixed `R*` locator gives

```text
deg(P_R*(P_T-P_T')) <= 136+107 = 243 = 249-7+1,
```

which is exactly the two-ended top-jet condition. The color-shell condition
gives `P_T(0)=-1`, so

```text
P_T*(0)=-P_R*(0) != 0
```

is common. Since `P_R*(beta) != 0`,

```text
P_T*(beta)=P_R*(beta) 4(beta-1) Phi(T),
```

so the same Cycle84 count of distinct `Phi(T)` values gives
`52,747,567,092` distinct bad parameters.

Thus, conditional on the same finite Cycle84 count and official-source gates
as the Cycle120 audit, the strict-ball addendum is:

```text
LD_sw(RS[F_17^32,H,256],263) >= 52,747,567,092.
```

This gives distance `249`, strictly below the radius
`250=(125/256)512`.

## Remaining Imports

The theorem above is generic. Its Cycle119 instantiation still imports the
Cycle84 exact occupancy count, the Cycle116 slot identity and color-shell
checks, and official ABF source review before prize-facing promotion.
