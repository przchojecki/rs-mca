---
workboard_item: K3/K4
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: In the pinned post-near rank-eleven anchor-star setup, dense-locator normalization forces at least 990810934 parts per billion of record/eleven-subset incidences onto positive-dimensional owner or kernel components; at least 540546700 parts per billion of records have a 98-percent component star; the full-rank star owner of deficiency at most 22320 is unique for its record; every rank-nine star is a split-pencil cell carrying at most 45567658 records; every lifted rank-nine plane either carries at most 1434405 records or shares a 134944-coordinate pair core; one fixed nine-subset carries at least 2578110 records and 5868470021012020 marked component extensions at the shortest endpoint; retaining that weight eliminates the rank-nine fixed target uniformly; multistep rank-raising counts and target-coloop multiplicities give all 28 inequalities coupling kernel corank d to d-t for 2<=t<d<=9; projective-normal pair counting lowers the complete shortened corank-one record cap to 8147918 and sharpens exact kernel-lane exclusion through K'=377673; owner-pair capacity excludes rank eight for every 37996<=K'<=1048576; and every surviving rank-eight chart on 22526<=K'<=37995 contains a delta<=4 owner with at least 200632 records.
architecture: POST_NEAR_ERROR_RANK11_DENSE_LOCATOR_COMPONENT_ROUTE_V1
partition_digest: inherited post-near rank-eleven route of PRs 1168 and 1169; no new first-match atom or partition digest
atom_or_cell: rank-eleven dense-locator component family, one fixed rank-nine split-pencil cell, its lifted owner plane, and one fixed nine-coordinate component chart
quantifier: Every survivor satisfying the pinned rank-eleven 32-anchor, 18-dense-root, ten-dimensional correction-space setup, uniformly for 10<=K'<=1048576
projection_and_unit: Distinct bad finite slopes per received line at record level; record/coordinate-subset incidences only where explicitly stated
claimed_bound: isolated equivalent <=2526815879272440; component incidence >=990810934 ppb; 98-percent records >=148639925144138894; one fixed rank-nine cell <=45567658 records; low-common-core rank-nine plane <=1434405 records; one typed fixed nine-subset >=2578110 and weighted endpoint >=5868470021012020; rank-nine weighted boundary demand 6849288576200976639 exceeds cap 147748596828055575; the one-shadow kernel LP closes through K'=15445; full containment closes through K'=15670; the rank-eight extension deficit C(67474,2)=2276336601 sharpens the cutoff to K'=17608; the seven two-step inequalities sharpen it to K'=18101; all 28 multistep inequalities sharpen it to K'=18158; the corank-one projective-pair cap 8147918 sharpens it to K'=377673 by endpoint gap 608290099077401798561583762592584078050381528604243813748500153228; rank-eight demand first exceeds owner-pair capacity at K'=37996 by 36370688210984; dense-owner averaging first forces 200632 records at K'=22526
status: PROVED LOCAL THEOREM PACKET / GLOBAL ROW OPEN
impact: ROUTE_CUT / BASE-FIELD-NORMALIZED SPLIT-PENCIL AND FIXED-CHART LEDGER
falsifier: A proper eleven-coordinate intersection with isolated multiplicity above 198; a record-star violating the rank trichotomy; a fixed rank-nine cell with more than 45567658 assigned records; a lifted plane above 1434405 records whose shared pair core has size below 134944; failure of the marked 5868470021012020 endpoint; a rank-nine chart exceeding 981105*(m'-10)*n' marked extensions; a kernel chart violating M_d*C(K'-10,d+1); a loopless corank-d eleven-set with fewer than C(d+2,t) spanning (11-t)-subsets for some 2<=t<d; one such shadow with more than C(K'-d-11+t,t) same-rank extensions; one record violating either nine-shadow resource; fewer than C(67472+d,t) rank-raising support t-sets; a rank-(10-d+t) target with more than C(9-d+t,t) source shadows; a complete shortened corank-one record with fewer than 134944 ordered independent coordinate pairs; more than 8147918 such records; a hierarchy capacity crossing before K'=377674; a rank-eight chart exceeding 981105*C(n'-9,2); failure of either owner-capacity crossing; failure of the 22526 dense-owner bridge; or a defect in the 4070408-slope fence.
replay: python3 experimental/scripts/verify_kb_mca_rank11_dense_locator_split_pencil_v1.py; python3 experimental/scripts/verify_kb_mca_rank11_dense_locator_split_pencil_v1.py --tamper-selftest; python3 experimental/scripts/verify_kb_mca_rank11_dense_locator_split_pencil_v1_independent.py
---

