# Final independent source and mathematics review

Date: 2026-08-13
Reviewer role: isolated source/mathematics reviewer; not the generator
Exact parent: `d4d653723f2f82390fd4351476e1926e55fb0caf` (current PR #1165 head)
Canonical packet payload audited: `fb0b78c20b06b1b563eb11cb766aac7deec978547a82ebe91481d23fab3af178`

## Statement audited

I audited the post-#1165 successor consisting of:

1. `thm:support-transverse-affine-span-mca`, which replaces the final
   global occupancy factor in the proper-subspace MCA count by the exact
   selected-support factor
   \[
   \theta=\min\!\left\{w+1,
      \min_{\gamma\in Z,\,b\in C'}
      |\{x\in S_\gamma:r_1(x)\ne b(x)\}|\right\};
   \]
2. `thm:mca-error-rank-gauge`, the reversible arbitrary-rank codeword
   gauge sending error affine rank `a` to explanation affine rank `a-1`;
3. `prop:kb-post-deletion-affine-error-router`, the conditional direct
   KoalaBear slope bound through selected error rank nine and the exact
   rank-10/11/12 direction-exception terminals.

The proposition is in units of distinct finite affine bad slopes on one
actual received line. It is conditional on the separately pinned intrinsic
near-rational theorem `|N|<=2w`; it is not an active-v4 atom or a KoalaBear
closure.

## Files/sections read

- `agents.md`, including the current workboard and exact nonbankability rules.
- `experimental/grande_finale.tex`, especially
  `thm:proper-subspace-mca`,
  `thm:support-transverse-affine-span-mca`,
  `thm:mca-error-rank-gauge`,
  `thm:sparse-direction-punctured-johnson-mca`,
  `thm:near-johnson-centered-gram`,
  `thm:mean-centered-gram-list`,
  `thm:full-explanation-lifted-rank-dichotomy`, and
  `prop:kb-post-deletion-affine-error-router`.
- `experimental/notes/thresholds/kb_mca_support_local_theta_and_error_rank_router_v1.md`.
- `experimental/data/certificates/kb-mca-support-local-theta-router-v1/{README.md,manifest.json}`.
- The Python, Sage, FLINT, and Wolfram replay sources for this packet.
- The PR #1165 proper-subspace, full-rank-gauge, punctured-Johnson, and
  centered-Gram verifier sources.
- PR #1160 commit `c5f4ea7a0c78828c901ae5f3428894a8b2e2806b`, especially the
  two-anchor near-rational proof and its exact `2w` scope.
- Campaign contract, frontier map, controls, dependency ledger, claim
  registry, and review registry.

Ancestor guidance was `math_code/AGENTS.md` plus this worktree's
`agents.md`. No sibling override was used as authority.

## Dependencies

| Dependency | Classification | Audit result |
|---|---|---|
| PR #1165 proper-subspace compiler | IMPORTED / PROVEN | Replayed; its lower-dimensional normal-flat count and endpoint optimization are the correct base for the local refinement. |
| Reed--Solomon root bound and MDS generalized weights | PROVEN | Used with exactly the stated dimensions; no hidden field-size or asymptotic hypothesis. |
| PR #1165 full-explanation lifted-rank dichotomy | IMPORTED / PROVEN | Compatible and sharper at explanation rank `K`; the new gauge is a genuine arbitrary-rank existence theorem rather than a conflicting classification. |
| PR #1165 punctured-Johnson, near-Johnson Gram, and mean-centered Gram continuations | IMPORTED / PROVEN | Separate sparse-direction routes. They neither imply nor conflict with the support-local `theta` theorem. Their exact verifiers passed. |
| PR #1160 intrinsic near-rational theorem | IMPORTED / PROVEN | The source proof gives at most `2w` near-rational support-wise bad slopes when `w>=1` and `3w<=n-k`. KoalaBear satisfies these guards: `3w=202416<=1048576`. |
| Exact integer thresholds and ceilings | CERTIFIED EXACT | Independently replayed in Python/Sage/FLINT; details below. |

## Mathematical audit

### 1. Support-local normal count

The proof repairs exactly the failed last-normal step and does not reuse the
refuted factor `w`.

- For an incident normal span of dimension `j<s`, the MDS generalized-weight
  argument gives occupancy at most `K-s+j`; an exact `m=K+w` support thus
  leaves at least `w+s-j` choices. These factors are
  `(w+1)^(overline{s-1})`.
- At dimension `s`, a zero slope coordinate in the annihilator gives the
  ordinary root-bound factor `w+1`. A nonzero slope coordinate gives the
  actual direction `b in C'`, and the selected support contributes at least
  `theta` normals outside the span.
- Pair noncontainment proves `theta_0>=1`: equality `r_1=b` on the identical
  support would make `(c_gamma-gamma b,b)` a simultaneous explanation.
- With `z` zero normals and `g<=z` identically incident zero normals, each
  selected parameter owns at least
  \[
     (m-g)\theta(w+1)^{\overline{s-1}}
  \]
  ordered full-rank tuples. A full-rank tuple determines at most one
  parameter point.
- For fixed `z`, the worst case is `g=z`. The consecutive-ratio sign is
  `n-(s+1)m+sz`, which is increasing in `z`; hence the maximum is at
  `z=0` or `z=K-s`. These endpoints are exactly the two printed terms.

This argument covers `s=1` (empty rising product), `s=K` (the zero-normal
interval has only `z=0`), and nonempty finite `Z`. I found no hidden
maximal-support or genericity assumption.

### 2. Exact comparison `theta>=L`

For every selected exact `m`-support and every `b in C' subset C`,
\[
 |\{x\in S_\gamma:r_1(x)\ne b(x)\}|
 \ge \operatorname{wt}(r_1-b)-(n-m)
 \ge e-(n-m).
\]
Together with pair noncontainment this gives
`theta_0>=max(1,e-(n-m))=L`. Interpolation on `K` coordinates gives
`e<=n-K`, so `e-(n-m)<=m-K=w`; consequently the cap at `w+1` cannot lower
`theta` below `L`. The statement `theta>=L` is therefore correct, including
the boundary `e-(n-m)<=1`.

### 3. Arbitrary-rank gauge and the parent full-rank theorem

Same-support noncontainment implies `r_1 notin C`. Therefore
\[
 (\delta,c)\longmapsto \delta r_1-c
\]
is injective on the lifted difference space `E`. Its image is exactly the
error-difference span, so `dim E=a`. The slope projection is nonzero; after
choosing `(1,b) in E`, the map `(delta,c) -> c-delta b` has image equal to
the kernel of that projection and dimension `a-1`. The displayed error
identity proves preservation of the finite slope, error word, exact support,
and same-support containment predicate in both directions.

At full explanation rank `K`, projection of `E` onto `C` is surjective, so
`dim E` is `K` or `K+1`. The new theorem then reproduces the existence
outcomes `K-1` and `K`; PR #1165's theorem remains strictly sharper because
it classifies every gauge. There is no duplicated or contradictory full-rank
claim.

The gauge changes the literal received-line representative. The packet uses
it only under a direct maximum over all received lines and explicitly refuses
to transport Q/BC/S/A/E ownership. That use is legitimate.

### 4. Intrinsic `2w` composition and exact-record coverage

The partition
\[
 N=\{\gamma\in Z_{\rm bad}:d(r_\gamma,C)\le w\},\qquad
 Z=Z_{\rm bad}\setminus N
\]
is intrinsic, disjoint, and in the same distinct-slope units as the direct
numerator. Thus `|Z_bad|=|N|+|Z|`; no first-match chronology or imported
multiplicity is needed for this direct statement.

The source now also closes the exact-record selection joint. Starting from
a support-wise bad witness `(S,c)` with `|S|>=m`, if every `m`-subset were
pair-contained, adjacent `m`-subsets would share `m-1>=K` coordinates.
Reed--Solomon uniqueness would make their explaining pairs identical, and
connectivity of the `m`-subset Johnson graph would glue one pair over all of
`S`, contradicting badness. Hence every bad slope supplies an exact
same-support-noncontained `m`-subwitness.

The low-rank edge cases are sound:

- with at least two slopes, error rank zero is impossible by injectivity;
- at error rank one, the gauged explanations coincide, and each
  noncontained support has a coordinate with nonzero translated direction;
  the agreement equation makes the slope-to-coordinate selection injective,
  giving `|Z|<=n`;
- for ranks `2` through `9`, the local theorem applies with explanation rank
  `s=a-1<=8` and `theta>=1`.

At ranks `10`, `11`, and `12`, failure of the paying margin is attained on
an actual selected support. If `b_0` is the gauge codeword and `b_1` the
translated direction-space codeword, the inverse terminal is correctly
stated on the original record as
\[
 r_1=b_0+b_1
\]
outside the identical exception set. The exception ceilings are therefore
`12`, `387`, and `12049`, not properties of an untransported gauge
representative.

### 5. Exact constants and floors

The exact computations agree across the replay implementations:

- the `GF(257)` negative control has `87` slopes, old cap `8`, repaired cap
  `759`, full incident normal rank `2`, direction maximum agreement `85`,
  and minimum near-code distance `170`;
- endpoint optimization matches the closed form on `10716` legal small
  profiles;
- KoalaBear explanation rank `s=8`, `theta=1` has cap
  `110390969172173096`;
- adding `2w=134944` gives `110390969172308040`, with signed slack
  `164589758939087047` against
  `B_*=274980728111395087`;
- the least paying margins at `s=9,10,11` are `13`, `388`, `12050`;
- the predecessor totals are respectively
  `285894151677963688`, `275500176064828033`, and
  `274992929018868606`, all strictly over budget;
- the shortened-row automatic wall is rank `9/10`, with subsequent least
  margins `4,49,757,11748`, and rank `14` remains infeasible even at the
  maximum allowed margin.

The verifier's `minimum_margin` uses the correct strict rational condition
for `floor(raw/theta)<=B`; I found no ceiling/floor or off-by-one defect.

### 6. Retractions, scope, and nonclaims

The source retracts only the former payments derived from the false
ordered-basis denominator. It then labels the new result as a distinct,
conditional post-deletion wall. It does not revive the stale unconditional
rank wall.

The note, manifest, README, workboard, and source agree that:

- active-v4 ledger movement is exactly zero;
- the conditional `2w` composition is a direct slope theorem, not a
  chronology-correct deployed atom;
- the 31-slope reserve is not used;
- ranks at least `13` remain unpaid;
- KoalaBear is not closed;
- no universal Prize result is claimed.

These nonclaims are honest. The parent centered-Gram continuations extend a
different sparse-direction support interval and create no overlap conflict.

The focused delta from parent `07546f903` to `d4d653723` is also sound. For
the mean-centered incidence Gram matrix `H=BPB^T`, positivity and
`rank(H)<=n-1` are exact. The endpoint-chord inequality for each
off-diagonal entry has slope `c-2A^2/n<=0`; combining it with
`1^T H 1>=0` gives the printed trace-square bound. The trace-rank inequality
then yields the denominator `A^2 T/n^2`. For the sparse-direction profile,
the suffix closure `B_h=min_{v>=h} C_v` is nondecreasing and Abel summation
with the decreasing owner weights `floor(e/h)` gives the stated profile.
This shifts only the parent sparse-direction endpoints to `e<=64047` on
KoalaBear and `e<=65454` on Mersenne-31. It changes no hypothesis, normal
count, gauge map, threshold, or terminal in the support-local successor.

## Parameter dependence

The abstract local theorem is finite and exact in `(n,K,m,w,s,theta)` with
`m=K+w`, `w>0`, and `1<=s<=K`. The KoalaBear proposition specializes to
the printed exact row. There is no dependence on `T`, `Y`, layer index `h`,
asymptotic constants, or an undeclared field-size limit. The only external
conditional input is the explicitly pinned `2w` theorem with its checked
guards.

## Layer-cake / dyadic summability

Not applicable. There is no level-set integration or additive dyadic error.

## Moment / Markov / Chebyshev

Not applicable. There is no moment inequality or probabilistic tail
optimization.

## Edge cases / notation

Checked: `s=1`, `s=K`, `|Z|=1`, error ranks `0` and `1`, exact versus
at-least-`m` witness supports, the `theta=w+1` cap, the boundary
`e-(n-m)<=1`, and maximum feasible shortened-row margins. Agreement
`m=1116048` is not confused with an error rank or slice parameter. The
proposition consistently uses code dimension `k=1048576` in the external
`3w<=n-k` guard.

## Numerical evidence and replay

The finite proof does not rely on numerical extrapolation. The `GF(257)`
fixture is a toy-scale falsification/regression control only. Exact deployed
integer arithmetic is certificate evidence, not a substitute for the
symbolic proof.

Checks run against the final parent included:

- normal and `python3 -O` canonical verification: PASS;
- hostile mutation suite: PASS, `32/32`;
- independent Sage replay: PASS;
- independent FLINT replay: PASS;
- parent proper-subspace verifier: PASS;
- parent full-rank gauge verifier: PASS;
- parent punctured-Johnson verifier: PASS;
- parent near-Johnson centered-Gram verifier: PASS;
- parent mean-centered Gram verifier: PASS (`109` checks and `2/2`
  mutations);
- campaign actionable audit: PASS;
- `git diff --check`: PASS;
- TeX Live compilation to `/tmp`: PASS, 100 pages.

The configured Wolfram Cloud replay could not be rerun by this reviewer
because the account returned `Insufficient credits`. Its script is
non-load-bearing for the proof, and the exact arithmetic was independently
reproduced by Sage and FLINT. Custody review should record this unavailable
trust base rather than infer a fresh Wolfram pass.

## Verdict

**GREEN - the source-level mathematical obligations audited here are
satisfied.**

The support-local theorem, `theta>=L`, arbitrary-rank gauge, intrinsic `2w`
composition, inverse-gauge exception terminals, exact ranks/ceilings, and
scope/nonclaims are all correct on the exact parent. No mathematical repair
is required before independent custody review and upstream handoff.

## Remaining risks

- This theorem does not identify or preserve v4 first-match owners; zero
  deployed ledger movement is essential.
- The rank-10/11/12 direction-exception families and rank-at-least-13 family
  remain genuine open terminals.
- Final release custody must update review-status metadata after this memo
  without changing the frozen theorem, and must rerun canonical hashes after
  any packet-file change.
- A fresh Wolfram execution remains unavailable until cloud credits are
  restored; this is an evidence-redundancy issue, not a proof gap.

## Minimal next action

Complete the separate custody review, regenerate only review/custody metadata
and canonical hashes if needed, rerun normal/optimized/tamper checks, and then
hand the GREEN theorem packet to upstream. The next mathematical attack is the
actual-record direction-exception forest at error ranks `10--12`, with rank
`>=13` retained as a separate terminal.

**GREEN**
