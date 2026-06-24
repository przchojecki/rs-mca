# L1 Prefix Bad-Prime Certificate

Status: PROVED / FINITE-FIELD REDUCTION / NOT A FULL AGGREGATION BOUND.

Date: 2026-06-24.

Agent/model: Codex.

## Purpose

This note adds a finite-field bad-prime layer to the L1 monomial-prefix
program.  It is designed to sit after the characteristic-zero reductions and
before any density-over-primes theorem.

The result is deliberately narrow:

```text
finite-field prefix collision
  => characteristic-zero collision
     or p divides an explicit integer resultant certificate.
```

Thus every aperiodic finite-field collision template has a computable bad-prime
certificate.  This does not yet prove the L1 local limit, because one still
has to aggregate these certificates over all aperiodic templates.  It does give
the missing algebraic bridge requested in `agents.md`: convert finite-field
collisions into algebraic-integer divisibility or norm events.

The companion verifier is:

```text
python3 experimental/scripts/verify_l1_prefix_bad_prime_certificate.py
```

It is nonmutating and uses only the Python standard library.

## Setup

Fix `n`, let `zeta` be a primitive `n`-th root of unity, and let

```text
A,B subset Z/nZ,        |A|=|B|=m.
```

For `1 <= r <= m`, define the exponent elementary-sum polynomial

```text
E_r(A;T) = sum_{I subset A, |I|=r} T^{sum_{i in I} i}
```

viewed in `Z[T]/(T^n-1)`.  The top locator coefficients of

```text
L_A(X)=prod_{a in A}(X-zeta^a)
```

are, up to signs, the values `E_r(A;zeta)`.

Let `Phi_n(T)` be the cyclotomic polynomial.  For a pair `(A,B)` and prefix
length `sigma`, set

```text
Delta_r(T) = E_r(A;T)-E_r(B;T),        1 <= r <= sigma.
```

If every `Delta_r` vanishes modulo `Phi_n`, then `(A,B)` is a
characteristic-zero prefix collision.  Otherwise define

```text
C_n,sigma(A,B)
  = gcd_{1 <= r <= sigma, Delta_r not 0 mod Phi_n}
      |Res(Phi_n, Delta_r)|.
```

This is a nonzero integer.  It is invariant under the Galois/dilation action
`A -> uA`, `B -> uB` for `u in (Z/nZ)^*`, and under common translations
`A -> A+t`, `B -> B+t`, up to multiplication of each `Delta_r(zeta)` by a
cyclotomic unit.

## Theorem: Split Bad-Prime Certificate

Let `p` be a prime with `p not dividing n` and `n | p-1`, and let
`h in F_p^*` have order `n`.  Suppose the reductions of `A` and `B` collide in
the finite-field monomial-prefix map:

```text
E_r(A;h) = E_r(B;h) in F_p,        1 <= r <= sigma.
```

Then either `(A,B)` is a characteristic-zero prefix collision, or

```text
p | C_n,sigma(A,B).
```

### Proof

The element `h` has order `n`, so it is a root of `Phi_n` modulo `p`.
For each `r <= sigma`, the finite-field collision hypothesis says that `h` is
also a root of `Delta_r` modulo `p`.

If `Delta_r` is not zero modulo `Phi_n`, the two integer polynomials
`Phi_n` and `Delta_r` have a common root modulo `p`.  Therefore their resultant
vanishes modulo `p`:

```text
Res(Phi_n, Delta_r) = 0 mod p.
```

This holds for every nonzero cyclotomic remainder among the `Delta_r`.  Hence
`p` divides their gcd, namely `C_n,sigma(A,B)`.  If no such nonzero remainder
exists, all `Delta_r` vanish at `zeta`, which is exactly a
characteristic-zero prefix collision.  This proves the theorem.

## General Finite-Field Form

The split hypothesis is only needed later for row accounting inside `F_p`.
The bad-prime divisibility statement itself works over any finite field.

Let `K` be a finite field of characteristic `p`, with `p not dividing n`, and
let `h in K^*` have exact order `n`.  If

```text
E_r(A;h) = E_r(B;h) in K,        1 <= r <= sigma,
```

then either `(A,B)` is a characteristic-zero prefix collision, or

```text
p | C_n,sigma(A,B).
```

The proof is the same.  The element `h` is a common root in an extension of
`F_p` of `Phi_n` and every active `Delta_r`; hence each active resultant
vanishes modulo `p`.

The verifier includes a non-split witness:

```text
K = F_9 = F_3[i]/(i^2+1),
n = 8,
h = 1+i,
A = {0,1},
B = {2,5},
sigma = 1.
```

Here `h` has order `8`, so `K` contains primitive eighth roots even though
`8` does not divide `3-1`.  The two templates collide over `F_9`, do not
collide in characteristic zero, and have

```text
C_8,1(A,B) = 36 = 2^2 * 3^2.
```

Modulo `3`, the common-root gcd has degree `2`, representing the quadratic
prime-ideal factor rather than two rational split embeddings.  This is why the
split-prime support list is empty while the rational bad prime `3` is still
detected by the certificate.

The same degree accounting also extends to nonsplit primes.  Let `f` be the
order of `p` modulo `n`, so that all primitive `n`-th roots lie in
`F_{p^f}`.  Because `p` does not divide `n`, `Phi_n` is squarefree modulo `p`;
therefore

```text
deg gcd(Phi_n, Delta_1, ..., Delta_sigma) in F_p[T]
```

