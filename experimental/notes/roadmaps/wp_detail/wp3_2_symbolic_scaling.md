# WP-3.2 detail (L3): symbolic scaling — the row descriptor and what still resists

- **Status:** inventory + spec; two genuinely-open symbolization items
  named. Numerics machine-checked.
- **Executability:** AGENT (restatements + descriptor tool); the two open
  items are small-lemma work suited to the bottom-up lane.
- **Parents:** r2 WP-3.2; consumes wp2_6 rung 3, s2, s4, s5_s0.

## 1. Symbolization inventory — status per pinned-row artifact

```text
already symbolic (cite, do not rework):
  tangent staircase compiler (1 <= B_Q <= (n-k)/3 => pinned)  [#147 +
    step-5 envelope, stated for general rows];
  tau*(rho, q) and every crossing formula                      [parametric
    in log2 q by construction, s4];
  V^T D V factorization; FM1 exact first moment; Johnson facts
    (gap = n); strip combinatorics C(n/M, j/M)                 [character
    sums / counting, field-generic given char coprime to n];
needs RESTATEMENT only (one lemma note each, AGENT):
  U1-U5 chart chain over abstract mu_{2^s}, char odd           [wp2_6
    rung 3 spec; degree bounds t + (n-j+1)t symbolic];
  fold-detection predicate (DFT support on multiples of M)     [wp2_3 T3];
needs REAL WORK (the two open items):
  (A) A_cl second-order term: 2^{beta(rho) N'(1 - o(1))} — the o(1)
      matters at corridor scale (s2 F4); needed: an explicit interval
      A_cl in [2^{beta N' - c log N'}, 2^{beta N'}] or better;
  (B) displacement identities over abstract 2^s fields          [WP-4.1's
      charter — cross-reference, do not duplicate].
```

## 2. The symbolic row descriptor (the P3 consumable)

**Spec:** `experimental/scripts/symbolic_row_descriptor.py` — input
`(p, e, s, rho)`; output the full derived table:

```text
n = 2^s, k = rho n;  q_line = p^e;  q_gen = p^ord(p mod 2^s);
generating? (q_gen == q_line);  gates B*_aff, B*_proj (+1 edge iff
2^128 | q_line + 1);  staircase cap (n-k)/3 and pinned? (B_Q <= cap);
corridor numbers: cap reserve, quotient crossing beta/( log2 q - 128 ),
tau*, list window [H/128, H/256] — all evaluated at THIS row's log2 q;
zone-(a) boundary N'_max(log2 q) with proved-exact quotient mass
  (verified samples: N'_max = 46 / 62 / 80 with masses 2^36.5 / 2^49.1 /
  2^63.4 at log2 q = 130.8 / 192 / 256, rho = 1/2);
m-sweep cap sqrt((n-k)/t) at the corridor;  hypothesis-table row (wp4_4).
```

Everything in the descriptor is O(poly(s, log q)) — no enumeration
anywhere; that is the entire point of symbolization (an n = 2^41 row costs
the same as n = 512).

**Acceptance test (regression):** on `(17, 32, 9, 1/2)` the descriptor
must reproduce the verified pinned-row values exactly

```text
B*_aff = B*_proj = 6; ord = 32 (generating); staircase cap = 85;
pinned? YES; 506/507 transition from the staircase formula;
```

and on the synthetic top-of-range row (`log2 q = 256`) it must reproduce
the master per-rate table of `s5_s0` to all printed digits. PASS = both
regressions green; the script becomes the single source for every number
quoted in dossier tables (no hand-copied constants anywhere downstream).

## 3. The two open symbolization items, framed for hand-off

```text
(A) A_cl interval [bottom-up lemma]: sharpen thm:exactcount's o(1) to an
    explicit second-order term for N' in the corridor-active range
    (N' ~ 128/beta to 512). Consumer: the S2 bracket's quotient end
    becomes a NUMBER instead of a shape; the s8_s9 low-confidence bet
    becomes testable. Toy validation: exact e_1 value-set counts at
    N' = 8..32 (feasible enumerations) against the candidate second-order
    formula.
(B) norm-threshold extension [bottom-up lemma, = s2 fork F3]: extend
    prop:qfloor's exactness past N'_max(log2 q) (46/62/80 above) toward
    the crossing N' ~ 161 at top-of-range — every step moves the PROVED
    part of the unsafe side; the zone-(b) interval narrows from the left.
```

## 4. Failure branches

```text
F1: (A) resists — the o(1) is genuinely irregular -> corridor stated as
    an interval forever; the dossier quotes brackets (already the s8_s9
    posture); no structural damage.
F2: char-p exceptions surface in the U1-U5 restatement (small p) ->
    print exclusions in the descriptor; official rows have p odd and
    large, so exclusions are cosmetic unless p | (something structural),
    which the acceptance regression would catch on synthetic small-p rows.
F3: a P3 row exposes a hypothesis the descriptor lacks (e.g. domain not
    the FULL 2-Sylow — a proper 2-power subgroup of a larger 2-part) ->
    add the |H|-vs-2-Sylow column; the strip and staircase survive, the
    q_gen computation changes (ord against |H|, already how it is coded).
```

## 5. What this buys

One descriptor script replaces every hand-derived row constant in P3-P7;
the two named open items are exactly where symbolic knowledge currently
ends, both shaped for the bottom-up lane, and both with verified toy
targets waiting.
