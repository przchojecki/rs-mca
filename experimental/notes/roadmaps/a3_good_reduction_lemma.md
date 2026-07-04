# A3: the good-reduction lemma for W_h's torsion structure

- **DAG node:** `a3_good_reduction_lemma`.
- **Consumers:** `h4_sparse_norm_gate`, the (A) closure assembly
  (`experimental/notes/roadmaps/a_closure_assembly.md`).
- **Status:** the fixed-(n,h) lemma (Theorem A3 below) is PROVED, with
  self-contained elementary proofs of every input except the two items
  in the Gap ledger (both are provenance/citation items, not logical
  gaps in the fixed-(n,h) chain).  The h-only ("n-uniform") variant is
  NOT proved and is shown below to be false in its naive form; the
  corrected form is recorded with its named gaps.
- **Verifier:** `experimental/scripts/verify_a3_good_reduction.py`.
- **Inputs:** x81 (square-shift normal form), x83 (obstruction gate +
  denominator control), X24 (char-0 dyadic descent) — all banked and
  verifier-green.

## Critical-path role

This packet is the proof-theoretic bridge used by the conditional prize
path's small-`h` primitive-trade lane.  It turns finite row candidates
over `F_q` into characteristic-zero candidates whenever the row prime is
coprime to the certified exceptional integer `D(n,h)`.  Together with X24
it gives zero primitive residue at clean `(n,h)` cells; the remaining work
for the closure assembly is finite certificate production plus row-wise
`gcd(p,D(n,h))` checks, not a new structural theorem.

## 1. Objects and conventions

### 1.1 The universal variety in root and coefficient coordinates

Fix h >= 2.  For a split 2h-support R = (x_1, ..., x_{2h}) (distinct,
invertible) write

```text
C(X) = prod_i (X - x_i) = X^{2h} + c_{2h-1} X^{2h-1} + ... + c_0.
```

Over any Z[1/2]-algebra the x83 recursion determines the unique monic

```text
S(X) = X^h + s_{h-1} X^{h-1} + ... + s_0
```

matching C in degrees 2h..h, and E = S^2 - C has deg E <= h-1.  The
obstructions are

```text
O_j(R) = [X^j] E,      1 <= j <= h-1,
```

and W_h subset G_m^{2h} is their common zero locus.  All O_j lie in
Z[1/2][c_0..c_{2h-1}] subset Z[1/2][x_1..x_{2h}]^{sym}, so W_h is a
closed subscheme of G_m^{2h} over Z[1/2], depending on h only.

**Lemma 0 (graph structure / exact triangularity).**  For 1 <= j <=
h-1 there are polynomials P_j in Z[1/2][c_h, ..., c_{2h-1}] with

```text
O_j = P_j(c_h, ..., c_{2h-1}) - c_j.
```

Hence, in coefficient space, W_h is the graph

```text
{ c_j = P_j(c_h..c_{2h-1}), 1 <= j <= h-1 }
```

over the h+1 free coordinates (c_0, c_h, ..., c_{2h-1}); equivalently
W_h's coefficient image is parametrized isomorphically by

```text
(s_0, ..., s_{h-1}, lambda) |-> C = S^2 - lambda,
```

an affine (h+1)-space over Z[1/2].

*Proof.*  The recursion determines s_{h-1}, ..., s_0 from c_{2h-1},
..., c_h alone (matching degrees 2h-1 down to h; each step is linear
in the new s with coefficient 2).  Then for 1 <= j <= h-1,

```text
O_j = [X^j] S^2 - c_j = ( sum_{a+b=j, 0<=a,b<=h} s_a s_b ) - c_j,
```

and the first summand involves only s_0..s_j, i.e. only c_h..c_{2h-1}.
That is the displayed graph form.  The (S, lambda) parametrization is
its inverse: given a graph point, set lambda = [X^0]S^2 - c_0; given
(S, lambda), read off the coefficients of S^2 - lambda.  Both maps
are polynomial over Z[1/2] (the recursion divides only by 2).  X81
uniqueness (char /= 2) gives injectivity of (S,lambda) -> C.  QED

