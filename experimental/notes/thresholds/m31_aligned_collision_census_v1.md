---
workboard_item: M1
row: Mersenne-31 list at 2^-100
object: LIST
target_epsilon: 2^-100
agreement: 1116023
B_star: 16777215
direct_statement: "On the pinned c=2048, (u,v)=(0,1) quotient profile rooted at the 479-point band anchor (core31 + T64 blocks {5,7,9,11,13,15,17}), the exhaustive dyadic-fiber-aligned depth-32 collision census over deficiencies e in [34,65] returns exactly 49 collisions at e=64 -- every one a whole-T64-block swap (7 anchor x 7 complement), with no non-block aligned collision -- and 0 collisions at every other reachable aligned deficiency (T16 e=48; T8 e=40,48,56). Aligned deficiencies are necessarily even. The unrestricted rooted census over the same range has enumeration space C(479,e)*C(543,e), from 10^106.2 at e=34 to 10^166.4 at e=65 (total 10^166.5), and is a minimum-weight balanced-codeword question for a structured [1022,>=990] F_p code."
architecture: DIRECT_PINNED_C2048_U0_V1_QUOTIENT_PROFILE
partition_digest: "N/A; fixed local support profile, no row atom banked"
atom_or_cell: Q / fixed-template quotient-prefix census
quantifier: "Exhaustive over all dyadic-fiber-aligned depth-32 exchanges (T16 at e in {48,64}, T8 at e in {40,48,56}) rooted at the fixed 479-point anchor in the punctured 1022-label quotient domain; the even-parity emptiness and the enumeration-space arithmetic hold for every e in [34,65]."
projection_and_unit: "479-subsets per first-32 quotient-locator coefficient target; no received-word, codeword, ray, or slope projection."
claimed_bound: "Aligned census: 49 collisions (all whole-T64-block) at e=64, 0 at e in {40,48,56}, 0 non-block aligned collisions anywhere, none at any odd e. Unrestricted space C(479,e)*C(543,e): 10^106.2 (e=34) to 10^166.4 (e=65), total 10^166.5; single-side enumeration >=10^35.6 years at 10^9/s, meet-in-the-middle 10^62-10^102 storage per side."
status: EXPERIMENTAL
impact: LOCAL_ONLY
falsifier: "A dyadic-fiber-aligned depth-32 collision at any e in {40,48,56}; a non-whole-block aligned collision, or a 50th collision, at e=64; any odd-e aligned exchange; a duplicate, oversize, or punctured support among the 49; or a binomial or base-10 magnitude in the cost table off from an independent recomputation."
replay: "python3 experimental/scripts/verify_m31_aligned_collision_census.py --check (recomputes the cost model, the dyadic 14/6/2 census, the complete T16-aligned e=48 and e=64 census, the 49-block-pair collision property, the power-sum<=>prefix-32 equivalence, and the eta / 49-441-1225 / nu=63 / nu=47 series cross-checks; ~10 s) and --tamper-selftest. No kernel Lean is shipped: the deliverable is a computational census whose two proved sub-facts -- even parity of aligned deficiencies and exact binomial cost arithmetic -- are elementary and are recomputed by the stdlib verifier."
consumers: "M31 list-row census/floor work (the integrated band_mixing / t16_mixing_floor rooted-shell series): this packet supplies the exhaustive aligned-slice census and the quantified infeasibility of the unrestricted census."
risk_limits: "Aligned-slice scope only (dyadic-fiber-aligned exchanges); the unrestricted, non-aligned census over [34,65] remains open; the T8 e=40/48/56 sweeps are recorded long-run results (exact repro commands, runtimes, empty hit logs) and are not re-run by the <1 min --check."
---

# M31 aligned collision census and unrestricted-census infeasibility

## Status

```text
T16-aligned e=64 census      = 49 collisions, all whole-T64-block (7 x 7)
T16-aligned e=64 non-block   = 0
T16-aligned e=48 census      = 0
T8-aligned e=40,48,56 census = 0   (recorded long-run sweeps)
odd-e aligned exchanges      = none (aligned deficiencies are even)  [PROVED]
unrestricted [34,65] space   = 10^106.2 .. 10^166.4, total 10^166.5   [PROVED]
brute force / MITM           = infeasible (>=10^35.6 yr; 10^62-10^102 storage)
min-weight reformulation     = structured [1022,>=990] F_p code
row ledger movement          = 0
```

This packet extends the integrated M31 quotient-floor / rooted-shell census
series with an exhaustive census of the dyadic-fiber-aligned depth-32 collisions
rooted at the fixed band anchor, a proof that aligned deficiencies are even, and
an exact enumeration-cost model that places the unrestricted census out of reach
of both brute force and meet-in-the-middle. It is deliberately support-level: it
works on one pinned quotient profile, at one fixed 479-point anchor, and makes no
received-line, codeword, ray, or slope claim.

