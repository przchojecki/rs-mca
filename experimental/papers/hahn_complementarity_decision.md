# Adjacent fixed-`G` interiors: exact Hahn complementarity decides the selected-support gap

**Status:** CERTIFIED STOP / EXACT EQUIVALENCE / NEW COMPLEMENTARITY REDUCTION

## Request worked from

Determine what decides the selected-support gap at the adjacent symmetric interior rows of the Mersenne-31 fixed-`G` ordinary boundary family.

## Abstract

No adjacent interior row is paid unconditionally here. The exact result is a
structural correction to the predecessor's interface.

For every valid exact-size selected-support realization at either adjacent row,
let

```text
E_Hahn = c1 G_1 + c2 G_2 + c3 G_3
```

and let `S_shell` be the nonnegative slack contributed by the negative values of
the frozen cubic dual away from its three integer root shells. Then the dual
argument has the exact complementarity identity

```text
H = L + E_Hahn + S_shell.                            (A)
```

More explicitly, with

```text
alpha = 118055716980403503 / 1924657059987219425146540,
```

and selected-support exchange distances `e_ij`,

```text
S_shell
  = (alpha/L) sum_{i != j}
      (e_ij-67448)(e_ij-70799)(e_ij-70800) >= 0.     (B)
```

Equivalently, if `t_ij` is the selected-support intersection size,

```text
S_shell
  = (alpha/L) sum_{i != j}
      (5412-t_ij)(2061-t_ij)(2060-t_ij).             (C)
```

At the first forbidden cardinality `L=B*=16777215`, equation (A) becomes the
conservation law

```text
Delta_open = E_Hahn + S_shell.                       (D)
```

Thus support choice cannot change the total open gap. It only transfers that
fixed amount between low-Hahn spectral energy and three-shell distance slack.

The predecessor's named condition `RS_HAHN123_SELECTION_GAP` asks for a valid
selection with `H-E_Hahn<L`. By (A), this is exactly the request
`S_shell<0`, which no valid selected family can satisfy. Consequently, under
the inherited dual factorization and the elementary existence of exact-size
support choices,

```text
RS_HAHN123_SELECTION_GAP
  if and only if
there is no adjacent ordinary list of size at least B*.
```

It is therefore not a weaker missing hypothesis: it is logically equivalent to
the desired adjacent-row list cap. An unsafe list itself is already a complete
falsifier; one need not enumerate all its support selections, because (A)
automatically shows that every selection fails the named condition.

The actual finite object left open is a coupled deletion/addition optimization
on the full agreement sets. At the low row, a target-sized hypothetical list
has average agreement surplus at most
`149030066/16777215 = 8.882884674...`; at the high row the corresponding cap is
`11955691/16777215 = 0.712614757...`. Exact random-transversal formulas reduce a
usable shell-slack certificate to the first three falling-factorial moments of
pairwise full-agreement intersections. No attached source supplies the
RS-specific inequality needed to make that certificate cross `Delta_open`.
That missing inequality, or an actual target-sized list, is the precise
obstruction.

## 1. Frozen rows and common selected-support object

The frozen parameters are

```text
p = 2147483647 = 2^31-1,
N = R = 981129,
w = 67447,
D = w+1 = 67448,
B* = 16777215,
ell = B*-1 = 16777214.
```

The adjacent symmetric rows are

```text
(d,m) = (5413,72860) and (840822,908269).
```

The ordinary object is the number `L` of distinct degree-`<d` polynomials over
`F_p` agreeing with one received word on at least `m` points of an
`N`-point boundary subset.

For the low row, choose a `72860`-point subset of each polynomial's agreement
set. For the high row, choose a `908269`-point agreement subset and complement
it. In either case one obtains an injective family

```text
S_1,...,S_L in J(981129,72860)
```

with minimum exchange distance `67448`. Put

```text
s0 = 72860,
e_ij = s0 - |S_i intersect S_j|.
```

For distinct indices, `e_ij>=67448`, or equivalently
`|S_i intersect S_j|<=5412`.

Let `A_e` be the ordered inner distribution divided by `L`; thus `A_0=1` and
`sum_e A_e=L`. Let `H_j(e)` be the normalized Johnson-scheme Hahn functions
used in the attached adjacent-Hahn certificate, and define

