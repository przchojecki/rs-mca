# Audit of PR #100: Cycle120 gate arithmetic + list→MCA implication

- **Status:** AUDIT / **arithmetic VERIFIED, result CONDITIONAL** on finite imports.
- **Agent/model:** Claude Opus 4.8 (L2 loop, branch `allen/l2-x1-interleaved-mca`).
- **Date:** 2026-06-24.
- **Target:** PR #100 (`notes/m1/m1_cycle120_gate_arithmetic_contract.md` and the
  `supportwise_mca_bridge` step, Codex) — the M1 Cycle120 ABF-facing candidate.
- **Verifier:** `scripts/verify_audit_pr100_cycle120_gate.py` (independent
  big-integer recomputation; does not reuse Codex's verifier).

## Scope

I audited **only the deterministic gate/arithmetic layer and the implication
logic** — the part that does not depend on the large finite computation. The row:
`K=F_17^32`, `H=<theta>`, `|H|=n=512`, `C=RS[K,H,256]`, `delta=125/256`,
`N=52,747,567,092`.

## Verdict: the arithmetic is exactly correct; the cap is correctly CONDITIONAL

**Independently verified (15/15 checks PASS):**
- closed agreement threshold `(1-delta)n = (131/256)·512 = 262`; distance radius
  `delta·n = 250`; Cycle116 agreement `262` meets the closed threshold;
  Cycle119 agreement `263` gives distance `512-263 = 249 < 250`, and
  `263 = (1 - 249/512)·512`;
- parameter envelope: `17^32 < 2^256`, `|H| = 2^9`, rate `256/512 = 1/2`,
  `k = 256 <= 2^40`;
- the crux denominator comparison, exact:
  `17^32 = 2367911594760467245844106297320951247361`,
  `floor(17^32 / 2^128) = 6`, `N = 52,747,567,092 > 6`, equivalently
  `N · 2^128 > 17^32`, so `N/|K| > 2^-128`; density `log2(N/17^32) = -95.18`;
- the **implication logic**: under the support-wise MCA definition (sample
  `gamma <- K`, count bad slopes with a common support `|S| >= 262`), if one pair
  `(f1,f2)` has `>= N` bad `gamma`, then `emca(C,125/256) >= N/|K| > 2^-128`,
  ruling out safety at the endpoint (`delta*_C <= 125/256`); and the Cycle119
  strict transfer (agreement `263`) sharpens this to `delta*_C <= 249/512 < 125/256`
  since `249/512 < 125/256`. This `LD_sw → emca` step is the same normalization
  as the deep-point/CA-MCA bridges (`notes/x1`, `notes/f1`), and it checks.

The `emca >= N/|K|` step is exactly the support-wise definition's bad-slope
density; it is sound. The closed-vs-strict ball subtlety is handled correctly:
under the printed ABF `|S| >= (1-delta)n` convention, agreement `262` already
suffices, and `263` is the optional strict strengthening.

**NOT verified here (the conditional imports — the real gates before any claim):**
1. **`N = 52,747,567,092` itself** — the Cycle84 finite occupancy/census. This is
   Danny's large generated computation; neither Codex's contract nor this audit
   independently reproduces it. *This is the critical remaining gate.*
2. The **Cycle116/Cycle119 fixed-jet transfer proofs** — that a pair `(f1,f2)`
   with `>= N` bad `gamma` at agreement `262`/`263` actually exists.
3. The **official ABF ePrint 2026/680 wording** (row gates, sampler, smoothness,
   support-wise predicate, closed threshold) — checked only against the PR #96
   PDF extract; direct ePrint retrieval is Cloudflare-blocked from this env.
4. `H=<theta>` smoothness/generator certification.

## Assessment of Codex's labeling

Codex's status labels are **accurate and conservative**: the contract is marked
CONDITIONAL / SOURCE-CHECK-NEEDED, the Nonclaims section explicitly disclaims an
accepted prize solution / exact `delta*_C` / independent validation of the
imports, and every import is enumerated. No overclaiming. The arithmetic contract
does exactly what it says: it is the deterministic layer those imports would feed.

## Bottom line

The Cycle120 **gate arithmetic and the list→MCA implication are correct and
independently reproduced**. The candidate's force rests entirely on the
**unreproduced finite count `N` and the transfer proofs** — so it is a
well-formed *conditional* prize-facing counterexample candidate, not (yet) a
verified result. The highest-leverage next step for promotion is an **independent
reproduction of the Cycle84 count `N`** and a human-readable Cycle116 transfer
proof — precisely the inputs the maintainer has been asking Danny for.

## Reproducibility
```bash
python3 experimental/scripts/verify_audit_pr100_cycle120_gate.py
python3 experimental/scripts/verify_audit_pr100_cycle120_gate.py --json
```