Per-claim status: the enumerations are `COMPUTED` (deterministic, replayable);
the even-parity statement is `PROVED` (elementary); the cost model is `PROVED`
(exact integer arithmetic).

The definitions below are all public and integrated. The pinned quotient domain,
the `T64` block structure, the `q_r` labels, and the rooted-shell census are
those of the `m31_quotient_band_mixing` and `m31_quotient_t16_mixing_floor`
packages (`experimental/lean/`, `experimental/notes/thresholds/`) and the
`m31_q_rooted_shell_envelope` shell compiler. The active proof labels are
`def:primitive-q`, `def:q-row-atom`, `prop:q-exact-target`, and
`lem:newton-equivalence` in `experimental/grande_finale.tex`; the depth-32
quotient-jet reduction is Corollary 3.2 of
`m31_c2048_fixed_template_interleaved_quotient_route_cut.md`.

## 1. Pinned quotient domain and band anchor

Put `p = 2^31 - 1 = 2147483647`. In `F_p[i]` use the norm-1, order-`2^31`
generator `g = (1717986917, 1288490189)`, and the quotient labels

```text
q_r = 2^{-2047} * Re(g^{r 2^19})  (mod p),   r odd, 1 <= r <= 2047,
```

with `2^{-2047} = 1073741824 = 2^30 (mod p)`. The `1024` labels are distinct.
The pinned `c=2048`, `(u,v)=(0,1)` profile punctures `q_1` and `q_3`, leaving

```text
Q' = { q_r : r odd, 1 <= r <= 2047, r not in {1,3} },   |Q'| = 1022.
```

For odd `a`, the `T64` block is `C_a = { q_r : r == a or -a (mod 64) }` (`64`
points); the fourteen classes `a in {5,7,...,31}` are intact in `Q'`. Each `C_a`
is a disjoint union of four intact `T16` classes `D_b = { q_r : r == b or -b
(mod 256) }` (`16` points each). The **band anchor** is

```text
A = core31  U  U_{a in {5,7,9,11,13,15,17}} C_a,   |A| = 31 + 7*64 = 479,
```

where `core31` is the `31`-point punctured-`C_1` core

```text
63, 65, 127, 129, 191, 193, 255, 257, 319, 321, 383, 385, 447, 449, 511, 513,
575, 577, 639, 641, 703, 705, 767, 769, 831, 833, 895, 897, 959, 961, 1023.
```

Its complement `Q' \ A` has `543` points. Among the `62` intact `T16` classes,
`28` lie inside `A` (the four subclasses of each of the seven anchor blocks),
`31` lie in the complement, and `3` straddle `A` (subclasses of the punctured
`C_1`).

## 2. Depth-32 collisions and the aligned slice

For a `479`-subset `E` write `V_E(Y) = prod_{q in E}(Y - q)` and
`pref_32(V_E)` for its top `32` nonleading coefficients. Two supports `A, B`
form a **depth-32 collision** when `pref_32(V_A) = pref_32(V_B)`. Writing
`X = A \ B`, `Y = B \ A` (so `|X| = |Y| = e`, the **deficiency**), the collision
depends only on `(X, Y)` and

```text
pref_32(V_A) = pref_32(V_B)   <=>   sum_{q in X} q^k = sum_{q in Y} q^k
                                    for k = 1, ..., 32,
```

i.e. the first `32` power sums of `X` and `Y` agree. The **dyadic-fiber-aligned**
slice restricts `X, Y` to disjoint unions of intact dyadic fibers (at scale
`T64`, `T32`, `T16`, `T8`, ...). Because `e <= 65` allows at most four `T16`
fibers per side, a-subset enumeration over the aligned classes is exhaustive:
this is the entire subspace in which the Chebyshev block-flatness mechanism can
produce a collision.

## 3. Aligned deficiencies are even  [PROVED]

> Every dyadic fiber `T_d` has even size `d in {2,4,8,16,32,64}`, the smallest
> being `T_2` with two points. A dyadic-fiber-aligned `X` is a disjoint union of
> whole fibers, so `e = |X|` is a sum of even sizes and is even. Hence no aligned
> exchange exists at odd deficiency; in particular every odd `e in [34,65]` has
> no aligned collision at all.

