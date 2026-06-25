# Experimental Summary

Status: AUDIT / EXPERIMENTAL.

This file summarizes the recent PR wave integrated into `experimental/`. It is
not a proof-status authority and it does not promote any result into the main
papers. The source triage records are:

- `notes/triage/pr-triage-2026-06-17.md`: PRs #1, #2, #3, and #46 through #66.
- `notes/triage/pr-triage-2026-06-18.md`: PRs #67 through #77, with #68 and #76
  superseded by #77.
- `notes/triage/pr-triage-2026-06-18-round3.md`: PRs #79 through #81.
- `notes/triage/pr-triage-2026-06-19.md`: PRs #82 and #84 through #95, with #85 through
  #91 superseded by #93 and PR #95 integrated only as a compact review layer.
- `notes/triage/pr-triage-2026-06-22.md`: PRs #96 through #98, with #96
  integrated only as a compact Cycle84 public replay audit and #97/#98 added as
  experimental F1/L1 notes plus scripts.
- `notes/triage/pr-triage-2026-06-25.md`: PRs #99 through #107, with #100 not
  imported as a raw generated packet and the remaining useful material added as
  experimental L1/M1/M2/F1/L2/X1 notes, verifiers, and Lean scaffolding.

The common policy was: keep Papers A-D unchanged, land new material in
`experimental/`, preserve explicit status labels, and require review before any
promotion into `tex/` or `scripts/`.

The current directory map is in `README.md`. Notes live under `notes/`, scripts
under `scripts/`, compact JSON/CSV fixtures under `data/`, and the Lean stub
under `lean/`.

## Big Picture

The recent PRs are pushing the project from broad corrected-reserve conjectures
toward a finite set of auditable local problems. They do this by turning the
main MCA/list questions into explicit ledgers:

- support-fiber and locator-fiber ledgers for L1;
- support-overlap, quotient-periodic, and occupancy ledgers for M1;
- extension-line and residue-line ledgers for F1;
- line-decoding conversion and separation ledgers for M2;
- full-agreement support intersection ledgers for L2;
- audit/citation/proof-record ledgers for Paper D and Paper C style protocol
  accounting.

The direction is constructive: after Paper A rules out no-slack MCA, the recent
experimental material is trying to identify exactly which obstructions remain
after the corrected reserve is paid. The most useful progress is not one single
large theorem yet; it is the reduction of several vague hazards into named,
script-checkable walls.

## What Was Added

### Latest 2026-06-25 integration

The 2026-06-25 PR round does not improve the Cycle120 numerator
`52,747,567,092`. Its useful estimate changes are endpoint and bridge
improvements:

- `notes/m1/m1_cycle120_standalone_ldsw_proof.md` records a standalone
  source-scoped proof note for
  `LD_sw(RS[F_17^32,H,256],262) >= 52,747,567,092`. Together with the already
  integrated Cycle119 strict-support note, the best current ABF-row obstruction
  remains `epsilon_mca(C,125/256) >= 52,747,567,092/17^32 > 2^-128`, with the
  sharper strict endpoint `delta*_C <= 249/512 < 125/256` if the finite inputs
  are correct.
- `notes/m2/m2_line_decoding_mca_bridge.md` gives the exact normalization
  `epsilon_mca(C,delta)=LD_sw(C,ceil((1-delta)n))/|F|` for the support-wise
  two-source object. This is the clean bridge future papers should use when
  translating between MCA and line-decoding estimates.
- `notes/f1/f1_fixed_rate_extension_counterexample.md` strengthens the F1
  warning: fixed-rate extension-line families have floors on the order of
  `(1-rho)^2/2` for sigma one and
  `(1-rho)^(sigma+1)/(sigma+1)!` at fixed sigma before extension-degree
  dilution.
- `notes/m1/m1_beta_pushforward_spectral_audit.md` finds no hidden growing
  `p^2` beta-pushforward mass in the scanned rows and leaves a conductor-style
  proof target.
- `notes/l2/l2_sharp_target_conjecture.md` sharpens the interleaved-list
  target: charge quotient-core mass diagonally and avoid the naive Cartesian
  numerator.