# KoalaBear rank-eleven dense-locator and split-pencil route

Status: **PROVED LOCAL THEOREM PACKET / ZERO DEPLOYED LEDGER MOVEMENT**.

Exact parent: PR #1169 head
`b4bad860750f91955dbaead8f2b5a0fdef1f1343`.

This packet imports thirty-four public, commit- and tree-pinned prize-DAG theorems.
They begin after the rank-eleven branch has produced one fixed degree-31
anchor interpolant, eighteen dense-pair roots, and a ten-dimensional
relative correction space.  They end with an exact ledger for one fixed
rank-nine ten-coordinate cell, a low-core/large-shared-core dichotomy for
its lifted owner plane, and one overlap-correct fixed nine-coordinate target.
They do not select the complete component lane or assign chronology across
different targets.  A final local-cap fence shows why that missing coupling
cannot be replaced by another deduplicated-record inequality on the fixed
chart alone. Retaining the marked component-extension weight does eliminate
the rank-nine fixed target. Canonical rank-basis capacities and two coupled
nine-shadow resources and the corank-one projective-pair cap then remove the
dominant kernel lane through residual dimension `377673`. Owner-pair
capacity removes rank eight from `K'=37996` through the deployed endpoint.
On the upper surviving interval, marked averaging reaches the exact dense
owner chronology terminal guarded by PR #1169.

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

### Record-intrinsic full-rank owner

The full-rank owner above is independent of the ten-subset used to expose
it.  If two distinct owner pairs for the same record both had deficiency at
most `22320`, their within-support cores would intersect in at least

```text
m'-2*22320=K'+22832
```

coordinates.  At least one component of their difference is a nonzero RS
polynomial of degree below `K'`, so the intersection has size at most
`K'-1`.  The contradiction gap is `22833`, uniformly over shortening.
This yields one intrinsic owner key for weighted aggregation, not a count of
owners across records or a deployed chronology.

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

## 7. Fixed-chart local-cap fence

The rank-nine target, considered without the weighted multiplicities of its
ancestor incidence census, is not locally contradictory.  On the official
row take a nonzero RS word `u` with exactly `K-1` evaluation roots `J`.  The
outside coordinate and rich-support weights are

```text
N=n-(K-1)=1048577,       L=m-(K-1)=67473.
```

Give eight owner points weight `L-1=67472`, and give each of the remaining
`508801` coordinates its own unit owner point.  Place the heavy points at
`P_i=(c+iM,0)` and the unit points at `Q_j=(j,1)`, where `M=508801`.  The
lines through `P_i,Q_j` have distinct parameters

```text
gamma_(i,j)=c+iM-j,
```

because their eight difference intervals are consecutive and disjoint.
There are

```text
8M=4070408>2578110
```

such lines.  With received columns

```text
r_0(x)=alpha_x u(x),       r_1(x)=beta_x u(x),
```

the line `alpha+gamma beta=c+iM` uses the codeword `(c+iM)u` and has exact
support `J`, one heavy fibre, and one unit fibre, hence size `m`.  A
containing polynomial pair would have its second component equal to zero on
the `m-1>K-1` coordinates in `J` and the heavy fibre, but equal to nonzero
`u` at the unit fibre.  The RS root bound forbids this.  Two heavy-fibre
coordinates adjoined to the fixed nine roots give the required rank-ten
eleven-subset and fixed-owner component.  Error differences lie in
`span(r_1,u)`.

