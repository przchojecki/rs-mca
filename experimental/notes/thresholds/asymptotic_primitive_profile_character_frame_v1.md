# Primitive-profile character-frame certificate

## Status

`PROVED CONDITIONAL CERTIFICATE / OPEN SOURCE-SPECIFIC PACKING INPUT`.

The original status string is retained for the integrated verifier.  Here
`SOURCE-SPECIFIC PACKING INPUT` means the named major/minor or succinct
source-algebraic construction in this packet, not unrestricted existential
selection of an arbitrary character subset.

**Subsequent converse.**  The existential packing target is superseded by
`asymptotic_primitive_profile_packed_flatness_converse_v1.md`.  MSS paving of
the restricted complete Fourier frame proves that a family of image-scale
size and subexponential raw Gram norm exists if and only if the relevant
full-slice or residual max-atom multiplier is subexponential.  The compiler,
Rayleigh guardrail, packed major/minor sufficient condition, and block-product
separation below remain correct; the unrestricted existence of a packed
family is no longer a distinct source theorem.

This note proves a finite character-frame implication and a packed
major/minor corollary.  It does **not** prove exact primitive-profile Q,
effective `(MI)+(MA)`, or the direct Sidon payment in the unrestricted
many-shell range.  The remaining source-specific assertion is the existence,
uniformly over the semantic primitive profiles, of a sufficiently large
character family with subexponential Gram norm.

## Relation to the current frontiers package

The active manuscript performs Fourier inversion on the effective difference
span

```text
V_g = Span_Fp { g(t)-g(t0) : t in T },
A_eff = |V_g|,
```

not on an ambient coefficient space.  It currently pays flatness by the
absolute Fourier interfaces `(EFP)`, `(MI)`, and `(MA)`.  A major-character
label is explicitly not an aggregate estimate.  The direct Sidon payment is
also still open outside the ranges printed in the manuscript.

The result below supplies a different sufficient interface.  It can use a
large, well-conditioned subset of the effective dual rather than summing the
absolute values of every effective Fourier coefficient.  This is potentially
useful when a structured major-difference locus can be avoided by character
packing.  It is not asserted to exist for every current source profile.

## Effective affine setup

Let `G` be a finite abelian group, let `Omega` be a finite full profile slice,
and let

```text
Phi : Omega -> s0 + G
```

be its profile map.  Translate by `s0` and put

```text
M       = |Omega|,
S       = { Phi(x)-s0 : x in Omega },
L       = |S|,
mu(z)   = |{x in Omega : Phi(x)-s0=z}| / M,
barN    = M/L.
```

In the frontiers application, `G=V_g`, `|G|=A_eff`, and `Omega` is the full
fixed-weight slice.  Any semantic first-match residual is a subset of the full
slice, so its fiber over `z` is no larger than the corresponding full-slice
fiber.

For a character `gamma in G^`, use

```text
hat_mu(gamma) = sum_z mu(z) gamma(z).
```

The affine translation is required: characters are evaluated at
`Phi(x)-s0`, not at an expression that assumes the realized image is itself a
subgroup.

## The character-frame theorem

### Theorem

Let `A` be a nonempty subset of the effective dual `G^`.  Define its Gram
matrix by

```text
K_A(gamma,gamma') = hat_mu(gamma' gamma^{-1}).
```

Then every full-slice fiber, and hence every residual fiber contained in it,
satisfies

```text
|F_z| <= M ||K_A||_op / |A|
      = (L ||K_A||_op / |A|) barN.                 (CF1)
```

Consequently, exact primitive-profile Q follows from the source-specific
uniform input

```text
|A| >= exp(-o(N)) L,
||K_A||_op <= exp(o(N)).                            (CF2)
```

### Proof

Work in `l2(Omega)` with counting measure.  For `gamma in A`, define

```text
v_gamma(x) = M^{-1/2} gamma(Phi(x)-s0).
```

Each `v_gamma` is a unit vector and

```text
<v_gamma,v_gamma'> = hat_mu(gamma' gamma^{-1}),
```

so `K_A` is their Gram matrix.  For a nonempty fiber `F_z`, put

```text
u_z = 1_{F_z}/sqrt(|F_z|).
```

Since the profile is constant on `F_z`,

```text
|<u_z,v_gamma>|^2 = |F_z|/M
```

for every `gamma in A`.  If `T` is the analysis operator
`Tf=(<f,v_gamma>)_gamma`, then

```text
|A| |F_z|/M = ||T u_z||_2^2
             <= ||T||^2
             = ||T T^*||_op
             = ||K_A||_op.
```

