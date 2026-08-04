---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
atom_or_cell: K3_M2_DIAGONAL_112_ALIGNED_POSITIVE_FIXED_MOVING
quantifier: all eighteen fixed-moving aligned-positive atlas cells on their declared named opens
projection_and_unit: exact q-slice schemes over GF(2130706433), with geometric empty-localization conclusions extending to GF(p^6)
claimed_bound: two balanced cells are empty; twelve literal high-complexity cells admit an exact six-orbit quadratic compatibility/rank dichotomy; sixteen cells remain open
status: PROVED_EXACT_LOCAL_LEMMA_REVIEW_REQUIRED_K3_OPEN
impact: aligned-positive frontier 18 -> 16; no owner, charge, or ledger movement
falsifier: a surviving point in F00-R11 or F01-R11 on the named open; a mismatched literal-cell census; failure of the quadratic resultant identity; a discarded V=0 component; or an orbit pairing with unequal exact fingerprints
replay: sage experimental/scripts/compile_kb_mca_v4_m2_aligned_positive_fixed_frontier_v1.sage --check --summary
---

# Aligned-positive fixed-moving closure and quadratic route cut

## 0. Verdict

This packet attacks the complete eighteen-cell frontier left by the moving
closure packet:

```text
F00,F01,F04,F05,F06,F07 x R02,R11,R20.
```

It proves exact named-open emptiness for

```text
F00-R11, F01-R11,
```

and retains the four literal two-dimensional q-slice schemes

```text
F00-R02, F00-R20, F01-R02, F01-R20.
```

For the other twelve cells it replaces an unbounded four-variable Groebner
attempt by a division-safe quadratic compatibility/rank dichotomy. Direct
literal compilation collapses those twelve cells to six exact fingerprint
orbits. This is a route cut, not an emptiness theorem for those cells.

The aligned-positive frontier therefore moves exactly

```text
18 open cells -> 2 empty + 16 open cells.
```

No owner, charge, K3 value, or KoalaBear row bound moves.

## 1. Upstream alignment

The live upstream board still identifies KoalaBear MCA at agreement
`1116048` as the primary unresolved row. PR #1143 now closes the complete
positive coordinate route `433-1a -> O0b` and role cell 14 of `433-1b ->
O0a`; its newest workboard instruction asks for the six aligned-positive
unramified cells. The `F00/F01` six-cell block is attacked here literally,
closing its two balanced cells and retaining the four crossed/identity
schemes.

PR #1148 is an exact affine-hull rigidity theorem for a punctured M31
fixture. It does not supply the missing containment theorem needed to apply
that hull classification here. PR #1147's cubic/product-line reduction is
also a different row, but its factor-before-elimination discipline supports
the quadratic compression used below. Neither PR is imported as a theorem.

PR #1144 remains mergeable and ready but is stacked on the still-open K3
dependency chain; this packet is a child of its exact eighteen-cell fence.

## 2. The two exact deletions

The compiler rebuilds all six `F00/F01` q-slice systems from the pinned
36-cell atlas, factors before localization, and uses only the declared named
units. Both `R11` full charts have two-dimensional raw q-slice ideals, but
the named localizer is nilpotent of exact index three. Hence their named-open
schemes are empty. Their exact full-basis fingerprints are

```text
F00-R11: dimension 2, size 127,
  sha256 64b31d79d37d777d49f10100d523e0b3ad05957aa7ed659a16b4f698aaef7f81
F01-R11: dimension 2, size 127,
  sha256 d91e61d31f513231173e66a12888ed6feb8345741bf588b4c8341ea7fa82ed8c.
```

The other four named-open schemes survive with dimension two. They are not
promoted to witnesses and are not forced into an owner.

## 3. Uniform quadratic compatibility lemma

For every literal cell in the `F04/F05/F06/F07` block, the first two
q-slice equations are quadratics in `w`:

```text
P=A w^2+B w+C,       Q=D w^2+E w+F.
```

Define

```text
U=AF-CD,   V=AE-BD,   Z=BF-CE.
```

Exact expansion gives

```text
Res_w(P,Q)=U^2-VZ,                                  (3.1)
D P-A Q=-(Vw+U).                                    (3.2)
```

Thus the branch `V!=0` has the unique reconstructed common root

```text
w=-U/V                                               (3.3)
```

and compatibility `U^2-VZ=0`. This reconstruction is sufficient, not merely
necessary: the identities

```text
V^2 P(-U/V)=A(U^2-VZ),
V^2 Q(-U/V)=D(U^2-VZ)
```

follow because `AZ-BU+CV=0` identically. The two remaining quartics may
therefore be substituted at (3.3), clearing exactly `V^4`.

The rank-drop branch `V=0` is retained. Any common quadratic root on that
branch also forces `U=0` by (3.2), but this packet does not divide by a
leading coefficient, discard degree drops, or claim the `U=V=0` component
empty.

Sage independently computes (3.1) directly and through the compressed
formula over `QQ`; Wolfram Language returned zero for all five generic
identities (3.1), (3.2), the two reconstructed evaluations, and
`AZ-BU+CV`. The Wolfram replay is an independent symbolic check, not the
source of the cell-specific fingerprints.

## 4. Exact six-orbit residual

All twelve literal cells compile successfully. Exact factor and resultant
hashes pair them as

```text
F04-R02 = F07-R02       F05-R02 = F06-R02
F04-R11 = F07-R11       F05-R11 = F06-R11
F04-R20 = F07-R20       F05-R20 = F06-R20.
```

The `R02/R20` resultants have total degree 42 and 3,679 terms; the balanced
`R11` resultants have total degree 38 and 2,464 terms. The complete hashes
of the resultants and the last nontrivial `U,V,Z` factors are sealed in the
JSON certificate. This six-orbit equality is observed by direct literal
reconstruction of every cell, not assumed from endpoint covariance.

An attempted monolithic four-variable localization for `F04-R02` remained
inside Singular after several minutes. The generic three-variable
substitution also remained inside a high-degree Groebner computation. These
failed routes are not evidence of a survivor or emptiness; the packet banks
only the exact compression and keeps both generic and rank-drop components.

## 5. Evidence level and next attack

**Proved:** the two named-open deletions; the complete eighteen-cell census;
the exact quadratic resultant/reconstruction lemma; the twelve literal
compressions; and their six fingerprint orbits.

**Not proved:** emptiness of the other sixteen cells, an owner/payment, the
aligned-positive orientation, K3, or the KoalaBear row.

The next maximal attack is the six-orbit dichotomy, in parallel with the
four smaller survivors:

1. For `F00/F01-R02/R20`, derive the full `J/I` quotient parity equations
   and test them against the existing two-dimensional bases.
2. For each of the six quadratic orbits, factor only the three high-degree
   `U,V,Z` cores after removing declared named units.
3. On `V!=0`, substitute `w=-U/V` into the two remaining quartics and use a
   regular chain or block elimination in the three base variables.
4. On `V=0`, impose `U=0` and split every actual leading-coefficient degree
   drop. Every component must end empty, in a named same-record owner, or as
   an explicit primitive route.

Do not retry the raw monolithic four-variable basis, use generic saturation,
or silently discard the `V=0` branch.
