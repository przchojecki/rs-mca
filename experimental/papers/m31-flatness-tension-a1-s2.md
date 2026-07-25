# M31 flatness tension: exact closure of the integrated mixed sector

**STATE: DRAFT**

**Request worked from:** adversarially attack the round-C1 pinned M31 flatness
champion by pure derivation from the integrated swap, floor, off-lattice,
constant-shift, moment-blind, and `T_32` selector ledgers.

## Abstract

The pinned conjecture asserts that every rooted same-target shell in the
deficiency band `33..213` has at most `1,233` supports.  Its known sharp point is
one anchor with `1,225` whole-`T_64` triple swaps and eight additional
`T_16`-mixed neighbors at deficiency `192`.  This paper attacks the conjecture
only through contradictions with the integrated ledger.  No contradiction is
found.  Instead, a stdlib Lean census proves that the eight mixed neighbors are
exactly closed under every complete-`T_64` and complete-`T_32`
same-canonical-remainder selector continuation at deficiency `192`.  The
corresponding reflected continuations create eight new direct-checked neighbors at
deficiency `256`; together with `1,225` whole-`T_64` quadruple swaps they give a
new rooted out-of-band floor of `1,233`.  The result kills the most immediate
closure attack on the champion's weakest link and identifies the next
falsification surface: ragged, remainder-changing continuations co-realized at
the saturated anchor.  It also certifies that the band conjecture alone cannot
supply the out-of-band premise used in the printed coefficient-four compiler.

## Exact object and champion statement

Fix

```text
p = 2^31 - 1,
|D| = 1,022,
|A| = |B| = 479,
prefix depth = 32.
```

Here `D` is the pinned punctured `c=2,048`, `(u,v)=(0,1)` quotient domain.  For
a locator-prefix target `eta`, an anchor `A` in its fiber, and a deficiency
`e`, define

```text
d_e(A) = #{B subset D : |B|=479, pref_32(B)=eta, |A\B|=e}.
```

The champion is

```text
for every eta, every A in pref_32^{-1}(eta), and every 33 <= e <= 213,
d_e(A) <= 1,233.
```

Its certificate-standard falsifier remains one target, anchor, and in-band
deficiency with `1,234` distinct valid supports.

## Current best theorem

Let `A` be the integrated standard anchor and let `M` be its eight certified
`T_16`-mixed deficiency-`192` neighbors.  Remove every complete `T_64` block
from a member of `M`, or every complete `T_32` block, and complete the resulting
canonical remainder with every selector of the required cardinality.  Retain a
completion only after reconstructing the full support and directly multiplying
its locator to verify the target.

**Theorem.**  The complete-`T_64` and complete-`T_32` closures agree at
deficiency `192`, and their distinct union is exactly `M`.  For the four
canonical remainder representatives, the closure sizes are `3,1,1,3`.

**Reflected theorem.**  At deficiency `256`, the same four remainder closures
again have sizes `3,1,1,3`; their distinct union consists of eight valid
same-target supports, all outside the whole-`T_64` family.  Adding the
`C(7,4)^2 = 1,225` whole-`T_64` quadruple swaps yields `1,233` distinct
deficiency-`256` neighbors of `A`.

Kernel-checked names:

```text
M31FlatnessConjectureA1S2.mixed_remainder_geometry_exact
M31FlatnessConjectureA1S2.mixed_t64_t32_closure_exact
M31FlatnessConjectureA1S2.reflected_e256_mixed_packet_exact
M31FlatnessConjectureA1S2.reflected_e256_full_packet_exact
```

The first closure theorem is the proved shard of the champion: it certifies that
the integrated mixed sector and its complete-block continuations do not contain
the ninth mixed neighbor needed to cross the cap.  It is not a full shell upper
bound.

## Mechanism

The eight mixed neighbors collapse to four canonical remainders.  Their exact
geometry is:

| quantity | four-representative profile |
|---|---|
| complete-`T_64` remainder sizes | `351,415,415,351` |
| available complete `T_64` classes | `4,2,2,4` |
| required complete `T_64` selectors | `2,1,1,2` |
| complete-`T_32` remainder sizes | `351,415,415,351` |
| available complete `T_32` classes | `9,5,5,9` |
| required complete `T_32` selectors | `4,2,2,4` |

The proof does not trust compressed selector equations as verification.
For every enumerated selector, Lean rebuilds the full `479`-support, checks
membership in the punctured domain and duplicate-freeness, computes the rooted
deficiency, and evaluates the first `32` locator coefficients by multiplying all
linear factors.  The `T_64` closure and finer `T_32` closure are then compared
as sets.

At deficiency `192`, the four closures contribute `3,1,1,3`, whose distinct
union is the original eight supports.  The corresponding selector continuations
remain in the same target fiber but move to deficiency `256`; they contribute
another `3,1,1,3`.  This reflection is why the attack creates a new
out-of-band floor without refuting the in-band statement.

## Evidence against the champion

The evidence is sharp but not contradictory.

