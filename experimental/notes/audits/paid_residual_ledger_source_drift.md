# Paid residual ledger source-artifact drift audit

Date: 2026-07-04

Status: AUDIT

## Claim

The replay failure in
`experimental/scripts/verify_f17_32_m3_low_rank2_12_paid_residual_ledger.py`
is a source-artifact key drift, not a mathematical or certificate-payload
failure.  A second replay failure in the affine-GCD sibling certificate is an
upstream source/prose drift introduced before this wave, not an arithmetic
payload mismatch.

The intended consistency check is that the affine-GCD and endpoint
quotient-image source certificates cite the same Paper D file and hash, and
the same row descriptor file and hash.  The committed certificates still use
the legacy source key `paper_d_v10`, but both records point at the current
Paper D path `tex/cs25_cap_v12.tex` with the same SHA-256:

```text
64fb843392bef75b05b50fcdae7f2e6ff9ae3b229d6848cacc39ecb28fd153ea
```

## Replay Evidence

Running the pre-fix serial affine-GCD verifier to completion takes about 39
minutes single-core and fails the stored-certificate byte comparison with:

```text
AssertionError: low-rank2..12 v10 affine-gcd certificate mismatch: experimental\data\certificates\hankel-f17-32-m3-low-rank2-12-v10-affine-gcd\f17_32_n512_k256_m3_low_rank2_12_v10_affine_gcd.json
```

The failure is deterministic and reproduces at any pre-fix revision of the
verifier (for example the version at `718df24`); it is not a timeout or an
environment artifact.

## Root Cause

Git history shows two related source-artifact drifts:

- `01add41 Integrate post-v10 roadmap packets` introduced the paid-residual
  ledger verifier and its sibling certificates with the Paper D source keyed
  as `paper_d_v10`.
- `718df24 Update Paper D references to v12` updated the paid-residual verifier
  lookup from `paper_d_v10` to `paper_d_v12`.
- The same upstream commit also hand-edited the stored affine-GCD certificate's
  `construction.argument` prose from `v10` to `v12`, while the generator
  script's literal string stayed `v10`.
- The committed paid-residual ledger was not regenerated after those source
  certificate edits, so its source-artifact hashes still point at the earlier
  source-certificate bytes.

The evidence commands are:

```powershell
git diff 01add41..718df24 -- experimental/data/certificates/hankel-f17-32-m3-low-rank2-12-v10-affine-gcd/f17_32_n512_k256_m3_low_rank2_12_v10_affine_gcd.json
git show 01add41:experimental/scripts/verify_f17_32_m3_low_rank2_12_v10_affine_gcd.py | Select-String "The v10 affine rank-drop gcd divides"
git show 718df24:experimental/scripts/verify_f17_32_m3_low_rank2_12_v10_affine_gcd.py | Select-String "The v10 affine rank-drop gcd divides"
git show 398beb9:experimental/scripts/verify_f17_32_m3_low_rank2_12_v10_affine_gcd.py | Select-String "The v10 affine rank-drop gcd divides"
git show 2c62db8:experimental/scripts/verify_f17_32_m3_low_rank2_12_v10_affine_gcd.py | Select-String "The v10 affine rank-drop gcd divides"
```

The first command shows the stored certificate changing:

```text
"The v10 affine rank-drop gcd divides" -> "The v12 affine rank-drop gcd divides"
"ref": "tex/cs25_cap_v10.tex" -> "ref": "tex/cs25_cap_v12.tex"
```

The four `git show` checks find the generator literal
`The v10 affine rank-drop gcd divides` unchanged at `01add41`, `718df24`,
`398beb9`, and `2c62db8`.