The verifier checks Lemma 0 symbolically at h = 3, 4, together with
the quasi-homogeneity

```text
O_j(gamma R) = gamma^{2h-j} O_j(R)
```

(weights: x_i of weight 1, c_j of weight 2h-j, s_j of weight h-j,
lambda of weight 2h).

### 1.2 Candidates = trades; the square filter is free on the anchored slice

Call a degree-2h monic C over a field F of odd characteristic (or over
K = Q(zeta_n)) an **(n,h)-candidate** when

```text
C = S^2 - lambda   (some monic S, some lambda)   and   C | X^n - 1.
```

Since X^n - 1 is separable over every field of characteristic /= 2
(n = 2^s), a candidate automatically has 2h distinct roots in mu_n,
and lambda /= 0 (else C = S^2 is non-squarefree).  By x81, if lambda
is a nonzero square in F, C splits uniquely as (S-a)(S+a), a^2 =
lambda, giving the unique unordered minimal h-trade {P, Q}; and every
minimal h-trade with support in mu_n arises this way.  Over Q-bar (or
any algebraically closed field) every candidate is a trade.

### 1.3 The anchored slice (care point (i))

The diagonal torus Delta = G_m (gamma . x = (gamma x_1, ...,
gamma x_{2h})) acts freely on G_m^{2h} and preserves W_h
(quasi-homogeneity).  Consequently **every** torsion point of W_h lies
on the positive-dimensional torsion coset zeta . (Delta cap torsion)
inside W_h, so Laurent-type statements applied to W_h itself are
vacuous ("everything is toral").  The scaling must be removed first.

Two removals are available: the quotient W_h/Delta subset
G_m^{2h}/Delta ~= G_m^{2h-1} (ratio coordinates x_i/x_1), or the
anchored slice.  The quotient is a genuine variety (the action is
free), but its mu_n-points are supports with **torsion ratios** and an
arbitrary global scale x_1 in G_m — a strictly larger set than the
row's trades, whose actual coordinates lie in mu_n(F_q).  The anchored
slice

```text
W_h^a = W_h cap { x_1 = 1 },   equivalently (unordered)  1 in R,
equivalently (coefficient space)  C(1) = 0,  i.e.  lambda = S(1)^2,
```

is a closed subscheme over Z[1/2], is a section of the quotient over
the locus we count, and matches the campaign's anchor convention
(anchored pairs, 1 in P: the banked orbit argument of
`anchored_nontoral_pte_bound`).  **We work with the anchored slice.**
Note the bonus: on the slice, lambda = S(1)^2 is automatically a
square in the field of the point, so **anchored candidates are
anchored trades** over any field — the non-algebraic square filter
disappears (it only ever removes points in the unanchored counting,
which we recover by the orbit factor).

Orbit accounting (proved, used by the assembly): for gamma in mu_n,
1 in gamma R iff gamma in R^{-1}; if the scaling stabilizer of R has
order d then d | 2h, the orbit has n/d distinct supports of which
exactly 2h/d are anchored.  Hence for any scaling-invariant set T of
supports (candidates and trades are scaling-invariant, since
lambda_{gamma R} = gamma^{2h} lambda_R = (gamma^h)^2 lambda_R),

```text
# T = (n / 2h) . # (anchored members of T),
```

exactly, with no freeness hypothesis.  In the campaign's ordered
split-pair currency this is the banked identity
"# ordered split pairs = (n/h) . A_h".

### 1.4 The fiber (coset-union) locus and primitivity (care point (ii))

