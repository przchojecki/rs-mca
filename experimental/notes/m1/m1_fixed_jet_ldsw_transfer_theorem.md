# M1 Fixed-Jet Locator-To-LDsw Transfer Theorem

Status: PROVED / AUDIT / GENERIC-FIXED-JET-LDSW-THEOREM.

Date: 2026-06-24.

This note isolates the generic proof-logic core used by the Cycle116 transfer:
a family of co-support locators with a common top jet gives one affine line
with one support-wise bad parameter for each distinct value of `P_J(beta)`.

The companion verifier is:

```text
python3 experimental/scripts/verify_m1_fixed_jet_ldsw_theorem.py
```

It checks the syndrome identities below on exact finite-field toy cases, then
checks that the current Cycle116/Cycle120 local verifiers supply the large
instance hypotheses consumed by the theorem.

## Theorem

Let `D` be an `n`-point subset of a field `F`, let `beta` be outside `D`, and
let `J` range over `j`-subsets of `D`. Write

```text
P_J(X)=prod_{a in J}(X-a).
```

Assume:

```text
deg(P_J-P_J') <= j-sigma       for every pair J,J',
sigma >= 1,
k = n-j-sigma,
P_J(beta) != 0                 for every J.
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

Let

```text
L_D(X)=prod_{x in D}(X-x)
```

and use the parity check

```text
(Hw)_m = sum_{x in D} x^m w(x)/L_D'(x),  0<=m<j+sigma.
```

The kernel of `H` is `RS[F,D,k]`, since this is the usual dual Vandermonde
parity check with redundancy `j+sigma=n-k`.

For a co-support `J`, put

```text
e_J(x)=L_D'(x)/((beta-x)P_J'(x))   if x in J,
e_J(x)=0                           if x notin J,
z_J=1/P_J(beta).
```

For each `m<j+sigma`, divide

```text
X^m = Q_{m,J}(X) P_J(X) + R_{m,J}(X).
```

Because the top `sigma` coefficients of all `P_J` agree, long division gives
the same quotient `Q_m` for every `J` in this range. Lagrange interpolation on
`J` gives

```text
(H e_J)_m = R_{m,J}(beta)/P_J(beta)
          = beta^m/P_J(beta) - Q_m(beta).
```

Thus

```text
H e_J = A + z_J B,
A_m=-Q_m(beta),
B_m=beta^m.
```

Now define

```text
g(x)=L_D(beta)/(beta-x).
```

Full-domain Lagrange interpolation gives `H g = B`. Fix one `J0` and set

```text
f=e_J0-z_J0 g.
```

For every `J`,

```text
H(f+z_J g-e_J)=0,
```

so `c_J=f+z_J g-e_J` is a codeword. Since `e_J` is supported on `J`, the line
point `f+z_J g` agrees with `c_J` on `D\J`, which has size `n-j`.

It remains to check support-wise noncontainment. If `g` agreed with a codeword
on `D\J`, then `g-h` would be supported on `J` and would have syndrome `B`.
Equivalently, the Vandermonde column at `beta` would lie in the span of the
`j` columns indexed by `J`. But `J union {beta}` contains `j+1` distinct
points, and `j+1 <= j+sigma`, so those columns are independent. Hence no such
`h` exists, and the same support cannot simultaneously explain `(f,g)`.

Distinct values of `P_J(beta)` give distinct `z_J`, so the number of bad
parameters is at least the number of distinct `P_J(beta)` values.

## Cycle116/Cycle120 Instantiation

The current M1 chain supplies the theorem hypotheses as follows:

```text
verify_m1_cycle116_fixed_jet_bridge.py
  proves P_T(X)=X^113-X^112+O(X^107),
  so j=113 and sigma=6.

verify_m1_cycle116_fixed_jet_transfer.py
  checks beta outside D0, nonzero scalar kappa, and injectivity of
  Phi -> W(beta)-V_D(beta)/(4(beta-1)Phi).

verify_m1_cycle84_exact_occupancy_chain.py
  supplies 52,747,567,092 distinct Phi(T) values.

verify_m1_cycle116_smooth_padding_transfer.py
  pads the same fixed-jet theorem to the smooth row with
  j=250, sigma=6, k=256, agreement=262.
```

Thus the remaining external PR #96 verifier is no longer needed as an opaque
proof-logic import. Its hash/source and executable replay are still useful
provenance checks, but the fixed-jet theorem used by the M1 chain is recorded
locally here.

## What This Does Not Prove

This theorem does not prove the Cycle84 product occupancy count, the slot
identity replay, or official ABF source compatibility. Those remain separate
audits in the Cycle120 finite chain.
