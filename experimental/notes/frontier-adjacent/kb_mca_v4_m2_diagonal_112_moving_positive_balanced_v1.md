---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
atom_or_cell: K3_M2_DIAGONAL_112_MOVING_POSITIVE_BALANCED_1_1
quantifier: the canonical unordered source-star pair {{2,b},{2,1/b}} with aligned-positive balanced root distribution (1,1)
projection_and_unit: exact source-facet reconstruction, finite-y w=0 deletion, four q-slice equations, and two necessary full-quotient parity equations in the deployed characteristic; not an owner or payment
claimed_bound: the canonical moving-moving aligned-positive balanced (1,1) pattern is empty
status: PROVED_CANONICAL_MOVING_MOVING_ALIGNED_POSITIVE_BALANCED_1_1_EMPTY
review: FRESH_INDEPENDENT_GREEN_NO_ISSUE
impact: deletes the balanced root distribution for one canonical source-star assignment; ledger movement zero
falsifier: an admissible canonical moving-moving balanced (1,1) reconstruction surviving the exhaustive first-match q-slice/parity partition
replay: python3 experimental/scripts/verify_kb_mca_v4_m2_diagonal_112_moving_positive_balanced_v1.py --check --tamper-selftest
---

# KoalaBear diagonal `(1,1,2)` canonical moving-positive balanced-pattern deletion

## 0. Verdict and scope

For the canonical unordered source-star pair

```text
{{2,b},{2,1/b}},
```

the moving-moving aligned-positive source-line pattern with balanced residual
root distribution

```text
at c: (W-1/c)(W-1/d),    at d: (W-1/c)(W-1/d)       (0.1)
```

is empty over the deployed field.

The proof is an exhaustive first-match partition of this one exact necessary
system. The affine boundary `w=0` is empty already at the q-slice. On the
remaining `w!=0` chart, the coefficient-zero and factor-boundary charts lie
on named parent boundaries, the `L2` chart is deleted by the `I`-side parity
constraint, and the generic `F5` chart is deleted by the `J`-side parity
constraint. A separate `y=infinity` computation is retained only as a
non-load-bearing compactification control.

This packet does **not** transport the result to the other three
moving-moving assignment types. Those are separate exact systems and remain
open. It also does not delete the doubled patterns `(2,0)` or `(0,2)`, a
near-aligned positive template, an exceptional branch, or the complete
`(1,1,2)` row. It books no owner and moves no ledger charge.

## 1. Imported source interface and canonical assignment

Use the saturated source-line interface of the universal source-facet census
at commit

```text
c2edcfa5cbfb8a41e7dea04ae1b34325c90ed5dc.          (1.1)
```

Normalize

```text
tau(x)=1/x,
J_0={2,1/2,b,1/b},
J_1={c,d}.                                           (1.2)
```

The parent census includes the canonical unordered source-star pair

```text
{{2,b},{2,1/b}}.                                     (1.3)
```

The parent combinatorial census also lists three other moving-moving
assignment types:

```text
{{2,b},{2,1/b}},
{{2,b},{1/2,b}},
{{2,1/b},{1/2,1/b}},
{{1/2,b},{1/2,1/b}}.                                (1.4)
```

No covariance statement is made. An exact audit found that the natural
endpoint-only Möbius action preserves the observed residual data but not the
aligned target, whereas the corresponding diagonal action on the `W`
coordinate preserves the target but not the observed residual data. Thus
neither action transports the complete exact system. This packet derives and
deletes only (1.3); the three assignments in (1.4) are
`OPEN_SEPARATE_EXACT_SYSTEMS`. The Python mutation suite rejects any
four-assignment or covariance globalization claim.

## 2. Exact q-slice descent

For the representative (1.3), the Sage replay rebuilds the parent
five-row source form

```text
G(T,W)=U(T,W)^2-WV(T,W)^2.                           (2.1)
```

