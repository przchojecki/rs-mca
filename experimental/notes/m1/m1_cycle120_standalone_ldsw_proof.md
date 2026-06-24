# M1 Cycle120 Standalone LDsw Proof

Status: PROVED / COMPUTATION-DEPENDENT / SOURCE-CONDITIONAL.

Date: 2026-06-24.

This note isolates the human-readable proof requested after the Cycle84--120
generated archive was rejected as nonmergeable.  The finite Cycle84 product
count is treated as the computational input; the proof below shows that this
input gives the Cycle120 support-wise bad-line lower bound.

The companion verifier is:

```text
python3 experimental/scripts/verify_m1_cycle120_standalone_ldsw_proof.py
```

It is nonmutating.  It checks the deterministic arithmetic, checks the generic
fixed-jet and smooth-padding transfer lemmas on exact small prime-field models,
and checks that the existing Cycle84 public replay audit records the finite
input used here.

## Target Theorem

Let

```text
K = F_17^32,
H = <theta> <= K^*,
|H| = 512,
C = RS[K,H,256],
N = 52,747,567,092.
```

Assume the Cycle84 finite-model theorem:

```text
#{Phi(T)} = N
```

for the seven-slot color-filtered family used in the Cycle116 construction,
and assume the Cycle116 slot identities and field facts recorded in the
Cycle84/Cycle116 audit.  Then

```text
LD_sw(C,262) >= N.
```

Consequently, under the printed ABF same-support grand-MCA convention,

```text
epsilon_mca(C,125/256) >= N / 17^32 > 2^-128.
```

This is not an ordinary list-decoding claim and it is not an accepted prize
solution.  It is a concrete finite obstruction to the printed ABF inequality
for this one smooth row, conditional on the finite Cycle84 computation and the
ABF source gates.

## Definitions Used Here

For a Reed--Solomon code `RS[F,D,k]`, write `LD_sw(C,a) >= M` to mean that
there is one affine line `f + z g` and at least `M` distinct parameters `z`
such that, for each such `z`, the line point `f+zg` agrees with a codeword on
some support `S_z` of size at least `a`, while the pair `(f,g)` is not
simultaneously code-explained on that same support.

This is the support-wise line-MCA predicate used by the Cycle120 ABF-facing
ledger.

## Lemma 1: Fixed-Jet Locator Transfer

Let `D` be an `n`-point subset of a field `F`, let `beta notin D`, and let
`J` range over a family of `j`-subsets of `D`.  Put

```text
P_J(X) = prod_{a in J}(X-a).
```

Assume:

```text
deg(P_J-P_J') <= j-sigma       for all J,J',
sigma >= 1,
k = n-j-sigma,
P_J(beta) != 0                 for all J.
```

Then

```text
LD_sw(RS[F,D,k], n-j) >= #{P_J(beta): J}.
```

### Proof

Let

```text
L_D(X)=prod_{x in D}(X-x).
```

Use the standard weighted Vandermonde parity check

```text
(Hw)_m = sum_{x in D} x^m w(x) / L_D'(x),   0 <= m < j+sigma.
```

Its kernel is `RS[F,D,k]`, since the redundancy is `j+sigma=n-k`.

For a co-support `J`, define an error word supported on `J` by

```text
e_J(x) = L_D'(x) / ((beta-x) P_J'(x))     if x in J,
e_J(x) = 0                               if x notin J.
```

For each `m < j+sigma`, divide

```text
X^m = Q_{m,J}(X) P_J(X) + R_{m,J}(X).
```

The fixed top `sigma` coefficients imply that `Q_{m,J}` is independent of `J`;
write it as `Q_m`.  Lagrange interpolation on `J` gives

```text
(H e_J)_m
  = R_{m,J}(beta) / P_J(beta)
  = beta^m / P_J(beta) - Q_m(beta).
```

Set

```text
B_m = beta^m,
A_m = -Q_m(beta),
z_J = 1 / P_J(beta).
```

Then

```text
H e_J = A + z_J B.
```

Now define

```text
g(x)=L_D(beta)/(beta-x).
```

The same Lagrange identity gives `H g = B`.  Fix one co-support `J_0` and put

```text
f = e_{J_0} - z_{J_0} g.
```

For every `J`,

```text
H(f + z_J g - e_J) = 0.
```

Thus `f+z_J g` agrees with a codeword on `D\J`, which has size `n-j`.

