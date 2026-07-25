---
workboard_item: M1
row: Mersenne-31 list at 2^-100
object: LIST
target_epsilon: 2^-100
agreement: 1116023
B_star: 16777215
direct_statement: "Attack the pinned depth-32 pointwise shell conjecture by removing each substantive hypothesis and testing its lattice, off-lattice, degenerate, and extremal boundaries."
architecture: DIRECT_PINNED_C2048_U0_V1_BOUNDARY_AUDIT
partition_digest: "N/A; support-level rooted-prefix packets, no first-match row atom"
atom_or_cell: "Q / pinned quotient prefix fiber / scalar rooted-shell conjecture"
quantifier: "Every valid depth-32 target, every canonical 479-support anchor in that target fiber, and every exact deficiency from 33 through 213 on the pinned two-puncture quotient domain."
projection_and_unit: "Canonical support lists representing 479-subsets, direct monic locator prefixes, rooted exact deficiency, and packet cardinality. No received word, codeword, ray, slope, or row payment."
claimed_bound: "The exact champion is not refuted. Three weakened interfaces are refuted to certificate standard: restore one puncture; observe only 31 coefficients; or pool exact deficiencies before applying the scalar cap."
status: CONJECTURAL
impact: ROUTE_CUT
falsifier: "For the surviving champion, one duplicate-free packet of 1234 canonical supports at one exact deficiency in the frozen band and one frozen target and anchor."
replay: "Stdlib-only package experimental/lean/m31_flatness_conjecture_a1_s3/. Every declaration has a #print axioms census; native_decide and ordinary decide are disclosed below."
---

# M31 flatness conjecture round A1 — necessity and boundary attack

**STATE: COMPLETE**

**Request worked from:** attack the round-C1 scalar champion through hypothesis
necessity, the lattice points, off-lattice residues, and every degenerate or
extremal regime it covers.

SURVIVES: the exact pinned depth-32, exact-shell cap was not refuted; the lens certifies three sharp failure surfaces—one restored puncture, one lost locator coefficient, and one lost exact-shell quantifier—and leaves the ordered obstructions below.

## Champion under attack

Write `Q'` for the frozen two-puncture quotient-label domain. For a valid target
`eta`, a canonical anchor `A` in its depth-32 locator-prefix fiber, and an exact
rooted deficiency `e`, let `d_e(A)` be the number of other canonical supports in
the same target fiber at deficiency `e`. The champion is

```text
for every eta, A, and e with 33 <= e <= 213: d_e(A) <= 1233.
```

The new certificates never replace cardinality by an average or moment. Each
claimed prefix is checked by truncated multiplication of all 479 linear
factors.

## Certified failure surface A — one restored puncture

Restore deleted representative `3`, while representative `1` remains deleted.
The ordered domain then has 1,023 labels. The standard anchor remains valid.
Its seven occupied intact T64 classes may exchange three classes with three of
eight available outside intact T64 classes. The exact candidate count is

```text
C(7,3) C(8,3) = 35 * 56 = 1960.
```

The formal packet takes the first 1,234 candidates and directly verifies
canonical 479-support validity, pairwise distinctness, exact deficiency 192,
and equality of all 32 locator coefficients with the anchor target.

```text
M31FlatnessConjectureA1S3.single_puncture_boundary_packet_exact
M31FlatnessConjectureA1S3.single_puncture_uniform_cap_refuted
```

Thus each of the two punctures is load-bearing at the proposed scalar. The
same-parameter comparison-domain constant-shift packet is a distinct second
angle showing that field size, domain size, support size, prefix depth, and the
ambient average alone cannot imply flatness.

## Certified failure surface B — depth 31

Keep the exact pinned domain and anchor, but observe only the first 31
nonleading locator coefficients. The seven occupied and seven outside T64
classes split into fourteen intact T32 classes on each side. Fix six occupied
T32 classes and choose six outside T32 classes. The full symmetric family has

```text
C(14,6) = 3003
3003^2 = 9018009
```

ordered removed/added pairs. The formal falsifier fixes one removed six-set and
checks the first 1,234 added six-sets. Every resulting support is canonical,
distinct, has exact deficiency 192, and shares the first 31 coefficients. One
selected member separates at coefficient 32:

```text
anchor coefficient 32 = 141998040
break coefficient 32  = 138806059.
```

```text
M31FlatnessConjectureA1S3.depth31_boundary_packet_exact
M31FlatnessConjectureA1S3.depth31_uniform_cap_refuted
```

This locates the prefix-depth boundary exactly between 31 and 32. The hidden
constant-shift block lemma supplies the independent mechanism-level angle: a
complete block whose degree exceeds the observed prefix is invisible there.

