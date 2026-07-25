# The sharp scalar depth-32 flatness conjecture on the pinned Mersenne-31 quotient profile

**Status:** COMPLETE formulation packet; conjecture open; finite consistency and compiler shard kernel-checked.

**Request worked from:** Formulate one exactly quantified maximum-versus-average depth-32 prefix-fiber conjecture whose truth closes the coefficient-four sub-crossover band on the pinned M31 instance and whose falsity certifies a new floor or kills the route.

## Abstract

For the pinned punctured Chebyshev quotient domain of size 1,022 over
\(\mathbb F_{2^{31}-1}\), let \(F_\eta\) be the 479-supports whose monic
locator has prescribed first 32 nonleading coefficients, and let \(d_e(A)\)
count same-fiber neighbors of an anchor \(A\) at rooted deficiency \(e\). This
paper proposes the sharp scalar conjecture

\[
\forall\eta\ \forall A\in F_\eta\ \forall e\in[33,213],
\qquad d_e(A)\le1233.
\]

The integer 1,233 is forced by a kernel-checked packet of 1,225 full-`T_64`
triple swaps plus eight mixed neighbors at deficiency 192. It is also small
enough that the existing coefficient-four compiler totals 15,007,628, leaving
1,769,587 below the deployed budget 16,777,215. The statement explicitly
allows off-lattice and ragged exchanges, is confined to the actual quotient
domain, and is pointwise rather than moment-derived. A minimal refutation is a
certificate containing one target, one anchor, one band deficiency, and 1,234
pairwise-distinct full supports with all 32 locator coefficients checked. Such a
refutation raises the uniform intercept floor; a packet of 5,192 neighbors
kills the coefficient-four scalar route outright.

## 1. Frozen object

Put

\[
p=2^{31}-1=2,147,483,647.
\]

Use the pinned quotient labels

\[
q_r=2^{-2047}\operatorname{Re}(g^{r2^{19}})\pmod p
\qquad(r=1,3,\ldots,2047),
\]

