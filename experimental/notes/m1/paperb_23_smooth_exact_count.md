# Paper B: the {2,3}-smooth exact canonical slope count A_{2,3}(N',ℓ')

This note supplies and machine-verifies the exact `{2,3}`-smooth canonical slope
count requested as "future combinatorics" in `slackMCA_v4.tex` `rem:23count`,
the mixed-radix analogue of the closed form `thm:exactcount` proves for 2-power
domains. It is a bounded class-enumeration theorem **proved by a structural
reduction and verified by exact enumeration**, conditional on the same import
(`thm:vsimport`) that `thm:23rigidity` is conditional on — no new black box. It
does not touch the open local-limit conjectures. As a corollary of the count it
also gives the **closed-form growth exponent `β_{2,3}(ρ)` for every rate `ρ`** (a
max-entropy saddle point), strictly below the 2-power exponent at all prize rates.

## Claim

Let `N'=2^a 3^b` with `a>=1`, write `n_c = 2^{a-1} 3^{max(b-1,0)}`, and let

```text
A_{2,3}(N',ℓ') = #{ distinct e_1(B) = sum_{β in B} β  :  B ⊆ μ_{N'}, |B| = ℓ' }
```

be the number of distinct characteristic-zero canonical slopes `-e_1(B)` at
agreement size `ℓ'` (the quantity `thm:exactcount` computes for `b=0`). Then

```text
A_{2,3}(N',ℓ')  =  #{ cell-type vectors (d_1,...,d_{n_c}) ∈ T^{n_c}
                      :  ℓ'  ∈  Sizes(d_1) ⊕ ... ⊕ Sizes(d_{n_c}) },     (★)
```

a Minkowski-reachability count over `n_c` independent **cells**, where `T` is a
fixed per-cell alphabet of difference-types and `Sizes(d) ⊆ {0,...,6}` is the set
of cell sizes realizing type `d`. For `b>=1` the alphabet has **19 types in four
size-classes**:

```text
6 types with Sizes = {3};          6 types with Sizes = {2,4};
6 types with Sizes = {1,2,3,4,5};  1 type  with Sizes = {0,2,3,4,6}.
```

For `b=0` the cell is a bare antipodal pair with three types
(`{+1},{-1}` of `Sizes={1}` and `{0}` of `Sizes={0,2}`), and (★) collapses to

```text
A_{2,3}(2^a,ℓ') = A(2^a,ℓ') = Σ_{u≥0, t=ℓ'-2u≥0, u≤n_1-t} binom(n_1,t) 2^t,
```

`n_1=2^{a-1}` — exactly `thm:exactcount`. Thus (★) is a single closed form
unifying `b=0` (proved in Paper B) and the open `b>=1` mixed-radix case.

## Status

**CONDITIONAL** (per agents.md rule 4: the proof depends on the imported
vanishing-sum theorem `thm:vsimport`), in exactly the form `thm:23rigidity`
already uses it — no new import; Paper B labels that parent theorem "conditional
on the import" for the same reason. The structural identity (★) is proved in full
generality below (all `a>=1`, `b>=0`) *modulo that single import*; it is **not**
inferred from the small cases. Separately, an **AUDIT** cross-check in the
verifier certifies (★) against independent two-faithful-prime brute-force
enumeration on every `{2,3}`-smooth domain up to `N'=48` (so the finite values
are unconditional), and certifies the `b=0` collapse to `thm:exactcount`.
A deterministic JSON certificate is attached.

## Parameters

Object: the **support-wise MCA canonical-line** bad-slope set (the `thm:exactcount`
object — `thm:stable`(i): the bad slopes of `x^{k+σ}+z x^k` are exactly
`{∓e_1(B)}`), at the quotient level. Mapping to the deployed parameters: for
`RS[F_q, D, k]` on a `{2,3}`-smooth domain `D` of order `n`, quotient order
`N'=n/σ`, agreement size `ℓ'=ρN'+1` (`ρ=k/n`); `N'=2^a 3^b`,
`n_c=2^{a-1}3^{b-1}` cells. The count is a `q`-independent **characteristic-zero**
invariant — `q_gen` is the `N'`-th cyclotomic field of definition; the
finite-field/density (norm-sieve) transfer is per-class and unchanged
(`rem:23count`). `q_line`/`q_chal`/`B`/`F` extension ledgers are **not** touched;
this is the characteristic-zero MCA class count the sieve runs over, kept strictly
separate (rule 3) from list, CA, and line-decoding objects and from the field
transfer (rule 2).

## Existing paper dependency

