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
confirming both the per-slope residual-zero condition and the finite residual
bound.