The KoalaBear base prime exceeds `18*4070408`, so a common translation avoids
the eighteen dense slopes.  This still does not construct the fixed
32-anchor/18-root ancestor packet or an unsafe line.  It proves only that
the target output in isolation admits more than the selector floor.  The
next theorem must retain pre-deduplication component weights, couple charts,
or use a specific dense-anchor identity that excludes this model.

## 8. Weighted elimination of the rank-nine fixed target

Before dividing by `C(m'-9,2)`, the same marking argument gives one fixed
`B` with marked component-extension weight

```text
W_B >=ceil((495405467/10^9)*274980728111260126
           *C(m',9)*C(m'-9,2)/C(n',9)).
```

At `K'=10` this is `5868470021012020`. In a rank-nine chart, every rank-ten
extension containing `B` determines one owner point and uses at least one
coordinate in that point's petal. One point owns at most `981105` records,
its core has size below `m'`, and plane petals are disjoint. Thus, in the
same `(record,T)` unit,

```text
W_B <=981105*(m'-10)*n'.
```

The distinct `2578110`-record target already forces a common plane core of
size at least `134944`. For `K'<=67472`, that core cannot fit strictly below
`m'`. For `K'>=67473`, exact boundary arithmetic gives

```text
6849288576200976639 > 147748596828055575,
gap = 6701539979372921064.
```

After cancellation, the demand/cap ratio is a constant times
`C(m',9)/C(n',9)*(m'-9)/n'`; every factor increases with `K'`. Hence the
rank-nine alternative is empty on the whole shortening interval. The fixed
kernel chart and rank-eight owner flat remain open.

The `4070408`-slope model remains a valid fence against deduplicated record
counting. It does not carry the marked extension weight and is not a
counterexample to this weighted elimination.

## 9. Canonical kernel bases and the finite capacity cut

For a rank-deficient component eleven-subset `T`, put

```text
r=rank(ev_T),  d=10-r,
```

and choose one canonical rank basis `B subset T`, `|B|=r`. All records
assigned to the same `B` share one quotient solution. After one affine
translation and exact cancellation of `B`, they lie in a single rank-`d`
explanation family. The remaining `d+1` coordinates of `T` are common zeros
of its kernel space. Generalized MDS leaves only `K'-10` additional common
zeros, so one basis carries at most

```text
M_d(K')*C(K'-10,d+1)
```

incidences. Assigning each tuple to one canonical basis makes these caps
summable. With `M_9=61871313426630599`, the complete capacity is

```text
Cap(K')=sum_(d=1)^9 C(n',10-d) M_d(K') C(K'-10,d+1).
```

Exact replay proves `Cap(K')` is below the dominant kernel-lane demand for
all `10<=K'<=4598`. At the final closed row the integer gap is

```text
219272330501201744129177266158988707697316238048878827197685.
```

At `K'=4599` capacity exceeds demand by
`95457494746881463288875361950515757435711627164872173764503`, so the
canonical-assignment estimate stops there.

The canonical tie-break discards guaranteed basis multiplicity. The
evaluation matroid on `T` is loopless because the residual correction space
has empty global common zero set. Starting from any rank-`(10-d)` basis,
fundamental-circuit exchange supplies one distinct new basis for each of
the `d+1` outside elements. Thus every `(record,T)` incidence has at least
`d+2` basis decorations. The fixed-basis argument applies to every
decoration, so the refined capacity is

```text
Cap_multi(K')=sum_(d=1)^9 floor(
  C(n',10-d) M_d(K') C(K'-10,d+1)/(d+2)).
```

Exact replay proves `Cap_multi(K')` is below demand for all
`10<=K'<=11641`. The endpoint gap is

```text
17769453550459149385453824948016076737082337523706893862084.
```

