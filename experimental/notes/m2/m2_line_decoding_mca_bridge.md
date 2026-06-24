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

## Support-Witness Projection Certificate

The per-support algebra gives a finite certificate object for `LD_sw`.  For a
line `f+z g` and agreement size `a`, define

```text
W_a(f,g)
  = { (S,z) :
        |S| >= a,
        (f+z g)|S in C|S,
        not (f|S in C|S and g|S in C|S) }.
```

Then the support-wise bad-slope set is exactly the projection

```text
pi_z W_a(f,g).
```

Hence

```text
#{support-wise noncontained slopes}
  <= |W_a(f,g)|.
```

Moreover, if every bad slope has at least `mu` witness supports in `W_a(f,g)`,
then

```text
#{support-wise noncontained slopes}
  <= |W_a(f,g)| / mu.
```

For linear codes this certificate can be emitted support-by-support: if
`g|S in C|S`, the support contributes no noncontained slope, while if
`g|S notin C|S`, it contributes at most one slope.  Thus an M2 certificate may
bound `LD_sw` either by counting noncontained supports directly or by using
slope-fiber multiplicity in the projection.  This is useful because the
support-family machinery often naturally bounds witness supports, while
line-decoding consumes distinct slopes.

For Reed-Solomon codes, this certificate may be reduced to exact-size
supports.  Suppose `C=RS[F,D,k]` and `a >= k+1`.  If a slope has a
support-wise noncontained witness on some support `T` with `|T| >= a`, then it
has one on a support `S subset T` with `|S|=a`.  Indeed, the line point remains
code-explained on every subset of `T`.  Since the witness on `T` is
noncontained, at least one of `f|T` or `g|T` is not the restriction of a
degree-`<k` polynomial.  That failure is already visible on some
`(k+1)`-subset of `T`; otherwise every `(k+1)`-subset would force the same
degree-`<k` interpolation one point at a time.  Extend this bad `(k+1)`-subset
inside `T` to size `a`.  The resulting support still explains the line point
but does not explain both `f` and `g`.

Thus for Reed-Solomon codes and `a >= k+1`, `LD_sw(C,a)` is unchanged if
`W_a(f,g)` is restricted to exact supports `|S|=a`.  This is the form most
useful for finite support-family scanners and for comparison with the M1
exact-support ledgers.

## Residue-Line Equivalence for Reed-Solomon Codes

The support-wise numerator is exactly the residue-line packing number from
`tex/slackMCA_v3.tex`, after translating radius into agreement size.  This is
the finite M2 bridge in agreement coordinates.

Let `C=RS[F,D,k]`, `|D|=n`, and `r=n-k`.  Assume there is a degree-`r`
polynomial nonzero on `D`; this holds for multiplicative domains by taking
`X^r`.  For `1 <= t <= r`, define a degree-`t` residue-line datum to be

```text
E in F[X], deg E=t, E(x) != 0 on D,
B in F[X], deg B<t,
w:D -> F.
```

For agreement size `a`, a slope `z` is witnessed by this datum if there are
`S subset D` and `Q_z in F[X]` such that

```text
|S| >= a,
deg Q_z < k+t,
Q_z == zB mod E,
Q_z = w on S,
```

and the witness is noncontained if no `A,G in F[X]_{<k}` satisfy

```text
A = w/E on S,        G = -B/E on S.
```

Let `RL_NC(D,k,a)` be the maximum, over all degrees `1 <= t <= r` and all such
data, of the number of slopes with noncontained witnesses.  Then

```text
LD_sw(RS[F,D,k],a) = RL_NC(D,k,a).
```

If `a >= k+1`, define `RL_NC^=(D,k,a)` by the same maximum but requiring every
witness support to have exact size `|S|=a`.  The exact-support reduction above
gives the sharper agreement-coordinate identity

```text
LD_sw(RS[F,D,k],a) = RL_NC^=(D,k,a) = RL_NC(D,k,a).
```

Consequently, the corrected M2 target can be stated equivalently as a bound on
the exact-support residue-line packing number `RL_NC^=(D,k,a(delta))` whenever
`a(delta) >= k+1`; dividing by `|F|` gives the MCA bound by the exact bridge
above.  This is the form aligned with the M1 exact-support overlap ledgers.

Proof.  First fix a line `f+z g` and a set of support-wise noncontained slopes.
Choose a degree-`r` polynomial `E` nonzero on `D`.  By interpolation and
Euclidean division, write on `D`

