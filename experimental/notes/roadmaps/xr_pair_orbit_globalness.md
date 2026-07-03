# E18/E19 XR Pair-Orbit Globalness Evidence

- **Status:** EXPERIMENTAL_EVIDENCE / exact finite corpus plus sampled telemetry.
- **Verifier:** `experimental/scripts/verify_xr_pair_orbit_globalness.py`.
- **Artifact:** `experimental/data/certificates/xr-pair-orbit-globalness/xr_pair_orbit_globalness.json`.
- **DAG links:** `c_xr_content`, `xr_inverse`, `xr_globalness_from_ledger`.

This packet upgrades the E11 dictionary scan in one concrete direction: it
computes actual alignment sets

```text
A_{u,v} = {T in D_j : H_u l_T parallel H_v l_T and H_v l_T != 0}
```

for a deterministic corpus of word pairs on the subgroup row.  In the exact
case, `n=16`, `j=8`, `F_97`, and window length `t=2`; the scanner computes
`E_3^J(A)` exactly on the Johnson graph and tabulates fixed-core link densities
for `r=1,2,3,4`.  It also runs sampled `n=32`, `j=16` telemetry using the same
alignment predicate.

## Main Readout

The exact `n=16` scan separates three effects:

1. raw high-`E_3` cases from Fourier-character pairs are paid global or
   degenerate rank-one structures and are stripped before interpreting XR;
2. fixed-core/fixed-hole shapes are recognized when they occur;
3. post-strip delta-character rows can top this finite actual-pair corpus while
   being link-dense but not exactly fixed-core/fixed-hole, so the strict phrase
   "top actual sets are only fixed-core/fixed-hole" is too narrow at this toy
   window.

The E19 measurement is the useful warning.  Several top post-strip
delta-character rows have near-full or full density on a fixed-core link while
not being exactly classified as fixed-core/fixed-hole.  The certificate reports
these as paid-tangent link-leak candidates: either the strip/taxonomy is
incomplete for this toy window, or the narrow `c_xr_content` statement needs an
extra member.

No exact `n=16` post-strip record exceeds the coarse polynomial KLLM proxy

```text
max link density at radius r <= min(1, n^r * density(A)).
```

but this proxy saturates on the dense toy records, so it is not the decisive
column here.  No sampled `n=32` record exceeds the same proxy either.

## Interpretation

For E18, this is not a proof of `c_xr_content`; it is a real-object falsifier
harness.  At `t=2`, the strict "top post-strip sets are fixed-core/fixed-hole"
reading fails in the exact corpus because delta-character sets appear in the
top decile.

For E19, the data report the failure branch loudly: the tested exact corpus has
paid-tangent link-leak candidates.  The next decision is whether these rows are
already paid by the tangent ledger after a sharper strip, or whether `C_XR`
needs a new named class.  The KLLM comparison remains a proxy until E20 records
the imported theorem's constants and loss exponents.

## Replay

```sh
python3 experimental/scripts/verify_xr_pair_orbit_globalness.py
python3 experimental/scripts/verify_xr_pair_orbit_globalness.py --write
python3 experimental/scripts/verify_xr_pair_orbit_globalness.py --check
python3 -m py_compile experimental/scripts/verify_xr_pair_orbit_globalness.py
```