At `K'=11642`, capacity exceeds demand by
`187031323586740190878769118921060658362307444191332937452616`, so the
refined method stops honestly. The factor `d+2` is sharp from looplessness
alone, using `9-d` coloops and one parallel class of size `d+2`.

There is a second summation order. For one record with exact support `S`,
`|S|=m'`, count bases only inside `S`. The same decoration and common-zero
argument gives the per-record capacity

```text
P_d(K')=floor(C(m',10-d) C(K'-10,d+1)/(d+2)).
```

If `R_actual>=N_min` is the actual residual record count, each stratum is
bounded by both the ambient capacity `A_d` and `R_actual*P_d`. After
division by `R_actual`, their minimum is nonincreasing in the record count,
so the worst case occurs at `N_min`. Exact replay of

```text
sum_d min(A_d,N_min*P_d)
```

closes every row through `K'=11772`. The endpoint gap is
`76504076505592948633027913576880724493595282142849410185084`; at
`K'=11773`, capacity exceeds demand by
`139343682529231472322825521514042608524569163680782450618944`.
The boundary branch pattern is `AARRRRRRR`.

The nine rank strata cannot saturate independently.  For one exact support
`S`, let `I_d(S)` count corank-`d` eleven-subsets and let `J_d(S)` count
rank-`(10-d)` nine-subsets.  A loopless rank-`(10-d)` matroid on eleven
elements has at least `C(d+2,2)` spanning nine-subsets: in the dual this is
the minimum number of independent pairs in a coloopless rank-`(d+1)`
matroid.  One fixed spanning nine-subset has at most
`C(K'-d-9,2)` same-rank extensions, since its closure is the common-zero
set of a `d`-dimensional polynomial space and has size at most `K'-d`.
Therefore

```text
sum_(d=1)^9 C(d+2,2) I_d(S)/C(K'-d-9,2) <= C(m',9).       (9.1)
```

After normalization by the unknown record count and intersection with the
individual ambient/record caps, (9.1) is a fractional-knapsack problem.
Exact rational replay closes all `15436` rows `10<=K'<=15445`.  At the
endpoint the scaled demand exceeds capacity by

```text
178044655461817065880792270525721984196903835342334290540589.
```

At `K'=15446` capacity exceeds demand by
`124087038578417364551353992932097013573495323735890481286577`.
Only corank one is filled and corank two partially filled at both boundary
rows.

A second count retains all `C(11,9)=55` contained nine-subsets, not only
the rank-preserving ones.  Let `J_1` count rank-nine nine-subsets and put

```text
E_0=C(m'-9,2),    E_1=C(K'-10,2),    I=sum_d I_d.
```

A rank-nine nine-subset extends to at most `E_1` kernel eleven-sets, while
every lower-rank nine-subset has at most `E_0` support-pair extensions.
Thus

```text
55 I <= E_1 J_1+E_0(C(m',9)-J_1).
```

The corank-one case of (9.1) gives `3I_1<=E_1J_1`.  Since `E_0>E_1`,
substitution yields the independent full-containment resource

```text
[52+3E_0/E_1] I_1+55 sum_(d=2)^9 I_d <= E_0 C(m',9).     (9.2)
```

Optimizing (9.1) and (9.2) together closes all `15661` rows
`10<=K'<=15670`.  At `K'=15670` the scaled demand and floored capacity are

```text
4475537178738548139330981218648452557243318003039175890361321166,
4475476933994360491615442893294277488243572130730662704491466634,
```

leaving gap
`60244744187647715538325354175068999745872308513185869854532`.
At `K'=15671` capacity exceeds demand by
`291105561463347587484268984669020036510369238771859813045635`.
At both rows only coranks one and two are positive and both resource
inequalities bind; the individual caps are slack.  An independent replay
uses nonnegative dual multipliers for (9.1) and (9.2), rather than the
primary primal optimizer.

## 10. Rank-eight nine-shadow extension deficit

