# Packed primitive-profile flatness: finite Fourier-paving converse

## Status

```text
FINITE RAW-NORM PAVING: PROVED with constant 3+2*sqrt(2).
SCALED PACKING INFIMUM: exactly equal to the max-atom multiplier.
FULL-SLICE EXISTENTIAL PPF: equivalent to full-slice max-fiber flatness.
RESIDUAL EXISTENTIAL PPF: equivalent to exact primitive-profile Q.
SOURCE-SPECIFIC MANY-SHELL MAX-ATOM BOUND: OPEN.
```

This note supplies the converse to the integrated character-frame compiler.
Existential packed flatness is not a separate weaker analytic theorem: up to a
universal raw-norm constant, it is max-atom flatness.  What may remain useful
as a distinct proof object is a succinct source-algebraic packing certificate;
that additional complexity restriction is not part of the existential theorem.

## 1. Finite setup

Let `V` be a finite abelian group, let `Gamma=hat(V)`, and put

```text
Q = |V| = |Gamma|.
```

Let `xi:V->[0,infinity)` be a subprobability measure and choose an integer `L`
with

```text
|supp(xi)| <= L <= Q.
```

For nonempty `A subset Gamma`, define

```text
K_A(gamma,gamma') = hat_xi(gamma' gamma^{-1}),
hat_xi(chi)        = sum_z xi(z) chi(z),
kappa_L(xi)        = L ||xi||_infinity.
```

## 2. Exact scaled identity and nontrivial raw paving

### Theorem

For every such `(V,xi,L)`:

```text
inf_{A subset Gamma, |A|>=L}
  (L/|A|) ||K_A||_op
    = kappa_L(xi).                                  (FP1)
```

Moreover, there exists `A subset Gamma` with

```text
|A| >= L,
||K_A||_op <= (3+2*sqrt(2)) kappa_L(xi).            (FP2)
```

The equality `(FP1)` is elementary.  The substantive assertion is the raw
operator-norm estimate `(FP2)`: the complete dual attains `(FP1)` but may have
raw norm `Q||xi||_infinity`, which is exponentially larger than `(FP2)` when
`Q/L` is exponential.

## 3. Rayleigh lower bound and the exact infimum

For `z in V`, define

```text
c_z = (conj(gamma(z)))_{gamma in A}.
```

Then `||c_z||_2^2=|A|` and

```text
K_A = sum_z xi(z) c_z c_z^*.
```

Every summand is positive semidefinite, so

```text
||K_A||_op >= |A| xi(z).
```

Maximizing over `z` gives

```text
(L/|A|)||K_A||_op >= L||xi||_infinity.             (FP3)
```

For `A=Gamma`, character orthogonality gives

```text
||K_Gamma||_op = Q||xi||_infinity,
```

and hence

```text
(L/Q)||K_Gamma||_op = L||xi||_infinity.
```

This proves `(FP1)` exactly.  In particular, a finite verifier that minimizes
only the scaled quantity will always report ratio one from the complete dual;
that calculation does not test the nontrivial paving theorem.

## 4. MSS proof of the raw-norm bound

Let `S=supp(xi)` and, for `gamma in Gamma`, define the restricted unweighted
Fourier vector

```text
u_gamma = Q^{-1/2}(gamma(z))_{z in S} in C^S.
```

Character orthogonality gives

```text
sum_{gamma in Gamma} u_gamma u_gamma^* = I,
||u_gamma||_2^2 = |S|/Q <= L/Q.                    (FP4)
```

Marcus--Spielman--Srivastava, Corollary 1.5, states that if

```text
sum_i u_i u_i^* = I,   ||u_i||_2^2 <= delta,
```

then for every positive integer `r` there is a partition into `r` parts such
that every part satisfies

```text
||sum_{i in A_j} u_i u_i^*||_op
  <= (1/sqrt(r)+sqrt(delta))^2.                    (MSS)
```

If `Q<2L`, take `A=Gamma`.  Then

```text
||K_A||_op = Q||xi||_infinity < 2L||xi||_infinity,
```

