# X1 / E6: GAP-1 non-equivariant periodic evidence

- **Status:** PROVED local rank lemma + EXPERIMENTAL / AUDIT evidence.
- **Agent/model:** Codex, acting autonomously for AllenGrahamHart.
- **Date:** 2026-07-02.
- **DAG target:** `gap1_noneq_mass`, `payment_completeness`.
- **Fable evidence item:** E6, "GAP-1 amplification".
- **Verifier:** `experimental/scripts/verify_x1_gap1_nonequivariant_periodic_evidence.py`.
- **Artifact:** `experimental/data/certificates/x1-gap1-nonequivariant-periodic-evidence/gap1_nonequivariant_periodic_evidence.json`.

## Purpose

This packet tests the GAP-1 evidence question from Fable's roadmap:

```text
Can non-equivariant periodic mass amplify beyond the per-character product
predicted by the isotypic decomposition?
```

It is evidence only.  It does not prove the L1/X1 quotient ledger, does not
close GAP-1, and does not change any Paper A-D statement.

## Local Rank Lemma

Let `B` be a field, let `H_n = <omega> <= B^*`, let `M | n`, and put
`zeta = omega^(n/M)`.  Let `S` be `K_M=<zeta>`-stable, and let
`alpha` lie in an extension field with `alpha^M in B`.

For a residue `r mod M`, suppose `U_r : S -> F` is `r`-isotypic and
base-amplitude valued, meaning

```text
U_r(zeta x) = zeta^r U_r(x)
```

and the free amplitudes on the quotient set `S/K_M` lie in `B`.  Let `P_r` be
the unique interpolant of degree `< |S|` agreeing with `U_r` on `S`.  Then

```text
P_r(X) = X^r G_r(X^M)          with G_r in B[Y],
P_r(alpha) in alpha^r B.
```

**Proof.**  For `x in S`, both `P_r(zeta x)` and `zeta^r P_r(x)` agree with
the data on the `K_M`-stable support.  The two polynomials have degree
`< |S|`, so they are equal.  Comparing coefficients gives zero coefficients
outside degrees congruent to `r mod M`.  Because the support and the quotient
amplitudes are defined over `B`, the surviving coefficients lie in `B`, giving
`P_r(X)=X^r G_r(X^M)`.  Evaluating at `alpha` gives
`P_r(alpha)=alpha^r G_r(alpha^M) in alpha^r B`.  Thus the image of the whole
`r`-character quotient-amplitude space is contained in the one-dimensional
`B`-line `alpha^r B`, independent of the number of quotient cosets.  ∎

For an active character set `R`, linearity gives

```text
{ P(alpha) : P uses only characters in R }
    subseteq sum_{r in R} alpha^r B.
```

Consequently the `B`-rank of the non-equivariant periodic slope family is at
most

```text
dim_B span{ alpha^r : r in R } <= |R|,
```

and the finite slope count is at most `|B|^rank`.  This proves, inside this
linear periodic model, that adding more `K_M` cosets cannot create extra slope
exponent.  The only possible growth is the expected per-character product, or
less if the lines `alpha^r B` are linearly dependent.

## Evidence Model

The input theory is the X1 confinement/isotypic package:

- `x1_confinement_from_stabilizer.md` proves confinement for a single
  equivariant character on a `K_M`-stable support.
- `x1_isotypic_decomposition.py` verifies that general periodic data decomposes
  into isotypic characters.
- `x1_nonequivariant_product_bound.py` proves the bounded-period product bound:
  non-equivariant slopes are sums of per-character confined slopes.
- `x1_quotient_reduction.md` reframes growing-period mass as a same-rate
  quotient-scale L1 problem.

The verifier stress-tests the lemma in cyclic rows `H_n <= F_p^*`, a period
`M | n`, and `K_M`-stable supports.  For each active set of isotypic characters
it computes the exact `F_p`-linear rank of

```text
data on S  ->  interpolant P_S  ->  P_S(alpha),
```

with `alpha^M in F_p`.  Thus the exact finite slope count for that linear family
is `p^rank`.

A GAP-1 amplification signal in this model would be:

```text
actual_rank > sum(per-character ranks)
```

or rank growth caused by adding more quotient cosets while keeping the active
character set fixed.

## Results

The verifier tests all `K_M`-stable supports in the small exact rows and spaced
constructive supports up to `n=256`.

| case | rows checked | max rank | max slope count | product-rank hits exceeded? | coset amplification? |
|---|---:|---:|---:|---:|---:|
| `F13`, `n=12`, `M=2`, all supports | 41 | 2 | `13^2` | 0 | 0 |
| `F13`, `n=12`, `M=4`, all supports | 66 | 4 | `13^4` | 0 | 0 |
| `F97`, `n=32`, `M=4`, all supports | 1012 | 4 | `97^4` | 0 | 0 |
| `F97`, `n=32`, `M=8`, all supports | 850 | 8 | `97^8` | 0 | 0 |
| `F257`, `n=64`, `M=8`, spaced supports | 765 | 8 | `257^8` | 0 | 0 |
| `F257`, `n=256`, `M=16`, spaced supports | 50 | 16 | `257^16` | 0 | 0 |

The packet classification is:

```text
NO_GAP1_AMPLIFICATION_SIGNAL_IN_TESTED_PERIODIC_MODELS
```

This is deliberately not a "small slope count" claim.  Full-character rows can
fill the expected extension degree, for example rank `16` in the
`F257, n=256, M=16` construction.  The point is that this is exactly the
per-character product model, not an additional GAP-1 mechanism.

## Interpretation

The tested models support the current X1/GAP-1 view:

1. A single character contributes one confined `F_p`-line.
2. Multiple characters add as an external product of those lines.
3. Adding more `K_M` cosets to the same active character set does not add slope
   exponent.
4. No tested row produces rank beyond the per-character product rank.

So the next proof target should not be "rule out mysterious extra
non-equivariant amplification" in this toy model.  The sharper remaining target
is the one already isolated in `x1_quotient_reduction.md`: track which quotient
scales are above their own reserve, and price the primitive core at those
scales.

If a later search finds a row with `actual_rank > product_rank`, this packet
should be used as the baseline for a COUNTEREXAMPLE/S9 update: record the
minimal support, active characters, quotient scale, and new ledger column.

## Reproducibility

```bash
python3 experimental/scripts/verify_x1_gap1_nonequivariant_periodic_evidence.py --emit
```
