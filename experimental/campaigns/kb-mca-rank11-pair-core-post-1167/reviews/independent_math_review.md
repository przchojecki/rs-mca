# Independent mathematics review

Date: 2026-08-13

Reviewer role: isolated statement, quantifier, algebra, and boundary auditor

Review type: proof audit / implication-chain audit

Status: **GREEN**

## Statement audited

I audited the three new statements in `experimental/grande_finale.tex`:

1. `thm:mca-nonuniform-support-margin`, asserting the pointwise resource
   bound
   \[
   \sum_{\gamma\in Z}\theta_\gamma\le C_s;
   \]
2. `thm:mca-weighted-pair-core-route-cut`, converting that resource into a
   weighted fixed-minimizing-pair terminal and proving the exact
   core-deficiency multiplicity
   \[
   c_\delta=\left\lfloor\frac{n-m+\delta}{\delta}\right\rfloor;
   \]
3. `prop:kb-rank-eleven-pair-core-terminal`, specializing the result to the
   KoalaBear error-rank-eleven slice and proving both the two row-wise
   concentration terminals and the complete printed-theorem/core-deficiency
   certificate-class wall.

This is a local route-cut audit. It does not audit or authorize an active-v4
payment, KoalaBear closure, or the universal four-rate statement.

## Files/sections read

- `/Users/scott/math_code/AGENTS.md` (ancestor-chain guidance; no closer
  `AGENTS.md` or `AGENTS.override.md` exists in the target worktree);
- `experimental/grande_finale.tex`, especially
  `thm:affine-span-list`, `thm:proper-subspace-mca`,
  `thm:support-transverse-affine-span-mca`, `thm:mca-error-rank-gauge`,
  `prop:kb-post-deletion-affine-error-router`,
  `thm:subsquare-interleaving-collapse`, and the three new statements;
- `experimental/notes/thresholds/kb_mca_rank11_pair_core_route_cut_v1.md`;
- `experimental/campaigns/kb-mca-rank11-pair-core-post-1167/00_contract.md`;
- `experimental/campaigns/kb-mca-rank11-pair-core-post-1167/proofs/nonuniform_theta_pair_route_cut.md`;
- `experimental/campaigns/kb-mca-rank11-pair-core-post-1167/threads/barrier_adversary.md`;
- the dependency and claim registries;
- the primary Python verifier, Sage replays, GF(7) control, and existing
  Wolfram arithmetic-replay memo.

During review I identified three statement-level blockers: a false common-pair
quantifier across two independently optimized cutoffs, a vacuous existential
when the forced load is zero, and an unstated globally fixed minimizer needed
for the cumulative deficiency distribution. The generator repaired all three
in the current source, note, and campaign proof before this verdict. I
re-audited the repaired bytes.

## Dependencies

- **PROVEN / IMPORTED:** exact post-near record selection and reversible
  error-rank gauge from PR #1166 at
  `b67078c7c0254ce9e54e5748634de5133fae98ef`.
- **PROVEN / IMPORTED:** recursive affine-span list bound,
  support-transverse affine-span theorem, and sub-square common-support
  interleaving collapse as pinned by PR #1167 at
  `491ccdf53d54846f5a013b808960645275c64ed3`.
- **PROVEN HERE:** the nonuniform sum-of-margins strengthening. It is not
  inferred by summing the old minimum-margin statement; it follows by
  summing the disjoint ordered-normal-basis ownership counts before taking
  the endpoint maximum.
- **PROVEN HERE:** fixed-pair exception-set disjointness and the resulting
  multiplicity/weight bound.
- **EXACT FINITE CERTIFICATE:** the two KoalaBear optimizations, field guards,
  adjacent cutoff values, unconditional Abel ceiling, and conditional
  resource-coupled ceiling.
- **EMPIRICAL ONLY IN ITS DECLARED SCOPE:** the GF(7)/GF(11) constant-code
  stars. They show that parallel records and the local fixed-pair multiplier
  are genuine; they are not rank-eleven KoalaBear counterexamples.
