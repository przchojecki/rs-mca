# C9 payment reduction map (W49–W53 hard-attack chain)

## Status
EXPERIMENTAL / AUDIT. **Overall verdict: OPEN**, sharply localized.
The easy closing mechanism is **dead**. One razor remains.

This note is a **synthesis** of already-filed, designer-verified results
(W49–W53). It does **not** claim the Sidon payment is settled either way.

## Phase 0 (chain re-check, this wave)
Local re-run of worktree verifiers (2026-07-10):

```text
W49 image_normalized_sidon_attack     RESULT: PASS  verdict MEASURED-SUPPORT  payload 594159a6…
W50 sidon_special_case_proof          RESULT: PASS  verdict PROVED-SPECIAL    payload a017e945…
W51 maxfiber_control_proof            RESULT: PASS  verdict PROVED-SPECIAL    payload e919e8f8…
W52 r2_maxfiber_proof                 RESULT: PASS  verdict PROVED-SPECIAL    payload f7a54058…
W53 largefiber_lowenergy_hunt         RESULT: PASS  verdict MEASURED-SUPPORT  payload f0e1f3be…
W53 largefiber_energy_proof           RESULT: PASS  verdict REDUCED           payload 8baa4e87…
```

## The chain (one status per step)

| Step | Content | Status | PR / wave |
|------|---------|--------|-----------|
| 0 START | `ass:image-normalized-sidon-input`: image-normalized Sidon/Fourier payment at `barN=\|Ω°\|/\|im Φ\|` — load-bearing open input (b); residual of (c) lands here after κ=Θ(n) | **OPEN (assumption)** | B1 notes / packaging; W49 attack |
| 1 REDUCE | Payment rate ≤ log(max_f/barN)/N so payment **reduces** to low-energy **max-fiber control** (max low-energy f_s/barN = exp(o(N))). Boundary: injective/singleton trivial | **REDUCED** (Lemma II) | **#575** (W50-M2) |
| 2 LOCALIZE R | R≥m ⇒ Φ injective (Newton–Girard) ⇒ max f=1; difficulty pinned to **R&lt;m** deep charts | **PROVED-SPECIAL** (R≥m) | **#577** (W51-M2) |
| 3 LOCALIZE m | R=2: f_s ≤ N^{m−2} by induction ⇒ **fixed m** discharged; useless at **m=Θ(N)** linear density | **PROVED-SPECIAL** (fixed m) | **#579** (W52-M1) |
| 4 CRUX measure | At R=2 linear density, largest fibers are **near the Sidon floor** (Δ~2/f): **106/108** measured. Natural closing law “large fiber ⇒ high additive energy” **fails**. No formal CE only because toy N≤16 is not exp-large | **MEASURED — mechanism fails** | **#581** (W53-M1) |
| 5 CRUX theory | CS gives only Δ≥1/f (→0 as f grows); Sidon floor Δ~2/f is the energy minimum. Closing needs a bound **beating Sidon** on R=2 fibers | **REDUCED** | **#582** (W53-M2) |
| 6 Supporting | W49 payment gate MEASURED-SUPPORT on toys; W50 margin attack MEASURED-ROBUST; W51/W52 deep observability fixed | MEASURED-SUPPORT | #573–#580 |

Also: W49 MEASURED-SUPPORT on finite payment gate; W50-M1 MEASURED-ROBUST thin-margin; W51-M1 MEASURED-SUPPORT deep (empty at thr=0.5, fixed later); W52-M2 observability fixed.

## The razor (precise remaining sub-problem)

**Question.** Does there exist an R=2 fiber of Φ=(∑t, ∑t²) at **genuine linear density**
(m/N ≥ α &gt; 0 fixed) that is **both**

1. **near-Sidon:** Δ_s ≤ thr (e.g. within o(1) of the Sidon floor ~2/f), **and**
2. **exp-large:** f_s ≥ exp(η N)·barN for some fixed η&gt;0?

| Answer | Consequence |
|--------|-------------|
| **YES** | `ass:image-normalized-sidon-input` fails on this route (payment fails) |
| **NO** | reduced max-fiber input holds on this route ⇒ payment holds via W50 Lemma II |

This is pure additive combinatorics: near-Sidon families of constant-weight vectors
sharing **two** power-sum constraints, at linear density.

## What would close it

1. **Bound:** Near-Sidon subsets of any single R=2 fiber at m=Θ(N) have size exp(o(N))
   (or Δ ≥ f^{−c} for some c&lt;1 on every large fiber).
2. **Or construction:** An explicit near-Sidon exp-large R=2 fiber at linear density
   (shows the payment assumption fails on this route).

Concrete attack angles beyond toy N≤16 (for later waves): counting DP on
(k, sum, sumsq) to N~60–100; Gauss/Kloosterman–Weil bounds on the energy of
quadratic level sets; BSG on the 2-constraint slice.

## Overall verdict

```text
OPEN — sharply localized.
Proved/reduced chain: payment → max-fiber → R<m → R=2 fixed-m proved.
Easy mechanism "large ⇒ high energy" is FALSE (near-Sidon largest fibers).
Remaining razor: near-Sidon AND exp-large on R=2 linear-density fibers?
```

## Dual routes (this capstone)

- **generator route:** synthesize filed chain with PR numbers + re-run stored certs
- **checker route:** independent re-execution of W49–W53 `--check` scripts (all PASS above)

## Nonclaims

- Does **not** settle the C9 payment at deployed scale.
- Does **not** replace Papers A–D.
- PR numbers are designer-filed labels from the automation thread; statuses match
  the local re-check verdicts listed in Phase 0.

## Reproducibility

```text
# re-run any step verifier in its worktree, e.g.
py -3.13 experimental/scripts/verify_r2_maxfiber_proof.py --check
py -3.13 experimental/scripts/verify_largefiber_lowenergy_hunt.py --check
# this wave
py -3.13 experimental/scripts/verify_c9_reduction_map.py --check
```
