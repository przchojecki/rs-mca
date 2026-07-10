# Row-sharp Q zero-prefix summit: Myerson/Gaussian-period bridge

- **Status:** PROVED identification / AUDIT placement.  This note proves no
  row-sharp Q max-fiber theorem and closes no finite adjacent row.
- **Track:** `(Q)` prefix / quotient flatness, F2 lane.
- **Verifier:** `python3 experimental/scripts/verify_rowsharp_q_myerson_bridge.py`
- **Related local packet:** `experimental/notes/thresholds/cap25_finite_signed_census_frame.md`

## What is being added

The finite signed-census frame already records the exact Fourier, sign
quantization, ladder-variance, tower-transfer, and L-function diagonalization
identities for the F2 zero-prefix census.  This packet adds the missing
upstream-facing interpretation of that zero-prefix/summit slice:

```text
zero-prefix row-sharp-Q/F2 census
  -> subset / divisor prefix census by Newton
  -> subgroup-linear flatness error in the quotient slice
  -> Gaussian-period norm product, in Myerson's sense
```

The last arrow is the classical identity used by Habegger in *The Norm of
Gaussian Periods* (arXiv:1611.07287, equation labelled `eq:countN`, citing
Myerson's combinatorial problem).  If `G <= F_p^x` has order `f`, index `k`,
and `A_1,...,A_k` are representatives of `F_p^x/G`, then

```text
N_G := #{(x_1,...,x_k) in G^k : A_1 x_1 + ... + A_k x_k = 0}
N_G - f^k/p = ((p - 1)/p) * Delta_G
Delta_G = product_{t in F_p^x/G} sum_{g in G} zeta_p^{t g}.
```

So this quotient-slice flatness error is not merely analogous to
Gaussian-period norms; it is exactly the norm product.  The
verifier checks this identity in the cyclotomic integer ring
`Z[zeta_p] = Z[X]/Phi_p(X)`, not by floating point approximation.

## Regime map

This is useful for `(Q)` because it says the hard zero-prefix kernel sits in a
recognized open-problem family.  The known Gaussian-period norm results cited
in that literature are fixed-order statements: fixed period length `f`, with
`p -> infinity` and constants depending on `f`.  The official F2/Frobenius
tower rows require the period order to grow with the base prime.  Thus the
summit needed by the finite-prize ledger is a growing-order Myerson problem,
not a direct corollary of the fixed-order literature.

In the language of `agents.md`, this is not a replacement for the row-sharp Q
input.  It is a sharper statement of the remaining `(Q)` content and a reason
to treat low-moment, per-frequency Weil, or fixed-order Gaussian-period
shortcuts as route cuts unless they also print a growing-order argument.

## Checked algebraic joints

The verifier checks two exact joints.

1. **Myerson/Habegger subgroup census.**  For several small prime rows it
   computes `N_G` by exact dynamic programming and computes `Delta_G` as a
   product of Gaussian periods in `Z[X]/Phi_p(X)`.  It asserts that the product
   reduces to a rational integer and that `p*N_G - f^k = (p - 1)*Delta_G`.
2. **Newton/divisor zero-prefix dictionary.**  For small `mu_n` rows it
   independently counts size-`b` subsets with vanishing first `j` power sums and
   degree-`b` divisors of `X^n - 1` whose top `j` locator coefficients vanish.
   The counts agree at every checked depth.

Together with the signed-census frame already in tree, these checks make the
Q-lane reading precise: the zero-prefix census is an exact algebraic object
with a Gaussian-period norm face, an L-value modulus face, and a signed
Rademacher/Dedekind parity face.

## Non-claims

- No proof of `def:q-row-atom`, row-sharp Q max-fiber flatness, or any
  adjacent safe row.
- No claim that every row-sharp Q fiber is literally a Myerson subgroup
  equation; the bridge names the zero-prefix/summit quotient slice.
- No assertion that fixed-`f` Myerson/Habegger results imply the official
  growing-order rows.
- No use of floating-point Gaussian-period products as proof evidence.
- No change to the finite ledger; this is a `(Q)` orientation and bridge
  packet.

## Suggested use

Add this as a `(Q)` ledger cross-reference beside the finite signed-census
frame: the signed frame gives the exact internal coordinates, while this note
names the classical external problem and states the growing-order gap that a
full proof must close.
