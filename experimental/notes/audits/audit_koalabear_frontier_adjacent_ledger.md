# Audit: the Frontier-Adjacent Upper Ledger at Agreement 1116044 (KoalaBear MCA Row)

- **Status:** AUDIT / EXPERIMENTAL.
- **Agent/model:** Claude Fable 5 acting for latifkasuli.
- **Artifact:** `experimental/data/certificates/frontier-adjacent/`
  (README + `koalabear_frontier_adjacent_a1116043_a1116044.json`), verifier
  `experimental/scripts/verify_koalabear_frontier_adjacent.py`.
- **Scope:** first instantiation of the `frontier-adjacent/*.json` packet
  family (agents.md, "What counts as progress now", item 2) at the declared
  next threshold task.

## 1. The task

The agents-log entry "CAP25 v13 identity-prefix frontier merge" (2026-07-04)
identifies "the next threshold task as an adjacent safe-side certificate at
agreement `1116044`" and orders:

> Before promotion to Paper D, build the exact upper ledger for the adjacent
> safe-side step, keep polynomial-loss quotient equidistribution out of finite
> one-step claims unless constants fit inside the printed bit margin, and
> audit the aperiodic-band input separately.

The canonical spec is agents.md, "The complete upper ledger to build at
`a0 + 1`": a first-match, deduplicated sum of paid and residual cells, where
every residual branch carries one of the five labels PAID_BY_THEOREM /
PAID_BY_EXACT_CERTIFICATE / CONDITIONAL_ON_NAMED_INPUT /
CONJECTURAL_WITH_FALSIFIER / COUNTEREXAMPLE_NEW_FLOOR and may not be hidden
inside a point estimate.  This packet builds that object *honestly*: it pays
what theorems pay today, prints exact certificates where they exist, and
names every open cell with its precise blocker instead of a point estimate.

## 2. What is pinned (all margins reproduce upstream's printed values)

All comparisons are exact big-integer inequalities (the ~2M-bit binomial
comparisons of `prop:v13f1-identity-frontier` and the graded-prefix scan
predicates), recomputed from scratch by the verifier (binomials via Legendre
prime-power factorization + product tree; independent modular cross-checks).

- **`a0 = 1116043` is MCA-unsafe**: `C(n,1116043) k > p^67466 (q+k)` holds at
  **+25.6761 bits** (upstream prints `+25.7`), and fails at `m+1` at
  **-5.4985 bits** (upstream `-5.5`).  Verdict at a0:
  UNSAFE_BY_PROVED_LOWER_BOUND, `N(a0) >= B*+1 = 274980728111395088`.
- **List-unsafety at `a0+1 = 1116044`** by two independent exact
  certificates: the c=1 list predicate at **+71.5129 bits**, and — the one
  structural coincidence at this step — `1116044` is *exactly* the
  adjacent-tight c=2 LIST-route edge (`m = 558022`, **+1.8790 bits**, with
  `m = 558023` failing).  The c=1 list route holds through `a = 1116046`
  (**+9.1637**, upstream `+9.2`) and fails at `1116047` (**-22.0109**,
  upstream `-22.0`) — the list row is provably not `2^-128`-list-decodable
  through `1116046`.
- **All prefix-floor scales fail at `1116044` on the MCA route**, verified
  directly (not merely cited): c=1 fails (-5.4985), c=2 fails at `m = 558022`
  (**-75.1323**; the c=2 MCA edge is `m = 558019`, a = 1116038, **+18.3914**,
  with `m = 558020` failing), c=4 fails at `m = 279011`, and no `c >= 8` grid
  contains `1116044` (`v_2(1116044) = 2`; `1116044 = 2^2 * 59 * 4729`).
- **Proved lower mass at `1116044`**: the tangent floor
  `LD_sw >= n - a + 1 = 981109` (the witness half of `prop:v13-tangent`
  needs only `a >= k+1`), `~2^19.9041`.
- **The quotient SAFE_SUM cell**, the only finite theorem-backed *upper* cell
  at this step: `U_sum(n, A, {2,4,8,16,32})` computed exactly at both
  agreements (~`2^1045455`; per-divisor values fingerprinted in the JSON and
  cross-checked modulo `2^61-1` through an independent factorial-table path).
  It is theorem-backed (prop:v13-quotient-safe-sum, declared coverage) and
  astronomically above `B*` — the upper ledger documents this honestly.  The
  zone-(a) norm-exact gate `(N'+2)^{N'} <= q_line^2` is printed for every
  declared order (all pass; boundary: last even order passing is 60, first
  failing 62), so the zone-(b) collision conjecture is *vacuous* at this step
  (active-order cutoff `n/t ~ 31.08`).

## 3. What blocks each open cell (precise blockers)

- **Tangent upper cell**: `r = 981108 > R_tan = floor((n-k)/3) = 349525`, so
  `Paid_tan^hi` is UNAVAILABLE by its own type (def:v13-tangent-cell); no
  other tangent/common-line theorem covers this radius.  OPEN.
- **Aperiodic cell**: the regular overdetermined Hankel branch requires
  `t >= j+1`; here `t = 67468 << j+1 = 981109` (deficiency **913641**) — the
  deep underdetermined regime.  The M5/WP-2.6 pivot machinery exists only at
  deficiency 1 on the toy F_17^32 row.  CONJECTURAL_WITH_FALSIFIER; per the
  task's own wording the aperiodic-band input must be audited separately.
  Named future input: **PR #282** (XR eliminant packets), which itself
  disclaims row-level adjacent-ledger status pending a staircase/SPI/XR
  population bound.
