# Protocol Ledger Rewrite Template

- **Status:** AUDIT
- **Agent/model:** Codex acting autonomously through AllenGrahamHart
- **Date:** 2026-06-17
- **Supports:** `tex/proximity_blueprint_v3.tex` P1/M4 and
  `tex/snarks_v4.tex` protocol-ledger accounting.

## Purpose

This template is for rewriting a concrete FRI/WHIR/STIR-style reduction in the
ledger language used by Paper C. It is not a proof by itself. It is a checklist
for making every consumed code object, field denominator, list term, MCA term,
query branch, and assumption explicit before a protocol-specific soundness
claim is promoted into a paper.

## Header

```text
Protocol:
Reference:
Reduction step or round:
Agent/model:
Date:
Status: PROVED / CONDITIONAL / CONJECTURAL / EXPERIMENTAL / AUDIT
```

## Code Object Ledger

| Field | Value |
| --- | --- |
| Base code `C` |  |
| Evaluation domain `D` |  |
| Domain type | subgroup / coset / coset union / affine / other |
| `n = |D|` |  |
| `k` |  |
| Rate `rho = k/n` |  |
| Minimum distance convention | relative / absolute |
| Interleaving arity `mu` |  |
| Fold or batch arity |  |
| Lifted or extension code? | yes / no |
| Code-family theorem used | Johnson / GGR / folded / subspace-design / conjectural |

## Field Ledger

| Field role | Symbol | Value | Justification |
| --- | --- | --- | --- |
| Generated field of the domain | `q_gen` |  |  |
| Line or combination challenge field | `q_line` |  |  |
| Protocol challenge field | `q_chal` |  |  |
| Extension degree over generated field | `[F:B]` |  |  |
| Does the locator problem genuinely lift? | yes / no / unknown |  |  |
| Are challenge slopes sampled outside `q_gen`? | yes / no |  |  |

Field-accounting rule:

```text
Use q_gen for entropy/list locator ledgers unless the code and locator data
are genuinely lifted. Use q_line or q_chal only for the line/MCA denominator
when a theorem justifies that field of slopes.
```

## Radius and Reserve Ledger

| Quantity | Value |
| --- | --- |
| Target radius `delta` |  |
| Capacity gap `eta = 1-rho-delta` |  |
| Generated-field entropy floor `tau*(rho,q_gen)` |  |
| Active quotient profile `Q_D(eta)` |  |
| Known failure-ladder gap |  |
| Universal-cap floor |  |
| Chosen safety margin |  |

Pass/fail statement:

```text
The reserve clears / does not clear the generated-field entropy floor,
active quotient floors, known MCA failure ladders, and universal-cap floor.
```

## List Ledger

| Item | Value |
| --- | --- |
| Base-code list bound `Lhat(delta)` |  |
| Interleaved-list bound `Lhat_mu(delta)` |  |
| Bound source | theorem / script / conjecture |
| List-over-field term | `Lhat_mu(delta) / q_line` |
| Target bits for list branch |  |
| Status | PROVED / CONDITIONAL / CONJECTURAL / EXPERIMENTAL / AUDIT |

Required citation or artifact:

```text
Theorem/script/certificate:
Command or exact parameters:
```

## MCA or Line-Decoding Ledger

| Item | Value |
| --- | --- |
| Consumed object | CA / MCA / line-decoding / curve-MCA |
| Line family | affine / polynomial generator / protocol-specific |
| MCA numerator or packing bound |  |
| Denominator field | `q_line` / `q_chal` / other |
| MCA-over-field term | numerator / denominator |
| Target bits for MCA branch |  |
| Extension-line status | theorem / assumption / open F1 / not used |
| Status | PROVED / CONDITIONAL / CONJECTURAL / EXPERIMENTAL / AUDIT |

Required citation or artifact:

```text
Theorem/script/certificate:
Command or exact parameters:
```

## Query Branch Ledger

For an independent spot-check branch with per-query survival probability `s`,
record:

| Item | Value |
| --- | --- |
| Per-query survival `s` |  |
| Query count `t` |  |
| Query error `s^t` |  |
| Target bits for query branch |  |
| Independence or sampling model | with / without replacement / other |
| Status | PROVED / CONDITIONAL / CONJECTURAL / EXPERIMENTAL / AUDIT |

If the branch uses the toy bound from Paper C, write the exact inequality:

```text
t >= lambda_query / log2(1/s)
```

## Composition Ledger

| Branch | Error term | Bits | Status |
| --- | --- | --- | --- |
| List branch |  |  |  |
| MCA or line branch |  |  |  |
| Query branch |  |  |  |
| Fiat-Shamir / transcript branch |  |  |  |
| Commitment branch |  |  |  |
| Zero-knowledge or masking branch |  |  |  |
| Total by union bound |  |  |  |

Required final statement:

```text
The protocol step is certified at <= 2^-lambda total error under the listed
PROVED/CONDITIONAL/CONJECTURAL assumptions.
```

## Assumption Ledger

| Assumption | Status | Where used | Replacement if false |
| --- | --- | --- | --- |
| Generated-field entropy rule |  |  |  |
| Quotient-profile local limit |  |  |  |
| Interleaved-list theorem or bound |  |  |  |
| MCA local limit / line-decoding theorem |  |  |  |
| Extension-line lift F1 |  |  |  |
| Polynomial-generator or curve-MCA theorem |  |  |  |
| Protocol-specific sampling independence |  |  |  |

## Audit Questions

1. Does the reduction consume list size, CA, MCA, line-decoding, or curve-MCA?
2. Is the field denominator `q_gen`, `q_line`, or `q_chal`, and why?
3. Does an extension challenge field only change slopes, or does it genuinely
   lift the locator/list object?
4. Are interleaved lists charged as a base-code product bound, a direct
   enumeration, or a theorem-backed bound?
5. Are all conjectural statements clearly separated from proved branches?
6. Are the theorem labels, scripts, commands, and parameter values enough for a
   later agent to reproduce the ledger?

## Promotion Rule

Do not promote a completed ledger into `tex/` until every row has either a
theorem citation, a script certificate, or an explicitly named assumption with
status `CONDITIONAL`, `CONJECTURAL`, or `AUDIT`.
