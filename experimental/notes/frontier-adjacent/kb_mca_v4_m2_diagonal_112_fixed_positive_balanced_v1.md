---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
atom_or_cell: K3_M2_DIAGONAL_112_FIXED_POSITIVE_BALANCED_1_1_REPRESENTATIVE
quantifier: the single normalized saturated source-line representative J_0={2,1/2,b,1/b}, J_1={c,d}, with fixed-moving assignment {{2,1/2},{2,b}} and balanced root distribution (1,1)
projection_and_unit: exact source-facet reconstruction and four q-slice projective equations in the deployed characteristic; not an owner or payment
claimed_bound: this normalized fixed-moving balanced (1,1) representative is empty
status: PROVED_REPRESENTATIVE_ONLY_OTHER_SEVEN_FIXED_MOVING_ASSIGNMENTS_OPEN_SEPARATE_EXACT_SYSTEMS_COVARIANCE_NOT_CLAIMED_K3_OPEN
impact: together with the repaired same-representative predecessors, removes all three root distributions for one normalized fixed-moving assignment; ledger movement zero
falsifier: an admissible reconstruction in the declared normalized representative surviving all four q-slice equations
replay: python3 experimental/scripts/verify_kb_mca_v4_m2_diagonal_112_fixed_positive_balanced_v1.py --check --tamper-selftest
---

# KoalaBear diagonal `(1,1,2)` fixed-positive balanced representative deletion

## 0. Verdict

For the exact normalization

```text
J_0={2,1/2,b,1/b},  J_1={c,d},
assignment={{2,1/2},{2,b}},
```

the fixed-moving aligned-positive source-line system with balanced residual
root distribution

```text
at c: (W-1/c)(W-1/d),    at d: (W-1/c)(W-1/d)       (0.1)
```

is empty over the deployed field. This is one normalized representative,
not the complete fixed-moving assignment class.

The other seven fixed-moving assignments are
`OPEN_SEPARATE_EXACT_SYSTEMS`. Complete-system projective covariance is
`NOT_CLAIMED`: acting only on endpoint labels preserves the observed
residual side but not the aligned target, while applying the corresponding
diagonal transport to the `W` coordinate preserves the target but not the
observed residual/source `W` divisor. Thus neither action transports the
whole source system proved below.

This is only the balanced multiplicity pattern `(1,1)`. For this same
representative, the repaired immediate predecessor deletes identity-doubled
`(2,0)` and binds the repaired crossed `(0,2)` predecessor. Consequently all
three root distributions are deleted **only for this one normalized
fixed-moving assignment**. The corresponding seven crossed, identity, and
balanced systems remain separate and open.

This does not delete a moving-moving template, a near-aligned positive
template, an exceptional branch, or the complete `(1,1,2)` row. It books no
owner and moves no ledger charge.

## 1. Imported interface and exact reconstruction

Use the saturated source-line interface of the universal source-facet census
at commit `c2edcfa5cbfb8a41e7dea04ae1b34325c90ed5dc`. Normalize

```text
tau(x)=1/x,
J_0={2,1/2,b,1/b},
J_1={c,d},
```

Fix the single internal assignment

```text
{2,1/2}, {2,b}.                                      (1.1)
```

The same-representative identity predecessor is pinned at commit
`9f5b7ffa8759f0372802792bc5baf589410cdd28`, with certificate, note, and
verifier blob OIDs

```text
1e083a5cac1bba0827ae2c6c9e72ffd9da03d3ba
8a541e989d9882316cd25de90bebb37afec116a6
45c5d583039c326705769e55dc309142f3b39813
```

and certificate payload
`ce59e2be2417dd8681bce65d7f0d838850445dfccbd82d68c137387510ea7cb5`.
That predecessor in turn binds the repaired crossed packet for this same
assignment.

No coordinate relabeling is used to enlarge this quantifier. Although an
endpoint normalizer may carry the displayed edge pair to another
fixed-moving combinatorial assignment, the complete source system is not
covariant under the asserted action: endpoint-only transport misses the
aligned target, and diagonal `W` transport misses the observed residual and
source `W` divisor. The algebra below therefore applies only to (1.1).

The Sage replay rebuilds the parent source form

```text
G(T,W)=U(T,W)^2-WV(T,W)^2                           (1.4)
```

over `QQ` from the five-row reconstruction system. At each of `c,d`, it
divides by the proved forced square `(W-w)^2` and imposes projective
proportionality to (0.1). This gives four exact polynomial equations:

```text
q_C(b,c,d,w)=0,  e_C(b,c,d,w)=0,
q_D(b,c,d,w)=0,  e_D(b,c,d,w)=0.                    (1.5)
```

Here `q_C,q_D` are quadratic in `b`; each has total degree 12 and 197
terms. The other two equations have total degree 20 and 943 terms. The
certificate binds all four canonical polynomial hashes. There is no
sampling or interpolation.

