---
workboard_item: M1
row: Mersenne-31 list at 2^-100
object: LIST
target_epsilon: 2^-100
agreement: 1116023
B_star: 16777215
direct_statement: "On the pinned c=2048, (u,v)=(0,1) quotient profile, a size-stratified refinement of the sharp fixed-remainder cap gives |F_eta| <= 1716*r(eta) + 5577 for every depth-32 locator-prefix target eta, where r(eta) counts the canonical T_32 remainders represented in the fiber. Consequently |F_eta| > 16777215 forces r(eta) >= 9774, raising the necessary remainder count from the previously recorded 4889. Separately, metric-and-remainder information alone cannot decide the row: there is an abstract prefix map at the exact cardinalities with a fiber of 10^9 supports that still satisfies the Newton gap, a uniform in-band shell cap, and a canonical-remainder contribution cap of 1."
architecture: DIRECT_PINNED_C2048_U0_V1_QUOTIENT_PROFILE
partition_digest: "N/A; support-level pinned quotient profile, no first-match ledger atom assigned"
atom_or_cell: Q / PINNED_QUOTIENT_PREFIX_FIBER / CANONICAL_T32_REMAINDER
quantifier: "Uniform over every target eta in F_p^32 for the stratified bound and its corollary; existential for the abstract route-cut map, which is a counterexample to a class of arguments and not a statement about the pinned map."
projection_and_unit: "Canonical 479-subsets per first-32 quotient-locator coefficient target, stratified by canonical T_32 remainder; no received-word, codeword, ray, slope, or first-match projection."
claimed_bound: "|F_eta| <= 1716*r(eta) + 5577, hence 1716*9773 + 5577 = 16776045 <= 16777215 and 1716*9774 + 5577 = 16777761 > 16777215, so an unsafe target needs at least 9774 canonical remainders. This is a necessary condition on any unsafe target and a conditional upper bound on |F_eta| given r(eta); it is not an unconditional upper bound on |F_eta|, establishes no uniform shell cap, and moves no ledger term. Standing of the inputs: the three selector-atlas facts the stratified inequality consumes are already integrated and kernel-checked upstream, and its derivation from them is reproduced in the note; the nonconstructive abstract map behind the route cut is the one input this packet carries rather than checks."
status: PROVED
impact: ROUTE_CUT
falsifier: "A fixed remainder in selector strata m=0..7, m=8..9, m=10..11 or m=12..13 contributing more than 482, 495, 1287 or 3003 respectively; one m=14 remainder contributing more than 3432, or two represented m=14 remainders for one target; two m=12 or three m=13 remainders each contributing more than 1716; a target whose directly enumerated remainder contributions violate the stratified inequality; an unsafe pinned target represented by at most 9773 canonical remainders; or, for the route cut, failure of the displayed selection or colouring inequalities."
replay: "cd experimental/lean/m31_remainder_barrier && lake clean && lake build; stdlib-only Lean package, no script is shipped, and every theorem carries a #print axioms census in M31RemainderBarrier/Barrier.lean. The stratified derivation and the abstract route-cut construction are stated with their hypotheses in the note; the Lean layer kernel-checks the exact arithmetic that follows from them."
---

# M31 canonical-remainder barrier: an unsafe target needs at least 9,774 remainders

## 0. Verdict

```text
STRATIFIED BOUND       = |F_eta| <= 1716*r(eta) + 5577       for every target
BARRIER                = |F_eta| > 16,777,215  ==>  r(eta) >= 9,774
PREVIOUS NECESSARY N   = 4,889 remainders (sharp fixed-remainder cap, 3,432 each)
BOUNDARY               = 1716*9773 + 5577 = 16,776,045  (1,170 under B*)
                         1716*9774 + 5577 = 16,777,761  (546 over B*)
ROUTE CUT              = metric-and-remainder information alone cannot decide the row
ROW LEDGER MOVEMENT    = 0
```

## 1. Frozen object

The row, field, generator, punctures and support conventions are those of the pinned
`c = 2048`, `(u,v) = (0,1)` quotient profile: `p = 2^31 - 1`, punctured domain `Q'` with
`|Q'| = 1022`, canonical supports of size `479`, depth-32 locator prefix, budget
`B* = 16,777,215` at agreement `1,116,023`. Deleting every complete intact `T_32` fiber from a
support leaves its **canonical remainder**; `r(eta)` denotes the number of distinct canonical
remainders represented in `F_eta`, and `r_m(eta)` the number of those whose selector stratum is `m`.

