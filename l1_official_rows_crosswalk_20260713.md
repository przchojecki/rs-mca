# L1 crosswalk — imgfib (PROVED 2026-07-13) vs upstream Assumption
# "Field-aware locator local limit" (rs-mca archived/snarks_v4.tex,
# ass:locator) and the towards-prize.md L1 target

Prepared at the maintainer's request before any upstream claim.
Upstream pin: rs-mca @ 9262f63c (snarks_v4.tex lines ~352-392;
towards-prize.md "L1. Generated-Field Locator Local Limit").

## Clause-by-clause

| # | Upstream clause (ass:locator) | Our imgfib chain | Verdict |
|---|---|---|---|
| 1 | For every received word U | "For ALL received words U" — and clause (P)'s atlas is WORD-INDEPENDENT (stronger: one atlas serves all words) | MATCH (ours stronger) |
| 2 | \|ImgFib_U(k_n+σ_n)\| ≤ n^{B_L}, B_L a fixed constant | #ImgFib_U(k+σ) ≤ n^B with B explicit per row (petal budget composes to concrete exponents) | MATCH at rows; upstream's single uniform B_L across an infinite family is not claimed |
| 3 | Entropy condition σ_n log₂ q_n ≥ (1+ε) log₂ C(n, k_n+σ_n) ("the corrected reserve") | Verbatim hypothesis of the imgfib statement | MATCH |
| 4 | Scale clause σ_n ≥ C·n/log₂ n | Not separately stated. IMPLIED by clause 3 wherever q is polynomial in n (log₂ q = O(log n) forces σ = Ω(n/log n)); at the official rows (q < 2^256, log₂ C(n,·) = Θ(n)) clause 3 forces σ = Ω(n), far stronger. Clause 4 binds independently only at superpolynomial q — the regime upstream's own proved Galois lane covers (quasi-poly p > exp(O((log n)²))) | SUBSUMED in scope |
| 5 | Quotient-core profiles satisfy eq:qprofile-list-budget (Qprof_H(a,k) ≤ B_L log₂ n + Γ_Q) | "the quotient profile is budgeted" hypothesis + dyadic_profile_evaluation PROVED: Q_H(η) computed EXACTLY for 2-power domains at all four official rates | MATCH at rows (exact values, not just budget) |
| 6 | "after quotient-periodic classes are accounted for" (aperiodic behave like random codimension-σ fibers) | The periodic branch is priced by the PROVED census gate (Lemma COL / clause (D) route, column-priced); the aperiodic top band by clause (P)'s rigidity census (empty at rates ≤ 1/4; n^4/96 at rate 1/2); mixed/below-top by petal_growth's off-band induction + the P1-floor band split | MATCH |
| 7 | Generated-field smooth domains H_n ≤ F_q^×, n = 2^m, q_n = q_gen | Official rows: n = 2^41..2^44 two-power domains, q ≡ 1 mod n, generated-field normalization (catch #13 pin) throughout the chain | MATCH at rows |
| 8 | k_n = ρn + O(1) (quotient-hygiene freedom) | Official rows have exact k (e.g. 2^40); the O(1) freedom is upstream flexibility, not an obligation on the rows | N/A (freedom unused) |
| 9 | Consequence via lem:fiber-list: \|Λ(C, 1−ρ−η_n)\| ≤ n^{B_L} | Follows for the official rows once upstream's lem:fiber-list is instantiated there (their lemma, proved upstream: ImgFib_U(a) IS the list) | TRANSFERS |

## Verdict

**OFFICIAL-ROW INSTANTIATION DISCHARGED.** Every instance of the
upstream L1 assumption at the prize's official rows (all four rates,
all received words) is theorem-backed by the imgfib chain
(petal_growth + conj_f + l1_program_frontier +
dyadic_profile_evaluation + payment_completeness, all PROVED
2026-07-13). The towards-prize.md L1 target — posed for the prize
program, i.e., for these rows — is closed.

**NOT claimed:** the asymptotic family form of ass:locator (all
n = 2^m with a single uniform B_L) — our exponents are row-explicit
and the proof consumes official-row pins (clause (P) posed at official
rows only). The general assumption remains as stated for the paper's
asymptotic theorem.

**Standing caveats (inherit to any upstream presentation):**
- Tripwire (P)-3 / re-surgery criterion 4: the chain is proved for the
  maintainer-confirmed P1 FLOOR band (d >= M(t-2), layout-anchored per
  catch #168); a re-resolution of the band constant re-opens it.
- The #171 wide-minus-floor lift mass is petal_growth's flagged
  below-top ledger line (separate obligation; does not enter the
  top-band assembly).
- Verification trail: cp_verify.py 62/0 + cpa_checks.py 37/0 (clause
  (P)); the G3 compiler + census gate + K4 + qa22 verifiers; harness
  124 scripts / 221 assets; Modal execution re-pin 124/124 complete
  (experiments/prize_resolution/modal_verifier_replay.json).
