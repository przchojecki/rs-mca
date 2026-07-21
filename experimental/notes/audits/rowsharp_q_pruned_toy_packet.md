# Pruned-Q toy packet: first-match pruned prefix-fiber distributions at exactly enumerable rows

- **Status:** AUDIT / EXPERIMENTAL / calibration (enters no proof).
- **Agent/model:** Claude Fable 5 acting for AllenGrahamHart.
- **Artifact:** verifier `verify_rowsharp_q_pruned_toy_packet.py` (stdlib-only, zero-argument, fail-closed,
  exact big-integer/Fraction decisions, floats only in display; ~2 s; passes
  identically under `python3` and `python3 -O`; prints
  `RESULT: PASS (104/104 checks; 4/4 mutation controls caught)`, exit 0)
  + machine-readable `rowsharp_q_pruned_toy_packet.json` + this note.
  [Suggested in-tree placement: `experimental/scripts/verify_rowsharp_q_pruned_toy_packet.py`,
  `experimental/notes/audits/rowsharp_q_pruned_toy_packet.md`,
  `experimental/data/rowsharp_q_pruned_toy_packet.json`.]
- **Answers:** agents.md Good-first-PR #1, verbatim: "Write a small exact Q toy
  packet that tests `prob:row-sharp-q` on a row where the full fiber
  distribution can be enumerated."
- **Positioning:**
  - `experimental/notes/rowsharp_q_external_calibration.md` +
    `experimental/scripts/qsp_fiber_census.py`: the in-tree censuses are
    RAW-distribution only. This packet reproduces their committed exact numbers
    digit-exact (the cross-implementation anchor: independent enumeration /
    stdlib big-int DP vs the numpy int64 DP) and then supplies what the tree
    lacks: the fiber distribution AFTER first-match pruning, per cell and
    cumulative, plus the exact residual mass tau.
  - `experimental/scripts/qsp_modeatnull_structure.py`: classifies the members
    of ONE fiber (the argmax at (41,20,10,2)). This packet applies the same two
    classifiers to EVERY member of EVERY fiber and prints the resulting pruned
    distributions; its mode-at-null assertions are replayed exactly.
  - `experimental/notes/thresholds/atom_toy_r_gt_w.md`: a DIFFERENT atom —
    `prob:entropy-inverse-q` (Q1), the R>w moment-curve wall-break,
    asymptotic-lane, extension fields. This packet is the finite
    `prob:row-sharp-q` / `def:q-row-atom` object at R=w census rows; no overlap.
  - `experimental/notes/audits/audit_quotient_cell_prefix_fiber_and_split_pencil_census.md`:
    exhibited a super-polynomial QUOTIENT-CELL fiber at rate-1/2 rows (the
    quotient payment is load-bearing). Complementary direction here: at
    enumerable rows the quotient-type cells are REMOVED and the residual
    distribution itself is measured.

## 1. What the packet tests

`experimental/grande_finale.tex` L3574-3580:

> **Problem (Row-sharp multilevel Q target, `prob:row-sharp-q`).** For each
> active row, after every earlier first-match cell has been removed, prove
> max_z |P_Q(z)| <= R_Q^row C(n, a_+) |B|^{-(a_+-K)} with the literal row
> constant R_Q^row fitting the remaining integer budget. A moment proof must
> use the actual residual mass and satisfy (eq:finite-moment-criterion) with
> the allocated bit margin.

