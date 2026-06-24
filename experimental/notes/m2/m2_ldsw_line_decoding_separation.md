# M2 LD_sw Versus ABF/GG Line-Decoding Separation

**Status:** PROVED structural lemma; COUNTEREXAMPLE / FINITE instance.

This note records a finite Reed-Solomon example showing that the support-wise
line-decoding numerator `LD_sw` does not imply the stronger ABF/GG
`(delta,a,b)` line-decodability predicate.  The received line is nonconstant,
with nonzero codeword direction, so the separation does not depend on allowing
degenerate constant lines.  Thus the M2 bridge can import an external
line-decoding theorem in the forward direction, but a small `LD_sw` bound
should not be read as proving the ABF/GG assignment-collinearity conclusion.

## Claim

There is a Reed-Solomon code `C=RS[F_13,{0,...,7},3]`, an agreement threshold
`a=5`, and a nonconstant received line with support-wise `LD_sw` contribution
`0`, while a close-codeword assignment on that same line violates the ABF/GG
collinearity conclusion with `b=n+1=9`.

Equivalently, bounded support-wise MCA numerator is not a converse to ABF/GG
line-decodability.

## Structural Mechanism

The finite example is an instance of a general code-direction invisibility
lemma.

Let `C <= F^D` be any linear code, let `r in F^D`, and let `v in C`.  For any
agreement threshold `a`, the received line

```text
ell_gamma = r + gamma v
```

has no support-wise noncontained slopes.  Indeed, if `ell_gamma|S` is explained
by a codeword on a support `S`, then

```text
r|S = ell_gamma|S - gamma v|S
```

is also explained on `S`, and `v|S` is explained because `v in C`.  Thus every
explaining support is already contained in the support-wise MCA sense.  If
`r notin C` and `v != 0`, the received line may be nonconstant and not
contained in `C`, but its contribution to `LD_sw(C,a)` is still `0`.

This invisibility is specific to the support-wise numerator.  For a code-line
candidate `u0+gamma u1` and an assigned close codeword `U(gamma)`, put

```text
c_gamma = U(gamma) - gamma v.
```

Then `U(gamma)` is close to `r+gamma v` exactly when `c_gamma` is close to
`r`, and

```text
u0 + gamma u1 = U(gamma)
```

holds exactly when

```text
u0 + gamma(u1-v) = c_gamma.
```

Thus, on a code-direction received line, the ABF/GG collinearity conclusion is
equivalent to finding a large affine graph inside the shifted assignment
`gamma -> c_gamma` into the ordinary close list of `r`.  The support-wise
numerator has already vanished before this assignment-collinearity question
appears.

As a direct obstruction, suppose two distinct codewords `c0,c1 in C` both
agree with `r` on at least `a` coordinates, and split the field into two
nonempty buckets `F=A0 disjoint union A1`.  Define

```text
U(gamma) = c0 + gamma v,        gamma in A0,
U(gamma) = c1 + gamma v,        gamma in A1.
```

Every assigned codeword is `a`-close to the corresponding line point
`r+gamma v`.  However, any code-line `u0+gamma u1` agrees with this assignment
on at most

```text
max(|A0|, |A1|, 2)
```

slopes.  To see this, subtract `gamma v` from the target assignment.  If
`u1=v`, the shifted code-line is constant and can match only one bucket.  If
`u1 != v`, then the shifted code-line can hit `c0` for at most one slope and
`c1` for at most one slope.  Therefore any collinearity threshold
`b > max(|A0|,|A1|,2)` fails, even though the support-wise numerator of the
same received line is zero.  With a balanced partition this rules out every
threshold `b > ceil(|F|/2)` whenever such a two-codeword close list exists.

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
domain points.  Let `v(x)=x`, a nonzero codeword in `C`, and consider the
received line

```text
ell_gamma = r + gamma v.
```

This line is nonconstant and is not contained in `C`, since `r` is not a
codeword: any degree-`<3` polynomial agreeing with `r` on `{0,1,2,3,4}` would
be `p0`, but `r(5)=p1(5) != 0`.  Every large support on which a line point is
code-explained also explains the base `r`: subtract the already code-explained
direction `gamma v`.  The same support explains the direction `v` because
`v in C`.  Hence this line has no support-wise noncontained slopes at agreement
`5`; its contribution to `LD_sw(C,5)` is `0`.

Now define an adversarial close-codeword assignment on the slopes:

```text
U(gamma) = p0 + gamma v for gamma in {0,1,2,3,4,5},
U(gamma) = p1 + gamma v for gamma in {6,7,8,9,10,11,12}.
```

Every assigned codeword is `delta=3/8` close to the corresponding line point
`r + gamma v`.  Thus the ABF/GG line-decoding premise is triggered for any
numerator `a_LD <= 13`.

However, no code-line `u0 + gamma u1` agrees with this assignment on nine
slopes.  This is the two-bucket obstruction above with bucket sizes `6` and
`7`; the exact maximum is `ceil(13/2)=7 < 9`.

## Consequence for M2

The parameter-match note proves the useful forward implication:

```text
ABF/GG (delta,a_LD,n+1) line-decodable
  => LD_sw(C,ceil((1-delta)n)) <= a_LD
  => epsilon_mca(C,delta) <= a_LD/|F|.
```

The structural lemma, exact shifted-assignment reduction, and finite
Reed-Solomon instance show the converse fails for a conceptual reason, not a
numerical accident.  A genuine M2 theorem therefore needs a separate
assignment-collinearity input if it aims to prove ABF/GG line-decodability;
residue-line packing or `LD_sw` alone proves the MCA numerator, not the
stronger close-codeword assignment theorem.

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
