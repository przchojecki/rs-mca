---
workboard_item: M1
row: Mersenne-31 list at 2^-100
object: LIST
target_epsilon: 2^-100
agreement: 1116023
B_star: 16777215
direct_statement: "The complete-T32 selector-atlas rooted maximum spectrum (the fourteen values 0,49,0,441,0,1225,60,1225,210,441,45,49,3,1 at block deficiency t=1..14) equals the pointwise maximum of the central binomial law E(t)=C(7,t/2)^2 (even t, else 0) and four irredundant atlas-sourced coefficient laws X_sigma(t)=[z^d q^(t-f)](q+z)^a(q^2+z)^b(1+z)^c. Equality holds against the exhaustive 68,896-edge atlas maximum at every t=1..14, and in point form against the printed cap at every e=34..479 including every off-lattice zero. Each of the four signatures is an explicit atlas edge and is irredundant."
architecture: DIRECT_PINNED_C2048_U0_V1_T32_SELECTOR_SPECTRUM
partition_digest: "N/A (structural selector-spectrum identity; no first-match partition, owner allocation, or signed payment)"
atom_or_cell: "Q / PINNED_QUOTIENT_PREFIX_FIBER / SAME_REMAINDER_SELECTOR_SPECTRUM; not a v4 bankable atom or owner transport"
quantifier: "Every T32 block deficiency t=1..14 and every point deficiency e=34..479 in the printed selector cap. No universal quantifier over deployed rooted shells is discharged."
projection_and_unit: "Rooted complete-T32 selectors per fixed compressed selector target. No off-remainder, complete-shell, received-word, codeword, ray, slope, or list-row projection."
claimed_bound: "PROVED exact structural identity for the fourteen-value selector spectrum and its point-deficiency form. No new upper bound on any deployed support degree s_e is claimed; s_224>=40 stays a separate deployed floor and 60 stays a selector-model value."
status: PROVED
impact: LOCAL_ONLY
falsifier: "Any t in 1..14 where the five-law generator differs from the exhaustive atlas maximum; absence of any one printed source edge from allPatternPairs; failure to extract any one stated signature; failure of the point-form generator to agree with the resolved selector cap at one e in 34..479; or deletion of one signature without the certified loss (45,136,28,0) at t=(7,9,11,13)."
replay: "lake build in experimental/lean/m31_selector_spectrum (14 native_decide theorems, each followed by #print axioms; stdlib-only, Lean v4.31.0). Independent stdlib recompute: python3 experimental/scripts/verify_m31_selector_spectrum_generator.py --check (recomputes E, all X_sigma two independent ways, the pointwise-max equality, deletion losses, single-term reductions) and --tamper-selftest (exit 0 iff every mutation is caught)."
consumers: "None required for validity. The identity is a self-contained selector-model result; converting selector maxima into statements about deployed supports is outside this packet's scope."
risk_limits: "Selector-model scope only. This is an equality of finite selector-cap functions, not the deployed support inequality s_e <= kappa_32(e). No deployed collision law, transport, or off-remainder statement is claimed. Disclosed axioms: native_decide per theorem, plus propext on the four computed-equality theorems."
---

# M31 selector-spectrum structural generator (v1)

## Status

This packet proves an exact structural characterization of a computed spectrum
object.  The exhaustive complete-T32 selector atlas scans 68,896 nontrivial
compressed collision edges and prints, for block deficiency `t = 1,...,14`, the
rooted maximum spectrum

```text
kappa_32(32 t) = 0, 49, 0, 441, 0, 1225, 60, 1225, 210, 441, 45, 49, 3, 1.
```

The packet proves this fourteen-value list is the pointwise maximum of one
central binomial law and four irredundant coefficient laws, each extracted from
an explicit atlas edge, and lifts the identity to the point-deficiency range
`34,...,479`.  It is support-selector level only.  It does not prove any
deployed support inequality; the deployed interpretation of this spectrum is
outside the scope of this note.

## 1. Frozen objects and definitions

The atlas is generated from nine canonical signed relations and contains 68,896
oriented compressed edges (`allPatternPairs`, length proved `= 68896`).  Its
rooted maximum at block deficiency `t`, with selector size at most fourteen as
forced by 479-point supports, is `selectorRootedMaximum t`, and the fourteen
computed values are `computedBlockDeficiencySpectrum`.