```text
G_j = sum_e A_e H_j(e).
```

The Johnson scheme gives `G_j>=0`.

## 2. The inherited cubic dual

The frozen degree-three dual is

```text
F(e) = 1 + c1 H_1(e) + c2 H_2(e) + c3 H_3(e),
```

where

```text
c1 = 979061542845605776592576657442
     / 21065719351149270924992461,

c2 = 2127197006408557278777618631055673
     / 1137547685530096782227047625,

c3 = 389001796223311531724035804630343856388
     / 20668103898396328436283228298625.
```

Its objective is

```text
H = 24044092640301071703360149280
    / 1159431963847722545269
  = 20737821.0968996317...,
```

and the attached exact factorization is

```text
F(e)
  = -alpha (e-67448)(e-70799)(e-70800),

alpha
  = 118055716980403503
    / 1924657059987219425146540
  > 0.                                                   (2.1)
```

There is no integer strictly between `70799` and `70800`. Hence, for every
allowed nonzero integer distance `e>=67448`,

```text
-F(e) = alpha (e-67448)(e-70799)(e-70800) >= 0.          (2.2)
```

The three zero-cost exchange-distance shells are

```text
67448, 70799, 70800,
```

corresponding to the three intersection shells

```text
5412, 2061, 2060.
```

## 3. Exact Hahn complementarity

### Theorem 3.1 — exact reserve decomposition

For every nonempty valid selected-support realization at either adjacent row,
define

```text
E_Hahn = c1 G_1 + c2 G_2 + c3 G_3,                   (3.1)
```

and

```text
S_shell = - sum_{e>0} A_e F(e).                      (3.2)
```

Then

```text
E_Hahn >= 0,
S_shell >= 0,
H = L + E_Hahn + S_shell.                            (3.3)
```

Moreover, equations (B) and (C) in the abstract hold exactly, and

```text
S_shell = 0
```

if and only if every distinct selected pair has exchange distance in
`{67448,70799,70800}`, equivalently intersection in `{5412,2061,2060}`.

**Proof.** By the definition of the inner distribution,

```text
sum_e A_e F(e)
  = sum_e A_e
    + c1 sum_e A_e H_1(e)
    + c2 sum_e A_e H_2(e)
    + c3 sum_e A_e H_3(e)
  = L + E_Hahn.                                      (3.4)
```

Splitting off the diagonal term `A_0F(0)=H` gives

```text
L + E_Hahn = H + sum_{e>0} A_eF(e) = H-S_shell.
```

This is (3.3). Nonnegativity of `E_Hahn` follows from `c_j>0` and `G_j>=0`;
nonnegativity and the zero characterization of `S_shell` follow from (2.1)--
(2.2). Replacing `e_ij` by `72860-t_ij` gives (C). □

**Direct falsifier.** A valid selected family for which exact evaluation of the
left and right sides of (3.3) differs, or an allowed integer distance for which
the cubic in (2.2) is negative.

### Corollary 3.2 — target-sized conservation

Any unsafe adjacent list contains a sublist of exactly `B*` codewords. For any
valid selected-support realization of that sublist,

```text
Delta_open = E_Hahn + S_shell,                       (3.5)
```

where

```text
Delta_open
  = H-B*
  = 4592053304955603301034903445
    / 1159431963847722545269
  = 3960606.0968996317....                           (3.6)
```

Thus every valid support choice partitions the same fixed quantity. The support
choice changes the partition, not the total.

For a fixed target-sized list, write `min S_shell` and `max S_shell` for the
extrema over all valid choices. Then

```text
max E_Hahn = Delta_open - min S_shell,
min E_Hahn = Delta_open - max S_shell.               (3.7)
```

In particular, the predecessor's requested inequality
`E_Hahn>Delta_open` is equivalent to `min S_shell<0`.

**Direct falsifier.** A target-sized selected family for which
`E_Hahn+S_shell` is not the exact rational in (3.6).

## 4. The named selected-support hypothesis is target-equivalent

Let `SAFE_adj` denote the statement that every ordinary list at either adjacent
row has `L<=ell`.