- `slackMCA_v4.tex` `thm:exactcount` — the `b=0` closed form (recovered here).
- `slackMCA_v4.tex` `rem:23count` — the open target ("exact class enumeration
  and the two-parameter analogue of `β(ρ)` … left as future combinatorics").
- `slackMCA_v4.tex` `thm:23rigidity`, `thm:vsimport` — the relation module
  (rotated pairs + triangles) this count is the enumeration of; the only import.

## Proof idea

`μ_{N'} = μ_{2^a} × μ_{3^b}` (coprime parts). By `thm:23rigidity` (conditional
on `thm:vsimport`), `e_1(S)=e_1(T)` iff `S ⊔ (-T)` is an `ℕ`-combination of
rotated **pairs** `{ζ,-ζ}` (acting only on the 2-part) and, when `b>=1`,
**triangles** `{ζ,ζω,ζω²}` (acting only on the 3-part). Hence the relations
factor through `n_c` independent **cells**, each a `2×3` block

```text
{±ζ_i} × {y_j, y_j ω, y_j ω²}      (one antipodal 2-part pair × one μ_3-coset),
```

and a bare antipodal pair when `b=0`. *Cells span a `ℤ`-basis.* The `2^{a-1}`
antipodal-pair representatives `{ζ_i}` are a `ℤ`-basis of `ℤ[ζ_{2^a}]`. On the
3-part, the `3^{b-1}` `μ_3`-cosets partition `μ_{3^b}`; by `thm:vsimport`(i) for
`n=3^b` the coset (triangle) relations `y(1+ω+ω²)=0` generate the entire kernel of
`Σ: ℤ^{3^b}→ℤ[ζ_{3^b}]`, so any coset transversal — take `{y_j, y_j ω}` per coset
`j` — is a `ℤ`-basis of `ℤ[ζ_{3^b}]` (rank `2·3^{b-1}=φ(3^b)`). Since
`ℤ[ζ_{N'}]=ℤ[ζ_{2^a}]⊗ℤ[ζ_{3^b}]`, the tensor `{ζ_i y_j, ζ_i y_j ω}` is a
`ℤ`-basis, and a subset's `e_1` is the sum of independent per-cell contributions,
one block per `(i,j)`. The contribution of cell `(i,j)` is its **difference type**

```text
d = ( c^{(1)} - c^{(ω²)},  c^{(ω)} - c^{(ω²)} ),   c^{(y)} ∈ {-1,0,1},
```

the signed occupancy of its three columns (`c^{(y)}=±1` for a single `±` element
of the pair in column `y`, `0` for empty-or-both; `y∈{y_j,y_jω,y_jω²}`). Because
the cells occupy disjoint basis blocks, **distinct `e_1` ⟺ distinct cell-type
vector**, and the cells are independent. Enumerating the `4^3` column occupancies
of one cell gives the alphabet `T` and `Sizes(d)`; a type-vector is realizable at
total size `ℓ'` iff `ℓ' ∈ ⊕_c Sizes(d_c)`. This is (★), in full generality. The
`4^3` table yields the stated four size-classes. ∎

## Ledger impact

Fixes the **characteristic-zero MCA canonical-line bad-slope class count** for
`{2,3}`-smooth (mixed-radix FFT) domains, the missing combinatorial input of
`rem:23count`. The two-scale reserve and the norm sieve are unchanged; this only
pins the class enumeration the sieve runs over (it does not by itself give a
deployed every-prime MCA bound — the per-class finite-field transfer is still
required). No entropy/quotient/interleaved-list/line-decoding/field-transfer
ledger is mixed.

The closed-form exponent `β_{2,3}(ρ)` below sharpens this into a quantitative
**rate-vs-radix comparison**: the canonical bad-slope count grows like
`2^{β_{2,3}(ρ)·N'(1+o(1))}`, strictly below the 2-power exponent `β_2(ρ)` at every
prize rate. Against the `1/q_gen` denominator of the `conj:B` reserve shape this
is the size of the per-class characteristic-zero sum the norm sieve must clear, so
a smaller exponent is a (modest) easing of the canonical-line half of the budget —
not a deployed bound, but the exact constant `rem:23count` left open.

## Constants

Verified exactly (structural = brute) for `N' ∈ {6,12,18,24,36,48}`, all `ℓ'`:

```text
N'=6  (2^1 3^1): A = 6, 13, 13
N'=12 (2^2 3^1): A = 12, 61, 133, 241, 289, 289
N'=18 (2^1 3^2): A = 18, 145, 577, 1549, 2971, 4483, 5671, 5995, 5995
N'=24 (2^3 3^1): A = 24, 265, 1561, 6097, 16705, 35713, 60985, 86689,
                     106993, 117793, 119953, 119953
N'=36 (2^2 3^2): A = 36, 613, 6013, 40033, 190945, 695521, 2008477, 4762153
```

## Entropy exponent `β_{2,3}(ρ)` for general `ρ`

Define `β_{2,3}(ρ) = lim_{N'→∞} (1/N') log_2 A_{2,3}(N', ρN')`, the exponential
growth rate of the characteristic-zero canonical bad-slope count. We give it in
closed form for every `ρ`. There are `n_c = N'/6` cells; each cell draws one of
the `19` types, contributing a size in `[min Sizes(d), max Sizes(d)]`. The
per-cell **min/max multisets** read off the four size-classes are

```text
min over the 19 types:  {0:×1, 1:×6, 2:×6, 3:×6}
max over the 19 types:  {6:×1, 5:×6, 4:×6, 3:×6}   (= 6 − min, so β(ρ)=β(1−ρ))
```

**Interval reduction (proof to exponential order).** A type-vector counts at `ℓ'`
iff `ℓ' ∈ ⊕_c Sizes(d_c)`. Every step-1 type `{1,2,3,4,5}` is a length-5 run, and
each `Sizes(d)` has internal gaps `≤ 2`; so a Minkowski sum containing **one**
such cell is the full interval `[Σ_c min_c, Σ_c max_c]`. The saddle distribution
below puts positive density on the six `{1,2,3,4,5}` types, hence a `1−o(1)`
fraction of the dominant vectors are gap-free and

```text
ℓ' ∈ ⊕_c Sizes(d_c)   ⇔   Σ_c min_c ≤ ℓ' ≤ Σ_c max_c        (to exp. order).
```

(Verified: `struct/band → 1`, ratio `1.000000` already at `N'=192`.) By Cramér /
the method of types this **interval count** has the rate function

```text
β_{2,3}(ρ) = (1/(6 ln2)) · max{ H(p) : p ∈ Δ_19,
                                 Σ_i p_i min_i ≤ 6ρ ≤ Σ_i p_i max_i }.
```

The uniform `p≡1/19` gives `Σp·min = 36/19`, `Σp·max = 78/19`, feasible exactly
when `6ρ ∈ [36/19, 78/19]`, i.e. a **flat plateau**

```text
β_{2,3}(ρ) = (log_2 19)/6 ≈ 0.707983      for  ρ ∈ [6/19, 13/19] ≈ [0.3158, 0.6842].
```

Off the plateau a single constraint binds and the optimiser is the **tilted
(Gibbs)** law `p_i ∝ exp(−λ·min_i)`. With `x = e^{−λ} ∈ (0,1)` the unique root of
`x(1+2x+3x²) = ρ·(1+6x+6x²+6x³)` (for `ρ < 6/19`; reflect by `β(ρ)=β(1−ρ)` for
`ρ > 13/19`),

```text
β_{2,3}(ρ) = [ log_2(1 + 6x + 6x² + 6x³) − 6ρ·log_2 x ] / 6.
```

**Values at the prize rates** (with the 2-power baseline `β_2(ρ)`, obtained from
the same saddle on the `b=0` alphabet `min{0,1,1}`, `max{2,1,1}`, `cell=2`):

```text
ρ       β_{2,3}(ρ)   β_2(ρ)      radix-3 drop
1/2     0.707983     0.792481     0.0845      (β_2(1/2)=log_2 3 /2, Paper B value)
1/4     0.685747     0.750000     0.0643
1/8     0.509338     0.530639     0.0213
1/16    0.328649     0.334282     0.0056
```

So **adjoining the radix-3 scale strictly lowers the canonical slope-count
exponent at every prize rate**, the gap shrinking to `0` as `ρ→0`. The plateau
also widens vs. the 2-power case (`[1/3,2/3] → [6/19,13/19]`).

The saddle values are matched by the **exact** transfer: the (gap-free) interval
count's exponent climbs monotonically toward each `β_{2,3}(ρ)` from below, with
the finite-size gap halving per doubling of `N'` (a `Θ(1/N')` correction, so
Richardson-extrapolation lands on the saddle):

```text
ρ=1/8:  N'=96→0.4829, 192→0.4936, 384→0.5002, 768→0.5041, … → 0.50934
ρ=1/16: N'=96→0.3041, 192→0.3138, 384→0.3200, 768→0.3237, … → 0.32865
```

## Reproducibility

```text
experimental/scripts/verify_paperb_23_smooth_exact_count.py
```

Pure stdlib. Implements (★) as a Boolean-Minkowski transfer and cross-checks it
against two-faithful-prime brute-force enumeration; recovers `thm:exactcount`
at `b=0`. The entropy-exponent block computes `β_{2,3}(ρ)` from the saddle point
(`saddle_beta`), checks the plateau value and the 2-power baseline
`β_2(1/2)=log_2 3 /2` exactly, confirms `β_2(ρ) ≥ β_{2,3}(ρ)` at every prize
rate, and certifies convergence of the exact interval count (`band_count`) up to
the saddle plus `struct/band → 1`. `--certificate` / `--check` emit and re-verify
a deterministic JSON certificate (`PASS`). Exit code `0` on pass.
