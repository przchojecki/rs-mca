# M0 Prize MCA Definition Freeze

- **Status:** AUDIT.
- **Agent/model:** Codex acting autonomously for AllenGrahamHart.
- **Scope:** repository-side conventions for the prize-facing
  `RS[F_17^32,H,256]` row and the v12 Hankel packet pipeline.

This note supplies the M0 convention freeze requested in `towards-prize.md`.
It records the object currently used by the repository and points to the notes
or certificates that consume it.  It is not a prize-resolution claim, and it
does not replace maintainer review of the official sampler.

## Frozen Object

| item | frozen repository convention | current caveat |
| --- | --- | --- |
| prize-facing row | `C = RS[F_17^32,H,256]`, `n=512`, `k=256`, `q_line=17^32` | The row descriptor, not this note, is the arithmetic source of truth for `H`. |
| support-wise MCA predicate | Count line slopes with an agreement support `S`, `|S| >= a`, whose line value is codeword-explained on `S` but whose pair is not same-support contained in `C^{equiv 2}`. | The predicate-level match to the external sampler remains an audit item, as in `audit_step1_sampler_reconciliation.md`. |
| same-support noncontainment | Noncontainment is tested on the same support `S`; a counted slope is not interchangeable with ordinary list decoding or line decoding without a bridge theorem. | Use `experimental/notes/m2/m2_line_decoding_mca_bridge.md` when translating to line-decoding language. |
| finite affine slope sampler | Slopes are `z in F_17^32`; denominator is `q_line=17^32`; the budget is `floor(q_line/2^128)=6`. | This is the default sampler for finite-slope `LD_sw` and M3 finite root tables. |
| projective sampler | Add the endpoint `[0:1]`; denominator is `q_line+1`; for this row `floor((q_line+1)/2^128)=6` as well. | Projective-infinity contributions are accounted separately from finite affine roots. |
| endpoint convention | Closed integer radius `r=n-a`; real-radius grid uses `a=ceil((1-delta)n)=n-floor(delta n)`. | For the high-agreement row the largest safe closed grid radius is `r=5`; `r=6` is the first unsafe integer radius. |
| closed grid versus supremum | The safe real interval is open at the first unsafe endpoint: `[0,6/512)`. | Do not restate this as safety at `delta=6/512`. |
| `q_gen` | Generated-field entropy for locator/list objects. | Do not use `q_gen` to pay MCA line-slope denominators unless a theorem supplies the transfer. |
| `q_line` | Slope field for MCA/CA/line-decoding packets; here `q_line=17^32`. | Finite and projective samplers print different denominators but the same `2^-128` budget in this row. |
| `q_chal` | Protocol challenge field. | Not used by M1/M3/M4 Hankel proof packets unless a protocol ledger explicitly imports them. |

## Convention Consumers

| repo theorem or packet | object consumed | sampler / denominator | endpoint convention | status |
| --- | --- | --- | --- | --- |
| `experimental/notes/thresholds/high_agreement_threshold_package.md` | finite-slope `LD_sw(C,a)` and M2 bridge arithmetic | finite affine `q_line`; projective variant recorded separately | closed integer radius, open supremum endpoint | PROVED-COMPILER-ARITHMETIC / AUDIT |
| `experimental/notes/audits/audit_step1_sampler_reconciliation.md` | reconciliation of repository support-wise MCA with survey anchors | finite and projective denominators compared | closed-ball arithmetic audited | AUDIT |
| `experimental/notes/m2/m2_line_decoding_mca_bridge.md` | bridge from support-wise MCA numerator to line-decoding language | finite affine denominator unless stated otherwise | uses `a=ceil((1-delta)n)` | PROVED locally, subject to stated object match |
| `experimental/data/certificates/hankel-smoke-f17-506-507/` | settled high-agreement row packet | finite-slope support-wise MCA numerator table | `A=506` unsafe, `A=507` safe | AUDIT / format test |
| `scripts/check_aperiodic_eliminant_packet.py` | v10 proof-packet schema validation | reads declared packet sampler and numerator fields | validates arithmetic fields, not ideal membership | AUDIT checker |
| `experimental/data/certificates/hankel-f17-32-m3-*` | M3 finite regular-Hankel root tables and local lemmas | finite affine roots over `F_17^32`; projective endpoint only when printed | agreement `A`, radius `r=n-A` | PROVED/AUDIT per packet |
| `experimental/data/certificates/hankel-f17-32-m3-m4-regular-bucket-synthesis/` | M4 decision table after tangent and local M5 filters | separates finite roots from projective infinity | same `A` and closed-radius convention | AUDIT synthesis |
| `experimental/data/certificates/hankel-f17-32-m3-one-spike-m4-budget/` | local one-spike finite/projective budget table | finite numerator `0`; projective numerator `1`; both budgets `6` | printed finite and projective denominators | PROVED for that family |
| L1/F1/L2 locator and extension notes | generated-field, base-field, or interleaved-list objects | use `q_gen` or extension fields only when stated | not an MCA slope sampler by default | separate theorem lanes |

## Use Rule

When adding a prize-facing certificate, print:

```text
object
sampler = finite_affine or projective
q_gen, q_line, q_chal as applicable
agreement A and radius r=n-A
closed-grid or supremum statement
which paid ledgers were subtracted
```

If any row cannot be filled without importing a theorem, mark it as a residual
or conditional dependency instead of silently merging ledgers.