At each of `c,d`, divide by the proved forced square `(W-w)^2` and impose
projective proportionality to (0.1). This gives four exact equations before
any specialization.

Put

```text
y=b+b^-1,             s=c+d,             p=cd.       (2.2)
```

Each reciprocal polynomial in `b` descends exactly to `y`. Reducing an
ordered root through

```text
X^2-sX+p=0                                               (2.3)
```

gives

```text
A_0(y,s,p,w)+c B_0(y,s,p,w)=0,
A_1(y,s,p,w)+c B_1(y,s,p,w)=0.                       (2.4)
```

The two equations at `d` are the swapped companions. Since `c-d` is a
declared unit, paired vanishing is equivalent to

```text
A_0=B_0=A_1=B_1=0.                                  (2.5)
```

This use of both companions is load-bearing: a single pointwise equation
`A+cB=0` would not imply `A=B=0`.

The source reconstruction also gives the exact incidence identity

```text
A=-4s+5p+5,
D=-2sw+4pw+2s-p+w-4,
E=-2sw+pw+2s-4p+4w-1,
z=-D/E.                                             (2.6)
```

The imported parent interface has `E!=0` because `E` is the source-incidence
denominator, and `A!=0` because `A` occurs in the reconstruction
determinant. The internal source point is nonzero; hence `z=-D/E` and
`E!=0` imply `D!=0`. These parent implications, rather than an undeclared
division, justify every later use of `A`, `E`, or `D` as a unit.

After removing only the named parent units, exact factorization gives

```text
B_0 ~ L2 F5,                 B_1 ~ F11,              (2.7)
L2 = y(p+1)-2s,
F5 = alpha(s,p,w)y+beta(s,p,w).
```

The certificate binds the complete metrics and hashes of
`A_0,B_0,A_1,B_1,L2,F5,F11,alpha,beta`.

The normalization/sign audit is explicit. The residual divisor
`(W-w)^2`, the target `W^2` pivot, and the root-reduction divisor
`X^2-sX+p` are monic. Each of the four raw rational projective lines is
cleared by its **entire** denominator and then multiplied by one common
nonzero rational scalar; no constant and linear coefficients are normalized
separately. In `c,c,d,d` order the common scalars are

```text
1/79766443076872509863361, -1/282429536481,
1/79766443076872509863361, -1/282429536481.          (2.8)
```

The two `c` lines have primitive denominator pattern

```text
cd(w-1)^2(w+1)^2(d-2)^2(2d-1)^2(b-1)^2(b+1)^2 A^2,
```

and the `d` lines have the companion with `c` in place of `d`. The source
reconstruction determinant is checked before inversion: its denominator is
`E^6`, while its numerator has exactly the declared collision factors
`(d-2)^2(2d-1)^2(c-2)^2(2c-1)^2(w-1)^5(w+1)^5
A(p-1)^2`. The q-slice removes only the whole factors
`(p-1)E^2,1,(p-1)E^2,1`. This audit is load-bearing: independent primitive
normalization of the two coefficients could change their relative sign.

## 3. Boundary-chart repair

The canonical parameter `b` is a finite nonzero field element, so
`y=b+b^-1` is affine and finite. Nevertheless, as a defensive
compactification check, homogenize the q-slice in `[Y:Z]` and evaluate
`Z=0` by taking the coefficient of `y^2`. The four resulting generators
have degree/multidegree/term-count data

```text
A0_y2  8 / (4,6,2) / 72,    B0_y2  7 / (3,5,2) / 44,
A1_y2 13 / (7,9,4) / 252,   B1_y2 12 / (6,8,4) / 182.          (3.1)
```

Their deployed-field ideal has dimension one and a 23-element reduced
Groebner basis. For the exact twelve-factor named localizer `H_infinity`,

```text
NF(H_infinity)!=0,          NF(H_infinity^2)=0.                 (3.2)
```

