---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
atom_or_cell: K3_M2_DIAGONAL_112_FIXED_POSITIVE_IDENTITY_2_0_REPRESENTATIVE
quantifier: the single normalized saturated source-line representative J_0={2,1/2,b,1/b}, J_1={c,d}, with fixed-moving assignment {{2,1/2},{2,b}} and identity-doubled root distribution (2,0)
projection_and_unit: exact source-facet reconstruction and full quotient identities in the deployed characteristic; not an owner or payment
claimed_bound: this normalized fixed-moving identity-doubled (2,0) representative is empty
status: PROVED_REPRESENTATIVE_ONLY_OTHER_SEVEN_FIXED_MOVING_ASSIGNMENTS_OPEN_SEPARATE_EXACT_SYSTEMS_COVARIANCE_NOT_CLAIMED_K3_OPEN
impact: removes one normalized fixed-moving aligned-positive identity-doubled representative; ledger movement zero
falsifier: an admissible reconstruction in the declared normalized representative surviving both full quotient identities
replay: python3 experimental/scripts/verify_kb_mca_v4_m2_diagonal_112_fixed_positive_identity_v1.py --check --tamper-selftest
---

# KoalaBear diagonal `(1,1,2)` fixed-positive identity representative deletion

## 0. Verdict

For the exact normalization

```text
J_0={2,1/2,b,1/b},  J_1={c,d},
assignment={{2,1/2},{2,b}},
```

the fixed-moving aligned-positive source-line system with identity-doubled
residual root distribution

```text
at c: (W-1/c)^2,        at d: (W-1/d)^2             (0.1)
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

This is also only multiplicity pattern `(2,0)`. For this same representative,
the crossed `(0,2)` pattern is deleted by the exact predecessor packet. The
other seven crossed systems and all eight balanced `(1,1)` systems remain
separate and open. Moving-moving templates, near-aligned positive templates,
the exceptional branches, the complete `(1,1,2)` row, and K3 also remain
open. No owner or charge is booked.

## 1. Imported interface and exact reconstruction

Use the saturated source-line interface of the universal source-facet census
at commit `c2edcfa5cbfb8a41e7dea04ae1b34325c90ed5dc`, especially equations
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

The Sage replay rebuilds

```text
G(T,W)=U(T,W)^2-WV(T,W)^2
```

over `QQ` from the parent five-row reconstruction system. It divides the
slices at `c` and `d` by the proved forced square `(W-w)^2` and imposes the
two projective quadratic conditions (0.1). No numerical interpolation is
used.

The constant projective equation at each of `c` and `d` has exactly two
primitive factors linear in `b`. Thus there are four ordinary branches

```text
(c_choice,d_choice) in {0,1}^2.                     (1.2)
```

The subsequent reductions solve first for `b` and, on `c_choice=1`, for
`w`. Section 2 checks all coefficient-zero charts before either division.

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
units on the retained parent chart. The parent also makes `c-w` a
distinct-label unit.

For a selected `c` factor write

```text
F_c=A_c b+C_c.
```

For every pair in (1.2), the replay imposes

```text
A_c, C_c, F_d, the second c equation, the second d equation,
t H-1.                                               (2.2)
```

Here `H=Hbasic`, with the additional declared unit `c-w` on
`c_choice=0`. All four localized Groebner bases over
`GF(2130706433)` are `[1]`. Hence solving the selected `c` factor for `b`
loses no admissible point.

On `c_choice=1`, the retained substituted `d` factor is linear in `w`;
write it as `F_w=A_w w+C_w`. For each `d` choice the replay imposes
`A_w=C_w=0`, the remaining equations, and a Rabinowitsch equation. The
localizer is substituted `Hbasic` times the nonzero `b` coefficient and all
introduced denominators. Both exact localized Groebner bases are `[1]`.

These are six finite named localizations, not a generic saturation.

## 3. Ordinary terminals

### 3.1 `c_choice=0`

After solving the selected linear `b` factor, the second projective equation
at `c` is exactly

```text
c (w-c)^2 (w-1)^2 (w+1)^2 (d-2)^2 (2d-1)^2
  (c-1)^2 (c+1)^2 A^2 (cd-1)^4.                    (3.1)
```

Every factor is a declared unit. Equation (3.1) deletes both `d` choices.

### 3.2 `c_choice=1,d_choice=0`

After solving for `w`, one reduced equation has, besides declared units, the
factor

```text
(c+d)^2.                                             (3.2)
```

Thus a survivor would have `d=-c`. Direct substitution into the exact
solved value of `b` gives

```text
b=1/2,                                               (3.3)
```

with its denominator nonzero on the named ordinary chart. This is a fixed
label collision, so the branch is empty.

### 3.3 `c_choice=1,d_choice=1`

After removing only displayed parent units, the two terminal polynomials
are

```text
E0 =
 36c^6d^4-180c^6d^3-172c^5d^4+297c^6d^2+920c^5d^3
 +524c^4d^4-180c^6d-1698c^5d^2-2428c^4d^3-960c^3d^4
 +36c^6+1256c^5d+4071c^4d^2+3648c^3d^3+860c^2d^4
 -328c^5-3052c^4d-5364c^3d^2-3052c^2d^3-328cd^4
 +860c^4+3648c^3d+4071c^2d^2+1256cd^3+36d^4
 -960c^3-2428c^2d-1698cd^2-180d^3+524c^2+920cd
 +297d^2-172c-180d+36,

