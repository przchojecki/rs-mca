# M2 LD_sw Versus ABF/GG Line-Decoding Separation

**Status:** COUNTEREXAMPLE / FINITE.

This note records a finite Reed-Solomon example showing that the support-wise
line-decoding numerator `LD_sw` does not imply the stronger ABF/GG
`(delta,a,b)` line-decodability predicate.  Thus the M2 bridge can import an
external line-decoding theorem in the forward direction, but a small `LD_sw`
bound should not be read as proving the ABF/GG assignment-collinearity
conclusion.

## Claim

There is a Reed-Solomon code `C=RS[F_13,{0,...,7},3]`, an agreement threshold
`a=5`, and a received line with support-wise `LD_sw` contribution `0`, while a
close-codeword assignment on that same line violates the ABF/GG collinearity
conclusion with `b=n+1=9`.

Equivalently, bounded support-wise MCA numerator is not a converse to ABF/GG
line-decodability.

## Construction

Let `D={0,...,7}` in `F_13`, let `C=RS[F_13,D,3]`, and put

```text
p0(x) = 0,             p1(x) = x(x-1).
```

The codewords `p0` and `p1` agree at `x=0,1`.  Define a received word `r` by

```text
r = p0 on {0,1,2,3,4},
r = p1 on {0,1,5,6,7}.
```

This is well-defined, and both `p0` and `p1` agree with `r` on exactly five
domain points.  Consider the constant received line

```text
ell_gamma = r + gamma 0.
```

Every large support on which a line point is code-explained also explains the
base `r` by that same codeword and explains the zero direction by the zero
codeword.  Hence this line has no support-wise noncontained slopes at agreement
`5`; its contribution to `LD_sw(C,5)` is `0`.

Now define an adversarial close-codeword assignment on the slopes:

```text
U(gamma) = p0 for gamma in {0,1,2,3,4,5},
U(gamma) = p1 for gamma in {6,7,8,9,10,11,12}.
```

Every assigned codeword is `delta=3/8` close to the corresponding line point
`r`.  Thus the ABF/GG line-decoding premise is triggered for any numerator
`a_LD <= 13`.

However, no code-line `u0 + gamma u1` agrees with this assignment on nine
slopes.  If `u1=0`, then the code-line is constant and matches at most the
larger bucket, namely seven slopes.  If `u1 != 0`, then it can hit `p0` for at
most one slope and `p1` for at most one slope, so it matches at most two slopes.
The exact maximum is therefore `7 < 9`.

## Consequence for M2

The parameter-match note proves the useful forward implication:

```text
ABF/GG (delta,a_LD,n+1) line-decodable
  => LD_sw(C,ceil((1-delta)n)) <= a_LD
  => epsilon_mca(C,delta) <= a_LD/|F|.
```

This example shows the converse fails even on a tiny Reed-Solomon code.  A
genuine M2 theorem therefore needs a separate assignment-collinearity input if
it aims to prove ABF/GG line-decodability; residue-line packing or `LD_sw`
alone proves the MCA numerator, not the stronger close-codeword assignment
theorem.

This does not contradict the ABF/GG theorem.  It only rules out a possible
shortcut from support-wise MCA bounds back to line-decodability.

## Verifier

The script
`experimental/scripts/verify_m2_ldsw_line_decoding_separation.py` enumerates
the finite RS code, all supports of size at least five, and all code-lines:

```bash
python3 experimental/scripts/verify_m2_ldsw_line_decoding_separation.py
python3 experimental/scripts/verify_m2_ldsw_line_decoding_separation.py --json
```
