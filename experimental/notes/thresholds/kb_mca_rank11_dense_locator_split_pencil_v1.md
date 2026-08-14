---
workboard_item: K3/K4
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: In the pinned post-near rank-eleven anchor-star setup, dense-locator normalization forces at least 990810934 parts per billion of record/eleven-subset incidences onto positive-dimensional owner or kernel components; at least 540546700 parts per billion of records have a 98-percent component star; every rank-nine star is a split-pencil cell carrying at most 45567658 records; every lifted rank-nine plane either carries at most 1434405 records or shares a 134944-coordinate pair core; and one fixed nine-subset carries at least 2578110 records in one typed component lane, routed to a fixed kernel chart, a shared-core rank-nine plane, or a rank-eight owner flat of error rank at most three.
architecture: POST_NEAR_ERROR_RANK11_DENSE_LOCATOR_COMPONENT_ROUTE_V1
partition_digest: inherited post-near rank-eleven route of PRs 1168 and 1169; no new first-match atom or partition digest
atom_or_cell: rank-eleven dense-locator component family, one fixed rank-nine split-pencil cell, its lifted owner plane, and one fixed nine-coordinate component chart
quantifier: Every survivor satisfying the pinned rank-eleven 32-anchor, 18-dense-root, ten-dimensional correction-space setup, uniformly for 10<=K'<=1048576
projection_and_unit: Distinct bad finite slopes per received line at record level; record/coordinate-subset incidences only where explicitly stated
claimed_bound: isolated equivalent <=2526815879272440; component incidence >=990810934 ppb; 98-percent records >=148639925144138894; one fixed rank-nine cell <=45567658 records; low-common-core rank-nine plane <=1434405 records; one typed fixed nine-subset >=2578110 records
status: PROVED LOCAL THEOREM PACKET / GLOBAL ROW OPEN
impact: ROUTE_CUT / BASE-FIELD-NORMALIZED SPLIT-PENCIL AND FIXED-CHART LEDGER
falsifier: A proper eleven-coordinate intersection with isolated multiplicity above 198; a record-star violating the rank trichotomy; a fixed rank-nine cell with more than 45567658 assigned records; a lifted plane above 1434405 records whose shared pair core has size below 134944; or failure to find the printed 2578110-record fixed nine-subset target.
replay: python3 experimental/scripts/verify_kb_mca_rank11_dense_locator_split_pencil_v1.py; python3 experimental/scripts/verify_kb_mca_rank11_dense_locator_split_pencil_v1.py --tamper-selftest; python3 experimental/scripts/verify_kb_mca_rank11_dense_locator_split_pencil_v1_independent.py
---

# KoalaBear rank-eleven dense-locator and split-pencil route

Status: **PROVED LOCAL THEOREM PACKET / ZERO DEPLOYED LEDGER MOVEMENT**.

Exact parent: PR #1169 head
`b4bad860750f91955dbaead8f2b5a0fdef1f1343`.

This packet imports eight public, commit- and tree-pinned prize-DAG theorems.
They begin after the rank-eleven branch has produced one fixed degree-31
anchor interpolant, eighteen dense-pair roots, and a ten-dimensional
relative correction space.  They end with an exact ledger for one fixed
rank-nine ten-coordinate cell, a low-core/large-shared-core dichotomy for
its lifted owner plane, and one overlap-correct fixed nine-coordinate target.
They do not select the complete component lane or assign chronology across
different targets.

Throughout, write

```text
R=1048576,  d=67472,
n'=R+K',   m'=d+K',    10<=K'<=1048576.
```

The output unit is kept typed.  A record is one distinct finite bad slope
on the fixed received line.  An incidence is a pair consisting of a record
and a coordinate subset of one of its agreement supports.  Incidence
density is never silently converted to record density.

## 1. Dense-root saturation

Let

```text
D_H(X,Z)=H(X,Z)-a_0'(X)-Z b_0'(X)
```

be the deviation interpolant of the fixed 32-record anchor star.  It
vanishes at eighteen distinct dense-pair slopes, while ten other values
span the full correction space `V'`, of dimension ten.  With

```text
q(Z)=product_(i=1)^18 (Z-gamma_i),
```

coefficientwise division gives

```text
D_H=qG,                 deg_Z G<=13.
```

Because `q` is monic, the coefficients of `D_H` in degrees `18,...,31`
triangularly recover all fourteen coefficients of `G`.  Hence

```text
span{H_j:j>=2}=V'.
```

Every correction space `W<=V'` which absorbs all high coefficients is
therefore exactly `V'`.  The putative absorbing dimensions `2,...,9` are
empty.  This identifies one common ten-dimensional space; it does not
aggregate its components.

## 2. Dense-locator component incidence

