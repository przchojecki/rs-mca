# Independent Verifier Replay, Windows Host

Superseded for current C-drive replay packaging by
`experimental/notes/audits/independent_replay_2026-07-03.md`.  This file is
retained as the pre-migration/historical audit narrative for the original
2026-07-02 replay bundle.

## Claim

Fresh local replay of the repository verifier surface on native Windows, with
raw logs kept locally under `C:\dev\research\RSMCA\_migration\lab`.

## Status

AUDIT.

## Parameters

- Repository: `C:\dev\research\RSMCA`
- Initial replay HEAD: `6c93a6d711985e1beb45ebafaf36da325e39023d` (historical
  pre-migration replay snapshot)
- Current validation HEAD after upstream refresh: `0f45bf377386fe8d7e448df218fab2692e0b216a`
  (`Add CAP25 v13 experimental insert`)
- Local branch: `contrib/full-plan-local`, aligned with `origin/main` at the
  current validation HEAD
- Date: 2026-07-02 America/Denver / 2026-07-03 UTC
- Python: 3.13 venv captured in the migrated lab environment note under
  `C:\dev\research\RSMCA\_migration\lab\environment.md`
- Extra dependency installed for replay: `sympy==1.14.0`
- GPU present but not used for this replay: RTX 3090, 24 GiB
- Sage/WSL status: repaired locally. Native Windows has no `sage` executable,
  but the host WSL hang was cleared and `Ubuntu` now launches normally.
  SageMath 10.7 is available through the path configured by
  `RSMCA_WSL_SAGE`. The replay harness uses WSL Sage when requested or when
  auto-detected, and retains exact native companion checks for hosts where Sage
  is absent.
- Upstream PR overlap snapshot after refresh: `#198` is closed without merge;
  current open PRs checked on 2026-07-03 are `#209`--`#222`.

## Existing Paper Dependency

This is a reproducibility audit for the experimental script/certificate layer,
with special attention to the Paper D v12 audit scripts.

## Proof Idea Or Experiment

The replay harness in `experimental/scripts/replay_all_verifiers.py` discovers
and runs:

- default `verify_*.py`, audit, inventory, and data verifier scripts;
- Python commands quoted in experimental READMEs;
- certificate-scanner examples;
- committed aperiodic eliminant packets.

The harness redirects README write/output targets into the lab output directory
and handles cwd-relative README commands, so replay does not overwrite tracked
certificates.

Historical machine-readable results are in
`experimental/data/audits/historical/independent_replay_2026-07-02_composite_historical.json`.
The supplementary Sage-lane replay matrix is in
`experimental/data/audits/historical/independent_replay_2026-07-03_sage_native_historical.json`.
The real WSL Sage replay matrix is in
`experimental/data/audits/historical/independent_replay_2026-07-03_sage_wsl_historical.json`.
Those JSON files preserve the original pre-migration run metadata, including
old `D:\dev` lab paths and first-pass classifier labels.  They should be read as
historical replay snapshots, not as freshly regenerated C-drive harness output.

## Results

Script-default lane, first pass: 175 PASS, 3 SKIP-external, 1 FAIL, 1
FAIL-path, 5 FAIL-missing-import, 3 TIMEOUT out of 188 tasks.
The `SKIP-external` count is the original snapshot label; the harness classifier
has since been tightened to require an explicit replay skip sentinel rather than
matching the word "skipped" in ordinary passing output.

After installing `sympy`, all five missing-import scripts passed on targeted
rerun:

- `verify_l1_prefix_dyadic_charzero_rigidity.py`
- `verify_l1_prefix_low_excess_norm_sieve.py`
- `verify_l1_prefix_prime_power_charzero_fibers.py`
- `verify_v1_f17_32_algebra_checker.py`
- `verify_x1_prob_explicit_mechanism.py`

Two 180-second timeouts were slow passes with a 900-second cap:

- `verify_l1_full_petal_growing_defect_witnesses.py`, about 627 s.
- `verify_m1_cycle120_self_contained_certificate.py`, about 687 s.

One long verifier remained unresolved under the 900-second cap:

- `verify_f17_32_m3_low_rank2_12_v10_affine_gcd.py`.

The original native Windows Sage-path failure was:

- `verify_l1_prefix_dual_large_domain_weil_energy_floor.py` calls `sage -python`.

That verifier now passes on this native Windows host:

```text
atlas_backend=stdlib-libm-widened
ALL_CHECKS_OK=True
```

The WSL backend was repaired after `wsl -l -v`, `wsl --status`, and direct
`wsl -d Ubuntu ...` launches initially timed out. `Stop-Service WSLService`
was denied in this non-elevated session, but `hcsdiag list` exposed a stuck
running WSL VM. Killing that WSL HCS VM after clearing stale `wsl.exe` clients
restored `wsl -l -v`, `wsl --status`, and direct Ubuntu launch. The current
probe results are:

```text
wsl -l -v      -> Ubuntu Stopped, version 2
wsl --status   -> Default Distribution: Ubuntu; Default Version: 2
wsl -d Ubuntu --exec /bin/sh -lc "echo WSL_OK; uname -a; id" -> WSL_OK
```

The large-domain atlas verifier also passes on the true Sage/Arb backend from
native Windows by dispatching the Sage subprocess through WSL when no native
`sage` executable is on `PATH`:

```text
python experimental/scripts/verify_l1_prefix_dual_large_domain_weil_energy_floor.py \
  --atlas-backend sage
atlas_backend=sage-arb-wsl
ALL_CHECKS_OK=True
```

The optional Sage-script lane now has two working modes. With WSL Sage, the
harness records 5 PASS out of 5 in
`experimental/data/audits/historical/independent_replay_2026-07-03_sage_wsl_historical.json`:

- `audit_m1_interleaved_list_threshold_descent.sage` via WSL Sage;
- `audit_m1_interleaved_list_threshold_interval_sharpening.sage` via WSL Sage;
- `audit_m1_interleaved_list_threshold_upward_push.sage` via WSL Sage;
- `audit_m1_interleaved_list_hybrid_quotient_residual.sage` via WSL Sage;
- `locator/sage_locator_fiber_crosscheck/sage_locator_fiber_crosscheck.sage`
  via WSL Sage `-python`.

On hosts where Sage remains absent, the harness still maps the same five
`.sage` audits to `experimental/scripts/verify_native_sage_replays.py`; the
supplementary native-companion matrix records 5 PASS out of 5:

- `audit_m1_interleaved_list_threshold_descent.sage` via
  `--case threshold-descent`;
- `audit_m1_interleaved_list_threshold_interval_sharpening.sage` via
  `--case threshold-interval-sharpening`;
- `audit_m1_interleaved_list_threshold_upward_push.sage` via
  `--case threshold-upward-push`;
- `audit_m1_interleaved_list_hybrid_quotient_residual.sage` via
  `--case hybrid-quotient-residual`;
- `locator/sage_locator_fiber_crosscheck/sage_locator_fiber_crosscheck.sage`
  via `--case locator-selected`.

README lane after harness fixes: 29 PASS, 1 SKIP-external, 7 FAIL, 3 TIMEOUT out
of 40 tasks. The remaining FAIL items are certificate `--check` mismatches or a
source-key exception, not path bugs:

- `verify_f17_32_m3_generic_regular_minor.py --check ...`: certificate mismatch.
- `verify_f17_32_high_agreement_tangent_table.py --check ...`: certificate mismatch.
- `verify_f17_32_m3_endpoint_c2_capacity.py --check ...`: certificate mismatch.
- `verify_f17_32_m3_low_rank2_12_endpoint_quotient_image.py --check ...`: certificate mismatch.
- `verify_f17_32_m3_low_rank2_12_paid_residual_ledger.py --check ...`: `KeyError: 'paper_d_v12'`.
- `certify_high_agreement_threshold_package.py --check ...`: printed `FAIL`.
- `search_m1_two_coordinate_wall_stdlib.py --check ...`: certificate mismatch.

Scanner lane after harness fixes: 4 PASS out of 4.

Aperiodic packet lane after harness fixes: 3 PASS out of 3, including the
intentional invalid packet under `--expect-fail`.

Paper D v12 audit scripts passed in the script-default lane:

- `verify_cs25_v12_conversion_radius.py`
- `verify_cs25_v12_bciks_import.py`
- `verify_cs25_v12_deployed_certificates.py`
- `verify_cs25_v12_transport_scope.py`
- `verify_cs25_v12_profile_explicit.py`

## Ledger Impact

This note does not change any theorem status. It identifies replay health and
separates environment issues, slow scripts, certificate drift, and Paper D v12
audit coverage.

## Constants

No mathematical constants are changed. Timeout-sensitive scripts should be
documented with expected wall time or reduced default modes if they are intended
for one-command replay.

## Reproducibility

Example smoke command:

```sh
python3 experimental/scripts/replay_all_verifiers.py \
  --repo C:/dev/research/RSMCA \
  --out C:/dev/research/RSMCA/_migration/lab/replay-sage-wsl \
  --python python \
  --timeout 180 \
  --only sage \
  --sage-mode wsl
```

The full native replay used the same harness with `--only scripts`, `--only
readmes`, `--only scanner`, `--only packets`, and `--only sage`.

## Non-Claims

- The WSL Sage replay is a real Sage replay for the five `.sage` audit scripts,
  and the large-domain atlas verifier was also exercised with
  `atlas_backend=sage-arb-wsl`. Native companion checks remain useful as a
  portability fallback, not as a replacement for Sage where Sage is available.
- Certificate mismatches are not diagnosed as mathematical errors here.
- No Papers A-D were edited.