- **NOT USED:** the literature sweep and Wolfram replay are corroboration,
  not load-bearing proof inputs.

## Parameter dependence

The abstract statements track `n`, `K`, `m=K+w`, affine explanation
dimension `s`, cutoff `tau` (or `J`), field size `|F|`, record threshold `E`,
individual margins `theta_gamma`, fixed-pair core `H`, and deficiency
`delta`. There is no hidden dependence on `T`, `Y`, `L`,
`L_{\bar I}`, `lambda`, `I`, or an asymptotic regime.

The KoalaBear proposition explicitly fixes

\[
(n,K,m,w,B_*)=(2097152,1048576,1116048,67472,
274980728111395087)
\]

and the actual sextic line field `|F|=2130706433^6`. The latter matters:
the sub-square guards are checked in the sextic field, not over the base
prime. The near add-back is exactly `2w=134944`, so an integer line with
more than `B_*` bad slopes leaves at least `E=B_*-2w+1` post-near slopes.

## Proof verification

### Nonuniform resource

For the one fixed affine explanation flat, the zero-normal data `(z,g)` are
global. A zero normal makes its affine incidence equation either identically
true on the flat or identically false. For each parameter point, the first
`s-1` independent extensions retain the common factor
`(w+1)^(overline{s-1})`, while the last extension has its individual lower
bound `theta_gamma`. An ordered independent `(s+1)`-tuple determines at
most one parameter point. Summing therefore gives

\[
(m-g)(w+1)^{\overline{s-1}}\sum_\gamma\theta_\gamma
\le (n-z)^{\underline{s+1}}.
\]

The inherited constraints `0<=g<=z<=K-s`, maximization first at `g=z`, and
the cited successive-ratio sign put the maximum at `z=0` or `z=K-s`. The
second endpoint denominator is indeed
`(w+s)(w+1)^(overline{s-1})=(w+1)^(overline s)`.

### Exact-record pair reconstruction

For a low record `theta_gamma<=tau<w+1`, the truncation in the margin is
inactive. With the fixed minimizer `b_gamma`, the pair
`a_gamma=c_gamma-gamma*b_gamma`, `b_gamma` lies in
`(c_0+C') x C'` and agrees with the identical received pair on at least
`m-tau>K` coordinates. Translation of the first component by `c_0`
preserves the common support, so the ordinary affine-span bound and the
two-column interleaving collapse apply without changing the received line,
slope, support, or explaining data.

For a fixed pair `(a,b)`, on the actual exact `m`-support,

\[
S_\gamma\cap H_{a,b}
=\{x\in S_\gamma:r_1(x)=b(x)\}.
\]

Thus `theta_gamma=|S_gamma\H|>=delta`. Outside `H`, the affine equation
determines at most one finite slope, so exception sets belonging to distinct
slopes are disjoint. If `|H|<m`, division of `n-|H|=n-m+delta` by `delta`
is exact; if `|H|>=m`, setting `delta=1` and using `n-|H|<=n-m` makes the
printed `n-m+1` numerator a safe one-unit overestimate. Hence both the
multiplicity and cutoff-weight inequalities are valid.

The theorem now assumes `(tau+1)E>C_s`, so its existential fixed-pair
conclusion is never invoked with an empty low family or zero forced weight.

### High subranks, cumulative cores, and quantifiers

The high family may span any affine subrank `0<=j<=s`. For `j>=1`, its
direction space is a subspace of `C'`, so minimizing over it cannot reduce
the inherited margins; the support-transverse theorem applies. Rank zero is
separately bounded by `floor(n/(J+1))`. Taking the maximum over all subranks
is therefore necessary and sufficient.

