# Certificate Provenance Normalization Audit

Date: 2026-07-03. Status: AUDIT.

## Claim

Seven certificate verifiers now treat script provenance portably across Windows
CRLF checkouts and Linux LF checkouts:

```text
provenance path = repository-relative POSIX path
provenance hash = sha256(LF-normalized UTF-8 script text)
```

The mathematical replay payload remains strict. During `--check`, the scripts
compare every certificate field except `script_sha256` exactly, then require
the stored `script_sha256` to remain a valid SHA-256 hex digest. This avoids
certificate JSON churn when a replay-only provenance fix changes the verifier
source itself.

## Affected Verifiers

- `experimental/scripts/verify_cluster_certificates.py`
- `experimental/scripts/verify_cyclotomic_root_difference_germ.py`
- `experimental/scripts/verify_xr_e3_calculus.py`
- `experimental/scripts/verify_m1_johnson_anticode_toolkit.py`
- `experimental/scripts/verify_height_only_impossibility.py`
- `experimental/scripts/verify_graded_collision_radius.py`
- `experimental/scripts/verify_exceptional_density.py`

Before this change, each script hashed raw `read_bytes()` and rendered
`str(script.relative_to(REPO))`, making replays sensitive to checkout line
endings and native path separators.

## Certificate State

No certificate JSON files are changed by this normalization pass.

Six affected certificates already store a POSIX script path and the
LF-normalized hash of the pre-fix verifier source. The
`exceptional_density.json` certificate also stores a POSIX path, but its stored
script hash does not match the current LF-normalized verifier source in
`origin/main`; that is recorded as pre-existing stale provenance. Its
mathematical payload replays exactly after the normalization fix.

## Separate Non-Goal

The `paper_d_v12` `KeyError` in
`experimental/scripts/verify_f17_32_m3_low_rank2_12_paid_residual_ledger.py`
is separate upstream content drift (`paper_d_v10` versus `paper_d_v12`) and is
not touched here.

## Reproducibility

Windows, using Python 3.13 with SymPy:

```powershell
$verifiers = @(
  'experimental/scripts/verify_cluster_certificates.py',
  'experimental/scripts/verify_cyclotomic_root_difference_germ.py',
  'experimental/scripts/verify_xr_e3_calculus.py',
  'experimental/scripts/verify_m1_johnson_anticode_toolkit.py',
  'experimental/scripts/verify_height_only_impossibility.py',
  'experimental/scripts/verify_graded_collision_radius.py',
  'experimental/scripts/verify_exceptional_density.py'
)
py -3.13 -m py_compile $verifiers
foreach ($v in $verifiers) { py -3.13 $v }
```

WSL, using Sage's Python because the base WSL `python3` lacks SymPy:

```bash
cd /mnt/c/dev/research/RSMCA
scripts=(
  experimental/scripts/verify_cluster_certificates.py
  experimental/scripts/verify_cyclotomic_root_difference_germ.py
  experimental/scripts/verify_xr_e3_calculus.py
  experimental/scripts/verify_m1_johnson_anticode_toolkit.py
  experimental/scripts/verify_height_only_impossibility.py
  experimental/scripts/verify_graded_collision_radius.py
  experimental/scripts/verify_exceptional_density.py
)
sage -python -m py_compile "${scripts[@]}"
for s in "${scripts[@]}"; do sage -python "$s"; done
```

Additional checks:

```powershell
python experimental/scripts/script_reproducibility_audit.py --format json
git diff --check
```

## Non-Claims

This audit does not regenerate certificates, does not change any mathematical
claim, and does not address timeout-policy findings from the replay harness.