Fix a rank-eight nine-subset `U` of an exact support `S`.  Write
`C=cl_S(U)`, `c=|C|`, and `X=S\C`.  Generalized MDS closure caps give
`c<=K'-2`, hence `q=|X|>=67474`.  Contracting by `U` leaves rank two.
Every parallel class in `X` has size at most `K'-1-c`: adjoining one such
class to `C` is a rank-nine flat.  Therefore every point of `X` has at least

```text
q-(K'-1-c)=m'-K'+1=67473
```

partners outside its parallel class.  Dividing the ordered count by two
shows that at least

```text
L_2=C(67474,2)=2276336601
```

support pairs raise rank eight to rank ten.  Thus the corank-two coefficient
in (9.2) improves from `55` to

```text
55+6L_2/C(K'-11,2).                                      (10.1)
```

The exact two-resource LP using (9.1), (9.2), and (10.1) closes all `17599`
rows `10<=K'<=17608`.  At `K'=17608`, demand exceeds floored capacity by

```text
126547040539829546354916747965612889135249249684319416999204.
```

At `K'=17609`, capacity exceeds demand by

```text
165662859003771823867021831078593815988062146919602894849014.
```

At both rows coranks one and three are capped, coranks two and four are
resource-tight, coranks five through nine vanish, and both shared resources
bind.  The primary replay enumerates every nonnegative dual vertex.  The
independent replay reconstructs the primal optimizer from a fifteen-interval
active-set ledger and checks strong duality row by row.

## 11. Two-step nine-shadow hierarchy

Let `I_d(S)` count rank-`(10-d)` eleven-subsets of one exact support and let
`J_d(S)` count rank-`(10-d)` nine-subsets.  For `3<=d<=9`, put

```text
s_d=C(d+2,2),       L_d=C(67472+d,2),
E_d=C(K'-d-9,2),    Q_d=C(11-d,2).
```

The shared-shadow theorem gives `s_d I_d<=E_d J_d`.  Fix a nine-shadow `U`
counted by `J_d`.  Its closure has size at most `K'-d`, so at least
`67472+d` support points lie outside.  In the contraction by `U`, every
parallel class has size at most `K'-d+1-|cl_S(U)|`.  Each outside point
therefore has at least `67471+d` partners in other classes, and at least
`L_d` unordered pairs raise rank by two.

A rank-`(12-d)` target eleven-set contains at most `Q_d` source shadows.
Indeed, the complementary pair must consist of two coloops by the dual-rank
identity.  The target matroid is loopless and has rank `12-d`, so it has at
most `11-d` coloops.  Double counting the rank-raising pairs gives the seven
inequalities

```text
(s_d L_d/E_d) I_d <= Q_d I_(d-2),       3<=d<=9.       (11.1)
```

The exact constants are

```text
d     s_d       L_d          Q_d
3      10    2276404075       28
4      15    2276471550       21
5      21    2276539026       15
6      28    2276606503       10
7      36    2276673981        6
8      45    2276741460        3
9      55    2276808940        1
```

Adding (11.1) to the preceding full-containment resource and the individual
caps closes every row through `K'=18101`.  On all `494` newly replayed rows
`17609<=K'<=18102`, the corank-one cap, full containment, and all seven
hierarchy inequalities bind; all nine coranks are positive; every other
individual cap and the rank-preserving shared-shadow resource are slack.
At `K'=18101`, demand exceeds floored capacity by

```text
33462159928103132226516704640419847248244116666500998762314.
```

At `K'=18102`, capacity exceeds demand by

```text
275016496133605602641019628236447268989861205055439981187167.
```

The primary replay reconstructs the odd and even primal chains and solves
the nine rational complementary-slackness equations by Gaussian
elimination.  The independent replay derives the seven hierarchy dual
multipliers by backward odd/even recurrences, then checks primal feasibility
and strong duality on every row.

## 12. Multistep shadow hierarchy