- The standard anchor has exactly the certified lower packet
  `1,225 + 8 = 1,233` at deficiency `192`.  A single additional distinct support
  there would refute the conjecture.
- A deployed off-lattice pair exists at deficiency `96` and agrees through
  locator coefficient `47`, first differing at `48`.
- The comparison-domain constant-shift construction has a fiber of
  `145,422,675`.
- Abstract occupancy maps can match moments through order `990` while one has
  maximum `16,794,161`, above the deployed budget.
- The complete-`T_32` selector atlas has selector-fiber maximum `3,432`.
- A reviewed candidate packet gives a ragged depth-`32` collision on the pinned
  domain (`M31T16RaggedWitness.RaggedWitness.explicit_ragged_collision`), so
  aligned dyadic censuses are not globally exhaustive.  Its target and anchor
  differ from the saturated packet, and it is not a premise of the theorems here.

Every item demonstrates a failure mode of a broad proof strategy.  None places
a `1,234`th support in the same target, at the same anchor, and at one in-band
deficiency.

## Evidence for survival under the tension lens

The attacks fail for distinct typed reasons.

**Whole-block and mixed census.**  The whole-`T_64` contribution at deficiency
`192` is `1,225`; the eight mixed supports reach but do not exceed the cap.
The new closure theorem exhausts all complete-block continuations of their four
remainders.

**Off-lattice pair.**  Deficiency `96` and deficiency `192` are different
pointwise shells.  Moreover, the selector-spectrum generator prints zero at
`96` while the deployed pair exists.  The kernel-checked coexistence theorem

```text
M31FlatnessConjectureA1S2.selector_zero_and_deployed_e96_coexist
```

shows that the selector generator is not a deployed-shell transport theorem.

**Constant-shift construction.**  Its large fiber lives on another evaluation
domain.  No theorem transfers it to the pinned quotient domain.

**Moment-blind pair.**  The abstract maps do not retain the RS target, anchor,
deficiency, or realizability data.  The numerical coexistence certificate is

```text
M31FlatnessConjectureA1S2.typed_external_obstructions_coexist.
```

**Selector skeleton.**  The exact atlas numbers `3,432` and `482` concern
selector fibers and selector collisions.  They cannot be added to the deployed
rooted shell.  Direct closure on the deployed supports produces no ninth mixed
neighbor.

## The compiler premise that remains open

The coefficient-four compiler sums `447` admissible deficiencies.  The champion
covers the inclusive band `33..213`, containing `181` deficiencies, leaving
`266` out of band.  The Lean theorem

```text
M31FlatnessConjectureA1S2.band_only_countermodel
```

constructs a formal shell function satisfying the champion's band cap while
taking value `5,192` at the first uncovered deficiency `214`.  This is a
logical countermodel, not an RS witness; it proves only that the band statement
does not imply a full-shell cap.

The arithmetic theorem

```text
M31FlatnessConjectureA1S2.compiler_arithmetic_requires_out_of_band_input
```

rechecks

```text
1 + 1,233*447 + 14,456,476 = 15,007,628,
16,777,215 - 15,007,628    = 1,769,587,

1 + 5,191*447 + 14,456,476 = 16,776,854,
1 + 5,192*447 + 14,456,476 = 16,777,301.
```

Thus `5,192` is the first failing uniform intercept in that arithmetic.  The
identities do not prove any out-of-band shell theorem.  The new
deficiency-`256` floor shows concretely that the omitted sector contains
nontrivial same-target mixing.

## Routes killed

The following derivations cannot refute the champion without a new bridge.

- Adding supports from different deficiencies.
- Adding the central and cross-pattern selector values, which form a pointwise
  maximum rather than a certified disjoint union.
- Extending one of the four known mixed remainders by complete `T_64` or
  complete `T_32` blocks.
- Transporting a comparison-domain fiber by parameter equality alone.
- Inverting unlabelled moments into a target-and-anchor pointwise shell bound.
- Treating the complete-`T_32` selector maximum as a deployed rooted degree.
- Treating the band conjecture as a theorem on all `447` admissible shells.

## Open questions and natural next step

The exact remaining falsification question is whether the standard saturated
anchor has a ragged, canonical-remainder-changing same-target neighbor at
deficiency `192` outside the eight certified mixed supports.

The natural next step is a target-labelled census of signed `T_8` and smaller
dyadic relations around that anchor, with direct locator multiplication as the
final check.  A decisive successor is either:

- a ninth non-full mixed support at deficiency `192`, giving the minimal
  `1,234`-support counterexample; or
- a theorem routing every ragged continuation away from the target, the
  deficiency, or the relevant first-match owner.

A separate theorem is required for the out-of-band compiler shells, regardless
of the champion's truth.

## Lean package, proof status, and axiom census

Package path:

```text
experimental/lean/m31_flatness_conjecture_a1_s2/
```

