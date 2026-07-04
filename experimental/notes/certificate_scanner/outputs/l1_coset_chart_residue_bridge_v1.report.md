# L1 coset-chart residue-line bridge v1

Status: `PROVED_LOCAL_COSET_CHART_RESIDUE_BRIDGE_NORMAL_FORM`.

## Result

Every capped full-petal coset-chart kernel set is either quotient-coset or emits a low-degree projective pair. After cancelling simultaneous active basepoints, the pair is an ordinary residue-line datum on the surviving quotient labels.

```text
w_r(a_i) = c_i f_r(a_i),
1 <= r < ell,
deg f_r, deg w_r <= t-2.
```

If `Z` is the simultaneous active zero set of the pair, cancellation by `prod_{i in Z}(Y-a_i)` gives denominator nonzero on the surviving labels and degree bound `<= active_count-2`.

Thus the bridge classifies every non-quotient kernel set by residue-line normal-form data. It does not prove that this residue-line family is paid or globally small.

## Verifier totals

```text
cases_checked: 8
subsets_checked: 76086
kernel_sets_checked: 187
minimal_kernel_sets_checked: 25
quotient_kernel_sets: 25
residue_bridge_kernel_sets: 162
minimal_quotient_kernel_sets: 23
minimal_residue_bridge_kernel_sets: 2
residue_bridge_certificates_checked: 162
residue_bridge_basepoint_certificates: 0
max_residue_bridge_basepoints: 0
unclassified_after_quotient_or_residue_bridge: 0
minimal_unclassified_after_quotient_or_residue_bridge: 0
optimized_crt_cross_checks: 12
synthetic_basepoint_count: 1
```

## Validation

```bash
python -m py_compile experimental/scripts/verify_l1_coset_chart_residue_bridge_v1.py
python experimental/scripts/verify_l1_coset_chart_residue_bridge_v1.py --check
python experimental/scripts/verify_l1_coset_chart_residue_bridge_v1.py --json
python -m json.tool experimental/data/certificates/l1-coset-chart-residue-bridge-v1/l1_coset_chart_residue_bridge_v1.json
git diff --check
```

## Non-claims

- Not a full L1 local-limit theorem.
- Not a quotient-only classification.
- Not an arbitrary-petal theorem.
- Not a primitive-vacancy theorem under the current stabilizer-primitive ledger.
- Not a proof that the residue-line family is paid or globally small.