## Certified failure surface C — pooling exact shells

At one standard target and anchor the certified exact-shell packets are

```text
e = 64  :   49 full-T64 neighbors
e = 128 :  441 full-T64 neighbors
e = 192 : 1233 neighbors = 1225 full-T64 + 8 T16-mixed.
```

Their union has

```text
49 + 441 + 1233 = 1723
```

canonical, pairwise distinct, same-target neighbors inside the band. The new
module directly rechecks the union and its exact deficiency spectrum.

```text
M31FlatnessConjectureA1S3.aggregate_shell_packet_exact
M31FlatnessConjectureA1S3.aggregate_uniform_cap_refuted
```

The cap is therefore pointwise in exact `e`; it cannot be charged once to a
whole-band fiber.

## Representation boundary

Canonical ordering and duplicate-freeness are necessary for the executable list
interface to represent set cardinality. If duplicate-freeness is removed, one
valid deficiency-64 neighbor can be repeated 1,234 times.

```text
M31FlatnessConjectureA1S3.duplicate_guard_boundary_exact
```

This refutes only the weakened representation, not the mathematical set
statement.

## Minimal surviving hypothesis set

| Clause | Boundary verdict | Evidence |
|---|---|---|
| Exact two-puncture quotient profile | Necessary | One restored point gives a direct 1,234-neighbor packet. |
| Prefix depth 32 | Necessary at cap 1,233 | Depth 31 gives a direct 1,234-neighbor packet and an explicit coefficient-32 break. |
| Exact deficiency `e` | Necessary | Pooling three shells gives 1,723 neighbors. |
| Canonical duplicate-free set encoding | Necessary for the executable representation | Repetition or permutation otherwise counts encodings rather than supports. |
| Lower cutoff 33 | Not necessary for truth | Newton rigidity empties all smaller distinct-support shells. |
| Upper cutoff 213 | Not certified necessary | It is the coefficient-four crossover; no next-shell counterexample was obtained. |
| Universal target and anchor | Still essential to the champion's scope | Fixed-anchor packets do not classify the worst anchor. |
| Full dyadic alignment | Invalid as a completeness hypothesis | Mixed and off-lattice witnesses leave that sector. |

The smallest substantive statement surviving this panel is the original pinned,
depth-32, exact-shell conjecture with set semantics. Its lower endpoint may be
extended through the empty Newton shells. Its upper endpoint is not shown sharp.

## Named attacks, two angles each

**Lattice point `e = 64`.** Full-T64 swaps give the exact rooted count 49. The
aligned census independently exhausts its declared deficiency-64 sector and
finds no non-block addition. The remaining obstruction is the unclassified
ragged sector; the local isolation lemma excludes only corrections moving at
most 32 additional points per side.

**Lattice point `e = 128`.** Full-T64 double swaps give 441. The independent
cross-remainder two-equation census reproduces 441 in its declared scope. No
theorem transports every support collision into that aligned scope.

**Lattice point `e = 192`.** The 1,225 full-T64 triple swaps are exact. Eight
direct T16-mixed neighbors raise the same rooted packet to 1,233 and consume all
scalar slack. A separate T32 exchange confirms that full-T64 classification is
false, but uses another anchor. A ninth non-full-class neighbor at the standard
anchor is the smallest champion falsifier.

**Off-lattice residue.** An integrated deficiency-96 pair agrees through
coefficient 47 and first differs at coefficient 48. Separately, the aligned
standard-anchor census is empty in its deficiency-96 slice and the corrected-tail
argument excludes perturbations through 32 points. The obstruction is
amplification: no construction puts 1,234 distinct off-lattice neighbors at one
target and anchor.

**Degenerate lower regime.** Newton rigidity eliminates distinct collisions
through deficiency 32. Removing representation guards creates only encoding
inflation, which the formal set interface excludes.

**Upper and extremal regime.** The same-remainder T32 census gives 40 at
deficiency 224. The full-T64 complement shell gives 1,225 at deficiency 256.
Both structured tests remain below the cap, but neither exhausts the ragged
post-crossover sector.

## Ordered obstructions that stopped refutation

1. **Standard-anchor ragged census missing.** The known deficiency-192 packet is
   exactly at the cap, but no exhaustive theorem decides whether a ninth ragged
   neighbor exists at that same target and anchor.
2. **Aligned equations are not complete.** T16 and T32 selector laws classify
   only their declared sectors.
3. **Off-lattice amplification is missing.** The deficiency-96 certificate gives
   existence on another anchor, not a large rooted degree.
4. **Post-crossover completeness is missing.** Structured upper tests stay below
   the cap, while the nonaligned residual has no census.