which is stronger than `(FP2)`.

Suppose `Q>=2L` and put `r=floor(Q/L)`.  Apply `(MSS)` to `(FP4)`.  Since
the `r` parts contain all `Q` characters, one part `A` has

```text
|A| >= Q/r >= L.                                   (FP5)
```

Let `D=diag(xi(z))_{z in S}` and

```text
w_gamma = (sqrt(xi(z)) gamma(z))_{z in S}
        = sqrt(Q) D^{1/2}u_gamma.
```

The nonzero eigenvalues of the Gram matrix `K_A` are those of the frame
operator `sum_{gamma in A}w_gamma w_gamma^*`.  Therefore

```text
||K_A||_op
 <= Q||xi||_infinity
      (1/sqrt(r)+sqrt(L/Q))^2.                     (FP6)
```

Writing `x=Q/L`, one has `x>=2` and `r=floor(x)>=x/2`, so

```text
Q(1/sqrt(r)+sqrt(L/Q))^2
 = L(sqrt(x/r)+1)^2
 <= (3+2*sqrt(2))L.
```

Substitution into `(FP6)` proves `(FP2)`.

The MSS partition uses only the support `S` through the unweighted restricted
Fourier frame.  This is an existential support-dependent selection, not an
efficient algorithm or a succinct source-algebraic description.

## 5. Full-slice consequence

For a full profile slice, let

```text
mu(z) = |Omega^0 intersect Phi^{-1}(s0+z)| / M,
L     = |Phi(Omega^0)|,
barN  = M/L.
```

Then

```text
kappa_L(mu)
 = L max_z mu(z)
 = max_z |Omega^0 intersect Phi^{-1}(s0+z)| / barN. (FP7)
```

If existential PPF supplies `|A|>=exp(-a_N N)L` and
`||K_A||_op<=exp(b_N N)`, the Rayleigh bound gives

```text
kappa_L(mu) <= (L/|A|)||K_A||_op <= exp((a_N+b_N)N).
```

Thus PPF implies full-slice max-fiber flatness.  Conversely, if
`(FP7)=exp(o(N))`, `(FP2)` supplies `|A|>=L` and
`||K_A||_op=exp(o(N))`.  Hence

```text
full-slice existential PPF
  <=> full-slice image-normalized max-fiber flatness. (FP8)
```

The equivalence is uniform profile-wise because the factor `3+2*sqrt(2)` is
universal.

## 6. Residual consequence

For the semantic residual define the subprobability measure

```text
nu(z) = |Omega^circ intersect Phi^{-1}(s0+z)| / M.
```

Use the same full-slice image size `L`.  Since `|supp(nu)|<=L`, the finite
theorem applies and

```text
kappa_L(nu)
 = L max_z nu(z)
 = max_z |Omega^circ intersect Phi^{-1}(s0+z)| / barN. (FP9)
```

Therefore

```text
residual existential PPF <=> exact primitive-profile Q. (FP10)
```

This is a constant-factor finite equivalence, not merely a logarithmic-moment
implication.

## 7. Heavy-atom obstruction family

The Rayleigh lower bound is quantitatively sharp enough to rule out the hope
that a clever packing can conceal one exponentially heavy atom.  Take

```text
V_N = (Z/2Z)^N,   L_N = |V_N| = 2^N,
mu_N(0) = 1/2,
mu_N(z) = 1/(2(L_N-1)) for z != 0.
```

This is a full-support probability measure, but

```text
kappa_{L_N}(mu_N) = L_N/2 = 2^{N-1}.              (FP11)
```

For every character family `A`, `(FP3)` gives

```text
||K_A||_op >= |A|/2.                              (FP12)
```

In particular, every image-scale family with
`|A|>=exp(-o(N))L_N` has exponentially large raw norm.  MSS supplies a family
within the universal factor of this floor; it cannot turn the floor into a
subexponential estimate.  This family is a symbolic regression against any
future claim that unrestricted character selection bypasses a heavy atom.

## 8. Full-slice/residual separation family

