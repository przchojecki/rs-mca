# Diagonal `c2 (1,1,2)` aligned-positive unramified block: all six cells closed

**Status:** proved — every one of the six aligned-positive **unramified**
(`w != 0`) allocation cells of the diagonal `c2 (1,1,2)` source line is
excluded over the deployed field. Two cells are empty already at the
necessary q-slice identity; the other four have q-slice survivors and are
excluded by the **full colored quotient** system. Remaining unramified
cells: **none**.

**Row:** KoalaBear MCA at `2^-128`, deployed field `F_2130706433`, exclusions
taken over `F_(2130706433^6)` and every required intermediate extension.

**Direct target:** workboard item K3, the aligned-positive unramified branch
of the saturated diagonal `c=2` `(1,1,2)` source line — i.e. exactly the six
cells that **our own** earlier packet in this same directory,
`kb_mca_v4_m2_u2_saturated_112_q_slice_exclusions_v1.md`, lists at `(6.1)`
under "Still open in this upstream packet", and exactly the six that its
verifier still prints as `remaining_unramified=6`. That identification is
**established**: `(6.1)` prints our partition verbatim. It is a different
question from, and must not be confused with, the *probable but
unestablished* correspondence with another contributor's atlas discussed in
section 4.

**Quantifier:** every admissible reconstructed saturated source-line
`(1,1,2)` candidate in the aligned-positive sign with `w != 0`: both
internal-edge templates, all three residual-square allocations, over the
deployed degree-six field and every finite extension in which a component
endpoint can live.

**Parent:** the pinned `c2 (1,1,2)` source-line gates —
`..._source_line_internal_star_reconstruction` and
`..._source_line_q_slice_resultant_gate` (all six cells), plus
`..._source_line_colored_quotient_compiler` (the four full-quotient cells) —
and, upstream, the saturated 112 q-slice packet at `543db66f` whose
`(6.1)` frontier this note discharges.

**Provenance and audit:** the six exclusion proofs were produced by the Codex
worker lineage and audited into the canonical DAG at
<https://github.com/AllenGrahamHart/rs-mca-prize-dag>. The integrating audit
record is the roadmap-r3 rate-half work cycle
`notes/work_cycles/roadmap_r3/14-rate-half-20260730-20260803.md`, whose five
burn-downs "aligned unramified determinant router", "moving-mixed full
quotient close", "fixed-same full quotient close", "fixed-swap full quotient
close" and "fixed-mixed full quotient close" carry the per-cell ledgers
reproduced in section 2; canonical prize pin
`1b2c2ee46951ef5031e100b21f4edd1eeb24b177`. Integration commits, all
2026-07-31: `2cb1206a` (moving-swap), `2d988aba` (moving-same), `98a63928`
(moving-mixed), `32d34bc2` (fixed-same), `000417d8` (fixed-swap), `525aa1a6`
(fixed-mixed); the nodes were carried through the manifest refactor
`4274661c` (2026-08-03). On 2026-08-06 every node's `verify.py` (claim
contract, dependency edges, custody hashes) and independent `verify_audit.py`
(coverage census, hostile mutations, survivor recount) was replayed **PASS**
in the canonical checkout under the local RAM guard; the recorded PASS lines
are pinned in the certificate. This note carries the census, the per-cell
mechanism ledger, and a self-contained arithmetic verifier; the full proof
artifacts live in the canonical DAG under
`background/nodes/rate_half_kb_m2_r4_diagonal_c2_112_aligned_positive_unramified_*`.

**Exact-verifier replay, 2026-08-06 — 11 PASS, 4 not completed on this
host.** Over and above the contract and audit verifiers, the FLINT-backed
per-cell exact component verifiers were re-run in the canonical checkout.
Eleven printed PASS, and their own counters agree with section 1 line by
line — `FIXED_SAME_EXHAUSTIVE norm_factors=28 survivors=4`,
`FIXED_SWAP_EXHAUSTIVE norm_factors=26 survivors=1`,
`FIXED_MIXED_DEGREE5 norm_factors=25 survivors=4`,
`FIXED_MIXED_LINEAR norm_factors=10 survivors=0`,
`FIXED_MIXED_OFF_COMMON branches=20 endpoints=5 boundary=5`,
`MOVING_MIXED_EXACT deployed_orientations=4 rejected=4`, and the three
`..._EXACT`/`..._QUOTIENT` lines reporting `rejected` equal to
`q_slice_survivors` in every case. The export verifier cross-checks all of
these against the certificate's per-cell ledger. Four scripts did **not**
complete: `moving_same/verify_exact.py`, `moving_swap/verify_exact.py`,
`moving_mixed/verify_exhaustive.py`, `moving_mixed/verify_survivors.py`. Each
imposes its own internal 60-second per-stage subprocess cap and at least one
stage exceeded it on this host, raising `TimeoutExpired`. **No assertion
inside any of the four failed** — this is a host-speed observation, not a
rejection and not a failed proof. Those cells rest here on their contract and
audit verifiers (both PASS above) and on their canonical replay at close.

