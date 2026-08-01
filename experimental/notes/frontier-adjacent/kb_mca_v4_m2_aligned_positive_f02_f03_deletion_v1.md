---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
atom_or_cell: K3_M2_DIAGONAL_112_ALIGNED_POSITIVE_F02_F03
quantifier: all three aligned-positive residual-root targets for the literal F02 source assignment and its exact full-source b-inversion partner F03
projection_and_unit: factor-first localized q-slice ideals over GF(2130706433), followed by an exact GF(p^2) point census and full J/I quotient checks on the two nonunit q-slice schemes
claimed_bound: F02 and F03 contribute no aligned-positive (1,1,2) solutions
status: GREEN_PROVED_EXACT_LOCAL_LEMMA_K3_OPEN
impact: deletes six of the thirty-six atlas cells; no owner, charge, or ledger movement
falsifier: a missing factor branch, a localized nonunit branch outside the recorded lex schemes, a full quotient identity holding at a recorded point, a zero mismatch norm, or failure of literal full-source b-inversion
replay: sage experimental/scripts/compile_kb_mca_v4_m2_aligned_positive_f02_f03_deletion_v1.sage --check && python3 experimental/scripts/verify_kb_mca_v4_m2_aligned_positive_f02_f03_deletion_v1.py --check --tamper-selftest
---

# Exact deletion of the aligned-positive `F02/F03` pair

## 0. Verdict and fence

For the source assignment

```text
F02 = {E01,E12},    E01=(T-2)(T-1/2),    E12=(T-1/2)(T-b),
```

all three aligned-positive q-slice targets are empty:

```text
F02-R02 = EMPTY,    F02-R11 = EMPTY,    F02-R20 = EMPTY.      (0.1)
```

Literal substitution `b -> b^-1` transports the complete source data of
`F02` to `F03={E01,E13}`.  It therefore gives

```text
F03-R02 = EMPTY,    F03-R11 = EMPTY,    F03-R20 = EMPTY.      (0.2)
```

This is a local deletion lemma, not a row closure.  It does not import the
external `F00` representative conclusions, so `F00/F01` remain open in this
packet.  It also leaves `F04`--`F07` and all moving-moving assignments open.
Ledger movement is zero.

## 1. Exact chart and factor-first branches

The packet imports the complete 36-cell source compiler only after binding
its compiler and certificate by raw SHA-256, git-blob SHA-1, and certificate
payload.  It rebuilds `F02` rather than copying stored equations.

The Rabinowitsch chart uses the exact raw product `H` of:

1. the atlas complete-line denominators and reconstruction units;
2. reduced and pairwise-distinct labels
   `J={2,1/2,b,b^-1,c,d}`;
3. the moving-label differences for `w` against `J` and its deck partners.

After taking the radical this is a declared list of 34 factors, of total
degree 43.  The raw product has degree 54 and 34,112 terms.  Each equation is
factored *before* localization, and only factors literally present in that
declared list are removed.

For `R02` and `R20`, the constant equations at `c` and `d` each have two
residual factors.  Thus the compiler checks the complete `2 x 2` Cartesian
branch set.  In each cell only branch `(0,0)` survives the q-slice ideal; the
other three branches have localized Groebner basis `[1]`.

For `R11`, each constant equation has one residual factor.  The unique
localized branch has Groebner basis `[1]`, so

```text
F02-R11 = EMPTY_LOCALIZED_QSLICE.                           (1.1)
```

No generic saturation is used.

## 2. The two exact survivor censuses

The `R02` survivor has lexicographic leading monomials

```text
tt, b, c, d^2, w^2.
```

Its quotient dimension is four.  The `w` eliminant is the irreducible
quadratic

```text
w^2 + 940017546*w + 1.                                    (2.1)
```

Consequently its four geometric points all lie in `GF(p^2)`, hence in the
declared challenge field `GF(p^6)`.

The `R20` survivor has leading monomials

```text
tt, b, c, d^2, w^4.
```

Its quotient dimension is eight, and its reciprocal quartic factors as

```text
(w^2 + 584912723*w + 1)
(w^2 + 1190675975*w + 1).                                 (2.2)
```

Both factors are irreducible over `GF(p)`.  Each supplies four exact
`GF(p^2)` points, for eight total.  The certificate stores all point
coordinates in the corresponding quadratic basis and re-evaluates the five
branch generators and the full raw localizer at every point.

## 3. Full quotient identities delete every q-slice point

The q-slice equations are necessary but not sufficient.  At every survivor
point the compiler reconstructs the actual rational `U,V,z`, forms

```text
G(T,Y)=U(T,Y)^2-Y*V(T,Y)^2,
```

and tests both complete projective quotient identities:

```text
prod_{x in J} G(x,Y)       proportional to L_K(Y)^4 q(Y)^2,
q(Y)^2 prod_{x in I}G(x,Y) proportional to L_R(Y)^4.        (3.1)
```

The first projective mismatch occurs at coefficient one.  Modulo each
quadratic `w^2+a*w+1`, the mismatch is `A*w+B`; its norm is

```text
N(A*w+B)=B^2-aAB+A^2.                                      (3.2)
```

The exact nonzero records are:

| Target | `a` | identity | `A` | `B` | norm |
|---|---:|---|---:|---:|---:|
| `R02` | 940017546 | `J` | 317112865 | 1161791022 | 627736383 |
| `R02` | 940017546 | `I` | 462252474 | 145305698 | 1796550960 |
| `R20` | 584912723 | `J` | 1671616282 | 297746731 | 555560394 |
| `R20` | 584912723 | `I` | 134663927 | 1672091025 | 1334100861 |
| `R20` | 1190675975 | `J` | 309729886 | 1997957961 | 2008265187 |
| `R20` | 1190675975 | `I` | 1042061214 | 2038553966 | 1196113770 |

Each remainder is uniform over the two `d` roots and the two conjugate `w`
roots of its component.  Since every norm is nonzero, neither identity can
hold at any survivor point.  Hence

```text
F02-R02 = EMPTY_FULL_SOURCE,
F02-R20 = EMPTY_FULL_SOURCE.                               (3.3)
```

## 4. Literal full-source inversion

For every one of the twelve atlas assignments the compiler independently
rebuilds `U,V,z` and substitutes `b -> b^-1` coefficientwise.  It proves the
declared map

```text
F00 <-> F01,   F02 <-> F03,   F04 <-> F05,   F06 <-> F07,
M01 <-> M02,   M00 -> M00,    M03 -> M03.                  (4.1)
```

The pullback fixes `V` and transports `z` exactly.  It transports `U`
exactly on the paired assignments and negates `U` on the two fixed
assignments `M00,M03`; in either case `G=U^2-WV^2` is exact.  The full
`J,I,K,R` label-factor multisets also transport exactly, so both identities
in (3.1) transport factor by factor.

Only the implication `F02 empty => F03 empty` is used in this packet.
Equation (4.1) is a literal source identity, not a Möbius covariance theorem,
and no other deletion conclusion is imported.

## 5. Evidence level and replay

The Sage compiler is load-bearing: it derives the factors, computes all nine
localized Groebner bases, constructs the lex schemes, enumerates every
quadratic-field point, and evaluates both complete quotient identities.

The independent Python verifier binds all inputs, replays the norm formula,
checks branch/component/point coverage and the twelve literal-transport
records, and rejects semantic mutations under both normal and optimized
Python.  A fresh reviewer independently replayed Sage and both Python modes,
audited the complete 34-factor open, checked the exact `F02 -> F03`
localizer transport, and returned `GREEN` for this local lemma.

K3 remains open.
