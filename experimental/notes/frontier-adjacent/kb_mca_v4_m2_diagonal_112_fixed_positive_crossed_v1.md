---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
atom_or_cell: K3_M2_DIAGONAL_112_FIXED_POSITIVE_CROSSED_0_2_REPRESENTATIVE
quantifier: the single normalized saturated source-line representative J_0={2,1/2,b,1/b}, J_1={c,d}, with fixed-moving assignment {{2,1/2},{2,b}} and crossed root distribution (0,2)
projection_and_unit: exact source-facet reconstruction and full quotient identities in the deployed characteristic; not an owner or payment
claimed_bound: this normalized fixed-moving crossed (0,2) representative is empty
status: PROVED_REPRESENTATIVE_ONLY_OTHER_SEVEN_FIXED_MOVING_ASSIGNMENTS_OPEN_SEPARATE_EXACT_SYSTEMS_COVARIANCE_NOT_CLAIMED_K3_OPEN
impact: removes one normalized fixed-moving aligned-positive crossed representative; ledger movement zero
falsifier: an admissible reconstruction in the declared normalized representative surviving both full quotient identities
replay: python3 experimental/scripts/verify_kb_mca_v4_m2_diagonal_112_fixed_positive_crossed_v1.py --check --tamper-selftest
---

# KoalaBear diagonal `(1,1,2)` fixed-positive crossed representative deletion

## 0. Verdict

For the exact normalization

```text
J_0={2,1/2,b,1/b},  J_1={c,d},
assignment={{2,1/2},{2,b}},
```

the fixed-moving aligned-positive source-line system with crossed residual
root distribution

```text
at c: (W-1/d)^2,        at d: (W-1/c)^2             (0.1)
```

is empty. This is one normalized representative, not the complete
fixed-moving assignment class.

The other seven fixed-moving assignments are
`OPEN_SEPARATE_EXACT_SYSTEMS`. Complete-system projective covariance is
`NOT_CLAIMED`: acting only on endpoint labels preserves the observed
residual side but not the aligned target, while applying the corresponding
diagonal transport to the `W` coordinate preserves the target but not the
observed residual/source `W` divisor. Thus neither action transports the
whole source system proved below.

This is also only the multiplicity pattern `(0,2)`. The identity-doubled
pattern `(2,0)` and balanced pattern `(1,1)` are separate equation systems
and remain open. Moving-moving templates, near-aligned positive templates,
the exceptional branches, the complete `(1,1,2)` row, and K3 also remain
open. No owner or charge is booked.

## 1. Imported interface and exact reconstruction

Use the saturated source-line interface of the universal source-facet
census at commit
`c2edcfa5cbfb8a41e7dea04ae1b34325c90ed5dc`, especially equations
(9.17)--(9.24). Normalize

```text
tau(x)=1/x,
J_0={2,1/2,b,1/b},
J_1={c,d}.
```

Fix the single internal assignment

```text
{2,1/2}, {2,b}.                                      (1.1)
```

The exact Sage replay rebuilds the positive reciprocal source form

```text
G(T,W)=U(T,W)^2-WV(T,W)^2
```

from the parent five-row reconstruction system. It then divides the slices
at `c` and `d` by the proved forced-square factor `(W-w)^2` and imposes the
two projective quadratic conditions (0.1). No numerical interpolation is
used.

The constant projective equation at each of `c` and `d` has exactly two
primitive factors linear in `b`. Hence there are four ordinary factor
branches, indexed by

```text
(c_choice,d_choice) in {0,1}^2.                     (1.2)
```

The subsequent reductions use two linear solves, first for `b` and then
for `w`. Section 2 checks the coefficient-zero charts before either
division.

## 2. Degenerate linear charts

Put

```text
E1=4cdw-cd-2cw-2dw+2c+2d+w-4,
E2=cdw-4cd-2cw-2dw+2c+2d+4w-1,
A =5cd-4c-4d+5,

Hbasic=bcdw E1 E2 (b-1)(b+1)(c-1)(c+1)(d-1)(d+1)
       (w-1)(w+1) A (cd-1)(b-2).                   (2.1)
```

These are named incidence, fixed-point, distinct-label, and reconstruction
units on the retained parent chart. This localizer is smaller than the
product of all parent label differences, so emptiness after inverting it is
a stronger check than emptiness only on the full parent open set.

For a selected `c` factor write

```text
F_c=A_c b+C_c.
```

The Sage replay forms, for every pair in (1.2), the exact ideal containing

```text
A_c, C_c, F_d, the second c equation, the second d equation,
t H-1,                                                   (2.2)
```

where `H=Hbasic`, with the additional known unit `d-w` on `c_choice=0`.
All four localized Groebner bases over `GF(2130706433)` are `[1]`.
Therefore no candidate is lost by solving the selected `c` factor for
`b`.

On `c_choice=1`, the retained factor after substituting `b` is linear in
`w`; write it as

```text
F_w=A_w w+C_w.
```

For each of the two `d` choices, the replay similarly imposes
`A_w=C_w=0`, the remaining equations, and a Rabinowitsch equation. Its
localizer is substituted `Hbasic` times the nonzero `b` coefficient and
every denominator introduced by that substitution. Both exact localized
Groebner bases are `[1]`. Thus solving for `w` is also exhaustive.

These are six finite named localizations, not a generic saturation.

## 3. The three ordinary terminals

### 3.1 `c_choice=0`

After solving its linear `b` factor, the second projective equation at `c`
is exactly

```text
d (w-d)^2 (w-1)^2 (w+1)^2 (d-2)^2 (2d-1)^2
  (c-1)^2 (c+1)^2 A^2 (cd-1)^4.                   (3.1)
```