For the cumulative core calculation, one minimizing direction and pair type
is now fixed once for every selected record before any `t` or `J` scan. The
sets counted by `G(t)` are consequently nested. A pair of deficiency at most
`t` agrees with the received pair on at least `m-t`, and monotonicity of
`Q_s(t)` makes the single guard `Q_s(J)^2<|F|` valid for every `t<=J`.
Since `c_delta` decreases, Abel summation gives the stated greedy upper
envelope. Low records and `theta>=J+1` records form a disjoint exhaustive
partition.

The proposition now correctly has a row-wise existential: each cutoff
supplies a fixed pair, but the pairs for `tau=6486` and `tau=1795` need not
coincide.

## Exact arithmetic and controls

Independent exact-integer reconstruction confirmed:

- `C_10=106618568137036225644`;
- at `tau=6486`, `Q=2255946383610`, forced weight `743449148`, at least
  `114624` records, and maximal compatible deficiency `8`;
- at `tau=1795`, `Q=1075288922022`, forced weight `360132809`, at least
  `200632` records, and maximal compatible deficiency `4`;
- the field guard holds at both cutoffs and through the final legal cutoff
  `65810`;
- the unconditional ceiling has unique minimum
  `813929118931913384` at `J=19737`; the adjacent values at `19736` and
  `19738` are strictly larger;
- the resource-coupled ceiling is
  `811958533186703629`, first attained at `J=26033` and constant through
  `J=65810`. The note does not incorrectly claim uniqueness for this
  coupled minimum.

The primary Python verifier passed in normal and optimized modes and rejected
all `6/6` hostile mutations. Both shipped Sage star controls passed. These
calculations are exact official-scale finite arithmetic for the displayed
integers; the small-field stars are only local sharpness controls.

## Layer-cake / dyadic summability

Not applicable. The cutoff partition and Abel summation are finite exact
combinatorial sums, with no dyadic weights or additive asymptotic errors.

## Moment / Markov / Chebyshev

Not applicable. No moment inequality, probability tail, or optimization in
a moment parameter is used.

## Edge cases / notation

- `s>=1` is inherited from the support-transverse theorem; the deployed
  application uses `s=10`.
- `1<=tau,J<=w-1` ensures `m-tau>K` and keeps the margin cap inactive.
- The new positive-load condition handles the empty-low-family boundary.
- Empty high or low portions satisfy their respective upper bounds.
- `delta=1` safely covers both a one-point deficient core and cores of size
  at least `m`.
- Only distinct finite affine slopes are counted. Pair labels, supports,
  minimizers, endpoints, and parallel graph incidences are not substituted
  for slopes.
- The two table rows are independent existential alternatives, not one
  simultaneously satisfying pair.
- Agreement `m`, cutoff `tau`, affine dimension `s`, and error rank eleven
  are not conflated.

## Numerical evidence

The official-row scans cover every legal integer cutoff, using exact big
integers. They certify the displayed finite maxima/minima conditional only
on the proved symbolic inequalities. The GF(7) and GF(11) stars are
toy-scale exact controls and prove no official-rank realization or
asymptotic statement. The abstract certificate-class packing is explicitly
not asserted to be simultaneously Reed--Solomon realizable.

## Verdict

**GREEN - proof obligation appears satisfied with dependencies verified.**

The corrected source proves a genuine local rank-eleven concentration and a
sharp route cut for the declared margin/pair/core certificate class. It does
not pay rank eleven or move the deployed chronology.

## Remaining risks

1. A chronology-correct owner or cross-pair collision theorem for the dense
   `delta<=4`, `>=200632` parallel terminal remains wholly unproved.
2. The cumulative ceiling is a method ceiling, not an actual RS extremizer.
3. Publication still requires the independent certificate/custody review
   and source-build gates specified by the campaign; this mathematics
   review does not substitute for them.

## Minimal next action

Complete the separate certificate/custody review on the repaired bytes. If
that remains GREEN, publish the scoped route cut. The next mathematical
attack must couple different actual minimizing pairs or route dense common
cores to an earlier chronology owner; another scalar cutoff or smaller
fixed-pair multiplier is ruled out by the exact local star control.

**Final status: GREEN.**