## 2. Exhaustive leading-coefficient split

Write

```text
q_C=L(c,d,w)b^2+M(c,d,w)b+N(c,d,w).                 (2.1)
```

The leading coefficient `L` has degree 10, 69 terms, and SHA-256

```text
1d10dcd6da3f56234773ef8067f1471d636ed43d71dca825576554e5fe05bd8e.
```

The proof partitions the complete affine chart into

```text
L=0,                  L!=0.                          (2.2)
```

No division by `L` precedes this split.

Put

```text
E1=4cdw-cd-2cw-2dw+2c+2d+w-4,
E2=cdw-4cd-2cw-2dw+2c+2d+4w-1,
A =5cd-4c-4d+5,

Hbasic=bcdw E1 E2 (b-1)(b+1)(c-1)(c+1)(d-1)(d+1)
       (w-1)(w+1) A (cd-1)(b-2)(2b-1)(c-d).        (2.3)
```

These are named parent incidence, fixed-point, distinct-label, and
reconstruction units. Every localization below is a displayed
Rabinowitsch equation, not a generic saturation.

## 3. The `L=0` chart

Over `GF(2130706433)`, the exact ideal

```text
<L,q_C,q_D,e_C,e_D,t Hbasic-1>                      (3.1)
```

has reduced Groebner basis `[1]`. The subchart `L=M=N=0`, on which the
now-linear equation would have both coefficient and constant zero, is
therefore also empty.

The localizer in (3.1) is deliberately smaller than the full parent
distinct-label localizer. Thus this deletion is stronger than the
full-chart statement needed here.

## 4. The quadratic `L!=0` chart

Work in

```text
K_0[b]/(q_C),             K_0=QQ(c,d,w).             (4.1)
```

The other three equations in (1.5) reduce to degree at most one in `b`.
Use the `q_D` remainder as the first pivot. Substituting its ordinary
solution into `q_C` gives the **complete** factorization

```text
q_terminal
 = -(w-1)^2 (w^2-cd) (cd-1) A^2 q_essential.       (4.2)
```

The replay asserts all five factors, their exponents, and the scalar `-1`
before selecting any component. This point is load-bearing:
`w^2-cd` is not a declared unit and is handled separately in Section 4.1.

### 4.1 The incidence component `cd=w^2`

The direct deployed-field ideal

```text
<q_C,q_D,e_C,e_D,cd-w^2,t Hbasic L Hfixed-1>        (4.3)
```

has basis `[1]`. Here `Hfixed` adds the fixed-label differences involving
`c,d` and `2,1/2`; all are part of the retained parent chart.

There is also a smaller independent replay. Substitute

```text
d=w^2/c.                                             (4.4)
```

After removing only factors in the named localizer, the essential `q_C`
and `q_D` factors have degree 8 and 32 terms each. Their hashes are

```text
q_C: 14d979e5e87e8c63e28417bef8ca2bfa5278cde9fb2004f2ca0e0d6ac87f4589
q_D: dcff91b87a60d0f9ae50f39b549602cd13d7b3176b9a1a88fe1b308e2ef2dc02.
```

Those two factors alone, together with the explicit substituted parent and
`L` localizer, generate the unit ideal. The checked Singular replay and the
local Wolfram replay independently recompute this compact unit ideal.

### 4.2 Symmetric form of `q_essential`

Put

```text
s=c+d,                    p=cd.                      (4.5)
```

The remaining two linear compatibilities are exchanged by `c<->d`. Exact
reduction modulo `c^2-sc+p` gives

```text
q_essential = Q(s,p,w),
slice(c,d,w)=A_0(s,p,w)+c B_0(s,p,w),
slice(d,c,w)=A_0(s,p,w)+d B_0(s,p,w).               (4.6)
```

Since `c-d` is a declared unit, the two slice equations are equivalent to

```text
Q=A_0=B_0=0.                                         (4.7)
```

The exact metrics are

```text
Q:   degree 7,  43 terms,
A_0: degree 9, 115 terms,
B_0: degree 8,  84 terms.                            (4.8)
```

Their certificate-bound hashes are independently replayed by Sage.

Localize (4.7) at the named symmetric units

```text
p, s^2-4p, p-1, 1-s+p, 1+s+p, 4-2s+p,
1-2s+4p, w, w^2-1, w^2-sw+p,
1-sw+pw^2, 5p-4s+5.                                 (4.9)
```

The localized ideal has dimension one. Its Groebner basis contains

```text
(p+w)^2,                (5s+4w-4)^2.                (4.10)
```

Therefore every geometric point over every extension of the deployed
prime field satisfies

```text
p=-w,                   5s+4w-4=0.                  (4.11)
```