For every non-dense record define

```text
R_gamma=(h_gamma'-a_0'-gamma b_0')/q(gamma) in V'.
```

The denominator is nonzero and this normalization preserves span.  At a
coordinate `x`, rich agreement becomes

```text
(a_0'-r_0')(x)+Z(b_0'-r_1')(x)+q(Z)R(x)=0.          (2.1)
```

After bihomogenization, (2.1) has divisor class at most
`18 H_Z+H_R` on `P^1 x P^10`.  Eleven coordinate equations therefore
have at most

```text
(18 H_Z+H_R)^11=198 H_Z H_R^10
```

isolated solutions counted with local multiplicity, even if excess
positive-dimensional components are present.

Summing over eleven-subsets gives the isolated-record equivalent

```text
A_iso(K')=ceil(198*C(n',11)/C(m',11))
         <=A_iso(10)=2526815879272440.               (2.2)
```

The endpoint is `K'=10` because every factor

```text
(R+K'-i)/(d+K'-i),       0<=i<=10,
```

decreases with `K'`.  An unsafe line leaves at least

```text
N_min=B_star+1-134944-18=274980728111260126
```

non-dense post-near records.  Thus isolated incidences occupy at most
`9189066` parts per billion, and positive-dimensional component incidences
occupy at least

```text
990810934 parts per billion.                         (2.3)
```

At a rich point such a component is either a full-evaluation-rank affine
owner curve or a rank-deficient kernel component.  One of the two lanes
carries at least `495405467` parts per billion.  These are incidence
statements, not component or record counts.

## 3. Record-star amplification

Let `tau=98/100`.  If `alpha` is the fraction of records whose own
component-incidence density is at least `tau`, then (2.3) gives

```text
990810934/10^9 <= alpha+(1-alpha)tau,
alpha >= 540546700/10^9.
```

Consequently at least

```text
148639925144138894
```

records have a 98-percent component star.  For each such record, averaging
eleven-subsets over their ten-subsets gives a ten-subset `B` with at least

```text
E(K')=ceil(98(m'-10)/100)
```

component extensions.  Exactly one of the following occurs.

1. `rank(ev_B)=10`: all component extensions lie on one affine owner, of
   support deficiency at most `22320`.
2. `rank(ev_B)=9`: with `ker(ev_B)=F u`, at least `45153` full-rank
   extensions lie on the affine owner pencil with direction
   `beta*(-gamma u,u)`.
3. `rank(ev_B)<=8`: the evaluation kernel has dimension at least two.

The trichotomy is recordwise.  Targets attached to different records are
not identified by this theorem.

## 4. One fixed rank-nine split-pencil cell

Fix one rank-nine ten-subset `B`, and let `u` span its evaluation kernel.
The affine codeword-pair owners agreeing with the received pair on `B` form
one affine plane `Pi_B`, with directions `(u,0)` and `(0,u)`.  A record of
slope `gamma` gives one line in `Pi_B`, with direction

```text
(-gamma u,u).
```

Distinct slopes give distinct line directions, so any two record lines
intersect at a unique owner point.  If `t_p` record lines pass through owner
point `p`, and the cell contains `g` records, then

```text
sum_p C(t_p,2)=C(g,2).                               (4.1)
```

Let `J_B` be the coordinates in `Z(u)` where the entire owner plane agrees
with the received pair.  Every owner core is the disjoint union

```text
C_p=J_B disjoint_union P_p,
```

and the off-root petals `P_p` are pairwise disjoint across owner points.
The `45153` full-rank extensions per record therefore give

```text
45153 g <= sum_p t_p |P_p|.                          (4.2)
```

For one fixed owner, exception sets for distinct slopes are disjoint away
from its pair core.  Pair noncontainment gives `|C_p|<m'`, hence

```text
t_p <= n'-m'+1=981105.
```

Since `|J_B|>=10`,

```text
sum_p |P_p| <= 2097152-10,
45153 g <= 981105*(2097152-10)=2057516501910,
g <= floor(2057516501910/45153)=45567658.            (4.3)
```

This is the base-field-normalized split-pencil census inside one fixed
cell.  No field-size factor is introduced: the ledger counts realized
finite slopes, owner-line incidences, and evaluation coordinates.

The public source node printed the valid but weaker ceiling `45567659`.
Equation (4.2) has an integer left side `45153*g`, so its sharp consequence
uses the floor, not the ceiling.  The manifest retains both numbers and the
replayers enforce this one-unit rounding repair.

## 5. Pair-core plane dichotomy

Lift one fixed residual rank-nine owner plane back to the original row.  Let
`J` be the coordinates where every owner in the plane equals the received
pair, put `j=|J|>=10`, and write `P_p=C_p minus J` for the pair-core petal of
owner `p`.  The petals are pairwise disjoint.  If two record lines meet at
`p`, their size-`1116048` supports intersect in at least