This proves `(CF1)`.  Substituting `(CF2)` proves the image-normalized
subexponential bound.  Deleting supports cannot enlarge a full-slice fiber.

## Converse guardrail

For every `z in S`, the Gram decomposition gives

```text
||K_A||_op >= |A| mu(z).
```

Indeed, use the character-value vector at `z` as a Rayleigh test vector;
the contribution of the atom `mu(z)` alone is `|A| mu(z)`, and all other
terms are nonnegative.  Therefore

```text
L ||K_A||_op / |A| >= L max_z mu(z).                (CF3)
```

Thus no character family can certify a multiplier below the true full-slice
max-fiber multiplier.  In particular, the criterion is not a relabeling trick
that can hide a heavy fiber.  Taking the whole dual makes this exact:

```text
||K_{G^}||_op = |G| max_z mu(z).
```

This identity also shows why the full-dual operator norm is not itself an
independent proof of Q; an independently bounded subfamily or structured
operator estimate is required.

## Packed major/minor corollary

Let `Mfrak` be a symmetric subset of `G^` containing the identity.  Interpret
it as a set of forbidden character differences.  The Cayley graph with

```text
gamma ~ gamma' iff gamma' gamma^{-1} in Mfrak - {1}
```

has maximum degree at most `|Mfrak|-1`, so it has an independent set `A`
with

```text
|A| >= |G^|/|Mfrak|.                                (CF4)
```

All off-diagonal differences of this `A` avoid `Mfrak`.  If

```text
|Mfrak| <= exp(o(N)) |G^|/L                         (CF5)
```

and

```text
max_gamma sum_{gamma' in A, gamma' != gamma}
  |hat_mu(gamma' gamma^{-1})| <= exp(o(N)),          (CF6)
```

then Gershgorin gives `||K_A||_op <= exp(o(N))`, while `(CF4)-(CF5)` give
`|A| >= exp(-o(N))L`.  The character-frame theorem proves Q.

This is strictly more targeted than requiring an all-character absolute
Fourier sum: only one packed difference set must be controlled.  Current
effective `(MI)` is one sufficient way to prove `(CF6)`, because for a fixed
row the map `gamma' -> gamma' gamma^{-1}` is injective and all off-diagonal
differences are minor.  The new source-specific burden is then the packing
estimate `(CF5)`, or a direct construction of `A` satisfying `(CF2)`.

For a finite row, the exact certified image multiplier is

```text
kappa_frame = L B_A / |A|,
```

where `B_A` is any proved upper bound for `||K_A||_op`; the maximum absolute
Gram row sum is a valid verifier-friendly choice.

## Executable evidence

The companion verifier enumerates small fixed-weight power-sum profiles.  It
computes the full image distribution, effective Fourier coefficients, a
greedy forbidden-difference packing, the exact finite Gram row-sum bound, and
the actual image-normalized max-fiber multiplier.

The committed census records:

* strict packed-frame improvement over the all-character absolute-sum
  multiplier on multiple toys;
* nonuniform-fiber cases, not only injective maps;
* the exact guardrail `actual_multiplier <= frame_multiplier` in every case;
* a synthetic heavy-atom regression for which `(CF3)` prevents a false
  flatness certificate.

The verifier also replays all five elementary-symmetric prefix rows from
`verify_boolean_prefix_fibers.py`:

```text
F5  n5  m2 w1
F11 n10 m5 w2
F13 n10 m5 w2
F17 n8  m4 w1
F17 n12 m6 w2
```

All five satisfy the frame and converse checks, and four have nonuniform
fibers.  None chooses a nontrivial forbidden-difference packing under the
deterministic threshold rule; its best certificate uses the full dual.  This
negative control is retained to avoid presenting the strict block-family
separation as a universal phenomenon on small prefix toys.

These finite cases show that the criterion is nonvacuous.  They do not prove
the uniform asymptotic packing input for the many-shell source profiles.

## A scalable separation from global absolute summation

The repository's block-profile toys fix an occupancy inside each block.  On
that existing profile model, the character-frame route has an exact scalable
advantage over global `(MI)+(MA)` absolute summation.

Fix an odd prime `p`.  For `k>=1`, take `k` disjoint blocks, each identified
with `F_p`, and require exactly one selected point in each block.  Thus

```text
Omega_k = (F_p)^k,
N_k     = p k,
m_k     = k.
```

Use the blockwise power-sum profile

```text
Phi_k(t_1,...,t_k)
  = ((t_1,t_1^2),...,(t_k,t_k^2))
  in G_k = (F_p^2)^k.
```

