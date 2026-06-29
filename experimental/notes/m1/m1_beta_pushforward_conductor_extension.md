# M1 (BETA_2) Beta-Pushforward Conductor: Extended Growing-p Scan

**Status:** EXPERIMENTAL / AUDIT.

This note records an extended finite probe of the conditional M1 import
`(BETA_2)` (`m1_kummer_weil_import_contract.md`). `(BETA_2)` asserts that the
rank-two good beta-pushforward trace

```text
G_{psi,phi} = sum_{(a,beta,r) in Y_G(F_p)} psi(a) phi(beta) chi(d_UV)
```

has **bounded conductor**: `|G_{psi,phi}| <= C_beta(e) p` with `C_beta(e)`
independent of `p`. Equivalently the per-prime conductor ratio
`max_{psi,phi != 1} |G_{psi,phi}| / p` should stay bounded as `p -> infinity` at
fixed quotient order `e`.

New script: `experimental/scripts/search_m1_beta_pushforward_conductor_scan.py`.
It **reuses** the validated `good_pushforward_matrix` (the `e x e` label matrix
`G_e`) and `spectral_stats` (the 2D DFT giving `max|G_{psi,phi}|`) from
`verify_m1_beta_pushforward_spectral_audit.py` -- whose fixed `(p,e)` audit rows
only reach `p=127` -- and scans FIXED `e` over a much larger `p` range. Two
ratios are tracked: `beta2/p` (pointwise `(BETA_2)`, `phi != 1`) and
`two_sided/p` (the centered `psi != 1, phi != 1` block consumed by the
quotient-conic M1 ledger, `(BETA_2^avg)`).

## Findings

**(1) No counterexample to `(BETA_2)`.** Across the extended range
(`e in {6,12}`, `p` up to several hundred), the per-prime conductor ratio stays
in a bounded band (roughly `2`-`7.5`). There is **no linear-in-`p` growth** --
the ratio does not trend toward `p`-scale -- which is what a violation of the
bounded-conductor `(BETA_2)` would look like. So the extended scan found no
counterexample; it is consistent with `(BETA_2)` holding.

**(2) The audit's `p<=127` conductor constants are underestimates.** The
fixed-row audit reported maximum ratios around `beta2/p ~ 5.67` (at `(109,12)`)
and `two_sided/p ~ 4.80` (at `(127,14)`). Extending the scan finds strictly
larger values:

```text
e = 6 :  beta2/p  >= 6.42 (p=379),   two_sided/p >= 4.45 (p=283)
e = 12:  beta2/p  >= 7.50,           two_sided/p >= 7.50
```

(scanned range `p <= ~430`; the sample-maximum is still slowly creeping upward
at `p ~ 400`, so these are lower bounds on `C_beta(e)`, not the pinned constant).
So the empirical conductor `C_beta(e)` is larger than the `p<=127` audit shows,
and grows with `e` (e=6 vs e=12).

## Interpretation

The behavior -- per-prime ratios oscillating in a bounded band while the
*sample-maximum* creeps up slowly as more primes are sampled -- is the expected
signature of a genuinely bounded conductor that the original `p<=127` audit
simply did not sample widely enough to pin. It does not distinguish a bounded
constant from very slow (e.g. logarithmic) growth, so it is evidence for, not a
proof of, `(BETA_2)`. The actionable consequence for the M1 quotient-conic
ledger: the conductor constant `C_beta(e)` it must accept is larger than the
`p<=127` audit suggested (`>= 6.42` at `e=6`, `>= 7.50` at `e=12`), and any
eventual proof of `(BETA_2)` must yield a constant at least this large.

## Round-2 extension (large-p tails + fresh e=18,24; conductor stops climbing)

A second sweep extended the two families that already had data (`e=6`, `e=12`)
into the large-`p` tail and added two fresh quotient orders (`e=18`, `e=24`; now
machine-checked in the certificate via the `(181,18)` and `(97,24)` anchors).
The decisive question -- does the per-prime ratio `beta2/p = |G|/p` stay bounded
(supports `(BETA_2)`) or climb with `p` (would refute it)? -- comes out
**bounded**, and more sharply than round-1: the *sample maximum stops climbing*.

- **`e=12`, tail `p = 541..1009`:** `beta2/p` bounces in a flat band
  `{5.90 @541, 3.98 @673, 5.15 @757, 3.25 @853, 4.66 @937, 4.49 @1009}` with no
  upward drift; the value at the largest prime (`4.49 @ p=1009`) is *below* both
  `p=541` and the round-1 peak (`>= 7.50`, which sat at small `p`).
- **`e=6`, tail `p = 601..811`:** decays `4.10 @601 -> 3.48 @811`, both well
  under the round-1 peak (`>= 6.42`).
- **`e=18` (fresh):** `beta2/p` over `p=181..577` stays in `3.77-6.42`; peak
  `C_beta(18) >= 6.4248 @ p=379` (two-sided peak `5.9584 @ p=433`).
- **`e=24` (fresh):** `beta2/p` over `p=97..601` stays in `3.53-6.84`; peak
  `C_beta(24) >= 6.8426 @ p=313` (two-sided peak `6.4272 @ p=193`).

So across all four `e` the per-prime ratio stays in a bounded `~3-7` band, and --
the new point over round-1 -- for the two families now sampled into the `p~1000`
tail the sample maximum *stops setting records*: the large-`p` tail maxima sit
below the small-`p` peaks. That is the expected signature of a genuinely
`p`-bounded conductor `C_beta(e)` that the original `p<=127` audit (and even the
round-1 `p<=430` extension, where the sample-max was still creeping) simply
under-sampled -- not linear-in-`p` growth. No counterexample to `(BETA_2)`.

(Diagnostic: the right boundedness test is that `beta2/p` itself stays bounded
and stops setting records, which it does. `beta2/p^2 -> 0` is a weaker statement
that holds even under slow growth and is not used here.)

The sampled conductor lower bounds are `e`-dependent -- `C_beta(6) >= 6.42`,
`C_beta(12) >= 7.50`, `C_beta(18) >= 6.42`, `C_beta(24) >= 6.84` (each a sample
minimum over its scanned `p`-range, not a pinned constant) -- so the
quotient-conic ledger must accept an `e`-dependent constant at least this large.

Reproduce (round-2):
```sh
python3 experimental/scripts/search_m1_beta_pushforward_conductor_scan.py --scan --e 12 --p-min 541 --p-max 1009
python3 experimental/scripts/search_m1_beta_pushforward_conductor_scan.py --scan --e 18 --p-min 181 --p-max 580
python3 experimental/scripts/search_m1_beta_pushforward_conductor_scan.py --scan --e 24 --p-min 90  --p-max 610
```

## Reproduce

```sh
python3 experimental/scripts/search_m1_beta_pushforward_conductor_scan.py --selftest
python3 experimental/scripts/search_m1_beta_pushforward_conductor_scan.py --check \
  experimental/data/certificates/m1-beta-pushforward-conductor/m1_beta_pushforward_conductor_certificate.json
python3 experimental/scripts/search_m1_beta_pushforward_conductor_scan.py --scan --e 12 --p-max 600
```

## Limitations

Finite numerical evidence only (floating-point character sums). It neither
proves `(BETA_2)` nor a sharper conductor constant, and cannot rule out slow
growth outside the scanned range. Its concrete value is the corrected lower
bound on the empirical conductor and the regression guard that no `p`-scale
conductor growth appears up to the scanned primes.
