---
workboard_item: M1
row: Mersenne-31 list at 2^-100
object: LIST
target_epsilon: 2^-100
agreement: 1116023
B_star: 16777215
direct_statement: "Adversarial tension audit of the pinned depth-32 quotient-prefix flatness conjecture. The integrated ledger does not force a 1,234th in-band neighbor. The eight known T16-mixed deficiency-192 neighbors are exactly closed under every same-canonical-T32-remainder selector continuation at deficiency 192. Their corresponding selector continuations produce eight direct-checked deficiency-256 neighbors, which together with 1,225 whole-T64 quadruple swaps give a rooted floor of 1,233 at deficiency 256. The band conjecture therefore survives this lens, but it does not by itself discharge the out-of-band premise used by the coefficient-four compiler."
architecture: DIRECT_PINNED_C2048_U0_V1_TENSION_AUDIT
partition_digest: "N/A; rooted support-fiber audit, no first-match owner or row atom"
atom_or_cell: "Q / pinned quotient prefix fiber / rooted shell flatness"
quantifier: "The closure theorem is exhaustive over all complete-T64 and complete-T32 selector continuations of the four canonical remainders represented by the eight integrated mixed neighbors. The logical countermodel is universal over the stated band implication only. No universal cap over all pinned-domain supports is proved."
projection_and_unit: "Valid 479-supports per fixed first-32 locator-coefficient target and fixed anchor, resolved by deficiency. No received word, codeword, explanation, ray, slope, or list-row payment."
claimed_bound: "Kernel-checked shard: exactly eight distinct deficiency-192 supports occur in the complete-block closure of the integrated mixed packet, and exactly eight corresponding deficiency-256 supports occur there; the deficiency-256 packet is disjoint from 1,225 whole-T64 quadruple swaps, yielding 1,233 direct-checked deficiency-256 neighbors. No upper bound on the full deficiency shell is claimed."
status: PROVED
impact: ROUTE_CUT
falsifier: "For the proved shard: any complete-T64 or complete-T32 selector continuation of one of the four represented mixed remainders that is a new deficiency-192 neighbor; any corresponding deficiency-256 support failing direct prefix equality, support validity, deficiency, or distinctness; or any overlap with the whole-T64 quadruple-swap family. For the champion conjecture: one pinned target, anchor, and deficiency in 33..213 with at least 1,234 distinct neighbors."
replay: "From experimental/lean/m31_flatness_conjecture_a1_s2: lake build M31FlatnessConjectureA1S2 M31FlatnessConjectureA1S2.Tension; lake build. Lean 4.31.0, stdlib only. Every theorem has a #print axioms census; native_decide use is disclosed."
---

# M31 flatness conjecture round A1: tension audit

**STATE: DRAFT**

**Request worked from:** attack the round-C1 pinned M31 flatness champion by pure
derivation from the integrated swap, mixing, obstruction, moment, and
selector-skeleton ledgers.

## Claim line

SHARD PROVED: the eight integrated `T_16`-mixed deficiency-`192` neighbors of the saturated anchor are exactly closed under every same-canonical-`T_32` selector continuation at deficiency `192`; the corresponding continuations give eight direct-checked deficiency-`256` neighbors, so the named tension ledger supplies no `1,234`th in-band neighbor, while exposing an out-of-band premise that the conjecture itself does not prove.

## Champion under attack

On the pinned quotient profile, let `D` be the punctured domain of size `1,022`,
let every support have size `479`, and let `pref_32` be the first `32`
nonleading coefficients of the monic support locator.  For a target `eta`, an
anchor `A` in its fiber, and a deficiency `e`, write

```text
d_e(A) = #{B : |B|=479, pref_32(B)=eta, |A\B|=e}.
```

The round-C1 champion is the pointwise assertion

```text
33 <= e <= 213  ==>  d_e(A) <= 1,233
```

for every target and anchor on this one pinned domain.

The attack found no contradiction to that quantifier.  It did find a missing
case in the advertised downstream story: the compiler sums all `447`
admissible deficiencies, whereas the champion controls only `181` of them.
The remaining `266` shells require a separate theorem.  The new
deficiency-`256` packet proves that this out-of-band sector is nonempty and can
reach the same rooted count as the saturated in-band shell.

## New kernel-checked closure theorem

The imported mixed packet has one standard anchor, `1,225` whole-`T_64`
triple-swap neighbors, and eight further `T_16`-mixed neighbors at deficiency
`192`.  Remove every complete `T_64` block, or every complete `T_32` block,
from each mixed neighbor.  The eight neighbors represent four canonical
remainders.