The Rabinowitsch ideal
`<A0_y2,B0_y2,A1_y2,B1_y2,t H_infinity-1>` has reduced basis `{1}`.
Sage, Singular, and Wolfram replay this calculation independently. It is
marked `load_bearing=false`: it neither enlarges the canonical affine
quantifier nor transports the result to another assignment.

The external repair audit payload for this control was
`16cd5144eb45c930e48d02388c658c7aee19d4e60956421e83bb0a485a7e28e8`;
the packet rederives it rather than trusting a serialized basis.

The actual first-match gate is the affine chart `w=0`. Direct specialization
of the four q-slice equations gives generators with data

```text
A0  8 / (2,6,6) / 74,       B0  7 / (2,4,5) / 48,
A1 11 / (2,9,9) / 154,      B1 10 / (2,7,8) / 119.             (3.3)
```

Their deployed-field ideal has dimension one and a 24-element reduced
Groebner basis. Let `H_0` be the product of the nine applicable parent
factors

```text
p, s^2-4p, p-1, 1-s+p, 1+s+p, 4-2s+p,
1-2s+4p, 5p-4s+5, 2s-4p-1.                         (3.4)
```

Then exact reduction gives

```text
NF(H_0)!=0,       NF(H_0^2)!=0,       NF(H_0^3)=0.              (3.5)
```

The Rabinowitsch ideal `<A0,B0,A1,B1,t H_0-1>` also has reduced basis
`{1}`. Thus the valid-label `w=0` chart is empty by the q-slice alone.
Only after this deletion may the parity argument enter the complementary
affine chart `w!=0`.

The external repair audit payload for this chart was
`e507788efd3bd9be3bd04b14a40e70cbf34acec0eadc24044a3294d057027980`;
again the packet rederives every generator, basis, remainder, and
Rabinowitsch conclusion.

## 4. Necessary quotient-parity constraints

Write `delta=b-b^-1`. On the moving-moving chart `delta` is nonzero. The
anti-invariant source reconstruction becomes symmetric after setting

```text
Ubar=delta U,
Gbar(T,Y)=Ubar(T,Y)^2-(y^2-4)YV(T,Y)^2.             (3.1)
```

Quadratic norms over the pairs `{b,1/b}` and `{c,d}` compute the endpoint
products without adjoining their roots. The first odd coefficient in each
full quotient identity factors as

```text
Parity_J ~ w^2 D L2 E^6 P25,
Parity_I ~ E^3 P46,                                  (3.2)

D=-2sw+4pw+2s-p+w-4,
E=-2sw+pw+2s-4p+4w-1.
```

Here `A`, `E`, and `D` are imported parent units by (2.6), while `w!=0`
holds only because the first-match `w=0` chart was deleted in Section 3.
The primitive factors have exact metrics

```text
P25: total degree 25, multidegree (6,14,14,6),  5048 terms,
P46: total degree 46, multidegree (5,25,25,17), 35534 terms.   (3.3)
```

Their hashes are

```text
P25 1a1685279f4e80a86eaf399153051a4c7f7ccc691a2d63c33791d5980174a8d3
P46 725c9adcb6d74e93868675be71a65b0321f79bdaf895ba3e571acdad4dac4696.
                                                               (3.4)
```

Only these necessary parity coefficients are used. The lower squared
quotient coefficients are not needed.

Each parity line is likewise cleared once as a whole line. The common
rational scalars are

```text
2/16423203268260658146231467800709255289,
1/17455927136175424851782794958953454680082898.      (3.5)
```

The corresponding primitive denominator patterns are

```text
core2^3 corehalf^3 (p-1)^3 (w-1)^4 A^5 (w+1)^5,
w^2 p^2 (p-1)^3 A^5 core2^5 corehalf^5
  (w-1)^5 (w+1)^5 D^2.                              (3.6)
```

The `L2` and `F5` substitutions clear their full denominators by
`(p+1)^degree_y` and `alpha^degree_y`, respectively. The final eliminant is
normalized by one common nonzero deployed-field scalar.