## 1. The census

The block is the exact product of two axes. The **template** axis is the
internal-edge assignment of the normalized star `J_0 = {2, 1/2, b, 1/b}`:

```text
fixed-moving  (FM):  internal edges {2,1/2} and {2,b}
moving-moving (MM):  internal edges {2,b}   and {2,1/b}.   (KBAPU6-0)
```

The **allocation** axis is the distribution of the aligned target's two roots
between the two residual quadratics of `(U^2 - W V^2)/W^2`; unique
factorization gives exactly three, `same`, `swap`, `mixed`. Hence

```text
{FM, MM} x {same, swap, mixed}  =  6 cells.               (KBAPU6-1)
```

These are **our** cell coordinates. We write them `FM-same`, `MM-mixed`, and
so on; they are not, and are not claimed to be, anyone else's labels (see
section 4).

Every cell must satisfy the necessary degree-eight `J_1` q-slice identity

```text
Res_T(q(T), U(T,W)^2 - W V(T,W)^2)
  ~ (W-w)^4 ((W-k_1)(W-k_2))^2,      w != 0.               (KBQS-1)
```

`(KBQS-1)` is necessary only. Four of the six cells have `(KBQS-1)`
survivors, and are closed instead by the two **sufficient-direction** norm
identities of the colored quotient system,

```text
Res_T(P_J, G) ~ K_5^4 q^2,
q^2 Res_T(P_I, G) ~ R_7^4,          G = U^2 - W V^2.       (KBQS-2)
```

The block is tiled by closure route:

```text
q-slice EMPTY          MM-same, MM-swap                     2
full-quotient EMPTY    MM-mixed, FM-same, FM-swap, FM-mixed 4
                                                 total      6
remaining unramified cells                                  0.  (KBAPU6-2)
```

Retained frontier inside the block: **none**. The residual
`rate_half_band_closure` frontier below this block is packet and source-row
assembly, not another cell of this allocation ledger.

Per-cell endpoint arithmetic, as replayed by the verifier:

| cell | direct component | norm degree | factors | endpoint candidates | split | q-slice survivors |
|---|---|---|---|---|---|---|
| MM-same | reciprocal cubic (minor-conic resultant, not divisible by it) | 272 | 21 | 21 | 8 boundary + 8 no common determinant/conic `w` + 5 failing `w` | 0 |
| MM-swap | exceptional norm on `p*t+5p+t=0` | 26 | 6 resolved | 6 | 4 boundary + 2 failing determinant candidates | 0 |
| MM-mixed | irreducible 91-term bidegree-`(12,12)` component | 1224 (in `t`) | 38 | 4 q-slice points, field degrees `3,3,7,7` | 2 embed in `F_(p^6)` (degree 3) + 2 do not (degree 7) | 4 |
| FM-same | reciprocal quartic | 472 | 28 | 20 | 12 boundary + 4 empty + 4 base-field points | 4 |
| FM-swap | reciprocal cubic | 333 | 26 | 24 | 12 boundary + 11 empty + 1 quadratic-field point | 1 |
| FM-mixed | reciprocal degree-five component | 338 | 25 | 19 | 9 boundary + 6 empty + 4 quadratic-field points | 4 |

Every split sums to its candidate count (`8+8+5=21`, `4+2=6`, `12+4+4=20`,
`12+11+1=24`, `9+6+4=19`); the verifier re-adds all of them and rejects a
mismatch. The survivor counts are exactly the `survivors=` fields printed by
the nodes' own `verify_audit.py`, which the verifier cross-checks against
this table.

Off-common (residual cofactor) ledgers, all resolving onto the explicit base
forbidden product:

```text
cell       residual cofactor grid   combinations   distinct endpoints
MM-same    7 endpoint factors                 7            7  (p)
MM-swap    7 endpoint factors                 7            8  (p)
MM-mixed   finite intersections              12            6
FM-same    2 x 1 x 1                          2            7  (p,t)
FM-swap    2 x 1 x 1                          2            9  (p,t)
FM-mixed   5 x 4 x 1                         20            5  (p,t).  (KBAPU6-3)
```

`FM-mixed` additionally carries the linear-rank route: the common component
`4p+5t+4=0` supports a quadratic rank curve in `w` whose intersection with
the **raw** kernel conic has degree `116` with ten factors, leaving four
base-boundary cases and twelve `w` values, of which nine are forbidden and
three have no common `b` (`9+3=12`, also re-added by the verifier).