counts the primitive roots in `F_{p^f}` where the template collides.  The root
set is stable under Frobenius `alpha -> alpha^p`, and every primitive
`n`-th-root Frobenius orbit has size exactly `f`.  Hence `deg G_p(A,B)` is a
multiple of `f`, and

```text
deg G_p(A,B) / f
```

is the number of prime ideals above `p` at which the template collides.
Summing over unordered template pairs gives

```text
sum_{A<B} deg G_p(A,B)
  = sum_{h primitive in F_{p^f}} |Coll(h)|.
```

The split-prime row-accounting identity is the special case `f=1`.

For the `F_9` witness row with `n=8`, `m=2`, and `sigma=1`, the verifier checks
all four primitive eighth roots.  Each root has `30` collision pairs, so there
are `120` root-template incidences.  The modular gcd ledger over `F_3` has the
same weighted mass: `48` non-characteristic-zero pairs have degree `2`, and
`6` characteristic-zero pairs have degree `4`.  Since `ord_8(3)=2`, this is
equivalently `48` one-prime-ideal pairs and `6` two-prime-ideal pairs, for
total rational-prime-ideal mass `60 = 120/2`.

The finite-field row/fiber bound below is also checked on this nonsplit row.
After the `6` characteristic-zero pairs per primitive root are accounted for
separately, the non-characteristic-zero family has common-ideal valuation
budget `96`.  Dividing by `phi(8)=4` gives a non-structural row bound `24`.
Together with the `6` structured pairs, this gives `30` total row pairs and the
formal fiber bound `M <= 8`; the actual maximum fiber in the `F_9` row is `4`.
The radical incidence index is exact on this row: its total `3`-adic valuation
over the `48` non-characteristic-zero pairs is also `96`, equal to the modular
common-root degree sum.

## Norm Size And Finite-Family Aggregation

The same certificate has a simple size bound.  Since

```text
Res(Phi_n, Delta_r) = Norm_{Q(zeta_n)/Q}(Delta_r(zeta_n)),
```

and each conjugate satisfies

```text
|Delta_r(zeta_n^u)| <= 2 binom(m,r),
```

we have

```text
|Res(Phi_n, Delta_r)| <= (2 binom(m,r))^phi(n).
```

Consequently each non-characteristic-zero template has only finitely many split
bad primes, all dividing a computable integer bounded by these norms.  For a
finite normalized template family `T`, all split primes that realize any member
of `T` divide

```text
LCM_T = lcm_{(A,B) in T} C_n,sigma(A,B).
```

This is not yet the desired L1 aggregation theorem, but it is the exact finite
object that such a theorem can try to bound.

## Prime-Ideal Refinement

The rational certificate is a necessary rational-prime filter, not a sufficient
collision test.  If `p` splits, the actual finite-field row also chooses a
prime ideal

```text
(p, zeta_n-h)
```

or equivalently a primitive `n`-th root `h in F_p`.  The exact ideal-level
condition is

```text
Delta_r(h) = 0 in F_p,        1 <= r <= sigma.
```

Equivalently, define the modular common-root factor

```text
G_p(T)=gcd(Phi_n(T), Delta_1(T), ..., Delta_sigma(T)) in F_p[T].
```

Then the template has a finite-field realization over some primitive `n`-th
root in `F_p` if and only if

```text
deg G_p > 0.
```

Indeed, because `p` does not divide `n`, the roots of `Phi_n` in the algebraic
closure are the primitive `n`-th roots and are simple.  A common zero of all
the `Delta_r` is therefore exactly a nonconstant common divisor of `Phi_n` and
the `Delta_r` reductions.

The same argument gives a counting form.  Since `Phi_n` is squarefree modulo
`p`, the common-root factor `G_p` is squarefree, and

```text
deg G_p
  = #{alpha in Fpbar : Phi_n(alpha)=0 and Delta_r(alpha)=0 for all r<=sigma}.
```

When `n | p-1`, this is just the number of primitive `n`-th roots
`h in F_p` for which the template realizes the prefix collision.  Thus the
modular gcd is not only a yes/no ideal-level filter; it records the exact
embedding multiplicity at the split prime.

Thus `p | C_n,sigma(A,B)` says that each nonzero `Delta_r(zeta_n)` vanishes
modulo at least one prime ideal above `p`; it need not be the same prime ideal
for all `r`.

The verifier records a small false-positive template:

```text
A = {0,1,2,7,9,13},
B = {0,1,2,3,4,11},
n = 16,
sigma = 4.
```

Its rational certificate is

```text
C_16,4(A,B) = 194 = 2 * 97,
```

so `97` passes the rational split-prime filter.  But evaluating the four
`Delta_r` at all primitive `16`-th roots in `F_97` gives no common zero;
equivalently the modular gcd `G_97` is constant, with degree and embedding
count both equal to `0`.  Hence there is no finite-field prefix collision for
this template over `F_97`.

This distinction is important for aggregation: lcm certificates produce a
candidate set of rational primes, while the final row-level verifier or theorem
must still impose the common-prime-ideal condition.

## Exact Common-Ideal Certificate

The prime-ideal refinement can be encoded by a sharper integer certificate,
not only by a per-prime modular gcd.  Let

```text
R_Z = Z[T] / Phi_n(T),
d = phi(n),
```

with basis `1,T,...,T^{d-1}`.  For each active nonzero remainder
`Delta_r mod Phi_n`, let `M_r` be the `d x d` integer matrix for
multiplication by `Delta_r` on `R_Z`.  Concatenate these blocks:

```text
M(A,B) = [ M_1 | M_2 | ... | M_a ].
```

Define

```text
I_n,sigma(A,B) = gcd of all d x d minors of M(A,B),
```

