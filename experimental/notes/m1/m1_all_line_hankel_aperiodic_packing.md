# M1 All-Line Hankel Aperiodic Packing Target

## Status

PROVED finite normal form / AUDIT verifier / NOT the final M1 theorem.

This note records the first M1 packet following the maintainer target:

```text
#{z : exists an aperiodic split locator T} <= n^B
```

after tangent/contained and quotient-periodic locator classes are charged.
It uses the Hankel-pencil normal form from `experimental/experiments.tex`.

## Set-Up

Let `F` be a finite field, let `D subset F` have size `n`, and let
`C=RS[F,D,k]`.  Put

```text
r=n-k,        j+t=r,        a=k+t=n-j.
```

For a line `(f,g):D->F^2`, write

```text
u=Syn(f),        v=Syn(g),
```

using the usual RS parity-check syndrome.  For each `j`-point complement
`T subset D`, let

```text
L_T(X)=prod_{x in T}(X-x),
ell_T=(ell_0,...,ell_j)^T
```

be its monic locator vector.  The Hankel-pencil test says that a finite slope
`z` is explained on `S=D\T` if and only if

```text
(H_{t,j}(u)+zH_{t,j}(v)) ell_T = 0.        (1)
```

It is support-wise noncontained on that support if and only if

```text
H_{t,j}(v) ell_T != 0.                      (2)
```

## Charged/Aperiodic Split-Locator Ledger

For fixed `(f,g,t,j)`, define `Bad(T)` to mean that `T` is a split complement
whose locator satisfies (1) for some slope and satisfies (2).  When this holds,
the slope is unique unless the whole vector `H(v)ell_T` vanishes, which is
exactly the contained/tangent-core class removed by (2).

When `D=H` is a cyclic multiplicative subgroup, a split complement `T` is
called whole-fiber quotient-periodic at scale `m|n`, `1<m<n`, if it is a union
of cosets of the subgroup of `H` of size `m`.  Let `QP(T)` mean that this
holds for at least one charged scale.

The finite all-line slope ledger is therefore the disjoint accounting

```text
Bad slopes
  = charged quotient-periodic slope image
    union aperiodic slope image,

AperSlope(f,g;t,j)
  = { z_T : Bad(T) and not QP(T) }.
```

The maintainer target is to prove a polynomial bound for this last image,
uniformly in the line `(f,g)`, after the tangent/contained and
quotient-periodic ledgers have been paid.

## Exactness Lemma

The ledger above is exact for every finite instance.

1. The Hankel-pencil theorem gives equivalence between support-wise line
   incidence and the existence of a split locator satisfying (1).
2. Condition (2) is exactly the noncontainment condition on the same support,
   so contained/tangent-core locators are removed before aperiodicity is
   counted.
3. The quotient-periodic predicate depends only on the support complement and
   the selected quotient scales, so charging it before taking slope images
   cannot create or remove aperiodic locators.
4. Every remaining bad locator contributes the unique slope forced by
   `H(u)ell_T + zH(v)ell_T=0`, and the set of these slopes is precisely
   `AperSlope(f,g;t,j)`.

Thus the residual M1 problem is no longer a question about support-wise MCA
definitions.  It is the slope image of the aperiodic split-locator incidence
inside the Hankel pencil.

## Verifier

The companion verifier

```bash
python3 experimental/scripts/verify_m1_all_line_hankel_aperiodic.py
```

enumerates small cyclic-domain cases.  For each case it:

- computes syndromes and Hankel windows for a deterministic family of all-line
  words;
- enumerates all split complements `T`;
- applies the projective slope gate for `t=2`;
- cross-checks every bad slope by direct RS interpolation on `D\T`;
- labels whole-fiber quotient-periodic complements at the selected scales;
- reports the aperiodic slope image after charged locators are removed.

The default audit currently checks three cyclic-domain parameter rows and
twelve deterministic line samples.  The largest observed residual aperiodic
slope image in this smoke packet has size `16`, after direct interpolation
checks on every reported support-wise bad slope.

This is an audit/verifier for the M1 target, not a proof of the desired
polynomial all-line bound.  Its purpose is to make future counterexample-first
work precise: a claimed obstruction should now say whether its split locators
are contained/tangent, quotient-periodic, or genuinely aperiodic in this
Hankel-pencil ledger.
