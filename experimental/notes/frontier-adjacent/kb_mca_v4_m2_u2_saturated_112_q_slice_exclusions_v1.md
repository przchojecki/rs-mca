---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: In the saturated diagonal c=2 (1,1,2) source-line branch, the necessary J_1 q-slice identity has no admissible near-aligned negative solution, no aligned positive solution on the forced source-ramified locus w=0, and no near-aligned positive solution on the homogeneous endpoint boundary q_hom=Y(T-dY); together with the pinned parent this deletes the complete aligned forced-ramified branch, while the six aligned positive unramified cells remain open.
architecture: null
partition_digest: null
atom_or_cell: K3_M2_U2_SATURATED_112_SOURCE_LINE_Q_SLICE_EXCLUSIONS
quantifier: every reconstructed saturated source-line (1,1,2) candidate in the three stated sign/chart loci over the algebraic closure of the deployed KoalaBear base field
projection_and_unit: necessary degree-eight J_1-slice resultant identity on reconstructed source forms; not a sufficient colored-quotient identity, carrier theorem, slope projection, owner, or payment
claimed_bound: exact deletion of both near-negative internal templates in all three relative-xi orbits including w=0, all six aligned-positive forced-ramified template/allocation cells, and all seven near-positive projective-boundary cells
status: PROVED_NEAR_NEGATIVE_ALIGNED_POSITIVE_RAMIFIED_AND_NEAR_POSITIVE_PROJECTIVE_Q_SLICE_EXCLUSIONS_K3_OPEN
impact: DELETES_THE_COMPLETE_ALIGNED_FORCED_RAMIFIED_SOURCE_LINE_BRANCH_AND_BANKS_THE_TWO_MISSING_NEAR_ALIGNED_SIGN_BOUNDARIES_WITH_SIX_ALIGNED_POSITIVE_UNRAMIFIED_CELLS_OPEN
falsifier: an admissible reconstructed candidate in any stated locus satisfying its necessary q-slice identity, a nonunit fully forbidden deployed-field saturation, a missing relative-xi/template/allocation cell, or failure of the projective infinity-root reconstruction
replay: python3 experimental/scripts/verify_kb_mca_v4_m2_u2_saturated_112_q_slice_exclusions_v1.py --check --tamper-selftest
deep_replay: python3 experimental/scripts/verify_kb_mca_v4_m2_u2_saturated_112_q_slice_exclusions_v1.py --list-deep; then run each printed case serially with --deep-case CASE
---

# KoalaBear saturated `(1,1,2)` q-slice exclusions

## 0. Verdict

The cumulative source-facet packet at commit `c2edcfa5` reduces every
classified saturated source-line `(1,1,2)` candidate to finitely many
reconstructed source forms. Each form must pass

```text
Res_T(q(T),U(T,W)^2-WV(T,W)^2)
  ~ (W-w)^4 ((W-k_1)(W-k_2))^2.                  (0.1)
```

The aligned target quadratic is `tau^*q`; the near-aligned target is
`tau^*chi_Omega`. This packet uses `(0.1)` only as a necessary prefilter.

Three previously open loci are empty:

1. both near-aligned negative templates, all three relative-`xi` orbits,
   including forced ramification `w=0`;
2. both aligned positive templates at `w=0`, for all three residual
   allocations `same`, `swap`, and `mixed`;
3. the positive near-aligned homogeneous endpoint boundary, in seven
   exhaustive template/orbit/sign cells.

The parent already deletes the aligned negative sign. Hence the complete
aligned forced-ramified source-line branch is empty. The six aligned positive
unramified cells remain open.

The separate `prize` worktree has exact proofs for all 18 near-positive
affine charts. They are not imported or claimed here: their last chart alone
has a large exact artifact bundle and should be reviewed as a separate
packet. Thus this note does not claim the complete near-aligned branch from
upstream material alone.

## 1. Pinned parent and scope

The verifier pins the note, verifier, and certificate blobs of

```text
experimental/notes/frontier-adjacent/
  kb_mca_v4_m2_u2_universal_source_facet_census_v1.md
```

at commit `c2edcfa5cbfb8a41e7dea04ae1b34325c90ed5dc`. In particular the
parent proves:

```text
J_0={2,1/2,b,1/b},
q=(T-c)(T-d),
G=U^2-WV^2,
Res_T(q,G) ~ (W-w)^4 target(W)^2,                 (1.1)
```

and deletes the aligned negative sign. It explicitly leaves the aligned
positive and both near-aligned signs open, so none of the exclusions below
is already booked by the parent.

All calculations are over the deployed base characteristic
`p=2130706433`. A unit saturated ideal over `F_p` has no point over its
algebraic closure and hence none over the deployed degree-six extension.

## 2. Near-aligned negative sign

Use

```text
P=cd-2c-2d+1,       Q=2cd-c-d+2,
B=bP+Q,              C=bQ+P.                     (2.1)
```

