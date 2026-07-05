# M720 Official Norm-Gate Case Manifest Soundness

Status: PROVED.

Source DAG node: `m720_official_norm_gate_case_manifest_soundness`.

## Statement

If a manifest covers every official-shape primitive `h=7..20` norm-gate case
and, for each case, supplies either a uniform nonvanishing theorem citation or
a `complete=true` zero-survivor certificate record, then
`m720_official_h7_20_norm_gate_payload` holds.

## Proof

Let `C` be the set of official-shape primitive `h=7..20` norm-gate cases. The
manifest covers `C`, so every primitive case appears exactly once, or appears
inside a declared disjoint case class with accounted multiplicity.

Each covered case has one accepted discharge type:

- a uniform nonvanishing theorem citation, which excludes the primitive
  norm-gate obstruction for the case or case class; or
- a certificate record with `complete=true` and zero unpaid non-toral
  survivors.

By `m720_certificate_semantics`, a `complete=true` zero-survivor record is a
complete zero certificate for that case. Since every official primitive case
is covered by one accepted discharge, the manifest supplies either a uniform
theorem or a complete zero certificate for all official-shape primitive
norm-gate cases. This is exactly `m720_official_h7_20_norm_gate_payload`.

## Non-Claims

This packet proves only manifest soundness. It does not construct the official
case manifest, prove a uniform nonvanishing theorem, or run any M720 MITM
payload scan.

## Replay

Regenerate:

```bash
python3 experimental/scripts/verify_m720_official_norm_gate_case_manifest_soundness.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_m720_official_norm_gate_case_manifest_soundness.py \
  --check experimental/data/certificates/m720-official-norm-gate-case-manifest-soundness/m720_official_norm_gate_case_manifest_soundness.json
```

The verifier checks note anchors and a toy manifest with coverage and
accepted-discharge failure cases.