Call a support R subset mu_n **coset-union (imprimitive)** if R is a
union of cosets of some mu_d, d > 1 (equivalently C(X) = C~(X^d):
multiplicative pullback; d | 2h since mu_d acts freely on R).  Call it
**primitive** otherwise.  X24's full mu_h-fiber trades are
coset-unions.  Geometrically, the coset-union candidates are the
toral part of W_h^a: the full-fiber families C = (X^h - alpha^h)(X^h -
beta^h) = (X^h - (alpha^h+beta^h)/2)^2 - ((alpha^h-beta^h)/2)^2 sweep
positive-dimensional torsion cosets inside W_h, and X24 (char-0
classification: trades in mu_n(C) are exactly full fibers) says
char-0 torsion candidates lie in this locus.  A3 does not need this
split — Theorem A3 below is a statement about **all** mu_n-points —
but the assembly counts the two parts against different ledgers
(coset-unions are strip/staircase-paid; primitives go against the
n^3 column).

## 2. Torsion rigidity of reduction (care points (iv), (v))

Let n = 2^s, K = Q(zeta_n), O = Z[zeta_n] (we only use that O is a
ring of algebraic integers containing mu_n; the full ring of integers
is not needed).  Let p be an odd prime and P a maximal ideal of O
above p, with residue field k(P) = F_{p^f}, f = ord of p in
(Z/n)^*.

**Lemma 1 (torsion rigidity).**  Reduction mod P is a group
isomorphism

```text
red_P : mu_n(K) --> mu_n(k(P)),
```

and mu_n(k(P)) has exactly n elements.  If moreover the row condition
n | q - 1 holds with q = p or q = p^2, then f | 2 and k(P) embeds in
F_q, so mu_n(k(P)) = mu_n(F_q) and red_P identifies mu_n(K) with the
row's subgroup mu_n(F_q).  The identification is a group isomorphism,
so it preserves and reflects the coset-union structure of supports:
R is coset-union iff red_P(R) is.

*Proof.*  Injectivity: for zeta /= xi in mu_n, zeta - xi =
xi(omega - 1) with omega = zeta xi^{-1} a primitive 2^j-th root of
unity, j >= 1.  Now N_{K/Q}(1 - omega) is a product of algebraic
conjugates of 1 - omega, each an algebraic integer, and equals
Phi_{2^j}(1)^{[K : Q(omega)]} = 2^{[K : Q(omega)]}.  So the norm of
zeta - xi is (a unit times) a power of 2; if zeta - xi were in P,
then p would divide that norm — impossible for odd p.  Distinct
torsion points stay distinct mod P.

Surjectivity and the count: the n images red_P(mu_n(K)) are n
distinct roots of X^n - 1 in k(P); X^n - 1 has at most n roots in the
field k(P); so the image is all of mu_n(k(P)) and #mu_n(k(P)) = n.

Row condition: n | q - 1 with q = p^e, e in {1,2}, means p^e = 1 in
(Z/n)^*, so f = ord(p) divides e <= 2, and F_{p^f} subset F_{p^e} =
F_q.  Since mu_n(F-bar_p) has exactly n elements (p odd) and both
mu_n(k(P)) and mu_n(F_q) contain n of them, they coincide.

Reduction is a ring homomorphism, so its restriction to mu_n is a
group homomorphism; a bijective group homomorphism transports
subgroups, cosets, and coset-unions both ways.  QED

Remarks (care point (iv), the two split behaviors at q = p^2): if
p = 1 in (Z/n)^* (p splits completely in K), then f = 1 and
mu_n(F_q) already lies in the prime field F_p subset F_q; if p has
order 2 (e.g. p = -1 mod n), then f = 2 and k(P) = F_{p^2} = F_q.
Both behaviors are covered by the single statement above; different
choices of P over p are Galois-conjugate, so all counts below are
independent of the choice of P.  Also note q = p is only possible
when f = 1.

Care point (v), where 1/2 is used — the complete ledger:

1. the recursion defining S divides by 2 at each step (needs 1/2 in
   the base ring; over a row field, odd characteristic);
2. the x81 split C = (S-a)(S+a) reconstructs P, Q from S, a via
   +-a /2-free algebra but its uniqueness argument needs char /= 2;