Consequently, over `[34,65]` the reachable aligned deficiencies are exactly the
even multiples supplied by the coarse fibers: `T16` gives `e in {48,64}`
(`a = 3, 4` classes per side); `T8` gives `e in {40,48,56}` (`a = 5,6,7`). Every
odd `e` is empty by the parity fact above; every even `e` not divisible by `8`
is aligned only through `T4` or `T2` fibers, which need `>= 9` up to `32` atoms
per side and are otherwise non-aligned. The `T16` and `T8` slices below therefore
cover every fiber-aligned collision that is feasible to enumerate in-range.

## 4. Exhaustive aligned census  [COMPUTED]

All counts are exact and deterministic. The `T16` slices are recomputed in full
by the verifier's `--check`; the `T8` slices are recorded long-run results (see
the reproduction block).

| scale | e | atoms/side | search space | collisions | classification |
|:---|---:|---:|:---|---:|:---|
| T16 | 64 | 4 | `C(28,4) x C(31,4)` | **49** | all whole-`T64`-block swaps (7 x 7); 0 non-block |
| T16 | 48 | 3 | `C(28,3) x C(31,3)` | 0 | -- |
| T8  | 40 | 5 | `C(56,5) x C(63,5)` | 0 | -- |
| T8  | 48 | 6 | `C(56,6) x C(63,6)` | 0 | -- |
| T8  | 56 | 7 | `C(56,7) x C(63,7)` | 0 | -- |

At `e = 64` the census is complete over all `C(28,4) x C(31,4)` pairs of
four-class `T16` selections. Every one of the `49` collisions is a whole-`T64`
block swap: one intact anchor block `C_a` (`a in {5,7,9,11,13,15,17}`) exchanged
for one intact complement block `C_b` (`b in {19,21,23,25,27,29,31}`), giving
`7 x 7 = 49`. **No non-block `T16`-aligned collision exists.** This strictly
extends the pre-built `49`-family of the integrated series: the family is now
known to be the entire `T16`-aligned `e=64` collision set, not merely a certified
subset. Because each block-swap side is a single intact `T64` fiber, the `49`
collisions are exactly the single-block dyadic-fiber exchanges at `e=64`.

The `49` are also verified directly, outside the hash-join census: for every one
of the `7 x 7` anchor/complement block pairs `(C_a, C_b)`, the first `32` power
sums of `C_a` and `C_b` coincide (`--check` asserts all `49`).

### Recorded long-run reproduction (T8 sweeps)

The `T8` sweeps are exhaustive `C(56,a) x C(63,a)` fingerprint censuses run by
the C fast path; an empty stdout hit log certifies zero collisions.

```text
python3 experimental/scripts/gen_atoms.py 8 atoms_d8.bin
cc -O3 -o census_atoms experimental/scripts/census_atoms.c
./census_atoms atoms_d8.bin 5 > hits_d8_a5.txt   # e=40   1.22 s     0 hits
./census_atoms atoms_d8.bin 6 > hits_d8_a6.txt   # e=48  12.56 s     0 hits
./census_atoms atoms_d8.bin 7 > hits_d8_a7.txt   # e=56 835.79 s     0 hits (~8.6 GB)
```

The `e=56` sweep is the long pole: `231,917,400` anchor `7`-subsets hashed and
`553,270,671` complement `7`-subsets streamed, `0` fingerprint hits. These
long-run results are recorded, not re-run by the sub-minute verifier; `--check`
instead recomputes the entire `T16` slice and carries the recorded `T8` EMPTY
outcomes in the certificate.

## 5. Unrestricted enumeration-cost model  [PROVED]

Dropping the aligned restriction, the rooted census at deficiency `e` compares
`C(479,e)` anchor-side `e`-subsets against `C(543,e)` complement-side `e`-subsets.
The enumeration space is `C(479,e) * C(543,e)`, computed by exact big-integer
binomials (representative rows; the verifier tabulates all of `34 <= e <= 65`):

| e | `C(479,e)` | `C(543,e)` | ordered pairs | MITM storage/side |
|---:|---:|---:|---:|---:|
| 34 | `10^52.1` | `10^54.1` | `10^106.2` | `10^62.7` |
| 40 | `10^58.6` | `10^60.8` | `10^119.4` | `10^71.2` |
| 48 | `10^66.5` | `10^69.2` | `10^135.8` | `10^81.9` |
| 56 | `10^73.8` | `10^77.0` | `10^150.8` | `10^92.0` |
| 64 | `10^80.5` | `10^84.2` | `10^164.8` | `10^101.6` |
| 65 | `10^81.3` | `10^85.1` | `10^166.4` | `10^101.6` |