For the four representatives, the exact complete-block geometry is:

| quantity | representative profile |
|---|---|
| remainder size after complete `T_64` removal | `351, 415, 415, 351` |
| available complete `T_64` classes | `4, 2, 2, 4` |
| required complete `T_64` selectors | `2, 1, 1, 2` |
| remainder size after complete `T_32` removal | `351, 415, 415, 351` |
| available complete `T_32` classes | `9, 5, 5, 9` |
| required complete `T_32` selectors | `4, 2, 2, 4` |

Every selector continuation is rebuilt as a full support and tested by direct
multiplication of all locator factors.  At deficiency `192`, the four closure
sizes are

```text
3, 1, 1, 3.
```

The complete-`T_64` and complete-`T_32` closures agree as sets for every
representative.  Their distinct union has size eight and is exactly the
integrated mixed-neighbor list.  Thus the most immediate closure attack on the
champion's weakest link is exhausted: the finer `T_32` skeleton does not create
a ninth mixed neighbor at the saturated shell.

Lean evidence:

```text
M31FlatnessConjectureA1S2.mixed_remainder_geometry_exact
M31FlatnessConjectureA1S2.mixed_t64_t32_closure_exact
```

The final predicate in the second theorem checks support validity, inequality
from the anchor, rooted deficiency, and equality of the first `32` locator
coefficients by direct multiplication.

## Corresponding out-of-band packet

The same four remainders have corresponding selector continuations at
deficiency `256`.  Their closure sizes are again

```text
3, 1, 1, 3.
```

The distinct union contains eight supports.  All eight are direct-checked
same-target neighbors and none is a whole-`T_64` swap.  Independently, choosing
four of the seven occupied complete `T_64` classes and four of the seven empty
ones gives

```text
C(7,4)^2 = 1,225
```

whole-block deficiency-`256` neighbors.  The two families are disjoint, so the
same anchor has at least

```text
1,225 + 8 = 1,233
```

neighbors at deficiency `256`.

Lean evidence:

```text
M31FlatnessConjectureA1S2.reflected_e256_mixed_packet_exact
M31FlatnessConjectureA1S2.reflected_e256_full_packet_exact
```

This is a new rooted support-level floor, not a full-shell upper bound and not
a list-row payment.  It does not refute the champion because `256` lies outside
the frozen band.

## Adversarial ledger, two angles per named attack

| named attack | first angle | second angle | outcome and precise obstruction |
|---|---|---|---|
| swap census route cuts | The whole-`T_64` shell reaches `1,225`, below the cap. | Closing the mixed packet under all complete-`T_64` swaps produces exactly the known eight at deficiency `192`. | No ninth neighbor; any refutation must change the canonical remainder or use a ragged continuation not generated by complete blocks. |
| the `1,225 + 8` composition | Exact direct support enumeration gives `1,233`, so the conjecture has no slack at the known anchor. | Corresponding selectors reproduce `1,225 + 8` at deficiency `256`, not at a second in-band shell. | Saturation is real but shell-local. Adding counts from different deficiencies is invalid. |
| off-lattice deficiency `96` | The deployed pair is in a different shell from deficiency `192`; the champion is pointwise in `e`. | The complete-`T_32` selector model prints zero at `96` while the deployed pair exists and agrees through locator coefficient `47`, breaking at `48`. | This is a scope counterexample to selector-to-deployed transport, not to the champion. Lean: `selector_zero_and_deployed_e96_coexist`. |
| constant-shift obstruction | The comparison fiber has size `145,422,675`, but it lives on a different evaluation domain. | A typed numerical model simultaneously has pinned-band shell `1,233` and the comparison-domain fiber above eight budgets. | No domain-transfer theorem exists; the obstruction kills domain-agnostic flatness only. |
| moment-blind pair | The unsafe abstract maximum is `16,794,161` after matching moments through order `990`, but the maps are arbitrary occupancy maps. | The statistics are unlabelled and do not retain target, anchor, shell, or RS-realizability. | No implication to a pinned rooted shell. Lean records numerical coexistence in `typed_external_obstructions_coexist`. |
| `T_32` skeleton cap | The exact selector fiber maximum is `3,432` and the nontrivial collision maximum is `482`; neither is a deployed rooted-shell count. | The exact same-remainder closure computation uses the deployed supports and direct locator multiplication, and still returns only the eight known mixed neighbors at deficiency `192`. | A refutation must be off-remainder or ragged; the selector maximum cannot simply be added to the deployed shell. |
| coefficient-four compiler | The champion controls `181` band shells, not the full `447`; `266` shells remain outside its quantifier. | `band_only_countermodel` gives a formal model satisfying the band cap and violating an out-of-band uniform cap at deficiency `214`; the actual corresponding packet shows concrete pressure at deficiency `256`. | The compiler consequence needs an explicit out-of-band rooted-shell theorem. The conjecture alone does not imply it. |