3. Lemma 1's injectivity needs p odd (differences of 2-power roots of
   unity have 2-power norm);
4. X^n - 1 is separable in characteristic p iff p is odd (n = 2^s);
5. rows automatically satisfy this: n | q - 1 with n >= 2 forces q
   odd, so p = 2 never occurs at a row; D(n,h) below is defined as an
   odd integer (2-parts are discarded throughout).

**Lemma 2 (integrality; x83, banked).**  For any support R subset
mu_n(K), the recursion gives s_{h-q} in 2^{-(2q-1)} O, hence all
coefficients of S in 2^{-(2h-1)} O, and

```text
2^{4h-2} O_j(R) in O    for 1 <= j <= h-1.
```

Write O_j^cl := 2^{4h-2} O_j for these cleared obstructions.  (Proof:
x83, "Proof", denominator paragraph; replayed by the x83 verifier
through h = 12.)

## 3. The exceptional divisor D(n,h)

Fix n = 2^s and h.  All (n,h)-candidates over Q-bar are defined over
K (their supports lie in mu_n(K)), and there are finitely many (at
most C(n,2h) supports).  Two definitions of the exceptional integer,
one proof-minimal, one computable; both are used below.

### 3.1 The pointwise (proof-minimal) definition

For an anchored 2h-subset R subset mu_n(K) with 1 in R which is NOT a
candidate (some O_j(R) /= 0), let

```text
a(R) = ideal of O generated by { O_j^cl(R), 1 <= j <= h-1 } (/= 0),
```

and define

```text
D_pt(n,h) = odd part of  prod_{[R]}  N(a(R)) = [O : a(R)],
```

the product over Galois-orbit representatives of anchored
non-candidates.  Each factor is a nonzero positive integer (Lemma 2 +
a(R) /= 0), so D_pt(n,h) is a nonzero integer.  Its prime support is
EXACTLY the set of odd primes p admitting an extra anchored mod-p
point (see the proof of Theorem A3), so D_pt is the minimal correct
exceptional object; it is defined by enumeration over ~ C(n-1, 2h-1)
supports, which is not feasible at n = 1024, h ~ 20.  The computable
object follows.

### 3.2 The certified (computable) definition — the eliminant chain

Work on the anchored slice in (S)-coordinates: variables s_0, ...,
s_{h-1}, with lambda := S(1)^2 eliminated.  The defining system is

```text
F_0, ..., F_{2h-1}  =  the coefficients of  rem( X^n - 1 ,  S(X)^2 - S(1)^2 )
in Z[s_0..s_{h-1}]   (all integral: no division by 2 occurs here),
```

computable by s = log2(n) repeated squarings of X modulo
S^2 - lambda followed by the substitution lambda = S(1)^2 (this is
the computable incarnation of x83's triangularity: Lemma 0 already
eliminated c_1..c_{h-1}; the remainder system eliminates nothing
further but is a finite, explicitly generated system in h variables).
By section 1.2, for every field F of odd characteristic or F = K, the
solutions of {F_i = 0} in F^h are exactly the anchored
(n,h)-candidates over F (bijectively: point <-> S <-> C <-> support).

A **certificate** for (n,h) is data (u, m, g, cofactors) as follows,
all verifiable by exact polynomial identity checks over Z[1/2]:

- a separating linear form u = sum a_i s_i, a_i in Z;
- m(T) in Z[T] primitive, squarefree over Q (or m = a nonzero
  constant if the system has no char-0 solutions);