with \(g=(1717986917,1288490189)\), and delete the labels represented by `1`
and `3`. The resulting domain \(Q'\) has 1,022 points. For a canonical
479-support \(E\subset Q'\), write

\[
V_E(Y)=\prod_{q\in E}(Y-q)
\]

and let \(\operatorname{pref}_{32}(V_E)\in\mathbb F_p^{32}\) be the first
32 nonleading monic coefficients. Define

\[
F_\eta=\{E\in\tbinom{Q'}{479}:
\operatorname{pref}_{32}(V_E)=\eta\},
\]

\[
\delta(A,B)=479-|A\cap B|,
\qquad
d_e(A)=|\{B\in F_\eta:B\ne A,\ \delta(A,B)=e\}|.
\]

Newton rigidity excludes distinct same-prefix pairs at deficiencies 1 through
32. The coefficient-four sub-crossover band is \(33\le e\le213\); the first
shell with positive ambient slack is 214. The global support and target counts
are

\[
M=\binom{1022}{479},\qquad Q=p^{32},
\]

with exact floor and ceiling averages 3,614,119 and 3,614,120.

The row motivating the packet is the M31 LIST stress row over
\(\mathbb F_{p^4}\), at errors 981,129, agreement 1,116,023, target failure
probability \(2^{-100}\), and budget \(B^*=16,777,215\). The present object is
the base-field support-prefix layer, not a received-word or list theorem.

## 2. Current best statement

> **Conjecture C1 (sharp scalar depth-32 band flatness).** For every
> \(\eta\in\mathbb F_p^{32}\), every \(A\in F_\eta\), and every integer
> \(e\) with \(33\le e\le213\),
> \[
> d_e(A)\le1233.
> \]

There are no hidden classification hypotheses. C1 does not require an exchange
to be a union of full `T_64`, `T_32`, or `T_16` classes, does not fix a
canonical remainder, and does not assume Fourier flatness, a finite moment
bound, or a degree-uniform character-sum estimate. It is restricted to the
actual pinned quotient-label domain.

For

\[
H_e=\binom{479}{e}\binom{543}{e},
\]

the integrated census has \(\lfloor4H_e/p^{32}\rfloor=0\) throughout the
band. Thus C1 is precisely the band specialization of the coefficient-four
maximum-versus-average envelope

\[
d_e(A)\le1233+\left\lfloor\frac{4H_e}{p^{32}}\right\rfloor.
\]

The Lean definition
`M31FlatnessConjectureC1.m31Depth32BandFlatnessConjecture` carries C1 as a
universal proposition over duplicate-free lists of certified neighbors. The
conjecture is not asserted by an axiom or theorem.

## 3. Mechanism and consequence if true

The integrated rooted-shell compiler has 447 admissible deficiencies after
depth-32 rigidity and ambient contribution

\[
\left\lfloor\frac{4M}{Q}\right\rfloor=14,456,476.
\]

Consequently C1 gives

\[
1+1233\cdot447+14,456,476
=15,007,628
\le16,777,215,
\]

with reserve

\[
16,777,215-15,007,628=1,769,587.
\]

The scalar boundary is exact:

\[
1+5191\cdot447+14,456,476=16,776,854\le B^*,
\]

whereas

\[
1+5192\cdot447+14,456,476=16,777,301>B^*.
\]

Truth therefore supplies the missing uniform band intercept for the existing
coefficient-four quotient-prefix compiler. It does not by itself establish
first-match survival, a received-word realization, a slope or ray projection,
an ordinary-list bound, or complete M31 row closure.

## 4. Evidence for C1

### 4.1 The sharp certified floor

`M31QuotientT16MixingFloor.Witness.one_thousand_two_hundred_thirty_three_distinct_neighbors`
checks a list of 1,233 pairwise-distinct valid neighbors of one anchor at
deficiency 192 with the same first 32 locator coefficients. The packet consists
of 1,225 full-`T_64` triple swaps and eight additional mixed supports. It proves
\(d_{192}(A)\ge1233\) for that anchor, so every smaller scalar is false. It does
not prove completeness of the shell.

The session theorem
`M31FlatnessConjectureC1.integrated_zoo_consistency_shard` checks that this list
satisfies the exact C1 packet predicate and that its length equals the champion
cap.

### 4.2 Full-class sectors

`M31QuotientBandMixing.Witnesses.rooted_shell_census` checks the full-class
packet sizes 49, 441, and 1,225 at deficiencies 64, 128, and 192. The session
consistency shard checks their exact target, anchor, deficiency, canonicality,
and duplicate-free hypotheses. Each fits C1.

### 4.3 Off-lattice behavior is admitted rather than denied

`M31QuotientBandMixing.Witnesses.mixing_prefix_exact` checks a deficiency-96
pair that agrees through locator coefficient 47 and first differs at 48; 96 is
not a multiple of 64. C1 places no lattice hypothesis on a neighbor, so the pair
is a legal singleton contribution and not a refutation.

### 4.4 The complete-`T_32` theorem has a different unit

`M31FlatnessKeystone.SelectorAtlas.selector_relation_atlas_exact` proves a
fixed-canonical-remainder fiber maximum of 3,432 and nontrivial collision
submaximum 482. The 3,432 quantity totals several rooted shells and is not one
\(d_e(A)\). The session theorem
`M31FlatnessConjectureC1.t32_skeleton_scope_shard` records the type guard

\[
482<1233<3432.
\]

## 5. Evidence against, quarantine checks, and weakest link

The integrated constant-shift comparison-domain packet constructs, at the same
field, domain size, support size, and prefix depth, an explicit domain with a
fiber of 145,422,675. This kills parameter-only and arbitrary-domain flatness.
C1 survives only because it names the pinned Chebyshev quotient domain.

The integrated moment-blind packet gives two abstract occupancies agreeing in
raw and falling moments through order 990 while their maxima fall on opposite
sides of the budget. C1 survives because it is pointwise in the target, anchor,
and shell; no finite unlabelled moment ledger is assumed.

A concurrent green lab packet supplies the kernel-checked theorem
`M31CappedRigidity.M31T16CompletenessS1.RaggedWitness.explicit_ragged_collision`:
an explicit deficiency-192 collision using opposite `T_8` halves inside an
intact `T_16` class, with locator agreement through coefficient 39 and first
mismatch at 40. It proves that ragged finer-scale mechanisms are real, but it
provides one neighbor rather than 1,234 neighbors at one target, anchor, and
shell, so it does not refute C1.

The weakest regime is the known deficiency-192 threshold anchor. Its full-class
sector already supplies 1,225 neighbors, leaving room for exactly eight further
neighbors, and the integrated packet exhibits eight. A ninth mixed neighbor at
that same target and anchor would immediately refute C1. The first adversarial
attack should therefore exhaust or extend the non-full-class deficiency-192
sector, including ragged opposite-half and cross-canonical-remainder relations.

## 6. Exact falsifier and consequence if false

A minimal refutation must print:

1. one integer \(e\in[33,213]\);
2. one target \(\eta\), with all 32 coefficients in `[0,p)`;
3. one canonical anchor, with all 479 representatives;
4. 1,234 pairwise-distinct canonical neighbor supports, each with all 479
   representatives;
5. all 32 quotient-locator coefficients for the anchor and every neighbor,
   matching the target exactly;
6. exact support validity, puncture-avoidance, ordering, cardinality,
   distinctness, non-anchor, and rooted-deficiency checks.

Shell completeness is unnecessary. The Lean predicate
`M31FlatnessConjectureC1.IsMinimalChampionFalsifier` carries this certificate
shape, and
`M31FlatnessConjectureC1.minimal_falsifier_refutes_champion` proves that any
such packet negates C1.

Every minimal falsifier is statement-changing: it raises the uniform scalar
floor from 1,233 to at least 1,234. Any certified packet of at least 5,192
neighbors also kills the coefficient-four scalar-intercept route.

## 7. Kernel-checked shard

The new stdlib-only package proves:

- `M31FlatnessConjectureC1.minimal_falsifier_refutes_champion`;
- `M31FlatnessConjectureC1.integrated_zoo_consistency_shard`;
- `M31FlatnessConjectureC1.t32_skeleton_scope_shard`;
- `M31FlatnessConjectureC1.ambient_average_shard`;
- `M31FlatnessConjectureC1.coefficient_four_compiler_shard`.

The zoo shard uses disclosed `native_decide` on closed support data. The
compiler theorem uses ordinary `decide`. Every theorem has a `#print axioms`
census. The green build log reports no `sorryAx`; the compiler theorem is
axiom-free, while the finite and imported enumeration theorems expose their
native certificate axioms exactly.

## 8. Routes killed or not reopened

- Full-`T_64` classification is false by the deficiency-96 and mixed
  deficiency-192 certificates.
- Parameter-only flatness is false by the constant-shift comparison domain.
- Finite unlabelled moments do not control the maximum by the order-990
  moment-blind pair.
- Coefficient 5 is already dead on the frozen row.
- Newton rigidity ends at deficiency 32 and gives no estimate inside the band.
- The integrated Fourier certificate has \(\Lambda^*=3\), too small for the
  deployed maximum.
- Degree-uniform Weil or character-sum certificates are not used; their
  calibrated route has already been cut.
- The weaker cap 5,191 would bank but is not sharp against the certified floor.
- An adaptive canonical-`T_32` remainder statement remains a possible successor,
  but falsifying it need not change the rooted-shell floor.

## 9. Open questions and natural next step

1. Are the eight known non-full-class neighbors exhaustive at the threshold
   deficiency-192 anchor?
2. Can a cross-remainder defect invariant bound mixed exchanges uniformly over
   all targets and anchors?
3. Can the complete fixed-remainder selector atlas be transported to rooted
   shell degrees without assuming a false full-class classification?
4. If C1 fails below 5,192, does the new family merely raise the floor or extend
   to a full route kill?

The natural next step is a certificate-complete adversarial census at the
threshold anchor: find a ninth mixed deficiency-192 neighbor, or prove the
integrated eight exhaust all non-full-class exchanges after conditioning on the
exact target and anchor.

## 10. References

Lean package:

```text
experimental/lean/m31_flatness_conjecture_c1/
```

Source dossier:

```text
experimental/notes/thresholds/m31_flatness_conjecture_c1.md
```

Concurrent ragged evidence: theorem
`M31CappedRigidity.M31T16CompletenessS1.RaggedWitness.explicit_ragged_collision`.
This packet was read for adversarial overlap but is not imported by the C1
package.

Exact upstream labels used:

```text
def:primitive-q
def:q-row-atom
prop:q-exact-target
lem:newton-equivalence
(RS) in m31_q_rooted_shell_envelope.md
```

Primary source packets:

```text
experimental/notes/thresholds/m31_flatness_keystone_constant_shift_obstruction.md
experimental/notes/thresholds/m31_flatness_keystone_moment_blind_pair.md
experimental/notes/thresholds/m31_t32_skeleton_flatness_keystone.md
experimental/notes/thresholds/m31_quotient_band_swap_census_t16_mixing.md
experimental/notes/thresholds/m31_quotient_t16_mixing_floor.md
experimental/notes/thresholds/m31_q_rooted_shell_envelope.md
```

## 11. Certified stop

This round formulates and stress-tests the keystone; it does not prove it. The
current best statement is C1, with a kernel-checked consistency/arithmetic
shard and a certificate-standard refutation interface. The work stops at the
universal pointwise cap on the pinned quotient domain.
