---
workboard_item: M1
row: Mersenne-31 list at 2^-100
object: LIST
target_epsilon: 2^-100
agreement: 1116023
B_star: 16777215
direct_statement: "On the pinned c=2048, (u,v)=(0,1) quotient profile there is an explicit depth-32 locator-prefix target and an explicit canonical 479-support anchor A in its fiber with d_192(A) >= 1237, consisting of 1225 whole-T_64 triple exchanges together with 12 complete-T_16 mixed supports. Since 192 lies in the band 33..213, the uniform in-band cap d_e(A) <= 1233 is false."
architecture: DIRECT_PINNED_C2048_U0_V1_QUOTIENT_PROFILE
partition_digest: "N/A; support-level pinned quotient profile, no first-match ledger atom assigned"
atom_or_cell: Q / PINNED_QUOTIENT_PREFIX_FIBER / ROOTED_SHELL
quantifier: "Existential: one target eta in F_p^32, one canonical 479-support anchor A of the punctured 1022-label quotient domain with pref_32(V_A)=eta, and 1237 pairwise-distinct same-target supports at rooted deficiency exactly 192."
projection_and_unit: "Rooted count of canonical 479-subsets sharing the same 32 quotient-locator coefficients; no received-word, codeword, ray, slope, or first-match projection."
claimed_bound: "d_192(A) >= 1237, so the uniform in-band intercept 1233 is refuted and any coefficient-four scalar intercept must satisfy b >= 1237. At b = 1237 the compiler gives 1 + 1237*447 + 14456476 = 15009416 <= 16777215, reserve 1767799; the previously certified failing intercept 5192 is unchanged, so the coefficient-four route is recalibrated and not killed. That total is compiler arithmetic under an intercept applied uniformly to all 447 admissible shells, while the refuted cap and any replacement are statements about the 181 shells in 33..213 alone; no uniform cap over the remaining 266 shells is established here or elsewhere, so the displayed reserve is not a banked total."
status: COUNTEREXAMPLE
impact: LOCAL_ONLY
falsifier: "Any of the 1237 supports leaving Q', having size other than 479, duplicating another, sitting at a deficiency other than 192, or disagreeing with the anchor in any of the first 32 monic locator coefficients; or an arithmetic mismatch in 1225 + 12 = 1237 or in the displayed compiler totals."
replay: "cd experimental/lean/m31_flatness_champion_refutation && lake clean && lake build; stdlib-only Lean package, no script is shipped, and every theorem carries a #print axioms census in M31FlatnessChampionRefutation/Refutation.lean. Heavy enumeration is reported as in-note recorded values with their exact parameters."
---

# M31 depth-32 shell counterexample: the uniform in-band cap 1233 is false

## 0. Verdict

```text
REFUTED                   = uniform in-band cap d_e(A) <= 1233 on 33 <= e <= 213
WITNESS                   = d_192(A) >= 1237 at one explicit target and anchor
PACKET                    = 1225 whole-T_64 triple exchanges + 12 complete-T_16 mixed supports
EXCESS OVER THE OLD CAP   = 4
NEW FORCED INTERCEPT      = b >= 1237
RECALIBRATED TOTAL        = 1 + 1237*447 + 14456476 = 15007628 + 1788 = 15009416
RECALIBRATED RESERVE      = 16777215 - 15009416 = 1767799
ROUTE-KILL THRESHOLD      = unchanged at 5192
ROW LEDGER MOVEMENT       = 0
```

The coefficient-four scalar route is **recalibrated, not killed**: the forced intercept rises from
`1233` to `1237`, and both remain far below the certified failing intercept `5192`.

## 1. Frozen object

The row is the Mersenne-31 list stress row over `F_(p^4)` at target `2^-100`, agreement
`1,116,023`, budget `B* = 16,777,215`, with

```text
p = 2^31 - 1 = 2147483647.
```

With the integrated norm-one generator `g = (1717986917, 1288490189)` the pinned quotient labels are

