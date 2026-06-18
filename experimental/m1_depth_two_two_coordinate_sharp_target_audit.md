# M1 Depth-Two Two-Coordinate Sharp-Target Audit

**Status:** AUDIT / EXPERIMENTAL.

## Claim Audited

The current slack-two depth-two ledger charges two-coordinate mixed Kummer
terms by the conditional degree-four constant `9p`. This note records a
finite exact-sum audit for the sharper possible target

```text
|S_{a,b,c,d}| <= 4p
```

when `d!=0` and exactly two of the coordinate exponents `(a,b,c)` are
nonzero.

This is not a proof of the uniform `4p` estimate and does not change the
certificate ledger. It is a sharpened target for the next M1 Kummer step.

## Exact Sums

With

```text
w=-1-u-v,
A(u,v)=-(u^2+v^2+uv+u+v+1),
```

the audited two-coordinate sums are

```text
S_{a,b,c,d} =
  sum_{u,v in F_p}
    chi^a(u) chi^b(v) chi^c(w) psi^d(A(u,v)),
```

where `chi` has kernel `D`, `psi` has kernel `D^2`, all characters are
extended by zero, `d!=0`, and exactly two of `a,b,c` are nonzero modulo the
coordinate-character order.

## Audit Result

The verifier exhausts all two-coordinate mixed tuples on the baseline
Kummer-audit samples and on several larger exhaustive samples:

```text
(p,n,e,h) = (17,8,2,4),
            (31,10,3,6),
            (37,9,4,4),
            (43,14,3,6),
            (61,20,3,6),
            (73,8,9,18),
            (79,26,3,6),
            (109,18,6,12),
            (113,16,7,14),
            (137,34,4,8),
            (193,64,3,6).
```

Every two-coordinate mixed term in these exhaustive samples satisfies the
sharper `4p` target. The largest exhaustive-sample ratio remains

```text
|S_{0,5,5,3}| / p = 3.3896787506
```

at `(p,n,e,h)=(109,18,6,12)`.
This exhaustive-sample maximum is already in the `ramified_nonreciprocal`
projective class.

The verifier also includes one targeted near-sharp obstruction:

```text
(p,n,e,h)=(421,20,21,42),        (a,b,c,d)=(5,5,0,6).
```

This targeted tuple has

```text
|S_{5,5,0,6}| / p = 3.9771715522,
```

still below `4p` but much closer to it. Its projective line monodromy class is
`ramified_nonreciprocal`, so it is not removed by the proved
infinity-unramified or projective-reciprocal reductions. This row is not an
exhaustive all-tuple audit for `(p,n)=(421,20)`; it is included to make the
near-sharp finite obstruction reproducible without making the verifier
expensive.

## Finite Obstruction Below `4p`

The older exhaustive sample already rules out the stronger uniform target
`3p`: the exact tuple

```text
(p,n,e,h)=(109,18,6,12),        (a,b,c,d)=(0,5,5,3)
```

has absolute value `369.4749838169`, which is larger than `3p=327`.
It is also `ramified_nonreciprocal`, so the obstruction to a `3p` theorem
survives the proved slice reductions.
The targeted `(421,20)` tuple strengthens the obstruction: any future
two-coordinate theorem of the form `|S| <= C p` needs

```text
C >= 3.9771715522
```

in this normalization. Thus the plausible `4p` target, if true, is nearly
sharp for the remaining ramified nonreciprocal family.

## Remaining-Wall Stress Scan

The targeted scanner
`experimental/search_m1_remaining_two_coordinate_wall.py` tests only the
ramified nonreciprocal class left after the proved slice reductions. Its
report preset exhausts all canonical active-pair remaining-wall tuples with
`p <= 500` and `e <= 24`, then scans the diagonal `n=20` family up to
`p <= 1601`. It finds no `4p` violation among `946184` tuple evaluations
across the two scans.

The top rows all have equal projective line monodromies. For example the
two largest observed ratios are

```text
(p,n,e,h)=(421,20,21,42),  (a,b,c,d)=(5,5,0,6),
|S|/p=3.9771715522,        lines=(10,10,10),

(p,n,e,h)=(461,20,23,46),  (a,b,c,d)=(18,18,0,15),
|S|/p=3.9643175123,        lines=(36,36,36).
```

This suggests that the equal-line-monodromy diagonal family may be the
right first analytic subtarget for the remaining `4p` theorem.
The symmetric-coordinate reduction for that subtarget is isolated in
`experimental/m1_depth_two_equal_line_diagonal_reduction.md`.

## Contribution to M1

The one-coordinate mixed terms are now reduced to one-dimensional input in
`m1_depth_two_quadratic_one_coordinate_lemma.md` and
`m1_depth_two_nonquadratic_one_coordinate_lemma.md`. This audit identifies
the next plausible strengthening: replace the remaining two-coordinate
degree-four import

```text
|S_{a,b,c,d}| <= 9p
```

by a sharper `4p` theorem, if the finite pattern persists uniformly.
After the infinity-unramified and projective-reciprocal reductions, the same
target is still necessary for the remaining ramified nonreciprocal family,
as witnessed by the `(421,20)` targeted row.
The three-coordinate `16p` term remains separate; the finite obstruction in
`m1_depth_two_kummer_constant_audit.md` already shows that not all mixed
terms can be collapsed to `4p`.

The verifier is

```bash
python3 experimental/verify_m1_depth_two_two_coordinate_sharp_target.py
```