Let `RS_HAHN123_SELECTION_GAP` have exactly the predecessor's meaning: every
adjacent list with `L>=B*` admits one valid selected-support realization with

```text
H-E_Hahn < L.                                        (4.1)
```

### Theorem 4.1 — logical equivalence

Under Theorem 3.1,

```text
RS_HAHN123_SELECTION_GAP  <->  SAFE_adj.             (4.2)
```

**Proof.** If the selected-support statement holds and an oversized list
exists, choose its promised realization. Theorem 3.1 rewrites its left side as

```text
H-E_Hahn = L+S_shell >= L,
```

contradicting (4.1). Hence no oversized list exists. Conversely, if `SAFE_adj`
holds, there is no list satisfying the antecedent `L>=B*`, so the predecessor's
universally quantified implication is true vacuously. □

The direct falsifier format therefore simplifies:

> One actual adjacent list with at least `B*` codewords is already a complete
> falsifier of `RS_HAHN123_SELECTION_GAP`. The universal dual identity itself
> proves that every valid selection from that list has objective at least `L`.

No separate certification over every selection is needed.

### Corollary 4.2 — the sharp one-mode number is an unsafe-list ceiling

The predecessor's open one-mode threshold is

```text
theta_open
  = Delta_open/c3
  = 81858218311343544899896663534139630625
    / 389001796223311531724035804630343856388
  = 0.2104314661425156296....                        (4.3)
```

For every target-sized valid selected family,

```text
G_3 <= theta_open.                                   (4.4)
```

Equality in (4.4) can occur only if simultaneously

```text
G_1 = 0,
G_2 = 0,
S_shell = 0.
```

Hence equality would require all selected pair distances to lie on the three
dual root shells and the first three complementarity conditions to be tight.

This reverses the interpretation of (4.3): for a hypothetical unsafe family it
is a ceiling, not a value that a support choice can cross. The predecessor's
convenient non-strict proxy

```text
theta_closed
  = 40929119489723721648112549908683964625
    / 194500898111655765862017902315171928194
  = 0.2104315192736428...
```

is larger still, so a target-sized selected family cannot meet it either. If
that proxy is guarded only by `L>=B*`, its existential hypothesis is likewise
target-equivalent rather than an independent structural statement.

**Direct falsifier.** A target-sized valid selected family with `G_3` above
(4.3), or equality without the three stated tightness conditions.

## 5. A small exact integrality refinement

The continuous fractional optimum has `G_1=0`. A target-sized integral family
of `72860`-subsets cannot.

Let `r_x` be the number of selected supports containing coordinate `x`. The
first Hahn moment has the exact form

```text
G_1
  = N/(B* s0 (N-s0))
    sum_x (r_x-B*s0/N)^2.                            (5.1)
```

Exact division gives

```text
B* s0 mod N = 244929.
```

The least possible integer variance occurs when the coordinate multiplicities
differ by at most one, so every target-sized selected family obeys

```text
G_1 >= 200351922 / 1233618913144709
    = 0.0000001624098981....                         (5.2)
```

Consequently its third moment satisfies the strictly smaller ceiling

```text
G_3
  <= 7745382636890381786544822902247859893375
     / 36807150535206474929475326013497088586156
   = 0.2104314657414686764....                       (5.3)
```

The improvement over `theta_open` is

```text
4.0104695319... * 10^-10.                            (5.4)
```

This is exact but far too small to pay the row. Its significance is structural:
the exact fractional boundary `G_1=G_2=G_3=S_shell=0` is not realizable by a
target-sized integral support family.

**Direct falsifier.** A family of exactly `B*` subsets of size `s0` whose first
Hahn moment is below (5.2), or exact divisibility `N | B*s0`.

## 6. What the support choice actually optimizes

The exact finite object is the family of all allowed transversals through the
full agreement sets.

### 6.1 Low row: coupled deletions

For the row `(d,m)=(5413,72860)`, let the full agreement set of codeword `i` be
`A_i`, and write

```text
|A_i| = 72860 + u_i.
```

Every exact support has the form

```text
S_i = A_i \ R_i,     |R_i|=u_i.                     (6.1)
```

Thus the selected intersection is

```text
|S_i intersect S_j|
  = |A_i intersect A_j|
    - |R_i intersect A_j|
    - |R_j intersect A_i|
    + |R_i intersect R_j|.                          (6.2)
```