with the convention `I_n,sigma(A,B)=0` for characteristic-zero prefix
collisions, where every `Delta_r` vanishes modulo `Phi_n`.

Equivalently, `I_n,sigma(A,B)` is the index of the lattice in `R_Z` generated
by the ideal

```text
(Delta_1, ..., Delta_sigma) R_Z
```

whenever this ideal has full rank.  This is the zeroth Fitting/determinantal
divisor of the common-ideal map.

For every prime `p` with `p not dividing n`,

```text
p | I_n,sigma(A,B)
  iff deg gcd(Phi_n, Delta_1, ..., Delta_sigma) in F_p[T] is positive.
```

Indeed, reducing `M(A,B)` modulo `p`, the image is exactly the ideal generated
by the `Delta_r` inside

```text
R_p = F_p[T] / Phi_n(T).
```

The matrix has full row rank over `F_p` iff this ideal is all of `R_p`.  Since
`p` does not divide `n`, the polynomial `Phi_n` is squarefree modulo `p`, so
`R_p` is reduced.  A proper ideal is therefore contained in a maximal ideal,
equivalently a common primitive-root zero of `Phi_n` and all active
`Delta_r` in the algebraic closure.  This is exactly the condition that the
modular common-root factor have positive degree.

This gives the exact rational-prime filter for simultaneous prime-ideal
collisions, away from the inseparable primes dividing `n`.

The index sharpens the norm certificate:

```text
I_n,sigma(A,B) | C_n,sigma(A,B).
```

The reason is that each single multiplication block `M_r` has determinant
`+- Res(Phi_n, Delta_r)`, while `M(A,B)` contains all such blocks.  The gcd of
all maximal minors of the concatenated matrix therefore divides the gcd of the
single-block determinants.

For the false-positive template above,

```text
C_16,4(A,B) = 194 = 2 * 97,
I_16,4(A,B) = 2.
```

Thus the exact common-ideal certificate removes the rational split prime `97`
before any root-by-root scan.  The false positive occurred because the separate
resultants vanish modulo `97` at incompatible prime ideals; the generated ideal
is still the whole algebra over `F_97`.

## Finite-Family Exact Aggregation

The common-ideal index gives an exact finite-family aggregation statement after
the characteristic-zero templates have been removed.

Let `T` be a finite family of unordered template pairs `(A,B)` such that no
member is a characteristic-zero prefix collision.  Define

```text
I_T = lcm_{(A,B) in T} I_n,sigma(A,B).
```

Then, for every prime `p` with `p not dividing n`,

```text
p | I_T
  iff there exists (A,B) in T with
      deg gcd(Phi_n, Delta_1(A,B), ..., Delta_sigma(A,B)) > 0
      in F_p[T].
```

If additionally `p` is split, meaning `n | p-1`, this is equivalent to saying
that some member of `T` realizes a finite-field prefix collision at some
primitive `n`-th root `h in F_p`.

Thus, for a finite normalized template family, the rational bad-prime support is
not merely bounded by a resultant lcm; it is exactly the prime support of the
common-ideal lcm, excluding the inseparable primes dividing `n`.  The remaining
L1 aggregation problem is therefore not to repair false positives inside a
fixed finite family, but to prove that the relevant aperiodic template family
has small enough common-ideal support or incidence mass.

This exact aggregation statement is still finite-family only.  It does not by
itself bound how many aperiodic templates can contribute to a single finite
field row as `n` grows.

The verifier checks this exact aggregation on the finite family consisting of
the forty `F_17` packet pairs together with the `p=97` rational false-positive
template.  The coarse resultant lcm has split-prime support `{17,97}`, while
the common-ideal lcm is `8704` and has exact split-prime support `{17}`.  Direct
modular gcd evaluation over the two candidate split primes confirms that only
`17` has a positive common-root row for this family.

## Valuation Incidence Budget

The common-ideal index also bounds multiplicity, not only support.  For a
non-characteristic-zero template define

```text
d_p(A,B) = deg gcd(Phi_n, Delta_1, ..., Delta_sigma) in F_p[T].
```

Then, for every prime `p` with `p not dividing n`,

```text
d_p(A,B) <= v_p(I_n,sigma(A,B)).
```

Indeed, let `d=phi(n)` and let `M(A,B)` be the `d x N` common-ideal matrix
above.  Over `F_p`, its image is the ideal generated by the reductions of the
`Delta_r` in `R_p=F_p[T]/Phi_n(T)`.  Therefore its cokernel is

```text
R_p / (Delta_1, ..., Delta_sigma)
  ~= F_p[T] / (Phi_n, Delta_1, ..., Delta_sigma)
  ~= F_p[T] / (G_p),
```

where `G_p=gcd(Phi_n, Delta_1, ..., Delta_sigma)`.  Since `p` does not divide
`n`, `Phi_n` is squarefree modulo `p`; in particular this cokernel has
`F_p`-dimension `deg G_p=d_p(A,B)`.

On the other hand, the Smith normal form of the integer map represented by
`M(A,B)` has full row rank and diagonal entries whose product is
`I_n,sigma(A,B)`.  The rank defect after reducing modulo `p` is the number of
Smith entries divisible by `p`, which is at most the sum of their `p`-adic
valuations.  This proves the inequality.

Consequently every finite non-characteristic-zero family `T` satisfies the
incidence budget

```text
sum_{(A,B) in T} d_p(A,B)
  <= sum_{(A,B) in T} v_p(I_n,sigma(A,B)).
```

