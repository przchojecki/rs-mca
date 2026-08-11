# CAP25 v13 near-rational support-mismatch audit

Status: RESOLVED LOCALLY by
`kb_mca_supportwise_near_rational_two_anchor_repair_v1.md`.

This note records a narrow audit finding for the CAP25 v13 raw and compact
spines.  It is not a finite adjacent proof, does not alter the unsafe side, and
does not prove or disprove any deployed row.  Its only purpose is to prevent one
near-rational safe-side reduction from silently replacing support-wise MCA by
ordinary common agreement.

## Source inference under audit

In the raw file, `cor:capfp-line` says that if two finite slopes have
`d_1(u+z_i v) <= w` with nonzero census, then `v` is within distance `2w` and
`u` within distance `3w` of codewords, so the pair has correlated agreement on a
large common support and "no slope is MCA-bad."  The compact file repeats the
same inference in `cor:balanced-core`.

The column-close conclusion is useful.  The final "no MCA-bad slope" conclusion
is too strong for the support-wise MCA predicate unless a separate
support-mismatch/tangent payment is invoked first.

## One-spike counterpacket

Let `C = RS[F,D,K]`, `|D| = n`, and assume `1 <= K <= n-2`.  Choose
`t in D`, and define the received pair

```text
u = 0,
v = 1_{t}.
```

Then `(u,v)` is jointly explained by the codeword pair `(0,0)` on
`D \ {t}`, so it has a common agreement support of size `n-1`.  In particular,
for every band agreement `m <= n-1`, the pair is column-close and has a large
plain correlated-agreement support.

However the finite slope `z = 0` is support-wise MCA-bad on the support
`S = D`.  The line value `u + 0 v = 0` is explained on all of `D` by the zero
codeword.  But `(u,v)` is not jointly explained on all of `D`: if a degree
`< K` polynomial agreed with `v`, it would vanish on `D \ {t}`, which has
`n-1 >= K+1` points, and would also take value `1` at `t`.  This is impossible.

Thus a large common agreement support does not rule out a support-wise MCA-bad
slope on a larger or different support.

## Repaired conclusion

The valid output of the two-low-`d_1` argument is:

```text
(u,v) is column-close/common-proximity to a codeword pair.
```

It is not, by itself:

```text
all support-wise MCA-bad slopes are absent.
```

To delete the near-rational branch from the balanced-core residual, the ledger
must first pay the support-mismatch created by the small error set.  Equivalently,
the reduction needs an explicit first-match priority step:

1. charge tangent/common-proximity support-mismatch slopes;
2. then move the remaining slopes to the balanced-core or split-pencil census.

Without this priority step, the proof can over-delete near-rational lines.

## Consequence for the CAP25 v13 safe side

This is a local source repair, not a new obstruction to the whole program.  In
the historical CAP25 v13 additive template, the finite adjacent target depends
on Q/BC/SP and a first-match upper ledger; there the near-rational column-close
branch must be paid support-wise before removal from the aperiodic residual.
The active Grande Finale v4 maximum-type route instead enters through actual
order-32 bad-slope records and has the separate `(S)/(A)/(E)` frontier.  This
repair applies to both routes but does not make the legacy Q/BC/K3 bridge a
prerequisite for the active one.

## Closed exact audit target

Audit the following replacement for the near-rational branch:

```text
If (u,v) is column-close to a codeword pair with error set E, then every
support-wise MCA-bad slope not already explained on the common support is
charged to a tangent ratio or to a shortened planted-core object supported on E.
After that charge, the remaining bad slopes lie in the balanced-core census.
```

The two-anchor theorem now proves this charge directly in support-wise units.
If `3w < n-K+1`, two near-codeword slopes determine a codeword line and an
error line supported on at most `2w` coordinates.  Every other near-rational
bad slope is recovered as an actual coordinate ratio on that error support,
so the whole stratum has at most `2w` distinct slopes.  At KoalaBear the exact
charge is `134944`.  The repaired proof uses the bad slope's identical witness
support and therefore does not identify it with the separate common support.