The shell defect is a coupled pairwise cubic energy in the deletion choices
`R_i`.

### 6.2 High row: coupled additions to error cores

For the row `(d,m)=(840822,908269)`, write again

```text
|A_i| = 908269 + u_i,
C_i = E0 \ A_i,
|C_i| = 72860-u_i.
```

After choosing an exact `908269`-point agreement subset and complementing it,
every selected support has the form

```text
S_i = C_i union P_i,
P_i subset A_i,
|P_i|=u_i.                                           (6.3)
```

The shell defect is the corresponding coupled cubic energy in the additions
`P_i`.

These are the actual selected-support optimization problems. They retain which
coordinates may be deleted or added and how one choice affects many pairs.
Scalar shortening and the ordinary pairwise inner distribution discard this
coupling.

### 6.3 Exact target-sized surplus caps

For a hypothetical list of exactly `B*` codewords, let

```text
T = sum_i |A_i|.
```

If `n_x` is the number of full agreement sets containing coordinate `x`, then

```text
T^2
  <= N sum_x n_x^2
  = N (T + sum_{i != j}|A_i intersect A_j|)
  <= N (T + B*(B*-1)(d-1)).                          (6.4)
```

Solving this integer quadratic gives the following exact maxima.

Low row:

```text
T <= 1222536914966,
T-B*72860 <= 149030066,
average u_i <= 149030066/16777215
             = 8.882884674....                       (6.5)
```

High row:

```text
T <= 15238236246526,
T-B*908269 <= 11955691,
average u_i <= 11955691/16777215
             = 0.712614757....                       (6.6)
```

In particular, a target-sized high-row counterexample would contain at least

```text
4821524
```

codewords whose full agreement set has exactly `908269` points.

These bounds do not close the row. They identify the scale of the remaining
coupled choice problem: average deletion depth below nine on the low side and
average addition depth below one on the high side.

**Direct falsifier.** A target-sized adjacent list satisfying the polynomial
root intersection bound but exceeding the corresponding integer maximum in
(6.5) or (6.6).

### 6.4 Exact random-transversal certificate

There is a support-choice certificate depending only on full agreement-set
sizes and pairwise overlaps.

For a pair `i,j`, put

```text
a_i = |A_i|,
a_j = |A_j|,
b_ij = |A_i intersect A_j|.
```

Choose independently and uniformly an exact `m`-point agreement subset from
each `A_i`. Let `U_ij` be the intersection size of the two chosen agreement
subsets. For `r=1,2,3`, using the falling factorial
`(z)_r=z(z-1)...(z-r+1)`, exact counting gives

```text
E[(U_ij)_r]
  = (b_ij)_r (m)_r^2 / ((a_i)_r (a_j)_r).            (6.7)
```

For the low row, the selected-support intersection is `t_ij=U_ij`. For the
high row it is

```text
t_ij = U_ij-835409.                                  (6.8)
```

Define

```text
Phi(t) = (5412-t)(2061-t)(2060-t).                   (6.9)
```

Because `Phi` is cubic, equations (6.7)--(6.9) determine
`E[Phi(t_ij)]` exactly from `a_i,a_j,b_ij`. Therefore

```text
E[S_shell]
  = (alpha/B*) sum_{i != j} E[Phi(t_ij)].            (6.10)
```

If the right side of (6.10) is strictly larger than `Delta_open`, then at least
one deterministic support choice has `S_shell>Delta_open`; equation (D) and
`E_Hahn>=0` give a contradiction. Hence (6.10) is a concrete sufficient
certificate for the adjacent cap.

No attached source gives a lower bound on the right side strong enough to cross
`Delta_open`. Establishing such a bound from fixed-syndrome or polynomial
compatibility, or printing a target-sized list for which it fails, is the exact
next obstruction.

**Direct falsifier.** Exact full agreement sets for which the right side of
(6.10) exceeds `Delta_open` but every deterministic valid selection has shell
defect at most `Delta_open`.

## 7. Necessary three-shell concentration of any unsafe list

For a target-sized hypothetical unsafe family, (D) and `E_Hahn>=0` imply
`S_shell<=Delta_open`. Therefore every valid selected realization obeys