## 5. Exhaustive first-match partition

The complete partition begins with

```text
0. finite y and w=0: empty by the q-slice;
1. finite y, w!=0, and L2=0;
2. finite y, w!=0, L2!=0, and F5=0:
   2a. alpha=0 (hence beta=0);
   2b. alpha!=0 and D=0,R=0;
   2c. alpha!=0 and D=0,R!=0,G9=0;
   2d. alpha!=0 and D!=0,R=0;
   2e. alpha!=0 and D!=0,R!=0,G9=0,                (4.1)

R=-5s+4p+4.
```

The non-load-bearing `y=infinity` compactification control is not a
first-match branch because canonical `b` is finite and nonzero. On every
branch after item 0, `w!=0`. On `alpha!=0`, substitute `y=-beta/alpha`.
After removing named parent factors,

```text
A_0 ~ G7,             A_1 ~ G15,             F11 ~ R G9.       (4.2)
```

The factors have respective degree/term counts

```text
G7:  7 / 43,          G15: 15 / 339,          G9: 9 / 94.      (4.3)
```

Thus (4.1), preceded by the `w=0` deletion, is disjoint and exhaustive on
the canonical affine system. Every nonzero declaration is included in that
chart's displayed localizer; no selector is divided out before its zero
chart is classified.

### 5.1 The `L2` chart

The coefficient-zero subchart `p+1=0` has `p=-1`; then `L2=0` forces
`s=0`, so the core locator is `T^2-1`. Its two roots are inversion-fixed
labels and the chart is a parent collision.

Off `p+1=0`, substitute

```text
y=2s/(p+1).                                          (4.4)
```

The retained q-slice equations are

```text
w^2-p=0,                   H9=0,                   R=0.          (4.5)
```

Their deployed-field ideal is zero-dimensional with a three-element reduced
Groebner basis. The `J` parity equation vanishes automatically because
`L2=0`; the `I` parity equation requires `P46=0`. Its normal form has degree
seven and twelve terms, with hash

```text
ae2e03fcbb73ab177ddf992966aab46dc1e575cb14377830b0c287831295294f.
                                                               (4.6)
```

After adjoining it, elimination gives

```text
p^2(p+1)^4(p-1)^2(p-4)(p-1/4).                      (4.7)
```

Every root is a named boundary:

```text
p=0       nonzero-core failure;
p=-1      the coefficient-zero chart above;
p=1       reciprocal-core collision;
p=4       R=0 gives s=4, hence q=(T-2)^2;
p=1/4     R=0 gives s=1, hence q=(T-1/2)^2.         (4.8)
```

Equivalently, the complete fourteen-factor named localizer has zero normal
form modulo the three-element `P46` basis. The localized ideal is the unit
ideal, so the whole `L2` chart is empty.

### 5.2 The coefficient-zero `F5` chart

If `alpha=0`, the equation `F5=0` also gives `beta=0`. The exact ideal

```text
<alpha,beta,A_0,A_1,F11>                             (4.9)
```

has dimension two and a 24-element deployed-field Groebner basis. The
product of `L2` and the thirteen named parent units has zero normal form.
Thus every component lies on `L2=0` or a parent collision; the retained
coefficient-zero chart is empty already at the q-slice.

### 5.3 The three factor-boundary `F5` charts

The exact q-slice bases and localizer conclusions are:

```text
chart                         dimension     basis size     NF(H)
D=0,R=0                           0              4           0
D=0,R!=0,G9=0                     1              9           0
D!=0,R=0                          1              2           0.             (4.10)
```

Here `H` is the product of the common parent factors, `alpha`, `L2`, and
exactly those first-match selectors declared nonzero in the row. Therefore
each component belongs to a named collision or an earlier first-match row.
No parity equation is needed on these three charts.

### 5.4 The generic `F5` chart

The q-slice ideal

```text
<G7,G15,G9>                                           (4.11)
```