5. **Generic methods are blocked.** Parameter-only flatness, averages, finite
   moments, small corrected tails, and degree-uniform character-sum routes do not
   control the required worst rooted shell.

The natural next attack is an exact standard-anchor census of the ragged
coefficient-32 kernel at deficiency 192. The first binary goal is one new
neighbor outside the certified 1,233-member packet.

## Derivation-direction ledger

| Printed item | Direction | Certificate or source |
|---|---|---|
| target `2^-100`, agreement `1116023`, budget `16777215` | Frozen row contract | workboard metadata and C1 dossier |
| `p = 2147483647` | Derived from `2^31-1` | `M31QuotientT16MixingFloor.Witness.fieldPrime` |
| deleted representatives `1` and `3` | Frozen and enumerated | `M31QuotientT16MixingFloor.Witness.puncturedReps` |
| pinned domain `1022`, support size `479` | Enumerated and direct-checked | `quotient_domain_exact`; packet predicates |
| depth `32`, band `33..213`, cap `1233` | Frozen | round-C1 dossier |
| one-puncture domain `1023` | Enumerated | `single_puncture_boundary_packet_exact` |
| class pools `7` and `8`, exchange size `3` | Enumerated by construction | `insideT64`, `restoreThreeOutsideT64`, `restoreThreeSpecs` |
| `1960 = 35*56` | Derived from exact combinations | `boundary_family_arithmetic`; candidate-list census |
| selected packet `1234` | Enumerated and direct-verified | one-puncture and depth-31 packet theorems |
| T32 pools `14` and `14`, exchange size `6` | Enumerated | `depth31_boundary_packet_exact`, `depth31Removed` |
| `C(14,6)=3003`, symmetric family `9018009` | Derived from exact combinations | `boundary_family_arithmetic` |
| coefficient-32 values `141998040`, `138806059` | Enumerated by direct 479-factor multiplication | `depth31_boundary_packet_exact` |
| deficiencies `64`, `128`, `192`; counts `49`, `441`, `1225`, mixed `8`, total `1233` | Enumerated | integrated rooted-shell and mixed-neighbor theorems |
| pooled count `1723` | Enumerated and derived | `aggregate_shell_packet_exact`, `boundary_family_arithmetic` |
| off-lattice deficiency `96`, agreement `47`, break `48` | Enumerated by direct multiplication | integrated mixing witness |
| Newton and local correction threshold `32` | Derived | `lem:newton-equivalence`; local isolation lemma |
| deficiency `224` count `40` | Exhaustively enumerated in its declared sector | dyadic weight-law packet |
| deficiency `256` count `1225` | Enumerated | `M31QuotientBandMixing.Witnesses.rooted_shell_census` |

No printed mathematical count is an unlabeled expectation or heuristic.

## Axiom and validation census

Package:

```text
experimental/lean/m31_flatness_conjecture_a1_s3/
```

Namespace:

```text
M31FlatnessConjectureA1S3
```

Every theorem appears in the module's terminal `#print axioms` census. The five
closed finite packet or arithmetic theorems use `native_decide`, whose generated
theorem-local certificate axiom is disclosed. The Boolean packet predicates and
the three logical refutations use ordinary `decide` only for closed coefficient,
band, and numeric side conditions; the refutations otherwise consume certified
packet equalities and elementary natural-number contradictions. The package is
stdlib-only and contains no Mathlib import, custom axiom, unsafe declaration,
`sorry`, `admit`, Python artifact, or committed `.lake/` directory.

## References and exact labels

- `experimental/notes/thresholds/m31_flatness_conjecture_c1.md` — champion,
  exact falsifier, consistency pre-check, and weakest link.
- `experimental/notes/thresholds/m31_quotient_t16_mixing_floor.md` — exact
  `1225+8` packet, off-lattice witness, and local Newton isolation lemma.
- `experimental/notes/thresholds/m31_aligned_collision_census_v1.md` — aligned
  low-band exhaustion and unrestricted-census boundary.
- `experimental/notes/thresholds/m31_dyadic_weight_laws_v1.md` — T16/T32 level
  laws and declared-sector spectra.
- `experimental/notes/thresholds/m31_flatness_keystone_constant_shift_obstruction.md`
  — generic-domain and hidden-block obstruction.
- `experimental/grande_finale.tex`: `def:primitive-q`, `def:q-row-atom`,
  `prop:q-exact-target`, and `lem:newton-equivalence`.
- `experimental/notes/thresholds/m31_c2048_fixed_template_interleaved_quotient_route_cut.md`:
  Corollary 3.2.
- `experimental/notes/thresholds/m31_q_rooted_shell_envelope.md`: theorem `(RS)`.
