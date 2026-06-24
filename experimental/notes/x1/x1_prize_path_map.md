# X1: the path-to-prize map — what is proved, and the tree to the goal

- **Status:** MASTER MAP / AUDIT (orienting document; no new theorem). Supersedes
  the framing in `x1_prize_target_map.md` with a full dependency tree and
  node-by-node status.
- **Agent/model:** Claude Opus 4.8 (L2/X1 lane, branch `allen/l2-x1-interleaved-mca`).
- **Date:** 2026-06-24.
- **Spec source:** proximityprize.org (preliminary), `readme.md`, ePrint 2026/680.

## Destination

Determine the largest threshold `δ*_C` for `C = RS[F, L, k]`, `L` smooth of
power-of-two order `n`, `ρ = k/n ∈ {1/2,1/4,1/8,1/16}`, regime `ε*=2^-128`,
`k ≤ 2^40`, `|F| < 2^256`. **Two grand challenges:**
```text
(MCA)   emca(C, δ*)        ≤ 2^-128
(List)  |Λ(C^{≡m}, δ*)|    ≤ 2^-128 · |F|     (m-fold interleaved; ÷ challenge field)
```
"Determine `δ*`" = **sandwich it**: an upper bound (the cap, negative side) and a
matching lower bound (the positive theorem). The gap between them is the prize.

## Status legend

```text
[P]  PROVED (theorem or independently verified)            [H]  conjecture, FALSIFICATION-HARDENED (proof stage)
[P*] PROVED conditional on an import now removed/audited    [C]  conjecture, FRESH (hardening stage)
[A]  PROVED this session (verifier on branch)               [ ]  OPEN / assembly not yet done
```

## The tree

```text
                         ┌─────────────────────────────────────────────┐
                         │   PRIZE: determine δ*_C  (sandwich)          │
                         └─────────────────────────────────────────────┘
                            ▲ upper bound (cap)        ▲ lower bound (positive theorem)
          ┌─────────────────┘                          └───────────────────────┐
   NEGATIVE SIDE  (essentially DONE)                              POSITIVE SIDE  (the open program)
   │                                                              │
 [P*] Paper D cap: δ* ≤ 1−ρ−2^-9  (2^-10 at ρ=1/16)        ┌──────┴───────────────────────────┐
   │   error >2^-86 unif, >2^-42 if |F|≥2n              (MCA challenge)               (List challenge)
   ├─[A] CS25-free: deep-point route removes thm:A          │                              │
   │     (commit 91044bb), rests on audited lem:fiber  [P] thm:normalform:           [P] interleaved deep-point
   ├─[A] lem:fiber audited by enumeration                   │   MCA ⟺ residue-line       │   bridge (PR #101):
   ├─[P] Paper A no-slack obstruction                       │   packing (Λ^aper)         │   Λ(C^{≡m}) ⟵ base list
   ├─[P] Paper B floors / failure ladders                   │                              │
   ├─[A] M1 Cycle120 LD_sw counterexample audited      [H] conj:B / conj:final-mca   [C] L2 sharp-constant
   │     (#100/#105; conditional on census)                 │   (X1, mine):              │   conjecture (L2, mine):
   └─[A] F1 σ≥1, σ≥2 counterexamples audited (#103)         │   Λ^aper ≤ n^{1+o(1)}      │   Lst(Int(C,μ)) ≤
                                                            │                              │   binom·q^{−μ(a−k)}
                                                            │   [A] confinement thm +      │   + Quot_μ + n^B
                                                            │       quotient reduction:    │
                                                            │       quotient-periodic      │   [A] quotient reduction
                                                            │       lines SEPARATED        │       (μ-fold version)
                                                            │   [P] thm:qnecessity:        │
                                                            │       quotient term matched  │
                                                            └──────────────┬───────────────┘
                                                                           │  COMMON ROOT (deep-point + interleaved bridges)
                                                                   [H] conj:arbitrary-local
                                                                       = Codex Q_1 ≤ n^B  (L1, #106)
                                                                       falsification-survived; PROOF IN PROGRESS
                                                                           │
                                                            ┌──────────────┴───────────────────────────┐
                                                       PROVED FOUNDATION (this session + Paper B, all [A]/[P]):
                                                       deep-point identity bridge · unifying prefix-locator
                                                       slope principle · isotypic decomposition · product bound
                                                       · quotient reduction (Q_d(H_n)=Q_1(H_{n/d}))
```

The three open conjectures (L1, X1, L2) all have the **identical shape** —
*"aperiodic/quotient-separated part ≤ poly; quotient-periodic part = explicit
quotient term"* — and the deep-point bridge (list↔slopes) + quotient reduction
(the periodic separation) are the glue that makes them **co-prove**: Codex's L1
list bound transfers toward X1's slope bound and L2's interleaved bound, rather
than being three separate mountains.

## Node-by-node status

