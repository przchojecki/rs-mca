# Paper D v12 Consolidated Audit Map

## Claim

The five AGENTS.md Paper D v12 audit lanes have local verifier/notes coverage in
this checkout. The current local replay found those verifier scripts passing,
with documentation-alignment and presentation follow-ups to carry forward.

## Status

AUDIT.

## Parameters

- Paper D: `tex/cs25_cap_v12.tex`
- Compact note: `tex/towards-prize.tex`
- Date: 2026-07-02 America/Denver / 2026-07-03 UTC
- Repo HEAD: `0f45bf377386fe8d7e448df218fab2692e0b216a`

## Existing Paper Dependency

This note does not edit Papers A-D. It maps the current audit surface for Paper
D v12 and the compact prize note.

## Proof Idea Or Experiment

Run the existing verifier scripts and compare their source labels against the
current TeX labels.

## Results

### Deep-Point Conversion Radius

- Note: `experimental/notes/audits/cs25_v12_conversion_radius_audit.md`
- Script: `experimental/scripts/verify_cs25_v12_conversion_radius.py`
- Source label: `tex/cs25_cap_v12.tex`, `thm:A`
- Replay status: PASS.
- Scope: checks the direct self-contained conversion and integer-radius
  condition `floor(delta n) <= n-k-1`.

### BCIKS Half-Distance Import

- Note: `experimental/notes/audits/cs25_v12_bciks_import_audit.md`
- Script: `experimental/scripts/verify_cs25_v12_bciks_import.py`
- Source labels: `cor:conditional-half`, `thm:mca-from-ca`,
  `thm:elementary-ca`; compact-note labels include `cor:import`, `thm:half`.
- Replay status: PASS.
- Scope: checks the normalization of `eca` consumed by the conditional
  half-distance safe side.

### Deployed Exact Certificates

- Note: `experimental/notes/audits/cs25_v12_deployed_certificate_audit.md`
- Script: `experimental/scripts/verify_cs25_v12_deployed_certificates.py`
- Packet: `experimental/data/certificates/cs25-v12-deployed-certificates/cs25_v12_deployed_certificates.json`
- Source labels: `def:certificate-v2`, `thm:T7-closure`, `tab:certs`.
- Replay status: PASS.
- Scope: checks Paper D deployed-row certificate arithmetic. Separately, the
  independent replay found non-Paper-D README certificate mismatches in several
  Hankel/M1 packets; the current C-drive replay refresh records those in
  `independent_replay_2026-07-03.md`.

### Circle / Genus-One / Transport Scope

- Note: `experimental/notes/audits/cs25_v12_transport_scope_audit.md`
- Script: `experimental/scripts/verify_cs25_v12_transport_scope.py`
- Source labels: `cor:ecfft-macroscopic`, `lem:stereographic`,
  `cor:circle-anyfield`.
- Replay status: PASS.
- Scope: arithmetic and small-field algebra checks for transport statements.
  It does not prove that an arbitrary deployed row is structurally
  `(psi,2)`-smooth.

### `towards-prize.tex` Alignment And Scoping

- Note: `experimental/notes/audits/towards_prize_v3_cap_package_audit.md`
- Script: `experimental/scripts/verify_towards_prize_v3_cap_package.py`
- Current source label: `tex/towards-prize.tex`, `prop:companion-certificate-package`.
- Replay status: PASS in targeted read-only run.
- Scope: checks that `towards-prize.tex` remains a compact theorem note, not the
  full Paper D ledger.

## Gaps / Follow-Up

1. The conversion audit is local-source complete, but the external ABF/CS PDF
   convention comparison is still source-conditioned when Cloudflare blocks
   direct fetches.
2. The profile verifier records a wording/clarity finding: one displayed
   rational bound is just below `ceil((q-n)/(3k))`, while the printed integer
   count is recovered by integrality.
3. The BCIKS import audit now records two adversarial follow-ups.  First,
   `cor:conditional-half` should explicitly reduce the stated integer-ball
   condition `2*floor(delta*n) <= n-k` to the BCIKS import radius
   `delta' = floor(delta*n)/n <= (1-rho)/2`; this is proof clarity, not an
   `eca` normalization failure.  Second, the circle widened unsafe edge in
   `tab:scanner2` is printed as `0.46788`, but the exact edge is
   `30663/65536 = 0.467880249...`; if the table keeps the caption's
   "rounded outward to five digits" convention for unsafe lower edges, the
   five-decimal value should be `0.46789` or the exact fraction should be used.

## Adversarial Checks

Three independent read-only audit agents were run on 2026-07-03:

- Deep-point conversion / `thm:A`: verdict `matches exactly` for the scoped
  local v12 chain; no surviving correction or hypothesis gap found.
- BCIKS / MCA transfer / sandwich: verdict `matches exactly` for the import
  normalization, with the two presentation follow-ups listed above.
- Circle / genus-one / towards-prize alignment: verdict `matches exactly` for
  the arithmetic and scope checked locally; the genus-one row still depends on
  the stated `(psi,2)`-smooth degree `(2,1)` structural hypothesis.

No retained Grok transcript is attached to this audit.  The findings above
therefore rest only on the local verifier outputs and retained audit notes; any
unretained advisory review should be treated as non-evidence.

## Resolved Local Documentation Drift

- `towards_prize_v3_cap_package_audit.md` now points at the current
  `tex/towards-prize.tex` label `prop:companion-certificate-package`.
- `experimental/notes/audits/theorem_label_map.md` now records Paper D v12's
  `thm:A` as a direct self-contained conversion and isolates the optional
  imported lanes in `thm:B` and `cor:conditional-half`.

## Ledger Impact

The core Paper D v12 audit scripts replay cleanly in the native Python lane. The
remaining items are documentation/provenance gaps, not theorem changes.

## Constants

No constants are changed.

## Reproducibility

```sh
python3 experimental/scripts/verify_cs25_v12_conversion_radius.py
python3 experimental/scripts/verify_cs25_v12_bciks_import.py
python3 experimental/scripts/verify_cs25_v12_deployed_certificates.py
python3 experimental/scripts/verify_cs25_v12_transport_scope.py
python3 experimental/scripts/verify_towards_prize_v3_cap_package.py
python3 experimental/scripts/verify_cs25_v12_profile_explicit.py
```

## Non-Claims

- This note does not alter Paper D or `towards-prize.tex`.
- This note does not close Open Problem `prob:band`.
- This note does not promote any conditional import to PROVED.