The package is stdlib-only and imports the integrated quotient, selector, and
rooted-shell dependencies through path manifests.  Every theorem has a `#print axioms` command.  The declarations
`integrated_floor_matches_cap`, `mixed_remainder_geometry_exact`,
`mixed_t64_t32_closure_exact`, `reflected_e256_mixed_packet_exact`, and
`reflected_e256_full_packet_exact` use `native_decide`; each printed census is
`propext` plus its theorem-local generated native-decision axiom.
`selector_zero_and_deployed_e96_coexist` inherits `propext` and the imported
generated native-decision axioms for the deployed support, prefix, and selector
zero certificates.  `selector_atlas_scope_arithmetic` inherits `propext`,
`Quot.sound`, and the imported atlas native-decision axiom.  The typed ledger and compiler arithmetic print no axioms.  The band
countermodel prints `propext` and `Quot.sound`.  There is no
`sorry`, `admit`, custom axiom, Mathlib dependency, `.lake/` artifact, or Python
artifact.

Green compilation validates the declarations and default target.  The
statement-to-source audit is recorded in the package correspondence file.

## Derivation-direction ledger

Alphanumeric lane labels, toolchain versions, and digits appearing only in file
paths or theorem names are identifiers rather than mathematical constants.

| printed value or family | direction | justification |
|---|---|---|
| `c=2,048`, `(u,v)=(0,1)` | frozen | pinned quotient profile |
| `2^31-1`, `2,147,483,647`, `2^-100` | derived / frozen | field and target |
| `1,116,023`, `16,777,215` | frozen | deployed agreement and budget |
| `1,022`, `479`, `32` | enumerated / frozen | domain, support size, prefix depth |
| `33`, `213`, `181` | frozen then derived | band endpoints and inclusive size |
| `447`, `266`, `214`, `479` | derived / bounded | full shell count, complement, first and last out-of-band labels |
| `8`, `16`, `32`, `64` | enumerated / structural | mixed count and dyadic block sizes |
| `7`, `4`, `C(7,4)^2`, `1,225` | enumerated then derived | whole-block quadruple-swap census |
| `1,225`, `8`, `1,233`, `1,234` | enumerated then derived | saturated floor, cap, and minimal falsifier |
| `64`, `96`, `128`, `192`, `256` | frozen shell labels | integrated shell evidence and reflected shell |
| `47`, `48` | enumerated | deployed off-lattice agreement and first break |
| `351,415,415,351` | enumerated | four canonical remainder sizes |
| `4,2,2,4`; `2,1,1,2`; `9,5,5,9`; `4,2,2,4` | enumerated | available classes and selector sizes |
| four canonical remainders; `3,1,1,3`, distinct total `8` | enumerated | remainder-class count, closure sizes, and union census |
| selector value `0` at deficiency `96`; `3,432`, `482` | enumerated | exact selector-spectrum prediction and selector-atlas maxima |
| `145,422,675`, multiplier `8`, excess `11,204,955` | enumerated then derived | comparison-domain obstruction |
| order `990`, maximum `16,794,161`, excess `16,946` | enumerated then derived | moment-blind pair |
| `14,456,476` | derived from a proved source theorem | ambient compiler contribution |
| `15,007,628`, `1,769,587` | derived | champion compiler total and reserve |
| `5,191`, `16,776,854` | derived | largest live uniform intercept and total |
| `5,192`, `16,777,301` | derived | first failing uniform intercept and total |
| full pinned-domain upper on every shell | not obtained / open | no exhaustive theorem |
| champion upper throughout `33..213` | not obtained / open | only a mixed-sector closure shard is proved |

## References

Lean:

- `experimental/lean/m31_flatness_conjecture_a1_s2/`
- `experimental/lean/m31_quotient_t16_mixing_floor/`
- `experimental/lean/m31_quotient_band_mixing/`
- `experimental/lean/m31_flatness_keystone/`
- `experimental/lean/m31_selector_spectrum/`
- `experimental/lean/m31_q_rooted_shell/`

Source notes:

- `experimental/notes/thresholds/m31_flatness_conjecture_c1.md`
- `experimental/notes/thresholds/m31_quotient_t16_mixing_floor.md`
- `experimental/notes/thresholds/m31_quotient_band_swap_census_t16_mixing.md`
- `experimental/notes/thresholds/m31_t32_skeleton_flatness_keystone.md`
- `experimental/notes/thresholds/m31_selector_spectrum_generator_v1.md`
- `experimental/notes/thresholds/m31_flatness_keystone_constant_shift_obstruction.md`
- `experimental/notes/thresholds/m31_flatness_keystone_moment_blind_pair.md`
- `experimental/notes/thresholds/m31_q_rooted_shell_envelope.md`

Reviewed candidate overlap, not used as a theorem premise:

- `experimental/notes/thresholds/m31_t16_ragged_witness_v1.md`
- `experimental/lean/m31_t16_ragged_witness/`

Upstream labels used:

```text
def:primitive-q
def:q-row-atom
prop:moment-sandwich
thm:moment-q
lem:newton-equivalence
```
