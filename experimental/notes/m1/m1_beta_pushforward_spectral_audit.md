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

## Finite Scan

The verifier now scans every centered quotient-character pair in the existing
audited ratio-surface cases and reports three normalized maxima:

```text
(p, e, good_points, lower_points, exceptional_points,
 max_bad/p, max_good_pushforward/p, max_total_singular_trace/p)

(17,  8,   98, 27,  70, 2.7058823529, 1.1361004999, 3.7647058824)
(17, 16,   98, 27,  70, 2.7058823529, 1.5728968500, 3.8054236055)
(31,  6,  486, 55, 164, 2.1612903226, 2.3225806452, 4.4838709677)
(31, 10,  486, 55, 164, 2.3436282530, 1.8416183853, 3.9213647064)
(43,  6, 1568, 79, 270, 2.8139534884, 3.0697674419, 4.8139534884)
(43, 14, 1568, 79, 270, 2.4536425998, 2.5116279070, 4.7441860465)
```

Here `max_good_pushforward/p` is the direct finite proxy for `(BETA_2)`.  The
other two columns check the already proved ledger around it: the bad pieces
stay within the explicit `p+19(p-1)` bound, and the full singular trace is the
sum of the good pushforward and those controlled bad pieces.

## Interpretation

The scan finds no hidden `p^2` component in the tested quotient rows.  The good
pushforward coefficients are p-scale in every audited case, with largest
observed ratio `3.0697674419` at `(p,e)=(43,6)`.

This is useful only as evidence and as a regression guard.  It cannot certify
`(BETA_2)`: the proof still needs a bounded-conductor/no-constant-summand
argument for the explicit rank-two beta pushforward.  The value of the scan is
that it tests precisely that remaining analytic object, rather than a cruder
two-variable Kummer surface or the already controlled exceptional ledger.

## Verifier

Run:

```bash
python3 experimental/scripts/verify_m1_depth_two_line_conic_resonance_reduction.py
```

The relevant output line is
`ratio_surface_quotient_trace_reduction_checked`; its tuple entries now include
`max_good_pushforward/p` between `max_bad/p` and
`max_total_singular_trace/p`.