This is the first aggregation inequality in the note.  It converts
degree-weighted common-prime-ideal incidence into a purely integer valuation
budget.  The remaining hard L1 problem is to bound that valuation budget over
the robustly aperiodic template families that arise at large `n`.

## Radical Incidence Index

The valuation budget can be sharpened by removing higher prime-power torsion.
Let

```text
s_1, ..., s_d
```

be diagonal entries obtained from the full-rank common-ideal matrix `M(A,B)` by
unimodular integer row and column operations.  Thus

```text
I_n,sigma(A,B) = product_i s_i.
```

Define the radical incidence index

```text
J_n,sigma(A,B) = product_i rad(s_i),
```

where `rad(s)` is the product of the rational primes dividing `s`.  Then

```text
J_n,sigma(A,B) | I_n,sigma(A,B).
```

For every prime `p` with `p not dividing n`,

```text
v_p(J_n,sigma(A,B)) = d_p(A,B).
```

Indeed, reducing the diagonal form modulo `p`, the cokernel dimension is
exactly the number of diagonal entries divisible by `p`.  That number is
`v_p(J_n,sigma(A,B))`.  The common-ideal argument above identifies the same
cokernel with

```text
F_p[T] / (Phi_n, Delta_1, ..., Delta_sigma)
  ~= F_p[T] / (G_p),
```

whose dimension is `deg G_p=d_p(A,B)` because `Phi_n` is squarefree modulo
`p`.

Thus for every finite non-characteristic-zero family `T`, if

```text
J_T = product_{(A,B) in T} J_n,sigma(A,B),
```

then the incidence identity is exact:

```text
v_p(J_T) = sum_{(A,B) in T} d_p(A,B),        p not dividing n.
```

The original common-ideal index `I` is still useful as a Fitting/norm divisor,
but `J` is the sharper object for row incidence: it remembers how many Smith
directions vanish modulo `p`, not how much higher `p`-power torsion is present
inside those directions.

There is also a global log-weighted form.  For a finite multiset `T` of
non-characteristic-zero templates, put

```text
D_T = product_{(A,B) in T} I_n,sigma(A,B),
d_T(p) = sum_{(A,B) in T} d_p(A,B).
```

Then, away from primes dividing `n`,

```text
product_{p not dividing n} p^{d_T(p)}  divides  D_T,
```

and therefore

```text
sum_{p not dividing n} d_T(p) log p
  <= log D_T
  = sum_{(A,B) in T} log I_n,sigma(A,B).
```

Since `I_n,sigma(A,B) | C_n,sigma(A,B)`, the right side is at most the
corresponding sum of logarithms of the resultant certificates.  Using the
trivial norm bound from above, each individual template also satisfies

```text
log I_n,sigma(A,B)
  <= min_{active r} phi(n) log(2 binom(m,r)).
```

This is a finite density-over-primes statement: large degree-weighted incidence
at many rational primes forces a large integer common-ideal product.  It still
does not prove the L1 local limit, because the hard part is bounding `D_T` for
the robustly aperiodic template families selected by the prefix problem.
The radical product `J_T` gives the corresponding exact incidence product:
away from primes dividing `n`,

```text
product_p p^{d_T(p)}
  = product_p p^{v_p(J_T)}.
```

Thus `J_T` is the sharp row-incidence ledger, while `D_T` is the coarser but
norm-controlled upper envelope.

## Newton Bridge To Power Sums

The same common-root factor can be computed from power sums whenever the small
integers `1,...,sigma` are invertible.  Define

```text
P_j(A;T) = sum_{a in A} T^{ja},        1 <= j <= sigma.
```

Let `G^e_{p,sigma}` be the modular common-root factor built from the elementary
differences `Delta_r=E_r(A)-E_r(B)`, and let `G^p_{p,sigma}` be the analogous
factor built from the power-sum differences

```text
P_j(A;T)-P_j(B;T).
```

If `p` does not divide `n sigma!`, then

```text
G^e_{p,sigma}(A,B) = G^p_{p,sigma}(A,B).
```

Indeed, at any root `alpha` of `Phi_n` in the algebraic closure of `F_p`, the
numbers `alpha^a` for `a in A` have elementary sums `E_r(A;alpha)` and power
sums `P_j(A;alpha)`.  Newton's identities form a triangular system relating
the first `sigma` elementary sums to the first `sigma` power sums, with diagonal
coefficients `1,2,...,sigma`.  Since these coefficients are invertible modulo
`p`, equality of the elementary prefix is equivalent to equality of the
power-sum prefix.  Because `p` does not divide `n`, `Phi_n` is squarefree, so
the two gcds are the same product of primitive-root factors.

This bridges the bad-prime certificate layer to the Fourier/moment formulation
used in the L1 orbit-cancellation notes.  The rational resultant certificate is
an elementary-symmetric certificate, but the ideal-level split-prime test can
be read equivalently in the power-sum coordinates used by Fourier analysis.

There is also a common-ideal version after localizing away from the Newton
denominators.  Let `I^e_n,sigma(A,B)` be the elementary common-ideal index above
and let `I^p_n,sigma(A,B)` be the analogous index built from the power-sum
differences

```text
P_j(A;T)-P_j(B;T),        1 <= j <= sigma.
```

For every prime `ell` with

```text
ell not dividing n sigma!,
```

one has

```text
v_ell(I^e_n,sigma(A,B)) = v_ell(I^p_n,sigma(A,B)).
```

Indeed, over the localized ring `Z_(ell)[T]/Phi_n(T)`, Newton's identities give
an invertible triangular change of generators between the first `sigma`
elementary differences and the first `sigma` power-sum differences.  The two
generated ideals are equal after localization, so their lattice/Fitting indices
have the same `ell`-adic valuation.

