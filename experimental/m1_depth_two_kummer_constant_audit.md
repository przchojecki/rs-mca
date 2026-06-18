# M1 Depth-Two Kummer Constant Audit

**Status:** AUDIT / EXPERIMENTAL.

## Claim

The M1 slack-two depth-two Kummer ledger uses the repaired degree-stratified
bounds

```text
d=0, coordinate nonprincipal:               p + 6 ceil(sqrt(p))
d!=0, coordinate principal:                 p + 6 ceil(sqrt(p))
d quadratic, exactly one coordinate active: 4p
d nonquadratic, exactly one coordinate:     4p
d!=0, two coordinate, mu nu eta^2=1:        2p + 5 ceil(sqrt(p))
d!=0, two coordinate, reciprocal line pair: 4p + 3 ceil(sqrt(p))
d!=0, two coordinate, remaining ramified:   9p
d!=0, three coordinate active:             16p
```

This note adds a finite exact character-sum audit for those bounds. It also
records the reason for the repair: the principal characters are extended by
zero on the Kummer open set, so the elementary Jacobi and conic-only pieces
are open-set sums, not unrestricted sums. It does not prove the uniform
two-variable normal-crossing Kummer estimate; it checks that the exact sums
satisfy the ledger in representative small prime and subgroup-index regimes,
including nonquadratic square-coset characters.

The proof-level open-set correction is isolated in
`experimental/m1_depth_two_elementary_open_set_lemma.md`; this note is the
finite exact-sum regression audit for that corrected ledger.
The proof-level one-coordinate mixed reductions are isolated in
`experimental/m1_depth_two_quadratic_one_coordinate_lemma.md` and
`experimental/m1_depth_two_nonquadratic_one_coordinate_lemma.md`.
The two-coordinate proof boundary is sharpened further in
`experimental/m1_depth_two_infinity_unramified_two_coordinate_lemma.md`,
which proves the full `mu nu eta^2=1` slice with a
`2p+2 sqrt(p)` core bound and the usual `3 sqrt(p)` line correction.
The reciprocal two-coordinate note also removes the projective line-pair
reciprocal slices `mu nu=1`, `nu eta^2=1`, and `mu eta^2=1`.
The raw saturation certificate now separates both the exact
`mu nu eta^2=1` L1 mass and the exact ramified projective-reciprocal L1 mass,
charging only the remaining ramified nonreciprocal two-coordinate mass by the
imported `9p` constant.

## Parameters

Let `p>3` be prime, let `D <= F_p^*` have order `n`, and put

```text
e=[F_p^*:D],        h=[F_p^*:D^2].
```

The audited sums are

```text
S_{a,b,c,d} =
  sum_{u,v in F_p}
    chi^a(u) chi^b(v) chi^c(-1-u-v) psi^d(A(u,v)),

A(u,v)=-(u^2+v^2+uv+u+v+1),
```

where `chi` has kernel `D`, `psi` has kernel `D^2`, and all characters are
extended by zero at zero. The verifier enumerates every tuple
`(a,b,c,d) in (Z/eZ)^3 x Z/hZ`, except the principal tuple, and classifies it
by active coordinate count and conic character.

## Audit Scope

The current sample set is

```text
(p,n,e,h) = (17,8,2,4),
            (31,10,3,6),
            (37,9,4,4),
            (43,14,3,6),
            (61,20,3,6).
```

These samples cover quadratic square-coset characters, nonquadratic conic
characters, odd and even `D`, and coordinate-character orders `2`, `3`, and
`4`.

The audit is reproduced by

```bash
python3 experimental/verify_m1_depth_two_kummer_constant_audit.py
```

It prints the largest observed absolute sum in each category and asserts that
each maximum is at most the appropriate repaired ledger bound.

## Finite Obstruction to an all-`4p` Shortcut

A tempting simplification would be to charge every mixed `d!=0` term by the
one-coordinate `4p` constant. The finite audit already rules this out. For

```text
(p,n,e,h) = (37,9,4,4),    (a,b,c,d) = (2,2,2,2),
```

the term is a three-coordinate mixed Kummer sum and has absolute value
`185 = 5p`. Thus the three-coordinate mixed ledger cannot be collapsed to the
degree-three `4p` constant. The remaining proof target is genuinely the
degree-stratified normal-crossing line/conic estimate.

## Contribution to M1

This audit targets the narrow dependency left in the slack-two depth-two
piece of PR #82: the normal-crossing line/conic Kummer estimate. It is useful
for two reasons.

First, it makes the conditional import falsifiable at the exact level used by
the ledger. A failure would identify a concrete tuple `(p,n,a,b,c,d)` and the
active radical degree responsible for the breakdown.

Second, it separates finite computational evidence from the uniform theorem.
The finite audit supports the repaired ledger but leaves one proof-status
boundary: after the one-coordinate and infinity-unramified two-coordinate
reductions, plus the projective reciprocal line-pair reductions, the
remaining mathematical task is a uniform normal-crossing Kummer estimate for
the ramified-infinity line/conic arrangement with no reciprocal line pair.
The projective equal-pair ledger and the subsequent line-conic-resonance
split sharpen this boundary further: the clean nonresonant target has no
equal or reciprocal projective line pair and no line-conic reciprocal dense
edge, while the line-conic-resonant asymmetric slice is now counted
separately by the `C_2^lc` ledger.
The saturation certificate keeps the conservative `9p` import active, but it
also reports the conditional ledger obtained by combining the projective
equal-pair import with a future nonresonant `4p+3 sqrt(p)` theorem.  Under
that combined import, the only remaining two-coordinate terms still charged
at `9p` are the line-conic-resonant asymmetric terms.
Those terms have now been reduced to a one-dimensional trace-family problem
in `experimental/m1_depth_two_line_conic_resonance_reduction.md`, whose
singular-value checklist is `{0,-1,2,3,infinity}`.