```text
g = R - B/E,        deg R<k,        deg B<r.
```

For a bad slope `z`, let `P_z in F[X]_{<k}` explain `f+z g` on a witness
support `S_z`.  Put

```text
w = E f,        Q_z = E(P_z - zR) + zB.
```

Then `deg Q_z<k+r`, `Q_z == zB mod E`, and on `S_z`,

```text
Q_z = E(f+z g-zR)+zB = E f = w.
```

If the residue witness were contained, then `A=w/E` and `G=-B/E` on `S_z`
would give degree-`<k` explanations of `f` and `g=R+G` on the same support,
contradicting support-wise noncontainment.  Thus every line contributes no
more slopes than one residue-line datum, so `LD_sw <= RL_NC`.

Conversely, given a residue-line datum and noncontained witnessed slopes,
define words on `D` by

```text
f = w/E,        g = -B/E.
```

For each witnessed slope, `Q_z-zB` is divisible by `E`; set

```text
P_z = (Q_z-zB)/E.
```

The degree bound gives `deg P_z<k`, and on the witness support
`P_z=(w-zB)/E=f+z g`.  Noncontainedness of the datum is exactly failure of
simultaneous degree-`<k` explanations for `f` and `g` on that support.  Hence
every residue-line packing instance gives a support-wise line-decoding
instance with the same slope set, proving `RL_NC <= LD_sw`.

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

## Common Code-Line Exception Residual Bound

The spike example is also a useful diagnostic for stronger external
line-decoding theorems.  If the exceptional case says not merely "the line has
many close points", but that the received line is close to a genuine code-line
on a common support, then the support-wise numerator is controlled by the
residual outside that support.

Let `C=RS[F,D,k]`, fix agreement size `a`, and suppose there are codewords
`c_f,c_g in C` and a support `S0 subset D` of size `b` such that

```text
f=c_f on S0,        g=c_g on S0,
```

with

```text
a+b-n >= k.
```

Put `Omega=D \ S0`, `f'=f-c_f`, and `g'=g-c_g`; then `f'` and `g'` vanish on
`S0`.  Set

```text
h = max(1,a-b),
c0 = |{x in Omega : f'(x)=g'(x)=0}|.
```

Every support-wise noncontained slope must satisfy

```text
|{x in Omega : f'(x)+z g'(x)=0}| >= h.
```

Consequently, if `h>c0`, then

```text
#{support-wise noncontained slopes}
  <= floor((|Omega|-c0)/(h-c0)).
```

The proof is a direct puncturing argument.  Let `z` have a witness support
`T`, and subtract the code-line `c_f+z c_g` from the explaining codeword on
`T`.  The residual degree-`<k` codeword vanishes on `T cap S0`, whose size is
at least `a+b-n >= k`; hence the residual codeword is zero.  Thus
`f'+z g'` vanishes on all of `T`, so it has at least `h` zeros in `Omega`.
If `h>c0`, the common residual-zero positions contribute to every slope, while
each remaining outside coordinate contributes to at most one slope.  Counting
coordinate-slope incidences gives the displayed bound.

For the spike line, take `S0=D \ {x0}` and the zero code-line.  Then
`b=a=n-1`, `h=1`, `c0=0`, and `|Omega|=1`, so the residual bound gives exactly
one possible support-wise noncontained slope.  This explains why a
code-line-proximity exception can absorb the `|F|` close-point count while
still leaving a small support-wise numerator to budget.

For a theorem with an exceptional "the line is explained" alternative, the
exception must be checked in the support-wise sense: for every close slope and
every large explaining support consumed by the protocol, the same support must
also explain both `f` and `g`.  A theorem that only says many line points are
close to `C` is not enough by itself, because MCA is sensitive to the common
support.  A common code-line exception is usable only after the residual
support-wise budget above, or a sharper replacement, is included in the
certificate.

Therefore the corrected M2 target can be stated as:

```text
For C_n = RS[F_qn,H_n,k_n], delta_n = 1-rho-eta_n,
and a_n = ceil((1-delta_n)n),

LD_sw(C_n,a_n)
  <= n^{1+o(1)}
     + 2^{(beta(rho)/H(rho)) Q_Hn(a_n,k_n)(1+o(1))}
```

under the same entropy and quotient-profile hypotheses as the corrected MCA
conjecture.  Equivalently, by the residue-line bridge above, the same bound is
the agreement-coordinate form of the companion's noncontained residue-line
packing conjecture.  The MCA statement is then the immediate corollary
obtained by dividing this numerator by `q_n`.  The spike-line separation shows
why this support-wise numerator is the right expected object: a stronger
close-point line-decoding theorem is welcome when available, but it should not
be assumed to follow from the residue-line packing conjecture.