The same example cleanly separates the two measures used by the proof
program.  Remove the heavy atom but retain the full-slice normalization:

```text
nu_N(0) = 0,
nu_N(z) = 1/(2(L_N-1)) for z != 0.
```

Then `nu_N` is a subprobability measure of total mass `1/2`, supported on
`L_N-1` image points, and

```text
kappa_{L_N}(nu_N)
  = L_N/(2(L_N-1))
  <= 2/3.                                         (FP13)
```

Thus full-slice existential PPF fails exponentially for `mu_N`, while
residual PPF and exact residual Q hold with a constant for `nu_N`.  The example
shows why the converse must state explicitly whether its measure is the full
pushforward `mu` or the semantic residual subprobability `nu`.  It also shows
that residual deletion can be mathematically decisive even though the scale
`barN=M/L` remains fixed by the full slice.

## 9. One-way bridge from the current signed large-sieve target

Write `(MF564)` for the max-atom conclusion that the technical signed
multilevel large-sieve input of PR #564 is designed to imply:

```text
L_lambda ||nu_lambda||_infinity <= exp(o(N_lambda))
```

uniformly over the semantically residual many-shell profiles.  Equations
`(FP9)` and `(FP10)` give the exact logical chain

```text
#564 signed large-sieve input
  => MF564
  <=> residual PPF
  <=> exact primitive-profile Q.                      (FP14)
```

The implication `MF564 => residual PPF` uses `(FP2)` and loses only the
universal factor `3+2*sqrt(2)`.  The reverse implication uses the Rayleigh
lower bound `(FP3)`.  Consequently, existential PPF neither weakens nor
independently advances the max-atom conclusion sought by the large-sieve lane.
A proof of the technical signed large-sieve input closes all three max-atom
formulations.  Conversely, unrestricted residual PPF recovers `MF564`, but it
does not necessarily recover PR #564's particular technical large-sieve
estimate; no such reverse implication is claimed.

## 10. Consequence for the proof program

The integrated character-frame compiler, converse guardrail, and strict
separation from global absolute Fourier summation remain correct.  The status
of its proposed next target changes:

```text
global absolute MI+MA can be exponentially weaker than Q/PPF;
existential PPF itself is equivalent to max-atom flatness;
searching for an unrestricted packed family cannot bypass a heavy atom.
```

The block-parabola product still demonstrates the first statement.  It
separates global absolute summation from Q/PPF, not PPF from Q.

The substantive source theorem remains

```text
L||mu||_infinity = exp(o(N))
```

for full-slice flatness, or

```text
L||nu||_infinity = exp(o(N))
```

for exact residual Q.  In the current cyclic max-fiber lane, PR #564 reduces
the relevant source theorem to a signed multilevel large-sieve input and
explicitly leaves that estimate open.

PPF remains distinct only after adding a real certificate-complexity
restriction, for example requiring `A` to be a succinct linear, product,
subspace-evasive, or bounded-circuit family whose norm bound follows from
named source-algebra certificates.  No such restricted equivalence is claimed
here.

## 11. Claim boundary

Proved:

```text
exact scaled-infimum identity (FP1);
universal raw-norm paving bound (FP2);
full-slice existential PPF/max-atom equivalence;
residual existential PPF/exact-Q equivalence.
```

Not proved:

```text
the many-shell source max-atom theorem;
the signed multilevel large-sieve input of PR #564;
an efficient MSS partition algorithm;
a succinct source-algebraic packed certificate;
first-match exhaustiveness, remaining ray compilation, or envelope closure.
```

## 12. Reference

A. W. Marcus, D. A. Spielman, and N. Srivastava, *Interlacing Families II:
Mixed Characteristic Polynomials and the Kadison--Singer Problem*, Annals of
Mathematics 182 (2015), 327--350, Corollary 1.5; arXiv:1306.3969.

## 13. Reproducibility

```sh
python experimental/scripts/verify_asymptotic_packed_flatness_converse_v1.py --check
python experimental/scripts/verify_asymptotic_packed_flatness_converse_v1.py --tamper-selftest
```