- (C1) delta_0 . m(u(s)) = sum_i q_i(s) F_i(s)  identically;
- (C2) for each i: delta_i . ( s_i . m'(u(s)) - g_i(u(s)) )
  = sum_j q_{ij}(s) F_j(s)  identically  (omit if m constant);
- (C3) for each j: e_j . m'(T)^{N_j} . F_j( g_0(T)/m'(T), ...,
  g_{h-1}(T)/m'(T) ) = r_j(T) . m(T)  identically after clearing
  denominators  (omit if m constant);
- (C4) Res(m, m') = +- 2^a . Delta_m, Delta_m odd (omit if m
  constant; then set Delta_m = 1 and lc(m) = m);
- (C5) e_u . ( sum_i a_i g_i(T) - T . m'(T) ) = r_u(T) . m(T)
  identically  ("u recovers T on the parametrization"; omit if m
  constant).

Define

```text
D(n,h) = odd part of   delta_0 . prod_i delta_i . prod_j e_j . e_u
                        . Delta_m . lc(m).
```

Such certificates exist: (C1)-(C3) is the rational univariate
representation of the zero-dimensional Q-scheme {F_i = 0} (shape:
Rouillier's RUR; [CITATION NEEDED — F. Rouillier, "Solving
zero-dimensional systems through the rational univariate
representation", AAECC 9 (1999); exact statement needed: every
zero-dimensional ideal I subset Q[s] with a separating form u admits
m, g_i in Q[T] with I's variety = { (g_i(tau)/m'(tau))_i : m(tau) =
0 } and u of each point recovering tau]).  The lemma below does NOT
assume that citation: it takes the certificate data as input and its
proof verifies everything it uses; the citation is provenance for
"the data always exists / how to compute it", and existence at each
concrete (n,h) is established by the computation itself plus the
identity checks.  If the char-0 solution set is empty, (C1) with m
constant is a Nullstellensatz certificate, whose existence at each
concrete (n,h) is again established by exhibiting it.

