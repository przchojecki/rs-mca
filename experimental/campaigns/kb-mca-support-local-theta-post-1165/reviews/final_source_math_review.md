# Final independent source and mathematics review

Date: 2026-08-13
Reviewer role: isolated source/mathematics reviewer; not the generator
Exact parent: `b6d30ef4f5ff966665b7672e1780a637509873a4` (current PR #1165 head)
Restacked successor source audited: `experimental/grande_finale.tex` Git blob
`a7de93eedf0288bf81912658a299555aab0c3f46` (SHA-256
`56ef3acaccf6ff45da2fde5c921d914b91b748214f19ac1c263d3638a9fa4b14`).
This memo is intentionally external to the canonical packet hash.  It does
not embed a manifest payload and thereby avoids a circular self-attestation.

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
- Every theorem, corollary, verifier, and independent auditor added in the
  22-commit parent delta `d4d653723..b6d30ef4`, from the terminal-deficit
  affine-line cap through the common-factor base-field descent.
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
| PR #1165 later full-lift line/core/interpolation chain | IMPORTED / PROVEN | The 22-commit restack delta was audited separately.  It extends the Koala full-lift low wall through `e=96150`, pays Mersenne through `e=130236`, and routes—not pays—`e=130237` to a common-factor branch.  It does not consume or alter the local-`theta`, arbitrary-rank-gauge, exact-`m`, or intrinsic-`2w` interfaces. |
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

### 7. Focused 22-commit parent-restack audit

The parent delta `d4d653723..b6d30ef4` contains 22 additive commits and adds
1727 lines to `experimental/grande_finale.tex` without deleting or editing
the proper-subspace theorem or any successor interface.  I checked the
following dependency groups rather than treating the delta as mere status
prose.

- The terminal and top-third affine-line arguments use the exact-layer owner
  weight and the degree-`<K` restriction injection with their printed guards.
  The global top-line synchronization and its total-core cap do not import a
  local-`theta` factor.
- The residue-zero, fixed-cutoff, boundary-line-bank, and recursive-peeling
  routes preserve disjoint slope ownership.  A removed explanation line is
  charged once; distinct line cores meet in at most `K-1`; and the convex
  joint-core charge is maximized by the printed endpoint fill.  The
  exact-layer incidence inequality
  `lambda*h <= e+(lambda-1)u` has the correct direction and ceiling.
- At Mersenne support `e=130237`, weighted interpolation gives kernel
  dimension at least `131175-130237=938`.  The `2705>52^2` comparison
  correctly forces a positive-`(Y,Z)`-degree common factor.  Cofactor Bezout,
  core-incidence Cauchy, weighted-degree dimension counting, base-field
  descent, and the degree-one projective-star split preserve their units and
  guards.  They do **not** pay the projective-star population or classify the
  higher-degree component.

The exact current status is therefore:

- Koala full lift is paid through `e=96150`, leaving
  `96151<=e<=1044238`;
- Mersenne full lift is paid through `e=130236`, leaving
  `130237<=e<=1044241`, with the first support only routed to the common-factor
  branch.

The repaired routing-table prose now distinguishes the proper-subspace/gauge
improvement from these separate full-lift continuations.  None of the 22
commits references the local `theta`, the arbitrary-rank gauge, the exact-`m`
subwitness bridge, the near-rational `2w` add-back, or the Koala conditional
router.  The parent and successor are adjacent but nonoverlapping proof lanes.

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
- all 36 Python verifiers/independent auditors added in the 22-commit parent
  delta: PASS;
- all four compiled constant-memory C interval replays added in that delta:
  PASS;
- the final Koala/Mersenne full-lift mean-centered global-line replay: PASS
  (`548` checks and `4/4` mutations);
- campaign actionable audit: PASS;
- `git diff --check`: PASS;
- TeX Live compilation to `/tmp`: PASS, 118 pages.

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
scope/nonclaims are all correct on exact parent `b6d30ef4`.  The 22 new
parent commits neither duplicate nor invalidate them.  The corrected parent
ranges and the external-attestation custody design are sound.  No further
mathematical repair is required before final packet reseal and upstream
handoff.

## Remaining risks

- This theorem does not identify or preserve v4 first-match owners; zero
  deployed ledger movement is essential.
- The rank-10/11/12 direction-exception families and rank-at-least-13 family
  remain genuine open terminals.
- The separate Mersenne `e=130237` common-factor branch remains unpaid: the
  projective-star population and higher-degree component classification are
  open and confer no Koala ledger credit.
- Any later in-packet change must trigger a fresh canonical reseal; the
  external review memo itself is deliberately outside that hash boundary.
- A fresh Wolfram execution remains unavailable until cloud credits are
  restored; this is an evidence-redundancy issue, not a proof gap.

## Recommended next action

The in-packet registry is resealed and the final normal, optimized, and
`32/32` hostile-mutation checks pass on a clean worktree.  Hand the GREEN
packet to upstream.  The maximal successor attack remains the actual-record
Koala direction-exception forest at error ranks `10--12`, with rank `>=13`
retained as a separate terminal.  The Mersenne common-factor classification
is an independent frontier lane, not a substitute for that attack.

**GREEN**
