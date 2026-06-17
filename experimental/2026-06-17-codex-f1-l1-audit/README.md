# Codex F1/L1 Audit Dump, 2026-06-17

This folder contains companion material produced by Codex while auditing 5.5 Pro
and Opus 4.8 answers against the current RS-MCA / Proximity Prize repository.

No main paper files were edited. Treat this as experimental/audit material for
human review and later promotion.

## Contents

- `context/`: reusable context pack, theorem-label map, status ledger, backlog,
  prompt files, and label extractor.
- `audits/`: audited findings and route verdicts.
- `raw/`: raw model outputs plus `SHA256SUMS.txt`.
- `verifiers/`: small dependency-free Python checks for the finite F1/L1 packets.

## High-Level Banked Items

- `COUNTEREXAMPLE`: unrestricted same-numerator extension-line MCA lift is false.
- `COUNTEREXAMPLE`: raw arbitrary `Fib_U` locator local limit overcounts supports.
- `BANKABLE_LEMMA`: fixed-rate `sigma=1` F1 counterexample family over
  `F_p -> F_{p^2}`, plus a proved `sigma=2` degree-one tail-slice family
  showing fixed positive residual slack is still sub-reserve-dangerous.
- `BANKABLE_LEMMA / EXACT_NEW_WALL`: residual-slack reduction; balanced
  denominators are the remaining F1 wall.
- `BANKABLE_LEMMA`: monic-anchor balanced denominators reduce to a base-field
  readout via `hatE = lcm(E,E^tau)`.
- `BANKABLE_LEMMA`: extension-line MCA over `F/B` is exactly a
  multiplication-slice MCA problem for the `e`-interleaved base code, after
  choosing a `B`-basis of `F`.
- `BANKABLE_LEMMA / COUNTEREXAMPLE`: arbitrary balanced anchors are governed by
  the support-interpolation residue cloud, and can split a single monic-anchor
  locator readout class into different bad slopes; they also have a sunflower
  lower floor `floor((n-k)/sigma)`.
- `AUDIT`: Paper D universal cap remains conditional pending primary
  Crites-Stewart / ABF import verification.

## Suggested Verification

Run from repo root:

```bash
python3 experimental/2026-06-17-codex-f1-l1-audit/verifiers/\
verify_f1_extension_counterexample.py
python3 experimental/2026-06-17-codex-f1-l1-audit/verifiers/\
verify_f1_fixed_rate_slice.py
python3 experimental/2026-06-17-codex-f1-l1-audit/verifiers/\
verify_f1_sigma2_degree1.py
python3 experimental/2026-06-17-codex-f1-l1-audit/verifiers/\
verify_f1_arbitrary_anchor_split.py
python3 experimental/2026-06-17-codex-f1-l1-audit/verifiers/\
verify_l1_arbitrary_fiber_overcount.py
```

## Most Important Next Step

Attack the remaining F1 arbitrary-anchor balanced-denominator gap:

- either reduce arbitrary anchors in `def:residue` to a base-field readout, or
- find a finite balanced extension counterexample with arbitrary anchor data.