Thus every separable bad-prime valuation budget away from the small primes
dividing `n sigma!` can be computed in the Fourier power-sum coordinates.  This
is the exact-index bridge between the finite-field bad-prime certificate lane
and the Fourier orbit-cancellation lane.

The same localization also transports the radical incidence index.  Let
`J^e_n,sigma(A,B)` and `J^p_n,sigma(A,B)` be the radical incidence indices
built from the elementary and power-sum common-ideal matrices.  For every prime
`ell` with

```text
ell not dividing n sigma!,
```

one has

```text
v_ell(J^e_n,sigma(A,B)) = v_ell(J^p_n,sigma(A,B)).
```

The reason is that the localized elementary and power-sum ideals are equal in
`Z_(ell)[T]/Phi_n(T)`, so the localized cokernels are isomorphic.  The
`ell`-adic radical valuation is the number of Smith directions killed modulo
`ell`, equivalently the dimension of the localized cokernel after reduction
modulo `ell`.  Thus the exact row-incidence ledger `J`, not only the coarser
index `I`, can be computed in Fourier power-sum coordinates away from the
Newton denominators.

## Affine-Orbit Reduction

The template data has an affine symmetry.  For `u in (Z/nZ)^*` and
`t in Z/nZ`, put

```text
A' = uA+t,
B' = uB+t.
```

Then

```text
Delta'_r(T) = T^(rt) Delta_r(T^u).
```

The substitution `T -> T^u` is a Galois automorphism on primitive `n`-th roots,
and `T^(rt)` is a cyclotomic unit.  Therefore:

```text
C_n,sigma(A',B') = C_n,sigma(A,B).
I_n,sigma(A',B') = I_n,sigma(A,B).
J_n,sigma(A',B') = J_n,sigma(A,B).
```

For the common-ideal index, the same identity sends the ideal generated by the
`Delta_r` in `Z[T]/Phi_n(T)` to the ideal generated by the transformed
`Delta'_r`: the substitution `T -> T^u` is a `Z`-algebra automorphism of
`Z[T]/Phi_n(T)`, and multiplication by `T^(rt)` is multiplication by a unit.
Thus the generated sublattice has the same index.
The quotient lattices are isomorphic as abelian groups, so the Smith invariant
factors, and therefore the radical incidence index `J`, are unchanged.

For every prime `p` not dividing `n`, the same identity permutes primitive
`n`-th roots in the algebraic closure of `F_p`, so the modular common-root
degree is also invariant:

```text
deg gcd(Phi_n, Delta'_1, ..., Delta'_sigma)
  =
deg gcd(Phi_n, Delta_1, ..., Delta_sigma).
```

Thus any finite bad-prime aggregation can quotient by affine template orbits
without changing the rational certificate, common-ideal index, valuation
budget, radical incidence index, or ideal-level collision test.

## Split-Prime Row Accounting

The common-root degree gives an exact row-level accounting identity.  Fix a
split prime `p` and write `P_h` for the finite-field prefix map obtained from
a primitive `n`-th root `h in F_p`.  Let

```text
Coll(h) = {{A,B}: A != B, P_h(A)=P_h(B)}
```

be the unordered collision-pair set at that root.  For an unordered template
pair define

```text
d_p(A,B) = deg gcd(Phi_n, Delta_1, ..., Delta_sigma) in F_p[T].
```

Then, because `d_p(A,B)` counts exactly the primitive roots at which this pair
collides,

```text
sum_{A<B} d_p(A,B)
  = sum_{h primitive} |Coll(h)|.
```

Moreover all primitive roots give the same row count.  If `h'=h^u` with
`u in (Z/nZ)^*`, then

```text
E_r(A;h') = E_r(uA;h),
```

and dilation by `u` is a bijection on the `m`-subsets of `Z/nZ`.  Hence
`|Coll(h')|=|Coll(h)|`, and therefore

```text
sum_{A<B} d_p(A,B) = phi(n) |Coll(h)|.
```

Thus the split-prime row count is exactly the common-prime-ideal incidence
mass divided by `phi(n)`.  After characteristic-zero and quotient-periodic
templates are removed, every nonzero summand must also satisfy
`p | I_n,sigma(A,B)` and contributes at most `v_p(I_n,sigma(A,B))` to the
degree-weighted incidence budget.  This is the precise finite object that a
future L1 density-over-primes or bad-prime aggregation theorem has to bound.

Combining this with affine invariance gives the quotient form.  If `O` ranges
over affine orbits of unordered template pairs and `(A_O,B_O)` is a
representative, then `d_p` is constant on `O`, so

```text
phi(n) |Coll(h)|
  = sum_O |O| d_p(A_O,B_O).
```

This is the practical aggregation ledger: an exact row bound can be proved by
bounding orbit sizes and representative common-root degrees, rather than by
enumerating every ordered root-template incidence separately.

## Dilation-Invariant Finite-Field Row And Fiber Bound

The valuation budget gives a direct row bound over any finite field containing
a primitive `n`-th root, once the finite template family is closed under
dilation.  Let `p` be a prime not dividing `n`, and let `K` be a finite field
of characteristic `p` containing a primitive `n`-th root `h`.  Let `T` be a
finite family of unordered non-characteristic-zero template pairs that is
stable under

```text
(A,B) -> (uA,uB),        u in (Z/nZ)^*.
```

Write

```text
Coll_T(h) = {{A,B} in T : E_r(A;h)=E_r(B;h) for all r<=sigma}.
```

