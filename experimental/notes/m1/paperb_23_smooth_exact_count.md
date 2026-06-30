# Paper B: the {2,3}-smooth exact canonical slope count A_{2,3}(N',ℓ')

This note supplies and machine-verifies the exact `{2,3}`-smooth canonical slope
count requested as "future combinatorics" in `slackMCA_v4.tex` `rem:23count`,
the mixed-radix analogue of the closed form `thm:exactcount` proves for 2-power
domains. It is a bounded class-enumeration theorem **proved by a structural
reduction and verified by exact enumeration**, conditional on the same import
(`thm:vsimport`) that `thm:23rigidity` is conditional on — no new black box. It
does not touch the open local-limit conjectures.

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

**Entropy exponent (the `β(ρ)` analogue at `ρ=1/2`).** The per-cell alphabet has
exactly `19` types, so the half-rate count saturates as
`A_{2,3}(N', N'/2) = 19^{n_c (1-o(1))} = 2^{(log_2 19 / 6) N' (1-o(1))}`, giving

```text
β_{2,3}(1/2) = (log_2 19)/6 ≈ 0.70798
```

(verified numerically converging: `0.7080` already at `N'=96..768`). Compare the
2-power value `β(1/2)=½ max_θ(𝓗(θ)+θ) ≈ 0.7925`: adjoining the radix-3 scale
*lowers* the half-rate canonical slope-count exponent. General `ρ` is the
saddle-point of the per-cell size generating function.

## Reproducibility

```text
experimental/scripts/verify_paperb_23_smooth_exact_count.py
```

Pure stdlib. Implements (★) as a Boolean-Minkowski transfer and cross-checks it
against two-faithful-prime brute-force enumeration; recovers `thm:exactcount`
at `b=0`; prints the entropy-exponent samples. `--certificate` / `--check` emit
and re-verify a deterministic JSON certificate (`PASS`). Exit code `0` on pass.
