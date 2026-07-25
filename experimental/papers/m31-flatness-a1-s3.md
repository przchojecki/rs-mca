# Necessity surfaces for the M31 flatness champion

**STATE: COMPLETE**

**Request worked from:** adversarially attack the round-C1 M31 pointwise
flatness champion through hypothesis removal and the lattice, off-lattice,
degenerate, and extremal boundaries.

## Abstract

The champion asserts that on the pinned two-puncture M31 quotient-label domain,
every depth-32 locator-prefix target, every canonical 479-support anchor in that
fiber, and every exact deficiency from 33 through 213 have rooted shell degree
at most 1,233. The exact assertion survives this necessity-and-boundary panel.
The panel nevertheless locates three sharp failure surfaces with direct
stdlib-Lean certificates. Restoring only one deleted quotient label creates a
1,234-neighbor depth-32 packet at deficiency 192. Keeping the exact domain but
observing only 31 coefficients creates a 1,234-neighbor packet, with a selected
support separating from the anchor at coefficient 32. Keeping the exact domain
and depth but pooling the exact deficiencies 64, 128, and 192 creates 1,723
distinct same-target neighbors. Thus the exact two-puncture profile, depth 32,
and pointwise exact-shell quantifier are each necessary at the proposed scalar.
The lower cutoff is not necessary for truth because Newton rigidity empties the
smaller shells; the upper cutoff remains a compiler crossover rather than a
certified mathematical boundary. The smallest unresolved falsifier is one
additional non-full-class neighbor at the known deficiency-192 anchor.

## Frozen object and current best statement

Let

```text
p = 2^31 - 1 = 2147483647,
|Q'| = 1022,
|A| = 479,
prefix depth = 32,
band = 33..213,
cap = 1233.
```

For a valid target `eta`, a canonical anchor `A` in its locator-prefix fiber,
and exact deficiency `e`, let `d_e(A)` denote the number of other canonical
supports in that same target fiber at rooted deficiency `e`.

The current best statement is the surviving conjecture

```text
For every eta, every canonical A in the eta fiber, and every exact e with
33 <= e <= 213, d_e(A) <= 1233.
```

This paper does not prove that statement. It records that the assigned lens did
not produce its exact falsifier and gives the strongest certified boundary
information obtained.

### Boundary theorem A — one puncture is sharp

Restore representative `3` while representative `1` remains deleted. The
resulting ordered domain has 1,023 labels. At the standard anchor, choosing
three removed classes among seven occupied intact T64 classes and three added
classes among eight outside intact T64 classes gives 1,960 candidate exchanges.
The first 1,234 form a duplicate-free packet of canonical 479-supports at exact
deficiency 192, all sharing the anchor's full depth-32 target. Therefore the
cap-1,233 uniform shell statement on this one-puncture domain is false.

Kernel evidence:

```text
M31FlatnessConjectureA1S3.single_puncture_boundary_packet_exact
M31FlatnessConjectureA1S3.single_puncture_uniform_cap_refuted
```

### Boundary theorem B — depth 31 is false

On the exact pinned domain, split the seven occupied and seven outside T64
classes into fourteen T32 classes on each side. Fix six removed inside T32
classes and enumerate added six-subsets. The first 1,234 resulting supports are
canonical, duplicate-free, have exact deficiency 192, and share the first 31
locator coefficients with the standard anchor. A selected support has
coefficient 32 equal to 138,806,059, while the anchor has 141,998,040.
Therefore the depth-31 cap-1,233 statement is false on the exact domain, and the
failure is witnessed exactly at coefficient 32.

Kernel evidence:

```text
M31FlatnessConjectureA1S3.depth31_boundary_packet_exact
M31FlatnessConjectureA1S3.depth31_uniform_cap_refuted
```

### Boundary theorem C — the shell quantifier is pointwise

At the standard target and anchor, exact deficiency packets have sizes 49, 441,
and 1,233 at deficiencies 64, 128, and 192. Their union is a canonical,
duplicate-free same-target packet of size 1,723, with the three-shell spectrum
rechecked directly. Therefore replacing the pointwise bound on each `d_e(A)` by
one cap on the whole band is false.

Kernel evidence:

```text
M31FlatnessConjectureA1S3.aggregate_shell_packet_exact
M31FlatnessConjectureA1S3.aggregate_uniform_cap_refuted
```

