# S3b.iii mechanism 1: divisor-variety / pencil-incidence rigidity (SKETCH)

- **Status:** SKETCH / CONJECTURE / GAP-WALL, labelled per node. NOT rigorous.
- **Parent:** `prize_proof_sketch_spine.md`, node S3b.iii. All arithmetic
  machine-checked before commit.
- **Role:** the sketch's preferred mechanism for making the first-moment
  model rigorous on the aperiodic stratum — the incidence-geometry route.
  Mechanism 2 (displacement/spectral) is a separate child file.

## 1. The two objects [SKETCH, exact definitions]

Fix `(u,v)` and exact agreement `A` (`t = A-k`, `j = n-A`, deficiency
`d = j+1-t`). In locator coefficient space `P^j`:

**The divisor set** `D_j = {squarefree monic degree-j divisors of X^n - 1}`,
`|D_j| = C(n,j)`. Algebraically `D_j = V(R_0, ..., R_{j-1})` where `R_m(l)`
is the `X^m`-coefficient of `(X^n - 1) mod l` — the same remainder system as
the WP-2.6 divisibility filter, with the locator free instead of
Cramer-parametrized. `D_j` carries the full symmetry of the group `H`
(translation by `H`, the Galois/Frobenius action, and the quotient maps
`x -> x^e` for `e | n`).

**The alignment variety** `X_{u,v} = V(Q_rs : 0 <= r < s < t)` where

```text
Q_rs(l) = (H_u l)_r (H_v l)_s - (H_u l)_s (H_v l)_r,
```

the 2x2 minors of the `2 x t` matrix `(H_u l ; H_v l)` — `t(t-1)/2` quadrics
(8128 at A=384). Since the rank-<=1 locus of `2 x t` matrices has codimension
`t-1`, the expected dimension is

```text
dim X_{u,v} = j - (t-1) = d      (machine-checked: A=384 -> dim 1 curve;
                                  A=340 -> 89; A=265 -> 239).
```

**Exact statement of the count [PROVED-cited frame, spine SS2]:**

```text
B_C(A) <= #(D_j  intersect  X_{u,v}) ,
```

with slopes recovered per aligned locator (<= 1 each, v8 ledger; the
`a = b = 0` stratum is the noncontainment exclusion, i.e. `X` contains the
"both-syndromes-vanish" LINEAR subspace `ker H_u cap ker H_v`, dim `>= j+1-2t`,
whose `D_j`-points are contained pairs — excluded, not counted).

## 2. What "paid" means geometrically [SKETCH]

The known mechanisms by which `#(D_j cap X_{u,v})` gets LARGE are special
positions of `X_{u,v}` relative to the symmetry of `D_j`:

```text
tangent:   (u,v) within radius of a common line -> a positive fraction of
           X's points over ONE slope fiber; many locators, ONE slope each —
           large locator count, small slope count. Paid by B_tan.
quotient:  (u,v) with K_e-periodic structure -> X_{u,v} is invariant under
           a subgroup action and meets the K_e-stable stratum of D_j
           (locators that are polynomials in X^e) in a combinatorially
           inflated set. Paid by B_quot. [PROVED-cited: the confinement /
           equivariance theorems — periodic supports <-> confined slopes.]
extension: pole structure over F \ B. Paid by B_ext.
```

**The aperiodic stratum is, by construction, `(u,v)` for which `X_{u,v}` has
no such special position.** The rigidity question: can a variety of
dimension `d` and controlled structure meet the `C(n,j)`-point set `D_j` in
super-poly-many UNSTRUCTURED points?

## 3. The core conjecture and the named wall

**Conjecture R2 (incidence rigidity) [CONJECTURE].** For every pair `(u,v)`,

```text
#( D_j cap X_{u,v} \ paid strata )  <=  n^B * max(1, C(n,j) / q^(t-1)),
```

with an absolute per-rate exponent `B`. Budget check (machine-verified): the
safe side tolerates `B <= 3` at `n = 2^41` (`3*41 = 123 < 128` bits), and
the induced shift of the R1 reserve is `~2^-33` — invisible at the `2^-8`
corridor. So R2 with `B <= 3` suffices for the full grand-MCA safe side
below `d_fm`.

**Named wall: SPI (structured-pencil incidence hypothesis) [GAP-WALL].**
The generic-position version of R2: a degree-controlled, displacement-
structured variety of dimension `d` cannot contain more than
`n^B * (density)` points of `D_j` unless it lies in a paid stratum. This is
the object to freeze with a consumer theorem (consumer: SPI + strip-periodic
(S3b.ii) + Paid(A) closure (S2) => R2 => S3b => per-rate grand MCA with S5).