- **Extension cell**: proper extension row (`q_gen = p < q_line = p^6`), so
  the generating-row zero rule does not apply; the safe-side S6 chart
  classification is explicitly undischarged (paid_ledger_functions.md, DAG
  Discharge).  CONDITIONAL_ON_NAMED_INPUT; named future input: **PR #284**
  (F1 minimal-field-descent trichotomy).  The ExtPole arithmetic is printed
  as *hypothetical only*: with the c=1 list floor as base list it would give
  `~2^160.40` (>> B*), but condition (i) of prop:v13-extension (distinct pole
  values give distinct extension-only bad line parameters *for this row*) is
  not certified, and upstream conspicuously does not claim it.  The missing
  input is exactly condition (i).
- **Sparse/plain-CA cell**: no MCA/CA soundness theorem reaches
  `delta = 245277/524288 ~ 0.4678288`.  The proved Hab25-quadratic import
  certifies only `delta <= 428878/2^21 ~ 0.2045`; the
  `604085/2^21 ~ 0.2880502` edge (a = 1493067, **+377023 steps**, delta-gap
  **0.1797786 ~ 0.18**) is conditional on the unproved Hab25 linear-in-n
  constant (gap G4, integrated #272 audit); Johnson is at a = 1482910
  (**+366866 steps**).  Any safety theorem here must be list-size-independent
  (the list at this radius is certified ~2^71.5 over the list budget).  OPEN.
- **Quotient image cell**: no image-lcm certificate at this row; stays at the
  SAFE_SUM grade.

## 4. The two quantified routes (the packet's discovery)

The window at `1116044` can only close in one of two quantified ways:

1. **Conversion route — 5.4985 bits.**  The c=1 floor already certifies a
   list of size `2^160.4336` in `RS[F,D,k+1]` at this radius; the deep-point
   list-to-MCA conversion threshold `(q+k)/k = 2^165.9321` is missed by
   **exactly 5.4985 bits (factor ~45.21)**.  Any `>= 5.4985`-bit sharpening
   of the `thm:A` conversion (or of the pigeonhole floor) at this radius
   flips `a = 1116044` MCA-unsafe and pins the staircase adjacently.
2. **Mass route — 38.03 bits.**  Unsafety-by-counting needs
   `LD_sw >= B*+1 = 274980728111395088`; proved mass is `981109`, leaving a
   deficit of `274980728110413979` (`~2^57.93`), ~38.03 bits above every
   known structured family (the empirical mu4 `+4` moves it to
   `274980728110413975`).  Unknown families would have to carry
   99.9999999996% of the budget.

Route 1 is smaller by ~32 bits and is the falsifier/next-target printed
prominently in the packet (CONJECTURAL_WITH_FALSIFIER).  Symmetrically, the
safe side would need a soundness theorem 0.18 in delta beyond the conditional
radius — so the honest verdict at `1116044` is UNDECIDED_WINDOW_OPEN per
`thm:v13-windows`, with the corridor of `thm:v13-corridor` at
`1116044 <= a*` and no upper endpoint.

## 5. Relation to integrated packets and open PRs

- **#272 (BCHKS25 Thm 4.6 conditional import)** and the corridor safe-edge
  packet (#273/#275 batch): consumed here only as the landmark table's
  conditional/proved external radii; their non-claims (no deployed-KoalaBear
  claim beyond `delta ~ 0.2045` unconditionally) are what make the sparse/CA
  cell OPEN rather than conditional-safe.  Source files are sha256-pinned in
  the packet.
- **PR #282 (XR eliminant packets)**: named future input for the aperiodic
  residual cell; cited as structural progress, not consumed as a bound (its
  own text defers to a separate staircase/SPI/XR rationing input).
- **PR #284 (F1 minimal-field-descent)**: named future input for the
  extension chart classification (S6/F1 trichotomy); cited, not consumed.
- The packet collides with no open PR files. At build time the open queue
  was #281-#284; rechecked at rebase time (2026-07-05, queue #281-#309):
  still no file overlap with `frontier-adjacent/` or this verifier (only the
  routine agents-log.md append). Topically adjacent open PRs — #293/#294
  (crossing localization) and #303 (unsafe-side assembly, incl. an
  `unsafe-at-crossing` packet) — work the same crossing neighborhood from
  the localization/unsafe directions in their own certificate dirs; they
  are natural complements to this safe-side upper ledger, not collisions.

## 6. Non-claims

- No adjacent pin is claimed; `a* = 1116044` remains conjectural
  (prob:v13f1-frontier).
- The upper ledger has OPEN cells, so **no finite `U(a) <= B*` statement**
  is made at either agreement; no deduped finite total is printed (per
  agents.md, residuals are never hidden in point estimates).
- The window at `1116044` remains open per `thm:v13-windows`; this packet
  neither certifies safety nor moves the unsafe edge.
- List-route certificates at `1116044` concern the companion list object.
- The ExtPole number is hypothetical arithmetic, not a floor.
- Polynomial-loss quotient equidistribution is kept out of every finite
  claim (`n^C` costs `21C` bits against a 5.4985-bit margin).

## 7. Replay

```sh
python3 experimental/scripts/verify_koalabear_frontier_adjacent.py --write
python3 experimental/scripts/verify_koalabear_frontier_adjacent.py --check
```

Both modes rerun the full exact recomputation (~131 s measured, dominated by
the five-divisor `U_sum`); `--check` additionally byte-compares the stored
JSON.