## 2. Per-cell mechanism ledger (work cycle 14, 2026-07-31)

| cell | mechanism (one line) | route |
|---|---|---|
| MM-same | exact `U/V` scale retention plus reciprocal trace descent make the four q-slice equations quadratic in `trace = b + b^-1`; the maximal-minor projections split into a linear component with only forbidden minor-conic support and a reciprocal cubic; the direct minor-conic resultant is not divisible by the cubic, and exact finite-extension replay makes every component `p` gcd linear, leaving five `w` candidates that all fail the original four trace equations | q-slice |
| MM-swap | the swapped-allocation equations are reciprocal quartics in `b`; exact trace descent makes them quadratic in `trace`, and a common trace root forces the four `3x3` coefficient minors to vanish with first-two-row kernel on the Veronese conic; only two admissibility-relevant common components survive (`4p+5t+4`, forbidden support; `p*t+5p+t`, on which the generic common determinant root misses the conic), and both remaining determinant candidates fail the original four trace equations | q-slice |
| MM-mixed | after the same trace descent the support is open factors, the forbidden linear component, one irreducible 91-term bidegree-`(12,12)` component, and twelve finite off-common intersections; on the degree-12 component exact finite-extension replay of the degree-1224 minor-conic norm leaves four q-slice points over fields of degrees `3,3,7,7`, the degree-7 points do not embed in `F_(p^6)`, and all four reciprocal `b` orientations above the two degree-3 traces reproduce `(KBQS-1)` yet fail both identities of `(KBQS-2)` | full quotient |
| FM-same | exact scale retention makes the four q-slice equations quadratic in the fixed-moving coordinate `b`; the common support is open factors, the forbidden linear component, and one reciprocal quartic, whose direct affine minor-conic resultant has a degree-472 norm with 28 factors; the four surviving base-field q-slice points each reconstruct `G = U^2 - W V^2`, reproduce `(KBQS-1)`, and fail both identities of `(KBQS-2)` | full quotient |
| FM-swap | same quadratic-in-`b` gate with a reciprocal **cubic** common component; the degree-333 direct norm's 26 factors leave a single quadratic-field q-slice point, which reproduces `(KBQS-1)` and fails both identities of `(KBQS-2)` | full quotient |
| FM-mixed | the reciprocal degree-five common component's degree-338 norm leaves four quadratic-field q-slice points, all reproducing `(KBQS-1)` and failing both identities of `(KBQS-2)`; the common linear component additionally carries a quadratic rank curve in `w` whose intersection with the **raw** (not residual) kernel conic is replayed over all ten of its degree-116 norm factors, leaving only forbidden `w` or empty `b` fibres; the residual common factors `p=0` and `t^2-4p=0` are boundary | full quotient |

Every cell's ledger is fail-closed at the node: an omitted factor, a
misclassified endpoint, a divided-away rank-drop branch, or an unreplayed
finite extension fails that node's own `verify_audit.py`.

Two disciplines are load-bearing across the block and are recorded here so
they are not lost in the export: (i) all six cells use **affine** minor-conic
resultants, so function-field denominator and rank-drop specializations are
retained rather than divided away; and (ii) `FM-mixed` deliberately uses the
**raw** first-pair kernel conic, whose degree-116 norm contains three
exceptional factor families that the degree-28 residual-conic norm does not.

## 3. Adjacent status (same pin, not part of this block)

`rate_half_kb_m2_r4_diagonal_c2_112_aligned_positive_ramified_q_slice_exclusion`
(the forced-ramified `w = 0` sibling of this block, six template/allocation
cells) is PROVED and was already exported in the saturated 112 packet. The
aggregation node
`rate_half_kb_m2_r4_diagonal_c2_112_source_line_complete_exclusion` is also
PROVED in our tree at this pin; it is **not exported here and nothing about
it is claimed here** — this note ships the six-cell block only.

## 4. Probable correspondence with the upstream aligned-positive atlas — **correspondence probable, not established**

Work on an "aligned-positive unramified six-cell block" of a diagonal
`c2 (1,1,2)` atlas is in flight in the neighbouring contributor lane
(PR #1140 / #1144 / #1149; #1149 is a **draft** whose own note says
cell-specific proof review is outstanding). Everything we say about that
lane is **CONTENT-REVIEWED at its published head, NOT REPLAYED by us** — its
compiler and verifier are outside this packet's compute contract, and no
statement below imports a theorem from it.

Four qualifiers match ours exactly: **`m = 2`**, **diagonal**, **`c2 (1,1,2)`**
(the string "112" denotes `c2(1,1,2)` on both sides, not two different
notations), and **aligned-positive**. Both sides describe a six-cell
aligned-positive unramified block and both call it that.

