# The Reed–Solomon MCA threshold: current final form

**Submission summary for the Proximity Prize committee — CAP25 (v12 + v13 raw).**

## 1. The answer, in one line

For `C = RS[F, D, k]` on a smooth multiplicative or circle domain `D ⊆ B`, rate `ρ`, base field `B`,
`β = log₂|B|`, the grand-challenge threshold is

```
δ*_C(ε*)  =  1 − ρ − g*(ρ, β) + o(1),      g*(ρ, β) = sup{ g : H₂(ρ+g) ≥ βg }
```

— the **entropy–subfield envelope**. The threshold is set by the base field alone (through `β`),
not by the challenge field `q`. Status: the `≥` direction at deployed sizes is **proved** to within
`< 10⁻⁶`; the matching `≤` direction is **conjectural** (Section 4). Everything known is consistent
with this closed form, and every mechanism that would beat it has been refuted (Section 2.3).

## 2. Proved unconditionally

### 2.1 Unsafe side (lower bounds on failure) — exact integer certificates

The identity-prefix floor (pigeonholing locator prefixes over `B`) plus the flexible-budget
deep-point conversion (v13 raw; the counting inside the list-to-CA conversion, run at the challenge
budget instead of the `q/k` threshold) give, at the deployed rows `n = 2²¹`, `k = 2²⁰`:

| row | target ε* | proved unsafe for δ ≥ | distance to envelope ceiling |
|---|---|---|---|
| KoalaBear sextic, MCA | 2⁻¹²⁸ | 981105/2097152 = 0.4678273… | 7.2·10⁻⁷ |
| KoalaBear sextic, list | 2⁻¹²⁸ | 490553/1048576 = 0.4678278… | 1.2·10⁻⁶ |
| Mersenne-31 circle, MCA | 2⁻¹⁰⁰ | 981129/2097152 = 0.4678388… | 4.9·10⁻⁷ |
| Mersenne-31 circle, list | 2⁻¹⁰⁰ | 490565/1048576 = 0.4678392… | 1.0·10⁻⁶ |

Each row is an exact integer comparison of the form `C(n,m) > p^w · ⌊ε*q⌋` (pass at the printed
edge, fail one step further), i.e. a finite, independently re-checkable certificate.

### 2.2 Safe side (upper bounds on failure)

Self-contained: `ε_mca ≤ n/q` for all `δ ≤ (1−ρ)/3` (deep regime). With one classical import
(BCIKS20 half-distance correlated agreement): safe up to `δ ≤ 1/4` at rate ½, both rows, below
both targets. Johnson-region list bounds close the list side up to `δ ≤ 1 − √ρ`.

**Resulting proved sandwich (rate ½, with the import):**
`δ*(2⁻¹²⁸) ∈ [0.25, 0.4678273]` (KoalaBear), `δ*(2⁻¹⁰⁰) ∈ [0.25, 0.4678388]` (M31);
self-contained lower edge `(1−ρ)/3 ≈ 0.1667`.

### 2.3 Structural theorems (all unconditional)

- **Witness classification.** For the pole lines realizing the floors, the threshold-`m` witness
  supports of *every* MCA-bad slope are exactly the prefix-fiber members; for `gcd(m,n) = 1`
  **all witnesses are aperiodic**.
- **The old aperiodic-band conjecture is false.** A single line carries > 2¹⁶⁴ (KoalaBear) /
  > 2¹⁰² (M31) aperiodically witnessed bad slopes inside the band, and an explicit family carries
  2^Ω(n): no `q`-independent polynomial bound exists below the envelope. The band input must be
  (and now is) **normalized with its left edge at the envelope**. Likewise, all challenge-field
  (`q`-scale) census models are refuted by base-field floors at every balanced profile; the correct
  models are `|B|`-normalized.
