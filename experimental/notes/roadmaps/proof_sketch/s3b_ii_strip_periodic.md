# S3b.ii: the strip-periodic step — exact statement of the aperiodic stratum

- **Status:** PROVED-cited backbone (the x1 confinement/equivariance
  theorems on main + verified stratum combinatorics) with the residual
  holes stated as named GAPs. NOT rigorous as a whole.
- **Parent:** `prize_proof_sketch_spine.md` S3b.ii. Numerics machine-checked.

## 1. Two nonequivalent notions of "periodic" [PROVED-cited]

**Support-side (geometric).** A locator `l` is `M`-periodic if its root set
`T` is a union of `K_M`-cosets (`K_M` = order-`M` subgroup), equivalently
`l(X) = g(X^M)` up to normalization. Requires `M | gcd(n, j)`. Verified
counts: the `M`-periodic stratum of `D_j` has size `C(n/M, j/M)` exactly
(enumerated at `(n,j) = (12,4)`: 15 at `M=2`, 3 at `M=4`, 0 at `M=3`).

**Line-side (rem:aper, Paper B source).** A residue line is
quotient-periodic if its DENOMINATOR is a pullback through `x -> x^M`,
`M | gcd(n,k)`, `M > 1`; `Lambda^aper` is the packing number with those
lines removed.

**The bridge is my proved confinement/equivariance pair** (x1 notes, main):
zeta-equivariant word + `K_M`-stable support => the completion folds
(`P_S = X^r G(X^M)`) and the slope confines — support-periodicity becomes
line-periodicity. The isotypic refinement shows the bridge is EXACT only on
the equivariant stratum: multi-isotypic words on stable supports produce
slopes that escape confinement (verified witness on main).

## 2. The strip, and where the paid mass actually comes from [SKETCH on proved parts]

For UNSTRUCTURED pairs, periodic locators get no alignment boost: FM1 gives
the same `q^{1-t}` per locator, and the periodic strata are exponentially
thin (`C(n/M, j/M)` vs `C(n,j)`), so their FM mass is negligible. The paid
quotient mass comes from STRUCTURED pairs, where the `t` syndrome conditions
fold to `~t/M` conditions on the quotient row — probability boosted to
`q^{1-t/M}` — which is exactly the proved multi-scale recursion
`Q_M(H_n) = Q_1(H_{n/M})` (rate-preserved, x1 quotient reduction on main).
Stripping convention for the chain: remove ALL periodic locators from the
aperiodic count and pay them at their own quotient scale (conservative —
their unstructured alignment probability is never above the generic one);
dedup enforced at locator level by the WP-0.4 checker.

## 3. The two named holes in the strip [GAP]

**GAP-1 (non-equivariant periodic mass).** My isotypic theorem shows the
quotient PRICING (`2^{(beta/H) Q_H}`, value sets on the quotient) captures
the equivariant stratum, while multi-isotypic words on stable supports can
escape confinement. Their lines still have pullback denominators (so
rem:aper strips them) — but the PRICE of that stratum is not derived from
quotient value sets. Needed: `#(multi-isotypic periodic alignments) <=
poly(n) * FM` [CONJECTURE; evidence: escape witnesses exist but are
isolated; no inflation mechanism known]. If super-poly: a NEW ledger column
and an earlier unsafe side — recompute the S2 bracket.

**GAP-2 (definitional seam).** Support-side periodicity needs
`M | gcd(n, j)`; rem:aper's line-side uses `M | gcd(n, k)`. For `rho = 1/2`
rows these can differ (`j = n - A` vs `k`). Also the claim "stable support
=> pullback denominator" should be checked against the actual normal form
(`thm:normalform` / `def:residue`), which I have not yet read closely —
queued for the S4/S0 turn. Until then the correspondence is
SKETCH-pending-source-check, and the M4 dedup must pick ONE convention.

## 4. The strip in the mechanisms' language [verified combinatorics + SKETCH]

**For XR (exchange dynamics) — three verified facts:**

```text
(i)   the M-periodic stratum is an INDEPENDENT SET in the Johnson exchange
      graph: no two stable sets are adjacent (enumerated, 0 adjacent pairs);
(ii)  every one-exchange EXITS the stratum (enumerated: all exits);
(iii) coset-moves (exchange a whole K_M-coset) restore exactly the quotient
      Johnson graph J(n/M, j/M) on the stratum (15 = C(6,2) vertices).
```

Consequence: the exchange dynamics FACTOR through the quotient precisely as
the counting does — single-exchange pumping can never wander into the paid
stratum (it is dynamically invisible), and the structured mass lives on its
own quotient copy of the whole problem, one scale down. The multi-scale
self-similarity of the counting (`Q_M = Q_1` on the quotient) and of the
dynamics (coset-moves = quotient exchanges) is the same recursion — strong
evidence the stratification is the RIGHT one, not merely a convenient one.

**For SPI (incidence geometry):** the periodic strata are exactly the
subvarieties of `D_j` fixed by the `K_M`-actions — the group-special cases
that Elekes-Szabo-type statements must except. Post-strip, `D_j^aper`
carries no subgroup symmetry: the ES genericity hypothesis becomes
available, which is what mechanism 1 needs to even state its theorem.

## 5. The post-strip claim the mechanisms must prove [CONJECTURE — operative R2]

```text
For every pair (u,v) that is not tangent-structured:
   #{ aligned l in D_j^aper }  <=  n^B * max(1, C(n,j) q^{1-t}),
and tangent-structured pairs concentrate on common-divisor planes,
paid by B_tan after fiber conversion (Conjecture F).
```

Dictionary caution: `conj:B`'s positive half is stated for `Lambda^aper`
(a packing number over the slack-line family), while the above counts
aligned locators per pair. The exact quantifier dictionary
(per-pair counts <-> packing numbers) is queued as the FIRST item of the
S4 turn — the sketch does NOT assert they coincide, only that both
formalize "post-strip alignment is FM-small."

## 6. Forks

```text
F1: GAP-1 super-poly -> new ledger; unsafe side moves earlier; S2 bracket
    recomputed; the prize is still resolved (S9 posture).
F2: GAP-2 seam real (gcd(n,j) vs gcd(n,k) strips differ) -> pick the
    coarser strip for safety, price the difference explicitly; flag to
    WP-0.1 as a definitional axis.
F3: the coset-move recursion fails at some scale (e.g. n/M not smooth
    enough) -> the smoothness hypothesis earns its keep; document which
    scales the official rows actually expose (2-power n: all scales smooth
    — likely a non-issue for the prize family; verify per row in S5).
```
