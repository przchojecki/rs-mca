---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
atom_or_cell: K3_M2_DIAGONAL_112_ALIGNED_POSITIVE_QSLICE_ATLAS
quantifier: all twelve compatible saturated source-line assignments and all three aligned-positive root distributions, as thirty-six separately generated necessary q-slice systems
projection_and_unit: exact source reconstruction and q-slice equation compiler over QQ with deployed-field metadata; not an emptiness theorem, owner, or payment
claimed_bound: none
status: PROVED_EXACT_36_CELL_COMPILER_ALL_CELLS_UNCLASSIFIED_REVIEW_REQUIRED_K3_OPEN
impact: replaces representative-orbit extrapolation by a source-bound exhaustive equation atlas; ledger movement zero
falsifier: a compatible assignment or aligned-positive root distribution absent from the registry, an equation not obtained from the displayed source reconstruction, a failed declared literal symmetry, or a hidden covariance/division
replay: sage experimental/scripts/compile_kb_mca_v4_m2_aligned_positive_qslice_atlas_v1.sage --check && python3 experimental/scripts/verify_kb_mca_v4_m2_aligned_positive_qslice_atlas_v1.py --check --tamper-selftest
---

# KoalaBear aligned-positive `(1,1,2)` q-slice atlas

## 0. Verdict

There are twelve compatible unordered internal source-star assignments and
three aligned-positive residual-root distributions.  This packet generates
all

```text
12 * 3 = 36
```

necessary q-slice systems directly from the parent source reconstruction.
Every cell occurs exactly once and is marked
`UNCLASSIFIED_QSLICE_GENERATED`.

This is the source-bound atlas foundation that the preceding representative
packets did not supply.  It is not an emptiness result: no new cell is paid,
no external theorem is imported, and the ledger movement is zero.  In
particular, the packet rejects both endpoint-only Möbius globalization and
diagonal transport of the `W` coordinate.

## 1. Exact registry

Put

```text
v0=2,       v1=1/2,       v2=b,       v3=b^-1,
Eij=(T-vi)(T-vj).
```

The eight fixed-moving and four moving-moving assignments are

```text
F00 {E01,E02}    F01 {E01,E03}
F02 {E01,E12}    F03 {E01,E13}
F04 {E02,E23}    F05 {E03,E23}
F06 {E12,E23}    F07 {E13,E23}

M00 {E02,E03}    M01 {E02,E12}
M02 {E03,E13}    M03 {E12,E13}.
```

Each pair has exactly one common endpoint.  For each assignment the compiler
uses that actual endpoint in the source incidence equation; it does not
normalize the assignment to `F00` or `M00`.

The three targets are

```text
R02: Qc=(W-1/d)^2,           Qd=(W-1/c)^2,
R11: Qc=Qd=(W-1/c)(W-1/d),
R20: Qc=(W-1/c)^2,           Qd=(W-1/d)^2.
```

Thus a semantic cell is the literal pair `assignment-target`, for example
`F04-R20`.  The JSON contains exactly the Cartesian product of these two
registries.

## 2. Universal positive source reconstruction

Let

```text
q(T)=(T-c)(T-d)=q0+q1*T+T^2,
q0=cd,                     q1=-(c+d),
F=q0-w,                    G=1-w*q0,
M=q1(1-w).
```

The positive reciprocal odd part is

```text
V(T,W)
 = (F+GW) + M(1+W)T + (G+FW)T^2.                  (2.1)
```

If `a` is the common endpoint of the selected source-star pair, write

```text
V(a,W)=N_a+W D_a,          z=-N_a/D_a.             (2.2)
```

The parent finite internal-label chart supplies `D_a!=0`.  At `W=z`, put

```text
l1=[T^2]V(T,z),            l0=[T]V(T,z)+a*l1.
```

For the ordered display `{E(a,r),E(a,s)}` of the unordered pair, the
positive internal target is

```text
P(T)=((l0+s*l1)E(a,r)+(l0+r*l1)E(a,s))/(s-r).      (2.3)
```

Swapping the displayed stars negates (2.3), hence negates `U` and leaves
`U^2-WV^2` unchanged.  This is the first honest symmetry audit.

Write

```text
U(T,W)
 =(x0+x1W+x2W^2)
 +(x3(1+W^2)+x4W)T
 +(x2+x1W+x0W^2)T^2.                               (2.4)
```

Instead of hiding reconstruction in a generic `5 x 5` inverse, the compiler
solves its `3+2` block form explicitly.  If
`P=p0+p1*T+p2*T^2`, set

```text
D0=(p0-p2)/(1-z^2),
R0=p0+p2,
R1=-(1+cd)(1-w^2)D0/(2(1-cd)),
H =w(1+z^2)-z(1+w^2)=(w-z)(1-wz).
```

Then

```text
S =(R0*w-2z*R1)/H,
x1=((1+z^2)R1-(1+w^2)R0/2)/H,
x0=(S+D0)/2,                 x2=(S-D0)/2,
A2=x2+x1*w+x0*w^2,
x3=(p1*w-z*q1*A2)/H,
x4=((1+z^2)q1*A2-(1+w^2)p1)/H.                    (2.5)
```

The only reconstruction units in (2.5) are

```text
1-z^2,        1-cd,        (w-z)(1-wz).             (2.6)
```

They are respectively the internal deck-fixed-point, reciprocal-core, and
forced/internal deck-orbit collision factors.  Their exact numerator and
denominator metrics are recorded separately for each assignment.  Direct
substitution checks both source-line equations at `w` and all three target
coefficients at `z`.

