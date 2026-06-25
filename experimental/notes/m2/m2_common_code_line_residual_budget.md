# M2 Common Code-Line Residual Budget

## Status

PROVED finite theorem for MDS codes. EXPERIMENTAL verifier.

This note packages the common-code-line exception needed by M2. It is a
support-wise replacement for the ordinary close-point statement "the received
line is close to a code-line": if the base and direction agree with a code-line
on a common support, then any remaining support-wise noncontained slopes must
be paid for by residual zeros outside that support.

## Theorem

Let `C <= F^D` be an MDS linear code of dimension `k`, so a nonzero codeword
has fewer than `k` zeros on `D`. Let `|D|=n`, let `a` be an agreement
threshold, and fix a received line

```text
ell_z = f + z g.
```

Assume there are codewords `c_f,c_g in C` and a common support `S0 subset D`
of size `b` such that

```text
f=c_f on S0,        g=c_g on S0,
```

and

```text
a+b-n >= k.
```

Put

```text
Omega = D \ S0,
f' = f-c_f,        g' = g-c_g,
h = max(1,a-b),
c0 = |{x in Omega : f'(x)=g'(x)=0}|.
```

Every support-wise noncontained slope at agreement `a` satisfies

```text
|{x in Omega : f'(x)+z g'(x)=0}| >= h.
```

Consequently, if `h>c0`, then

```text
#{support-wise noncontained slopes}
  <= floor((|Omega|-c0)/(h-c0)).
```

## Defect-Coordinate Form

It is often clearer to parameterize the exception by its defect outside the
common support.  Let

```text
e = n-a,        s = |Omega| = n-b.
```

Then the MDS forcing condition is

```text
a+b-n >= k        <=>        n-e-s >= k.
```

For an `[n,k]` MDS code, writing `r=n-k`, this says `e+s <= r`: the common
code-line exception can spend only redundancy coordinates.  The residual
zero threshold becomes

```text
h = max(1,a-b) = max(1,s-e).
```

Hence the same theorem gives

```text
#{support-wise noncontained slopes}
  <= floor((s-c0)/(max(1,s-e)-c0))
```

whenever the denominator is positive.  In the generic no-common-residual-zero
case `c0=0`, this specializes to

```text
<= s                         if s <= e,
<= floor(s/(s-e))            if s > e.
```

Thus a code-line-proximity exception is not a free pass for M2.  It consumes a
visible residual slope budget, and the budget is controlled by how many
coordinates the common code-line support omits relative to the decoding error
allowance.

## Import Criterion

This gives a finite certificate shape for external line-decoding theorems with
exceptional code-line alternatives.  For a received line `f+z g`, let `Z_sw`
be the support-wise noncontained slope set at agreement `a`.  Suppose an
external argument supplies:

1. an unexceptional slope set `Z0` with `|Z0| <= A`;
2. common code-line certificates

```text
(c_f,j, c_g,j, S_j)        for j=1,...,J
```

each satisfying the theorem's hypotheses, with residual budgets `B_j`; and
3. a residual-threshold cover

```text
Z_sw subset Z0 union R_1 union ... union R_J,
```

where `R_j` is the slope set satisfying the residual-zero inequality attached
to the `j`th certificate.

Then

```text
|Z_sw| <= A + B_1 + ... + B_J.
```

The proof is just the union bound plus the theorem above, applied to each
residual-threshold set.  The point is the data requirement: an imported
close-point line-decoding theorem must output a common support and a residual
budget, not only the assertion that many line points are close to some
codeword.  This is the local M2 check that prevents the spike separation from
being misread as a large MCA numerator.

## Proof

Let `z` have a support-wise noncontained witness `T`, so `|T|>=a` and
`(f+z g)|T` is explained by some codeword `u_z in C`. Subtract the common
code-line point `c_f+z c_g` and set

```text
r_z = u_z - c_f - z c_g in C.
```

On `T cap S0`, the residual word `f'+z g'` is zero, so `r_z` vanishes there.
Since

```text
|T cap S0| >= |T|+|S0|-n >= a+b-n >= k,
```

the MDS zero property forces `r_z=0`. Hence `f'+z g'` vanishes on all of `T`,
and at least

```text
|T|-|S0| >= a-b
```

positions of `Omega`. The lower bound is at least `h=max(1,a-b)` because a
noncontained witness cannot be explained entirely by the common code-line on
`S0`.

Now count outside coordinates. The `c0` common residual-zero coordinates
vanish for every slope. Every other coordinate of `Omega` can vanish for at
most one slope, because the equation

```text
f'(x)+z g'(x)=0
```

has at most one solution in `z` unless both residuals vanish. If `h>c0`, each
bad slope needs at least `h-c0` private outside coordinates, so the displayed
bound follows.

## RS Consequence

Reed-Solomon codes are MDS, so the theorem applies to

```text
C = RS[F,D,k].
```

For the spike separation in `m2_line_decoding_mca_bridge.md`, take
`S0=D\{x0}`, `a=b=n-1`, and the zero code-line. Then

```text
Omega={x0},        h=1,        c0=0,
```

so the residual budget gives exactly one support-wise noncontained slope,
even though ordinary close-point line-decoding sees all `|F|` slopes.

This is the support-wise condition an external close-point line-decoding
theorem must provide if it uses a common-code-line exception. A bare statement
that many line points are close to the code is not enough for MCA; the common
support and residual budget are the consumable M2 certificate.

## Verifier

Run from the repository root:

```sh
python3 experimental/scripts/verify_m2_common_code_line_residual_budget.py
```

The verifier enumerates small Reed-Solomon codes, all agreement supports, and
all slopes. It checks the spike example and deterministic residual cases,
including a case with common residual-zero coordinates, confirming both the
per-slope residual-zero condition and the finite residual bound.