The rest of the round is proof-program infrastructure: L1 characteristic-zero
prefix reductions, quotient-budgeted locator targets, X1 deep-point and
quotient-reduction bridges, audit notes, standard-library verifiers, and a
small Lean formalization scaffold. No newly imported PR script was run locally.

### Latest 2026-06-22 integration

The 2026-06-22 PR round adds three useful but deliberately scoped items:

- `notes/m1/m1_cycle84_public_replay_audit.md` records the public Cycle84
  replay result. The finite-model computation is
  `m_max(beta)=2`, `Occ(beta)=52,747,567,092`, `D=24`, twelve double fibers, and
  no fibers of size at least three. This is important evidence for the finite
  M1 wall, but it is not a prize-level theorem and was integrated without the
  live workflow, zip bundles, or raw million-line cycle archive from PR #96.
- `notes/f1/f1_deep_point_list_to_ca_mca.md` records a simple-pole deep-point
  identity converting nearby `RS[F,D,k+1]` lists into CA/MCA bad slopes for
  `RS[F,D,k]`. The identity is the durable part; the direct cap application
  remains an audit target before any Paper D promotion.
- `notes/l1/l1_prefix_fourier_orbit_cancellation.md` adds the dual-dilation
  orbit-kernel reduction for the monomial-prefix L1 Fourier lane. It proves
  exact orbit identities and records a route cut: pointwise kernel saving can
  fail even in quotient-free prefix slices.

No PR code was run locally during this triage pass. The new scripts were
inspected as text for dangerous side effects and kept as experimental
reproducibility tools pending explicit reviewer execution.

### Latest 2026-06-23 review

The only changed open PR was Danny's #96 branch, now extended through Cycle120.
It remains non-mergeable as a branch: the new delta adds 678 files and about
201k lines of raw/generated material, including zips, prompt packets, generated
checkers, copied PDF extracts, and new generated proof-record directories.

The useful part is summarized in
`notes/m1/m1_cycle119_strict263_admissibility_review.md`. Cycle119 claims a
two-ended locator transfer

```text
LD_sw(RS[F_17^32,H,256],263) >= 52,747,567,092,
|H|=512.
```

If the proof and the Cycle84 finite computation it depends on are correct, the
row appears admissible under the ABF grand MCA formulation: smooth
power-of-two multiplicative subgroup, rate `1/2`, same-support MCA predicate,
and uniform `gamma` from the code field. The exact ABF PDF should still be
independently checked before any public claim. The right external framing is:
under the printed ABF formulation, this is a prize-facing negative
counterexample candidate for that row, not an accepted prize solution. The
project should ask for a standalone human-readable proof, not
another generated archive.

The follow-up Cycle120 packet is integrated only as
`notes/m1/m1_cycle120_abf_counterexample_candidate.md`. The key clarification is
that Cycle116 agreement `262` already reaches the printed ABF closed threshold
at `delta=125/256`; Cycle119 agreement `263` is a checked strict-ball
strengthening. The counterexample is only to the ABF grand MCA inequality
`epsilon_mca(C,125/256) <= 2^-128` for this one smooth row; equivalently, if
the finite proof chain is correct then Cycle116 gives `delta*_C <= 125/256`
under a supremum convention, and Cycle119 gives the sharper
`delta*_C <= 249/512 < 125/256`. It is not an ordinary list-decoding claim, not
a protocol soundness claim, and not an exact determination of `delta*_C`. The
result remains conditional on the Cycle84/Cycle116 finite inputs and on
independent source verification.

### Latest 2026-06-19 integration

The 2026-06-19 PR round adds five durable experimental bundles:

- `notes/l1/l1_prefix_divisor_count.md` gives the cleanest current L1 split: exact
  quotient-core divisor counts, dilation/localization, arbitrary-word `ImgFib`
  lift, and a Fourier reduction for the aperiodic remainder.
- The Scott L1 consolidation files
  `notes/l1/l1_repaired_locator_theorem_package.md`,
  `notes/l1/l1_syndrome_catalecticant_shells.md`,
  `notes/l1/l1_periodic_support_multisequence_reduction.md`, and
  `notes/l1/l1_quotient_defect_closure.md` turn raw locator fibers into a repaired,
  quotient-defect-aware proof program.
