# M720 Certificate Semantics

Status: PROVED.

Source DAG node: `m720_certificate_semantics`.

## Statement

For M720 MITM outputs, a zero active-core count is a complete calibration-cell
zero certificate only when the run has `complete=true`, equivalently `W=n` and
the run did not abort. If `complete=false`, the output is slice-local evidence
only and cannot be promoted to a global zero certificate.

## Proof

The MITM enumerator contract records the window size `W`, the row size `n`,
and whether the run aborted. Its completeness flag is defined by

```text
complete = (W == n) and not aborted.
```

If `complete=true`, the enumerated window is the whole row and the run
finished, so a zero unpaid active-core count is a complete-cell zero
certificate.

If `W<n`, the enumerator covered only a proper window. A zero count is then
local to that window. If the run aborted, it did not finish even the declared
window. In either case the output may be useful evidence but is not a global
zero certificate.

Thus M720 certificate consumers may use zero-count records as complete
calibration-cell certificates only when the explicit `complete=true` metadata
is present.

## Non-Claims

This packet proves only certificate semantics. It does not run the MITM scan,
construct zero certificates, or prove any official norm-gate payload.

## Replay

Regenerate:

```bash
python3 experimental/scripts/verify_m720_certificate_semantics.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_m720_certificate_semantics.py \
  --check experimental/data/certificates/m720-certificate-semantics/m720_certificate_semantics.json
```

The verifier checks note anchors and a toy truth table for the completeness
rule.