Central law:

```text
E(t) = C(7, t/2)^2   if t is even,
E(t) = 0             if t is odd.
```

Coefficient law for a signature `sigma = (a,b,c,f,d)`:

```text
X_sigma(t) = [z^d q^(t-f)] (q+z)^a (q^2+z)^b (1+z)^c
           = sum over x+y+z=d with f+(a-x)+2(b-y)=t of C(a,x) C(b,y) C(c,z).
```

Four signatures:

```text
sigma_7  = (5, 0, 6, 4, 3),
sigma_9  = (8, 0, 3, 5, 5),
sigma_11 = (5, 3, 3, 3, 5),
sigma_13 = (3, 2, 3, 7, 4).
```

Generator and point-deficiency form:

```text
K(t) = max( E(t), X_{sigma_7}(t), X_{sigma_9}(t), X_{sigma_11}(t), X_{sigma_13}(t) ),

kappa_hat_32(e) = K(e/32)  if 32 | e and 1 <= e/32 <= 14,
                = 0        otherwise.
```

## 2. The generator theorem

The proved law is `selectorRootedMaximum(t) = K(t)` for `1 <= t <= 14`, obtained
by direct equality of the five-law generator with the exhaustive 68,896-edge
atlas maximum (`structural_generator_matches_exhaustive_selector_atlas`).  The
central and cross-pattern envelopes are:

| `t`            | 1 | 2  | 3 | 4   | 5 | 6    | 7  | 8    | 9   | 10  | 11 | 12 | 13 | 14 |
|----------------|--:|---:|--:|----:|--:|-----:|---:|-----:|----:|----:|---:|---:|---:|---:|
| `E(t)`         | 0 | 49 | 0 | 441 | 0 | 1225 | 0  | 1225 | 0   | 441 | 0  | 49 | 0  | 1  |
| `max_i X_i(t)` | 0 | 0  | 0 | 0   | 0 | 10   | 60 | 108  | 210 | 168 | 45 | 11 | 3  | 0  |
| `K(t)`         | 0 | 49 | 0 | 441 | 0 | 1225 | 60 | 1225 | 210 | 441 | 45 | 49 | 3  | 1  |

At the four exceptional odd deficiencies the coefficient sums are

```text
X_{sigma_7}(7)  = 60  = C(5,2) C(6,1)              (one term),
X_{sigma_9}(9)  = 210 = C(8,4) C(3,1)              (one term),
X_{sigma_11}(11)= 45  = 15 + 30                    (two terms),
X_{sigma_13}(13)= 3   = C(3,1)                      (one term).
```

Point form: `deficiency_generator_matches_atlas_cap_on_contract` checks the list
equality `(kappa_hat_32(34),...,kappa_hat_32(479)) = (cap(34),...,cap(479))`
against the resolved selector cap on all 446 deficiencies, with every off-lattice
value zero, the explicit zeros at `e = 96, 160`, and the exceptional positive
values `kappa_hat_32(224,288,352,416) = 60,210,45,3`.

## 3. Signature semantics

Each signature `(a,b,c,f,d)` is not fitted: it is extracted from one explicit
oriented atlas edge by the predecessor coordinate categories, and
`exceptional_sources_extract_signatures` proves the extraction.  The categories
are:

- `a` (`anchorOne`): partner-zero coordinates where the anchor selects one block;
- `b` (`anchorBoth`): partner-zero coordinates where the anchor selects both blocks;
- `c` (`zeroZero`): partner-zero coordinates where the anchor selects neither block;
- `f` (`fixedRemoved`): deficiency already forced outside those three categories; and
- `d` (`partnerDoubled`): zero-pairs doubled by the partner selector.

`exceptional_sources_are_atlas_edges` proves each of the four sources is a
member of `allPatternPairs` (the last three stored in the opposite canonical
orientation, which the exhaustive computation scans).  The coefficient law is
exactly the binomial expansion of the atlas cross-count formula, so the four
sources give valid lower candidates while direct equality with the exhaustive
computation supplies the upper half.

## 4. Irredundancy

