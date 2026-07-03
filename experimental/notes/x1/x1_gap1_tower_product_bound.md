# X1 / GAP-1: tower product bound for non-equivariant periodic slopes

- **Status:** PROVED algebraic product theorem / AUDIT for GAP-1 use.
- **Agent/model:** Codex.
- **Date:** 2026-07-03.
- **DAG target:** `gap1_product_model`, feeding `gap1_noneq_mass`.
- **Inputs:** `x1_gap1_nonequivariant_periodic_evidence.md`,
  `x1_confinement_from_stabilizer.md`, and `x1_quotient_reduction.md`.

## Purpose

The E6 packet proves the base-line rank lemma in the case
`alpha^M in B`: one isotypic character contributes one `B`-line
`alpha^r B`, and multi-isotypic data contributes at most the product of the
per-character line counts.

This note records the corresponding tower statement.  If `alpha^M` lies in, or
generates, an intermediate field `K`, then each isotypic character contributes
one `K`-line.  If that `K`-valued quotient contribution has further periodic
structure, the same argument recurses down the tower.  In every case the
multi-isotypic slope set is bounded by the product of its per-character
contributions; there is no additional cross-character amplification.

This is the algebraic part of `gap1_product_model`.  It does not by itself
prove `gap1_noneq_mass <= poly(n) * FM`: that final step still requires the
per-character quotient-scale reserve/bookkeeping discussed in
`x1_quotient_reduction.md`.

## Setup

Let `B <= K <= F` be fields, let `H_n = <omega> <= B^*`, let `M | n`, and put
`zeta = omega^(n/M)`.  Let `S subset H_n` be `K_M=<zeta>`-stable.  Let
`alpha in F` and assume

```text
beta := alpha^M in K.
```

For a residue `r mod M`, let `U_r : S -> F` be `r`-isotypic with
`B`-valued quotient amplitudes:

```text
U_r(zeta x) = zeta^r U_r(x).
```

Let `P_r` be the Lagrange interpolant on `S` of degree `< |S|`.

## Theorem 1: one character maps into one intermediate-field line

For every residue `r`,

```text
P_r(X) = X^r G_r(X^M)       with G_r in B[Y],
P_r(alpha) = alpha^r G_r(beta) in alpha^r K.
```

Therefore the image of the whole `r`-isotypic quotient-amplitude space is
contained in the one-dimensional `K`-line `alpha^r K`.  Its size is at most
`|K|`, and more sharply at most the size of the actual per-character image

```text
A_r := { alpha^r G_r(beta) : G_r comes from the allowed r-isotypic data }.
```

### Proof

For `x in S`, both `P_r(zeta x)` and `zeta^r P_r(x)` agree with the
`r`-isotypic data on `S`.  The two polynomials have degree `< |S|`, so they
are identical.  Writing `P_r(X)=sum_i c_i X^i`, the identity gives
`(zeta^i - zeta^r)c_i=0`, hence `c_i=0` unless `i == r mod M`.

The quotient amplitudes and the support quotient are defined over `B`, so the
surviving coefficients lie in `B`.  Thus `P_r(X)=X^r G_r(X^M)` with
`G_r in B[Y]`.  Evaluating at `alpha` gives
`P_r(alpha)=alpha^r G_r(alpha^M)=alpha^r G_r(beta)`, and since
`beta in K`, this lies in `alpha^r K`.  This proves the claim.

## Theorem 2: non-equivariant mass is bounded by the per-character product

Let `R` be the active character set.  For general non-equivariant data

```text
U = sum_{r in R} U_r,
```

linearity of interpolation and evaluation gives

```text
P_U(alpha) = sum_{r in R} P_r(alpha).
```

Consequently the slope image satisfies

```text
{ P_U(alpha) : U uses characters in R }
    subseteq A_{r1} + ... + A_{rs},
```

where `R={r1,...,rs}`.  Hence

```text
|{ P_U(alpha) }| <= product_{r in R} |A_r| <= |K|^|R|.
```

Equivalently, over the base field `B`,

```text
rank_B { P_U(alpha) } <= sum_{r in R} rank_B(A_r)
                       <= |R| [K:B].
```

The inequality can be strict when the `K`-lines `alpha^r K` are linearly
dependent over `B` or when the sum map has collisions.  Equality is a special
case, not an assumption.

### Proof

The map from data on `S` to the interpolant and then to evaluation at `alpha`
is linear.  The isotypic decomposition is also linear.  Therefore the image of
the direct sum of active character spaces is contained in the Minkowski sum of
their individual images.  The cardinality of a sumset is at most the product of
the cardinalities of the factors, proving the displayed bound.  The rank bound
is the same statement after replacing each finite image by its `B`-linear span.

## Theorem 3: tower recursion

Assume now that the quotient contribution has a tower

```text
B = K_0 <= K_1 <= ... <= K_s = K
```

and that at some quotient level a per-character polynomial value
`G(beta)` has another periodic split.  Concretely, if `beta^L in K_{s-1}` and
the quotient data is `L`-isotypic, then the same proof gives

```text
G(Y) = Y^a H(Y^L),      H in K_{s-1}[T],
G(beta) in beta^a K_{s-1}.
```

For multiple quotient characters, the image of `G(beta)` is bounded by the
product of those lower-level per-character images.  Iterating down the tower
gives a product over terminal character leaves.  Thus tower recursion cannot
create more slope exponent than the product of the per-character leaf masses.

### Proof

Apply Theorem 1 with base field `K_{s-1}`, pole `beta`, period `L`, and
stabilizer generator at the quotient level.  Then apply Theorem 2 to the
active quotient characters.  Repeating the same argument at each lower field
level gives the stated terminal product bound.

If no further periodic split is present at a level, the recursion stops there;
the terminal factor is the actual image size at that primitive quotient scale.
This is exactly the per-scale reserve object isolated in
`x1_quotient_reduction.md`.

## Consequences for GAP-1

1. The E6 base case extends cleanly from `alpha^M in B` to
   `alpha^M in K`: replace one `B`-line by one `K`-line.
2. Multi-isotypic periodic data cannot amplify beyond the product of the
   active per-character images.  The only possible mass comes from the
   per-character quotient-scale leaves.
3. Therefore any GAP-1 proof may focus on the per-character reserve/fiber
   problem at quotient scales.  A counterexample must exceed a per-character
   leaf bound, not arise from cross-character mixing.

The final polynomial `gap1_noneq_mass` bound follows only after those terminal
per-character leaves are shown to satisfy the required reserve estimate.  This
note proves the algebraic product mechanism, not that reserve estimate.

## Existing checks

The existing E6 verifiers cover the base-field case and product-bound behavior:

```bash
python3 experimental/scripts/verify_x1_gap1_nonequivariant_periodic_evidence.py
python3 experimental/scripts/verify_x1_nonequivariant_product_bound.py
python3 experimental/scripts/verify_x1_gap1_tower_product_bound.py
```

They report no examples exceeding the per-character product rank in the tested
`F_13`, `F_97`, and `F_257` periodic models.  The tower verifier checks the
intermediate-field case `F_17(alpha)`, `K=F_17(alpha^2)`: period-2 characters
land in `K` and `alpha K`, and all tested multi-character ranks are bounded by
the sum of their per-character ranks.
