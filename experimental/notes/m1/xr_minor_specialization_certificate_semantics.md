# XR Minor-Specialization Certificate Semantics

Status: PROVED.

Source DAG node: `xr_minor_specialization_certificate_semantics`.

## Statement

In the XR light-triangle eliminant normal form, a certificate consisting of

- a maximal minor of the normal-form matrix; and
- one admissible specialization of the profile chart at which that minor
  evaluates nonzero

proves that the corresponding maximal minor is not the zero polynomial on the
profile chart. Consequently the profile eliminant is not identically zero on
that chart.

## Proof

Fix a light-triangle profile chart and the normal-form matrix. The chart
coordinates live in a coordinate ring `R`; if the chosen chart uses
denominators, admissibility means those denominators are chart units at the
specialization, and the determinant can be read after clearing those units.
Thus each maximal minor is represented by a well-defined polynomial function
on the chart.

Let `Delta` be the maximal minor named by the certificate, and let `a` be the
admissible specialization named by the certificate. Evaluation at `a` is a
ring homomorphism from the chart coordinate ring to the coefficient field:

```text
ev_a : R -> K.
```

If `Delta` were the zero polynomial in `R`, then every ring homomorphism would
send it to zero, so `ev_a(Delta) = 0`. The certificate asserts the opposite:
the determinant of the specialized minor is nonzero. Therefore `Delta` is not
the zero polynomial on the chart.

The light-profile eliminant is the collection of maximal minors controlling
rank stagnation in the normal form. Once one maximal minor is a nonzero
polynomial, not all maximal minors vanish identically. Hence the profile
eliminant is not identically zero on that profile chart.

## Non-Claims

This packet proves only certificate semantics. It does not produce the
profile-by-profile minor certificates and does not count points on the
remaining proper hypersurfaces.

## Replay

Regenerate:

```bash
python3 experimental/scripts/verify_xr_minor_specialization_certificate_semantics.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_xr_minor_specialization_certificate_semantics.py \
  --check experimental/data/certificates/xr-minor-specialization-certificate-semantics/xr_minor_specialization_certificate_semantics.json
```

The verifier checks note anchors and a toy polynomial determinant
specialization over `F_101`.