```text
(1/(B*(B*-1))) sum_{i != j} Phi(t_ij)
  <= Q_star,                                         (7.1)
```

where

```text
Q_star
  = Delta_open/(alpha(B*-1))
  = 181495440148245273326617612350
    / 47158238754849128004301
  = 3848647.5521646297....                           (7.2)
```

An exact enumeration of the `5413` allowed integer intersections shows

```text
min Phi(t) = 32835100
```

when `t` is at distance at least `100` from each of
`{2060,2061,5412}`. Hence at most

```text
0.1172113851386057...
```

of the ordered distinct pairs can lie outside those three radius-`99` bands.
Equivalently, at least

```text
0.8827886148613943...
```

of all ordered distinct selected pairs must lie within distance `99` of one of
the three root intersections. This must hold for **every** valid support choice
from an unsafe target-sized list.

This is not a proof of safety, but it turns the obstruction into a rigid
selection-polytope statement: every allowed transversal must remain highly
concentrated around the dual root shells.

**Direct falsifier.** A target-sized unsafe list and one valid support selection
with a larger outside-band fraction than the bound above.

## 8. Evidence for and against

### Evidence for a structural attack

1. The shell defect is an explicit nonnegative cubic cost on selected pair
   intersections, not an unspecified spectral quantity.
2. The target-sized low and high rows have very small average support-choice
   depths, given by (6.5)--(6.6).
3. The random-transversal identity (6.10) converts the existential support
   choice into an exact statistic of the full agreement hypergraph.
4. Any unsafe list must satisfy the universal three-shell concentration in
   Section 7 for every valid selection, a much stronger requirement than one
   arbitrarily selected pairwise distribution.

### Evidence against a pairwise-only closure

The matching fractional Hahn optimum from `fixedg_adjacent_hahn_stop.md` places
all off-diagonal mass on the three zero-cost shells and has

```text
G_1=G_2=G_3=0.
```

Thus both reserves in (A) vanish at the relaxation optimum. Ordinary
Johnson-scheme positivity and the distance support constraints alone cannot
force either reserve to exceed the target gap. The target-sized integrality
floor in Section 5 excludes exact realization of the continuous optimum, but
its contribution is only `0.0075482485...`, negligible compared with
`Delta_open`.

## 9. Routes killed and certified stop

### 9.1 The named selected-support hypothesis as a weaker bridge

Killed exactly. For every valid selection,

```text
H-E_Hahn-L = S_shell >= 0.                           (9.1)
```

Therefore the predecessor's requested strict inequality is impossible for any
existing oversized list. The hypothesis is equivalent to the desired list cap,
not one independent statement short of it.

### 9.2 Optimizing the frozen dual over support choices

Killed as a standalone payment route. For a fixed actual list,

```text
min_selection (H-E_Hahn)
  = L + min_selection S_shell
  >= L.                                              (9.2)
```

Support optimization can tighten the frozen dual certificate down toward the
actual list size, but never below it.

### 9.3 Ordinary pairwise Hahn/Delsarte at all degrees

Inherited exact route stop:

```text
floor(H) = 20737821,
20737821-16777214 = 3960607.                         (9.3)
```

The matching fractional optimum has zero spectral and shell reserves.

### 9.4 Repeated scalar shortening with Plotkin/singleton terminal caps

Inherited exact route stop:

```text
minimum pulled-back cap = 30682446,
30682446-16777214 = 13905232.                        (9.4)
```

The minimum occurs after two shortenings.

### Stop verdict

The adjacent rows remain unconditionally open. The exact obstruction is no
longer an unnamed selected-support hypothesis. It is the absence of an
RS-specific theorem forcing the coupled deletion/addition system of Section 6
to contribute more than the conserved target reserve, together with the lack
of an actual target-sized counterexample.

## 10. Current best statements and falsifiers

### Claim A — exact complementarity theorem

**Statement.** Under the frozen adjacent dual factorization, every valid
selected-support realization satisfies (3.3), with the explicit nonnegative
shell defect (B)--(C).

**Falsifier.** One exact valid realization violating the identity or
nonnegativity.

### Claim B — target-equivalence theorem

