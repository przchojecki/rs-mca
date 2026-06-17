# M2 Line-Decoding to MCA Bridge

**Status:** PROVED for the finite-support implications below; AUDIT for matching
external line-decoding theorems to this predicate.

This note isolates the exact line-decoding object that implies the support-wise
MCA bound used in `tex/snarks_v4.tex`.  It is meant as a small step toward the
M2 target in `agents.md`: restating the corrected residue-line packing
conjecture as a line-decoding statement with explicit parameters.  It does not
prove the corrected asymptotic MCA conjecture.

## Setup

Let `C <= F^D` be a linear code over a finite field `F`, with `|D|=n`.
For `S subset D`, write `C|S` for the punctured code on `S`.  Let

```text
a(delta) = ceil((1-delta)n).
```

For a line `ell_z = f + z g`, with `f,g in F^D`, call a slope `z`
support-wise noncontained at agreement size `a` if there is a support
`S subset D` such that

```text
|S| >= a,
(f + z g)|S in C|S,
and there do not exist c_f,c_g in C with f|S=c_f|S and g|S=c_g|S.
```

Define the support-wise line-decoding numerator

```text
LD_sw(C,a) =
  max_{f,g in F^D} #{z in F : z is support-wise noncontained for f+z g
                    at agreement size a}.
```

This is the line-decoding numerator that the MCA ledger can consume directly.

## Exact Bridge

For every linear code `C <= F^D` and every `delta in [0,1]`,

```text
eps_mca(C,delta) = LD_sw(C,ceil((1-delta)n)) / |F|.
```

This is an equality, not only an implication.  The support-wise MCA definition
maximizes over the same pairs `(f,g)` and counts the same slopes `z`: a large
support explaining the line point but not simultaneously explaining `(f,g)`.
The only conversion is from radius to agreement size by
`a=ceil((1-delta)n)`.

Consequently, any theorem proving

```text
LD_sw(C,a(delta)) <= a_LD
```

immediately gives

```text
eps_mca(C,delta) <= a_LD / |F|.
```

This is the precise finite-length content behind the manuscript phrase
`(delta,a_LD,n+1) line-decodable => eps_mca <= a_LD/|F|`.

## Per-Support Algebra

Fix `S subset D`.  The set of slopes that make the line point land in the
punctured code is

```text
E_S(f,g) = {z in F : f|S + z g|S in C|S}.
```

Because `C|S` is a linear subspace:

1. If `g|S in C|S` and `f|S in C|S`, then `E_S(f,g)=F`, but the support is
   contained and contributes no support-wise MCA-bad slope.
2. If `g|S in C|S` and `f|S notin C|S`, then `E_S(f,g)` is empty.
3. If `g|S notin C|S`, then `E_S(f,g)` has size at most one.  If it is
   nonempty, its unique element is noncontained on `S`.

Thus every contributing support contributes at most one bad slope.  For
Reed-Solomon codes, when `|S|>k`, the condition `g|S notin C|S` is exactly the
condition that the direction is not explained on that support by a degree `< k`
polynomial.  This is the local algebra behind both the one-bad-parameter
support bound and the residue-line packing formulation.

## What an External Line-Decoding Theorem Must Prove

A close-point line-decoding bound with a contained-line exception,

```text
either f+F g is contained in C, or #{z : dist(f+z g,C) <= delta} <= a_LD,
```

is sufficient, since support-wise noncontained slopes are a subset of close
line points, and a line contained in `C` has no support-wise noncontained
slopes.  This sufficient condition is usually stronger than necessary.

## Close-Point Line-Decoding Is Strictly Stronger

The sufficient close-point predicate above is not equivalent to the
support-wise numerator.  This matters when importing external line-decoding
theorems: a theorem that bounds all close line points with only a "line
contained in the code" exception may be much stronger than what MCA needs.

Here is an explicit Reed-Solomon separation.  Let `C=RS[F,D,k]`, `|D|=n`, and
assume

```text
k <= n-2,        a=n-1.
```

Choose `x0 in D` and let `h` be the one-point spike supported at `x0`, with
`h(x0)=1`.  Fix `lambda in F`, and take

```text
f = lambda h,        g = h.
```

Then the affine line `f+F g` is not contained in `C`, but every slope is a
close point:

```text
#{z in F : dist(f+z g,C) <= 1/n} = |F|.
```

By contrast, the support-wise noncontained slopes at agreement `a=n-1` are
exactly

```text
{-lambda}.
```

Thus ordinary close-point line-decoding can count `|F|` slopes on a line whose
support-wise numerator is only `1`.  The gap is entirely a common-support
issue: for every `z != -lambda`, the line point is explained by the zero
codeword on the punctured support `D \ {x0}`, and that same support also
explains both `f` and `g`.

Proof.  A nonzero degree-`<k` polynomial cannot agree with `h` on any support
of size `n-1` containing `x0`: it would have at least `n-2 >= k` roots and
also be nonzero at `x0`.  Hence `h` is not in `C`, so the line is not contained
in `C`.

For every `z`, the word `f+z g=(lambda+z)h` agrees with the zero codeword on
`D \ {x0}`, so every slope is close at radius `1/n`.  If `z != -lambda`, this
is the only size-`n-1` explaining support.  Any size-`n-1` support containing
`x0` would force a degree-`<k` polynomial to have `n-2` zeros and a nonzero
value at `x0`, impossible.  The unique explaining support therefore also
explains `f` and `g`, so the slope is not support-wise noncontained.

For `z=-lambda`, the line point is the zero codeword on every support.  Choose
a size-`n-1` support containing `x0`.  The line point is explained there, but
the same root-counting argument shows that `g` is not explained by a
degree-`<k` codeword on that support.  Therefore no pair of codewords can
explain both `f` and `g` there, so this slope is support-wise noncontained.

For a theorem with an exceptional "the line is explained" alternative, the
exception must be checked in the support-wise sense: for every close slope and
every large explaining support consumed by the protocol, the same support must
also explain both `f` and `g`.  A theorem that only says many line points are
close to `C` is not enough by itself, because MCA is sensitive to the common
support.

Therefore the corrected M2 target can be stated as:

```text
For C_n = RS[F_qn,H_n,k_n], delta_n = 1-rho-eta_n,
and a_n = ceil((1-delta_n)n),

LD_sw(C_n,a_n)
  <= n^{1+o(1)}
     + 2^{(beta(rho)/H(rho)) Q_Hn(a_n,k_n)(1+o(1))}
```

under the same entropy and quotient-profile hypotheses as the corrected MCA
conjecture.  The MCA statement is then the immediate corollary obtained by
dividing this numerator by `q_n`.  The spike-line separation shows why this
support-wise numerator is the right expected object: a stronger close-point
line-decoding theorem is welcome when available, but it should not be assumed
to follow from the residue-line packing conjecture.

## Follow-Up Checks

- Match the external `(delta,a_LD,n+1)` line-decoding definition used in
  protocol papers against `LD_sw(C,a)`.
- Express the residue-line packing number in `tex/slackMCA_v3.tex` as this
  `LD_sw` numerator.
- Decide whether the `n+1` parameter is only a codeword-uniqueness threshold or
  whether it hides an additional proximity-loss convention.
- Check whether protocol line-decoding imports have a common-support or
  code-line-proximity exception strong enough to avoid the spike-line
  close-point separation.

## Verifier

The script `experimental/m2_line_decoding_separation.py` verifies the spike
line on a tiny prime-field RS code by enumerating all degree-`<k` codewords and
all supports of size `n-1`:

```bash
python3 experimental/m2_line_decoding_separation.py
python3 experimental/m2_line_decoding_separation.py --format json
```