## 4. Why this could be true — and what tool family it lives in [SKETCH]

1. **Elekes-Szabo phenomenology.** `D_j` is a "combinatorially structured"
   finite set (all j-subsets of a multiplicative group), and ES-type theorems
   say: a low-dimensional variety cannot over-intersect a product-structured
   set unless the variety is special, where "special" means group-related
   (cosets/subgroups). The striking match: the ES special cases correspond
   exactly to the PAID strata (quotient = subgroup structure, tangent =
   graph-of-a-line structure). The sketch's bet: an ES-type theorem for
   subset-power sets `H^(j)` in place of Cartesian products, over `F_q`,
   with the exceptional varieties classified as paid.
2. **The base case is already provable machinery.** At `d = 1` (A=384),
   `X_{u,v}` is the Cramer CURVE `Z -> L(Z, .)` and SPI reduces to
   elimination: the WP-2.6 rung-1 eliminant bounds
   `#(curve cap D_j) <= 49408` for the declared family — poly, unconditional
   once the chart closes. **WP-2.6 is SPI at dimension 1; the deficiency
   ladder is SPI dimension growth.** This is the sketch's strongest internal
   coherence point: the running PR #172 is already testing the mechanism's
   base case (prediction P3).
3. **Fiber bookkeeping is exact.** Slopes-vs-locators is not a leak: per
   locator <= 1 slope (v8); large fibers force tangent/quotient structure
   (SKETCH claim, refine later: "unpaid fibers are O(1)" — this is where the
   noncontainment gate and the pencil-degeneracy analysis do work).
4. **Not in the foreclosed toolkit.** prop:noanchor forecloses
   prime-averaging, polynomial method (in its anchor form), subgroup
   exponential sums, anticoncentration. Incidence/ES methods over `F_q` are
   a genuinely different hammer (with the honest caveat that some incidence
   proofs internally use polynomial partitioning — the foreclosure argument
   should be re-read against ES specifically; queue this as a check).
5. **Averaged version = Hooley-Katz lane.** Odd-moment / average-case
   versions of R2 over `(u,v)` are exponential-sum-friendly (the Scott #120
   direction): plausibly PROVABLE and would confirm FM on average. The wall
   is the worst-case de-correlation — exactly the shape of every deep
   incidence theorem (average easy, worst-case is the theorem).

## 5. Quantitative targets per rung [SKETCH, numbers verified]

```text
d = 1   (A = 384 pinned row):  eliminant degree <= 49408; SPI(1) provable by
        elimination for declared families; target: remove the declared-family
        hypothesis via U2-style genericity or per-family enumeration.
d small (ladder rungs A = 384 - 2m): elimination in d+1 variables; measure
        degree growth; SPI(d) by resultant towers while effective.
d in-band (the real target, d ~ n(delta - (1-rho)/2 + 1/n)): elimination is
        hopeless (d = 239 already at the pinned row's A=265); SPI must come
        from a dimension-free argument: ES-type incidence, or displacement
        structure (mechanism 2), or moment+rigidity hybrid.
```

**Honest stall risk:** if no dimension-free form materializes, the route
stalls at bounded `d` — which pins additional grid points near the regular
boundary but never reaches the band. This is the sketch's sharpest
single risk; it is why mechanism 2 (displacement/spectral, dimension-free by
construction) is refined next even though mechanism 1 is geometrically
cleaner.

## 6. Forks and failure branches

```text
F1: an unpaid special variety class exists (ES exceptional case that is not
    tangent/quotient/extension) -> it IS a new ledger; add to Paid(A),
    re-run S5 (spine S9 branch). The prize is still resolved, lower.
F2: SPI provable only on average -> the grand challenges as stated (worst
    row in family) may still follow IF the family quantifier lets averaged
    bounds pick the row — check official wording (WP-0.2); else partial.
F3: SPI(d) only for d <= d_0 -> partial: extended safe grid near the regular
    boundary; band open; document as interim dossier result.
F4: prop:noanchor extends to ES-type arguments -> mechanism 1 dead; weight
    shifts to mechanism 2 and the monodromy route (BETA_2 instantiation).
```

## 7. Next refinements queued from this note

```text
- mechanism 2 child: displacement/spectral route (the #170 identities as a
  dimension-free handle on X_{u,v}: alignment = rank-1 displacement
  perturbation; connect det(I + Z K_h) spectra to incidence counts);
- "unpaid fibers are O(1)" sub-sketch (fiber bookkeeping, feeds SS4.3);
- re-read prop:noanchor against ES/incidence methods (F4 check);
- SPI freeze note draft (frozen statement + consumer theorem + toy
  reproduction at d=1  — the WP-2.6 acid test doubles as SPI(1)'s toy).
```