The integrated sharp cap states that a fixed remainder and a fixed target admit at most `3,432`
supports. That value is exactly `C(14,7)`, the number of ways to choose which seven of the fourteen
intact `T_32`-pair classes lie inside the support, and the strata coefficients below are binomial in
the same family: `495 = C(12,4)`, `1287 = C(13,5)`, `1716 = C(13,6)`, `3003 = C(14,6)`,
`3432 = C(14,7)`.

## 2. The stratified compiler

**Theorem (size-stratified canonical-remainder compiler).** For every target `eta`,

```text
|F_eta| <=  482*sum_{m=0}^{7} r_m(eta)
          + 495*(r_8 + r_9)
          + 1287*(r_10 + r_11)
          + 1716*(r_12 + r_13)
          + 7293,
```

and moreover, for a fixed target: at most one represented remainder has `m = 14`; among the `m = 12`
remainders at most one contributes more than `1,716`; among the `m = 13` remainders at most two do;
and every contribution above `1,716` equals `3,003` or `3,432`.

**Inputs, all integrated.** The exact pinned `T_32` block decomposition; the canonical-remainder
definition; and three selector-atlas facts, each of them already proved and kernel-checked in the
integrated sharp `T_32` skeleton keystone rather than assumed here — a single compressed pattern has
multiplicity `binom(z,j)` for one binomial coefficient; the nontrivial compressed collision graph is
a matching, since its `137,792` endpoints are pairwise distinct; and the largest nontrivial
fixed-size collision fiber is `20 + 462 = 482`, at selector size `15`. The same keystone supplies the
sharp cap `3,432` and the threshold `4,889` cited above, and its Lean package discloses
`native_decide`; this packet inherits that disclosure for those inputs and uses none of its own.

**Corollary (the `9,774` barrier).** Every stratum coefficient is at most `1,716`, and the
exceptional contributions above `1,716` are limited to one `m = 14` remainder at `3,432`, one
`m = 12` remainder and two `m = 13` remainders at `3,003`. Bounding each represented remainder by
`1,716` and charging the exceptions separately gives the constant

```text
(3432 - 1716) + 3*(3003 - 1716) = 1716 + 3861 = 5577,
```

which is also `7293 - 1716`, the stratified constant with one `1,716` absorbed into `r(eta)`. Hence

```text
|F_eta| <= 1716*r(eta) + 5577
```

for every target, and therefore

```text
1716*9773 + 5577 = 16776045 <= 16777215      (1170 under budget)
1716*9774 + 5577 = 16777761 >  16777215      (546 over budget)
```

so an unsafe target must be represented by at least `9,774` canonical remainders. The previously
recorded necessary count, from the flat cap `3,432` per remainder, was `4,889`; this raises it.

## 3. Route cut: metric and remainder information are not enough

There is an abstract surjective prefix map at the exact cardinalities of the pinned problem
possessing a fiber of `10^9` supports while still satisfying, simultaneously, the Newton gap on
deficiencies `1..32`, a uniform in-band shell cap, and a canonical-remainder contribution cap of `1`.
No argument that uses only those three interfaces can therefore decide whether the pinned fiber
respects the budget, whatever numerical values it assigns them.

This strengthens rather than replaces the two integrated obstructions of the same kind: the
same-cardinality comparison domain with a `145,422,675` fiber, and the moment-indistinguishable pair
agreeing to order `990`. The missing input is target-labelled locator algebra coupling different
canonical remainders — which is precisely what none of the three interfaces expresses.

## 4. Status of the replacement hypothesis

The previously proposed uniform in-band cap `d_e(A) <= 1233` on `33 <= e <= 213` is refuted; an
explicit target and anchor have `d_192(A) >= 1237`. Its natural replacement

```text
(H_1237)   for every target, every anchor and every e in [33,213],  d_e(A) <= 1237
```

is **open**: the refuting packet forces any uniform intercept to be at least `1,237` but establishes
no upper bound. Conditional on `H_1237`, an unsafe fiber has at most `181*1237 = 223,897` in-band
neighbours, hence at least `16,777,215 - 223,897 = 16,553,318` out-of-band ones, and since
`16,553,318 = 266*62,230 + 138` some shell in `214..479` has degree at least `62,231`. That
conditional is stated here for the record; it is not used by anything above.

