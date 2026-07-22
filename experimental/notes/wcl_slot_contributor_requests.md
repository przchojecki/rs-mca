# Contributor Requests: the WCL Ten-Slot Register (Compute and Result Requests, CPU-Time Budgets)

- **Status:** CONTRIBUTOR REQUEST / EXPERIMENTAL — enters no proof in this
  tree; every item is a self-contained finite problem with a deterministic
  checker and declared success/failure semantics.
- **Agent/model:** Claude Fable 5 acting for AllenGrahamHart.
- **Artifact:** `experimental/scripts/verify_wcl_slot_decomposition.py`
  (stdlib, <1s) — the machine certificate that the ten requested cells
  jointly exhaust the obligation.
- **Cross-repo source (SHA-pinned, read-only):**
  `github.com/AllenGrahamHart/rs-mca-prize-dag@b959fe8f` — node
  `critical/nodes/dli_wcl_zone_coverage/` (statement, ten-slot conditional
  assembly, `official_terminal_attack.md` sizing ledger,
  `verify_slot_decomposition.py`), the ten slot nodes
  `critical/nodes/dli_wcl_slot_*_emptiness/`, audit + screen packets at
  `notes/wcl_decomposition_audit_20260722/`.
- **Local source commit / upstream target commit:** `b959fe8f` / `fb6d9555`.

## 1. What this is, honestly scoped

This register serves the **auditing repo's** resolution architecture (its
`dli` lane), not a hard input of the Grande Finale spine — it is offered on
the contributor-marketplace model: well-specified finite problems that any
contributor can run or prove independently, with results consumable by the
auditing tree and full attribution both ways. It is disjoint from Lanes in
`agents.md` (including the new Lane L) and from open PRs #1047–#1049.

**The object.** In the auditing tree, a conditional chain reduces a prize-
critical conjecture (endpoint budget `2^121`) to a 100-bit product baseline,
which holds iff a per-level ledger-mass bound `W <= 1/32` holds at every
level of a 34-level dyadic tower (dims `2^32,...,4,2,1,1`). Machine-verified
reduction: that bound holds **iff ten finite cells are empty**, where cell
`(ell, w)` asks:

> no reduced signed weight-`w` polynomial `P` (support a `w`-subset of
> `[0, 256*ell)`, coefficients `+-1` modulo global sign, no exponent-gcd
> filter) has `P(omega^(2j-1)) = 0` for all `j = 1..ell`, with `omega` of
> EXACT order `512*ell`, such that the associated cyclotomic norm has a
> prime divisor `q < 2^256` with `v_2(q-1) >= 41`.

The completeness of the ten-cell list is not prose: the shipped verifier
re-derives it from the pinned primitives (tower, window `[L+1, L+7]` with
`L` the level DIMENSION, the Newton short-window theorem `w >= 2*ell+1`, the
proved weight-3/4 ambient exclusions, the `1/32` mass threshold — minimum
single-orbit breach factor 32x) with five mutation controls, including a
simulated level-index/level-dimension conflation. Two sibling cells,
`(2,5)` and `(2,6)`, are already CLOSED by audited certificates (norm-gcd
over 168 Pocklington-certified primes; a 404,740-orbit recursive-norm
census) — the conventions above were audited against those closed
certificates with no mismatch, so a sweep built to this spec provably
targets the right space.

**Both outcomes are first-class.** Emptiness certificates close cells of
the auditing tree's conditional assembly. An EVENT (an official-admissible
prime dividing a cell norm) is a refutation deliverable: it demotes a
conditional node in the auditing tree and relocates that program's route —
a finding, not a failure. Either way the checker semantics below say
exactly what was established.

**Evidence state (so contributors know the prior).** Powered pre-registered
sampling (934 orbits across the four cheapest cells, 2026-07-22, seeds
banked): zero events, zero candidates; maximum `v_2(q-1)` observed = 24
against the gate of 41. Survival evidence only — nothing below is
discharged by it.

## 2. Compute requests (CPU-time budgets at measured reference rates)

**Mandatory implementation constraint** (banked catch): prime factors of
these cyclotomic norms are NOT all `== 1 mod n` (roots may live in
extensions; witnessed: `31` divides an order-64 norm). Progression-based
trial division is UNSOUND. Full factoring or certified partial factoring
only; keep a gp/ECM-class stage in the loop for hard 150–450-bit cofactors
(typical norms measure ~200–300 bits; worst-case bounds 594–718 bits).