The parent's negative factor gate leaves `B=0` in the fixed-moving template
and `BC=0` in the moving-moving template. Since

```text
C(b)=b B(1/b),                                      (2.2)
```

inversion of the unordered moving edge pair carries `C=0` to the represented
`B=0` case. On `B=0`, admissibility gives `P!=0`, so `b=-Q/P`.

Exact reconstruction gives the same internal label `z` and the same odd
vector `V` in the two templates, while their even vectors have opposite
sign. They therefore have the same `G=U^2-WV^2`. Its monic residual quartic
has constant coefficient one. For

```text
Omega={xi,d},       xi in {2,1/2,b},
```

the near target has constant coefficient `1/(xi^2 d^2)`, forcing

```text
(xi*d)^2=1.                                        (2.3)
```

The plus branch `xi*d=1` is the collision `d=tau(xi)`. On the minus branch,
two exact resultants and their gcd give:

```text
xi=2:    d=-1/2,  projection (c+2)^4(13c-14)^4;
xi=1/2:  d=-2,    projection (2c+1)^4(14c-13)^4;
xi=b:    2cd^2-2cd+2c-d^2+4d-1=0,
         projection d^2(d-1)^6(d+1)^6(d+2)^4
                    (d^3-6d^2+3d-2)^4.           (2.4)
```

The first two rows reconstruct only `w=-1,+1`. In the last row, `d=0,+/-1`
is forbidden, `d=-2` forces `b=1/2`, and the cubic factor reconstructs only
`w=-1`. Saturating each complete mismatch ideal by exactly these forbidden
factors gives the unit ideal modulo `p`. This includes `w=0`; no negative
forced-ramified fiber was divided away.

The deep replay first verifies template equivalence and then independently
recomputes the three projections, every residue fiber, and all three unit
saturations.

## 3. Aligned positive forced ramification

Put

```text
q(T)=T^2+tT+p,       w=0.
```

The parent's repaired complete-source equations give

```text
U(T,0) in <q>,       V(T,0) in <q> minus {0}.
```

Normalize `V(T,0)=q(T)`. For the positive reciprocal source form write

```text
U_0=x_0+x_1W+x_2W^2,
U_1=x_3(1+W^2)+x_4W,
U_2=x_2+x_1W+x_0W^2.
```

Modulo `q`, define

```text
L=(x_2-px_0, x_3-tx_0),
C=((1-p)x_1, x_4-tx_1),
Gamma=lambda(1-p^2,t(1-p)).
```

Direct reduction gives

```text
(U^2-WV^2)/W^2
 = L^2 W^2 + (2LC-Gamma^2)W + C^2       modulo q. (3.1)
```

Unique factorization has exactly three allocations of the aligned target's
two roots between the two residual quadratics: `same`, `swap`, and `mixed`.
Each gives four polynomial equations.

The corrected fraction-free reconstruction retains the relative `U/V`
scale. Its linear normalization is

```text
fixed-moving:
  lambda=3(2b-1)(p-1)(p+2t+4),

moving-moving:
  lambda=-3(b-1)(b+1)(p-1)(p+2t+4)(5p+4t+5).    (3.2)
```

For fixed-moving, substitute `(3.2)` and saturate by

```text
b(b-2)(2b-1)(b-1)(b+1)
*p(p-1)(p-t+1)(p+t+1)
*(p+2t+4)(4p+2t+1)(5p+4t+5)(t^2-4p)
*(b^2+tb+p)(1+tb+pb^2).                          (3.3)
```

For moving-moving, all four equations are reciprocal quartics in `b`.
Dividing by `b^2` and putting `s=b+1/b` is exact. The endpoint-orbit
collision test descends to

```text
Q_b=p(s^2-2)+t(1+p)s+1+t^2+p^2.                 (3.4)
```

The trace saturation product is

```text
(s-2)(s+2)(2s-5)
*p(p-1)(p-t+1)(p+t+1)
*(p+2t+4)(4p+2t+1)(5p+4t+5)(t^2-4p)Q_b.         (3.5)
```

For each of the six template/allocation cells, the four reduced equations
together with the inverse equation for `(3.3)` or `(3.5)` have basis `<1>`
over `F_p`. The helper also rebuilds the exact five-equation source
reconstruction and checks `(3.1)` before saturation. No unscaled norm
calculation is used.

## 4. Near-positive projective boundary

The finite-root near chart does not contain the endpoint at infinity.
Orient that boundary as

```text
eta=infinity,       ell=d,
w=tau(eta)=0,       q_hom(T,Y)=Y(T-dY).           (4.1)
```

The repaired odd vector and internal label are

```text
V(T,W)=(-d,1+W,-dW),
z=(d-2)/(2-4d).                                   (4.2)
```

Membership `U(T,0) in <q_hom>` gives two linear equations. Together with
the three internal-star equations, these form an invertible `5 x 5` system
for the five reciprocal coefficients of `U`.

The roots of `q_hom` are `d` and infinity. Thus the projective q-slice is