- `notes/m1/m1_residue_line_roadmap.md`,
  `notes/m1/m1_depth_two_lift_window_theorem.md`, and the new depth-two Kummer notes
  update the M1 low-slack ledger. They narrow the remaining wall to explicit
  two-coordinate, line-conic, and conductor targets, but remain conditional or
  experimental where they consume unproved Kummer estimates.
- `notes/l2/l2_interleaved_dilation_constants.md` records dilation symmetry, exact
  aligned quotient-core counts `Quot_mu`, extension-coordinate checks, and
  small arity scans. This is the current best orientation for avoiding the
  trivial Cartesian interleaved-list exponent.
- The NFB frontier JSON data folder adds a compact
  extension-valued deep-hole `F\B` proof-record packet related to Paper D's
  `cor:Fvalued`, while `notes/f1/fable-loop/PRZ_REVIEW_INDEX.md` records the
  selected Cycle 49--57 upper-side MCA route map from PR #95.

This round is useful because it makes future work more modular: L1 has a
quotient/aperiodic divisor ledger, M1 has a named low-slack conductor ledger,
L2 has an aligned interleaving constant target, and the Fable loop now points
future agents to the high-`j` constant-rate replacement instead of the cut
`t=2,j=2` toy regime.

### Locator fibers and L1

The locator-fiber work now has three layers:

- `locator_fiber_sweep/` and `locator_fiber_sweep_analysis/` provide Python
  sweep and analysis tooling.
- `sage_locator_fiber_crosscheck/`, `locator_fiber_crosscheck_report/`, and
  `locator_fiber_local_packet/` add independent Sage/Python cross-checks and a
  reproducible local packet runner.
- `l1_aperiodic_prefix_collision.md` and
  `verify_l1_aperiodic_prefix_collision.py` isolate a concrete `F_17`
  monomial-prefix collision packet and a complement-locator formulation.

This helps the MCA program because the corrected conjecture needs polynomial
control of generated-field locator fibers after quotient obstructions are
removed. The new material gives exact toy computations, catches overstrong
proof routes, and provides a path for separating quotient-periodic fibers from
aperiodic collisions.

What it does not yet give: a general generated-field local-limit theorem in the
fixed-rate corrected-reserve regime.

### M1 support overlap and quotient profiles

The M1 material has become much more ledger-like:

- `m1_average_support_collinearity.md` gives random-line support-collinearity
  estimates and shows covariance is concentrated in high-overlap support pairs.
- `m1_support_coefficient_test.md` records a local coefficient-test route.
- `m1_quotient_periodic_overlap_profile.md`,
  `m1_occupancy_profile_scan.py`, and `m1_support_occupancy_scan.py` give exact
  quotient-periodic and occupancy-profile overlap formulas.
- `quotient_profile.py` and `quotient_profile_dither.py` scan exact quotient
  profiles and dithered dimensions.
- `verify_m1_quotient_remainder_profile.py` and the slack-three verifiers check
  finite quotient/remainder cases.

This pushes toward the MCA conjecture by converting "bad support packing" into
explicit exchange-codegree and quotient-occupancy terms. The quotient terms can
now be budgeted, killed by dimension dithering in some regimes, or separated
from the genuinely aperiodic part of the problem.

What is still missing: a proof that the remaining aperiodic residue-line
packing is small enough above the corrected reserve.

### F1 extension lines and residue-line walls

The F1 work is now the most developed obstruction ledger:

- `f1-extension-witness/` gives an initial extension witness package.
- `f1_extension_slope_sweep.py` scans extension-line slopes.
- `f1_fixed_rate_extension_counterexample.md` proves that an unrestricted
  same-numerator extension-line transfer is false.
- `f1_extension_coordinate_transfer.md` records the reduction of extension-line
  MCA to a multiplication-slice/interleaved base-code problem.
- `f1_arbitrary_anchor_locator_split.md` and
  `f1_monic_anchor_base_core_reduction.md` isolate the arbitrary-anchor and
  monic-anchor residue-line issues.
