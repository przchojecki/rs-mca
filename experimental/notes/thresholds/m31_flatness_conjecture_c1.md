STATE: COMPLETE

---
workboard_item: M1
row: Mersenne-31 list at 2^-100
object: LIST
target_epsilon: 2^-100
agreement: 1116023
B_star: 16777215
direct_statement: "On the pinned c=2048, (u,v)=(0,1) quotient profile, for every depth-32 target eta, every canonical 479-support A in its fiber, and every deficiency 33<=e<=213, the rooted same-prefix degree satisfies d_e(A)<=1233."
architecture: DIRECT_PINNED_C2048_U0_V1_QUOTIENT_PROFILE
partition_digest: "N/A; support-level pinned quotient profile, no first-match ledger atom assigned"
atom_or_cell: Q / PINNED_QUOTIENT_PREFIX_FIBER / SUB_CROSSOVER_BAND
quantifier: "Uniform over every target eta in F_p^32, every canonical 479-subset anchor A of the punctured 1022-label quotient domain with pref_32(V_A)=eta, and every integer deficiency e in [33,213]."
projection_and_unit: "Rooted count of canonical 479-subsets with the same 32 quotient-locator coefficients; no received-word, codeword, ray, slope, or first-match projection."
claimed_bound: "CONJECTURAL d_e(A)<=1233. If true, the proved coefficient-four compiler gives 15007628<=16777215. If false, a minimal 1234-neighbor packet raises the uniform intercept floor to at least 1234; any degree at least 5192 kills the coefficient-four route."
status: CONJECTURAL
impact: LOCAL_ONLY
falsifier: "One e in [33,213], one full 32-coefficient target, one full canonical 479-support anchor, and 1234 pairwise-distinct full canonical 479-support neighbors, all in the punctured quotient domain, all with that target, all at rooted deficiency e, and none equal to the anchor."
replay: "cd experimental/lean/m31_flatness_conjecture_c1 && lake clean && lake build; stdlib-only Lean package, no Python artifact is shipped; every theorem carries a #print axioms census in M31FlatnessConjectureC1/Champion.lean."
---

# M31 flatness conjecture C1: the sharp scalar keystone

## 0. Verdict

```text
CHAMPION                  = uniform rooted-shell cap 1,233
TRUTH CONSEQUENCE         = coefficient-four total 15,007,628
TRUTH RESERVE             = 1,769,587 below B*=16,777,215
KNOWN THRESHOLD PACKET    = certified d_192(A) >= 1,233
MINIMAL FALSIFIER         = 1,234 certified neighbors in one band shell
FALSE CONSEQUENCE         = new intercept floor at least 1,234
ROUTE-KILL THRESHOLD      = one certified shell degree at least 5,192
ROW LEDGER MOVEMENT TODAY = 0
STATUS                    = CONJECTURAL / PROVED SHARD / LOCAL ONLY
```

This dossier contains exactly one champion conjecture. Candidate alternatives
appear only in Section 8 and are explicitly classified as weaker, killed, or
future successors. Every printed mathematical count is classified in the
ledger in Section 10.

## 1. Frozen pinned object

The M31 LIST stress row is over \(\mathbb F_{p^4}\), with target failure
probability `2^-100`, deployed errors `981,129`, agreement `1,116,023`, and
budget `B*=16,777,215`, where

\[
p=2^{31}-1=2,147,483,647.
\]

The support-level quotient object lives over \(\mathbb F_p\). Use the pinned
quotient labels

\[
q_r=2^{-2047}\operatorname{Re}(g^{r2^{19}})\pmod p
\qquad(r=1,3,\ldots,2047),
\]

with the integrated norm-one generator
\(g=(1717986917,1288490189)\). Delete the labels represented by `1` and `3`.
The resulting punctured domain is

\[
Q'=\{q_r:r\text{ odd},\ 1\le r\le2047,\ r\notin\{1,3\}\},
\qquad |Q'|=1022.
\]