Then all primitive roots in `K` have the same row count, and

```text
|Coll_T(h)|
  = (1/phi(n)) sum_{(A,B) in T} v_p(J_n,sigma(A,B))
  = (1/phi(n)) sum_{(A,B) in T} d_p(A,B)
  <= (1/phi(n)) sum_{(A,B) in T} v_p(I_n,sigma(A,B)).
```

Here `d_p(A,B)` is the degree of the common-root gcd over `F_p`.  The equality
does not require `p` to split over `F_p`: the roots of `Phi_n` are simple
because `p` does not divide `n`, and `d_p(A,B)` counts all primitive roots in
the algebraic closure where the template collides.  Since every primitive root
is `h^u`, dilation stability makes the row count independent of the primitive
root.  The inequality is the valuation incidence budget.

Equivalently, after quotienting by affine orbits contained in `T`,

```text
|Coll_T(h)|
  = (1/phi(n)) sum_O |O| v_p(J_n,sigma(A_O,B_O))
  <= (1/phi(n)) sum_O |O| v_p(I_n,sigma(A_O,B_O)).
```

This is the form closest to the desired L1 local-limit estimate: after the
structured characteristic-zero and quotient-periodic strata are removed, a row
collision-pair bound follows from bounding the valuation budget of a
dilation-stable aperiodic template family.

It also gives the immediate locator-fiber consequence.  Suppose a candidate
locator set has at most `C_0` structured collision pairs in each row after the
characteristic-zero and quotient-periodic ledgers are applied, and all remaining
collision pairs lie in such a dilation-stable family `T`.  Put

```text
B_p(T) = sum_{(A,B) in T} v_p(J_n,sigma(A,B)),
C_p = C_0 + floor(B_p(T)/phi(n)).
```

If `M` is the largest prefix fiber in the row over `h`, then

```text
binom(M,2) <= C_p,
```

so

```text
M <= floor((1 + sqrt(1 + 8 C_p))/2).
```

Thus an L1 polynomial locator-fiber bound follows from two separate budgets:
the already-structured row contribution `C_0`, and the exact common-ideal
radical incidence budget `B_p(T)` for the robustly aperiodic remainder.  The
coarser `I`-valuation budget can replace `J` whenever one wants a bound that is
immediately dominated by the norm certificate.

## Prefix-Depth Filtration

The bad-prime objects are monotone in the prefix length.  Write
`C_sigma(A,B)`, `I_sigma(A,B)`, and `G_{p,sigma}(A,B)` for the resultant
certificate, common-ideal index, and modular common-root factor using ranks
`1 <= r <= sigma`.

For fixed `p`, adding one more prefix equation can only shrink the common-root
factor:

```text
G_{p,sigma+1}(A,B) | G_{p,sigma}(A,B),
deg G_{p,sigma+1}(A,B) <= deg G_{p,sigma}(A,B).
```

Once `C_sigma(A,B)` is nonzero, the deeper certificates form a divisibility
filtration:

```text
C_{sigma+1}(A,B) | C_sigma(A,B).
I_{sigma+1}(A,B) | I_sigma(A,B).
```

Indeed, `G_{p,sigma+1}` is obtained by taking one more gcd with
`Delta_{sigma+1}`.  Similarly, `C_{sigma+1}` is the gcd of the previous active
resultants and possibly one additional active resultant.  For the exact index,
the ideal generated by

```text
Delta_1, ..., Delta_sigma, Delta_{sigma+1}
```

contains the previous ideal generated by `Delta_1,...,Delta_sigma`; the lattice
index can only divide the previous index.  Therefore deeper prefixes can only
remove primitive-root embeddings and rational split-prime candidates.  Row
fiber sizes and collision-pair counts are also nonincreasing, because equality
of `sigma+1` prefix coefficients implies equality of the first `sigma`.

This is the local mechanism behind the L1 prefix threshold: increasing `sigma`
does not merely add data heuristically; it refines the algebraic bad-prime
sieve by divisibility.

The radical incidence ledger makes the depth loss exact.  For primes `p` not
dividing `n`, write

```text
d_{p,sigma}(A,B)=deg G_{p,sigma}(A,B).
```

Since `v_p(J_sigma)=d_{p,sigma}`, one has

```text
v_p(J_sigma(A,B))-v_p(J_{sigma+1}(A,B))
  =
d_{p,sigma}(A,B)-d_{p,sigma+1}(A,B).
```

Equivalently, because

```text
G_{p,sigma+1}=gcd(G_{p,sigma}, Delta_{sigma+1}),
```

one has `G_{p,sigma+1}` dividing `G_{p,sigma}`.  Define the modular frontier
factor

```text
H_{p,sigma}(A,B)=G_{p,sigma}(A,B)/G_{p,sigma+1}(A,B) in F_p[X].
```

Since `p` does not divide `n`, `Phi_n` is squarefree modulo `p`, so this
quotient is squarefree.  Its roots are exactly the primitive-root embeddings
that satisfied the first `sigma` equations but fail the next one, and

```text
deg H_{p,sigma}(A,B)
  =
v_p(J_sigma(A,B))-v_p(J_{sigma+1}(A,B)).
```

Thus, away from the inseparable primes dividing `n`, the quotient of radical
incidence ledgers is not merely monotone: it is the exact depth-frontier mass
removed by the next prefix coefficient.

Telescoping to the full-prefix endpoint gives the depth decomposition.  If
`A != B`, `|A|=|B|=m`, and `sigma<m`, then the full-prefix endpoint has no
prime support away from primes dividing `n`, so