It remains to prove support-wise noncontainment.  If `g` were code-explained on
`D\J`, then `g-h` would be supported on `J` for some degree `<k` codeword `h`.
Equivalently, the Vandermonde column at `beta` would lie in the span of the
columns indexed by `J`.  This is impossible because `J union {beta}` has
`j+1` distinct points and the parity-check space has `j+sigma >= j+1` rows.

Distinct values of `P_J(beta)` give distinct parameters `z_J`, proving the
lemma.

## Cycle116 Native Instance

The Cycle116 finite construction has a native domain `D0` of size `256` and
co-supports `J_T` of size `113`.  Its slot identities give

```text
P_T(X) = X^113 - X^112 + O(X^107).
```

Therefore the fixed-jet lemma applies with

```text
n = 256,
j = 113,
sigma = 6,
k = 256 - 113 - 6 = 137,
n-j = 143.
```

The same finite construction gives the evaluation identity

```text
P_T(beta) = 4(beta-1) Phi(T),
```

with `4(beta-1) != 0`.  Hence distinct `Phi(T)` values give distinct
`P_T(beta)` values.  The Cycle84 finite theorem therefore gives

```text
LD_sw(RS[F_17^16,D0,137],143) >= N.
```

The same line may be viewed over the quadratic extension `K=F_17^32`.
Support-wise noncontainment is preserved under this extension of scalars:
the interpolation equations for a degree `<137` explanation on a fixed
support have coefficients and right-hand side in `F_17^16`, so solvability
over `K` is equivalent to solvability over `F_17^16` by Gaussian elimination
over the base field.

## Lemma 2: Smooth Padding Transfer

Let `D,A,R` be disjoint sets in a field, put `H=D union A union R`, and let

```text
L_A(X)=prod_{a in A}(X-a).
```

Suppose one line `f+zg` is support-wise bad for `RS[F,D,k]` on supports
`S_z` of size at least `a`.  Define lifted words on `H` by

```text
f_+(x)=L_A(x) f(x),   g_+(x)=L_A(x) g(x)     for x in D,
f_+(x)=g_+(x)=0                              for x in A,
```

with arbitrary values on `R`.  Then the same parameters are support-wise bad
for `RS[F,H,k+|A|]` on supports

```text
S_z union A.
```

Indeed, if `c_z` explains `f+zg` on `S_z`, then `L_A c_z` has degree
`< k+|A|` and explains `f_+ + z g_+` on `S_z union A`.  Conversely, if `f_+`
and `g_+` were simultaneously explained on `S_z union A`, both explaining
polynomials would vanish on every point of `A`, hence would be divisible by
`L_A`; division by `L_A` would give simultaneous explanations of `f,g` on
`S_z`, contradiction.

## Cycle120 Smooth Row

The Cycle120 row uses

```text
H = <theta> = D0 disjoint_union theta D0,
|H| = 512.
```

Inside the odd coset, split off a padding block `A` of size `119`; the remaining
odd-coset points form `R` of size `137`.  Applying Lemma 2 to the Cycle116
native line gives

```text
143 + 119 = 262,
137 + 119 = 256.
```

Therefore

```text
LD_sw(RS[F_17^32,H,256],262) >= N.
```

This proves the target theorem, subject only to the finite Cycle84 input and
the stated Cycle116 field/slot identities.

## ABF Grand-MCA Consequence

At

```text
delta = 125/256,
n = 512,
```

the closed ABF support threshold is

```text
(1-delta)n = (131/256)512 = 262.
```

The line parameter is sampled from `K=F_17^32`, so the support-wise lower bound
gives

```text
epsilon_mca(C,125/256) >= N / 17^32.
```

Finally,

```text
floor(17^32 / 2^128) = 6,
N = 52,747,567,092 > 6.
```

Thus

```text
N / 17^32 > 2^-128.
```

## Proof Boundary

This note proves the transfer:

```text
Cycle84 finite count + Cycle116 slot identities
  => LD_sw(RS[F_17^32,H,256],262) >= 52,747,567,092.
```

It does not independently rerun the full Cycle84 census.  That finite
computation remains the separate computer-assisted input recorded in
`m1_cycle84_public_replay_audit.md`.

The strict-ball Cycle119 addendum would require the two-ended fixed-jet variant:

```text
LD_sw(RS[F_17^32,H,256],263) >= 52,747,567,092.
```

That stronger statement is compatible with this proof but is intentionally kept
out of the minimal closed-threshold proof above.