## Exact consistency and route cuts

The known in-band packet is checked again as

```text
1,225 whole-block neighbors
+    8 mixed neighbors
=1,233 distinct deficiency-192 neighbors.
```

A ninth mixed neighbor would give `1,234` and refute the champion immediately at
that anchor.  The closure theorem proves that neither complete-`T_64` nor
complete-`T_32` selector continuation supplies it.

The selector-atlas arithmetic remains consistent:

```text
nontrivial selector collision maximum = 482
central deficiency-192 value          = 1,225
cross-pattern value at that shell     = 10
pointwise selector maximum            = max(1,225,10) = 1,225
full selector-fiber maximum           = 3,432.
```

The cross-pattern value is an alternative candidate inside a pointwise maximum,
not an additive family certified to co-realize with the central shell.

The compiler arithmetic is also exact:

```text
1 + 1,233*447 + 14,456,476 = 15,007,628
16,777,215 - 15,007,628    = 1,769,587

1 + 5,191*447 + 14,456,476 = 16,776,854
1 + 5,192*447 + 14,456,476 = 16,777,301.
```

These identities show why a full-shell intercept of `5,192` fails.  They do not
supply the missing full-shell theorem.

## Routes killed

- **Shell aggregation.**  A support at deficiency `96` or `256` cannot be added
  to the rooted deficiency-`192` shell.
- **Selector-envelope addition.**  The central and cross-pattern selector laws
  enter a pointwise maximum, not an automatically disjoint sum.
- **Complete-block continuation.**  The complete-`T_64` and complete-`T_32`
  closures of all four known mixed remainders are exhausted.
- **Comparison-domain transfer.**  The constant-shift construction changes the
  domain and does not specialize to the pinned quotient set.
- **Moment inversion.**  Matching unlabelled moments through the certified order
  does not constrain the rooted RS-realizable shell.
- **Band-to-compiler implication.**  A cap on `33..213` does not control
  `214..479`.

## What remains capable of refutation

The champion's minimal falsifier is still one full list of `1,234` distinct
valid supports for one target, anchor, and deficiency in `33..213`.  After this
audit, the sharpest search space is:

- ragged continuations that change the canonical `T_32` remainder;
- off-remainder collisions co-realized at the standard saturated anchor;
- signed `T_8` or smaller-block relations not expressible as complete-`T_32`
  selector completion; and
- an anchor transport placing a known ragged collision into the saturated
  fiber without changing the target or deficiency.

The reviewed ragged packet constructs a deficiency-`192` pair agreeing through
locator coefficient `39` on the pinned domain, but it supplies a different
target and anchor rather than a ninth neighbor of the saturated root.  It is a
candidate mechanism, not a theorem premise of this packet.  The missing theorem
is co-realization with the standard `1,233`-neighbor root.

## Lean package and axiom disclosure

Package:

```text
experimental/lean/m31_flatness_conjecture_a1_s2/
```

Namespace:

```text
M31FlatnessConjectureA1S2
```

The following five declarations use stdlib `native_decide`; their printed axiom
censuses contain `propext` and the generated theorem-local native-decision
certificate axiom:

```text
integrated_floor_matches_cap
mixed_remainder_geometry_exact
mixed_t64_t32_closure_exact
reflected_e256_mixed_packet_exact
reflected_e256_full_packet_exact
```

`selector_zero_and_deployed_e96_coexist` composes three already checked source
theorems and prints `propext` plus their generated native-decision certificate
axioms.  `selector_atlas_scope_arithmetic` prints `propext`, `Quot.sound`, and
the source selector-atlas native-decision certificate axiom.
`band_only_countermodel` prints `propext` and `Quot.sound`, inherited from the
stdlib simplifier proof.  `typed_external_obstructions_coexist` and
`compiler_arithmetic_requires_out_of_band_input` print no axioms.

Every declared theorem is followed by `#print axioms`.  No `sorry`, `admit`,
custom axiom, Mathlib import, or Python artifact is present.

## Derivation-direction ledger

Alphanumeric lane identifiers, toolchain versions, and digits occurring only
inside source paths or Lean declaration names are identifiers, not printed
mathematical constants.