has dimension one and a 38-element deployed-field Groebner basis. The
normal forms of the two parity factors each have degree thirteen and 368
terms:

```text
P25 d320c59d012bb6c3d8287c7f83ec9dd3e0977faeff61528c401b316e0333a0ce
P46 a0f77109edc5d92ab670dabddfe35a6116012e65e8845fed72aadf3a43a29406.
                                                               (4.12)
```

Adjoining only the `P25` normal form leaves a dimension-one, 35-element
basis. Let `H` be the product of the thirteen parent units and the four
nonzero selectors

```text
alpha, L2, D, R.                                      (4.13)
```

Sequential exact reduction gives

```text
NF(H)!=0,                         NF(H^2)=0.          (4.14)
```

After localization at `H`, equation (4.14) makes the ideal unit. Hence the
generic component is empty. `P46` is not needed for this deletion.

## 6. Field, evidence, and nonclaims

The reconstruction, reciprocal descent, factor extraction, and parity
factorization are exact characteristic-zero identities. Every incidence
and localization statement is replayed natively in

```text
GF(2130706433).                                      (6.1)
```

The challenge field is the degree-six extension of this prime field. Unit
ideals and pointwise component containment persist under scalar extension.

This is an exact deployed-field proof, not a toy-field, sampled, numerical,
or asymptotic experiment. Layer-cake summability and
Markov/Chebyshev/moment optimization are not used. The parameters
`T,Y,L,L_barI,lambda,I,h` do not occur; there are no hidden asymptotic
constants.

In particular this packet claims only:

```text
canonical {{2,b},{2,1/b}} moving-moving aligned-positive
balanced (1,1): EMPTY.                                           (6.2)
```

It does **not** claim:

- either moving-moving doubled root distribution is empty;
- any of the other three moving-moving source-star assignments is empty;
- a covariance or orbit transport from the canonical assignment;
- any near-aligned positive or exceptional branch is empty;
- the complete `(1,1,2)` row, K3, or the KoalaBear row is closed;
- an owner, a slope/codeword projection, or a ledger payment;
- a new theorem over arbitrary characteristics.

## 7. Replay and audit status

Run:

```bash
python3 experimental/scripts/verify_kb_mca_v4_m2_diagonal_112_moving_positive_balanced_v1.py \
  --check --tamper-selftest
```

The Python verifier checks canonical JSON, provenance and Git blobs, the
canonical assignment scope, exact branch coverage, polynomial metrics,
artifact hashes, and mutation rejection—including rejection of an orbit
globalization overclaim. The Sage replay rebuilds the source and parity
inputs rather than loading a serialized discovery object. Sage, Singular,
and Wolfram each replay the affine `w=0` q-slice and the non-load-bearing
`y=infinity` control. Singular also replays the representative `L2/P46`
elimination and factorization; Wolfram recomputes the six finite-`y`,
`w!=0` Groebner/localizer checks, including `NF(H)!=0` and `NF(H^2)=0` on
the generic chart.

Generator proof-audit classification for the frozen packet:

- **PROVEN / IMPORTED:** the source-facet interface and its twelve-assignment
  census at (1.1);
- **PROVEN:** for the canonical assignment, reciprocal/symmetric q-slice
  descent, the affine `w=0` deletion, both parity factors, the exhaustive
  finite-`y` first-match partition, and all six `w!=0` localized deletions;
- **CONTROL / NON-LOAD-BEARING:** the `y=infinity` compactification chart;
- **OPEN:** the three other moving-moving assignment systems;
- **NOT CLAIMED:** global ownership, add-back, K3, or row payment.

Generator assessment: the exact derivation and native tool replays are
complete. A fresh independent reviewer returned **GREEN / NO ISSUE** for the
repaired canonical packet. The canonical local deletion is therefore GREEN
and may be banked. This promotion does not enlarge its quantifier: the other
three moving-moving assignment systems, global K3, and the KoalaBear row
remain open, and ledger movement remains zero.
