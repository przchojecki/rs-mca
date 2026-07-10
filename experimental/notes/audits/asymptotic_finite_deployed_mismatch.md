# Asymptotic entropy frontier vs finite deployed rows

**Status:** EXPERIMENTAL / AUDIT
**Verdict vocabulary:** 6 × `NO ISSUE` / 0 × `OPEN GAP` / 0 × `COUNTEREXAMPLE_NEW_FLOOR`
**Object:** `experimental/asymptotic_rs_mca.tex` — `thm:frontier`, Stirling identity, `remark` (Finite adjacent rows), plus the four deployed adjacent pairs used by the integrated adjacent-margin ledger.
**Failure mode attacked:** agents.md adversarial checklist item *mismatch between asymptotic proof and finite deployed rows* (also *entropy-frontier algebra error*).
**Evidence type:** `INDEPENDENT_RECHECK`
**Not a counterexample, not a finite adjacent certificate, not a closed-ledger audit.**

## Primary finding

Independently recomputing the paper’s entropy–subfield crossing

```text
g*(rho, beta) = sup { g in [0,1-rho] : H2(rho+g) >= beta * g }
a*            = (rho + g*) * n
delta_env     = 1 - rho - g*
```

at the four deployed row parameters (`n = 2^21`, `rho = 1/2`, `beta = log2|B|` for KoalaBear and Mersenne-31 base primes) places the asymptotic agreement `a*` within distance **3** of every finite adjacent `a0`:

| row | beta ≈ | g* | a* | a0 | a0 − a* | delta_env | radius at a0 |
|-----|--------|-----|-----|-----|---------|-----------|--------------|
| KoalaBear MCA | 30.9887 | 0.03217339 | 1116048.50 | 1116047 | −1.50 | 0.46782661 | 0.46782732 |
| KoalaBear list | 30.9887 | 0.03217339 | 1116048.50 | 1116046 | −2.50 | 0.46782661 | 0.46782780 |
| Mersenne-31 MCA | 31.0000 | 0.03216172 | 1116024.02 | 1116023 | −1.02 | 0.46783828 | 0.46783876 |
| Mersenne-31 list | 31.0000 | 0.03216172 | 1116024.02 | 1116022 | −2.02 | 0.46783828 | 0.46783924 |

So the asymptotic threshold prediction of `thm:frontier` **agrees with the finite adjacent agreement table to O(1) positions** at the deployed length. This is a consistency check, not a proof of either side: it shows the named “mismatch” failure mode does **not** fire as a contradiction between the compact asymptotic paper and the finite row table.

## Secondary findings (all `NO ISSUE`)

1. **Paper scope is honest.** The finite-adjacent remark in `asymptotic_rs_mca.tex` states that the argument is asymptotic, absorbs `exp(o(n))` losses, and does **not** supply printed constants for finite deployed pairs. Byte-matched in the verifier’s paper-quote gate.
2. **`exp(o(n))` cannot silently close the finite spare margins.** With printed fail margins ≈ 22.20 / 22.01 / 3.26 / 3.07 bits, any overhead `2^{eps·n}` with `eps ≥ margin/n` already consumes the margin. That threshold is
   ```text
   eps_max ≈ 1.06e-5 bits/symbol  (KoalaBear MCA)
   eps_max ≈ 1.47e-6 bits/symbol  (Mersenne-31 list)
   ```
   So even a “small” linear-rate ledger overhead is fatal at `n = 2^21`. The asymptotic theorem and the finite adjacent certificate project remain separate, exactly as the paper claims.
3. **Prize challenge size fits the paper’s hypothesis.** `thm:frontier` assumes `log2(1/eps_n) = O(n)`. Prize targets use `lambda ∈ {100,128}`, both `O(1) ⊂ O(n)` at `n = 2^21`.
4. **In-paper sandwich lemmas (toy recompute).**
   - `lem:moment-max`: lower ≤ Gord_q ≤ upper on a three-level multiset.
   - `lem:q-sp`: `sum N(s)^2 ≤ (max N)·(sum N)` on a five-level toy.

## Attack table (mandated vocabulary)

| failure mode | object | verdict |
|--------------|--------|---------|
| entropy-frontier algebra error | g* + Stirling + a0 vs a* | **NO ISSUE** |
| mismatch asymptotic vs finite deployed | thm:frontier vs adjacent a0/a1 | **NO ISSUE** |
| asymptotic losses close finite margins | remark:finite + spare-margin budget | **NO ISSUE** |
| lem:moment-max sandwich | toy multiset | **NO ISSUE** |
| lem:q-sp second moment | toy N(s) | **NO ISSUE** |
| prize log2(1/eps) vs O(n) | challenge-normalization hypothesis | **NO ISSUE** |

## What this does *not* do

- Does not prove `thm:frontier` or the closed-ledger package `(C1)--(C9)`.
- Does not audit C9 / B1 / add-back / window-uniformity gaps treated by sibling open PRs.
- Does not produce a finite upper ledger `U(a0+1) ≤ B*`.
- Does not claim that matching `a*` to `a0` settles the prize finite margins — the spare-margin calculation shows the opposite: asymptotic `exp(o(n))` is still far too coarse for the few-bit finite gap.

## Reproducibility

```bash
python experimental/scripts/verify_asymptotic_finite_deployed_mismatch.py --emit-defaults
python experimental/scripts/verify_asymptotic_finite_deployed_mismatch.py --check
python experimental/scripts/verify_asymptotic_finite_deployed_mismatch.py --tamper-selftest
python -m py_compile experimental/scripts/verify_asymptotic_finite_deployed_mismatch.py
python -m json.tool experimental/data/certificates/asymptotic-finite-mismatch/asymptotic_finite_deployed_mismatch.json
```

Certificate: `experimental/data/certificates/asymptotic-finite-mismatch/asymptotic_finite_deployed_mismatch.json`
Verifier: `experimental/scripts/verify_asymptotic_finite_deployed_mismatch.py` (stdlib only).

## Self-red-team

Could this be overread as “the asymptotic proof is confirmed for deployed rows”? No: the note’s primary finding is only O(1) agreement of the crossing location, and the secondary finding explicitly quantifies that `exp(o(n))` overhead destroys the finite spare margins. Could the float bisection of g* be the only evidence? The a0/a* comparison is stable under large tolerance (distance ≤ 3 positions out of `n = 2^21`), and the paper-quote gate is exact string match. Could the adjacent a0 table be wrong? The verifier cross-links the integrated `capg_adjacent_pair_margins` certificate when present; the four a0 values appear there.
