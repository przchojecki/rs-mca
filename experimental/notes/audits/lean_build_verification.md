# Lean Build Verification

## Claim

The Lean starter package builds on an unrestricted native Windows host with the
toolchain pinned by the repository.

## Status

AUDIT.

## Parameters

- Directory: `experimental/lean/rs_mca_formalization`
- Toolchain file: `leanprover/lean4:v4.31.0`
- Host date: 2026-07-02 America/Denver / 2026-07-03 UTC
- Elan: 4.2.3
- Lean: 4.31.0, `x86_64-w64-windows-gnu`, commit `68218e876d2a38b1985b8590fff244a83c321783`
- Lake: 5.0.0-src+68218e8
- Dependency posture: stdlib-only; no `mathlib` dependency in `lakefile.lean`.

## Existing Paper Dependency

This audits the experimental Lean formalization layer. It does not promote any
formalized statement into Papers A-D.

## Proof Idea Or Experiment

Run `lake build`, grep the imported modules for proof placeholders, and run an
independent `#print axioms` probe for representative exported theorems.

## Results

`lake build` completed successfully:

```text
Build completed successfully (13 jobs).
```

The build included the repository's in-file `#print axioms` checks in
`RsMca/QFBridge_A1.lean`, reporting:

```text
qf_half_closed: [propext, Classical.choice, Quot.sound]
QFBridgeA1.assembly_gen: [propext, Classical.choice, Quot.sound]
QFBridgeA1.reindex_reverse: [propext, Quot.sound]
QFBridgeA1.qft_eq: no axioms
QFBridgeA1.sum_map_zero: [propext]
QFBridgeA1.aux_secondSum: [propext, Quot.sound]
```

An independent temporary probe migrated under
`C:\dev\research\RSMCA\_migration\lab\lean_axiom_probe.lean` reported:

```text
RsMca.field_count_gate: no axioms
RsMca.field_floor: no axioms
RsMca.safe_iff_agreement_ge_507: [propext, Classical.choice, Quot.sound]
RsMca.f17_staircase: no axioms
RsMca.f17_largest_safe_radius: no axioms
RsMca.tangentExact_iff_radius: [propext, Classical.choice, Quot.sound]
RsMca.not_strictActive_of_t_le_m: [propext, Quot.sound]
RsMca.maximalDither_kills: [propext, Quot.sound]
W1.W1_first_root: [propext, Quot.sound]
W1.hockey: [propext, Quot.sound]
qf_half_closed: [propext, Classical.choice, Quot.sound]
```

A grep for `sorry`, `admit`, and `native_decide` in imported modules found only
documentation/comment mentions, not proof terms.

After the 2026-07-03 upstream refresh to `e1635f0`, the original
`rs_mca_formalization` package was rebuilt and still completed successfully
with 13 jobs.

The refresh also added two Mathlib-backed Lean 4.28 packages:

- `experimental/lean/RS_disproof_v3`: after `lake exe cache get`, `lake build`
  completed successfully with 8031 jobs.
- `experimental/lean/cs25_cap_v12`: this is an explicit skeleton package with
  `sorry` placeholders. Grep found proof placeholders in files such as
  `Fiber.lean`, `CircleCode.lean`, `ECFFT.lean`, `InterleavingTransfer.lean`,
  `QuotientRemainder.lean`, and `AperiodicHankel.lean`. After repairing a
  stale generated `.lake/packages/mathlib` checkout and rerunning
  `lake exe cache get`, a direct `lake build` completed successfully with
  8043 jobs. The build emitted the expected Lean warnings that the skeleton
  modules contain declarations using `sorry`, plus minor linter warnings for
  unused variables. This is a successful syntax/typechecking build of the new
  skeleton package, not a proof-completeness claim.

### 2026-07-03 Clean Paper A Reproduction After Faster-Drive Migration

A fresh detached `origin/main` worktree at
`0f45bf377386fe8d7e448df218fab2692e0b216a` was created under
`C:\dev\research\rsmca-clean-lean-origin-main-20260703-143504` to reproduce the
Paper A Lean package from a canonical state. Before setup, the package had no
`lakefile.lean` shadow and no `.lake/` directory.