```text
2*1116048-2097152=134944
```

coordinates.  The two distinct slope equations recover both received
columns there, so this intersection lies in `C_p`.

In the low-common-core branch `j<=134943`, put

```text
D=2097152-1116048=981104,
x=1116048-|C_p|,  y=t_p-1.
```

Fixed-owner exception disjointness gives `yx<=D`.  Therefore

```text
D+1-x-y=(D-yx)+(y-1)(x-1)>=0,
|P_p|>=t_p-1,  and  t_p<=D+1.
```

Doubling the line-design identity and summing over the disjoint petals gives

```text
g(g-1)=sum_p t_p(t_p-1)
      <=981105*sum_p |P_p|
      <=981105*(2097152-10)
       =2057516501910.
```

Exact integer comparison yields `g<=1434405`; the next integer exceeds the
resource by `2636520`.  Hence every larger plane has `j>=134944`, a pair core
shared by all owners and records in that plane.  This theorem is plane-local:
it neither counts different planes nor pays the large shared-core branch.

## 6. Nine-subset concentration and fixed-target routing

Choose the heavier of the affine-owner and rank-deficient component lanes.
It carries at least `495405467/10^9` of all record/eleven-subset incidences.
Mark all `55=C(11,9)` nine-subsets of every such eleven-subset.  One fixed
`(record,B)` pair is marked at most `C(m'-9,2)` times, and

```text
55*C(m',11)=C(m',9)*C(m'-9,2).
```

Averaging over domain nine-subsets therefore gives one fixed `B` carrying
at least

```text
ceil((495405467/10^9)*274980728111260126
     *C(m',9)/C(n',9))
>=2578110
```

distinct records in that same lane.  The endpoint is `K'=10`, because all
nine factors in `C(m',9)/C(n',9)` increase with `K'`.

In the kernel lane, every retained rank-deficient eleven-subset has kernel
inside the same nonzero `ker(ev_B)`.  In the affine-owner lane, a rank-ten
eleven-subset restricts to rank eight or nine on `B`.  At rank nine, the
nine-cell ordered-pair resource is

```text
981105*(2097152-9)=2057517483015,
```

whose integer plane cap remains `1434405`.  Since `2578110` exceeds that
cap by `1143705`, the lifted plane shares at least `134944` received
coordinate pairs.  At rank eight, with `U=ker(ev_B)` of dimension two, all
selected owners lie in one affine `U^2` flat.  Writing

```text
h_gamma=A_*+gamma B_*+v_gamma,  v_gamma in U,
```

shows that anchored error differences lie in `span(U,r_1-B_*)`, of
dimension at most three.  These are fixed populated targets, not aggregate
payments.

## 7. Exact impact on the open route

The packet supplies eight route cuts.

1. High-core absorption has exactly dimension ten, not a range `2,...,10`.
2. More than 99 percent of record/eleven-subset incidences enter an affine
   owner or kernel component.
3. More than half of records have a 98-percent star and enter a large-owner,
   rank-nine pencil, or kernel-plane target.
4. One fixed rank-nine pencil cell carries at most `45567658` records.
5. One lifted rank-nine plane either carries at most `1434405` records or
   has a shared pair core of size at least `134944`.
6. One typed component lane has a fixed nine-subset carrying at least
   `2578110` distinct records.
7. The rank-nine plane cap remains `1434405` for that nine-coordinate chart.
8. The fixed chart is a kernel target, a shared-core rank-nine plane, or a
   rank-eight owner flat with selected error rank at most three.

It does not select the complete component lane, recursively cover its
remainder, construct a chronology-correct owner satisfying PR #1169, or pay
the fixed kernel, shared-core, and rank-eight targets.  Therefore `U_BC`,
`U_new`, error rank eleven, and the KoalaBear row remain open.

## 8. Provenance and replay

The manifest pins the eight public source nodes by commit, Git tree, and
source-contract SHA-256.  The primary verifier recomputes all displayed
integer endpoints and a finite-field dense-root saturation model.  The
independent verifier uses a separate rational-product calculation and an
exhaustive check of all `981104` admissible owner-core sizes, the independent
nine-subset product endpoint, and finite affine-plane/rank-three models.

```text
python3 experimental/scripts/verify_kb_mca_rank11_dense_locator_split_pencil_v1.py
python3 experimental/scripts/verify_kb_mca_rank11_dense_locator_split_pencil_v1.py --tamper-selftest
python3 experimental/scripts/verify_kb_mca_rank11_dense_locator_split_pencil_v1_independent.py
```

No deployed v4 atom moves, and neither prize problem is closed.