The pair argument extends to every admissible step. For `2<=t<d<=9`, let
`J_(d,t)(S)` count rank-`(10-d)` subsets of size `11-t` and put

```text
s_(d,t)=C(d+2,t),                 L_(d,t)=C(67472+d,t),
E_(d,t)=C(K'-d-11+t,t),          Q_(d,t)=C(9-d+t,t).
```

Then

```text
(s_(d,t)L_(d,t)/E_(d,t)) I_d <= Q_(d,t) I_(d-t).     (12.1)
```

For the source eleven-set, the dual evaluation matroid is coloopless of
rank `d+1`. If `f_j` is its number of independent `j`-sets, every
independent `j`-set has at least `d+2-j` one-point extensions: otherwise
the `d+1-j` points needed outside its closure would occur in every basis,
creating a coloop. Hence
`(j+1)f_(j+1)>=(d+2-j)f_j`, and iteration from `f_0=1` gives
`f_t>=C(d+2,t)`. These complements are the spanning `(11-t)`-shadows.
Any fixed shadow has at most `E_(d,t)` same-rank source extensions.

Starting from such a shadow, add independent support points successively.
At stage `j`, its closure has size at most `K'-d+j`, leaving at least
`67472+d-j` choices. Division by `t!` gives at least `L_(d,t)` unordered
rank-raising `t`-sets. Conversely, for a target eleven-set of rank
`10-d+t`, the complementary `t`-set must consist of coloops. A loopless
rank-`(10-d+t)` matroid on eleven points has at most `9-d+t` coloops, so a
target has at most `Q_(d,t)` source shadows. The two double counts prove
(12.1). There are exactly 28 rows; `t=2` recovers (11.1).

The exact all-step LP is certified by the seven-edge tree

```text
(t,d)=(2,3),(2,4),(2,6),(2,8),(3,5),(2,7),(2,9).
```

The corank-one cap and full-containment resource bind, all nine coranks are
positive, and the rank-preserving nine-shadow resource and all other caps
are slack. Seventeen of the 28 hierarchy rows bind; ten rows outside the
tree are checked as exact cycle identities. This closes all 57 new rows
`18102<=K'<=18158`. At `K'=18158`, demand exceeds floored capacity by

```text
289110608820324799941118306538399899258195112067661304310498.
```

At `K'=18159`, capacity exceeds demand by

```text
20286290696334777989469267474876769475675508046109372076445.
```

The primary replay solves the nine exact complementary-slackness equations
by Gaussian elimination. The independent replay reconstructs the primal
and dual by forward and backward tree recurrences and checks all 28
inequalities on every replayed row.

## 13. Corank-one projective-pair cap

After canonical rank-nine basis cancellation, the complete shortened
corank-one chart has

```text
(n,K,m,s)=(1048577,1,67473,1).
```

Agreement normals lie in a two-dimensional space. The common-zero bound
gives `z<=K-s=0`, and same-support pair noncontainment forces the `m`
incident normals of every selected record to span. If their nonempty
projective-class sizes are `a_1,...,a_c`, then `c>=2` and

```text
m^2-sum_i a_i^2 >= m^2-((m-1)^2+1)=2(m-1)=134944.
```

Every ordered independent coordinate pair determines at most one parameter
point. Therefore

```text
M_1<=floor(1048577*1048576/134944)=8147918,
```

with remainder `29760`. This improves the generic support-local cap
`16295594` by `8147676`.

Substituting the new cap into the all-step hierarchy LP gives two active
roots, coranks one and two. The seven tree edges are

```text
(t,d)=(2,3),(3,4),(2,5),(2,6),(2,7),(2,8),(2,9).
```

Both shared resources and every nonroot individual cap are slack; all nine
coranks are positive; 22 hierarchy rows bind. Positive backward-tree dual
prices prove exact optimality. The source-pinned 64-worker replay checks all
`359516` rows through the adjacent wall. At `K'=377673`, demand exceeds
floored capacity by

```text
608290099077401798561583762592584078050381528604243813748500153228.
```