```text
Res_T(q_hom,G)=G(d,W) * coeff_(T^4) G(T,W).        (4.3)
```

Both factors in `(4.3)` are divisible by `W^2`. After exact division, let
the residual quadratics be `R_d,R_infinity`. For each relative orbit
`xi in {2,1/2,b}`, passage requires

```text
R_d R_infinity ~ ((W-1/xi)(W-1/d))^2.             (4.4)
```

Cross-multiplication by the observed leading coefficient avoids any generic
division. The exhaustive cells are:

```text
fixed-moving:  xi=2, 1/2, b                         (3)
moving-moving: xi=2, 1/2 after s=b+1/b descent      (2)
moving-moving: xi=b, two constant/leading signs      (2).
```

All seven fully forbidden saturations are unit over `F_p`. The replay
reconstructs both projective roots, checks both forced `W^2` divisions,
proves reciprocity before trace descent, and splits the other-`xi` equation
as an exact difference of squares.

## 5. Replay and resource contract

The default verifier is inexpensive. It checks the pinned parent blobs and
payload, hashes all five helper modules, reconstructs the certificate, and
runs eleven hostile mutations:

```bash
python3 experimental/scripts/verify_kb_mca_v4_m2_u2_saturated_112_q_slice_exclusions_v1.py \
  --check --tamper-selftest
```

The exact CAS proof has 17 independent cases. List them with:

```bash
python3 experimental/scripts/verify_kb_mca_v4_m2_u2_saturated_112_q_slice_exclusions_v1.py \
  --list-deep
```

Run each name serially using `--deep-case NAME`. The wrapper enforces a
60-second wall cap, kills the whole child process group on timeout, and
prints available partial output. The six aligned ramified cases and seven
projective cases print SHA-256 equation-system digests before acceptance;
the near-negative cases print exact projected factors and residue fibers.

No deep case should be run in parallel on a memory-constrained host. An
external cgroup or container memory limit is recommended; all recorded
replays completed under a 256 MB cgroup.

## 6. Exact frontier and nonclaims

Banked here:

```text
near negative:                    EMPTY
aligned positive w=0:             EMPTY
near positive projective boundary EMPTY
aligned negative:                 EMPTY by pinned parent
aligned forced-ramified branch:   EMPTY after combination
```

Still open in this upstream packet:

```text
aligned positive w!=0:
  fixed-moving  x {same,swap,mixed}
  moving-moving x {same,swap,mixed}.              (6.1)
```

Also not banked here are the 18 separately proved near-positive affine
cells. Consequently this packet does not delete the full saturated
`(1,1,2)` orbit row, the order-two type, K3, any owner/payment atom, the
KoalaBear row, or the Prize problem.

Provenance: the source proofs are `prize` commits `08a2e4de` (near
negative), `e9baa0de` (aligned positive ramified), and `7d2d7aca` (near
positive projective). Their exact helper implementations are reproduced
here rather than imported as opaque status claims.

## 7. Status addendum (2026-08-06) — `(6.1)` is now discharged: `remaining_unramified` is 6 for this packet and **0** in the tree

The six aligned-positive unramified cells listed as open at `(6.1)` —
`{fixed-moving, moving-moving} x {same, swap, mixed}` — are **all six PROVED**
in the canonical DAG, closed on 2026-07-31 in roadmap-r3 rate-half work cycle
14 and replayed PASS on 2026-08-06. Two are empty already at the necessary
q-slice identity; the other four have q-slice survivors and are excluded by
the full colored quotient norm identities. Census, per-cell mechanism ledger,
provenance pins, certificate and self-contained verifier:

```text
experimental/notes/frontier-adjacent/
  kb_mca_v4_m2_r4_diagonal_c2_112_aligned_positive_unramified_six_cell_closure_v1.md
```

**Read the two counters correctly — they are both right.** The verifier of
*this* packet prints

```text
remaining_unramified=6
```

and that number is **packet-local and unchanged**: it reports what *this*
packet, at its own pinned scope, leaves open, and it is pinned by this
packet's certificate and tamper self-test. It is **not** an assertion that the
cells are open in the tree, and it must **not** be edited — editing it would
break the custody chain of a correct historical record. The tree-level
counter is the one that moved:

```text
remaining_unramified (this packet's own scope)   6   unchanged
remaining_unramified (canonical DAG, 2026-08-06) 0   all six PROVED.
```

Anyone reading `remaining_unramified=6` as the current state of the frontier
is reading a packet-scope figure as a tree-scope figure. The sibling note
above is the tree-scope record.

Unchanged by this addendum: `(6.1)`'s own text, every exclusion and nonclaim
in sections 0-6, the 18 unimported near-positive affine charts, and the fact
that this packet still does not delete the full saturated `(1,1,2)` orbit row,
the order-two type, K3, any owner/payment atom, the KoalaBear row, or the
Prize problem. The six-cell closure does not change any of those either.