This pointwise inference is valid despite the squared relations: fields
have no nonzero nilpotents. Singular and Wolfram independently reduce both
squares to zero modulo the exact localized ideal.

### 4.3 First-pivot ordinary chart

Retain the ordered root `c`, impose

```text
c^2-sc+p=0,                                          (4.12)
```

and invert the actual coefficient and denominator of the linear `q_D`
remainder, in addition to (4.9). The exact localized ideal generated by
`Q,A_0,B_0` and (4.12) has basis `[1]`.

Thus an ordinary first pivot loses no point. On the only support (4.11),
both the coefficient and constant of that first remainder vanish, so the
support is passed to a second, exhaustive pivot rather than divided away.

### 4.4 Second-pivot split on the support curve

Substitute (4.11) while retaining the ordered root:

```text
s=4(1-w)/5,             p=-w,
c^2-(4/5)(1-w)c-w=0.                                (4.13)
```

Of the three linear remainders in (4.1):

```text
q_D remainder:       coefficient=constant=0,
e_C remainder:       not identically zero,
e_D remainder:       not identically zero.          (4.14)
```

Use the `e_C` remainder as the second pivot.

The coefficient-zero chart imposes its actual coefficient and constant,
the curve equation (4.13), and every denominator introduced on the chart.
Its localized basis is `[1]`.

On the complementary ordinary chart, solve for `b` and impose both `q_C`
and the remaining `e_D` remainder. With the actual pivot numerator,
denominators, and named curve units inverted, this localized basis is also
`[1]`.

Equations (4.14) and the two second-pivot charts are exhaustive. Hence the
`q_essential` component is empty.

## 5. Characteristic and theorem scope

The source reconstruction, factor extraction, and symmetric reductions are
exact characteristic-zero identities. Every emptiness statement is
replayed natively in the deployed characteristic

```text
p=2130706433.                                        (5.1)
```

The challenge field is the degree-six extension of this prime field. Unit
ideals and the pointwise polynomial consequences remain valid after scalar
extension.

This is an exact deployed-field proof for the one declared representative,
not a toy-field or asymptotic experiment. It does not use the full quotient
identities or the endpoint coefficients of the degree-30 `H` products: the
four q-slice equations already delete its balanced pattern.

## 6. Replay

Run:

```bash
python3 experimental/scripts/verify_kb_mca_v4_m2_diagonal_112_fixed_positive_balanced_v1.py \
  --check --tamper-selftest
/usr/local/bin/sage \
  experimental/scripts/verify_kb_mca_v4_m2_diagonal_112_fixed_positive_balanced_v1.sage
Singular -q \
  experimental/scripts/verify_kb_mca_v4_m2_diagonal_112_fixed_positive_balanced_v1.sing
"/Applications/Wolfram Engine.app/Contents/Resources/Wolfram Player.app/Contents/MacOS/WolframKernel" \
  -script experimental/scripts/verify_kb_mca_v4_m2_diagonal_112_fixed_positive_balanced_v1.wl
```

On the July 30 local image, `/usr/local/bin/sage` points into a damaged
Sage app wrapper whose `build/bin/sage-site` target is absent. The same
Sage 10.9 installation replays exactly through its intact embedded Python
and preparser:

```bash
env HOME=/private/tmp/rs_mca_sage_home \
  /Applications/SageMath-10-9.app/Contents/Frameworks/Sage.framework/Versions/10.9/local/bin/python3 \
  -c 'from sage.all_cmdline import *; from sage.repl.preparse import preparse_file; import pathlib; path=pathlib.Path("experimental/scripts/verify_kb_mca_v4_m2_diagonal_112_fixed_positive_balanced_v1.sage"); exec(preparse_file(path.read_text()), globals())'
```

The Python verifier rejects duplicate JSON keys, enforces canonical bytes
and the pinned payload, binds the exact source-facet parent and repaired
same-representative immediate-predecessor blobs and payload, binds all three
CAS scripts, checks the representative-only assignment scope and the
complete factor partition including `w^2-cd`, and fail-closes full-orbit,
covariance, and other-seven-closed overclaims through 77 semantic mutations.
Optimized Python is refused.

The Singular replay independently checks the repaired `cd=w^2` unit ideal
and the two support-square reductions. The local Wolfram replay consumes
the same explicit integer polynomials but independently recomputes both
Groebner certificates with the Wolfram engine.

## 7. Nonclaims

Not proved:

- the balanced `(1,1)` system for the other seven fixed-moving assignments;
- the crossed `(0,2)` or identity `(2,0)` systems for the other seven
  fixed-moving assignments;
- projective covariance of the complete source system;
- any moving-moving or near-aligned positive pattern;
- the exceptional unsaturated orbit or biquadratic source-cover branch;
- deletion of the complete `(1,1,2)` row;
- an owner, payment, K3 value, KoalaBear row bound, or Prize closure.