The four signatures are irredundant.  Removing the signature responsible for
`t = 7, 9, 11, 13` lowers the corresponding value from `60, 210, 45, 3` to
`45, 136, 28, 0`, respectively (`exceptional_signatures_irredundant`, kernel
checked).  No proper subset of the four reproduces the spectrum.

## 5. Honest scope

This is an equality of selector-cap functions, proved at the finite
selector-atlas level.  It is not the deployed support inequality `s_e <=
kappa_32(e)`.  Deployed transport, deployed collision laws, and
off-remainder statements are outside this packet's scope.  In particular, at
`e = 224` the deployed floor and the selector value stay separate: `s_224 >=
40` is a distinct deployed witness, while `60` is the exact selector-model
value, and no `s_224 <= 60` is claimed.

## 6. Routes killed

1. **Central / T64-only generator.** `E(t)` is zero at `t = 7, 9, 11, 13`, while
   the exact values are `60, 210, 45, 3`; the central binomial law alone cannot
   produce the odd shells.
2. **Three-signature exceptional generator.** Each of the four cross-pattern
   signatures is necessary; the deletion losses `45, 136, 28, 0` are kernel
   checked.
3. **A single flat cap as a spectrum law.** The value `1225` is attained at
   `t = 6, 8`, but a flat cap hides the exact zeros, the odd-shell structure,
   and the small tail `49, 3, 1`.

## 7. Kernel-checked evidence

Package `experimental/lean/m31_selector_spectrum` (namespace
`M31SelectorSpectrum`, Lean `v4.31.0`, stdlib only, self-contained -- no
external `require`).  Fourteen `native_decide` theorems, each followed by
`#print axioms`:

```text
M31SelectorSpectrum.Atlas.selector_rooted_spectrum_exact          -- 68896 edges + spectrum
M31SelectorSpectrum.Atlas.selector_e224_prediction                -- selectorRootedMaximum 7 = 60
M31SelectorSpectrum.SpectrumGenerator.exceptional_sources_are_atlas_edges
M31SelectorSpectrum.SpectrumGenerator.exceptional_sources_extract_signatures
M31SelectorSpectrum.SpectrumGenerator.exceptional_signature_values
M31SelectorSpectrum.SpectrumGenerator.central_pattern_spectrum_exact
M31SelectorSpectrum.SpectrumGenerator.exceptional_envelope_spectrum_exact
M31SelectorSpectrum.SpectrumGenerator.structural_generator_matches_exhaustive_selector_atlas
M31SelectorSpectrum.SpectrumGenerator.structural_generator_prints_atlas_spectrum
M31SelectorSpectrum.SpectrumGenerator.exceptional_signatures_irredundant
M31SelectorSpectrum.DeficiencyLaw.deficiency_generator_matches_atlas_cap_on_contract
M31SelectorSpectrum.DeficiencyLaw.off_lattice_contract_is_zero
M31SelectorSpectrum.DeficiencyLaw.explicit_zero_predictions
M31SelectorSpectrum.DeficiencyLaw.exceptional_point_deficiency_values
```

Axiom census (verified from the `#print axioms` output of a green `lake build`):
ten of the fourteen theorems report only their own generated `native_decide`
axiom.  Four also report `propext`: the two replayed atlas theorems
`selector_rooted_spectrum_exact` and `selector_e224_prediction`, and the two
computed list equalities `structural_generator_matches_exhaustive_selector_atlas`
and `deficiency_generator_matches_atlas_cap_on_contract`.  No `sorry`, `admit`,
custom axiom, or Mathlib import is used.

## 8. Replay

- Lean target: `lake build` in `experimental/lean/m31_selector_spectrum`
  (builds all fourteen theorems and prints the axiom censuses).
- Independent recompute (stdlib, well under a minute):
  `python3 experimental/scripts/verify_m31_selector_spectrum_generator.py --check`
  recomputes `E`, all `X_sigma` two independent ways (full polynomial expansion
  and the closed triple-sum), the pointwise-max equality against the shipped
  spectrum, the envelope, the exceptional values, the single-/few-term
  reductions, and the deletion losses; `--tamper-selftest` returns exit 0 iff
  every seeded mutation is caught.