**Statement.** Under Claim A and existence of exact-size support choices,
`RS_HAHN123_SELECTION_GAP` is equivalent to the adjacent cap `L<=16777214`.

**Falsifier.** One adjacent row on which the two propositions have different
truth values while Claim A holds.

### Claim C — target-sized surplus census

**Statement.** Every hypothetical target-sized low-row list satisfies (6.5),
and every hypothetical target-sized high-row list satisfies (6.6).

**Falsifier.** A target-sized list exceeding the corresponding total-incidence
maximum while respecting the degree root bound.

### Claim D — random-transversal certificate

**Statement.** If the exact expectation in (6.10) exceeds `Delta_open`, then no
target-sized adjacent list with those full agreement sets exists.

**Falsifier.** Full agreement sets satisfying the strict expectation inequality
but admitting a target-sized list.

### Open claim

An inequality strong enough to make (6.10), or another independent hybrid
reserve bound, exceed `Delta_open` for every target-sized adjacent RS list is
**not obtained / open**. An explicit target-sized unsafe list is also **not
obtained / open**.

## 11. Natural next step

Work with exactly `B*` codewords and their full agreement sets, not an already
selected constant-weight family.

The most direct next theorem is one of the following equivalent forms of a
noncircular structural input:

1. a lower bound on the random-transversal expectation (6.10) derived from a
   fixed-syndrome or Padé compatibility identity;
2. a deterministic lower bound on the maximum shell defect of the coupled
   deletion/addition system; or
3. a hybrid theorem for one common selection,
   `E_Hahn>=eta` and `S_shell>Delta_open-eta`, where the component bounds are
   stated on an independently defined RS class rather than guarded only by
   `L>=B*`.

A negative result should print one target-sized ordinary list, or a complete
full-agreement hypergraph satisfying all polynomial compatibility constraints
and keeping every valid selection at or below the conserved reserve.

## 12. Derivation-direction ledger

| Printed quantity | Exact value | Direction |
|---|---:|---|
| field characteristic | `2147483647` | frozen input, also derived as `2^31-1` |
| domain size | `981129` | frozen input |
| boundary weight | `67447` | frozen input |
| exchange distance | `67448` | derived as `w+1` |
| common selected weight `s0` | `72860` | derived from the adjacent rows and complement symmetry |
| budget | `16777215` | frozen input |
| ordinary cap target | `16777214` | derived as `B*-1` |
| adjacent rows | `(5413,72860)`, `(840822,908269)` | frozen input |
| pairwise full-agreement caps | `5412,840821` | derived as `d-1` on the low and high rows |
| dual coefficients `c1,c2,c3` | exact rationals in Section 2 | inherited from `fixedg_adjacent_hahn_stop.md` |
| dual objective `H` | exact rational in Section 2 | inherited from the matching dual/primal certificate |
| decimal `H` | `20737821.0968996317...` | bounded decimal display of the exact rational |
| cubic coefficient `alpha` | exact rational in (2.1) | inherited from the exact dual factorization |
| exchange-distance roots | `67448,70799,70800` | inherited factorization roots |
| intersection roots | `5412,2061,2060` | derived by subtracting the distance roots from `72860` |
| `Delta_open` | exact rational in (3.6) | derived as `H-B*` |
| decimal `Delta_open` | `3960606.0968996317...` | bounded decimal display |
| `theta_open` | exact rational in (4.3) | derived as `Delta_open/c3` |
| `theta_closed` | exact rational in Section 4 | inherited convenient non-strict proxy, derived as `(H-ell)/c3` |
| target-size incidence remainder | `244929` | enumerated by exact division of `B*s0` by `N` |
| integral `G_1` floor | exact rational in (5.2) | derived by minimizing integer coordinate-degree variance |
| integral `G_3` ceiling | exact rational in (5.3) | derived from complementarity, the `G_1` floor, and nonnegativity |
| ceiling improvement | `4.0104695319...*10^-10` | bounded difference of the exact ceilings |
| low-row total-incidence maximum | `1222536914966` | derived by exact integer solution of (6.4) at `L=B*` |
| low-row total surplus | `149030066` | derived by subtraction |
| low-row average surplus | `149030066/16777215` | derived by division; decimal bounded |
| high-row total-incidence maximum | `15238236246526` | derived by exact integer solution of (6.4) at `L=B*` |
| high-row total surplus | `11955691` | derived by subtraction |
| high-row average surplus | `11955691/16777215` | derived by division; decimal bounded |
| exact-size high-row codewords | at least `4821524` | bounded by subtracting total surplus from `B*` |
| high-row complement shift | `-835409` | derived as `N-2*908269` |
| falling-factorial orders | `1,2,3` | derived from the cubic degree of `Phi` |
| allowed intersection count | `5413` | derived from integer range `0..5412` |
| `Q_star` | exact rational in (7.2) | derived as `Delta_open/(alpha(B*-1))` |
| outside-band radius | `100` | chosen test radius |
| inside-band radius | `99` | derived as the complementary integer radius below `100` |
| minimum outside-band shell cost | `32835100` | enumerated over all `5413` allowed intersections |
| outside-band fraction | `0.1172113851386057...` | bounded by `Q_star/32835100` |
| inside-band fraction | `0.8827886148613943...` | derived as one minus the outside bound |
| target-sized first-moment contribution | `0.0075482485...` | bounded decimal of `c1` times the exact floor (5.2) |
| endpoint ordinary cap | `2310492` | inherited from `fixedg_boundary_endpoint_plotkin.md` |
| complete Hahn integer cap | `20737821` | derived as `floor(H)` in the attached certificate |
| complete Hahn target excess | `3960607` | derived by integer subtraction |
| scalar-route minimum | `30682446` | inherited exact all-depth route minimum |
| minimizing shortening depth | `2` | inherited exact argmin of the scalar route |
| scalar-route target excess | `13905232` | derived by subtraction |
| unconditional adjacent payment | not obtained / open | open |
| proof of a nonvacuous RS reserve lower bound | not obtained / open | open |
| explicit adjacent unsafe list | not obtained / open | open |