| id | cell(s) | space (exact) | est. CPU time | status / stage-0 items |
|---|---|---:|---|---|
| CQ-1 | (1,5) order-256 coset layer | 243,474 orbits | **7–25 CPU-h** | READY — the starter request; closes 10.6% of the (1,5) space outright |
| CQ-2 | (1,5) full ambient | 2,296,920 orbits | **~445 CPU-h** total (~46% already banked by the auditing side; checkpoint manifest available on request — merging leaves ~238 CPU-h) | READY after two specified stage-0 repairs: re-shard the final aggregation; add an ECM stage for slow-factoring tail norms |
| CQ-3 | (2,7) router space | 94,652,815 presentations (ambient 4.35e11; the router is the validated constraint-first form) | **~33,000 CPU-h** at the measured reference rate (1.25 s/orbit, pure-integer pipeline); the gcd stage is ~60% of cost — a GMP/FLINT gcd implementation is the known optimization target (expected substantial reduction, unmeasured) | Reference pipeline independently reconstructed and validated exactly mod q (6/6 self-checks; bit profile matches the banked pilot to ~1%); includes the saturation-screening stage |
| CQ-4 | (1,6) ambient | 185,569,028 orbits | **>= 36,000 CPU-h** (rate floor from the (1,5) reference rate; factor-stage growth uncalibrated beyond a 256-row sample) | Open to pilot bids: a 10k-orbit pilot (~2 CPU-h) would price the full run properly |

**Explicitly NOT requested as compute** (do not burn cycles here):
(1,7) ~2.5M CPU-h, (1,8), (2,8), (2,9) — census-infeasible; these are
result-request territory (R3). The (4,w) cells are census-infeasible at any
rate and descent-shaped (R1).

**Certificate format + checker** (all compute requests): per-orbit record
(canonical representative, exact norm or its certified factor stack,
per-factor `v_2(q-1)`, outcome in {CLEAR, EVENT(q), UNRESOLVED-TAIL(bound)}),
per-shard sha256, coverage accounting that tiles the declared space, and a
deterministic streaming re-checker (stdlib) that re-validates coverage +
hashes + the zero-event claim without re-running the search. The closed
(2,5)/(2,6) certificates in the source repo are the format exemplars.
PASS = coverage complete + zero EVENT + UNRESOLVED tails carrying explicit
smoothness certificates. FAIL = an EVENT with its witness `(P, q)` — please
report immediately; it is a major finding. Incomplete = partial coverage
honestly tiled (mergeable).

## 3. Result requests (proof work; no compute budget)

| id | item | shape | why it is leveraged |
|---|---|---|---|
| R1 | Descent statements + Delta-integer certificates for (4,10) and (4,11) | The proved (4,9) quartic-divisor descent + straight-line lift are the pattern; the odd pattern `w = 2*ell+3` extends to (4,11) (degree-5 system), the even pattern to (4,10); 4-variable, degree <= 3 ideals | The only viable route at `ell = 4`; two of three descents already proved in the source tree |
| R2 | Unit-ideal certificate at the three-variable (1,5) ideal | Prove the vanishing ideal has no official-admissible zero (algebra, not enumeration) | **A land retires every census request above** — the highest-leverage single item in this register |
| R3 | Exclusion algebra at (1,7)/(1,8)/(2,8)/(2,9) | Extend the proved weight-3/4 ambient-exclusion pattern (affine-Galois quotient, then 2-adic valuation forcing on norms) to higher weight, possibly by structured subfamilies | These cells are provably out of compute reach; partial subfamily theorems shrink them permanently (the source tree's weight-5 subfamily work — 1.4% of (1,5) proved event-free — is the working example) |
| R4 | Pocklington upgrade of the probable-prime classifications in the banked (1,5) subfamily certificates | Small, fully specified | Converts probable-prime-level exclusions to banking grade |

## 4. Non-claims (fence)

This register does not touch any Grande Finale hard input, Lane L, SS0.4,
SS0.5, or any Paper-D theorem row; it moves no score in this tree. The
conditional structure it serves lives in the auditing repo; emptiness
results close cells THERE (with attribution), and an event refutes a
conditional node THERE. Estimates are measured-reference-rate projections,
not commitments; every exact count above is reproducible from the
SHA-pinned source packets.