```text
q_r = 2^(-2047) * Re(g^(r * 2^19)) mod p,     r odd, 1 <= r <= 2047,
```

and the labels represented by `r = 1` and `r = 3` are deleted, leaving the punctured domain `Q'`
with `|Q'| = 1022`. For a canonical support `E` of size `479`, `V_E(Y) = prod_{q in E} (Y - q)` and
`pref_32(V_E)` is its first `32` nonleading monic coefficients. For a target `eta`,
`F_eta = { E : pref_32(V_E) = eta }`; for `A, B` in `F_eta`, `delta(A,B) = 479 - |A cap B|`, and
`d_e(A)` counts the `B != A` in `F_eta` at `delta(A,B) = e`. Newton rigidity gives `d_e(A) = 0` for
`1 <= e <= 32`, leaving `447 = 479 - 32` admissible deficiencies.

### 1.1 Class-indexing convention, stated because it is easy to get wrong

Throughout, a **`T_16` class** is a fiber of the map `q -> T_16(2q)`: the 1,024 labels split into
`64` classes of exactly `16`, and a class is named by the **smallest `r`-representative** it
contains. Class `3` is therefore

```text
r in {3, 253, 259, 509, 515, 765, 771, 1021, 1027, 1277, 1283, 1533, 1539, 1789, 1795, 2045},
```

which is **not** the residue class of `3` modulo `128`. A support in this note is a union of `29`
whole `T_16` classes together with the `15` labels of class `3` that survive the puncture of `r = 3`,
giving `29*16 + 15 = 479`. Reading the classes as residues modulo `128` reproduces this particular
anchor's label set by a coincidence of unions while disagreeing with it on every individual class,
and then fails on the mixed supports; the fiber convention above is the correct one.

## 2. The counterexample

The anchor `A` is the union of the `29` whole `T_16` classes

```text
5, 7, 9, 11, 13, 17, 19, 45, 47, 51, 53, 55, 57, 59, 69, 71, 73, 75, 77, 81, 83,
109, 111, 115, 117, 119, 121, 123, 125
```

together with the `15` surviving labels of class `3`, and `eta = pref_32(V_A)`. Two disjoint
families of same-target supports sit at deficiency `192`:

```text
1225 = 35^2   whole-T_64 triple exchanges     (three complete T_64 classes swapped each side)
  12          complete-T_16 mixed supports    (declared b in {2,4} same-core sector)
-----
1237          pairwise-distinct supports at delta(A,B) = 192, all with pref_32 = eta
```

Since `33 <= 192 <= 213`, the uniform in-band cap `1233` is false, with exact excess `4`.

### 2.1 The twelve mixed supports, printed

Each mixed support is obtained from `A` by exchanging twelve whole `T_16` classes for twelve others,
in the class naming of §1.1; the core stays fixed. Removing the listed classes from `A`'s twenty-nine
and adding the listed replacements gives a support of size `479` inside `Q'` at deficiency exactly
`192` from `A`, with the same `pref_32`.