### Interface theorem — duplicate-freeness is essential

Removing the duplicate guard from the executable list interface lets one valid
deficiency-64 neighbor be repeated 1,234 times. This refutes only the weakened
list encoding, not the set-cardinality champion.

Kernel evidence:

```text
M31FlatnessConjectureA1S3.duplicate_guard_boundary_exact
```

## Mechanism

A complete dyadic block of degree `d` has a monic locator of the form
`H(Y)-lambda`. Products of equally many blocks have a common leading `H`-power,
while every class-dependent term loses at least `d` degrees. A prefix shorter
than `d` therefore cannot distinguish the block selection. Restoring one
puncture turns an additional T64 class into a complete block; dropping the
prefix depth to 31 makes T32 blocks invisible.

The compressed block law is only the discovery mechanism. The formal
certificates construct each support and run the direct truncated product of all
479 linear factors. No compressed moment or selector equation is accepted as
the verification layer.

Deficiency is also part of the theorem's index, not an accounting convenience.
The packets at deficiencies 64, 128, and 192 are disjoint because their rooted
intersection sizes differ. Pooling them changes the object from a shell degree
to a band degree. Canonical ordering and duplicate-freeness likewise separate
set cardinality from the number of list encodings.

## Evidence for and against

The integrated standard-anchor zoo gives exact rooted counts

```text
e = 64  : 49,
e = 128 : 441,
e = 192 : 1225 + 8 = 1233.
```

The deficiency-192 packet is scalar-sharp but not a violation. Its 1,225
full-T64 neighbors and eight T16-mixed neighbors are direct locator-prefix
certificates. The aligned deficiency-64 census finds only the 49 full-block
swaps in its declared sector. The cross-remainder census reproduces 441 at
deficiency 128 and 1,233 at deficiency 192 in its declared scope. These support
the champion only inside typed aligned sectors; they do not prove an all-support
classification.

The first structured post-band probes also stay below the scalar. The
same-remainder T32 census has 40 at deficiency 224, and the full-T64 complement
shell has 1,225 at deficiency 256. This is evidence against an immediate
structured failure after the crossover, not a proof of continuation.

Against the champion, its weakest point has zero slack at deficiency 192.
Full-T64 classification is already false: eight T16-mixed neighbors and an
independent T32 pair leave that class. An off-lattice deficiency-96 pair agrees
through coefficient 47 before breaking at coefficient 48. A same-parameter
comparison domain has a much larger prefix fiber, excluding parameter-only or
average-only flatness. None reaches the champion's exact quantifiers: the mixed
and off-lattice packets do not provide 1,234 distinct neighbors at one pinned
target and anchor, while the comparison construction changes the domain.

## Hypothesis ledger

| Champion clause | Necessity status | Reason |
|---|---|---|
| Exact two-puncture domain | Certified necessary | Restoring one point gives a direct 1,234-neighbor packet. |
| Prefix depth 32 | Certified necessary at cap 1,233 | Depth 31 gives a direct 1,234-neighbor packet and an exact coefficient-32 break. |
| Exact shell `e` | Certified necessary | The three-shell union has 1,723 neighbors. |
| Canonical duplicate-free support encoding | Certified necessary for the executable representation | Repetition and permutation otherwise inflate representations. |
| Lower cutoff 33 | Not necessary for truth | Newton rigidity makes smaller distinct-support shells empty. |
| Upper cutoff 213 | Open as a mathematical boundary | No next-shell counterexample is certified; the cutoff comes from the coefficient-four compiler. |
| Universal target and anchor | Unresolved and retained | Fixing either weakens the theorem; no worst-anchor classification is known. |
| Full dyadic alignment | Invalid as a complete replacement | Mixed and off-lattice witnesses already leave that sector. |

The minimal substantive statement surviving this panel is the original
pinned-domain, depth-32, exact-shell conjecture with set semantics. Its lower
range may be extended across the empty Newton shells, while its upper range
cannot presently be enlarged or proved sharp.

## Routes killed

1. **Domain-agnostic flatness.** The one-restored-puncture packet breaks the
   scalar; the generic comparison domain separately breaks parameter-only
   control.
2. **Depth-31 replacement.** The direct 1,234-neighbor packet breaks it exactly
   at the next coefficient.