Every factor is a declared unit on this branch. Equation (3.1) is therefore
nonzero and deletes both `d` choices.

### 3.2 H8: `c_choice=1,d_choice=0`

After solving for `w`, the second reduced equation factors, up to parent
units, through

```text
(c+d)^2.                                            (3.2)
```

Thus a surviving point would have `d=-c`. On this divisor the exact
numerator and denominator of the solved value of `w` are

```text
w_num=10c^2(c-1),       w_den=10c(c-1).             (3.3)
```

The parent units make the denominator nonzero, and (3.3) gives `w=c`.
This is a forbidden source-label collision. Hence H8 is empty.

### 3.3 H9: `c_choice=1,d_choice=1`

After removing only the displayed parent units, H9 is the two-equation
system

```text
e0 =
 4c^2d^4-120c^2d^3+8cd^4+193c^2d^2+120cd^3+4d^4
 -84c^2d-262cd^2-84d^3+4c^2+120cd+193d^2+8c-120d+4,

e1 =
 4c^4d^2+8c^4d-120c^3d^2+4c^4+120c^3d+193c^2d^2
 -84c^3-262c^2d-84cd^2+193c^2+120cd+4d^2-120c+8d+4.
                                                               (3.4)
```

Let `p=2130706433`. A native lexicographic Groebner basis of
`(e0,e1)` over `GF(p)` has three elements. Its pure-`c` eliminant is, up to
a nonzero scalar,

```text
(2c-1)^3 (c-2)^3 q2(c) q6(c) h(c),                (3.5)

q2=c^2-14c+1,
q6=4c^6-112c^5+317c^4-430c^3+317c^2-112c+4,
h =100c^4-504c^3+817c^2-504c+100.
```

The two linear factors are fixed-label collisions. Reduction in the
component ideals gives

```text
q2=0  => cd=1,          q6=0 => d=c,                (3.6)
```

so these are reciprocal-label and equal-label collisions.

On the remaining component,

```text
h=0,
375d-1600c^3+6664c^2-7241c+1400=0.                (3.7)
```

The Sage replay reconstructs the complete quotient expressions from the
source form, not merely the `J_1`-slice prefilter (9.24). For each of the
two identities in (9.18), its coefficient-one proportionality minor is a
cubic `m_I` or `m_J`. Exact extended Euclidean witnesses prove

```text
gcd(h,m_I)=gcd(h,m_J)=1 in GF(p)[c].                (3.8)
```

The certificate records every coefficient of both mismatches and both
Bezout pairs. Thus neither full quotient identity can hold at a point of
the `h` component. H9 is empty.

For an additional native-field check,

```text
h=100(c^2+272520209c+1210481498)
     (c^2+1602501447c+1516822740) mod p.            (3.9)
```

The pure-Python verifier substitutes the relations in (3.6)--(3.7) back
into both equations (3.4), multiplies (3.9), and replays both Bezout
identities with independent exact modular polynomial arithmetic.

## 4. Characteristic and theorem scope

The reconstruction, projective equations, factorizations (3.1)--(3.4), and
H8 collision are derived over `QQ` as cleared-denominator polynomial
identities. The six coefficient-zero charts and the H9 component
decomposition are then checked natively in the deployed characteristic
`p=2130706433`. The challenge field is the degree-six extension of this
prime field, so a unit ideal, collision identity, or Bezout unit over
`GF(p)` remains such after scalar extension.

This argument is therefore an exact deployed-field deletion. It is not an
asymptotic argument and contains no sampled or toy-field evidence.

The apparent relabeling `c<->d` does not turn this theorem into a proof for
the `(2,0)` system. That swap also transports the target polynomial and
preserves whether the `J_1`-to-`tau(J_1)` matching is crossed or identity.
The `(2,0)` and `(1,1)` equations must be audited separately.

Nor does a normalizer of the endpoint deck action close the other seven
fixed-moving assignments. Endpoint-only transport preserves the observed
residual side but does not preserve the aligned target. Diagonal transport
of endpoints together with `W` preserves the target but changes the
observed residual/source `W` divisor. A covariance theorem for the complete
source system would need one action preserving both sides, and no such
action is proved here. Each of the other seven assignments therefore
requires its own exact system.

## 5. Replay and nonclaims

Run:

```bash
python3 experimental/scripts/verify_kb_mca_v4_m2_diagonal_112_fixed_positive_crossed_v1.py \
  --check --tamper-selftest
/usr/local/bin/sage \
  experimental/scripts/verify_kb_mca_v4_m2_diagonal_112_fixed_positive_crossed_v1.sage
Singular \
  experimental/scripts/verify_kb_mca_v4_m2_diagonal_112_fixed_positive_crossed_v1.sing
"/Applications/Wolfram Engine.app/Contents/Resources/Wolfram Player.app/Contents/MacOS/WolframKernel" \
  -script experimental/scripts/verify_kb_mca_v4_m2_diagonal_112_fixed_positive_crossed_v1.wl
```

The Python verifier rejects duplicate JSON keys, enforces canonical bytes
and the payload hash, binds the exact source-facet parent and predecessor
blobs, binds all three CAS scripts, performs the exact modular component
and quotient checks, and fail-closes against full-orbit, covariance, and
seven-assignment-closure mutations. Optimized Python is refused.

Not proved:

- any of the other seven fixed-moving assignments;
- projective covariance of the complete source system;
- the fixed-moving identity-doubled `(2,0)` pattern;
- the fixed-moving balanced `(1,1)` pattern;
- any moving-moving or near-aligned positive pattern;
- the exceptional unsaturated orbit or biquadratic source-cover branch;
- deletion of the complete `(1,1,2)` row;
- an owner, payment, K3 value, KoalaBear row bound, or Prize closure.
