# WP-2.5 + WP-4.1 detail (L3): window residual charts + displacement uniformization

- **Status:** chart plan (window side) + a derivation route that makes the
  uniformization INDEPENDENT of the unintegrated mega-PR (algebra side).
  Extension-field anchor machine-verified this turn.
- **Executability:** AGENT throughout.
- **Parents:** r2 WP-2.5/4.1; consumes wp2_3 (tree), wp2_6 (chart
  machinery), s3a (predicted outcome), s3b_iii_2 (the factorization).

## 1. WP-2.5: closing the window's residual leaves

**Where window residuals come from.** In the overdetermined window the
kernel is generically trivial; alignment lives only on the rank-drop
locus — the FINITELY many `Z` where the canonical gcd vanishes. So window
M5 is **per-point, not per-curve**: at each such `Z_0`, a finite linear-
algebra decision (does the now-nontrivial kernel contain a valid split
locator?), which is the easy sibling of the in-band chart problem. The
chart ladder per bucket, in the roadmap's order:

```text
1. affine pivots  B_h(l) != 0: chart ideal = collinearity + graph
   equation, saturated by Delta_X B_h; eliminant or per-Z decision;
2. projective infinity (B = 0, A != 0): certify empty or count <= 1
   projective parameter (paid to the projective column);
3. curve pivots (degree-d families): <= d per support (v8 ledger) —
   bounded, never a blow-up;
4. dimension-degree: diagnostic only, never an end state by itself;
5. residual classification: quotient / tangent / extension /
   candidate_new_obstruction / unknown — and the exit criterion is
   ZERO 'unknown' leaves across 385 <= A <= 426.
```

**Acceptance test:** a per-A bucket log emitted by script — every bucket
ends `regular-closed(root table)` or `chart-closed(per-Z decisions)` or
`residual(named != unknown)`; the WP-0.4 harness ingests the log; the
s3a prediction (aperiodic numerator 0 throughout — the P1 family) is the
expected content of the final column, and any deviation is a FINDING
routed to the s3a fork table. **Failure branches:** a `Z_0` resists the
per-point decision (degenerate kernel + splitting test ambiguity) ->
that single point is a named residual with a minimal reproduction —
front-beta-adjacent and exactly what WP-2.2 wants to see; curve families
appear -> bounded by `d`, priced, never blocking.

## 2. WP-4.1: displacement identities over abstract 2^s fields

**The route that avoids waiting on integration.** The #170 identities
(det factorization `det(H_X + Z H_Y) = det(V_X)^2 prod(x^h) det(I + Z K_h)`,
rank-one Toeplitz-Cauchy displacement, replacement-subset/Cauchy-Binet
coefficients, shift-two transfer) are computations ON the subgroup
factorization `H = V^T D V` — which is elementary, char-generic, and now
verified on BOTH a prime field (F_13, turn 3 of the sketch) and an
EXTENSION field (F_49 = F_7[i], mu_8 — this turn, entrywise). Deriving
the identities FROM the factorization gives the uniform statements
directly:

```text
U-A  det factorization over any F with mu_{2^s} <= F*, char F odd,
     under printed nonvanishing hypotheses (denominators 1 - alpha^e
     with e != 0 mod ord(alpha) — these become explicit hypotheses,
     not char exclusions);
U-B  displacement-rank statements: char-free linear algebra, no
     hypotheses beyond U-A's denominators;
U-C  the derivation is INDEPENDENT of #170's files — WP-0.3's replay
     then becomes a cross-check (two derivations of the same identities)
     instead of a dependency.
```

**Acceptance test:** one verifier, three instantiations — `(F_13, mu_4)`,
`(F_17, mu_16)`, `(F_49, mu_16)` (divisibility facts verified: 4|12,
16|16, 16|48) — checking each identity exactly at small `(t, j, h)`,
plus the printed hypothesis table (which `(m, a, i)` denominators must
not vanish, per subgroup order). PASS = all three fields green with the
SAME script. **Failure branches:** an identity fails on one field only
-> a char/order hypothesis was missed, add it (this is what the
three-field design detects); an identity fails everywhere -> it was
mis-transcribed from #170, which is a WP-0.3 divergence FINDING, and the
uniform note simply proves the corrected form.

## 3. What this buys

Window M5 becomes a finite, per-point cleanup with a predicted outcome
and a defined finding-format for surprises; and the displacement algebra
— the dimension-free hope of mechanism 2 — gets uniform, three-field-
tested statements that do not wait on mega-PR integration, turning the
replay from a blocker into a cross-check.