3. **Band-level scalar accounting.** The 1,723-neighbor union breaks it.
4. **Full-T64 classification.** Integrated T16 and T32 witnesses refute it.
5. **Small corrected tails.** Newton isolation forces corrections through 32
   points per side to be trivial.
6. **Aligned-census promotion.** Exact aligned results do not classify the
   ragged support sector.
7. **Average, finite-moment, and degree-uniform character-sum control.** The
   frozen route cuts do not imply a worst rooted-shell cap.

## Open questions and natural next step

The decisive question is whether the standard deficiency-192 target and anchor
have a ninth neighbor outside the eight certified T16-mixed supports and the
1,225 full-T64 supports. The natural next step is an exact census of the ragged
coefficient-32 kernel at that fixed anchor. The first binary milestone is one
additional canonical support; failure must come with a certificate covering the
complete ragged domain, not only a dyadic selector slice.

Secondary questions are whether off-lattice deficiency-96 relations can be
amplified at one anchor, whether the pointwise cap continues past deficiency
213, and whether every post-crossover collision admits a finite structural
atlas.

## Derivation-direction ledger

| Printed item | Direction | Evidence |
|---|---|---|
| target `2^-100`, agreement `1116023`, budget `16777215` | Frozen row contract | workboard metadata and champion dossier |
| `p = 2147483647` | Derived from `2^31-1` | frozen field definition |
| deleted representatives `1` and `3` | Frozen and enumerated | `M31QuotientT16MixingFloor.Witness.puncturedReps` |
| pinned domain `1022`, support `479` | Enumerated and direct-checked | `quotient_domain_exact`; packet predicates |
| depth `32`, band `33..213`, cap `1233` | Frozen | round-C1 dossier |
| one-puncture domain `1023` | Enumerated | `single_puncture_boundary_packet_exact` |
| class pools `7` and `8`, exchange size `3` | Enumerated | formal class lists and packet generator |
| one-puncture family `1960 = C(7,3)C(8,3)` | Derived from exact combinations | `boundary_family_arithmetic`; candidate-list census |
| selected packet `1234` | Enumerated and direct-checked | one-puncture and depth-31 packet theorems |
| T32 pools `14` and `14`, exchange size `6` | Enumerated | `depth31_boundary_packet_exact`, `depth31Removed` |
| `C(14,6)=3003`, symmetric family `9018009` | Derived from exact combinations | `boundary_family_arithmetic` |
| coefficient-32 values `138806059`, `141998040` | Enumerated by direct multiplication | `depth31_boundary_packet_exact` |
| exact deficiencies `64`, `128`, `192`; counts `49`, `441`, `1225`, mixed `8`, total `1233` | Enumerated | integrated rooted-shell and mixed-neighbor theorems |
| pooled count `1723` | Enumerated and derived | `aggregate_shell_packet_exact`, `boundary_family_arithmetic` |
| off-lattice deficiency `96`, agreement `47`, break `48` | Enumerated by direct multiplication | integrated mixing witness |
| Newton and correction threshold `32` | Derived | `lem:newton-equivalence`; local isolation lemma |
| post-band deficiency `224` count `40` | Exhaustively enumerated in its declared sector | dyadic weight-law packet |
| post-band deficiency `256` count `1225` | Enumerated | `M31QuotientBandMixing.Witnesses.rooted_shell_census` |

No printed mathematical count is an unlabeled expectation or heuristic.

## Formal package and axiom census

Package path:

```text
experimental/lean/m31_flatness_conjecture_a1_s3/
```

Namespace:

```text
M31FlatnessConjectureA1S3
```

Every theorem appears in the module's terminal `#print axioms` census. The five
closed finite packet or arithmetic results use `native_decide`, whose generated
theorem-local certificate axiom is disclosed. The Boolean packet predicates and
the three logical refutations use ordinary `decide` only for closed coefficient,
band, and numeric side conditions; the refutations otherwise use the certified
packet equalities and elementary natural-number contradiction. The package is
stdlib-only and contains no Mathlib import, custom axiom, unsafe declaration,
`sorry`, `admit`, Python artifact, or committed `.lake/` directory.

## References

- `experimental/notes/thresholds/m31_flatness_conjecture_c1.md` — champion,
  exact falsifier, consistency pre-check, and weakest link.
- `experimental/notes/thresholds/m31_flatness_conjecture_a1_s3.md` — complete
  attack report and ordered obstruction list.
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
