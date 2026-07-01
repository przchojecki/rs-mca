# S3b.iii.3: fiber rigidity, and prop:noanchor read against the mechanisms

- **Status:** SKETCH / CONJECTURE, with one **correction** to earlier turns
  recorded in §3 and every quoted statement checked against the actual
  Paper B source (`tex/slackMCA_v4.tex`). All numerics machine-verified.
- **Parent:** `prize_proof_sketch_spine.md` S3b.iii; completes the mechanism
  cluster begun in `s3b_iii_1` (SPI) and `s3b_iii_2` (XR).

## 1. Fiber bookkeeping [verified toy + CONJECTURE]

For a slope `Z`, define `fiber(Z) = #(D_j ∩ P(ker M(Z)))` — valid locators
aligned at `Z`. Since `ker M(Z)` is a linear space, fibers are **linear-plane
sections of the divisor set**. Verified facts (F_13, `H = F_13^*`, `n=12`,
`k=3`, planted pair with agreement `A_0 = 10` at slope `Z=0`):

```text
window correction: the alignment window is m = 1..t (coefficients k+j..n-1
  of W*ell mod X^n - 1), NOT m = 0..t-1; the m=0 row sees the constant
  coefficient. With the corrected window the planted family appears exactly.
A=8 (t=5, j=4, deficiency 0): fiber = 45 = C(10,2) planted, 0 extras.
  Generic kernel is trivial at d=0, yet the planted slope has kernel dim 3 =
  A_0 - A + 1: TANGENT SLOPES ARE RANK-DROP SINGULARITIES, their fibers the
  common-divisor planes  ell_E * P(deg <= A_0 - A),  E = error co-support.
A=6 (t=3, j=6, deficiency 4): fiber = 210 = C(10,4) planted, 0 extras.
```

So the planted-fiber law `fiber = C(A_0, A_0 - A)` on the common-divisor
plane is exact in the toys, and large fibers came only from the paid
(tangent) structure — no unstructured extras at all.

**Conjecture F (fiber rigidity) [CONJECTURE].** Any linear plane
`P ⊆ P^j` with `#(P ∩ D_j)` super-poly in `n` contains common-divisor
structure: its `D_j` points share a divisor of degree `j - dim P + O(log_n)`
(tangent shape), or are stabilized by a proper quotient pullback (quotient
shape). Consequence: **unpaid fibers are poly**, so the locator-level FM
model and the slope-level count agree up to poly on the aperiodic stratum —
the missing bookkeeping step flagged in mechanism 1 §4.3.

## 2. The unification: Conjecture F is the parent of the repo's frozen core [textually grounded SKETCH]

Paper B's `prob:perfiber` (quoted from source): *"every fiber of the prefix
map `Phi_sigma(A) = (e_1(A), ..., e_sigma(A))` on s-subsets of H contains at
most `n^{O(1)}` ordered pairs that are prefix-equal mod p but not in
`Z[zeta]`."* But `e_i(A)` are elementary symmetric functions — i.e. **the
first sigma locator coefficients**. Fibers of `Phi_sigma` are therefore
COORDINATE-plane sections of the divisor set, and `prob:perfiber` is exactly
**Conjecture F specialized to prefix/coordinate planes**, with the
`Z[zeta]`-coincidences as the structured escape. The family portrait:

```text
Conjecture F     linear-plane sections of D_j have poly unpaid points
 |- prob:perfiber   coordinate (prefix) planes         [the paper's core]
 |- fiber(Z)        kernel planes ker M(Z)             [this note, S3b]
 |- L1 / #106 Q_1   list-side fibers ImgFib_U          [Codex's conjecture]
 |- SPI / XR        the alignment (quadric) version    [mechanisms 1-2]
```

Also recorded for S2 from the same source: `rem:aper` defines
quotient-periodic as denominator pullback through `x -> x^M`, `M | gcd(n,k)`
— matching the paid-strata geometry — and `conj:B` prices the removed
quotient mass at `2^{(beta/H) Q_H}` with (machine-verified closed forms)

```text
beta(1/2) = (1/2)log2(3) = 0.7925   H/beta = 1.2619
beta(1/4) = 0.7500                  H/beta = 1.0817
beta(1/8) = 0.5306                  H/beta = 1.0244
beta(1/16) = 0.3343                 H/beta = 1.0090
```

— these constants are the shape of `Paid(A)`'s quotient term (S2 turn).

## 3. prop:noanchor, read from the source — with a correction [ground truth]

**Actual statement** (`slackMCA_v4.tex:1269`): every pair `(S,T)` of
s-subsets is simultaneously an agreement pattern of some received word;
hence *"no word-free pair condition exists"*, and methods that certify by
**averaging over primes** (characteristic-zero anchors, density theorems)
*"are structurally incapable of bounding emca over all lines, the words
being quantified after the prime. The all-lines positive half rests
entirely on fixed-prime technology."*

**Correction to turns 1-3:** my earlier paraphrase attributed the four-tool
foreclosure to prop:noanchor. In the source, prop:noanchor forecloses only
the characteristic-zero-anchor / prime-averaging family; the four standard
attacks terminate at `prob:perfiber` for stated per-tool reasons:

```text
prime averaging          blocked at fixed p by construction (= noanchor)
polynomial method        Nullstellensatz coefficients on subgroup grids
                         become complete character sums
subgroup exp. sums       known ranges end at N >= p^{3/7+eps}
anticoncentration        forward inequalities reduce to the same
                         even-moment counts
```

**Assessment for the sketch's mechanisms:** ES-type incidence and the
exchange/expansion argument are **fixed-prime technology** — precisely the
category prop:noanchor says the positive half must live in; neither is
foreclosed by it. The live danger is the anticoncentration clause: any
version of XR/SPI whose only input is second/even moments reduces to "the
same even-moment counts" and dies at the same wall. Therefore the
mechanisms' essential content must be the **structure-crystallization step**
(the classification "dense alignment ⟹ paid"), which consumes odd/rigid
information that moments do not see. This sharpens where the new idea has
to live — and explains why the Hooley-Katz ODD-moment lane (#120) is
listed by the roadmap as an attack vector: odd moments are the cheapest
rigid input beyond the foreclosed even ones.

## 4. What this changes in the sketch

```text
- spine S3b.iii wording corrected (noanchor vs perfiber attribution);
- Conjecture F installed as the parent statement; prob:perfiber = its
  coordinate-plane case — so the sketch's fiber step and the paper's frozen
  core are ONE object, in different planes;
- the mechanisms' target refined: classification/crystallization, not
  moment bounds; averaged-XR remains valuable but cannot be the whole
  argument (it is even-moment-shaped);
- Paid(A)'s quotient term has explicit constants (beta table) — S2 next.
```

## 5. Forks

```text
F1: Conjecture F false for kernel planes but true for coordinate planes ->
    the alignment problem is genuinely harder than prob:perfiber; the
    kernel-plane extras become a new ledger candidate (S9).
F2: crystallization step exists only over Z[zeta] (char-0 coincidences) ->
    matches prob:perfiber's shape; the fixed-prime transfer is then the
    entire difficulty, and the BETA_2/monodromy lane is the natural (only)
    consumer — the sketch would then predict the prize waits on monodromy.
F3: odd-moment inputs suffice for crystallization -> the Hooley-Katz lane
    (#120) upgrades from attack vector to critical path; flag to the
    maintainer if the alpha scan supports it.
```