For each root `r` of `q`, the compiler then forms

```text
G(r,W)=U(r,W)^2-WV(r,W)^2
```

and divides exactly by the parent forced square `(W-w)^2`.  The remainder is
asserted to vanish.  Projective proportionality to the selected monic
quadratic target gives two equations at `c` and two at `d`.

Every rational projective equation is cleared by its complete denominator
and one common scalar.  Constant and linear coefficients are never
normalized independently.

## 3. Exact literal symmetries

The compiler proves only these identities:

1. **Star swap/global sign.**  Swapping the two source stars sends
   `P,U` to `-P,-U` and fixes `U^2-WV^2`.
2. **Core-root companion.**  Literal substitution `c<->d` exchanges the
   two pairs of q-slice equations in every one of the 36 cells.
3. **Endpoint inversion.**  After clearing the complete equation and
   removing only a monomial `b` chart unit, literal `b->b^-1` gives

```text
F00 <-> F01,   F02 <-> F03,   F04 <-> F05,   F06 <-> F07,
M01 <-> M02,   M00 -> M00,    M03 -> M03.          (3.1)
```

The equation and localizer pullbacks are checked cell by cell.  On the two
fixed assignments `M00,M03`, the certificate records the even/odd
eigencharacter of every cleared equation in the quotient coordinates

```text
y=b+b^-1,       delta=b-b^-1,       delta^2=y^2-4.  (3.2)
```

Reduction is performed only after the complete projective line has been
cleared.  No factor is divided before its parent provenance is declared.

Neither (3.1) nor any other calculation proves a Möbius orbit theorem.  An
endpoint-only normalizer does not preserve the aligned target, while the
matching diagonal action on `W` does not preserve the observed
source/residual divisor.  The certificate therefore rejects all three
strings

```text
ENDPOINT_ONLY_MOBIUS_ORBIT,
DIAGONAL_W_MOBIUS_ORBIT,
FULL_SOURCE_SYSTEM_COVARIANCE.
```

## 4. External packets are annotations only

Four cells carry exact external provenance:

| Cell | External packet | Atlas treatment |
|---|---|---|
| `F00-R02` | PR #1135 representative deletion | pinned annotation, scope not imported |
| `F00-R20` | PR #1136 representative deletion | pinned annotation, scope not imported |
| `F00-R11` | PR #1137 repaired representative deletion | pinned annotation, scope not imported |
| `M00-R11` | PR #1138 canonical GREEN deletion | pinned annotation, scope not imported |

Each annotation binds an exact commit, certificate blob, raw certificate
SHA-256, and external payload SHA-256.  The atlas remains based only on
parent commit

```text
c2edcfa5cbfb8a41e7dea04ae1b34325c90ed5dc.
```

Consequently all 36 atlas classifications remain
`UNCLASSIFIED_QSLICE_GENERATED`, including the four annotated cells.

## 5. Replay and evidence level

Run the bounded symbolic replay:

```bash
env HOME=/private/tmp/rs_mca_sage_home /usr/local/bin/sage \
  experimental/scripts/compile_kb_mca_v4_m2_aligned_positive_qslice_atlas_v1.sage \
  --check
```

Run the independent exact-rational and mutation replay:

```bash
python3 \
  experimental/scripts/verify_kb_mca_v4_m2_aligned_positive_qslice_atlas_v1.py \
  --check --tamper-selftest
```

Run the independent Wolfram reconstruction:

```bash
'/Applications/Wolfram Engine.app/Contents/Resources/Wolfram Player.app/Contents/MacOS/WolframKernel' \
  -script \
  experimental/scripts/verify_kb_mca_v4_m2_aligned_positive_qslice_atlas_v1.wls
```

The Python verifier reconstructs every assignment at two declared rational
fixtures, performs the forced-square division exactly, and compares all four
projective values in every cell.  It also rejects missing/duplicate cells,
covariance drift, denominator drift, owner-order drift, registry drift,
coefficientwise normalization, imported external scope, and nonzero ledger
movement.  The twenty-five mutations also include false `EMPTY`/paid-owner
terminals, a changed radical localizer set, and independent payload and
external-provenance corruption.  Wolfram independently replays all 72
assignment/target/fixture combinations and 144 literal `c<->d` and
`b<->b^-1` controls.

The polynomial identities and hashes are exact symbolic evidence over
`QQ`; they are not toy-field evidence.  The two rational fixtures are
independent cross-tool controls, not proof of the symbolic identities.
There is no layer-cake, moment, Markov, Chebyshev, asymptotic, or hidden
parameter dependence in this finite algebraic compiler.

## 6. Status and next attack

The atlas compiler is a rigorous foundation, but its mathematical verdict is
YELLOW for K3: all 36 cells still require a first-match classification.
The next maximal attack is bounded and exhaustive:

1. consume the four exact external representative packets only after their
   scopes are repaired and independently audited;
2. quotient by the literal symmetries (3.1), without changing the 36-cell
   semantic registry;
3. derive a first-match factor/component partition for each remaining orbit
   representative;
4. terminate every component in an exact empty chart, a named source-bound
   owner, or an explicit `UNPAID_PRIMITIVE` route cut.

No generic saturation should precede a fixed component equation.  A fresh
reviewer must audit the source reconstruction, cell exhaustivity, and
symmetry/localizer claims before this zero-ledger foundation is promoted.