- **Slope elimination and lattice reduction.** Per line, the slope quantifier is eliminated
  (each non-common support carries ≤ 1 slope); the census is the split locus of an explicit
  rank-two `F[X]`-lattice; the near-rational stratum is solved exactly; the entire aperiodic input
  reduces to one **split-pencil problem** for determinantal representations of the domain
  polynomial, and prefix-fiber flatness (Q) is its boundary profile.
- **Rigidity.** Identically split kernel sections of exact-agreement pencils are constant and
  tangent-borne (≤ max(γ,1) bad slopes) only at thresholds satisfying `n-a'≤t`; deficiency-one
  charts meet that guard and are eliminant-or-tangent with no residual branch. At arbitrary
  deficiency this is a structural route, not a payment. Prefix fibers are rigid (`|M∖M′| ≥ w+1` per side), giving an unconditional
  worst-case fiber cap (≈ 3.6·10⁵ bits below trivial per deployed row) and an exact second-moment
  ledger whose top stratum is the constant-shift split-pair census.
- **Proved base cases of (Q).** Two-sided fiber flatness (Weil range) at head depths:
  `w ≤ 21–22` (KoalaBear), `w ≤ 10–11` (M31), including all witness lists at those depths.

## 3. Computational status of the above

All "proved" items in 2.1 are theorems whose final step is a finite integer inequality, verified by
exact (arbitrary-precision) arithmetic; they are hand-checkable in principle. Constructive lemmas
were additionally verified by exhaustive small-field enumeration. Bit "margins" quoted anywhere are
floating-point orientation values only and carry no load. Measured collision-hierarchy values
(Γ_r tables) are **calibration evidence only** and enter no proof.

## 4. What remains conjectural

The matching safe-side direction — that nothing beats the identity floor — rests on two named
inputs, now provably reducible to **one problem**:

1. **(Q) prefix-fiber flatness**: max fiber ≤ e^{o(n)} · average, at primitive scales in the band
   (equivalently: equidistribution of prescribed-top-coefficient divisors of `Xⁿ − β`). Proved only
   at head depths; the band depth `w ≈ 6.7·10⁴` corresponds, over **Z**, to divisor equidistribution
   in moduli of size `(#divisors)^{1−o(1)}` — open. Per-term character/monodromy methods provably
   fall ≈ 2.4·10⁷ bits short; joint cancellation across the character-tuple family is required.
2. **Split-pencil census** (final form of the aperiodic input, `|B|`-normalized, interior profiles):
   bounds the balanced two-generator divisor families. Contains (Q) as its boundary stratum.

**Asymptotic prize:** (Q) + split-pencil ⇒ `δ* = 1 − ρ − g* + o(1)`; polynomial losses are
absorbed given an `O(log n)` agreement reserve.

**Finite prize (the four adjacent pairs):** conjectured first safe agreements are exactly one step
past the proved unsafe edges — `(a₀, a₀+1)` = (1116047, 1116048) KB-MCA, (1116046, 1116047)
KB-list, (1116023, 1116024) M31-MCA, (1116022, 1116023) M31-list — with fail margins **22.2, 22.0,
3.3, 3.1 bits**. Deciding these requires exact-constant (not `poly(n)`-loss) forms of the inputs,
plus a per-rung audit of the quotient ledger at `a₀+1` (pending). The Mersenne-31 rows, at ≈ 3
bits, demand exact extremality.

## 5. Falsifiability

A counterexample to the conjectured answer cannot fail silently: it must exhibit either a
super-polynomial **primitive prefix fiber** (refuting (Q), and producing exponentially many
balanced-ternary codewords of the moment kernel), or a super-polynomial **primitive split-pencil
family** (refuting the census). Both objects are explicit and machine-checkable.

---
*One-sentence version: the RS MCA threshold is the entropy–subfield envelope
`1 − ρ − g*(ρ, log₂|B|)`; the failure side is proved to within 10⁻⁶ of it by exact integer
certificates, every route past it is refuted, and the safety side is reduced to a single explicit
divisor-counting conjecture (split-pencil / prefix-fiber flatness), proved at head depths and open
at band depth.*