At `K'=377674`, capacity exceeds demand by

```text
1089804128361045148874283346879615159892995682385275039289561845323.
```

The packet verifiers independently reconstruct the projective partition
extremum and the replay start, endpoint, and adjacent wall by direct path
products.

## 14. Rank-eight owner-pair capacity

Fix a rank-eight nine-set `B` and put `U=ker(ev_B)`, `dim U=2`. For a
full-rank extension `T=B union {x,y}`, evaluation on `{x,y}` is invertible
on `U`. The coordinate pair therefore determines at most one owner point in
the affine `U^2` flat. Since one fixed owner owns at most `981105` records,

```text
W_B<=981105*C(n'-9,2).
```

This is in the selector's exact marked `(record,T)` unit. At `K'=37995`,
the cap still exceeds demand by `18174297527234`. At `K'=37996`, demand
exceeds the cap by `36370688210984`. The identity

```text
C(n',9)C(n'-9,2)=55C(n',11)
```

reduces the unrounded demand/cap ratio to a constant times
`C(m',11)/C(n',11)`. All eleven factors increase, so rank eight is excluded
for every `37996<=K'<=1048576`.

The same marked decomposition gives more before that wall. If `q_p` counts
coordinate pairs determining owner `p` and `t_p` its records, then
`W_B<=sum_p t_p q_p` and `sum_p q_p<=C(n'-9,2)`. At `K'=22526`,

```text
W_B-200631*C(n'-9,2)=11714977255865.
```

Thus one owner has at least `200632` records. An owner of core deficiency
at least five has at most `1+floor(981104/5)=196221` records, so this owner
has deficiency at most four. The same monotone ratio propagates the bridge
through `K'=37995`; at `K'=22525` the comparison still misses by
`1170919108090`. This reaches the #1169 chronology terminal but does not
assign chronology or coalesce owners.

## 15. Exact impact on the open route

The packet supplies thirty-four route cuts.

1. High-core absorption has exactly dimension ten, not a range `2,...,10`.
2. More than 99 percent of record/eleven-subset incidences enter an affine
   owner or kernel component.
3. More than half of records have a 98-percent star and enter a large-owner,
   rank-nine pencil, or kernel-plane target.
4. Every full-rank large owner below deficiency `22320` is unique for its
   record and independent of the exposing ten-subset.
5. One fixed rank-nine pencil cell carries at most `45567658` records.
6. One lifted rank-nine plane either carries at most `1434405` records or
   has a shared pair core of size at least `134944`.
7. One typed component lane has a fixed nine-subset carrying at least
   `2578110` distinct records.
8. The rank-nine plane cap remains `1434405` for that nine-coordinate chart.
9. The fixed chart is a kernel target, a shared-core rank-nine plane, or a
   rank-eight owner flat with selected error rank at most three.
10. The rank-nine target output alone admits `4070408` exact-support slopes;
   therefore its local hypotheses do not pay the `2578110` selector floor.
11. The fixed selector retains at least `5868470021012020` marked component
    extensions even at the shortest endpoint.
12. Every fixed rank-nine chart has marked load at most
    `981105*(m'-10)*n'`.
13. The rank-nine fixed target is empty uniformly; only the fixed-kernel and
    rank-eight owner-flat alternatives remain.
14. Every fixed kernel rank-basis chart has exact capacity
    `M_d*C(K'-10,d+1)`.
15. Summed kernel capacity excludes dominant kernel lanes for
    `10<=K'<=4598`; `K'=4599` is the first method wall.
16. Every corank-`d` kernel incidence has at least `d+2` basis decorations,
    and the fixed-basis cap remains valid for all decorations.
17. The refined multi-basis capacity excludes dominant kernel lanes for
    `10<=K'<=11641`; `K'=11642` is the first refined method wall.
18. One exact support has per-record corank-`d` capacity
    `floor(C(m',10-d)C(K'-10,d+1)/(d+2))`.