- `2026-06-17-codex-f1-l1-audit/` and `2026-06-18-fable-loop/` record audited
  route cuts, local checks, and raw model provenance for balanced-denominator
  and line-incidence routes.

This is useful because extension challenges are a likely protocol pressure
point. The recent work makes clear that one cannot simply use a base-field MCA
numerator and divide by a larger extension challenge field. It also narrows the
positive F1 target to a precise residue-line incidence problem.

The current live wall is the arbitrary-anchor balanced-denominator regime. In
the Fable-loop audit, the restricted `t=sigma=2`, `j=2` and parts of `j=3`
line-incidence story are reduced to explicit conic/quadric/rank-determinant
conditions. The unresolved branch is the rank/determinant resonance, especially
the `Q==0` split-cubic case and the extension of these arguments beyond the
small restricted regimes.

### M2 line decoding

The line-decoding material keeps the protocol object honest:

- `m2_line_decoding_mca_bridge.md` translates between MCA bad slopes and
  line-decoding ambiguity.
- `m2_line_decoding_separation.py` gives a tiny separation check showing that
  close-point line decoding and support-wise noncontainment are not identical
  without the right support accounting.

This matters because Paper C style protocols may consume line-decoding rather
than support-wise MCA directly. The experiments help prevent accidental
replacement of MCA, CA, and line-decoding by each other.

What is still missing: a final corrected-reserve line-decoding theorem with
parameters matched to Paper B's MCA formulation.

### L2 interleaving

The L2 material changes the interleaved-list accounting from a product bound to
an intersection-profile problem:

- `l2_interleaved_support_bridge.md` proves a finite support injection and
  full-agreement support formula.
- `l2_exact_support_diagonalization.md` handles the exact-support case.
- `interleaved_list_enum.py`, `interleaved_budget.py`, and
  `quotient_core_interleaving.py` provide small enumerators and proof records.

This is directly useful for protocol parameters. It says that interleaving does
not automatically multiply the list exponent by the row arity if the rows share
the same agreement columns and the full-support intersection profile is small.

What is still missing: sharp constants near capacity for the concrete arities
and radii used in protocols.

### A0/A1 audits, proof-record tooling, and formalization

The support material is also important:

- `a0_cs25_import_audit.md`, `a0_deep_point_cap_dependency_split.md`,
  `a0_cs25_rational_constant_derivation.md`, and `cs25_import_audit.md` track
  the Crites-Stewart/ABF dependency for Paper D.  The original import remains
  unaudited against primary sources, but the X1 deep-point route gives a local
  CS25-free dependency path for the headline MCA cap.
- `a1_paperA_finite_verification_crosswalk.md` maps Paper A finite claims to
  scripts and proof records.
- The reserve-emitter script, reserve JSON schema, and
  `protocol_ledger_template.md` move toward Paper C style reserve records.
- `theorem_label_map.md` and the TeX audit/inventory scripts support citation
  hygiene before promotion.
- `lean_formalization/` is an initial Lean scaffold, not a completed
  formalization.

This work does not prove MCA, but it raises the chance that any future proof is
auditable and that field ledgers do not get mixed.

## How This Points Toward The MCA Conjecture

The strongest emerging picture is:

1. Quotient-periodic support families can be explicitly accounted for.
   The new M1 scanners and dither ledgers make these obstructions visible at
   finite parameters instead of treating them as background risk.

2. The aperiodic problem is now more isolated.
   Once quotient occupancy and high-overlap codegrees are printed, what remains
   is closer to a genuine inverse-additive or residue-line packing theorem.

3. Extension-line behavior is no longer a black box.
   The counterexamples show which extension-transfer statements are false, and
   the coordinate-transfer notes suggest the positive theorem should probably
   be phrased as an interleaved or multiplication-slice statement.

4. Interleaving may be cheaper than the trivial product bound.
   The L2 full-support formula gives a plausible way to keep protocol
   interleaved-list costs within the reserve budget, if the required support
   intersection bounds can be proved.

5. The line-decoding ledger is becoming compatible with MCA.
   M2 is not solved, but there is now a concrete bridge and a warning example
   against using the wrong object.

