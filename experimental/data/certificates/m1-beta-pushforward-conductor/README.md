# M1 (BETA_2) beta-pushforward conductor scan certificate

Deterministic certificate for `experimental/scripts/search_m1_beta_pushforward_conductor_scan.py`,
a conductor-growth probe for the conditional M1 import `(BETA_2)`
(`m1_kummer_weil_import_contract.md`): the rank-two good beta-pushforward trace
`G_{psi,phi} = sum_{Y_G} psi(a) phi(beta) chi(d_UV)` should satisfy
`|G_{psi,phi}| <= C_beta(e) p` with conductor `C_beta(e)` independent of `p`.

The scanner reuses the *validated* `good_pushforward_matrix` (the `e x e` label
matrix, an `O(p^2)` build) and `spectral_stats` (the 2D DFT giving
`max|G_{psi,phi}|`) from `verify_m1_beta_pushforward_spectral_audit.py` (whose
fixed `(p,e)` rows only reach `p=127`), and scans FIXED `e` over a much larger
`p` range to watch whether the conductor ratio `max|G|/p` stays bounded (no
counterexample to `(BETA_2)`) or grows with `p`.

## What the certificate pins

- **Reproduces four audit datapoints** from the imported functions:
  `(43,6)`, `(61,12)`, `(73,12)`, `(109,12)` -> the published
  `(two_sided/p, beta2/p)` rows exactly (e.g. `(43,6)` gives
  `3.0697674419 / 3.2558139535`).
- **A small deterministic extended trend** (`e=6, p<=151`): peak
  `beta2/p = 5.50684932`, peak `two_sided/p = 3.98165138`.

## Reproduce

```sh
python3 experimental/scripts/search_m1_beta_pushforward_conductor_scan.py --selftest
python3 experimental/scripts/search_m1_beta_pushforward_conductor_scan.py --check \
  experimental/data/certificates/m1-beta-pushforward-conductor/m1_beta_pushforward_conductor_certificate.json
# larger fixed-e conductor trend (the extended finding):
python3 experimental/scripts/search_m1_beta_pushforward_conductor_scan.py --scan --e 12 --p-max 600
```

Status `EXPERIMENTAL / AUDIT` (finite numerical evidence, not a proof of
`(BETA_2)`). See `experimental/notes/m1/m1_beta_pushforward_conductor_extension.md`.
