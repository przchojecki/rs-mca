# M1 Beta-Pushforward Spectral Audit

**Status:** EXPERIMENTAL / FINITE SPECTRAL AUDIT.

This note records a counterexample-first finite check of the remaining
`(BETA_2)` input in `m1_kummer_weil_import_contract.md`.  It does not prove the
bounded-conductor estimate.  It tests the exact quotient-character object that
would fail if the good beta pushforward had a hidden geometrically constant
piece or a two-dimensional coherent component.

## Object Tested

For a quotient order `e | p-1`, let `Phi_e` be the quotient characters and let
`phi != 1`.  On the good beta cover from
`m1_depth_two_line_conic_resonance_reduction.md`, define

```text
G_{psi,phi}
  = sum_{(a,r) in G}
      psi(a) chi(rM(a,r)) (phi(beta_1)+phi(beta_2)),
```

with zero contribution on nonsplit fibers.  The `(BETA_2)` import asks for

```text
|G_{psi,phi}| <= C_beta(e) p
```

with `C_beta(e)` independent of `p`.  A counterexample search should therefore
look for `|G_{psi,phi}|` growing on the order of `p^2`, or even for rapidly
growing `|G_{psi,phi}|/p` across exact finite rows.

The M1 quotient-conic ledger also admits a weaker averaged target.  It is
enough to prove

```text
||G_e^circ||_F <= C_beta^avg(e) p,
```

where `G_e` is the quotient-label matrix of the good pushforward and
`G_e^circ` is its row/column-centered part.  The pointwise `(BETA_2)` estimate
implies this averaged estimate, but the averaged estimate alone already gives
`P_e=O_e(p^2)` and `M_e^o=O_e(p^2)` after adding the explicit bad-ledger
constant.  Thus the finite audit reports both the largest individual
coefficient and the centered Frobenius norm.

## Finite Scan

The verifier now scans every centered quotient-character pair in the existing
audited ratio-surface cases and reports three normalized maxima plus the
row/column-centered Frobenius norm of the exact good-pushforward quotient
matrix:

```text
(p, e, good_points, lower_points, exceptional_points,
 max_bad/p, max_good_pushforward/p, good_centered_frobenius/p,
 max_total_singular_trace/p)

(17,  8,   98, 27,  70, 2.7058823529, 1.1361004999,
 0.4744784060, 3.7647058824)
(17, 16,   98, 27,  70, 2.7058823529, 1.5728968500,
 0.4632352941, 3.8054236055)
(31,  6,  486, 55, 164, 2.1612903226, 2.3225806452,
 0.6634504452, 4.4838709677)
(31, 10,  486, 55, 164, 2.3436282530, 1.8416183853,
 0.5965213065, 3.9213647064)
(43,  6, 1568, 79, 270, 2.8139534884, 3.0697674419,
 1.1366043634, 4.8139534884)
(43, 14, 1568, 79, 270, 2.4536425998, 2.5116279070,
 0.8267620588, 4.7441860465)
```

Here `max_good_pushforward/p` is the direct finite proxy for `(BETA_2)`.  The
other two columns check the already proved ledger around it: the bad pieces
stay within the explicit `p+19(p-1)` bound, and the full singular trace is the
sum of the good pushforward and those controlled bad pieces.  The
`good_centered_frobenius/p` column is the averaged version of the same test:
the verifier checks the exact Parseval identity

```text
||G_e^circ||_F^2
  = e^{-2} sum_{psi,phi != 1} |G_{psi,phi}|^2,
```

where `G_e^circ` is the row/column-centered quotient matrix of the good
pushforward.  This is the same Fourier normalization used by the surrounding
singular-excess matrix ledger.

## Interpretation

The scan finds no hidden `p^2` component in the tested quotient rows.  The good
pushforward coefficients are p-scale in every audited case, with largest
observed coefficient ratio `3.0697674419` and largest centered-Frobenius ratio
`1.1366043634`, both at `(p,e)=(43,6)`.

The standalone verifier expands the scan to 20 rows through `p=127`, without
adding those larger rows to the broad line-conic verifier.  In the expanded
audit the largest individual coefficient ratio is

```text
max |G_{psi,phi}|/p = 4.8036624425 at (p,e)=(127,14),
```

while the largest centered-Frobenius ratio is still

```text
||G_e^circ||_F/p = 1.1366043634 at (p,e)=(43,6).
```

Thus the averaged target remains substantially smaller than the largest
individual coefficient in the finite rows, matching the point of the
`(BETA_2^avg)` reformulation.

This is useful only as evidence and as a regression guard.  It cannot certify
`(BETA_2)`: the proof still needs a bounded-conductor/no-constant-summand
argument for the explicit rank-two beta pushforward, or a direct proof of the
averaged `(BETA_2^avg)` matrix bound.  The value of the scan is that it tests
precisely that remaining analytic object, rather than a cruder two-variable
Kummer surface or the already controlled exceptional ledger.

## Verifier

Run:

```bash
python3 experimental/scripts/verify_m1_depth_two_line_conic_resonance_reduction.py
python3 experimental/scripts/verify_m1_beta_pushforward_spectral_audit.py
python3 experimental/scripts/verify_m1_beta_pushforward_spectral_audit.py --json
```

The relevant output line is
`ratio_surface_quotient_trace_reduction_checked`; its tuple entries now include
`max_good_pushforward/p` and `good_centered_frobenius/p` between `max_bad/p`
and `max_total_singular_trace/p`.  The standalone beta-pushforward verifier
checks a larger fixed grid and hard-codes the audited row values as regression
data.