| printed value or family | direction | source or derivation |
|---|---|---|
| pinned profile `c=2,048`, `(u,v)=(0,1)` | frozen | round contract |
| `2^31-1`, `2^-100`, `2,147,483,647` | derived / frozen | field and target contract |
| `1,116,023`, `16,777,215` | frozen | deployed list-row agreement and budget |
| `1,022`, `479`, `32` | enumerated / frozen | deployed punctured domain, support size, prefix depth |
| `33`, `213`, `181` | frozen then derived | champion endpoints; inclusive band size |
| `447`, `266`, `214`, `479` | derived / bounded-domain labels | full admissible shell count, uncovered count, first uncovered shell, terminal deficiency |
| `8`, `16`, `32`, `64` | enumerated / structural | quotient block sizes and integrated mixed count |
| `7`, `4`, `1,225` in `C(7,4)^2` | enumerated then derived | complete-class quadruple-swap census |
| `1,225`, `8`, `1,233`, `1,234` | enumerated then derived | integrated shell composition, cap, and minimal falsifier |
| `64`, `96`, `128`, `192`, `256` | frozen shell labels | integrated whole-block, off-lattice, saturated, and corresponding shells |
| `39`, `40`, `47`, `48`, `63` | enumerated | reviewed ragged and integrated prefix agreement / first-break depths |
| four canonical remainder representatives | enumerated | quotient by equality of complete-block remainder among the eight integrated mixed neighbors |
| `351,415,415,351` | enumerated | canonical remainder sizes for the four representatives |
| `4,2,2,4`; `2,1,1,2`; `9,5,5,9`; `4,2,2,4` | enumerated | available classes and selector sizes at the two block levels |
| `3,1,1,3` and distinct total `8` | enumerated | closure sizes and union size at each of the two audited deficiencies |
| selector structural value `0` at deficiency `96` | enumerated | exact deficiency-spectrum generator; contrasted with the deployed pair without transport |
| `3,432`, `482`, `10`, `1,225` | enumerated / derived comparison | selector atlas maxima and the pointwise central/cross comparison |
| `145,422,675`, multiplier `8`, excess `11,204,955` | enumerated then derived | comparison-domain obstruction and budget excess |
| order `990`, maximum `16,794,161`, excess `16,946` | enumerated then derived | abstract moment-blind pair |
| `14,456,476` | derived from a proved theorem | coefficient-four ambient contribution |
| `15,007,628`, `1,769,587` | derived | champion compiler total and reserve |
| `5,191`, `16,776,854` | derived | largest live uniform intercept and its total |
| `5,192`, `16,777,301` | derived | first failing uniform intercept and its total |
| universal full-shell upper for the pinned profile | not obtained / open | no source theorem covers every remaining shell |
| champion pointwise upper on `33..213` | not obtained / open | this packet proves only a closure shard and consistency audit |

## References

- `experimental/notes/thresholds/m31_flatness_conjecture_c1.md` — champion
  statement, falsifier, consistency pre-check, and weakest link.
- `experimental/notes/thresholds/m31_quotient_t16_mixing_floor.md` — integrated
  `1,225 + 8` rooted packet and direct prefix certificates.
- `experimental/notes/thresholds/m31_quotient_band_swap_census_t16_mixing.md` —
  whole-block shell census and off-lattice witness.
- `experimental/notes/thresholds/m31_t32_skeleton_flatness_keystone.md` —
  selector atlas and scope boundary.
- `experimental/notes/thresholds/m31_selector_spectrum_generator_v1.md` —
  exact structural selector spectrum and zero predictions.
- `experimental/notes/thresholds/m31_flatness_keystone_constant_shift_obstruction.md`
  — comparison-domain route cut.
- `experimental/notes/thresholds/m31_flatness_keystone_moment_blind_pair.md` —
  abstract moment-blind occupancy pair.
- `experimental/notes/thresholds/m31_q_rooted_shell_envelope.md` — rooted-shell
  compiler interface and open deployed premise.
- `experimental/notes/thresholds/m31_t16_ragged_witness_v1.md` and
  `experimental/lean/m31_t16_ragged_witness/` — reviewed candidate mechanism,
  not a theorem premise of this packet.
- Active manuscript labels: `def:primitive-q`, `def:q-row-atom`,
  `prop:moment-sandwich`, `thm:moment-q`, and `lem:newton-equivalence`.

## Natural next step

Enumerate the standard anchor's ragged, remainder-changing deficiency-`192`
sector with target-labelled constraints retained.  The first decisive output is
either a ninth non-full mixed neighbor, which refutes the champion, or a theorem
that every such continuation changes target, deficiency, or first-match owner.
