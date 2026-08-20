# MCA sparse-direction terminal-deficit line payment v1

## Status

PROVED / EXACT FINITE CALIBRATION.

This packet strengthens only the exact outside-deficit `h=e` layer of the
field-general sparse-direction profile.  It does not prove an official row
or turn failure of the adjacent calculation into an unsafe certificate.

## The structural cap

Use the codeword gauge

```text
r_1=b+q,       E=supp(q),       |E|=e,
N=R+K,         m=d+K,           n=N-e,
A=m-e,         c=K-1.
```

An explanation of exact outside deficit `e` has exactly `A` outside
agreements.  Owning a selected slope therefore forces agreement at every
coordinate of `E`.  If `e>=K`, restriction to `E` is injective on
degree-`<K` codewords, so all terminal explanations lie on one affine
codeword line.

Outside `E`, their agreement sets are disjoint after deleting a common zero
core of size at most `c`.  Hence

```text
L_e <= floor((n-c)/(A-c)).
```

For `h<e`, retain the already proved Johnson/mean-centered cumulative caps
and take suffix minima only over the prefix.  Add the affine-line cap for
the terminal layer, whose slope-owner weight is one.

## Exact official rows

```text
KoalaBear e=64048:
  prefix profile = 181326056
  terminal cap   =       287
  total          = 181326343 <= 274980728111395087

Mersenne-31 e=65455:
  prefix profile = 16100154
  terminal cap   =      493
  total          = 16100647 <= 16777215
```

At KoalaBear `e=64049`, the cap at `h=e-1` is unavailable.  At Mersenne
`e=65456`, the resulting valid profile is `17119507`, over budget by
`342292`.  Thus the residual full-lift intervals become

```text
KoalaBear:   64049 <= e <= 1044238
Mersenne-31: 65456 <= e <= 1044241.
```

## Replay

Run

```bash
python3 experimental/verify_mca_sparse_direction_terminal_deficit_line_payment_v1.py
```

The verifier reconstructs every prefix cap with exact integers, checks the
two terminal affine-line caps, verifies both paid profiles and both adjacent
stopping modes, and runs hostile mutations plus a finite common-core packing
control.