The stronger ABF/GG line-decodability predicate is also not implied by an
`LD_sw` bound.  The finite RS separation in
`experimental/notes/m2/m2_ldsw_line_decoding_separation.md` gives a
nonconstant received line with support-wise `LD_sw` contribution `0`, while an
adversarial close-codeword assignment violates `(delta,a_LD,n+1)`
line-decodability for every nonvacuous numerator.  Thus a genuine M2 theorem
needs an additional assignment-collinearity input beyond residue-line packing.
The structural reason is that every received line with codeword direction
`r+gamma v`, `v in C`, is invisible to `LD_sw`: all explaining supports also
explain the base and direction.  ABF/GG line-decodability can still fail because
the close-codeword assignment need not come from one affine code-line.  After
subtracting `gamma v`, the ABF/GG conclusion becomes an affine-graph incidence
problem inside the ordinary close list of the base word `r`.  The general
criterion is exact on code-direction lines, under the same greedy-extension
size hypothesis: if `G_b(L_a(r))` denotes the largest partial assignment from
slopes into the ordinary close list with no `b` points on an affine graph in
the code space, then the code-direction slice satisfies the trigger numerator
`a_LD` exactly when `G_b(L_a(r)) < a_LD` for every base word `r`.  The general
`m`-bucket obstruction gives the concrete failure threshold
`max(ceil(|F|/m),m)` for a base word with `m` close codewords.  Equivalently,
at collinearity threshold `b`, line-decodability on such code-direction lines
requires ordinary close-list size below `ceil(|F|/(b-1))` whenever that number
is at most `b-1`.  Conversely, if the close list has size at most
`floor((A-1)/(b-1))` for a trigger size `A`, pigeonhole already supplies the
required `b` agreeing slopes on code-direction lines.
More generally, `LD_sw` depends on the received direction only modulo `C`,
whereas ABF/GG line-decodability depends on the shifted close-codeword
assignment inside that quotient class.
For full-field code-direction assignments, when
`ceil(|F|/(b-1)) <= b-1`, this gives an exact criterion: the shifted close list
of every base word must have size below `ceil(|F|/(b-1))`.
In larger-field regimes, the necessary condition becomes geometric rather than
purely cardinal: the ordinary close list may not contain
`ceil(|F|/(b-1))` codewords with no `b` points on a nonconstant affine line in
the code space, since such an affine cap can be bucketed across the slopes to
defeat every `b`-slope code-line agreement.
For such a `b`-affine-cap close list `L`, the exact graph-free number is
`G_b(L)=min(|F|,(b-1)|L|)`.
If `|C| > binom(|F|,2)` and `b >= 3`, the same obstruction works at the actual
trigger numerator `a_LD`: a cap of size `ceil(a_LD/(b-1))` can be bucketed on
`a_LD` close slopes and greedily extended to the remaining slopes without
creating a `b`-point affine graph.
The exact `G_b` formulation is genuinely stronger than the affine-cap
necessary condition: a full affine code-line inside a close list already has
`G_b=|F|` for every `3 <= b <= |F|`, by the nonlinear parametrization
`gamma -> gamma^(b-1)` along that line.

## Follow-Up Checks

- The external `(delta,a_LD,n+1)` line-decoding definition used in ABF/GG is
  matched, source-conditionally, in
  `experimental/notes/m2/m2_abf_gg_line_decoding_parameter_match.md`.  In that
  convention `a_LD` is the line-decoding numerator, `b=n+1` is the
  collinearity threshold in the imported MCA implication, and the line-decoding
  section has no extra proximity-loss parameter.
- The converse direction is false: bounded `LD_sw` does not imply ABF/GG
  line-decodability.  See
  `experimental/notes/m2/m2_ldsw_line_decoding_separation.md`.
- Check whether protocol line-decoding imports have a common-support or
  code-line-proximity exception strong enough to avoid the spike-line
  close-point separation.

## Verifier

The script `experimental/scripts/m2_line_decoding_separation.py` verifies the
spike line on a tiny prime-field RS code by enumerating all degree-`<k`
codewords and all supports of size `n-1`:

```bash
python3 experimental/scripts/m2_line_decoding_separation.py
python3 experimental/scripts/m2_line_decoding_separation.py --format json
```
