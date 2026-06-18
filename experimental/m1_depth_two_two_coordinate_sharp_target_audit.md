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
Kummer-audit samples and on several larger targeted samples:

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

Every audited two-coordinate mixed term satisfies the sharper `4p` target.
The largest audited ratio is

```text
|S_{0,5,5,3}| / p = 3.3896787506
```

at `(p,n,e,h)=(109,18,6,12)`.

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
The three-coordinate `16p` term remains separate; the finite obstruction in
`m1_depth_two_kummer_constant_audit.md` already shows that not all mixed
terms can be collapsed to `4p`.

The verifier is

```bash
python3 experimental/verify_m1_depth_two_two_coordinate_sharp_target.py
```
