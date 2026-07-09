# B1 Image-Scale Repair for `asymptotic_rs_mca`

Status: AUDIT / CONDITIONAL

This note records the TeX-level implementation of the image-scale repair path
for the B1 normalization bridge in `experimental/asymptotic_rs_mca.tex`.

## Claim Boundary

The repair proves two local bookkeeping lemmas:

```text
lem:ambient-image-max
lem:moment-normalization
```

The second lemma records the exact relation

```text
Gamma_amb(q) = (A/L)^(q-1) Gamma_img(q),
```

where `A` is the ambient group size and `L = |im Phi|`.

The C9 Fourier/Sidon payment is not proved here.  It is now an explicit
image-normalized assumption:

```text
ass:image-normalized-sidon-input
```

with normalization by

```text
barN = |Omega^circ| / |im Phi|.
```

## Why This Matters

The asymptotic proof uses primitive leaf moments at image scale.  Without this
repair, an ambient moment or Fourier statement could be consumed as if it were
already normalized over `im Phi`.  The moment-normalization identity shows the
exact conversion factor and makes the safe direction explicit.

An ambient upper bound can imply the corresponding image upper bound.  The
reverse direction is unsafe without a printed bound on `A/L`, so C9 is stated
directly at image scale.

## Nonclaims

This packet does not prove:

```text
C9 moduli/Fourier-Sidon source theorem
B3 window uniformity
add-back profile decomposition
lower-side pole-reservoir collision loss
any finite deployed adjacent row
```

It only repairs the B1 normalization interface and makes the remaining
dependencies visible in the paper text.