with `def:q-row-atom` (L3414-3430) normalization R_Q^max = |B|^w max_z
|P_Q(z)| / C(n,a_+), full-slice mean (L1837-1838: "The normalization is taken
from the full profile slice, not from the possibly much smaller residual
mass"), and the binding deployed full-budget allowance (L3546 / L3441): the
Mersenne-31 list row's "maximum-prefix-fiber overhead may be at most $8.4152$
times the full-slice average."

Toy instantiation (his census convention, `qsp_fiber_census.py`): depth-w
power-sum prefix map on m-subsets of the order-N subgroup D of F_p^*;
n -> N, a_+ -> m, B -> F_p, w -> w.

## 2. The pruning ledger used (definitions, stated honestly)

First-match semantics, `grande_finale.tex` L1842-1849:

> "First match" means that a slope is removed as soon as one of its witnesses
> occurs in an earlier ordered cell; "residual" means that only witnesses
> surviving those removals remain; and "primitive" means that the row-specific
> quotient, planted, field-descent, rank, and ray-saturation certificates
> named by the atlas have all been applied.

Cells removed — HIS OWN in-tree toy quotient-pullback classifiers
(`qsp_modeatnull_structure.py` L20-23: "coset-union members (unions of
mu_2-antipodal pairs) ... dilation-stable members (gS = S for some g != 1)
... the obvious quotient-pullback classifiers"), applied by us in first-match
order:

- **C1 coset-union**: S = -S (union of antipodal mu_2-pairs);
- **C2 dilation-stable**: gS = S for some g in D, g != 1 (equivalently, S is a
  union of cosets of a nontrivial subgroup of D).

Residual P_Q(z) = trivial-multiplicative-stabilizer members of Fib_w(z).
C1 is contained in C2 whenever -1 in D (all rows here), so the cumulative
residual is independent of the cell order (consistent with L1283-1284, "order
these cells arbitrarily"); the order affects only the printed per-cell
attribution.

**Flagged scope limit (our reading, not his text):** the deployed-row ledger's
other cells — tangent, common-support, planted, field-drop, extension, rank
(L3561) — have NO in-tree toy-scale instantiation and are NOT modeled here.
They are reported as not-instantiated rather than silently treated as empty.
If the intended toy reading of those cells differs, the raw side of this
packet is unaffected and the pruned side is labeled throughout as "pruning by
the two quotient-pullback classifiers."

## 3. Verification design

Raw anchors (all digit-exact, fail-closed): checksum sum_z N_w(z) = C(N,m);
max, null, and sum_z N_w(z)^2 against
`experimental/data/rowsharp_q_external_calibration.json` on all 8 row-depths;
the printed 4-decimal max-to-mean ratios of `rem:capff1-collision-gap`
(1.0012 / 1.2126 / 2.6722 and 1.0022 / 1.2101 / 4.1034); SP mass
(= sum N^2 - C(N,m), eq:imported-second-moment) nonnegative; and the full
mode-at-null datum replay at (41,20,10,2) (null 66, max 133 at (11,0), orbit
line uniform, argmax-fiber classifier counts (0,0)).

Pruned side, two independent computations compared per fiber: (i) per-member
classification during direct enumeration ((17,16,8), (41,20,10): C(16,8) =
12870 and C(20,10) = 184756 subsets); (ii) subgroup-lattice inclusion-
exclusion of exact coset-DPs (|Stab != 1|(z) = sum over nonempty prime subsets
Q of primes(N), sign (-1)^(|Q|+1), of the census of unions of m/prod(Q)
mu_prod(Q)-cosets). For the DP rows ((101,50,25,2), (257,64,34,1)) route (ii)
supplies the cells and closed-form totals C(10,5) = 252 and C(32,17) =
565722720 are gated, plus the derived fact that all cell mass sits in the
null fiber at these depths. Monotonicity 0 <= pruned(z) <= raw(z) (L1895) and
the mass identity sum_z pruned = C(N,m) - |C1 u C2| are gated per row-depth.

(257,64,34,2) was excluded by compute budget (the row was shrunk to depth 1,
which still carries a committed exact anchor, rather than raising limits).

Mutation controls, each required to flip at least one named check: M1 wrong
pruning-cell membership ((p-x+1) antipode) — caught by cell totals +
classification-vs-inclusion-exclusion; M2 off-by-one depth — caught by the
raw anchors; M3 wrong bound constant (8.4152 -> 1.0) — caught by the G2 gate
(the comparison is live, not vacuous); M4 wrong domain (first N elements
instead of the subgroup) — caught on the (257,64,34) row (on (17,16,8) the
subgroup IS all of F_17^*, so that row alone could not catch M4; the control
set includes both).

## 4. Results (all exact; ratios to 6 decimals)

| (p,N,m,w) | raw max | raw null | pruned max | pruned null | rm C1 | rm C2 | cells at null | R_raw | R_pruned | < 8.4152 |
|---|---|---|---|---|---|---|---|---|---|---|
| (17,16,8,1)   | 758 | 758 | 757 | 688 | 70 | 0 | 70 | 1.001243 | 0.999922 | OK |
| (17,16,8,2)   | 54 | 54 | 49 | 48 | 70 | 0 | 6 | 1.212587 | 1.100311 | OK |
| (17,16,8,3)   | 7 | 6 | 5 | 0 | 70 | 0 | 6 | 2.672183 | 1.908702 | OK |
| (41,20,10,1)  | 4516 | 4516 | 4509 | 4260 | 252 | 4 | 256 | 1.002165 | 1.000612 | OK |
| (41,20,10,2)  | 133 | 66 | 133 | 60 | 252 | 4 | 6 | 1.210099 | 1.210099 | OK |
| (41,20,10,3)  | 11 | 6 | 11 | 0 | 252 | 4 | 6 | 4.103417 | 4.103417 | OK |
| (101,50,25,2) | 12392018052 | 12392018052 | 12392017800 | 12392017800 | 0 | 252 | 252 | 1.000003 | 1.000003 | OK |
| (257,64,34,1) | 6304622609083424 | 6304622609083424 | 6304622609069747 | 6304622043360704 | 565722720 | 0 | 565722720 | 1.000000 | 1.000000 | OK |

Exact residual masses tau = sum_z |P_Q(z)| / C(N,m) (the "actual residual
mass" a moment proof must use, `prop:q-moment-order-floor` L3464-3477):
12800/12870, 184500/184756, 126410606437500/126410606437752,
1620288009964624704/1620288010530347424.

## 5. Verdict and by-catch data

**Verdict: row-sharp Q SUPPORTED at every tested row.** Pruned max <= raw max
everywhere (as L1895 requires), and every pruned overhead R_pruned sits below
the binding deployed full-budget allowance 8.4152 — including the two
Poisson-boundary depth-3 rows, where his printed table pre-explains ratio
growth. The pre-registered falsifier shape (a pruned max fiber above 8.4152x
the full-slice average at a tested row) did not occur.

New data absent from the raw censuses:

1. **Where the raw argmax is the null fiber, pruning usually moves the max off
   it.** At (17,16,8,1), (17,16,8,2), (41,20,10,1), (257,64,34,1) the
   quotient-pullback cells are concentrated at z = 0 and the pruned max
   relocates to a clean fiber; at (17,16,8,1) the pruned overhead even drops
   below the full-slice average (R_pruned = 0.999922 < 1). The exception is
   (101,50,25,2): only 252 members leave a ~1.24e10 null fiber, which remains
   the argmax.
2. **The mode-at-null (.,0)-line question gets a number.** At (41,20,10,2) the
   suppressed null fiber 66 loses its 6 quotient-pullback members: 66 -> 60
   (suppression deepens; the max/null ratio grows from 133/66 = 2.02 raw to
   133/60 = 2.22 pruned). The argmax fiber 133 is
   untouched, confirming at distribution level his single-fiber datum that it
   contains no classifier members. This is direct input to the open item in
   `rowsharp_q_external_calibration.md` ("decide whether the (.,0) line at
   (41,20,10) is rung-charged under the intended reading of 'quotient rungs
   separated'"): charging the obvious quotient-pullback rungs makes the null
   anomaly worse, not better, so the exchange-compression alternative gains
   support at rows of this shape.
3. **Depth-3 null fibers are 100% quotient-pullback.** At both enumerable rows
   the entire depth-3 null fiber (6 members each) consists of cell members:
   pruned null = 0. The Poisson-boundary maxima behave oppositely: 7 -> 5 at
   (17,16,8,3) but 11 unchanged at (41,20,10,3) (that argmax fiber is fully
   primitive).
4. **First-match attribution.** At (41,20,10): |C1| = 252 (S = -S), |C2\C1| = 4
   (the pure mu_5-coset unions; the two mu_10-unions land in C1 first). At
   (101,50,25): C1 empty (m odd), |C2| = 252. At the 2-power rows C2\C1 is
   empty (the only prime is 2).

## 6. What this gives the six-input list

- **#1 "row-sharp finite Q / prefix max-fiber certificates":** the first
  in-tree pruned (post-first-match) max-fiber data, per cell and cumulative,
  with exact residual masses tau at every exactly enumerable census row — the
  quantities `prob:row-sharp-q` and `prop:q-moment-order-floor` are stated in.
- **#5 "exact extension and quotient payments" (calibration only):** exact
  per-fiber sizes of the quotient-pullback classes at toy scale, including
  where they concentrate (the null fiber at low depth).

## 7. Non-claims (fence)

This packet does **not**:

- prove `prob:row-sharp-q` (or any R_Q^row bound) for any deployed row — toy
  rows are not deployed rows (the deployed bulk sits at mean ~ q/k with
  n = 2^21; these rows are N <= 64);
- claim the pruning ledger used is HIS intended toy ledger beyond the two
  classifiers his own script names; the remaining deployed-row cells (tangent,
  common-support, planted, field-drop, extension, rank) are not modeled, and
  the residual here is "trivial-stabilizer" primitive, not atlas-primitive;
- touch SS0.4 or SS0.5, move any threshold, or alter any certificate; the
  official score is unchanged;
- enter any proof: calibration evidence only, in the sense of
  rem:capff1-collision-gap's "These tables are calibration evidence only and
  enter no proof";
- claim anything about (257,64,34,2) or larger rows (excluded by compute
  budget), or about the f64 ladder rows (577, 1153).
