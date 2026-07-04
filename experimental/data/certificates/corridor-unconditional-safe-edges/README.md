# Corridor Unconditional Safe Edges: GKL24 + Hab25 Imports on the Six Clean-Rate Rows

- **Status:** AUDIT / PROVED (both import theorems independently
  proof-audited externally; all row arithmetic exact-integer, replayed by the
  verifier below).
- **Agent/model:** Claude Fable 5 acting for latifkasuli.
- **Scope:** re-baselines the *below-band* certified safe edge of the six
  clean-rate corridor rows (Row C `n = 2^10` and prize-max `n = 2^41`, rates
  `1/4, 1/8, 1/16`) using two **unconditional** mutual-correlated-agreement
  imports. The corridor band itself and its five blockers are untouched (see
  Non-claims).

## Use Rule header

```text
object:            def:mca safe edges (count of MCA-bad slopes <= B*) from two
                   proof-audited imports: GKL24 Thm 3 (1.5-Johnson, linear-in-n)
                   and Hab25 Thm 2 (Johnson, quadratic-in-n)
sampler:           finite_affine (slopes z in F; projective variant: numerator
                   +1, denominator q_line + 1 — immaterial at these margins)
q_line:            Row C idealized 2^250, prime unpinned (qa3 flag C1(b));
                   prize idealized 2^255.9
budget:            epsilon <= 2^-128 certified as count <= B* = floor(q_line/2^128);
                   B* = 2^122 (Row C), floor(2^127.9) = integer 10th root of
                   2^1279 (prize) — exact integers per xr_budget_audit.md
agreement/radius:  closed integer grid r = n - a; supremum open at the first
                   unadmitted point (M0 freeze conventions)
statement type:    safe-side upper bounds on the def:mca numerator; per-row
                   adjacent failure exhibited one grid step past each edge
paid ledgers:      none consumed (theorem imports, not census subtractions)
```

## Result: three certified safe-edge columns per row

Certified safe edges (closed integer radius `r`; `delta = r/n`); **bold** = the
new unconditional frontier of the row:

| row | n | k | current (BCIKS20 `(1-rho)/2`) | GKL24-1.5J (unconditional, proof-audited) | Hab25-Johnson-quadratic (unconditional, proof-audited) |
|---|---|---|---|---|---|
| Row C 1/4 | 2^10 | 256 | 384 (0.375000) | 379 (0.370117) — no gain | **512 (0.500000)** |
| Row C 1/8 | 2^10 | 128 | 448 (0.437500) | 513 (0.500977) | **663 (0.647461)** |
| Row C 1/16 | 2^10 | 64 | 480 (0.468750) | 619 (0.604492) | **769 (0.750977)** |
| prize 1/4 | 2^41 | 2^39 | 824633720832 (0.375000) | 813725411113 (0.370039) — no gain | **1092724518963 (0.496914)** |
| prize 1/8 | 2^41 | 2^38 | 962072674304 (0.437500) | 1099511627777 = 2^40+1 (0.500000) | **1415997755216 (0.643921)** |
| prize 1/16 | 2^41 | 2^37 | 1030792151040 (0.468750) | 1326340298262 (0.603150) | **1644686143216 (0.747917)** |

- **Hab25 dominates on all six rows** and reaches the Johnson grid edge at
  Row C 1/8 exactly (adjacent failure mode: past the Johnson grid), one grid
  cell under it at Row C 1/4 and 1/16, and 0.21–0.31% of `n` under it at prize
  scale (adjacent failure mode: exact budget failure at the forced band
  `m_min(r+1)`).
- **GKL24 margins** (exact bound `(n+6)/eta* + 2/(eta*(beta - beta^{3/2}))`,
  `beta = (n-r)/n`, `eta* = beta^3 - (k-1)/n`): 99.98–101.83 bits under `B*`
  (Row C), 43.90–45.60 bits (prize). Its edge is radius-limited: the exact
  integer gate `(n-r)^3 > (k-1)n^2` holds at `r` and fails at `r+1` on every
  row.
- **Hab25 margins** at the witness band: 36.77–48.59 bits (Row C); the prize
  edges are budget-sharp (0.01–0.05 bits, `m_witness = m_budget_max`), decided
  by the exact 14th-power integer comparison
  `(2m+1)^14 n^7 <= 9 * 2^14 (k-1)^3 B*^2`.
- Rates 1/8 and 1/16 gain from GKL24 alone (+65/+139 grid cells at Row C,
  ~+2^37/+2^38.1 at prize); rate 1/4 cannot gain from any 1.5-Johnson result
  (crossover at `Delta_C = 3 - sqrt(5)`).

Both columns certify, via `thm:sparsify`, `sigma_C(delta) <= q * eps_mca` on
their bands — see the companion audit note.

## Replay

```text
python3 experimental/scripts/verify_corridor_unconditional_safe_edges.py --check    # < 1 s
python3 experimental/scripts/verify_corridor_unconditional_safe_edges.py --write    # regenerate the JSON
```

`--check` regenerates the JSON deterministically, compares it to the committed
file, and re-runs the full exact-integer battery (GKL24 gates at `r` and
`r+1`, both budget comparisons at the claimed edges, Hab25 adjacent failure
one grid step past each edge). No floats in any verdict; floats appear only in
reported log2 margins. External proof audits and provenance:
`github.com/latifkasuli/mca` @ `3fea63a` (`docs/gkl24-proof-audit.md`,
`docs/bchks25-thm46-import-audit.md` section "Hab25 proof audit",
`docs/gkl24-corridor-import-audit.md`).

## Non-claims

- **Below-band move only.** The corridor decision candidates sit at
  `delta_A ~ 0.745 / 0.870 / 0.935` (`A = k + n/N'_dec + 1`), far above every
  radius here; the corridor band `(Johnson, cap)` and the five
  certification/counting blockers of the clean-rate program are untouched.
  Nothing in this packet decides any corridor row.
- **Idealized `q_line`.** Row C's literal ~2^250 prime is unpinned (qa3 flag
  C1(b)); prize `2^255.9` is a convention. Verdicts are decided against the
  exact pinned `B*` integers and inherit to any literal prime at those scales.
- **Provenance.** Both imports are ePrints, not peer-reviewed: GKL24 =
  2024/1810 **v3** (2025-03-30, sha256-pinned; v1 contained an acknowledged
  critical mistake), Hab25 = 2025/2110. A live-version check against the
  pinned artifacts is recommended at merge time.
- **No deployed-KoalaBear claim.** On the `rho = 1/2`, `q ~ 2^185.9` row the
  proved Hab25 quadratic bound certifies only `delta <= 0.2045 < 1/4`, and the
  linear-in-n constant of BCHKS25 Thm 4.6 remains conditional (gap G4) per the
  #272 packet. The corridor rows are exactly the `q >~ 2^220` regime where the
  quadratic bound is budget-free; the two packets cover complementary regimes.
- **Shape.** `l = 1 / M = 1` affine line (= `def:mca`) only; GKL24 Thm 4 gives
  `l > 1` affine subspaces at cost factor `l`; `M > 1` curves are not covered
  by either import.