**That is where the agreement stops, and this note asserts nothing further.**
The two partitions are stated on **different axes**: ours is
`{fixed-moving, moving-moving} x {same, swap, mixed}` — i.e. it contains
three moving-moving cells — while the other partition is *two fixed-moving
label assignments by three root patterns*, and its moving-moving labels were
deleted in a separate change. **No cell-for-cell mapping row exists on
either side**; the one requested on #1140 on 2026-07-31 has still not been
supplied by us or by anyone else. Consequently:

- this note does **not** assert that our six cells are that lane's six
  cells, and no reader should infer it;
- our "6/6 closed" and a "2/6 closed, 4 retained" reading of that lane are
  **not in contradiction** under either identification: retained cells are
  *open*, never shown nonempty;
- the mapping row remains the open coordination item, and is the correct
  next artifact for whichever side prints it first.

This section is published as a **request for the mapping row**, not as a
priority claim. Our closures stand on our own coordinates `(KBAPU6-0)` /
`(KBAPU6-1)` and on the pinned nodes of section 2 alone; they neither depend
on nor corroborate any external artifact, none of which has been replayed by
us. **Correspondence probable, not established.**

Our half of the mapping row, offered so the other half can be written
against it: our six cells are indexed by the internal-edge template
`(KBAPU6-0)` and by which of the aligned target's two roots each residual
quadratic receives; the template axis is *not* a root-pattern axis, and our
three `MM-*` cells are moving-moving in the internal-edge sense of
`(KBAPU6-0)`, which is a statement about `J_0` and need not agree with any
other lane's use of the words "fixed" and "moving".

## 5. Explicitly not claimed

This closes **one six-cell block of one sign of one source line**: the
aligned-**positive**, **unramified** (`w != 0`) allocation cells of the
diagonal `c2 (1,1,2)` source line. It does **not** close the 36-cell
aligned-positive atlas, any outer/transverse frontier, the residual terminal
types `(m,r,delta) = (2,4,2)` and `(2,8,1)` (untouched here), the near-aligned
branch, the full saturated `(1,1,2)` orbit row, the order-two type,
`rate_half_band_closure`, K3, any owner/charge/payment atom, the KoalaBear
row, LIST, MCA, or either Prize problem. Packet and source-row assembly
remain open.

All exclusions are exact over the deployed prime `F_2130706433` and its
degree-six extension and are **not characteristic-uniform**; they do not
transfer by themselves to other allocations, orientations, or prize rows.
In four of the six cells the q-slice itself is **not** empty — closure there
is by the full colored quotient identities `(KBQS-2)`, and the surviving
q-slice points are retained as regression fixtures rather than deleted. Bare
resultants remain only necessary; every degenerate specialization and
rank-drop branch was reopened before exclusion.

The per-cell exact CAS proofs are **not** re-verified by this note's
verifier; they are pinned by node id to the canonical DAG, where their own
contract and audit verifiers were replayed PASS.

## 6. Falsifier

An admissible deployed-field candidate in any of the six cells satisfying
`(KBQS-1)` and both identities of `(KBQS-2)`; a missing template/allocation
cell (the product `(KBAPU6-1)` is exhaustive by unique factorization of the
residual quadratics — a fourth allocation would break it); an endpoint split
that does not re-add to its candidate count; a norm factor omitted from a
finite-extension replay; a rank-drop or denominator branch divided away
rather than retained; a survivor count disagreeing with the node's own audit
verifier; or an off-common cofactor combination whose endpoint is not on the
explicit base forbidden product.

## 7. Verifier

`experimental/scripts/verify_kb_mca_v4_m2_r4_diagonal_c2_112_aligned_positive_unramified_six_cell_closure_v1.py`
(pure python, no third-party imports, fail-closed): replays the census
arithmetic of section 1 (the `2 x 3` tiling, exactly one entry per cell, the
route split `2 + 4 = 6`, `remaining_unramified = 0`), re-adds every per-cell
endpoint split and the `FM-mixed` linear-rank split, recomputes the
off-common cofactor grid products, checks the `F_(p^6)` embeddability
arithmetic for `MM-mixed`'s field degrees `3,3,7,7`, cross-checks each cell's
recorded `verify_audit.py` survivor count and each of the eleven exact-verifier
PASS counters against the section-1 table, cross-checks the certificate's
pinned node ids and provenance commits, and checks this note's ledger,
correspondence-discipline and nonclaim sentences plus the workboard addendum.
It reads nothing outside this repository.

The per-cell exact CAS proofs themselves are **not** re-executed by this
verifier; it checks that what they printed is what this note claims. The
proofs are pinned by node id to the canonical DAG.