## 13. References

- `fixedg_interior_hahn_gap_paper.md`: Conjecture
  `RS_HAHN123_SELECTION_GAP`, equations (3.1)--(3.5), and Sections 4--7.
- `fixedg_interior_hahn_gap_note.md`: Sections 3--5 and the
  derivation-direction ledger.
- `fixedg_adjacent_hahn_stop.md`: Theorems 1--2; Section 4.1, exact cubic dual
  factorization; Section 4.2, matching fractional primal and its three root
  shells.
- `fixedg_boundary_endpoint_plotkin.md`: Theorem 2.1 and Section 6, endpoint
  payment and adjacent scalar route stop.
- `fixedg_universal_rs_embedding.md`: Theorem 4.1 and Corollaries 5.1--5.2,
  fixed-`G`/ordinary-list embedding and threshold equivalence.

The attachment names above resolve in this repository as follows.

- `fixedg_boundary_endpoint_plotkin.md` is
  `experimental/notes/thresholds/m31_fixed_g_boundary_endpoint_plotkin_v1.md`,
  integrated.
- `fixedg_universal_rs_embedding.md` is
  `experimental/notes/thresholds/m31_fixed_g_universal_rs_embedding_v1.md`,
  integrated.
- `fixedg_adjacent_hahn_stop.md` is
  `experimental/notes/thresholds/l_fixedg_adjacent_hahn_stop_v1.md`; it was
  submitted and was not yet integrated when this round ran.
- `fixedg_interior_hahn_gap_paper.md` and `fixedg_interior_hahn_gap_note.md` are
  `experimental/papers/fixedg_interior_hahn_gap.md` and
  `experimental/notes/thresholds/fixedg_interior_hahn_gap.md`; both were
  submitted and were not yet integrated when this round ran.

## Serendipity epilogue

The high row is much more discrete than its symmetric constant-weight picture
suggests. Any target-sized counterexample would have average full-agreement
surplus below one, so at least `4821524` of its codewords would have exactly the
minimum `908269` agreements and therefore no support-choice freedom at all.
The remaining codewords must simultaneously carry every available addition
choice while keeping **every** resulting transversal concentrated near the
three dual root shells. That rigid mixture of millions of frozen error cores
and a comparatively sparse set of movable additions was not part of the
request, but it is likely the cleanest concrete object for the next attack.