6. The main missing proof is getting smaller and sharper.
   The recent Fable-loop work repeatedly converts broad residue-line claims
   into explicit algebraic surfaces, rank conditions, and finite verifier
   targets. That is progress even when the conclusion is a route cut.

## What Is Still Missing

The project still needs the following before the MCA conjecture can be treated
as settled.

1. A general M1 corrected-reserve local limit.
   The current material controls random baselines, quotient-periodic families,
   and several toy occupancy regimes. It does not yet prove that all aperiodic
   residue-line support packings are polynomially small above the reserve.

2. A general L1 generated-field locator local limit.
   The locator-fiber tools are strong enough to find and classify finite
   packets, but the desired theorem for arbitrary received words over
   polynomial generated fields is still open.

3. A repaired F1 extension-transfer theorem or corrected-reserve
   counterexample.
   The naive same-numerator lift is false. The live positive route must handle
   arbitrary anchors, balanced denominators, multiplication-slice behavior, and
   the rank/determinant resonance branch.

4. Sharp L2 interleaved-list constants.
   The support-intersection formula is promising, but protocol use needs
   constants for actual arities and radii, not only structural reductions.

5. A clean M2 line-decoding theorem.
   The bridge note must become a parameter-exact statement that says exactly
   when Paper B's MCA form implies the line-decoding object Paper C wants.

6. A completed A0 dependency audit for imported routes.
   The headline MCA cap has a local deep-point dependency path, but the
   original CS25/ABF route and slacked fallback still need primary-source and
   exact-constant checks before they can be cited as source-certified imports.

7. Promotion discipline.
   Several files contain local `PROVED` or old proof-sketch claims, but the
   project should not promote them into the papers until a human review checks
   hypotheses, constants, notation compatibility, and field-ledger separation.

## Next Steps

Recommended next work:

1. Run a full experimental verifier suite and record a machine-readable result
   ledger, starting from the scripts named in the two PR triage files.

2. Turn the M1 quotient occupancy formulas into a compact theorem note with
   exact hypotheses, then separate "budgeted quotient" terms from the
   aperiodic residue-line target.

3. Continue the F1 rank/determinant split work from
   `2026-06-18-fable-loop/`, especially the `Q==0` split-cubic branch and the
   transition from `t=2` toy regimes to corrected-reserve slack.

4. Use `locator_fiber_local_packet/` as the canonical L1 cross-check entry
   point and expand it from tiny examples toward the `q=17`, `q=257`, and
   dyadic toy cases in `agents.md`.

5. Convert the L2 full-support intersection formula into concrete proof records
   for `mu=2` and then for protocol-relevant arities.

6. Finish the A0 Crites-Stewart/ABF import audit before relying on the original
   imported route or slacked fallback as source-certified infrastructure; cite
   the deep-point route separately for the headline MCA cap after reviewing the
   `lem:fiber(ii)` lower bound and notation compatibility.

7. Choose a small set of stable lemmas for Lean formalization: support
   injection, full-support interleaving formula, complement-prefix locator
   lemma, and quotient-periodic overlap profile.

8. Keep all new material in `experimental/` first, with an `agents-log.md`
   entry and a reproducible command, proof record, or computation whenever
   possible.

## Reading Order

For a new contributor trying to understand the current experimental state:

1. Read `agents-log.md`.
2. Read `pr-triage-2026-06-17.md` and `pr-triage-2026-06-18.md`.
3. Read `m1_quotient_periodic_overlap_profile.md`,
   `m1_average_support_collinearity.md`, and `quotient_profile_dither.md`.
4. Read `f1_fixed_rate_extension_counterexample.md`,
   `f1_extension_coordinate_transfer.md`, and
   `2026-06-18-fable-loop/README.md`.
5. Read `l1_aperiodic_prefix_collision.md` and the locator-fiber packet
   READMEs.
6. Read `l2_interleaved_support_bridge.md` and
   `m2_line_decoding_mca_bridge.md`.
7. Read `a0_cs25_import_audit.md`,
   `a1_paperA_finite_verification_crosswalk.md`, and
   `protocol_ledger_template.md` before touching protocol claims.