Independent corroboration: the integrated WP-0.3 replay audit
(`experimental/notes/audits/audit_wp03_low_rank2_12_affine_gcd_replay.md`)
already recorded the `718df24` prose/reference bump as data-neutral ("the diff
touches no data row") and independently re-derived all 462 affine-GCD records
on an external second stack with zero divergences.  That external replay
confirms the certificate DATA is sound; what it did not flag — and what this
note adds — is that the same prose bump breaks the repo verifier's own
regenerate-and-compare replay, which is the defect fixed here.  The bump was a
deliberate reference update whose unintended side effect was the self-replay
breakage; it was not a data edit.

The previous paid-residual verifier therefore raised:

```text
KeyError: 'paper_d_v12'
```

before it reached the hash comparison it was meant to perform.  The previous
affine-GCD verifier regenerated a certificate whose mathematical payload
matched, but whose source/prose fields differed from the hand-edited stored
certificate.

## Fix

The paid-residual verifier now resolves the Paper D source record by source
semantics:

1. accept either `paper_d_v12` or the legacy `paper_d_v10` key;
2. require the resolved record to cite `tex/cs25_cap_v12.tex`;
3. require a `sha256` field;
4. compare the resolved affine and endpoint Paper D hashes exactly.

The row descriptor source-hash comparison is unchanged.  No certificate JSON is
modified.

The sibling `--check` paths for the affine-GCD and endpoint quotient-image
verifiers now also tolerate source-artifact-only replay drift.  Exact byte
comparison still succeeds first when possible.  If it fails, the checker
compares the certificate payload after normalizing:

- path separators in source-artifact refs;
- the legacy `paper_d_v10`/`paper_d_v12` source key;
- source-artifact SHA placeholder fields that already drift by construction;
- exactly one stale construction-prose string:
  `The v12 affine rank-drop gcd divides` ->
  `The v10 affine rank-drop gcd divides`.

This does not relax any arithmetic records, ledger counts, aggregate fields, or
deterministic record hashes.  Field-by-field regeneration diff confirmed
`records`, `aggregate`, and `deterministic_record_hash` are equal after this
source/prose normalization.

The affine-GCD verifier also accepts `--jobs N` to compute the independent
agreement rows in parallel.  The default remains serial; `--jobs` changes only
the replay schedule, and the emitted records are sorted before hash comparison.

## Recommended Upstream Resolution

The normalizer is a bridge for replay across the upstream source/prose drift.
The maintainer should eventually choose one canonical spelling:

- correct the stored affine-GCD certificate prose back to `v10`; or
- update the generator's construction string to `v12`.

This branch does not edit the maintainer-authored certificate JSON.

## Reproducibility

Before the fix:

```powershell
py -3.13 experimental\scripts\verify_f17_32_m3_low_rank2_12_paid_residual_ledger.py --check experimental\data\certificates\hankel-f17-32-m3-low-rank2-12-paid-residual-ledger\f17_32_n512_k256_m3_low_rank2_12_paid_residual_ledger.json
```

failed with `KeyError: 'paper_d_v12'`.

The completed pre-fix affine-GCD replay:

```powershell
py -3.13 experimental\scripts\verify_f17_32_m3_low_rank2_12_v10_affine_gcd.py --check experimental\data\certificates\hankel-f17-32-m3-low-rank2-12-v10-affine-gcd\f17_32_n512_k256_m3_low_rank2_12_v10_affine_gcd.json
```

failed with the certificate-mismatch `AssertionError` shown above.

After the fix, replay:

```powershell
py -3.13 experimental\scripts\verify_f17_32_m3_low_rank2_12_paid_residual_ledger.py --check experimental\data\certificates\hankel-f17-32-m3-low-rank2-12-paid-residual-ledger\f17_32_n512_k256_m3_low_rank2_12_paid_residual_ledger.json
```

and run the sibling source certificates:

```powershell
py -3.13 experimental\scripts\verify_f17_32_m3_low_rank2_12_v10_affine_gcd.py --jobs 6 --check experimental\data\certificates\hankel-f17-32-m3-low-rank2-12-v10-affine-gcd\f17_32_n512_k256_m3_low_rank2_12_v10_affine_gcd.json
py -3.13 experimental\scripts\verify_f17_32_m3_low_rank2_12_endpoint_quotient_image.py --check experimental\data\certificates\hankel-f17-32-m3-low-rank2-12-endpoint-quotient-image\f17_32_n512_k256_m3_low_rank2_12_endpoint_quotient_image.json
```

## Non-Claims

- This audit does not regenerate or alter the committed certificates.
- This audit does not change the paid-residual ledger arithmetic.
- This audit does not rename the historical `v10` packet paths.
- This audit does not decide whether the canonical prose should say `v10` or
  `v12`; that is a maintainer data-file decision.