## 5. Verification standing — which claims this packet checks and which it carries

This packet is deliberately not uniform in verification standing, and the distinction is printed
rather than left implicit.

The three tiers are distinct and are marked as such in the ledger of §7.

**Tier 1 — integrated and kernel-checked elsewhere:** the sharp cap `3,432`, the collision
submaximum `482`, the matching property, the binomial multiplicity law, and the threshold `4,889`.
These are citations to the integrated keystone, not assumptions of this note.

**Tier 2 — derived here from those inputs, and checked by exact computation as part of preparing
this note:** every arithmetic identity above —
the constant `5577` by both routes, the two boundary evaluations at `9,773` and `9,774` with their
exact slacks `1,170` and `546`, the binomial identities for `495`, `1287`, `1716`, `3003`, `3432`,
and the conditional arithmetic `181*1237`, `16,553,318` and `266*62,230 + 138`. These are the
statements the Lean layer kernel-checks.

The stratified inequality of §2 sits between these two: its inputs are tier 1 and its arithmetic
consequences are tier 2, while the derivation joining them is the round's proof, reproduced above
with its exceptional clauses and its falsifier. That is ordinary standing for a proved packet and is
what `status: PROVED` rests on.

**Tier 3 — carried, not checked here:** the existence of the abstract `10^9` map of §3, a
nonconstructive selection-and-colouring argument with no integrated source. It is stated with its
falsifier so a reader can attack it directly; it is not a finite computation, and this note does not
claim to have re-derived it. `impact: ROUTE_CUT` rests on this section, so the label and its one
carried input are declared together rather than separately.

## 6. Explicit nonclaims

The barrier is a **necessary condition on an unsafe target**, not a proof that the row is safe. It
gives no unconditional upper bound on `|F_eta|`, no uniform shell cap, and no bound on `r(eta)`
itself — closing the row by this route would require showing that no target reaches `9,774`
remainders, which is not attempted here. Nothing above moves a ledger term, and the object
throughout is support counting on one pinned quotient profile: not an MCA numerator, not slopes, not
rays, and not received-line counting.

## 7. Derivation-direction ledger

| printed value | direction | basis |
|---|---|---|
| `p`, punctures, `|Q'| = 1022`, support size `479`, depth `32`, `B*` | frozen | integrated pinned profile |
| fixed-remainder cap `3,432`, collision submaximum `482`, old threshold `4,889` | cited | integrated sharp `T_32` skeleton theorem |
| `495`, `1287`, `1716`, `3003`, `3432` as binomials | derived | direct evaluation |
| binomial multiplicity law, matching property, collision maximum `482` | cited | integrated sharp `T_32` skeleton keystone, kernel-checked there |
| stratified inequality and its four exceptional clauses | derived from the cited inputs | the round's proof, reproduced in §2 |
| constant `5577`, and `5577 = 7293 - 1716` | derived | exact arithmetic, two independent routes |
| `16,776,045`, `16,777,761`, slacks `1,170` and `546` | derived | exact arithmetic |
| barrier `r(eta) >= 9,774` | derived | the two boundary evaluations |
| abstract `10^9` fiber | carried | nonconstructive selection/colouring argument, no integrated source |
| `223,897`, `16,553,318`, shell degree `62,231` | derived | exact arithmetic, conditional on `H_1237` |

## 8. Formalization and replay boundary

The stdlib-only Lean package `experimental/lean/m31_remainder_barrier/` kernel-checks the exact
arithmetic of §2 and §4: the constant `5577` by both routes, the two boundary evaluations with their
comparisons against `B*` and their exact slacks, the binomial values, and the conditional chain
`181*1237 -> 16,553,318 -> 62,231`. Each theorem carries a `#print axioms` census in
`M31RemainderBarrier/Barrier.lean`.

Axiom disclosure, as the build prints it. The package declares `21` theorems and **every one of them
reports `does not depend on any axioms`**. No theorem reports `sorryAx`. Proofs use `rfl` and
`decide` only — **`native_decide` is not used anywhere in this package**, so every check is a kernel
reduction rather than a compiled evaluation. The package is stdlib-only with no dependencies, so the
binomial coefficients are defined inside the module as `binom`. No script accompanies this packet in
any language.