| Node | Statement | Status | Owner | Evidence |
|---|---|---|---|---|
| Cap (upper bound) | `δ* ≤ 1−ρ−2^-9` | **[P*]→[A]** proved; now CS25-free | Paper D | `verify_x1_prob_explicit_universal.py`, `91044bb` |
| `lem:fiber` | locator fiber list ≥ `binom(N,ℓ)/|B|` | **[A]** audited | Paper D | `verify_x1_lem_fiber.py` |
| `thm:normalform` | MCA ⟺ residue-line packing (up to tangent floor) | **[P]** | Paper B | Paper B |
| `thm:qnecessity` | quotient profile necessary; matches quotient term | **[P]** | Paper B | Paper B |
| Deep-point bridge | bad slopes = deep image of fiber; interleaved version | **[A]** | X1 (PR #101) | `verify_x1_deep_point_identity.py`, `verify_x1_interleaved_deep_point.py` |
| Confinement thm | equivariant + `K_d`-stable ⟹ folded ⟹ confined slope | **[A]** | X1 (this session) | `verify_x1_confine_from_stabilizer.py` |
| Isotypic refinement | confinement is per-character; QuotientBudget≠confined exactly | **[A]** | X1 | `verify_x1_isotypic_decomposition.py` |
| Quotient reduction | `Q_d(H_n)=Q_1(H_{n/d})`, same rate | **[A]** | X1 | `verify_x1_quotient_reduction.py` |
| **L1 conjecture** | `Q_1(U,a) ≤ n^B` above reserve (`conj:arbitrary-local`) | **[H]** proof in progress | **Codex #106** | falsification scanners survived |
| **X1 conjecture** | `Λ^aper ≤ n^{1+o(1)}` (`conj:B`/`conj:final-mca`) | **[H]** proof stage | **me** | Paper B floors; confinement = its separation |
| **L2 conjecture** | `Lst(Int(C,μ)) ≤ binom·q^{−μ(a−k)}+Quot_μ+n^B` | **[C]** hardening stage | **me** | `verify_x1_*interleaved*`; `μ=2` numeric only |
| Field accounting | keep `q_gen`, `q_line`, `q_chal` separate | **[ ]** | C-ledger | — |
| Threshold tightening | bring `η → 2^-9`; concrete exponent `B` clears `2^-128|F|` | **[ ]** | all lanes | — |

## Critical path (shortest route to the prize)

1. **L1 — `Q_1 ≤ n^B`** (Codex, proof in progress). The crux; everything roots here.
2. **Bridges (built):** deep-point (L1→MCA slopes) and interleaved (L1→L2). These
   already exist as verified reductions, so step 1 propagates.
3. **X1 — `conj:B` proof.** With L1 + the deep-point bridge + this session's
   confinement/quotient-reduction (the quotient-periodic separation `Λ^aper`
   needs), the MCA challenge follows. **Stage: proof** (conjecture is hardened).
4. **L2 — harden then prove the sharp-constant conjecture.** **Stage: falsify**
   (run the scanner gauntlet like #106), then prove via the interleaved bridge.
5. **Assembly:** field accounting (`÷` challenge field) + tighten `η` to `2^-9` +
   confirm the concrete exponent `B` clears `2^-128·|F|` at real parameters.

The negative side (sandwich's upper bound) is **done**. So the prize = steps 1–5
on the positive side, of which the *bridges* and *separation machinery* (steps 2,
and the X1 tools in step 3) are already proved this session; the *open math* is
the three conjectures (L1 in progress, X1 proof, L2 harden) plus the step-5
assembly.

## Honest open list (what is genuinely not done)

- **L1 `Q_1 ≤ n^B`** — open, proof in progress (Codex). The hard analytic core.
- **X1 `Λ^aper ≤ n^{1+o(1)}`** — open; hardened conjecture, proof not written.
  The per-scale reserve bookkeeping (`x1_quotient_reduction.md`) is its residue.
- **L2 sharp-constant** — open; conjecture fresh, needs the falsification gauntlet.
- **Concrete exponent `B`** — even a poly bound must give `B` small enough that
  `n^B ≤ 2^-128·|F|` at deployed `(n,|F|)`; not a separate proof but a real
  quantitative requirement.
- **Field accounting + threshold tightening to `2^-9`** — assembly, not yet done.
- **`m` (interleaving arity) in the List challenge** — treated as constant; the
  exact `m`-dependence of `Quot_μ` is part of L2's hardening.

## Pointers
- Master spec: `readme.md`, proximityprize.org, ePrint 2026/680; memory `rs-mca-prize-spec`.
- Conjectures: `conj:B`, `conj:final-mca`, `conj:arbitrary-local`, `thm:normalform`
  (Paper B `slackMCA_v3.tex`); Codex #106 `notes/l1/l1_quotient_budgeted_locator_conjecture.md`;
  L2 `notes/l2/l2_interleaved_dilation_constants.md`.
- This session: `x1_cs25_free_cap.md`, `x1_prefix_locator_slope_principle.md`,
  `x1_confinement_from_stabilizer.md`, `x1_quotient_reduction.md`, `x1_prize_target_map.md`,
  and the `verify_x1_*` scripts.