| # | classes removed from `A` | classes added |
|---:|---|---|
| 1 | 5, 13, 19, 45, 47, 69, 73, 75, 77, 111, 117, 119 | 29, 35, 37, 39, 41, 85, 95, 97, 101, 103, 105, 107 |
| 2 | 9, 11, 17, 51, 53, 55, 59, 81, 83, 109, 115, 123 | 21, 23, 25, 27, 31, 33, 43, 87, 89, 91, 93, 99 |
| 3 | 7, 59, 71, 75, 77, 81, 83, 109, 111, 115, 117, 123 | 21, 25, 39, 43, 79, 85, 91, 93, 99, 101, 107, 113 |
| 4 | 5, 11, 13, 17, 19, 45, 47, 51, 53, 57, 69, 121 | 15, 21, 27, 29, 35, 37, 43, 49, 85, 89, 103, 107 |
| 5 | 7, 59, 71, 75, 77, 81, 83, 109, 111, 115, 117, 123 | 23, 25, 39, 41, 79, 87, 91, 93, 99, 101, 105, 113 |
| 6 | 5, 11, 13, 17, 19, 45, 47, 51, 53, 57, 69, 121 | 15, 23, 27, 29, 35, 37, 41, 49, 87, 89, 103, 105 |
| 7 | 7, 59, 71, 75, 77, 81, 83, 109, 111, 115, 117, 123 | 25, 31, 33, 39, 79, 91, 93, 95, 97, 99, 101, 113 |
| 8 | 5, 11, 13, 17, 19, 45, 47, 51, 53, 57, 69, 121 | 15, 27, 29, 31, 33, 35, 37, 49, 89, 95, 97, 103 |
| 9 | 5, 11, 17, 45, 51, 57, 69, 75, 81, 109, 115, 121 | 15, 23, 33, 39, 41, 49, 65, 79, 97, 103, 113, 127 |
| 10 | 5, 11, 17, 45, 51, 57, 69, 75, 81, 109, 115, 121 | 21, 23, 33, 39, 41, 43, 65, 85, 97, 103, 107, 127 |
| 11 | 5, 11, 17, 45, 51, 57, 69, 75, 81, 109, 115, 121 | 23, 27, 33, 37, 39, 41, 65, 91, 97, 101, 103, 127 |
| 12 | 5, 11, 17, 45, 51, 57, 69, 75, 81, 109, 115, 121 | 23, 29, 33, 35, 39, 41, 65, 93, 97, 99, 103, 127 |

The twelve are pairwise distinct and none equals `A`, so with the `1,225` whole-`T_64` exchanges —
which are disjoint from them, being unions of whole `T_64` classes — the shell contains at least
`1,237` supports. Together with §1.1 this makes the whole packet reconstructible from this note
alone, and the falsifier above directly exercisable on every one of the `1,237`.

The whole-`T_64` family is the classical one: a `479`-support contains at most seven whole `T_64`
classes, `479 = 7*64 + 31`, and exchanging `k` of the seven for `k` of the seven complementary
intact classes preserves `pref_32` because the class polynomials differ by a constant, giving
`C(7,k)^2` supports at deficiency `64k` and `C(7,3)^2 = 1225` at `k = 3`. The `12` further supports
are not unions of whole `T_64` classes.

## 3. Census, and a corrected summary value

The declared same-core mixed sector contains exactly `26` selectors: `12` at deficiency `192` from
this anchor and `14` at deficiency `256`. Over all `3,432` whole-`T_64` anchors the incidence of the
`192` sector is distributed as

```text
incidence : 0    2    3   4    5    6    8    9   10   11   12
anchors   : 406  492  312  82  332  522  460  304  86  312  124      total 3432
```

so the maximum incidence over that anchor family is **`12`**, attained by `124` anchors, and the
counts sum to `3,432 = C(14,7)`, the full whole-`T_64` family. The corresponding deficiency-`256`
distribution has maximum `18`, giving a second anchor with `d_256(A') >= 1225 + 18 = 1243`.

**Provenance.** The source enumeration certificate for this census initially carried a summary field
recording the maximum `192` incidence as `8` — the value from the earlier, smaller mixed packet —
while its own incidence distribution and its own replay output both gave `12`. The certificate was
corrected at source to `12`; the distribution above is printed in full so that the summary value is
redundant rather than load-bearing.

## 4. Compiler recalibration

The integrated rooted-shell compiler sums `447` admissible deficiencies against the exact ambient
term `floor(4M/Q) = 14,456,476`, `M = C(1022,479)`, `Q = p^32`. Substituting the forced intercept:

```text
b = 1233 (refuted):  1 + 1233*447 + 14456476 = 15007628
b = 1237 (forced) :  1 + 1237*447 + 14456476 = 15009416 <= 16777215,  reserve 1767799
b = 5191          :  1 + 5191*447 + 14456476 = 16776854 <= 16777215
b = 5192          :  1 + 5192*447 + 14456476 = 16777301 >  16777215
```