```text
part_away_n(J_sigma(A,B))
  =
product_{r=sigma}^{m-1} Frontier_r(A,B),
```

where `Frontier_r(A,B)` is the away-from-`n` radical quotient from depth `r`
to `r+1`.  Prime by prime, this says

```text
v_p(J_sigma(A,B))
  =
sum_{r=sigma}^{m-1}
  (d_{p,r}(A,B)-d_{p,r+1}(A,B)),        p not dividing n.
```

Thus the full bad-prime incidence budget at a partial prefix is exactly the sum
of the successive frontier masses killed before the rigid endpoint.

For a finite dilation-stable non-characteristic-zero family `T`, this
telescopes at the row level.  If `h` is any primitive `n`-th root in a finite
field of characteristic `p not dividing n`, then

```text
|Coll_{T,sigma}(h)|
  =
  (1/phi(n)) sum_{r=sigma}^{m-1}
    sum_{(A,B) in T}
      deg H_{p,r}(A,B).
```

The left side is the row collision count at depth `sigma`; the right side is
the sum of all future frontier layers.  This is the depth-local aggregation
target: after structured rows are removed, it is enough to bound the radical
frontier layers rather than the whole partial-prefix collision relation at
once.

## Full-Prefix Rigidity

The endpoint of the filtration is rigid.  Let `p` be split, let `h in F_p`
have order `n`, and take `A,B subset Z/nZ` with `|A|=|B|=m`.  If

```text
E_r(A;h) = E_r(B;h),        1 <= r <= m,
```

then `A=B`.

Indeed, the monic locator polynomials

```text
L_A(X)=prod_{a in A}(X-h^a),
L_B(X)=prod_{b in B}(X-h^b)
```

have degree `m`.  Equality of the first `m` elementary sums is equality of all
nonleading coefficients of these monic degree-`m` polynomials.  Hence
`L_A=L_B`.  Since `h` has exact order `n`, the elements `h^0,...,h^{n-1}` are
distinct in `F_p`, so the two root subsets coincide.

Thus every split-prime collision at fixed complement size `m` is necessarily a
partial-prefix phenomenon with `sigma < m`.  The bad-prime aggregation problem
only needs to control how quickly the prefix-depth filtration reaches this
rigid endpoint.

The exact common-ideal index has the corresponding endpoint.  If `A != B` and
`sigma=m`, then

```text
prime divisors of I_n,m(A,B) are all divisors of n.
```

Indeed, if a prime `p` not dividing `n` divided `I_n,m(A,B)`, the exact
common-ideal criterion would give a primitive `n`-th root `alpha` in the
algebraic closure of `F_p` where all elementary sums agree:

```text
E_r(A;alpha)=E_r(B;alpha),        1 <= r <= m.
```

The two monic locator polynomials over that algebraic closure would then have
the same degree and all the same coefficients.  Since `alpha` has exact order
`n`, its powers are distinct, so the root subsets coincide and `A=B`, a
contradiction.  Thus the prefix-depth filtration removes every separable
rational bad prime by the full-prefix endpoint; only primes dividing `n` can
remain in `I_n,m`.

## Worked L1 Packet: F_17, n=16

The existing aperiodic collision certificate in
`l1_aperiodic_prefix_collision.md` uses

```text
p = 17,
n = 16,
k = 6,
sigma = 4,
m = n-k-sigma = 6.
```

There are `8008` complement locators, `7968` prefix values, and exactly `40`
two-point finite-field collisions.  These forty pairs are not quotient-core
collisions for the active quotient orders.

The bad-prime certificate explains why this finite-field packet can occur
without being a characteristic-zero collision.  For the three dilation orbits
recorded in the earlier note, the certificate values are:

```text
orbit size 16: C = 68     = 2^2 * 17
orbit size 16: C = 272    = 2^4 * 17
orbit size 8:  C = 147968 = 2^9 * 17^2
```

The aggregate lcm for the whole packet is

```text
LCM = 147968 = 2^9 * 17^2.
```

Thus `17` is the only split prime in the certificate of every collision
template and of the complete three-orbit packet.  In particular, the packet is
a genuine finite-field bad-prime event, not evidence for a characteristic-zero
aperiodic family.

The exact common-ideal index sharpens this packet without changing the rational
split-prime support.  Across the same forty pairs the index distribution is:

```text
16 pairs: I = 68
16 pairs: I = 272
 8 pairs: I = 8704 = 2^9 * 17.
```

The aggregate exact-index lcm is therefore

```text
LCM_I = 8704 = 2^9 * 17,
```

which divides the norm-certificate lcm and removes one redundant factor of
`17`.  This distinction is not needed to explain the small `F_17` packet, but
it is the right integer object for a future bad-prime aggregation theorem,
because its rational prime support is exact for simultaneous common-ideal
collisions away from primes dividing `n`.

The verifier also checks the split-prime row accounting identity across all
primitive roots in `F_17`.  There are `phi(16)=8` such roots, each gives `40`
collision pairs, and the root-template incidence ledger has

```text
8 * 40 = 320
```

incidences.  The modular-gcd side has the same weighted mass: there are `320`
incident unordered template pairs, each with common-root degree `1`.  Thus the
known `F_17` packet is exactly accounted for by the degree-weighted
common-prime-ideal ledger.

After quotienting by affine orbits, the same ledger has only three rows:

```text
orbit size 64,  common-root degree 1, contribution 64
orbit size 128, common-root degree 1, contribution 128
orbit size 128, common-root degree 1, contribution 128
```