The effective difference span is all of `G_k`.  The profile is injective, so

```text
M_k = L_k = p^k,
mu_k is uniform on the product of k parabolas.
```

For the effective-span assertion, anchor each block at `t=0`.  In one block,
the two difference vectors at `t=1` and `t=-1` are `(1,1)` and `(-1,1)`.
Their determinant is `2`, which is nonzero because `p` is odd.  They span
`F_p^2`, and the disjoint block coordinates give all of `G_k`.

For one block, the normalized Fourier coefficient at `(a,b)` is

```text
p^{-1} sum_t exp(2 pi i (a t+b t^2)/p).
```

It equals `1` at `(0,0)`, equals `0` when `b=0` and `a!=0`, and has absolute
value `p^{-1/2}` when `b!=0`, by the quadratic Gauss-sum evaluation.  Hence
the one-block absolute Fourier mass is

```text
C_p = 1 + (p-1) sqrt(p).
```

For completeness, when `b!=0`, completing the square reduces the magnitude to
that of `sum_t psi(b t^2)`.  Its squared magnitude is

```text
sum_{u,v} psi(b(u^2-v^2))
  = sum_{r,s} psi(b r s)
  = p,
```

because `(u,v) -> (r,s)=(u-v,u+v)` is bijective in odd characteristic, and
the inner sum over `s` is `p` for `r=0` and zero otherwise.  Thus the
normalized magnitude is exactly `p^{-1/2}`.

Product factorization gives the exact global effective Fourier multiplier

```text
kappa_abs(k) = C_p^k.
```

Since `N_k=pk`,

```text
log(kappa_abs(k))/N_k = log(C_p)/p > 0.
```

Therefore a global `(MI)+(MA)` absolute sum over all effective characters is
exponential in `N_k` and is inconclusive for a subexponential flatness target,
regardless of how those same absolute terms are partitioned into minor and
major sets.

Now choose

```text
A_k = { ((a_1,0),...,(a_k,0)) : a_i in F_p }.
```

Then `|A_k|=p^k=L_k`.  For two distinct characters in `A_k`, some blockwise
difference is `(a,0)` with `a!=0`, whose Fourier coefficient is zero.  Thus

```text
K_{A_k} = I,
||K_{A_k}||_op = 1,
kappa_frame(k) = L_k/|A_k| = 1.
```

The packed frame certificate is exact for every `k`, while the global
absolute-sum certificate loses `exp((log C_p/p)N_k)`.

The verifier checks the base Gauss magnitudes for `p=3,5,7`, explicitly
enumerates the product distribution and Gram rows through `k=2`, and prints
the scalable rows `k=1,2,4,8,16`.  For `p=5`, the global loss rate is
approximately `0.4593` per ambient coordinate, while the packed multiplier
remains one.

This is an interface-separation family, not a claimed semantic primitive
residual: its visible block occupancy may be routed by an earlier structural
cell in the final atlas.  Its role is to prove that the packed theorem can
close a family on which the current global absolute Fourier interface, taken
literally, cannot deliver a subexponential bound.

## Claim boundary and next target

Proved here:

```text
finite character-frame inequality;
converse Rayleigh lower bound;
packed forbidden-difference corollary;
exact finite row-sum multiplier;
deterministic toy replay and tamper checks.
scalable block-parabola separation from global absolute summation.
```

Not proved here:

```text
exact primitive-profile Q in the unrestricted many-shell range;
existence of a packed character family for every semantic residual profile;
the source-specific major-difference cardinality bound (CF5);
the packed minor Gram bound (CF6);
effective (MI), effective (MA), or the direct Sidon moment input;
witness-exhaustiveness of the first-match atlas.
semantic residuality of the block-parabola separation family.
```

The former next target was the source-derived existential statement:

```text
For every semantically residual many-shell profile, construct
A_lambda subset of hat(V_g) such that

  |A_lambda| >= exp(-o(N_lambda)) L_lambda,
  ||K_{A_lambda}||_op <= exp(o(N_lambda)),

uniformly over the required frontier window.
```

The subsequent finite converse shows that, without a certificate-complexity
restriction, this statement is equivalent to the corresponding max-atom
bound.  The actual open target is therefore the source many-shell max-fiber
theorem itself, currently reduced in the cyclic lane to the signed multilevel
large-sieve input, or a genuinely restricted succinct algebraic packing
certificate.

## Reproducibility

```sh
python experimental/scripts/verify_asymptotic_primitive_profile_character_frame_v1.py --check
python experimental/scripts/verify_asymptotic_primitive_profile_character_frame_v1.py --tamper-selftest
```