The refutation therefore costs `1,788` of reserve and leaves the coefficient-four scalar route
arithmetically viable for `1237 <= b <= 5191`.

## 5. Routes killed

- **The uniform in-band cap `1233`.** Killed by the displayed `1,237`-support packet at deficiency
  `192`, excess `4`.
- **"The previously saturated anchor captures the worst mixed target."** Killed: this target is
  puncture-centred and its mixed incidence is `12`, above the `8` of the earlier seed.
- **"Complete-block closure of the earlier mixed seed is a universal mixed-sector closure."** Killed
  as a universal statement: that closure remains correct for its own declared seed, and is not
  exhaustive over the sector enumerated here. Nothing in it is retracted.
- **"A different whole-`T_64` anchor yields a larger in-band excess in this sector."** Killed by the
  exhaustive incidence distribution above: the maximum over all `3,432` anchors is `12`.

## 6. Explicit nonclaims

This is a support-level statement about one pinned quotient profile. It is not a bound on the row,
not an MCA numerator, not a slope or ray count, and it moves no ledger term. First-match survival,
received-word realization and the projection to codewords are untouched. The packet proves a lower
bound on one shell; it proves no upper bound on any shell, and in particular it does not establish
any replacement uniform cap — `d_e(A) <= 1237` on the band is an open hypothesis, not a result of
this note.

## 7. Derivation-direction ledger

| printed value | direction | basis |
|---|---|---|
| `p`, generator, punctures, `|Q'| = 1022`, support size `479`, depth `32` | frozen | integrated pinned profile |
| `447 = 479 - 32`, band `33..213` | derived | Newton rigidity |
| `1225 = C(7,3)^2`, family size `3432 = C(14,7)` | derived | constant-shift whole-class exchange |
| `12` mixed supports at `192`, `14` at `256`, sector size `26` | enumerated | declared same-core sector census |
| incidence distribution over `3,432` anchors | enumerated | full anchor sweep, counts sum to `3432` |
| `d_192(A) >= 1237`, `d_256(A') >= 1243` | derived from the two enumerations | `1225 + 12`, `1225 + 18` |
| `14,456,476` | cited | integrated compiler ambient term |
| `15009416`, `1767799`, `16776854`, `16777301` | derived | exact compiler arithmetic |
| maximum incidence `12` | enumerated | distribution above; source summary field corrected from `8` |

## 8. Formalization and replay boundary

The stdlib-only Lean package `experimental/lean/m31_flatness_champion_refutation/` kernel-checks the
exact arithmetic of every claim line above: the packet identity `1225 + 12 = 1237`, the band
membership `33 <= 192 <= 213` and the strict excess over `1233`, the deficiency-`256` floor
`1225 + 18 = 1243`, the four compiler totals with their comparisons against `B*`, the reserve, the
incidence-distribution total `3432` with its maximum `12`, and the binomial identities
`C(7,3)^2 = 1225` and `C(14,7) = 3432`. Each theorem carries a `#print axioms` census in
`M31FlatnessChampionRefutation/Refutation.lean`.

Axiom disclosure, as the build prints it. The package declares `22` theorems. Twenty-one of them
report `does not depend on any axioms`; the single exception is `census_max_attained`, which reports
`depends on axioms: [propext, Quot.sound]`, both entering through decidable list membership. No
theorem reports `sorryAx`. Proofs use `rfl` and `decide` only — **`native_decide` is not used
anywhere in this package**, so every check above is a kernel reduction rather than a compiled
evaluation. The package is stdlib-only with no dependencies, so `Nat.choose` is unavailable and the
binomial coefficients are defined inside the module as `binom`.

The enumeration itself — the label reconstruction, the sector sweep and the direct prefix
multiplications — is reported here as recorded values with their exact parameters, in line with the
repository's no-shipped-script convention. No script accompanies this packet in any language.
