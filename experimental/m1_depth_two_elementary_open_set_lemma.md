# M1 Depth-Two Elementary Open-Set Lemma

**Status:** CONDITIONAL / AUDIT.

## Claim

Assume the standard Jacobi-sum bound and the standard genus-zero
multiplicative Weil bound on `P^1`. Let `p>3`, put

```text
w=-1-u-v,
A(u,v)=-(u^2+v^2+uv+u+v+1),
```

and extend all multiplicative characters by zero at zero.

Then the elementary terms in the M1 slack-two depth-two Kummer expansion obey
the open-set bounds

```text
|sum_{u,v} chi^a(u) chi^b(v) chi^c(w) psi^0(A(u,v))|
  <= p + 6 sqrt(p)
```

for every nonzero coordinate tuple `(a,b,c)`, and

```text
|sum_{u,v} chi^0(u) chi^0(v) chi^0(w) psi^d(A(u,v))|
  <= p + 6 sqrt(p)
```

for every nonzero square-coset exponent `d`.

Here `psi^0(A)` is the principal character extended by zero, so the first
sum omits `A=0`; the second sum omits the three coordinate lines
`u=0`, `v=0`, and `w=0`.

## Jacobi Term

Without the `A!=0` restriction,

```text
sum_{u+v+w=-1} chi^a(u) chi^b(v) chi^c(w)
```

is a three-character Jacobi sum. For a nonzero tuple `(a,b,c)`, the standard
Jacobi recursion bounds it by `p`.

The removed part lies on the smooth projective conic

```text
C : U^2 + V^2 + UV + UZ + VZ + Z^2 = 0.
```

On `C`, the rational functions

```text
u=U/Z,        v=V/Z,        w=(-U-V-Z)/Z
```

have zero-pole support contained in the three coordinate line sections and
the line at infinity. Each section has geometric degree two. If
`(a,b,c)` is nonzero, the product `u^a v^b w^c` is not a character-order
power on `C`, because at least one coordinate zero divisor has nonzero
coefficient. Thus the genus-zero Kummer bound gives the conic correction

```text
(8-2) sqrt(p) = 6 sqrt(p).
```

Adding the unrestricted Jacobi bound gives `p + 6 sqrt(p)`.

## Conic-Only Term

Without the coordinate-line restrictions, completing the square gives the
exact affine-plane conic sum

```text
|sum_{u,v} psi^d(A(u,v))| = p
```

for every nonzero `d`.

The open-set restriction removes the union of the three lines

```text
u=0,        v=0,        w=0.
```

On each line, `A` restricts to a scalar multiple of the separable quadratic

```text
T^2 + T + 1.
```

For every nontrivial `psi^d`, this one-variable rational function is not a
character-order power, so the genus-zero Kummer bound gives `sqrt(p)` for
each line. The three pairwise line intersections all have `A=-1`, so their
total inclusion-exclusion contribution has absolute value at most `3`.
Since `3 sqrt(p)+3 <= 6 sqrt(p)` for `p>3`, the coordinate-line removal costs
at most `6 sqrt(p)`.

Adding the unrestricted conic-only bound gives `p + 6 sqrt(p)`.

## Contribution to M1

This lemma is the proof-level version of the elementary open-set correction
used by `m1_support_occupancy_scan.py`. It explains why the repaired
depth-two ledger subtracts

```text
6 ceil(sqrt(p)) * (jacobi_l1_bound + conic_l1_bound)
```

in addition to the linear weighted error. It does not address the remaining
mixed two-variable normal-crossing Kummer estimate; that dependency remains
isolated in `m1_kummer_weil_import_contract.md`.