Their weighted sum is again `320`.  This is the orbit-level form that a larger
finite-family bad-prime aggregation would try to control.

The valuation row/fiber consequence is exact at the row-pair level on this
packet.  The dilation-stable incident family has common-ideal valuation budget
`320`; after division by `phi(16)=8`, the row-pair bound is `40`, matching the
actual collision-pair count for every primitive root.  The resulting formal
fiber bound is `M <= 9`, while the actual maximum fiber at `sigma=4` is `2`.
The radical incidence index sharpens the same statement: the total `17`-adic
radical valuation is exactly `320`, equal to the modular common-root degree
sum, with no contribution from the `p=97` rational false-positive template.

The prefix-depth filtration is sharp on this same row.  For `p=17`, `n=16`,
and `m=6`, the full row profile is:

```text
sigma  distinct prefixes  max fiber  collision pairs
1      17                 472        1882116
2      289                32         107352
3      4480               5          4480
4      7968               2          40
5      8008               1          0
6      8008               1          0
```

For the representative pair

```text
A = {0,1,2,3,4,14},
B = {5,6,7,9,12,15},
```

the corresponding certificate and common-root-degree filtration is:

```text
sigma  C_sigma  I_sigma  split support  deg G_17,sigma
1      2312     2312     {17}           2
2      68       68       {17}           1
3      68       68       {17}           1
4      68       68       {17}           1
5      4        4        {}             0
6      4        4        {}             0
```

Thus the known `sigma=4` bad-prime collision disappears at the next prefix
rank: `17` leaves the certificate support and the modular common-root factor
becomes constant.

The radical frontier-drop ledger records the same disappearance exactly.  For
the representative pair above, the away-from-`n` radical drops are:

```text
sigma 1 -> 2: 17
sigma 2 -> 3: 1
sigma 3 -> 4: 1
sigma 4 -> 5: 17
sigma 5 -> 6: 1
```

For the full `40`-pair `F_17` packet, every pair has radical frontier drop
`17` from `sigma=4` to `sigma=5`, so the aggregate frontier product is
`17^40`.  The nonsplit `F_9` witness similarly has radical frontier drop
`3^2` from `sigma=1` to the full-prefix endpoint `sigma=2`.
Telescoping all the way to the full-prefix endpoint gives the same products:
the `F_17` packet has full-depth radical frontier product `17^40`, and the
`F_9` witness has full-depth product `3^2`.

At the row level, the `F_17` dilation-stable incident family has frontier
layer sums

```text
sigma 4 -> 5: 320
sigma 5 -> 6: 0
```

Dividing by `phi(16)=8` gives the fixed-root row count `40`.  For the nonsplit
`F_9` non-characteristic-zero family, the single frontier layer has sum `96`;
dividing by `phi(8)=4` gives the non-structural row contribution `24`, with
the remaining `6` row pairs coming from the characteristic-zero stratum.
The verifier also computes the frontier factors themselves: the fixed-root
`F_17` packet has forty degree-one factors from `sigma=4` to `sigma=5`, the
full dilation-stable `F_17` family has degree sums `320,0` across the two
frontier layers, and the nonsplit `F_9` family has forty-eight degree-two
frontier factors at `sigma=1`.

The verifier separately checks this full-prefix endpoint for `n=16` at the
split primes `17` and `97`, for every complement size `1 <= m <= 8`: at
`sigma=m`, every fiber is a singleton and the collision-pair count is `0`.

The verifier also checks the Newton bridge on this packet.  For all `40`
`F_17` collision pairs at `sigma=4`, the elementary common-root factor and the
power-sum common-root factor agree and have degree `1`; for the `p=97`
rational false-positive template both factors are constant.  Along the
representative depth filtration above, the elementary and power-sum factors
agree at every `1 <= sigma <= 6`.

The localized radical incidence bridge is checked on the same packet.  The
elementary/power radical-index pairs are

```text
16 pairs: 68 -> 136
16 pairs: 272 -> 272
 8 pairs: 4352 -> 4352
```

The only displayed discrepancy is at the excluded small prime `2`; the
`17`-adic radical valuation is `1` for every collision pair in both coordinate
systems.

The verifier also checks the same row over the next split primes

```text
p = 97, 113, 193,
```

and finds no collisions.  This is not a proof for all primes; it is a finite
sanity check that the certificate is detecting the known exceptional row.

The current verifier also runs a bounded exact row scan:

```text
p <= 5000,
p = 1 mod 16.
```

It enumerates the full prefix-fiber histogram for every such prime and finds
that the only nonzero collision row is:

```text
p = 17, collision pairs = 40, max fiber = 2.
```

This is a finite theorem for the bounded range, not an asymptotic statement.

## Relation To Scott's L1 Characteristic-Zero PR

PR `#99` develops characteristic-zero prefix-fiber structure.  This note does
not repeat that lane.  It supplies the complementary finite-field layer:
once a template is not one of the characteristic-zero structures, any modular
collision has to pay an explicit bad-prime certificate.

This is the local step needed before one can attempt a density-over-primes or
bad-prime aggregation theorem.

## What Remains Open

The theorem is templatewise.  A positive L1 local-limit theorem still needs a
uniform aggregation bound such as:

```text
sum over robustly aperiodic templates of v_p(J_n,sigma(A,B))
```

for the exact radical incidence ledger, or a norm-controlled upper bound via
the common-ideal index `I_n,sigma(A,B)`.  Equivalently, after quotient and
characteristic-zero strata are removed, one needs a theorem proving that only
polynomially many bad-prime templates can contribute to any one finite field.

That aggregation problem is the next hard L1 target.