The following commands were run from
`experimental/lean/RS_disproof_v3`; stdout, stderr, wall time, exit status, and
command metadata were captured locally under
`_migration/lab/paper-a-clean-repro-20260703-new-checkout/`:

```text
lake exe cache get
  exit_status=EXIT
  exit_code=0
  wall_seconds=482.245

lake build +RS_disproof_v3.Main:olean
  exit_status=EXIT
  exit_code=0
  wall_seconds=47.968

lake build +RS_disproof_v3.ExtensionTower:olean
  exit_status=EXIT
  exit_code=0
  wall_seconds=35.707

lake build
  exit_status=EXIT
  exit_code=0
  wall_seconds=61.356
  result: Build completed successfully (8031 jobs).
```

This faster-checkout clean reproduction did not reproduce the earlier
`Main:olean` timeout from the old drive. Because the upstream commit is the
same and the package state was clean before setup, the provisional
classification for the old timeout is `LOCAL ENV/performance issue`, not
`LOCAL PACKAGING issue` or `UPSTREAM LEAN PROOF/PERFORMANCE issue`.

## Ledger Impact

Issue #159 appears to be an environment/toolchain-download failure in restricted
agent sandboxes, not a Lean package failure. The package itself builds once
Lean 4.31.0 is installed. The newer Lean 4.28 Mathlib packages should be
tracked separately because they have different dependencies and proof-status
posture. The separate old-drive Paper A timeout did not reproduce in the clean
faster checkout and should remain classified as a local environment/performance
issue unless a later clean reproduction contradicts these logs.

## Constants

No mathematical constants are changed.

## Reproducibility

```sh
cd experimental/lean/rs_mca_formalization
lake build
```

Upstream Mathlib-backed packages:

```sh
cd experimental/lean/RS_disproof_v3
lake exe cache get
lake build +RS_disproof_v3.Main:olean
lake build +RS_disproof_v3.ExtensionTower:olean
lake build

cd ../cs25_cap_v12
lake exe cache get
lake build
```

Representative axiom probe:

```lean
import RsMca

#print axioms RsMca.field_count_gate
#print axioms RsMca.field_floor
#print axioms RsMca.safe_iff_agreement_ge_507
#print axioms RsMca.f17_staircase
#print axioms RsMca.f17_largest_safe_radius
#print axioms RsMca.tangentExact_iff_radius
#print axioms RsMca.not_strictActive_of_t_le_m
#print axioms RsMca.maximalDither_kills
#print axioms W1.W1_first_root
#print axioms W1.hockey
#print axioms qf_half_closed
```

## Draft Issue Comment For #159

Do not post without maintainer/user review.

````markdown
I was able to build the Lean package locally on native Windows after installing
Lean via elan.

Environment:
- toolchain: leanprover/lean4:v4.31.0
- Lean: 4.31.0, x86_64-w64-windows-gnu
- Lake: 5.0.0-src+68218e8

Command:

```sh
cd experimental/lean/rs_mca_formalization
lake build
```

Result: build completed successfully (13 jobs).

I also checked that the package is stdlib-only/no mathlib, and a grep for
`sorry`, `admit`, and `native_decide` in imported modules found only comments.
Representative `#print axioms` checks report either no axioms for the concrete
finite gates or standard Lean axioms such as `propext`, `Classical.choice`, and
`Quot.sound` for symbolic arithmetic lemmas.

So this looks like a sandbox/toolchain-download issue rather than a package
failure. A short docs note saying "install elan/Lean first; mathlib is not
required" would probably prevent the same triage failure.
````

## Non-Claims

- This does not prove the main MCA conjectures.
- This does not assert axiom-freeness for every symbolic theorem; it records
  representative `#print axioms` output and a successful full build.
- This does not claim the new `cs25_cap_v12` Lean skeleton is sorry-free. It is
  locally build-verified as a skeleton package, and the `sorry` warnings are
  explicit proof targets.
- No issue comment was posted.
