# Independent audit: L1 Conjecture 1 (full-list quotient-budgeted bound)

- **Status:** AUDIT / INDEPENDENT CORROBORATION (mechanism, small-model). Not a
  proof, not a re-run of Codex's scanner.
- **Agent/model:** Claude Opus 4.8 (independent audit, branch `allen/l1-audit`).
- **Date:** 2026-06-26.
- **Target:** Codex's L1 crux, `l1_full_list_quotient_proof_program.md` **Conjecture
  1**, the bound everything on the positive side roots on (the X1 `conj:B` proof and
  the L2 sharp saving both reduce to it). This is the sanctioned interaction with the
  L1 lane (independent audit only); it does not edit Codex's L1 notes/branches.

## The claim audited

For `RS[F_q,H_n,k]`, `s = k+σ`, above the reserve, the **actual** Reed–Solomon list
`ImgFib_U(s) = {deg-<k P : |{x: U(x)=P(x)}| ≥ s}` is split by the **multiplicative
stabilizer** of the agreement set `A_P(U)={x:U(x)=P(x)}`:
```
Stab(P;U) = { h in H_n : h·A_P(U) = A_P(U) },   Q_d^list(U,s) = #{P : |Stab(P;U)|=d}.
```
**Conjecture 1:** the aperiodic (trivial-stabilizer) remainder is polynomial,
```
Q_1^list(U, k+σ) ≤ n^B,
```
with quotient-periodic mass (`|Stab|=d>1`) charged separately to `Σ_{d>1} Q_d^list`.

## Independent verifier (`verify_l1_fulllist_independent_audit.py`)

A separate small-model implementation (own RS enumeration + own stabilizer routine),
full enumeration of the deg-`<k` list, run on random / quotient-periodic / monomial /
gluing / random-sweep words, with these checks:

1. **Stabilizer is a subgroup** — `|Stab(P;U)|` divides `n` for every listed `P`
   across every word. **Holds** (structural sanity of the split).
2. **The mechanism — quotient mass routes to `Q_{d>1}`, leaving `Q_1` small.**
   Concrete witness (`p=17, k=3, s=6`): a quotient-periodic word has list size `6`,
   split `Q_1=2` (aperiodic) + `Q_2=4` (period-2 stabilizer) — the large list is
   quotient-periodic mass, **not** aperiodic mass. **Holds** across configs: the big
   lists of periodic words land in `Q_{d>1}`. This is the structural heart of the
   conjecture and it checks out independently.
3. **Aperiodic-remainder hunt.** Worst `Q_1^list` over all tested families was `3`
   (at the main configs) — no family produced a large aperiodic list.
4. **Larger-`n` scaling** (`k=2, s=5`, `n=18..30`): worst aperiodic `Q_1` =
   `3, 4, 6, 9` — **roughly linear in `n`** (`≤ n`), i.e. polynomial, no super-poly
   blow-up.

## Honest scope / limits

- This **corroborates the stabilizer mechanism** of Conjecture 1 (the quotient/aperiodic
  split behaves exactly as claimed) and finds **no aperiodic pathology** in the tested
  families — an independent second implementation agreeing with the conjecture's
  structure.
- It is **not** an above-reserve test. The conjecture is asserted above the reserve
  (`σ ≥ C n/log n`); full enumeration of the list is only feasible for small `k`
  (`k=2,3`), which is the low-rate / below-reserve regime. The linear `Q_1` growth in
  step 4 is the expected below-reserve list inflation (fixed small `s` as `n` grows),
  **not** a counterexample — and it stays polynomial. A genuine fixed-rate
  (`k ≈ ρn`) test needs `q^k` exponential enumeration, out of small-model reach.
- Therefore: **independent corroboration of the mechanism**, not of the asymptotic
  bound. The asymptotic `Q_1^list ≤ n^B` remains Codex's proof obligation
  (proof program Theorems 21–22 etc.).

## Reproducibility
```bash
python3 experimental/scripts/verify_l1_fulllist_independent_audit.py
```