Relation between the two definitions: support(D_pt) subset
support(D(n,h)) union {p : p | D(n,h)} — i.e. p coprime to D(n,h)
implies p coprime to D_pt (immediate from Theorem A3's proof, which
shows p coprime to D(n,h) forbids the extra points whose existence
defines D_pt's support).

## 4. Theorem A3 (good reduction at fixed (n,h))

**Theorem A3.**  Fix n = 2^s, h >= 2, and a certificate for (n,h) as
in 3.2, with exceptional integer D(n,h).  Let q = p or p^2 with p an
odd prime, n | q - 1, and suppose

```text
gcd(p, D(n,h)) = 1.
```

Fix any maximal ideal P over p in O and identify mu_n(K) =
mu_n(F_q) by Lemma 1.  Then reduction mod P is a **bijection**

```text
{ anchored (n,h)-candidates over K }  -->  { anchored (n,h)-candidates over F_q },
```

and it matches coset-union candidates with coset-union candidates and
primitive with primitive.  Consequently:

(a) every mu_n(F_q)-point of W_h^a is the reduction of a
    characteristic-zero torsion point of W_h^a (and hence every
    mu_n(F_q)-point of W_h is the reduction of a characteristic-zero
    torsion point of W_h, by the free scaling action);

(b) # anchored primitive h-trades over (F_q, mu_n)
    = # anchored primitive char-0 candidates =: T^a_prim(n,h);

(c) with X24 (banked): T^a_prim(n,h) = 0 — char-0 candidates are
    trades over Q-bar, X24 forces them to be full mu_h fibers, which
    are coset-unions.  So the row has NO primitive h-trades in the
    square-shift currency:  zero, not merely bounded.

*Proof.*  All s-coordinates of candidates over K lie in 2^{-(2h-1)} O
(Lemma 2), so reduction mod P of char-0 candidates is defined (p
odd).  Reduction of a candidate is a candidate: the equations F_i have
integer coefficients and reduction is a ring homomorphism, so F_i = 0
is preserved; the support of the reduced C is the P-reduction of the
support (Lemma 1: 2h distinct mu_n(K)-roots reduce to 2h distinct
mu_n(F_q)-roots, which then exhaust the roots of the reduced monic
degree-2h polynomial).

Injectivity: distinct char-0 candidates have distinct supports in
mu_n(K), which reduce to distinct subsets of mu_n(F_q) (Lemma 1),
hence distinct reduced candidates.  (When m is non-constant this is
re-proved by the certificate: distinct candidates have distinct
u-values among the roots of m — by (C2), u determines the point —
and roots of m reduce injectively since p does not divide Delta_m.)

Surjectivity — the heart.  Let s-bar in F_q^h solve {F_i = 0} (an
anchored F_q-candidate; note its coordinates automatically lie in
F_q since the support lies in mu_n(F_q)).

Case m constant (empty char-0 fiber): reducing (C1) mod P gives
delta_0-bar . m-bar = 0 with both factors nonzero in F_q (p coprime
to delta_0 and to the odd part of the constant m; the 2-power part is
a unit): contradiction, so no F_q-candidate exists and surjectivity
is vacuous — the bijection is empty <-> empty.

Case m non-constant: let u-bar = u(s-bar).  Reducing (C1) at s-bar:
delta_0-bar . m-bar(u-bar) = 0, and delta_0-bar /= 0, so m-bar(u-bar)
= 0.  Since p does not divide lc(m) . Delta_m, m-bar has degree
deg m and is squarefree, so m-bar'(u-bar) /= 0.  Reducing (C2) at
s-bar: s-bar_i . m-bar'(u-bar) = g-bar_i(u-bar), i.e.

```text
s-bar_i = g-bar_i(u-bar) / m-bar'(u-bar):
```

the point is determined by u-bar.  Now lift the root.  First, every
root tau of m over Q-bar lies in K and is 2-integral: by (C3),
sigma(tau) = (g_i(tau)/m'(tau))_i is a char-0 candidate, so its
coordinates lie in 2^{-(2h-1)} O subset K (Lemma 2 applied to its
support, which lies in mu_n(K)); by (C5) and m'(tau) /= 0,
tau = u(sigma(tau)) = sum a_i sigma(tau)_i, an integer combination of
2-integral elements of K.  So over K, m = lc(m) . prod_r (T - tau_r)
with every tau_r 2-integral; reducing this factorization mod P shows
the roots of m-bar are exactly the reductions tau_r-bar, which are
distinct (m-bar squarefree).  Hence u-bar = tau_r-bar for exactly
one r.  Let sigma(tau_r) = (g_i(tau_r)/m'(tau_r))_i be the
char-0 point attached to tau_r: it solves {F_i = 0} by (C3) (evaluate
the identity at T = tau_r; m(tau_r) = 0 and m'(tau_r) /= 0 and e_j is
a nonzero rational away from p), so it is a char-0 anchored
candidate; and its reduction has coordinates
g-bar_i(tau_r-bar)/m-bar'(tau_r-bar) = g-bar_i(u-bar)/m-bar'(u-bar)
= s-bar_i.  So s-bar is the reduction of the char-0 candidate
sigma(tau_r).  (Note the logic: the roots of m need not a priori be
u-values of candidates; what the argument uses is only (C3)'s
direction — every root of m yields a candidate via sigma.  Combined
with (C1)+(C2), the roots and the candidates are in fact in
bijection, which is the local constancy used in section 5.)

Coset-union matching: by Lemma 1 the support identification is a
group isomorphism, so R is a mu_d-coset-union iff red_P(R) is.

(a) restates surjectivity on the slice; the unanchored statement
follows by scaling (every mu_n(F_q)-point of W_h scales by the
inverse of its first coordinate — an element of mu_n(F_q) — to an
anchored one, and the char-0 lift scales back by the corresponding
element of mu_n(K)).

(b) anchored trades = anchored candidates on both sides (section
1.3: lambda = S(1)^2 is a square in the field of the point), and the
bijection preserves primitivity.

(c) a char-0 anchored candidate C splits over Q-bar (lambda /= 0 is
automatically a square there) into a genuine trade P, Q: disjoint
h-subsets of mu_n(Q-bar) = mu_n(K)... with equal e_1..e_{h-1}.  X24
(applied to mu_n(C), which contains mu_n(Q-bar) after any embedding)
says such trades exist only for h a power of two and are then full
mu_h fibers, i.e. R = P union Q is a union of mu_h-cosets: a
coset-union.  So no primitive char-0 candidate exists.  QED

Remark (choice of P): a different P' over p is sigma(P) for some
sigma in Gal(K/Q); sigma permutes the char-0 candidates and fixes the
F_q-side counts, so the bijection's existence and all counts are
P-independent.

Remark (what "extra" means, and exactness of D_pt): if p IS
exceptional, the failing object is surjectivity: an F_q-candidate
whose char-0 identification (via Lemma 1 on supports) is a
NON-candidate R with all O_j^cl(R) in P — equivalently a(R) subset
P, equivalently p | N(a(R)), equivalently p in support(D_pt).  So
extras exist at p iff p | D_pt(n,h): D_pt's support is exactly the
exceptional set, and Theorem A3 shows support(D_pt) subset
support(2 D(n,h)).  This is the F_193 / q-sweep non-monotonicity
phenomenon in its final form: those primes divide the corresponding
exceptional integers.

## 5. Scheme-theoretic remark: flatness and multiplicity (care point (iii))

The certified route above is self-contained; this remark records the
standard geometric picture and the multiplicity statement used in the
failure-mode analysis.

Let B^a_{n,h} = Z[1/2][s_0..s_{h-1}]/(F_0..F_{2h-1}).  Every
geometric fiber of Spec B^a_{n,h} -> Spec Z[1/2] is finite (its
points are anchored candidates over that field, of which there are at
most C(n-1, 2h-1)), and all fiber points have 2-integral coordinates.

- Away from the finitely many primes where B^a_{n,h} has Z-torsion,
  the minimal primes of B^a_{n,h} all have characteristic 0 (an
  element of a minimal prime is a zerodivisor; a rational prime p
  that is a zerodivisor on B^a means Z-torsion), so every F-bar_p
  point of the special fiber is the specialization of a
  characteristic-zero point: surjectivity of reduction "by
  flatness".  This recovers Theorem A3(a) with D replaced by the
  torsion exponent of B^a — an alternative computable definition
  (Smith normal form of a presentation), equivalent for our purposes
  but heavier to certify than the RUR route; we do not use it.
- Local constancy of the fiber count: for p coprime to D(n,h), the
  proof of Theorem A3 shows # points(fiber at p) = # roots of m-bar
  = deg m = # points(generic fiber): the certified D(n,h) IS the
  explicit conductor/discriminant datum making the fiber count
  locally constant, which is the precise content requested of
  D(n,h).  (The general-theory versions — generic flatness [CITATION
  NEEDED — EGA IV 6.9.1, exact statement: a finite-type module over
  a noetherian integral base is flat over a nonempty open of the
  base] and semicontinuity of fiber degree — are not needed: the
  certificate replaces them with explicit integers.)
- Multiplicity at bad p: for p | D(n,h), the fiber can gain points
  (D_pt's support) and char-0 points can collide.  The count of
  F-bar_p points is still bounded by dim_{F_p}(B^a tensor F_p) when
  that is finite, but no useful a-priori bound below the Bezout-type
  bound is claimed here; the assembly handles bad p by direct
  enumeration (Gap G3 below and
  `a_closure_assembly.md` section "failure mode").

## 6. The h-only variant, and why naive n-uniformity is false

The DAG node asks for an exceptional set S(h) depending on h only.
In the naive reading — a single integer D(h) with: for all n and all
p coprime to D(h), no extras at (n, h) — this is **false as a
target shape**: extras at level n arise from anchored non-candidates
R subset mu_n with a(R) subset P, and as n grows through 2-powers,
new non-candidates appear whose obstruction values are new nonzero
cyclotomic integers with new prime divisors; nothing bounds their
prime support uniformly in n (the verified q-sweep exceptional primes
at increasing n illustrate this).  The correct forms are:

- **A3(n,h) (proved above):** exceptional integer D(n,h) per pair,
  computable once per pair, row-independent within the row class
  (all Row-C-class rows share n = 2^10; all prize rows share
  n = 2^41).  This is exit (ii) of the DAG node ("compute once,
  per-row GCD"), and it is what the closure assembly consumes.
- **A3-strong (open, not needed for closure):** the char-0 side IS
  n-uniform: by A2/Laurent [CITATION NEEDED — M. Laurent,
  "Équations diophantiennes exponentielles", Invent. Math. 78
  (1984), exact statement needed: for a subvariety W of G_m^N over
  Q-bar, the torsion points of W lie in finitely many torsion cosets
  contained in W], the primitive torsion candidates of W_h^a over
  ALL n number at most C(h); with X24 this set is empty, so
  A2's role in this lane is packaging, not load-bearing.  What
  remains genuinely open in the h-only direction is a uniform-in-n
  description of the BAD-PRIME side, e.g. "p is exceptional at (n,h)
  only if p | D(h) OR p has small order in (Z/n)^*" — no such
  statement is proved or claimed here.  Gap G4.

## 7. Gap ledger and citations

- **G1 [CITATION NEEDED, provenance only]:** Rouillier's RUR
  (existence/computation of certificates).  Not load-bearing: at each
  concrete (n,h) the certificate is verified by identity checks, and
  Theorem A3's proof uses only the verified identities.
- **G2 [CITATION NEEDED, packaging only]:** Laurent's theorem, for
  the n-uniform char-0 count (A2's node).  Not on the fixed-n
  critical path: at fixed n the char-0 candidate set is finite
  outright, and X24 (banked, proved in-repo) supplies the
  classification.
- **G3 [named gap]:** no a-priori multiplicity bound at bad primes
  p | D(n,h) beyond Bezout; handled by per-row enumeration + the
  banked n^3 absorbency (quantified in `a_closure_assembly.md`).
- **G4 [named gap]:** the h-only uniform bad-prime statement
  (section 6); not needed for the closure at official rows.
- **G5 [named input]:** existence of the concrete certificates at
  n = 1024, h in the window — a computation (the parallel pilot's
  deliverable), not a theorem; Theorem A3 is conditional on the
  certificate DATA existing and passing its identity checks at each
  (n,h) consumed.  At small (n,h) the verifier exhibits the
  mechanism end-to-end ((n,h) = (16,3): empty char-0 fiber,
  Nullstellensatz-style exceptional primes, exact match against
  brute-force row trades, including a q = p^2 row).
- Cyclotomic facts used (norm of 1 - zeta_{2^j} is a power of 2;
  X^n - 1 separable away from 2) are proved inline in Lemma 1; the
  full O_K = Z[zeta_n] is never used.

## 8. Verification

Run:

```bash
python3 experimental/scripts/verify_a3_good_reduction.py
```

Sections: (S1) quasi-homogeneity of O_j at h = 3, 4, symbolic;
(S2) Lemma 0 graph/triangularity at h = 3, 4, symbolic; (S3) Lemma 1
norm facts at n = 16, exact; (S4) end-to-end A3 mechanism at
(n,h) = (16,3): char-0 emptiness (X24 instance), pointwise
exceptional-prime support, exact equivalence "trades at F_q iff p
exceptional" across all rows q = p <= 700 and extension rows
q = p^2 in {49, 529}; (S5) anchored/orbit accounting identity on the
same data; (S6) budget arithmetic against the banked QA.22/W4
certificates (consumed by `a_closure_assembly.md`).

Current upstream replay: **15 PASS, 0 FAIL** (the original 14 checks plus
the pinned-certificate check).  Notable outputs: the (16,3)
exceptional set over the tested rows is exactly {7, 17, 97} (7 via
the extension row q = 49), and it matches the brute-force row trade
census in both directions; the trade-bearing rows carry 352 / 16 / 56
unordered trades (p = 17 / 97 / 7^2) with the orbit identity
#T * 2h = n * #anchored exact on each.
