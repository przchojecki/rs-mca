# WP-2.3 detail (L3): the syndrome-space stratification case-tree

- **Status:** plan; leaf pricing cites PROVED / pending-replay lemmas per
  node; the tree itself is a definition (total by construction).
- **Executability:** AGENT (tree + fuzz harness); leaf lemmas partly
  pending WP-0.3 replay (#170/#171 material).
- **Parents:** r2 WP-2.3; consumes `proof_sketch/s3b_ii` (strip),
  `s2` (Paid), `s3a` (window), `wp2_6` (deficiency charts).

## 1. Design principle

The tree is evaluated FIRST-MATCH-WINS in the order below; that order IS
the dedup convention (a pair pays in the first stratum that claims it —
the same convention the M4 table and the WP-0.4 checker must enforce, so
the tree definition and the dedup logic are one artifact, not two).
Cheap predicates come before expensive chart work. Every leaf emits a
certificate naming its stratum, its price source, and its label from the
roadmap's allowed set.

## 2. The tree (per exact agreement A; pair (u,v); t = A-k, j = n-A)

```text
T0 containment gate      predicate: exists locator l with H(u)l = H(v)l = 0
                         (the degenerate-pencil stratum, s4 = def:residue's
                         noncontainment)  -> EXCLUDED from LD_sw. [exact]
T1 degenerate pairs      v = 0 / u = 0 / v = lambda u  -> zero/proportional
                         leaves; priced by the #171 zero-u/zero-v/
                         proportional lemmas [pending replay].
T2 tangent overlap       exists Z0, codeword c, agreement(u + Z0 v, c) =
                         A0 > A  -> TANGENT-PAID; fiber = common-divisor
                         plane, count C(A0, A0 - A) [verified toy,
                         s3b_iii_3]; price B_tan [PROVED-cited #147 range].
T3 quotient periodicity  the pencil folds rate-preservingly through
                         x -> x^M, M | gcd(n,k), M > 1 (syndromes descend)
                         -> QUOTIENT-PAID at scale M; recursion to the
                         quotient row [PROVED-cited Q_M = Q_1 + rem:aper
                         convention, s3b_ii/s4]; zone-(b) cells stay
                         intervals [s2].
T4 direction rank        r = generic rank of the pencil; r <= r0 (currently
                         r0 = 12 for the synthetic families) -> low-rank
                         ladder leaves [#170, pending replay]; else full.
T5 regime split          t >= j+1 -> REGULAR bucket: canonical gcd/lcm
                         ledger, fronts alpha/beta [predictions P1a/b/c,
                         P-beta, s3a]; else deficiency-d chart program
                         [wp2_6: Cramer/divisibility at d = 1, pencil
                         charts at d >= 2].
T6 cross-bucket dedup    kernel locators of degree < j -> charged to the
                         higher-agreement bucket [wp2_6 side chart; exact].
T7 split-locator gate    surviving eliminant roots filtered by
                         L | X^n - 1 and the noncontainment gate
                         [#171 gate, pending replay; s3b_iii_3 window
                         convention m = 1..t].
LEAF residual(named)     whatever survives: labelled quotient / tangent /
                         extension / candidate_new_obstruction / unknown
                         per towards-prize.md §4.6 — the catch-all that
                         makes the tree TOTAL.
```

Extension rows add T3' (subfield confinement / pole type) between T3 and
T4, per `s6`'s classification; generating rows skip it.

## 3. Route and prerequisites

```text
- T0/T2/T6 predicates are exact linear algebra on the toy row TODAY
  (verified pieces in s3b_iii_3 and wp2_6); scale to F_17^32 via the #148
  field tower.
- T1/T4/T7 leaf pricing cites #170/#171 lemmas -> BLOCKED on WP-0.3
  replay (standing order 12); the tree can be built and fuzz-tested with
  those leaves marked pending.
- T3 needs the fold-detection predicate: syndromes descend iff the
  windowed DFT coefficients are supported on multiples of M [derive from
  the V^T D V factorization, s3b_iii_2 — one lemma, AGENT].
- T5-regular consumes the M3 campaign; T5-underdetermined consumes PR
  #172's rungs.
```

## 4. Acceptance test (verifier-runnable)

`experimental/scripts/verify_m3_stratification_tree.py`, toy row
`F_97 / mu_16, n = 16, k = 8` (the wp2_6 acid-test row):

```text
(i)   constructors: planted pairs for each stratum (contained pair;
      v = 0; proportional; planted tangent A0 > A; folded M = 2 pair;
      low-rank synthetic; generic random) — seeds pinned;
(ii)  totality: every constructed AND 500 random pairs land in exactly
      one leaf (first-match) — no fall-through, no double-claim;
(iii) pricing: per leaf, the predicted contribution equals the
      brute-force bad-slope count for that pair on the toy row
      (exhaustive: C(16, j) supports x 97 slopes);
(iv)  dedup: the sum over leaves of priced contributions, evaluated on a
      mixed-structure pair (tangent AND folded), counts each slope once —
      first-match order verified against brute force.
PASS = (ii) + (iii) + (iv) green; any residual-leaf arrival by a
constructed pair is a FINDING (mispriced stratum), not a failure of the
harness.
```

## 5. Failure branches

```text
F1: a RANDOM toy pair reaches the residual leaf unpaid -> at toy scale FM
    says this is possible (small q!) — compute the toy FM expectation
    first and assert only the excess; at F_17^32 scale any unpaid
    residual arrival is P1c-grade news (s3a).
F2: T3's fold-detection predicate misses non-equivariant periodic pairs
    (GAP-1, s3b_ii) -> they land in the residual leaf BY DESIGN — the
    tree makes GAP-1's mass visible and measurable rather than hidden.
F3: first-match order disagrees with the M4 table's dedup -> the tree
    order is normative; regenerate the table (one convention, WP-0.4).
F4: #170/#171 replay changes a leaf lemma -> only that leaf's price
    updates; the tree shape is stable.
```

## 6. What this buys

The tree is the executable form of "every pair is paid or named": it
operationalizes the strip (s3b_ii), makes the dedup convention a single
artifact, gives GAP-1 a measurement instrument, and provides the harness
that the window theorem (s3a's aperiodic-0 prediction) will be checked
against, stratum by stratum.