For a canonical support \(E\in\binom{Q'}{479}\), put

\[
V_E(Y)=\prod_{q\in E}(Y-q),
\]

and let \(\operatorname{pref}_{32}(V_E)\in\mathbb F_p^{32}\) be its first
thirty-two nonleading monic coefficients. For
\(\eta\in\mathbb F_p^{32}\), define

\[
F_\eta=\{E\in\tbinom{Q'}{479}:
\operatorname{pref}_{32}(V_E)=\eta\}.
\]

For \(A,B\in\binom{Q'}{479}\), define

\[
\delta(A,B)=479-|A\cap B|,
\]

and, for \(A\in F_\eta\),

\[
d_e(A)=|\{B\in F_\eta:B\ne A,\ \delta(A,B)=e\}|.
\]

Newton rigidity gives \(d_e(A)=0\) for deficiencies `1..32`. The frozen
sub-crossover band is `33..213`; the first shell with positive coefficient-four
ambient slack is `214`.

## 2. Champion — exactly one conjecture

> **Conjecture C1 (sharp scalar depth-32 band flatness).** For every target
> \(\eta\in\mathbb F_p^{32}\), every anchor \(A\in F_\eta\), and every integer
> \(e\) with
> \[
> 33\le e\le213,
> \]
> one has
> \[
> \boxed{d_e(A)\le1233.}
> \tag{C1}
> \]

There is no structural side condition. In particular, `(C1)` does not require
an exchange to be a union of `T_64`, `T_32`, or `T_16` classes; does not fix a
canonical remainder; does not average over targets or anchors; and does not
assume a moment, Fourier, or character-sum estimate. The domain is the exact
pinned quotient-label domain, not an arbitrary domain with the same size.

Let

\[
H_e=\binom{479}{e}\binom{543}{e}.
\]

On the band, the integrated shell census gives
\(\lfloor4H_e/p^{32}\rfloor=0\). Thus `(C1)` is exactly the band part of the
maximum-versus-average envelope

\[
d_e(A)\le1233+\left\lfloor\frac{4H_e}{p^{32}}\right\rfloor.
\]

The Lean-carriable form quantifies over every duplicate-free list of canonical
neighbors satisfying the target and deficiency conditions and bounds its length
by `1233`. Since the support universe is finite, this is equivalent to `(C1)`.

The scalar is sharp against current certificates: one integrated anchor has a
list of `1,233` distinct same-prefix neighbors at deficiency `192`, namely
`1,225` full-`T_64` triple swaps and `8` further mixed supports. This proves
only \(d_{192}(A)\ge1233\); shell completeness is not claimed. Consequently
every smaller scalar is already false, while `1,233` remains in the live
compiler window.

## 3. Why truth closes the coefficient-four band

Put

\[
M=\binom{1022}{479},\qquad Q=p^{32}.
\]

The exact floor and ceiling averages are

\[
\left\lfloor\frac{M}{Q}\right\rfloor=3,614,119,
\qquad
\left\lceil\frac{M}{Q}\right\rceil=3,614,120.
\]

The integrated rooted-shell compiler has `447=479-32` admissible deficiencies
and the exact coefficient-four ambient contribution

\[
\left\lfloor\frac{4M}{Q}\right\rfloor=14,456,476.
\]

Substituting the champion cap gives

\[
1+1233\cdot447+14,456,476
=15,007,628
\le16,777,215,
\]

with reserve

\[
16,777,215-15,007,628=1,769,587.
\]

The live scalar edge is exact:

```text
b=5,191: total 16,776,854 <= 16,777,215,
b=5,192: total 16,777,301 >  16,777,215.
```

Therefore truth of `(C1)`, together with the already integrated out-of-band
shell input, closes the coefficient-four quotient-prefix compiler. This is a
local support-level consequence only; first-match survival, received-word
realization, slope projection, and ordinary-list closure remain separate.

## 4. Mandatory consistency pre-check

### 4.1 Full-`T_64` lattice packets

The certified full-class packet lengths at deficiencies `64`, `128`, and `192`
are respectively

\[
49,\qquad441,\qquad1225.
\]

All are at most the champion cap. The largest is below it by `8`.
`M31FlatnessConjectureC1.integrated_zoo_consistency_shard` checks each packet's
length and exact band predicate.

### 4.2 The certified `1,233` packet

For the integrated target and anchor, the `1,225` full-class supports and the
`8` mixed supports are pairwise distinct, valid, at deficiency `192`, and share
all first `32` locator coefficients with the anchor. Their union has length
`1,233`, so it reaches but does not exceed the champion threshold. This is a
lower packet, not an equality or shell-completeness theorem.

### 4.3 The off-lattice deficiency-`96` pair

The integrated off-lattice pair has deficiency `96`, agrees through locator
coefficient `47`, and first differs at coefficient `48`; moreover
`96 mod 64 = 32`. Conjecture `(C1)` permits arbitrary exchange mechanisms and
caps their total rooted multiplicity, so this singleton packet does not refute
it.

### 4.4 Complete-`T_32` skeleton

The complete selector atlas proves a fixed-canonical-remainder fiber maximum
`3,432` and a nontrivial compressed-collision submaximum `482`. The former is a
total fixed-remainder fiber size across several rooted shells, not one
\(d_e(A)\). The session theorem `t32_skeleton_scope_shard` records the exact
type guard

\[
482<1233<3432.
\]

### 4.5 Constant-shift comparison domain

The comparison-domain obstruction has a depth-32 fiber of size `145,422,675` at
the same numerical parameters. It kills any theorem uniform over arbitrary
`1,022`-point domains. It lies outside `(C1)`, whose domain hypothesis is the
pinned Chebyshev quotient set.

### 4.6 Moment-blind pair

The abstract occupancy pair agrees in raw and falling fiber moments through
order `990`, while its maxima lie on opposite sides of the deployed budget; the
unsafe maximum is `16,794,161`. Conjecture `(C1)` is pointwise in target,
anchor, and shell, so no finite unlabelled moment ledger is a hypothesis.

**Pre-check verdict:** no integrated certificate refutes `(C1)`. The certified
deficiency-`192` packet proves that no smaller scalar cap survives the zoo.

## 5. Exact falsifier certificate

A certificate-standard minimal refutation must list:

1. one integer \(e\) with `33 <= e <= 213`;
2. one target \(\eta=(\eta_1,\ldots,\eta_{32})\), printing all `32`
   coefficients as integers in `[0,p)`;
3. one canonical anchor support, printing all `479` odd representatives in the
   punctured domain;
4. exactly `1,234` canonical neighbor supports, each printed in full with all
   `479` representatives;
5. for the anchor and every neighbor, all `32` quotient-locator coefficients,
   each equal to the printed target;
6. exact validity, cardinality, puncture-avoidance, canonical-order, and
   pairwise-distinctness checks;
7. exact checks that no neighbor equals the anchor and that every rooted
   deficiency is the same printed \(e\).

No proof that the list exhausts the shell is required. In Lean this is
`M31FlatnessConjectureC1.IsMinimalChampionFalsifier`, and
`minimal_falsifier_refutes_champion` proves that any such packet negates C1.
Every minimal falsifier raises the certified scalar floor to at least `1,234`.
A packet of at least `5,192` neighbors also kills the coefficient-four scalar
route.

## 6. Proved shard

The nontrivial session shard consists of:

- `integrated_zoo_consistency_shard`: exact `T_64` packet lengths and band
  predicates, the off-lattice deficiency-`96` packet and coefficient boundary,
  and the mixed deficiency-`192` packet of length `1,233`;
- `t32_skeleton_scope_shard`: the fixed-remainder `3,432/482` scope guard;
- `ambient_average_shard`: floor average, ceiling average, and
  `floor(4M/Q)=14,456,476`;
- `coefficient_four_compiler_shard`: champion total, reserve, and the
  `5,191/5,192` edge;
- `minimal_falsifier_refutes_champion`: the exact logical refutation interface.

The conjecture itself is only a `def : Prop`; no theorem or axiom asserts it.
The finite zoo shard uses disclosed `native_decide`; the compiler arithmetic
uses ordinary `decide`. Every theorem has a `#print axioms` census.

## 7. Weakest link

The first attack should target the **non-full-class contribution at the known
deficiency-`192` threshold anchor**. The full-class sector already contributes
`1,225`, leaving room for exactly `8` further neighbors under `(C1)`, and the
integrated packet exhibits `8`. A ninth certified mixed neighbor at that same
target, anchor, and shell would give degree `1,234` and immediately refute the
champion.

Evidence raising confidence would be an exhaustive classification of all
non-full-class deficiency-`192` exchanges for that anchor proving that the
known eight are complete, followed by transport to arbitrary anchors and the
other band deficiencies. Evidence lowering confidence would be any ninth
same-prefix support, especially a ragged finer-scale or cross-canonical-
remainder relation not visible in the current nested-block atlases.

## 8. Ranked alternates

1. **Adaptive canonical-`T_32` remainder cap — KEEP as a successor.** It may
   explain exceptional mass, but an extra remainder could falsify the
   decomposition without raising a rooted-shell floor.
2. **Uniform scalar cap `d_e(A)<=5,191` — KEEP as a weak fallback.** Truth banks,
   but it throws away the entire certified floor-to-window interval.
3. **Every band collision is a union of full `T_64` classes — KILLED.** The
   deficiency-`96` and mixed deficiency-`192` certificates refute it.
4. **A finite unlabelled moment ledger controls the maximum — KILLED.** The
   order-`990` moment-blind pair separates that interface from pointwise
   flatness.
5. **A theorem uniform over all domains with the same cardinalities — KILLED.**
   The constant-shift comparison fiber is already far above budget.

## 9. Calibrated nonroutes not reopened

Coefficient `5` is dead on the frozen row. Newton rigidity is used only for
deficiencies `1..32`; it provides no band estimate. The integrated Fourier
certificate has `Lambda*=3` and does not reach the deployed maximum. Finite
moment methods remain direction-deciders after the moment-blind obstruction.
Degree-uniform character-sum or Weil certificates are not hypotheses of `(C1)`
and are not claimed to prove it.

## 10. Derivation-direction ledger

| Printed datum | Value | Direction | Exact source or operation |
|---|---:|---|---|
| target failure probability | `2^-100` | `FROZEN` | M31 LIST row contract |
| deployed errors | `981,129` | `FROZEN` | M31 LIST row contract |
| agreement | `1,116,023` | `FROZEN` | M31 LIST row contract |
| evaluation length | `2,097,152` | `DERIVED` | errors plus agreement |
| code field | `F_(p^4)` | `FROZEN` | M31 LIST row contract |
| base prime | `2^31-1 = 2,147,483,647` | `FROZEN` | pinned instance |
| quotient template | `c=2,048`, `(u,v)=(0,1)` | `FROZEN` | pinned instance |
| generator | `(1,717,986,917,1,288,490,189)` | `FROZEN / CITED` | imported witness package |
| quotient exponent data | `-2,047`, `2^19`, representatives `1..2,047` | `FROZEN / CITED` | imported witness package |
| unpunctured labels | `1,024` | `ENUMERATED` | `quotient_domain_exact` |
| punctures | `2`, represented by `1,3` | `FROZEN / ENUMERATED` | pinned profile |
| punctured domain size | `1,022` | `ENUMERATED` | `quotient_domain_exact` |
| support size | `479` | `FROZEN` | pinned instance |
| complement size | `543` | `DERIVED` | `1,022-479` |
| prefix depth | `32` | `FROZEN` | pinned instance |
| rigid deficiencies | `1..32` | `PROVED / CITED` | `lem:newton-equivalence` |
| band | `33..213` | `FROZEN / CITED` | lane contract |
| first slack shell | `214` | `DERIVED / CITED` | integrated shell census |
| floor average | `3,614,119` | `DERIVED` | exact division in `ambient_average_shard` |
| ceiling average | `3,614,120` | `DERIVED` | exact division in `ambient_average_shard` |
| budget | `16,777,215` | `FROZEN` | M31 LIST row contract |
| ambient coefficient-four term | `14,456,476` | `DERIVED` | `floor(4M/Q)` |
| admissible shell count | `447` | `DERIVED` | `479-32` |
| full-`T_64` packets | `49,441,1,225` | `ENUMERATED / DERIVED` | exact packets at `e=64,128,192` |
| mixed packet contribution | `8` | `ENUMERATED` | imported full support list |
| certified lower degree | `1,233` | `DERIVED / ENUMERATED` | `1,225+8`; no completeness claim |
| off-lattice data | `e=96`, residue `32`, boundary `47/48` | `ENUMERATED / DERIVED` | direct support and locator checks |
| selector-atlas values | `3,432`, `482` | `ENUMERATED / PROVED` | complete fixed-remainder atlas |
| comparison-domain fiber | `145,422,675` | `ENUMERATED / DERIVED` | constant-shift obstruction |
| moment-blind order | `990` | `DERIVED / PROVED ABSTRACT` | finite-difference construction |
| moment-blind unsafe maximum | `16,794,161` | `DERIVED / PROVED ABSTRACT` | occupancy construction, not RS witness |
| champion cap | `1,233` | `BOUNDED / SHARP CANDIDATE` | minimum scalar surviving certificates |
| minimal falsifier size | `1,234` | `DERIVED` | successor of champion cap |
| champion total | `15,007,628` | `DERIVED` | exact compiler arithmetic |
| champion reserve | `1,769,587` | `DERIVED` | budget minus champion total |
| live upper edge | `5,191` | `DERIVED / BOUNDED` | total `16,776,854` fits |
| first dead scalar | `5,192` | `DERIVED` | total `16,777,301` exceeds budget |
| dead coefficient | `5` | `PROVED / CITED` | integrated compiler result |
| Fourier constant | `Lambda*=3` | `ENUMERATED / CITED` | calibrated route certificate |
| row-ledger movement | `0` | `STATUS` | conjecture and local shard only |

## 11. Validation, nonclaims, and references

Both explicit and default-target builds completed with `13` jobs and no
`sorryAx` dependency. The only warnings are inherited unused-variable lints in
the selector-atlas module.

The new declaration census is:

```text
minimal_falsifier_refutes_champion:
  [propext]
integrated_zoo_consistency_shard:
  [propext, integrated_zoo_consistency_shard._native.native_decide.ax_1_1]
t32_skeleton_scope_shard:
  [propext, Quot.sound,
   M31FlatnessKeystone.SelectorAtlas.selector_relation_atlas_exact._native.native_decide.ax_1_1]
ambient_average_shard:
  [M31QuotientBandMixing.Witnesses.quotient_average_arithmetic._native.native_decide.ax_1_1]
coefficient_four_compiler_shard:
  []
```

Green CI proves compilation and the printed census only. The source-to-Lean
comparison is recorded in `CORRESPONDENCE.md`.

This dossier does not prove `(C1)`, a deployed `U_Q`, a received word, a
first-match survivor bound, a slope/ray projection, an ordinary-list upper
bound, or the M31 row.

Lean package and namespace:

```text
experimental/lean/m31_flatness_conjecture_c1/
M31FlatnessConjectureC1
```

Primary integrated source packets:

```text
experimental/notes/thresholds/m31_flatness_keystone_constant_shift_obstruction.md
experimental/notes/thresholds/m31_flatness_keystone_moment_blind_pair.md
experimental/notes/thresholds/m31_t32_skeleton_flatness_keystone.md
experimental/notes/thresholds/m31_quotient_band_swap_census_t16_mixing.md
experimental/notes/thresholds/m31_quotient_t16_mixing_floor.md
experimental/notes/thresholds/m31_q_rooted_shell_envelope.md
```

Exact upstream labels used:

```text
def:primitive-q
def:q-row-atom
prop:q-exact-target
lem:newton-equivalence
(RS) in m31_q_rooted_shell_envelope.md
```

# OPEN GAP