Summed over `[34,65]` the ordered-pair count is `10^166.5`. Even enumerating a
single side at the smallest deficiency is out of reach: `C(479,34) = 10^52.1`, so
at an optimistic `10^9` subset-operations per second the single-side pass alone
takes `10^35.6` years. Meet-in-the-middle needs between `10^62.7` (`e=34`) and
`10^101.6` (`e=64,65`) entries of storage per side, i.e. `10^62` to `10^102`.

## 6. Routes killed

The two direct enumeration attacks on the unrestricted `[34,65]` census are both
infeasible, with the numbers above:

- **Brute-force pair enumeration** would scan up to `10^166.4` ordered `(X,Y)`
  pairs at a single deficiency and `10^166.5` in total. Even the reduced form
  that hashes one side and streams the other must first enumerate that side, and
  the smallest such single-side pass, `C(479,34) = 10^52.1`, already costs
  `10^35.6` years at `10^9`/s.
- **Meet-in-the-middle** splitting each side in half needs `10^62` to `10^102`
  stored half-subset fingerprints per side, exceeding any realizable storage.

Neither is a compiler route cut on the M31 LIST residual; they record that the
unrestricted census cannot be closed by direct enumeration, so any resolution
off the aligned slice must be structural.

## 7. Minimum-weight-codeword reformulation

A depth-32 collision is a nonzero balanced `+/-1` vector in the kernel over `F_p`
of the `32 x 1022` power-sum matrix `V = [q_r^k]_{k=1..32, r in D}`: setting
`z_r = +1` on `X`, `-1` on `Y`, `0` elsewhere gives `sum_r z_r q_r^k = 0` for
`k = 1,...,32`. That kernel is a length-`1022` `F_p` code of dimension at least
`1022 - 32 = 990`, so the minimum unrestricted deficiency is the minimum-weight
balanced codeword of a structured `[1022, >=990]` `F_p` code. This is stated only
as a reformulation of the census question; no hardness is claimed.

## 8. Sanity gate

Before the census was trusted, the domain engine was cross-checked against the
integrated series along independent locator-polynomial and power-sum paths; the
verifier's `--check` recomputes each:

- the quotient labels agree between direct exponentiation and the order-`1024`
  recurrence, and their SHA-256 matches the integrated `band_mixing` digest;
- the intact dyadic-fiber census is `14 / 6 / 2` at `T64 / T128 / T256`;
- the certified `32`-coefficient depth-32 target `eta` of the `t16_mixing_floor`
  anchor is reproduced;
- the rooted-shell family counts are `49 / 441 / 1225` at `e = 64 / 128 / 192`
  (closed form `C(7,t)^2` and direct enumeration agree);
- all `1225` triple-`T64` swaps agree through coefficient `63` and break at `64`;
- the `e=96` `T16` mixing witness shares exactly `47` nonleading coefficients;
- the `power sums agree  <=>  prefix-32 agree` equivalence holds on both
  colliding and non-colliding `479`-support witnesses; and
- the C fingerprint enumerator and the Python census agree at `d=16, a=4` (`49`).

## 9. Validation and replay

```text
python3 experimental/scripts/verify_m31_aligned_collision_census.py --check
python3 experimental/scripts/verify_m31_aligned_collision_census.py --tamper-selftest
python3 experimental/scripts/verify_m31_aligned_collision_census.py --write   # regenerate certificate
```

`--check` is deterministic, stdlib-only, and runs in about ten seconds. The
enumerator sources are shipped for the long-run reproduction:
`experimental/scripts/census_aligned.py` (standalone `T16` census),
`experimental/scripts/gen_atoms.py` and `experimental/scripts/census_atoms.c`
(the `T8`/`T16` fast path). The canonical certificate is

```text
experimental/data/certificates/m31-aligned-collision-census-v1/results_census.json
```

No kernel Lean is shipped. The deliverable is a computational census; its only
proved sub-facts are the even parity of aligned deficiencies (Section 3) and the
exact binomial cost arithmetic (Section 5), both elementary and recomputed by the
verifier. Following the standing formal-statement policy, a statement-only Lean
stub is not shipped.

## 10. Nonclaims

- No uniform band upper bound, and no statement about any non-aligned exchange,
  is proved; only the dyadic-fiber-aligned slice is exhaustive.
- The unrestricted `[34,65]` census is not resolved; the cost model bounds the
  cost of the direct-enumeration routes, not the answer.
- The `T8` `e in {40,48,56}` sweeps are recorded long-run results, not re-verified
  by `--check`.
- No received word, first-match survivor, codeword, ray, or slope is constructed;
  no row-global atom, adjacent-row closure, or endpoint movement is claimed.
- Nothing extrapolates beyond the pinned `(u,v)=(0,1)` profile and the stated
  `479`-point anchor.

# EXPERIMENTAL
