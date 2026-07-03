# Lean Certification Map

Status: Tier-1 / stdlib-only arithmetic certificates.

Scope: this map records exactly which Lean theorems certify the finite
submission-gate arithmetic requested in
`experimental/notes/roadmaps/wp_detail/wp1_1_wp1_2_submission_and_lean.md`.
The Lean package deliberately proves only `Nat`, `Int`, and normalized `Rat`
ledger facts.  Reed-Solomon, finite-field, polynomial, and protocol statements
remain cited proofs, verifier outputs, or typed targets.

Build command:

```bash
cd experimental/lean/rs_mca_formalization
lake build
```

## Tier-1 Gate Certificates

| Claim consumed by the submission note | Lean certificate | Source claim | Status |
| --- | --- | --- | --- |
| Positive lower slack in the field-count gate: `6 * 2^128 + 326217393234836465063858652730341978625 = 17^32`. | `RsMca.f17_lower_add_certificate` | WP-1.2 gate bracketing addition certificate. | Lean-certified |
| Positive upper slack in the field-count gate: `17^32 + 14064973686101998399515954701426232831 = 7 * 2^128`. | `RsMca.f17_upper_add_certificate` | WP-1.2 gate bracketing addition certificate. | Lean-certified |
| The printed bracket `6 * 2^128 < 17^32 < 7 * 2^128` follows from positive slack witnesses. | `RsMca.f17_bracket_from_add_certificates` | WP-1.2 gate bracketing. | Lean-certified |
| `floor(17^32 / 2^128) = 6`. | `RsMca.f17_BQ_eq`; also `RsMca.field_floor`. | WP-1.2 staircase budget `B_Q = 6`. | Lean-certified |
| The budget lies inside the exact tangent range cap: `6 <= 85 = (512 - 256) / 3`. | `RsMca.f17_budget_inside_tangent_cap` | WP-1.2 staircase arithmetic. | Lean-certified |
| Agreement endpoints lie in the exact tangent range. | `RsMca.f17_506_in_range`; `RsMca.f17_507_in_range`; `RsMca.tangentExact_iff_radius`. | Tangent staircase exact-range gate. | Lean-certified |
| Endpoint staircase values: agreement `507` has numerator `6`, agreement `506` has numerator `7`. | `RsMca.f17_LDsw_507`; `RsMca.f17_LDsw_506`; `RsMca.f17_staircase`. | WP-1.2 safe/unsafe adjacent endpoint. | Lean-certified |
| Radius bookkeeping: `r = n - a` maps `507 -> 5` and `506 -> 6`. | `RsMca.f17_radius_endpoints`; `RsMca.f17_endpoint_conversions`. | WP-1.2 endpoint conversion. | Lean-certified |
| Normalized rational endpoint conversion: `5/512 < 6/512 = 3/256`. | `RsMca.f17_endpoint_ratios`; `RsMca.f17_endpoint_conversions`. | WP-1.2 Rat endpoint facts. | Lean-certified |
| General high-agreement numerator monotonicity in the radius. | `RsMca.lineNumerator_mono`; `RsMca.curveNumerator_mono_radius`; `RsMca.totalNumerator_mono_radius`. | High-agreement ledger arithmetic. | Lean-certified |
| Line plus one interleaved-list numerator is `r + 2`. | `RsMca.totalNumerator_line_plus_list`; `RsMca.lineListSafe_iff`. | WP-1.2 common-denominator ledger arithmetic. | Lean-certified |
| Projective denominator `17^32 + 1` has the same integer upper gate. | `RsMca.field_count_gate_proj`. | Finite-threshold projective-slope variant. | Lean-certified |

## Typed Targets And Non-Claims

| Claim boundary | Lean artifact | Classification |
| --- | --- | --- |
| Deep-point identity and a-regular collapse require finite-set and finite-field infrastructure. | `RsMca.DeepPointIdentity`; `RsMca.ARegularCollapse`. | Typed target, not proved here. |
| A6 quotient-floor semantics are bridged by the Python verifier and the parity-split Lean arithmetic. | `RsMca.QuotientFloorBridge`; `RsMca.qf_half_closed`. | Conditional bridge plus Lean-certified arithmetic. |
| F1 sigma-one extension-line badness requires polynomial/RS semantics over genuine finite fields. | `RsMca.F1Ext.F1ExtensionSigmaOneBridge`. | Typed target, verifier-backed outside Lean. |
| The BETA_2 analytic conductor bound is an l-adic/cohomological input. | `RsMca.BetaTwo.BetaTwoConductorBound`. | Typed target, not stdlib-certifiable. |

## Audit Rule

For a dossier row to be called Lean-certified by this map, its claim must be
one of the tier-1 arithmetic rows above or a direct conjunction of those rows.
All other dossier claims must be marked `harness-verified`, `cited-proof`, or
`conditional(...)`; this map is not a blanket proof of MCA/list decoding,
finite-field semantics, or protocol soundness.
