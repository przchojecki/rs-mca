# M720 Official Norm-Gate Certificate Soundness

Status: PROVED.

Source DAG node: `m720_official_norm_gate_certificate_soundness`.

## Statement

Assume `m720_official_paid_branch_alignment`: every official-shape `h=7..20`
active-core candidate is either paid/toral or belongs to the primitive x83
norm-gate branch.

If a payload or uniform theorem covers every primitive official `h=7..20`
norm-gate case and certifies zero unpaid non-toral survivors in each covered
case, with complete records in the sense of `m720_certificate_semantics`, then
the primitive norm-gate branch contributes no unpaid active cores.

## Proof

By `m720_official_paid_branch_alignment`, every official-shape `h=7..20`
active-core candidate lies in exactly one relevant branch for this consumer:

1. the paid or toral branch, already charged elsewhere; or
2. the primitive p-specific norm-gate branch.

This packet concerns only the second branch. If a uniform nonvanishing theorem
covers that primitive branch, then no primitive norm-gate event occurs, so
there is no unpaid non-toral survivor.

Alternatively, suppose a certificate payload covers every official primitive
norm-gate case. By `m720_certificate_semantics`, only records with
`complete=true` are complete zero certificates; incomplete slices are
slice-local evidence only. If every covered primitive record is complete and
reports zero unpaid non-toral survivors, then every primitive norm-gate case
has been checked globally and has no survivor.

The other branch is paid or toral, so an accepted primitive payload excludes
the entire unpaid primitive norm-gate branch.

## Non-Claims

This packet proves only the soundness of a complete primitive norm-gate
payload or uniform theorem under the stated branch-alignment dependency. It
does not provide the actual official `h=7..20` payload and does not run the
M720 MITM certificates.

## Replay

Regenerate:

```bash
python3 experimental/scripts/verify_m720_official_norm_gate_certificate_soundness.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_m720_official_norm_gate_certificate_soundness.py \
  --check experimental/data/certificates/m720-official-norm-gate-certificate-soundness/m720_official_norm_gate_certificate_soundness.json
```

The verifier checks note anchors and a toy payload schema with coverage,
branch, completeness, and nonzero-survivor rejection cases.
