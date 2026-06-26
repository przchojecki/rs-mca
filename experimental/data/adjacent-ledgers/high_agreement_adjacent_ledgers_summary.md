# High-agreement adjacent ledgers

This packet extends the tangent staircase beyond finite-slope support-wise MCA.

## Results

Let `C = RS[F,D,k]`, `|D| = n`, `q = |F|`.

### 1. CA and projective-slope MCA

If

```text
3a - 2n >= k,
```

then the high-agreement tangent staircase pins three affine/projective line
quantities:

```text
LD_sw(C,a) = LD_ca(C,a) = LD_sw,proj(C,a) = n-a+1.
```

Here `LD_ca` is the no-loss correlated-agreement finite-slope count, and
`LD_sw,proj` allows the point at infinity in `P^1(F)`.

### 2. Degree-d curve MCA / curve-CA

For finite-parameter degree-`d` power curves

```text
W_gamma = f_0 + gamma f_1 + ... + gamma^d f_d,  gamma in F,
```

if

```text
(d+2)a - (d+1)n >= k,
```

then

```text
CurveLD_sw^(d)(C,a) = CurveLD_ca^(d)(C,a)
                    = min(q, d*(n-a+1)).
```

The lower bound is a degree-`d` tangent construction that assigns up to `d`
bad parameters to each residual coordinate.  The upper bound interpolates
`d+1` bad parameters to recover a common code-curve on a large intersection,
then charges residual roots; each residual coordinate contributes at most `d`
bad parameters.

### 3. Interleaved-list uniqueness

For every interleaving arity `mu >= 1`, if

```text
2a - n >= k,
```

then

```text
Lambda_mu(C,a) = 1.
```

This is the ordinary MDS unique-decoding argument applied row-wise to common
agreement supports.

## F_17^32, n=512, k=256 consequences

Let

```text
C = RS[GF(17^32), H, 256], |H| = 512.
```

Then

```text
floor(17^32 / 2^128) = 6.
```

The high-agreement ledgers are:

```text
LD_sw(C,a) = LD_ca(C,a) = LD_sw,proj(C,a) = 513-a,  for a >= 427.
Lambda_mu(C,a) = 1,                                  for a >= 384.
CurveLD^(d)(C,a) = d*(513-a)                         in the degree-d curve range.
```

Thus, for a protocol whose coding error is exactly one affine/projective
line CA/MCA term plus one interleaved-list term, with no query/folding error,
the combined numerator is

```text
(513-a) + 1 = 514-a.
```

So:

```text
a=507: line numerator 6 + list numerator 1 = 7  -> unsafe for 2^-128
a=508: line numerator 5 + list numerator 1 = 6  -> safe for 2^-128
```

For degree-`d` curves plus the interleaved list term, the condition is

```text
d*(513-a) + 1 <= 6.
```

Consequences:

```text
d=1: safe with list iff a >= 508
d=2: safe with list iff a >= 511
d=3,4,5: safe with list only at a = 512
d>=6: no safe grid point with the list term
```

## Challenge-map pullback ledger

The line and curve statements above are sampler statements over their actual
parameter set `X`: finite slopes, projective slopes, or finite curve
parameters.  A protocol challenge set `K` inherits such a statement only
through an explicit map

```text
phi : K -> X.
```

If a theorem bounds the bad parameter set by `L`, the pulled-back failure
probability is

```text
|phi^{-1}(Bad)| / |K|.
```

Thus, if every fiber has size at most `m`, then

```text
Pr_chal[bad] <= min(|K|, L*m) / |K|.
```

The exact size-only envelope is sharper.  If the nonzero fiber sizes of `phi`
are

```text
s_1 >= s_2 >= ... >= s_M > 0,
```

then the worst bad set of at most `L` parameters has probability exactly

```text
(s_1 + ... + s_min(L,M)) / |K|.
```

A degree certificate gives one common usable form: a nonconstant polynomial
map, or a reduced rational map to `P^1`, of degree `D` has every fiber of size
at most `D`.  A linear certificate gives another: if `phi:F_q^e -> V` is
`F_q`-linear of rank `r`, then every nonempty fiber has size `q^(e-r)`, the
image has size `q^r`, and the effective denominator is exactly `q^r`.

For the active `F_17^32` row, this rank ledger is unforgiving:

```text
floor(17^32 / 2^128) = 6,
floor(17^31 / 2^128) = 0.
```

So a full-rank `F_17`-linear challenge map into the analyzed slope field keeps
the printed budget `6`, while any rank loss to at most `31` dimensions gives
no positive bad-parameter budget at `2^-128`.  Trace maps, coordinate
projections, and other rank-deficient maps therefore recover only their image
denominator; they do not justify silently dividing by the full challenge-field
size.

Equivalently, for any protocol ledger that charges a total integer
bad-parameter numerator `N` against this same sampler, a rank-`r` linear
challenge map over `F_17` gives the target condition

```text
N <= floor(17^r / 2^128).
```

For the active line-plus-list ledger,

```text
N_line+list(a) = 514-a.
```

For the degree-`d` curve-plus-list ledger,

```text
N_curve+list,d(a) = d*(513-a) + 1.
```

At full rank `r=32`, these reproduce the printed thresholds.  At every
rank `r<=31`, the effective budget is zero, so no positive-numerator coding
ledger of this form can meet a `2^-128` target.  This is a rank-aware
protocol-ledger statement, not a new coding theorem: it applies only after the
protocol reduction has identified which printed coding numerators are charged
to the same sampled parameter.

The same envelope also fixes how multiple adjacent terms compose.  If several
bad-parameter ledgers are charged to the same challenge and the same sampler
with total integer numerator

```text
N = N_1 + ... + N_s,
```

then the shared-challenge union bound is the single envelope evaluated at `N`.
For a rank-`r` linear sampler this is

```text
min(N,17^r) / 17^r.
```

This is the calculation used by the line-plus-list and curve-plus-list rows
above.  If instead the protocol uses separate challenge maps

```text
phi_i : K_i -> X_i,
```

the union bound is the sum of the separate envelopes,

```text
Pr[any bad term] <= Envelope(phi_1,N_1) + ... + Envelope(phi_s,N_s).
```

Those denominators do not multiply for a union event; a product denominator is
available only for an intersection-style event with independence that the
protocol proof actually consumes.

The result is not a general SNARK theorem.  It is a coding-ledger theorem for
protocol reductions that consume exactly the printed coding terms over the
printed field, plus any separately added query/folding/cryptographic errors.