19. Taking the per-corank minimum of ambient and record-support capacities
    excludes dominant kernel lanes through `K'=11772`; `K'=11773` is the
    first hybrid wall.
20. The spanning nine-shadows of all coranks share the single resource
    (9.1), with coefficient `C(d+2,2)/C(K'-d-9,2)` in corank `d`.
21. The one-shadow fractional-knapsack capacity excludes dominant kernel
    lanes through `K'=15445`; `K'=15446` is its exact method wall.
22. Counting all 55 contained nine-subsets gives the independent
    full-containment resource (9.2).
23. The resulting exact two-resource LP excludes dominant kernel lanes
    through `K'=15670`; `K'=15671` is its exact method wall.
24. Every rank-eight nine-shadow loses at least `C(67474,2)` support-pair
    extensions from the unrestricted kernel-extension cap.
25. The sharpened exact two-resource LP excludes dominant kernel lanes
    through `K'=17608`; `K'=17609` is its exact method wall.
26. A rank-eight fixed chart has marked owner-pair capacity
    `981105*C(n'-9,2)`.
27. Rank eight is impossible for `37996<=K'<=1048576`; `K'=37995` is the
    final failed row for this method.
28. Every surviving rank-eight chart on `22526<=K'<=37995` contains a
    `delta<=4` owner with at least `200632` records, reaching the guarded
    chronology terminal without closing it.
29. Rank-raising pairs and loopless target-coloop multiplicities give the
    seven two-step inequalities (11.1), coupling every corank `d>=3` to
    corank `d-2`.
30. The hierarchy-saturated exact LP excludes dominant kernel lanes through
    `K'=18101`; `K'=18102` is its exact method wall.
31. Every `2<=t<d<=9` gives the multistep shadow inequality (12.1), for 28
    exact couplings in total.
32. The all-step hierarchy LP excludes dominant kernel lanes through
    `K'=18158`; `K'=18159` is its exact method wall.
33. In the complete shortened corank-one chart, projective-normal pairs
    lower the exact record cap from `16295594` to `8147918`.
34. The resulting two-root hierarchy LP excludes dominant kernel lanes
    through `K'=377673`; `K'=377674` is its exact method wall.

It does not select the complete component lane, recursively cover its
remainder, construct a chronology-correct owner satisfying PR #1169, or pay
the fixed kernel above `K'=377673`, rank-eight targets below `K'=22526`, or
the dense-owner chronology terminal on `22526..37995`.
Therefore `U_BC`,
`U_new`, error rank eleven, and the KoalaBear row remain open.

The exact unresolved intervals are:

```text
10..22525:        rank eight only,
22526..37995:     dense-owner chronology terminal only,
37996..377673:    no rank-eleven component target,
377674..1048576:  kernel only.
```

## 16. Provenance and replay

The manifest pins the thirty-four public source nodes by commit, Git tree, and
source-contract SHA-256.  The primary verifier recomputes all displayed
integer endpoints and a finite-field dense-root saturation model.  The
independent verifier uses a separate rational-product calculation and an
exhaustive check of all `981104` admissible owner-core sizes, the independent
nine-subset product endpoint, all `11763` hybrid rows, all `15436`
one-shadow rows, all `15661` full-containment rows, all `17599`
rank-eight-deficit rows, all `494` two-step boundary rows, all `58`
all-step boundary rows, the projective partition extremum, three exact
projective-capacity boundary rows, and all `11`
rank-eight monotonicity factors, together with finite
affine-plane/rank-three models and the two dense-owner bridge boundary rows.

```text
python3 experimental/scripts/verify_kb_mca_rank11_dense_locator_split_pencil_v1.py
python3 experimental/scripts/verify_kb_mca_rank11_dense_locator_split_pencil_v1.py --tamper-selftest
python3 experimental/scripts/verify_kb_mca_rank11_dense_locator_split_pencil_v1_independent.py
```

No deployed v4 atom moves, and neither prize problem is closed.