E1 = E0(d,c).                                        (3.4)
```

Their exact characteristic-zero resultant is

```text
Res_d(E0,E1)
 = 3^20 (c-2)^4 (2c-1)^4 (c-1)^10 (c+1)^10
   f6(c) f8(c) f10(c),                               (3.5)
```

where

```text
f6 = 9c^6-82c^5+119c^4-156c^3+119c^2-82c+9,

f8 = 324c^8-5328c^7+29617c^6-77552c^5+106134c^4
     -77552c^3+29617c^2-5328c+324,

f10= 36c^10-352c^9+1741c^8-5266c^7+9871c^6
     -12124c^5+9871c^4-5266c^3+1741c^2-352c+36.
                                                               (3.6)
```

The four displayed linear factors are fixed-label or deck-fixed-point
collisions. Native Groebner reductions over `GF(p)`, `p=2130706433`, give

```text
f6=0  => cd=1 and w=1,
f10=0 => d=c.                                        (3.7)
```

Thus `f6` and `f10` are inadmissible.

The `f8` component has a two-element lexicographic basis, including one
relation linear in `d`; hence it contains no unclassified `d` branch. The
Sage replay reconstructs the complete quotient expressions from the source
form, not merely the `J_1`-slice prefilter. For each identity in (9.18), its
coefficient-one proportionality minor is a polynomial `m_I` or `m_J`.
The certificate records explicit deployed-field witnesses

```text
u_I f8 + v_I m_I = 1,
u_J f8 + v_J m_J = 1                 in GF(p)[c].     (3.8)
```

Therefore neither full quotient identity can hold on `f8`. This deletes the
last terminal component.

## 4. Characteristic and theorem scope

The reconstruction, projective equations, (3.1)--(3.6), and the half-label
collision are cleared-denominator identities over `QQ`. The six
coefficient-zero charts and component reductions (3.7)--(3.8) are checked
natively in the deployed characteristic. Since the challenge field is the
degree-six extension of this prime field, unit ideals, collision identities,
and Bezout units remain valid after scalar extension.

This is an exact deployed-field deletion. It is not an asymptotic argument
and uses no sampled or toy-field evidence.

The repaired predecessor at commit
`f0a1d20ea16721d9596a3520658406528f5ade9f`, payload
`ec52873035a42fec4c3f19f429913197df872487c2a6137646dd81474c6fedf7`,
deletes the crossed `(0,2)` system for this same normalized representative
only. That fact is provenance, not a symmetry shortcut: this packet
independently derives the representative identity `(2,0)` equations. The
predecessor explicitly leaves its other seven fixed-moving assignments
open and claims no complete-system covariance.

## 5. Replay and nonclaims

Run:

```bash
python3 experimental/scripts/verify_kb_mca_v4_m2_diagonal_112_fixed_positive_identity_v1.py \
  --check --tamper-selftest
/usr/local/bin/sage \
  experimental/scripts/verify_kb_mca_v4_m2_diagonal_112_fixed_positive_identity_v1.sage
Singular -q \
  experimental/scripts/verify_kb_mca_v4_m2_diagonal_112_fixed_positive_identity_v1.sing
"/Applications/Wolfram Engine.app/Contents/Resources/Wolfram Player.app/Contents/MacOS/WolframKernel" \
  -script experimental/scripts/verify_kb_mca_v4_m2_diagonal_112_fixed_positive_identity_v1.wl
```

On the July 30 local image, `/usr/local/bin/sage` points into a damaged
Sage app wrapper whose `build/bin/sage-site` target is absent. The same
Sage 10.9 installation replays exactly through its intact embedded Python
and preparser:

```bash
env HOME=/private/tmp/rs_mca_sage_home \
  /Applications/SageMath-10-9.app/Contents/Frameworks/Sage.framework/Versions/10.9/local/bin/python3 \
  -c 'from sage.all_cmdline import *; from sage.repl.preparse import preparse_file; import pathlib; path=pathlib.Path("experimental/scripts/verify_kb_mca_v4_m2_diagonal_112_fixed_positive_identity_v1.sage"); exec(preparse_file(path.read_text()), globals())'
```

The Python verifier rejects duplicate JSON keys, enforces canonical bytes
and the payload hash, binds the exact source-facet parent and repaired
representative-only crossed predecessor blobs, payload, and scope, binds all
three CAS scripts, replays both Bezout identities with independent exact
modular polynomial arithmetic, and fail-closes representative scope,
full-orbit, covariance, closing-seven, and wrong-predecessor-scope
mutations. Optimized Python is refused.

Not proved:

- the other seven fixed-moving identity `(2,0)` systems;
- the other seven fixed-moving crossed `(0,2)` systems;
- complete-system projective covariance;
- any of the eight fixed-moving balanced `(1,1)` systems;
- any moving-moving or near-aligned positive pattern;
- the exceptional unsaturated orbit or biquadratic source-cover branch;
- deletion of the complete `(1,1,2)` row;
- an owner, payment, K3 value, KoalaBear row bound, or Prize closure.
