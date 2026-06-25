# L1 Full-List Quotient Proof Program

Status: CONJECTURAL / PROOF PROGRAM.

Date: 2026-06-24.

Agent/model: Codex.

## Conjecture 1. Full-List Quotient-Budgeted L1

Fix a rate window and an entropy slack `epsilon > 0`.  There should be
constants `B,C,N_0`, depending only on the window and on `epsilon`, with the
following property.

Let `H_n <= F_q^*` be a smooth cyclic domain of order `n >= N_0`, with
generated field `q = poly(n)`.  Let

```text
k = rho n + O(1),
s = k + sigma,
```

and assume the generated-field reserve and lower cutoff clear:

```text
sigma log_2(q) >= (1 + epsilon) log_2 binom(n,s),
sigma >= C n / log n.
```

For every received word `U : H_n -> F_q`, define the actual Reed--Solomon list

```text
ImgFib_U(s) = { P in F_q[X] : deg P < k and
                |{x in H_n : U(x)=P(x)}| >= s }.
```

For `P in ImgFib_U(s)`, put

```text
A_P(U) = { x in H_n : U(x)=P(x) },
Stab(P;U) = { h in H_n : h A_P(U) = A_P(U) }.
```

For each divisor `d | n`, let

```text
Q_d^list(U,s) = #{ P in ImgFib_U(s) : |Stab(P;U)| = d }.
```

The conjecture is the primitive full-list bound

```text
Q_1^list(U,k+sigma) <= n^B
```

uniformly in `U`.  Equivalently,

```text
|ImgFib_U(k+sigma)|
  <= sum_{d>1} Q_d^list(U,k+sigma) + n^B.
```

This statement is deliberately about listed codewords, not raw support
subfibers.  The quotient term is not claimed small here; it is the structured
mass that must be charged to the separate quotient ledger.

## Why This Is The Right Object

The raw arbitrary-word support fiber is too large for a positive local limit:
one high-agreement codeword contributes every `s`-subsupport of its agreement
set.  Passing to `ImgFib_U(s)` removes that artificial multiplicity while
retaining the actual list object consumed by the repaired L1 package.

The exact stabilizer split also avoids treating quotient-periodic structure as
noise.  A large list caused by cyclic quotient symmetry should be paid for by
the quotient ledger.  Conjecture 1 asks only that the stabilizer-primitive
remainder is polynomial once the entropy reserve and lower cutoff clear.

## Proof Strategy

The intended proof is by contradiction.

1. **Sparse-syndrome formulation.**  Identify `ImgFib_U(s)` with the set of
   low-weight errors in one syndrome coset,

   ```text
   M_C e = z,        wt(e) <= n-s.
   ```

   The agreement set of the corresponding listed codeword is the zero set of
   `e`.

2. **High-multiplicity extraction.**  If `Q_1^list(U,s) > n^B`, extract a
   bounded-complexity sublist certificate: a small agreement hypergraph or RIM
   rank-defect witness whose listed codewords are still primitive after the
   quotient ledger is removed.

3. **Quotient and low-defect removal.**  Separate exact quotient-periodic
   strata, folded strata, and low-defect quotient closures before calling the
   remaining family aperiodic.  Exact stabilizer one is not by itself a
   sufficient aperiodicity condition.

4. **Aperiodic extension counting.**  For each extracted certificate `c`,
   prove a uniform bound

   ```text
   sum_c |E_b^aper(c)| <= n^(B-theta)
   ```

   for some `theta > 0`, after the quotient extension sets are charged to the
   quotient ledger.

5. **Packing closure.**  Combine the certificate packing lemma with the
   quotient and aperiodic extension budgets.  The leftover packing term is
   `O(log n)` at the intended cutoff and is absorbed by `n^B`.

## Theorem J. Full-List Johnson Region

Status: PROVED.

Let `H` be any Reed--Solomon evaluation domain of size `n`, and let
`C = RS[H,k]`.  For every received word `U : H -> F_q`, define

```text
ImgFib_U(s) = { P in F_q[X] : deg P < k and
                |{x in H : U(x)=P(x)}| >= s }.
```

Then:

1. If `2s > n+k-1`, then `|ImgFib_U(s)| <= 1`.
2. If `s^2 > n(k-1)`, then

```text
|ImgFib_U(s)| <= n(n-k+1) / (s^2 - n(k-1)).
```

In particular, because `Q_1^list(U,s) <= |ImgFib_U(s)|`, Conjecture 1 holds
with a polynomial primitive remainder throughout the ordinary Johnson region
`s^2 > n(k-1)`, without using any quotient-budget term.

### Proof

Let `P_1,...,P_L` be the distinct polynomials in `ImgFib_U(s)`, and write

```text
A_i = { x in H : U(x)=P_i(x) }.
```

If `L=0`, there is nothing to prove.  Assume `L>0`.
Then `|A_i| >= s` for every `i`.  Distinct degree-`<k` polynomials agree on at
most `k-1` points, hence

```text
|A_i cap A_j| <= k-1        for i != j.
```

The unique-decoding claim follows immediately: two listed codewords would have
`|A_i cap A_j| >= 2s-n`, contradicting `2s-n > k-1`.

For the Johnson bound, put

```text
m_x = #{ i : x in A_i },        I = sum_x m_x.
```

Then `I >= Ls`, while the pairwise-intersection bound gives

```text
sum_x binom(m_x,2) <= binom(L,2)(k-1).
```

By Cauchy--Schwarz,

```text
I^2 <= n sum_x m_x^2
    = n(I + 2 sum_x binom(m_x,2))
    <= n(I + L(L-1)(k-1)).
```

Since also `I <= Ln`, we get

```text
L^2 s^2 <= n(Ln + L(L-1)(k-1)).
```

After dividing by `L` and rearranging,

```text
L(s^2 - n(k-1)) <= n(n-k+1).
```

When `s^2 > n(k-1)`, this is the claimed bound.

### Role In The L1 Program

The theorem supplies a proved base region for the full-list quotient program.
The remaining L1 difficulty is not ordinary pairwise packing; it is the
sub-Johnson range where `s^2 <= n(k-1)`.  In that range the quotient ledger,
sunflower reductions, and aperiodic extension counts below are genuinely needed.

### Profile-Tail Form

For `a>k`, let

```text
N_{>=a}(U) = #{ P : deg P < k and |A_P(U)| >= a },
N_{=a}(U)  = #{ P : deg P < k and |A_P(U)| = a }.
```

Then the same proof gives, for every `a` with `a^2 > n(k-1)`,

```text
N_{>=a}(U) <= n(n-k+1) / (a^2 - n(k-1)),
N_{=a}(U)  <= n(n-k+1) / (a^2 - n(k-1)).
```

If `2a > n+k-1`, then `N_{>=a}(U) <= 1`, and hence `N_{=a}(U) <= 1`.

This is just Theorem J applied with threshold `s=a`, but it is the form needed
by stratified codegree reductions: any later argument may sum over agreement
sizes using this proved Johnson tail wherever the punctured or unpunctured
profile lies inside the ordinary Johnson region.

### Punctured Profile-Tail Form

The same statement holds on every punctured evaluation set.  Let `A subset H`
have size `N`, let `U_A : A -> F_q`, and consider distinct codewords in the
punctured code obtained by restricting degree-`<k` polynomials to `A`.  Put

```text
k_A = min(k,N).
```

The punctured code has dimension `k_A`, and two distinct punctured codewords
agree on at most `k_A-1` points.  Put

```text
N_A,>=a(U_A) = #{ c in RS[A,k] : |{x in A : U_A(x)=c(x)}| >= a },
N_A,=a(U_A)  = #{ c in RS[A,k] : |{x in A : U_A(x)=c(x)}| = a }.
```

If `a^2 > N(k_A-1)`, then

```text
N_A,>=a(U_A) <= N(N-k_A+1) / (a^2 - N(k_A-1)),
N_A,=a(U_A)  <= N(N-k_A+1) / (a^2 - N(k_A-1)).
```

If `2a > N+k_A-1`, then `N_A,>=a(U_A) <= 1`.

This is not a new proof: it is Theorem J applied to the evaluation domain
`A`, with `k` replaced by the effective punctured dimension `k_A`.  It is
recorded separately because punctured domains are the natural objects in
codegree decompositions and interleaved-list reductions.

### Abel Profile Ledger

Let

```text
T(a)=N_{>=a}(U),        E(a)=N_{=a}(U)
```

for `a=s,...,n`, and let `w(a)` be any nondecreasing nonnegative weight on
this interval.  Then

```text
sum_{a=s}^n E(a) w(a)
  = T(s)w(s) + sum_{a=s+1}^n T(a)(w(a)-w(a-1)).
```

The same identity holds on a punctured domain `A` with `n` replaced by `N`.
Consequently, whenever a stratified reduction charges each listed codeword by
a monotone cost depending only on its agreement size, it may use the Johnson
tail bounds above for every agreement level in the ordinary Johnson region and
leave only the genuinely sub-Johnson levels to the non-pairwise L1 machinery.

The identity is just summation by parts: since

```text
E(a)=T(a)-T(a+1),        T(n+1)=0,
```

telescoping gives the displayed formula.

### Johnson-Covered Weighted Tail

On a punctured domain of size `N`, put `k_A=min(k,N)` and define the Johnson
tail envelope

```text
J_N,k(a) =
  1                                               if 2a > N+k_A-1,
  N(N-k_A+1) / (a^2 - N(k_A-1))                  otherwise,
```

for agreement levels satisfying `a^2 > N(k_A-1)`.  Let

```text
a_0 >= s,        a_0^2 > N(k_A-1),
```

and let `w(a)` be nondecreasing and nonnegative for `a_0 <= a <= N`.  Then
the Johnson-covered part of any punctured agreement profile satisfies

```text
sum_{a=a_0}^N N_A,=a(U_A) w(a)
  <= J_N,k(a_0)w(a_0)
     + sum_{a=a_0+1}^N J_N,k(a)(w(a)-w(a-1)).
```

Thus a weighted stratified reduction can be split cleanly at the first
Johnson-covered level `a_0`: the displayed formula controls the high-agreement
tail, and only levels `a<a_0` remain to be controlled by quotient,
sunflower, or aperiodic input.

This follows from the Abel profile ledger and the punctured Johnson tail bound
`T(a)<=J_N,k(a)` at every level in the displayed range.

## First Lemma Target

The first obstruction family isolated by the falsification scans is a
glued-codeword sunflower.  Let `C subset H_n` have size `k-1`, let
`T_1,...,T_M` be disjoint petals in `H_n \ C` of size `sigma+1`, and define

```text
L_C(X) = prod_{x in C}(X-x),
P_i(X) = c_i L_C(X)
```

with distinct nonzero `c_i`.  Define `U` by putting `U=P_i` on `T_i`, and
`U=0` on `C` and the unused background.

**Lemma target.**  For this sunflower received word, the number of non-planted
primitive listed codewords whose agreement sets mix several petals is bounded
by a fixed polynomial in `n`, and preferably by a small polynomial in the
planted floor

```text
M <= floor((n-k+1)/(sigma+1)).
```

Equivalently, if mixed-petal amplification is super-polynomial, then the
agreement equations must force quotient, low-defect, or another explicitly
budgeted structured family.

## Lemma 2. Sunflower Core-Defect Reduction

Status: PROVED.

Use the notation of the sunflower construction above.  Let

```text
R = H_n \ (C union T_1 union ... union T_M)
```

be the unused background, and let `P in ImgFib_U(s)` have agreement set
`A=A_P(U)`.  Put

```text
C_P = A cap C,
R_P = A cap R,
S_i = A cap T_i,
D = C \ C_P,
d = |D|.
```

Then there is a unique polynomial `W_P` with `deg W_P <= d` such that

```text
P = L_{C_P} W_P,
W_P(x) = 0                  for x in R_P,
W_P(x) = c_i L_D(x)         for x in S_i.
```

Moreover, if `P` is not one of the planted codewords `c_i L_C`, then

```text
|S_i| <= d        for every petal T_i.
```

In particular, any non-planted extra codeword that contains a full petal must
miss at least `sigma+1` core points.

### Proof

The polynomial `P` agrees with `U=0` on `C_P union R_P`, so it vanishes on
`C_P`.  Hence `P=L_{C_P}W_P` for a unique polynomial `W_P`.  Since
`|C|=k-1` and `d=|C\C_P|`, one has

```text
deg W_P < k-|C_P| = d+1,
```

so `deg W_P <= d`.  For `x in R_P`, the factor `L_{C_P}(x)` is nonzero, and
`P(x)=U(x)=0`; hence `W_P(x)=0`.  For `x in S_i`, one has

```text
L_{C_P}(x) W_P(x) = P(x) = U(x) = c_i L_C(x).
```

Since `T_i` is disjoint from `C`, the factor `L_{C_P}(x)` is nonzero.  Writing
`L_C=L_{C_P}L_D` gives

```text
W_P(x)=c_i L_D(x).
```

Now suppose `|S_i|>d` for some petal.  The polynomial

```text
W_P - c_i L_D
```

has degree at most `d` and more than `d` roots, so it is identically zero.
Thus `W_P=c_iL_D` and therefore

```text
P=L_{C_P}W_P=c_iL_C,
```

which is the planted codeword for petal `T_i`.  Therefore a non-planted
codeword has `|S_i|<=d` on every petal.  A full petal has size `sigma+1`, so a
non-planted codeword containing a full petal must have `d>=sigma+1`.

### Consequences

For a non-planted mixed-petal extra, the remaining unknown is no longer a
degree-`<k` polynomial on `H_n`.  It is a degree-`<=d` polynomial `W_P` whose
values on each petal lie on one of the shifted targets `c_iL_D`.  The agreement
condition gives

```text
sum_i |S_i| >= d + 1 + sigma - |R_P|.
```

Combined with the per-petal cap `|S_i|<=d`, this forces genuinely mixed-petal
behavior whenever the background agreement `|R_P|` is small.  The remaining
amplification problem is therefore a lower-dimensional incidence question:
count degree-`<=d` polynomials that have many zeros across the family

```text
W - c_i L_D        on T_i.
```

This is the first precise target for the mixed-petal amplification bound.

## Lemma 3. Fixed-Defect Sunflower Layers Are Polynomial

Status: PROVED.

For the sunflower received word above, fix an integer `d0 >= 0`.  The number
of listed codewords `P in ImgFib_U(s)` whose agreement set misses at most `d0`
core points is at most

```text
sum_{d=0}^{d0} binom(k-1,d) binom(n-k+1,d+1).
```

In particular, for fixed `d0` this contribution is `O_{d0}(n^{2d0+1})`.

### Proof

Let `P` have core defect `d <= d0`, and keep the notation of Lemma 2.  Once
the missed core set

```text
D = C \ C_P
```

is fixed, the codeword is determined by the degree-`<=d` polynomial `W_P`,
because `P=L_{C_P}W_P`.

Let `B` be the non-core part of the domain,

```text
B = H_n \ C.
```

For fixed `D`, Lemma 2 gives a target value on every point of `B`:

```text
tau_D(x) = 0             if x is in the unused background R,
tau_D(x) = c_i L_D(x)   if x is in the petal T_i.
```

The list condition gives

```text
|A_P(U) cap B| >= s - |C_P| = (k+sigma) - (k-1-d)
                = sigma + d + 1.
```

Thus `W_P` agrees with `tau_D` on at least `d+1` points of `B`.  With a fixed
ordering of `B`, choose the first `d+1` such points.  A degree-`<=d` polynomial
is uniquely determined by its values at these distinct points, so the pair

```text
(D, first d+1 non-core agreement points)
```

determines `W_P`, hence determines `P`.  For exact defect `d`, there are at
most

```text
binom(k-1,d) binom(n-k+1,d+1)
```

such pairs.  Summing over `0 <= d <= d0` gives the claimed bound.

### Consequences

The mixed-petal sunflower obstruction is harmless on every fixed-defect layer.
The numerical extras seen in the `n=16` scans all lie in small-defect layers,
so Lemma 3 explains why those examples amplify the planted floor only mildly.

Any super-polynomial sunflower counterexample to Conjecture 1 must therefore
come from core defect `d` growing with `n`.  The next proof target is a
large-defect incidence bound for the same equations

```text
W - c_i L_D        on T_i,
```

or a proof that large-defect concentration forces quotient, low-defect, or
another budgeted structure.

## Lemma 4. Petal-Support Tradeoff

Status: PROVED.

Let `P` be a non-planted listed codeword for the sunflower received word.  Use
the notation of Lemma 2, and write

```text
r = |R_P|,
h = sum_i |S_i|,
t = #{ i : S_i is nonempty }.
```

If `d>0`, then

```text
t >= ceil((sigma+d+1-r)/d),
```

and equivalently

```text
(t-1)d >= sigma+1-r.
```

If the sunflower is maximal, so that the unused background has size
`b=|R|<sigma+1`, then every non-planted listed codeword satisfies `t>=2`.
More generally, any non-planted listed codeword supported on at most `T`
petals satisfies

```text
d >= ceil((sigma+1-b)/(T-1))        for T >= 2.
```

### Proof

The list condition and the definition of the core defect give

```text
h + r = |A cap (H_n \ C)| >= s - |C_P|
      = (k+sigma) - (k-1-d) = sigma+d+1.
```

Thus `h >= sigma+d+1-r`.  Lemma 2 gives the per-petal bound `|S_i|<=d` for a
non-planted codeword, so `h <= td`.  Combining these inequalities gives

```text
td >= sigma+d+1-r,
```

which is the asserted tradeoff.

If the sunflower is maximal, then `r<=b<sigma+1`.  First, `d=0` is impossible:
the per-petal bound gives `h=0`, while the list condition gives
`h+r>=sigma+1`.  Thus `d>0`.  A zero- or one-petal extra would have
`(t-1)d<=0`, contradicting `(t-1)d >= sigma+1-r > 0`.  The displayed lower
bound for `d` follows from the same inequality and `r<=b`.

### Consequences

Lemma 4 explains why the small `F_97,n=16,k=8,s=10` extras are genuinely
mixed-petal.  In that row `sigma=2` and the maximal sunflower has no unused
background, so a defect-`2` extra must touch at least three petals, while a
two-petal extra must have defect at least `3`.

For the asymptotic proof program, the remaining danger is now sharper.  A
counterexample must either spread across many petals, or it must pay a large
core defect proportional to `sigma/(T-1)` if it is supported on only `T`
petals.  The next incidence estimate can therefore be organized by the pair
`(d,t)` rather than by all mixed-petal extras at once.

## Lemma 5. Background-Free Two-Petal Pencil

Status: PROVED.

Assume the sunflower has no unused background, so

```text
H_n = C union T_1 union ... union T_M.
```

Put `ell=sigma+1=|T_i|`.  Let `P` be a non-planted listed codeword touching
exactly two petals, say `T_i` and `T_j`.  Then

```text
d = ell,        S_i = T_i,        S_j = T_j,
```

and the missed-core locator `L_D` lies in the affine pencil

```text
L_D = (1+beta) L_{T_i} - beta L_{T_j}
```

for some `beta in F_q`.

Conversely, if `D subset C` has size `ell` and satisfies the displayed pencil
identity for some pair of petals and some `beta`, then it produces a listed
codeword agreeing with `U` on

```text
(C \ D) union T_i union T_j.
```

If this codeword has no further petal agreements, it is exactly a two-petal
non-planted extra.

### Proof

Since `R` is empty and `t=2`, Lemma 4 gives

```text
d >= sigma+1 = ell.
```

The list condition gives `h >= sigma+d+1`, while the two petals have total
size `2ell`.  Thus

```text
sigma+d+1 <= h <= 2ell.
```

Since `ell=sigma+1`, this forces `d=ell` and `h=2ell`.  Therefore the two
touched petals are full:

```text
S_i = T_i,        S_j = T_j.
```

By Lemma 2,

```text
W_P - c_i L_D
```

vanishes on `T_i`, and

```text
W_P - c_j L_D
```

vanishes on `T_j`.  All three polynomials have degree at most `ell`, so there
are scalars `alpha_i, alpha_j` with

```text
W_P - c_i L_D = alpha_i L_{T_i},
W_P - c_j L_D = alpha_j L_{T_j}.
```

Subtracting gives

```text
(c_j-c_i)L_D = alpha_i L_{T_i} - alpha_j L_{T_j}.
```

The petal scalars are distinct, so `c_j-c_i` is nonzero.  Put

```text
beta = alpha_j / (c_j-c_i).
```

Because both sides have leading coefficient `1`, the leading coefficients in
the previous identity give

```text
alpha_i / (c_j-c_i) = 1 + beta.
```

Dividing by `c_j-c_i` gives the asserted pencil identity.

Conversely, suppose

```text
L_D = (1+beta)L_{T_i} - beta L_{T_j}.
```

Let `Delta=c_j-c_i` and define

```text
W = c_iL_D + (1+beta)Delta L_{T_i}.
```

Then

```text
W - c_iL_D = (1+beta)Delta L_{T_i},
W - c_jL_D = beta Delta L_{T_j}.
```

Therefore `P=L_{C\D}W` agrees with `U` on `C\D`, on `T_i`, and on `T_j`.
The agreement count is

```text
|C\D| + |T_i| + |T_j| = (k-1-ell) + 2ell = k+sigma = s,
```

so `P` is listed.  It is non-planted: if `W` vanished on all of `D`, then
`W` would be a scalar multiple of `L_D`, forcing `L_D` to be a scalar multiple
of `L_{T_i}` or `L_{T_j}`, impossible because `D`, `T_i`, and `T_j` are
disjoint.  Since this non-planted codeword contains two full petals, Lemma 2
forces its actual core defect to be at least `ell`; since it already vanishes
on `C\D`, its actual core defect is at most `ell`.  Hence the actual missed
core is exactly `D`.  If no other petal contributes an agreement, the codeword
is exactly a two-petal extra.

### Consequences

The background-free two-petal obstruction is no longer a free large-defect
family.  It is a locator-pencil problem: for each pair of petals, count the
core subsets `D` of size `ell` whose locator polynomial lies on the line

```text
{ (1+beta)L_{T_i} - beta L_{T_j} : beta in F_q }.
```

The two-petal profile seen in the `F_97,n=16,k=8,s=10` seed sweep is exactly
of this type: `ell=3`, defect `d=3`, and two full petals.  Future progress on
this subcase should attack splitting of this affine pencil inside the core,
rather than re-enumerating full received words.

## Lemma 6. Background-Free Two-Petal Count

Status: PROVED.

In the background-free sunflower setting of Lemma 5, the number of
non-planted listed codewords that touch exactly two petals is at most

```text
binom(M,2) q.
```

Consequently, in the generated-field regime `q=poly(n)`, the entire
background-free two-petal obstruction is polynomially bounded.  At the L1
lower cutoff `sigma >= C n/log n`, this bound is

```text
O(q log(n)^2).
```

### Proof

Each two-petal extra has a unique unordered pair of touched petals
`{T_i,T_j}`.  Fix the order `i<j`.  By Lemma 5, the missed-core locator lies
on the affine pencil

```text
L_D = (1+beta)L_{T_i} - beta L_{T_j}.
```

For this fixed pair, the map

```text
beta |-> (1+beta)L_{T_i} - beta L_{T_j}
```

is injective.  Indeed, two values of `beta` give the same polynomial only if
`L_{T_i}=L_{T_j}`, which is impossible because the petals are disjoint and
nonempty.  For a given polynomial in the pencil, there is at most one subset
`D subset C` whose locator polynomial equals it, since the roots determine
`D`.  Lemma 5 then gives at most one listed codeword for that pair and that
`beta`.

There are `binom(M,2)` unordered petal pairs and `q` possible values of
`beta`, proving the bound.  Since a background-free sunflower has

```text
M = (n-k+1)/(sigma+1),
```

the lower cutoff `sigma >= C n/log n` gives `M=O(log n)`, and hence
`binom(M,2)q = O(q log(n)^2)`.

### Consequences

This closes the exact background-free two-petal profile as a possible
super-polynomial obstruction to Conjecture 1 in the polynomial generated-field
window.  The remaining background-free sunflower cases either touch at least
three petals or involve a different structured degeneracy not captured by the
two-petal pencil.

## Lemma 7. Full-Petal CRT Compression

Status: PROVED.

Assume the sunflower has no unused background.  Let `I` be the exact set of
petals touched by a non-planted listed codeword `P`, and suppose every touched
petal is full:

```text
S_i = T_i        for i in I,
S_j = empty      for j notin I.
```

Put `t=|I|`, `ell=sigma+1`, and keep the missed-core set `D` and defect `d`
from Lemma 2.  Then

```text
ell <= d <= (t-1)ell.
```

Let

```text
N_I = prod_{i in I} L_{T_i}.
```

There is a unique polynomial `W_{D,I}` of degree `< t*ell` satisfying the CRT
conditions

```text
W_{D,I} = c_i L_D        mod L_{T_i}        for every i in I.
```

The listed codeword `P` is exactly

```text
P = L_{C\D} W_{D,I},
```

and the degree cutoff is

```text
deg W_{D,I} <= d.
```

Equivalently, the top `t*ell-d-1` coefficients of the CRT residue `W_{D,I}`
vanish.  Conversely, any pair `(D,I)` with `|I|>=2`, `|D|=d`, and
`ell <= d <= (t-1)ell` satisfying `deg W_{D,I}<=d` produces a listed codeword
that agrees with `U` on

```text
(C \ D) union union_{i in I} T_i.
```

If it has no agreements on petals outside `I` and `W_{D,I}` is nonzero on
`D`, then its exact missed-core set is `D` and its exact touched-petal set is
`I`.

### Proof

Since the codeword is non-planted and contains at least one full petal, Lemma 2
gives `d>=ell`.  The list condition gives

```text
t*ell = sum_{i in I} |S_i| >= sigma+d+1 = ell+d,
```

so `d <= (t-1)ell`.

For every touched petal, Lemma 2 gives

```text
W_P = c_i L_D        on T_i,
```

or equivalently `W_P = c_iL_D mod L_{T_i}`.  The petal locators are pairwise
coprime, so the Chinese remainder theorem gives a unique residue
`W_{D,I}` modulo `N_I`, represented by a polynomial of degree `< t*ell`.

The actual `W_P` has degree at most `d`, and the displayed inequality gives
`d < t*ell`.  Therefore `W_P` and `W_{D,I}` are two representatives of the same
CRT class with degree `< t*ell`; they are equal.  This proves the forward
direction and the coefficient-vanishing formulation.

Conversely, if `deg W_{D,I}<=d`, then `P=L_{C\D}W_{D,I}` has degree

```text
deg P <= (k-1-d)+d = k-1.
```

It agrees with `U` on `C\D` and on every petal in `I`.  Thus it has at least

```text
(k-1-d)+t*ell >= (k-1-d)+(ell+d) = k+sigma = s
```

agreements, and so it is listed.  The final exactness assertions follow
directly from excluding agreements outside `I` and zeros of `W_{D,I}` on `D`.

### Consequences

The full-petal part of the remaining `t>=3` problem is now an explicit
coefficient-vanishing problem.  For fixed `D` and `I`, the CRT residue is
linear in the coefficients of `L_D`; the obstruction is the vanishing of the
highest `t*ell-d-1` coefficients of that residue.

For `t=2`, this recovers Lemma 5 and Lemma 6.  For `t>=3`, it gives the next
concrete target: bound how often core locators make these CRT top
coefficients vanish, or show that many such vanishing events force quotient or
low-defect structure.

## Lemma 8. Full-Petal Rank Certificate

Status: PROVED.

Keep the background-free notation of Lemma 7.  Fix a touched-petal set `I`
with `t=|I|>=2`, and fix an integer

```text
ell <= d <= (t-1)ell.
```

Let `V_d` be the vector space of polynomials over `F_q` of degree at most `d`.
Define the linear CRT operator

```text
R_{I,d} : V_d -> F_q[X]_{< t*ell}
```

by requiring

```text
R_{I,d}(F) = c_i F        mod L_{T_i}        for every i in I.
```

Let

```text
pi_{>d} : F_q[X]_{< t*ell} -> F_q^{t*ell-d-1}
```

extract the coefficients of degrees `d+1,...,t*ell-1`, and put

```text
K_{I,d} = ker(pi_{>d} R_{I,d}).
```

Then the full-petal listed codewords with exact touched-petal set `I` and
core defect `d` inject into

```text
{ L_D : D subset C, |D|=d } cap K_{I,d}.
```

In particular, if

```text
r_{I,d} = rank(pi_{>d} R_{I,d}),
```

then their number is at most

```text
q^{d+1-r_{I,d}}.
```

### Proof

Lemma 7 sends each such codeword to its missed-core locator `L_D`.  The exact
missed-core set is part of the codeword data, so this map is injective.  The
same lemma says that the corresponding CRT residue has degree at most `d`,
which is exactly the condition

```text
pi_{>d} R_{I,d}(L_D) = 0.
```

Thus the image lies in the displayed split-locator intersection.

The linear map `pi_{>d}R_{I,d}` has kernel dimension `d+1-r_{I,d}` inside the
`d+1` dimensional space `V_d`.  The split locators form a subset of this
kernel, so there are at most `q^{d+1-r_{I,d}}` possible images, hence at most
that many full-petal listed codewords.

### Consequences

The remaining full-petal sunflower problem is now a rank problem.  A
polynomial bound follows for any regime in which

```text
d+1-r_{I,d} = O(log n / log q).
```

Since `q=poly(n)` in the generated-field window, it is enough to prove
`r_{I,d} >= d-O(1)` uniformly outside explicitly budgeted quotient or
low-defect strata.

Conversely, a super-polynomial full-petal family must create a large rank
defect in `pi_{>d}R_{I,d}` or an unusually large split-locator concentration
inside its kernel.  This is now a concrete finite-dimensional certificate
matching the rank-defect philosophy in the L1 repaired locator package.

## Lemma 9. Minimal-Defect Full-Petal Count

Status: PROVED.

Assume the sunflower has no unused background.  The number of non-planted
listed codewords whose touched petals are all full and whose core defect is
minimal,

```text
d = ell = sigma+1,
```

is at most

```text
binom(M,2) q.
```

This bound includes codewords touching three or more full petals.  Consequently,
at the L1 lower cutoff and in the generated-field window `q=poly(n)`, the
minimal-defect full-petal layer is polynomially bounded.

### Proof

Let `P` be such a codeword, with touched-petal set `I`.  Since `P` is
non-planted and contains a full petal, Lemma 2 gives `d>=ell`; by hypothesis
`d=ell`.  The list condition gives at least two full petals, because one full
petal plus the retained core would give only

```text
(k-1-ell)+ell = k-1 < s.
```

Choose the two smallest indices `i<j` in `I`.  Lemma 2 gives

```text
W_P - c_i L_D = alpha_i L_{T_i},
W_P - c_j L_D = alpha_j L_{T_j},
```

because both sides have degree at most `ell` and vanish on a full petal of
size `ell`.  The same leading-coefficient comparison as in Lemma 5 gives a
unique `beta in F_q` such that

```text
L_D = (1+beta)L_{T_i} - beta L_{T_j}.
```

Thus the codeword determines a certificate

```text
({i,j}, beta).
```

Conversely, this certificate determines `L_D`, hence `D`, and then determines
`W_P` by

```text
W_P = c_iL_D + (1+beta)(c_j-c_i)L_{T_i}.
```

Therefore two codewords with the same certificate are equal.  There are
`binom(M,2)` choices of `{i,j}` and `q` choices of `beta`, proving the bound.
At the lower cutoff, `M=O(log n)`, so this is `O(q log(n)^2)`.

### Consequences

The full-petal obstruction now has two closed polynomial layers:

```text
t=2, any allowed defect;
d=ell, any number of full petals.
```

The remaining full-petal danger must have both

```text
t>=3,        d>ell.
```

Equivalently, any further super-polynomial sunflower family must be a genuine
higher-defect, many-petal rank-defect phenomenon, not the minimal
locator-pencil mechanism seen in the first scans.

## Lemma 10. Bounded-Excess Full-Petal Count

Status: PROVED.

Assume the sunflower has no unused background.  Fix `e0 >= 0`.  The number of
non-planted listed codewords whose touched petals are all full and whose core
defect satisfies

```text
ell <= d <= ell+e0
```

is at most

```text
binom(M,2) sum_{e=0}^{e0} q^{2(e+1)}.
```

For fixed `e0`, this is polynomial in the generated-field window `q=poly(n)`.
At the L1 lower cutoff, where `M=O(log n)`, it is

```text
O_{e0}(q^{2e0+2} log(n)^2).
```

### Proof

Let `P` be such a codeword.  By Lemma 4, it touches at least two petals.
Choose the two smallest touched-petal indices `i<j`.  Put

```text
e = d - ell.
```

Since both petals are full, Lemma 2 gives

```text
W_P - c_i L_D = L_{T_i} A_i,
W_P - c_j L_D = L_{T_j} A_j,
```

where

```text
deg A_i <= e,        deg A_j <= e.
```

Indeed, all displayed polynomials have degree at most `d`, and division by the
degree-`ell` petal locator leaves degree at most `d-ell=e`.

Thus the codeword determines the certificate

```text
({i,j}, A_i, A_j).
```

Conversely, this certificate determines

```text
L_D = (L_{T_i}A_i - L_{T_j}A_j)/(c_j-c_i)
```

and then

```text
W_P = c_iL_D + L_{T_i}A_i,
P = L_{C\D}W_P,
```

whenever the right-hand side is a valid missed-core locator.  Therefore the
map from codewords to certificates is injective.  For fixed `e`, there are
`binom(M,2)` choices of `{i,j}` and at most `q^{e+1}` choices for each of
`A_i` and `A_j`.  Summing over `0 <= e <= e0` proves the bound.

### Consequences

This closes every bounded-excess full-petal layer.  The remaining full-petal
danger must have

```text
d - ell -> infinity,        t>=3.
```

Thus a future counterexample cannot come from the minimal locator-pencil
mechanism plus bounded perturbation.  It must use genuinely growing
core-defect excess, or it must leave the full-petal regime and use partial
petal agreements.

## Lemma 11. Two-Petal Syzygy Compression

Status: PROVED.

Return to the general sunflower notation of Lemma 2; the unused background may
be nonempty.  Let `P` be a non-planted listed codeword, and suppose it touches
two distinct petals `T_i,T_j`.  Put

```text
a_i = |S_i|,        a_j = |S_j|.
```

Then there are polynomials `A_i,A_j` satisfying

```text
deg A_i <= d-a_i,        deg A_j <= d-a_j,
```

and

```text
(c_j-c_i)L_D = L_{S_i}A_i - L_{S_j}A_j.
```

Moreover,

```text
W_P = c_iL_D + L_{S_i}A_i
    = c_jL_D + L_{S_j}A_j.
```

### Proof

By Lemma 2,

```text
W_P - c_iL_D
```

vanishes on `S_i`, and

```text
W_P - c_jL_D
```

vanishes on `S_j`.  Since `P` is non-planted, Lemma 2 also gives
`a_i,a_j <= d`.  Therefore

```text
W_P - c_iL_D = L_{S_i}A_i,
W_P - c_jL_D = L_{S_j}A_j
```

with the displayed degree bounds.  Subtracting these identities gives the
syzygy for `L_D`, and either identity recovers `W_P`.

### Counted Near-Saturated Corollary

Assume now that the sunflower has no unused background, and fix integers
`e0,u0 >= 0`.  The number of non-planted listed codewords satisfying

```text
d <= ell+e0
```

and having two touched petals with at most `u0` missed points in each of those
petals is at most

```text
binom(M,2)
  * (sum_{u=0}^{u0} binom(ell,u))^2
  * q^{2(e0+u0+1)}.
```

Indeed, choose the lexicographically first pair of touched petals whose
deficits are at most `u0`.  The codeword is determined by the certificate

```text
({i,j}, S_i, S_j, A_i, A_j).
```

The chosen subsets have the form `S_i subset T_i`, `S_j subset T_j`, each
missing at most `u0` points.  Since

```text
d-a_i <= e0+u0,        d-a_j <= e0+u0,
```

there are at most `q^{e0+u0+1}` choices for each cofactor.  The syzygy then
determines `L_D`; if this is a valid missed-core locator, it determines `D`,
then `W_P`, and finally `P`.  Certificates that do not recover a valid locator
or listed codeword are simply discarded.  Thus the certificate map is
injective and the displayed bound follows.

At the L1 lower cutoff, where `M=O(log n)` and `ell<=n`, this near-saturated
partial-petal family is polynomial for fixed `e0,u0` in the generated-field
window `q=poly(n)`.

### Consequences

The bounded-excess full-petal count is the special case `u0=0`.  Lemma 11
also covers partial-petal extras that are small perturbations of that full
petal situation.  Any remaining partial-petal super-polynomial obstruction
must therefore either have growing defect excess, or avoid having two
near-saturated petals.

## Proposition 12. Background-Free Residual Normal Form

Status: PROVED.

Assume the sunflower has no unused background, and work at the L1 lower cutoff
with generated field `q=poly(n)`.  Fix constants `e0,u0 >= 0`.  The following
classes of non-planted listed codewords are polynomially bounded:

1. codewords touching exactly two petals;
2. full-petal codewords with `d-ell <= e0`;
3. codewords with `d <= ell+e0` and two touched petals each missing at most
   `u0` points.

More explicitly, their union is bounded by the sum of

```text
binom(M,2) q,
binom(M,2) sum_{e=0}^{e0} q^{2(e+1)},
binom(M,2) (sum_{u=0}^{u0} binom(ell,u))^2 q^{2(e0+u0+1)}.
```

Since `M=O(log n)` and `ell<=n` at the lower cutoff, this is polynomial in
`n` for fixed `e0,u0`.

Consequently, any background-free sunflower family that gives a
super-polynomial primitive contribution must have, for every fixed `e0,u0`,
super-polynomially many extras outside this union.  Such residual extras
satisfy:

```text
t >= 3;
if all touched petals are full, then d-ell > e0;
if d <= ell+e0, no two touched petals both have deficit <= u0.
```

Equivalently, after the proved polynomial layers are removed, the remaining
obstruction must either have genuinely growing core-defect excess, or it must
spread its partial-petal deficits so that no bounded-deficit pair exists.

### Proof

The first class is bounded by Lemma 6.  The second is bounded by Lemma 10.  The
third is bounded by the counted near-saturated corollary of Lemma 11.  Taking
the union bound gives the displayed expression.

At the lower cutoff, the planted floor satisfies `M=O(log n)`.  Since `u0` and
`e0` are fixed, the binomial sum in `ell` is polynomial in `n`, and all powers
of `q` appearing above are fixed powers.  Thus the union is polynomially
bounded in the generated-field window.

The residual assertions are exactly the negation of membership in these three
polynomially bounded classes.

### Consequences

This proposition is the current stopping point of the sunflower proof program.
The first scan obstruction has been reduced to a residual normal form.  A
future proof of the mixed-petal amplification lemma can now focus on two
genuinely hard cases:

1. growing-excess full-petal CRT kernels;
2. diffuse partial-petal patterns with no bounded-deficit petal pair.

Conversely, a counterexample search should target those two residual regimes,
not the already-controlled two-petal, minimal-defect, bounded-excess, or
near-saturated layers.

## Lemma 13. Full-Petal High Rank Below Top Defect

Status: PROVED.

Keep the background-free full-petal notation of Lemma 8.  Suppose `t=|I|>=3`
and

```text
ell <= d < (t-1)ell.
```

Then

```text
dim K_{I,d} <= d-ell+1,
```

or equivalently

```text
r_{I,d} >= ell.
```

Consequently, for fixed `I` and `d`, the number of full-petal listed codewords
with exact touched-petal set `I` and core defect `d` is at most

```text
q^{d-ell+1}.
```

### Proof

Fix one petal index `i in I`.  If `F in K_{I,d}`, Lemma 8 gives a polynomial
`W` of degree at most `d` such that

```text
W = c_j F        mod L_{T_j}        for all j in I.
```

Write

```text
W - c_iF = L_{T_i}A_i,
```

where `deg A_i <= d-ell`.  We claim that the map

```text
F |-> A_i
```

is injective on `K_{I,d}`.  If `A_i=0`, then `W=c_iF`.  For every
`j in I\{i}`,

```text
(c_i-c_j)F = W-c_jF
```

is divisible by `L_{T_j}`.  The petal scalars are distinct, so `F` is divisible
by each `L_{T_j}` for `j != i`.  These locators are pairwise coprime, hence
`F` is divisible by

```text
prod_{j in I, j != i} L_{T_j},
```

which has degree `(t-1)ell`.  Since `deg F <= d < (t-1)ell`, this forces
`F=0`.  The injection follows, so

```text
dim K_{I,d} <= dim F_q[X]_{<= d-ell} = d-ell+1.
```

Since `dim V_d=d+1`, this is equivalent to `r_{I,d}>=ell`.  The counting
bound follows from Lemma 8.

### Consequences

Before the top-defect boundary `d=(t-1)ell`, the full-petal residual regime is
not caused by a low-rank CRT map: the top-coefficient map always has rank at
least `ell`.  A remaining super-polynomial family below that boundary must
come from many split core locators inside a kernel of dimension `d-ell+1`,
with `d-ell` growing.  The exact top-defect boundary remains a separate
case.

## Lemma 14. Full-Petal Top-Defect Rank

Status: PROVED.

Keep the background-free full-petal notation of Lemma 8.  Suppose `t=|I|>=3`
and

```text
d = (t-1)ell.
```

Then the CRT top-coefficient map has full target rank:

```text
r_{I,d} = ell-1.
```

Consequently, for fixed `I`, the number of full-petal listed codewords with
exact touched-petal set `I` and top core defect `d=(t-1)ell` is at most

```text
q^{d-ell+2}.
```

### Proof

Fix one petal index `i in I`.  As in Lemma 13, every `F in K_{I,d}` determines
a polynomial `W` of degree at most `d` and a cofactor `A_i` with

```text
W-c_iF = L_{T_i}A_i,
deg A_i <= d-ell.
```

Consider the linear map `F |-> A_i` on `K_{I,d}`.  If `A_i=0`, then
`W=c_iF`.  For every `j in I\{i}`, the congruence defining `W` gives

```text
(c_i-c_j)F = W-c_jF
```

divisible by `L_{T_j}`.  Since the petal scalars are distinct and the petal
locators are pairwise coprime, `F` is divisible by

```text
B_i = prod_{j in I, j != i} L_{T_j}.
```

Now `deg B_i=(t-1)ell=d`, while `deg F<=d`, so the kernel of `F |-> A_i` is
at most the one-dimensional span of `B_i`.  Therefore

```text
dim K_{I,d} <= dim F_q[X]_{<= d-ell} + 1 = d-ell+2.
```

Since `dim V_d=d+1`, this gives

```text
r_{I,d} >= ell-1.
```

But the target of `pi_{>d}` has dimension

```text
t*ell-d-1 = ell-1,
```

so equality holds.  The counting bound follows from Lemma 8.

### Consequences

The exact top-defect boundary is also not a low-rank CRT phenomenon: the
top-coefficient map is surjective.  Thus the full-petal residual obstruction
has been reduced uniformly to split-locator concentration inside explicit CRT
kernels.  Below the top boundary the kernel has dimension at most `d-ell+1`;
at the boundary it has dimension at most `d-ell+2`.

## Lemma 15. Uniform Full-Petal Cofactor Injection

Status: PROVED.

Keep the background-free full-petal notation of Lemma 8.  Fix `I` with
`t=|I|>=3`, fix `i in I`, and suppose

```text
ell <= d <= (t-1)ell.
```

The map sending a full-petal listed codeword with exact touched-petal set `I`
and core defect `d` to its cofactor

```text
A_i = (W_P-c_iL_D)/L_{T_i}
```

is injective.  Consequently, for every fixed `I` and `d`, the number of such
full-petal listed codewords is at most

```text
q^{d-ell+1}.
```

### Proof

For a full-petal listed codeword, Lemma 7 gives the missed-core locator
`F=L_D` and a polynomial `W` of degree at most `d` such that

```text
W-c_jF
```

is divisible by `L_{T_j}` for every `j in I`.  Thus the displayed cofactor
`A_i` has degree at most `d-ell`.

Suppose two full-petal listed codewords give the same cofactor `A_i`.  Write
their data as `(F,W)` and `(F',W')`.  Equality of the cofactors gives

```text
W-W' = c_i(F-F').
```

For every `j in I\{i}`, subtracting the two divisibility relations modulo
`L_{T_j}` gives

```text
(c_i-c_j)(F-F') = W-W'-c_j(F-F')
```

divisible by `L_{T_j}`.  Since the petal scalars are distinct and the petal
locators are pairwise coprime, `F-F'` is divisible by

```text
B_i = prod_{j in I, j != i} L_{T_j}.
```

If `d<(t-1)ell`, then `deg(F-F')<deg B_i`, so `F=F'`.  If
`d=(t-1)ell`, then `F` and `F'` are both monic of degree `d`; hence
`deg(F-F')<d=deg B_i` unless `F=F'`.  Thus `F=F'` in all cases.  Lemma 7 then
recovers the listed codeword from `F`, so the cofactor map is injective.

There are at most `q^{d-ell+1}` choices for a polynomial `A_i` of degree at
most `d-ell`, proving the count.

### Consequences

The top-defect boundary no longer carries the extra linear-kernel factor from
Lemma 14 once one restricts to actual monic missed-core locators.  For fixed
`I` and `d`, every full-petal layer with `t>=3` satisfies the same cofactor
bound

```text
q^{d-ell+1}.
```

The remaining full-petal task is therefore not a rank or boundary artifact:
it is to bound how often split monic degree-`d` locators can land in the
cofactor image as `d-ell` grows.

## Lemma 16. Cofactor-Budgeted Full-Petal Layers

Status: PROVED.

Assume the sunflower has no unused background.  Fix an integer `E>=0`.  The
number of non-planted listed codewords whose touched petals are all full and
whose core defect satisfies

```text
ell <= d <= ell+E
```

is at most

```text
binom(M,2)q + 2^M sum_{e=1}^{E} q^{e+1}.
```

For `E=0`, the sum is empty.  In particular, at the L1 lower cutoff, where
`M=O(log n)` and `q=poly(n)`, every fixed-`E` full-petal layer is polynomially
bounded.  More generally, the same conclusion holds for any varying `E=E(n)`
such that

```text
2^M q^{E+1} <= n^{O(1)}.
```

### Proof

The layer `d=ell` is bounded by Lemma 9, giving the first term
`binom(M,2)q`.

Now put `d=ell+e` with `1<=e<=E`.  A full-petal listed codeword touching
exactly two petals would have `d=ell` by Lemma 7, so every such codeword has
an exact touched-petal set `I` with `|I|>=3`.  For each fixed `I`, Lemma 15
gives at most

```text
q^{d-ell+1} = q^{e+1}
```

listed codewords.  There are at most `2^M` choices of `I`, so summing over
`e=1,...,E` gives the displayed bound.

The polynomiality assertions follow directly from the displayed estimate and
the lower-cutoff bound `M=O(log n)`.

### Consequences

Lemma 10 already showed that fixed-excess full-petal layers are polynomially
bounded.  The cofactor-injection argument refines the dependence on the
excess: the full-petal residual cannot appear until the excess leaves the
explicit budget

```text
2^M q^{E+1} <= n^{O(1)}.
```

Thus a future counterexample or proof target in the full-petal regime should
look for genuinely growing cofactor excess, not merely the top-defect boundary
or bounded-excess CRT rank loss.

## Lemma 17. Mixed-Petal Cofactor Injection

Status: PROVED.

Assume the sunflower has no unused background.  Let `P` be a non-planted
listed codeword, with touched-petal set `I`, partial-petal agreements

```text
S_i = A_P(U) cap T_i,        a_i = |S_i| > 0        for i in I,
```

and core defect `d=|D|`.  Fix the support pattern `(I,(S_i)_{i in I})` and
fix one index `i in I`.  Among all listed codewords with this fixed support
pattern and this fixed defect `d`, the map

```text
P |-> A_i = (W_P-c_iL_D)/L_{S_i}
```

is injective.  Consequently the number of such codewords is at most

```text
q^{d-a_i+1}.
```

In particular, choosing an index with `a_i=max_{j in I} a_j` gives the fixed
support-pattern bound

```text
q^{d-a_*+1},        a_* = max_{j in I} |S_j|.
```

### Proof

Lemma 2 gives

```text
W_P-c_jL_D
```

vanishing on `S_j` for every `j in I`, and also gives `a_j<=d` for
non-planted codewords.  Hence each cofactor `A_j` exists and has
`deg A_j<=d-a_j`.

Suppose two listed codewords with the same support pattern and defect give the
same cofactor `A_i`.  Write their data as `(F,W)` and `(F',W')`, where
`F=L_D` and `F'=L_{D'}` are monic of degree `d`.  Equality of cofactors gives

```text
W-W' = c_i(F-F').
```

For every `j in I\{i}`, subtracting the two vanishing relations on `S_j`
gives

```text
(c_i-c_j)(F-F') = W-W'-c_j(F-F')
```

vanishing on `S_j`.  Since the petal scalars are distinct and the sets `S_j`
are disjoint, `F-F'` is divisible by

```text
B_i = prod_{j in I, j != i} L_{S_j}.
```

Let `h=sum_{j in I} a_j`.  Because the sunflower has no unused background, the
list condition gives

```text
h >= ell+d.
```

Since `a_i<=ell`, this implies

```text
deg B_i = h-a_i >= d.
```

If `h-a_i>d`, then `deg(F-F')<=d<deg B_i`, so `F=F'`.  If `h-a_i=d`, then
both `F` and `F'` are monic of degree `d`, so either `F=F'` or
`deg(F-F')<d=deg B_i`; again `F=F'`.  The locator `F=L_D` determines `D`,
and then the fixed support pattern determines the CRT residue `W_P` of degree
at most `d`, hence determines `P=L_{C\D}W_P`.  Thus the cofactor map is
injective.

There are at most `q^{d-a_i+1}` possible cofactors of degree at most `d-a_i`,
which proves the bound.

### Consequences

The cofactor-injection mechanism is not special to full petals.  Once a
partial-petal support pattern is fixed, the only remaining freedom is a
cofactor of degree controlled by

```text
d - max_i |S_i|.
```

Thus the diffuse partial-petal residual must pay either many support patterns
or growing cofactor dimension.

## Lemma 18. Bounded-Deficit Mixed-Petal Layers

Status: PROVED.

Assume the sunflower has no unused background.  For a listed codeword with
touched-petal set `I`, define its total petal deficit by

```text
u(P) = sum_{i in I} (ell-|S_i|).
```

Fix integers `E,U>=0`.  The number of non-planted listed codewords satisfying

```text
d <= ell+E,        u(P) <= U
```

is at most

```text
(E+U+1) 2^M (sum_{u=0}^{U} binom(Mell,u)) q^{E+U+1}.
```

At the L1 lower cutoff, where `M=O(log n)`, `ell<=n`, and `q=poly(n)`, this
is polynomial in `n` for fixed `E` and `U`.

### Proof

Fix the support pattern `(I,(S_i)_{i in I})` and the defect `d`.  Put
`u=sum_{i in I}(ell-|S_i|)` and choose `i` so that `a_i=|S_i|` is maximal.
Then

```text
a_i >= ell-u >= ell-U.
```

Lemma 17 therefore gives at most

```text
q^{d-a_i+1} <= q^{E+U+1}
```

listed codewords with this fixed support pattern and defect.  Also
`a_i<=d`, so `d>=ell-U`.  Since `d<=ell+E`, there are at most `E+U+1`
possible defect values.

It remains to count support patterns with total petal deficit at most `U`.
There are at most `2^M` choices for the touched-petal set `I`.  Once `I` is
chosen, a support pattern with total deficit `u` is obtained by choosing `u`
missing petal points among the at most `Mell` petal points, so the number of
patterns with total deficit at most `U` is bounded by

```text
2^M sum_{u=0}^{U} binom(Mell,u).
```

Multiplying these three bounds proves the displayed estimate.  The
polynomiality statement follows from `M=O(log n)` and `q=poly(n)` for fixed
`E,U`.

### Consequences

The diffuse partial-petal residual is now sharper.  After this lemma, a
super-polynomial background-free sunflower family at the L1 lower cutoff must
have either growing cofactor excess

```text
d-ell -> infinity
```

or growing total petal deficit

```text
u(P) -> infinity.
```

It is not enough for the family merely to avoid two near-saturated petals; it
must spread an unbounded number of missing petal points or move to genuinely
large cofactor dimension.

## Lemma 19. Deficit-Average Mixed-Petal Strata

Status: PROVED.

Assume the sunflower has no unused background.  Fix integers

```text
E>=0,        t>=2,        u>=0.
```

The number of non-planted listed codewords satisfying

```text
d <= ell+E,
#{i : S_i nonempty} = t,
sum_i (ell-|S_i|) = u
```

is at most

```text
binom(M,t) binom(t*ell,u)
  (E+floor(u/t)+1) q^{E+floor(u/t)+1}.
```

Here `binom(M,t)=0` if `t>M`, and `binom(t*ell,u)=0` if `u>t*ell`.

### Proof

Fix the touched-petal set `I` with `|I|=t`, and fix a support pattern
`(S_i)_{i in I}` with total deficit `u`.  Some touched petal has deficit at
most `floor(u/t)`, so, for

```text
a_* = max_{i in I} |S_i|,
```

one has

```text
a_* >= ell-floor(u/t).
```

For any fixed defect `d`, Lemma 17 gives at most

```text
q^{d-a_*+1} <= q^{E+floor(u/t)+1}
```

listed codewords with this fixed support pattern.  Since Lemma 2 gives
`a_*<=d` and by hypothesis `d<=ell+E`, the number of possible defect values
for this support pattern is at most

```text
E+floor(u/t)+1.
```

There are `binom(M,t)` choices for `I`.  For fixed `I`, a support pattern with
total deficit `u` is determined by choosing the `u` missing points from the
`t*ell` points in the touched petals; this gives at most `binom(t*ell,u)`
patterns.  Multiplying these estimates proves the bound.

### Consequences

The cofactor dimension is controlled by the average missing-petal density, not
just by the total number of missing petal points.  In a residual family with
many touched petals, diffuse deficits are dangerous only through the
combinatorial number of deficit placements; the polynomial cofactor part
remains controlled when `d-ell` and `u/t` are controlled.  This separates the
next problem into two clearer subproblems:

1. growing cofactor excess `d-ell`;
2. entropy of many petal-deficit placements.

## Proposition 20. Bounded-Width Mixed-Petal Layers

Status: PROVED.

Assume the sunflower has no unused background, and work at the L1 lower cutoff
with generated field `q=poly(n)`.  Fix integer constants

```text
E,T,A >= 0.
```

The number of non-planted listed codewords satisfying

```text
d <= ell+E,
t(P) = #{i : S_i nonempty} <= T,
u(P) = sum_i (ell-|S_i|) <= A t(P)
```

is polynomial in `n`.  More explicitly, it is at most

```text
sum_{t=2}^{T} sum_{u=0}^{At}
  binom(M,t) binom(t*ell,u)
  (E+floor(u/t)+1) q^{E+floor(u/t)+1}.
```

### Proof

In the background-free case, Lemma 4 rules out non-planted zero- or one-petal
extras, so `t(P)>=2`.  For each fixed pair `(t,u)` in the displayed ranges,
Lemma 19 bounds the corresponding stratum by

```text
binom(M,t) binom(t*ell,u)
  (E+floor(u/t)+1) q^{E+floor(u/t)+1}.
```

Summing over `2<=t<=T` and `0<=u<=At` gives the displayed estimate.

At the L1 lower cutoff, `M=O(log n)`, `ell<=n`, and `q=poly(n)`.  Since
`E,T,A` are fixed, the number of summands is fixed, the binomial factors are
polynomial in `n`, and the power of `q` is bounded by the fixed exponent
`E+A+1`.  Hence the displayed sum is polynomial in `n`.

### Consequences

The partial-petal residual has now been narrowed from "diffuse" to a genuinely
large-width or large-average-deficit phenomenon.  A super-polynomial
background-free sunflower family with bounded cofactor excess must satisfy at
least one of

```text
t(P) -> infinity,
u(P)/t(P) -> infinity.
```

Thus the next obstruction search should no longer spend effort on bounded
numbers of mildly deficient petals; those are polynomially controlled by the
cofactor-injection mechanism.

## Theorem 21. Background-Free Bounded-Parameter Sunflower Closure

Status: PROVED.

Assume the sunflower has no unused background, and work at the L1 lower cutoff
with generated field `q=poly(n)`.  Fix integer constants

```text
E,T,A >= 0.
```

Then the following union of non-planted listed codewords is polynomially
bounded in `n`:

1. full-petal codewords with `d<=ell+E`;
2. partial-petal codewords with

```text
d <= ell+E,
t(P) <= T,
u(P) <= A t(P).
```

More explicitly, the union is bounded by

```text
binom(M,2)q + 2^M sum_{e=1}^{E} q^{e+1}
  + sum_{t=2}^{T} sum_{u=0}^{At}
      binom(M,t) binom(t*ell,u)
      (E+floor(u/t)+1) q^{E+floor(u/t)+1}.
```

Consequently, any super-polynomial background-free sunflower family at the L1
lower cutoff must have at least one of the following unbounded parameters:

```text
d-ell,
t(P)        for partial-petal codewords,
u(P)/t(P)  for partial-petal codewords.
```

### Proof

The full-petal part is bounded by Lemma 16.  The partial-petal part is bounded
by Proposition 20.  Taking the union bound gives the displayed estimate.

At the L1 lower cutoff, `M=O(log n)`, `ell<=n`, and `q=poly(n)`.  For fixed
`E,T,A`, every term in the displayed estimate is polynomial in `n`, so the
union is polynomially bounded.

For the final assertion, suppose a background-free sunflower family is
super-polynomial while all three displayed parameters are bounded along the
family.  Choose constants `E,T,A` bounding them.  Full-petal members lie in
the first controlled class, and partial-petal members lie in the second.  The
theorem would then give a polynomial bound, a contradiction.

### Consequences

The first sunflower obstruction is now localized to a smaller, more structural
region.  Bounded-excess full-petal layers and bounded-width partial-petal
layers are no longer viable sources of super-polynomial primitive list mass.
The remaining proof or counterexample target is one of:

1. genuinely growing cofactor excess;
2. partial-petal patterns touching an unbounded number of petals;
3. partial-petal patterns with unbounded average deficit per touched petal.

The next theorem removes the second alternative when the average deficit is
bounded.

## Theorem 22. Average-Deficit Sunflower Closure

Status: PROVED.

Assume the sunflower has no unused background, and work at the L1 lower cutoff
with generated field `q=poly(n)`.  Fix integer constants

```text
E,A >= 0.
```

Then the following union of non-planted listed codewords is polynomially
bounded in `n`:

1. full-petal codewords with `d<=ell+E`;
2. partial-petal codewords with

```text
d <= ell+E,
u(P) <= A t(P).
```

More explicitly, the union is bounded by

```text
binom(M,2)q + 2^M sum_{e=1}^{E} q^{e+1}
  + binom(M,2) (sum_{v=0}^{2A} binom(ell,v))^2 q^{2(E+2A+1)}.
```

Consequently, any super-polynomial background-free sunflower family at the L1
lower cutoff must have either

```text
d-ell -> infinity,
```

or, along its partial-petal members,

```text
u(P)/t(P) -> infinity.
```

### Proof

The full-petal part is bounded by Lemma 16.

Now consider a partial-petal codeword with touched-petal count `t=t(P)` and
total petal deficit `u(P)<=At`.  In the background-free case, Lemma 4 rules
out one-petal non-planted extras, so `t>=2`.  If fewer than two touched petals
had deficit at most `2A`, then at least `t-1` touched petals would have
deficit at least `2A+1`, giving

```text
u(P) >= (t-1)(2A+1) > At
```

for every `t>=2`, a contradiction.  Thus the codeword has two touched petals
each missing at most `2A` points.

The counted near-saturated corollary of Lemma 11, with `e0=E` and `u0=2A`,
therefore bounds all such partial-petal codewords by

```text
binom(M,2) (sum_{v=0}^{2A} binom(ell,v))^2 q^{2(E+2A+1)}.
```

Adding the full-petal bound gives the displayed estimate.  At the L1 lower
cutoff, `M=O(log n)`, `ell<=n`, and `q=poly(n)`, so this estimate is
polynomial in `n` for fixed `E,A`.

For the final assertion, if both `d-ell` and the partial-petal average deficit
were bounded along a super-polynomial family, some fixed `E,A` would contain
the family in the displayed polynomially bounded union, a contradiction.

### Consequences

This removes the bounded-width escape route from Theorem 21.  The sunflower
obstruction has been reduced to two genuinely quantitative regimes:

1. growing cofactor excess `d-ell`;
2. partial-petal codewords whose average missing-petal deficit grows without
   bound.

## Corollary 23. Defect-Deficit Sandwich

Status: PROVED.

Assume the sunflower has no unused background.  For any non-planted listed
codeword, let

```text
t = #{i : S_i nonempty},
h = sum_i |S_i|,
u = sum_i (ell-|S_i|).
```

Then

```text
t(ell-d) <= u <= (t-1)ell-d.
```

Consequently,

```text
u/t >= ell-d.
```

In particular, bounded average petal deficit forces `d>=ell-O(1)`.

### Proof

The identity `u=t*ell-h` is immediate from the definition of total petal
deficit.  Lemma 2 gives the per-petal cap `|S_i|<=d`, so

```text
h <= td.
```

Substituting into `u=t*ell-h` gives the lower bound

```text
u >= t(ell-d).
```

The list condition in the background-free case gives

```text
h >= ell+d.
```

Substitution gives the upper bound

```text
u <= t*ell-(ell+d) = (t-1)ell-d.
```

Dividing the lower bound by `t` proves `u/t>=ell-d`.

### Consequences

The average-deficit residual in Theorem 22 also contains all cases where the
core defect falls far below the petal size.  Thus the sunflower proof program
has a two-sided interpretation: bounded average deficit pins `d` to a bounded
window below `ell`, while Theorem 22 controls bounded excess above `ell`.

## Lemma B1. Background-Aware Near-Saturated Pair Count

Status: PROVED.

Return to the general sunflower notation of Lemma 2; the unused background
`R` may be nonempty.  Fix integers `e0,u0 >= 0`.  The number of non-planted
listed codewords satisfying

```text
d <= ell+e0
```

and having two touched petals `T_i,T_j` with

```text
|T_i \ S_i| <= u0,        |T_j \ S_j| <= u0
```

is at most

```text
binom(M,2) (sum_{v=0}^{u0} binom(ell,v))^2 q^{2(e0+u0+1)}.
```

This is the counted near-saturated corollary of Lemma 11 without the
background-free hypothesis.

### Proof

For each codeword, choose the lexicographically first unordered pair of
touched petals satisfying the displayed deficit bound.  Let

```text
a_i=|S_i|,        a_j=|S_j|.
```

By Lemma 11 there are polynomials `A_i,A_j` such that

```text
(c_j-c_i)L_D = L_{S_i}A_i - L_{S_j}A_j,
```

and

```text
deg A_i <= d-a_i,        deg A_j <= d-a_j.
```

Since `d<=ell+e0` and `a_i,a_j >= ell-u0`, both cofactors have degree at most
`e0+u0`.

The chosen certificate

```text
({i,j}, S_i, S_j, A_i, A_j)
```

determines `L_D` by the syzygy, hence determines `D` if the right-hand side is
a valid missed-core locator.  It then determines

```text
W_P = c_iL_D + L_{S_i}A_i
```

and finally `P=L_{C\D}W_P`.  Certificates that do not recover a valid listed
codeword are discarded, so this map from codewords to certificates is
injective.

There are `binom(M,2)` choices for the petal pair, at most
`sum_{v=0}^{u0} binom(ell,v)` choices for each near-saturated petal support,
and at most `q^{e0+u0+1}` choices for each cofactor.  Multiplying gives the
claimed bound.

### Consequences

Unused background agreements do not affect the two-petal syzygy certificate.
Thus any sunflower family with bounded cofactor excess and two
near-saturated touched petals is already polynomially controlled, even before
the unused background is stripped away.

## Theorem B2. Maximal Average-Deficit Closure With Background

Status: PROVED.

Assume the sunflower is maximal, so its unused background has size
`b=|R|<ell`, and work at the L1 lower cutoff with generated field
`q=poly(n)`.  For a non-planted listed codeword put

```text
t(P)=#{i : S_i nonempty},
u(P)=sum_i (ell-|S_i|),
```

where the sum is over touched petals.  Fix integer constants `E,A >= 0`.
Then the number of non-planted listed codewords satisfying

```text
d <= ell+E
```

and

```text
u(P) <= A t(P),
```

is polynomial in `n`.

Consequently, any super-polynomial maximal-sunflower family at the L1 lower
cutoff with bounded cofactor excess `d-ell` must have

```text
u(P)/t(P) -> infinity.
```

### Proof

By Lemma 4, maximal sunflowers have no non-planted listed codewords with fewer
than two touched petals.  Thus `t=t(P)>=2`.

If `u(P)<=At`, then at least two touched petals have deficit at most `2A`;
otherwise at least `t-1` touched petals would have deficit at least `2A+1`,
giving

```text
u(P) >= (t-1)(2A+1) > At
```

for every `t>=2`, a contradiction.  Therefore every codeword in the displayed
class has two near-saturated touched petals with `u0=2A`.  Lemma B1, with
`e0=E` and `u0=2A`, bounds these codewords by

```text
binom(M,2) (sum_{v=0}^{2A} binom(ell,v))^2 q^{2(E+2A+1)}.
```

At the L1 lower cutoff, `M=O(log n)`, `ell<=n`, and `q=poly(n)`, so this is
polynomial in `n` for fixed `E,A`.

For the final assertion, if a super-polynomial family had bounded
`d-ell` and bounded `u(P)/t(P)`, fixed constants `E,A` would contain it in
the polynomially bounded union just proved.

### Consequences

This theorem removes the artificial background-free hypothesis from the
average-deficit sunflower closure.  Unused-background agreements do not create
a separate residual regime once the sunflower is maximal: with bounded
cofactor excess, bounded average petal deficit is already polynomially
controlled.  The remaining maximal-sunflower obstruction is therefore the same
two-parameter quantitative problem as in the background-free model:

```text
d-ell -> infinity        or        u(P)/t(P) -> infinity.
```

## Lemma B3. Maximal Background-Anchor Injection

Status: PROVED.

Assume the sunflower is maximal, so `b=|R|<ell`.  Fix the following data:

```text
d,
R_0 subset R,
I subset {1,...,M},
S_i subset T_i        for i in I,
```

where every `S_i` is nonempty.  Write

```text
r = |R_0|,        a_i=|S_i|,        h=sum_{i in I} a_i,
a_* = max_{i in I} a_i.
```

Consider non-planted listed codewords with exact background agreement
`R_P=R_0`, exact touched-petal set `I`, exact petal supports `S_i`, and core
defect `d`.  Then this fixed-support-pattern layer has size at most

```text
q^{max(0, d-max(r,a_*)+1)}.
```

Equivalently, the layer injects both into a largest-petal cofactor space of
dimension `max(0,d-a_*+1)` and into the background quotient space

```text
{ V : deg V <= d-r },        W_P = L_{R_0}V,
```

with the convention that the relevant space has size `1` when the displayed
degree bound is negative.

### Proof

Fix an index `i in I`.  As in Lemma 11, every codeword in the layer has

```text
W_P-c_jL_D = L_{S_j}A_j        for j in I,
deg A_j <= d-a_j.
```

We first show that the map `P |-> A_i` is injective on the fixed layer.  If
two codewords give the same `A_i`, write their data as `(F,W)` and `(F',W')`,
where `F=L_D` and `F'=L_{D'}` are monic of degree `d`.  Equality of `A_i`
gives

```text
W-W' = c_i(F-F').
```

For every `j in I\{i}`, subtracting the two petal congruences shows that
`F-F'` vanishes on `S_j`.  On the fixed background support `R_0`, both `W`
and `W'` vanish, so the displayed identity also gives that `F-F'` vanishes on
`R_0`.  Hence `F-F'` is divisible by

```text
L_{R_0} prod_{j in I, j != i} L_{S_j},
```

whose degree is `r+h-a_i`.  The list condition gives

```text
r+h >= ell+d.
```

Since `a_i<=ell`, we have `r+h-a_i>=d`.  If this degree is larger than `d`,
then `F-F'=0`.  If it equals `d`, the monicity of `F` and `F'` gives
`deg(F-F')<d` unless `F=F'`, so again `F=F'`.  The displayed identity then
gives `W=W'`, and hence `P=L_{C\D}W` is the same listed codeword.  Thus the
petal cofactor map is injective, giving the bound `q^{max(0,d-a_i+1)}`;
choosing `i` with `a_i=a_*` gives the first exponent.

For the background injection, write `W=L_{R_0}V`, with `V=0` if `d<r`.  If
two codewords have the same `V`, then they have the same `W`.  Subtracting
the petal congruences for every `j in I` shows that `F-F'` vanishes on
`union_{j in I} S_j`, whose size is `h`.  Because the sunflower is maximal,
`r<ell`, and the list condition gives

```text
h >= ell+d-r > d.
```

Therefore `F=F'`; since `W` is also the same, the two listed codewords are
equal.  The quotient space has size `q^{max(0,d-r+1)}`, proving the second
injection and the displayed bound.

### Consequences

Background agreement is not just harmless; in fixed support-pattern strata it
is an additional rank source.  The remaining residual should therefore be
measured by the support entropy left after charging the cofactor dimension

```text
max(0, d-max(r,a_*)+1).
```

This gives a concrete finite-dimensional certificate for any future
counterexample: it must exhibit enough choices of background and petal support
patterns to beat this joint petal/background-anchor exponent.

## Proposition B4. Maximal Deficit-Background Stratum Ledger

Status: PROVED.

Assume the sunflower is maximal and work at the L1 lower cutoff.  Fix
integers

```text
E>=0,        t>=2,        u>=0,        r>=0.
```

The number of non-planted listed codewords satisfying

```text
d <= ell+E,
|R_P| = r,
#{i : S_i nonempty} = t,
sum_i (ell-|S_i|) = u
```

is at most

```text
binom(b,r) binom(M,t) binom(t*ell,u) (ell+E+1) q^gamma,
```

where

```text
gamma = min(E+floor(u/t)+1, max(0,E+ell-r+1)).
```

Here `binom(b,r)=0` if `r>b`, and `binom(M,t)=0` if `t>M`.

### Proof

Choose the background support `R_0`, the touched-petal set `I`, and the
missing petal points inside the `t` touched petals.  This gives at most

```text
binom(b,r) binom(M,t) binom(t*ell,u)
```

support patterns.

For a fixed support pattern, let `a_*` be the largest petal support size.
Since the total petal deficit is `u`, some touched petal has deficit at most
`floor(u/t)`, so

```text
a_* >= ell-floor(u/t).
```

For every defect `d<=ell+E`, Lemma B3 gives the fixed-pattern bound

```text
q^{max(0,d-max(r,a_*)+1)}
  <= q^{min(E+floor(u/t)+1, max(0,E+ell-r+1))}.
```

There are at most `ell+E+1` possible values of `d`.  Multiplying the support
pattern count, the defect count, and the fixed-pattern bound proves the
ledger.

### Consequences

Proposition B4 is the current quantitative form of the maximal-sunflower
residual.  The already-proved bounded-average theorem is the case where
`floor(u/t)` is bounded and the near-saturated pair certificate avoids paying
the full support entropy.  Outside that case, any counterexample must beat the
explicit ledger above: a large number of petal/background support patterns has
to overcome the joint exponent supplied by the largest petal support and the
background quotient.

The experimental scanner
`experimental/scripts/scan_l1_full_list_quotient_conjecture.py` now reports
the parameters

```text
(d, r, t, u, a_*, d-ell, max(0,d-max(r,a_*)+1))
```

for sampled sunflower extras.  These diagnostics are only experimental, but
they make the B3/B4 residual falsifiable in the same vocabulary as the proof
ledger.

## Lemma B5. Two-Anchor Deficit Certificate

Status: PROVED.

Return to the general sunflower notation of Lemma 2; the unused background may
be nonempty.  Fix integers `E,V >= 0`.  The number of non-planted listed
codewords satisfying

```text
d <= ell+E
```

and having two touched petals whose combined deficit is at most `V` is at most

```text
binom(M,2) (sum_{v=0}^{V} binom(2ell,v)) q^{2E+V+2}.
```

More explicitly, if the two touched petals are `T_i,T_j` and

```text
v_i = ell-|S_i|,        v_j = ell-|S_j|,
```

then the certificate uses only the pair `{i,j}`, the two support subsets
`S_i,S_j`, and the two cofactors in the syzygy

```text
(c_j-c_i)L_D = L_{S_i}A_i - L_{S_j}A_j.
```

### Proof

For each codeword in the displayed class, choose the lexicographically first
unordered pair of touched petals with `v_i+v_j <= V`.  By Lemma 11 there are
polynomials `A_i,A_j` such that

```text
deg A_i <= d-|S_i|,        deg A_j <= d-|S_j|,
```

and

```text
(c_j-c_i)L_D = L_{S_i}A_i - L_{S_j}A_j.
```

Since `d<=ell+E`, these degree bounds give

```text
deg A_i <= E+v_i,        deg A_j <= E+v_j.
```

For a fixed petal pair and fixed supports `S_i,S_j`, the two cofactors
determine `L_D` by the syzygy.  If the right-hand side is not a scalar multiple
of a valid missed-core locator, the certificate is discarded.  Otherwise it
determines `D`, then

```text
W_P = c_iL_D + L_{S_i}A_i,
```

and finally `P=L_{C\D}W_P`.  Thus the certificate map is injective.

For a fixed unordered petal pair, the number of choices for the two support
subsets with total deficit `v` is at most `binom(2ell,v)`.  For such a pair of
supports, the cofactors contribute at most

```text
q^{E+v_i+1} q^{E+v_j+1} = q^{2E+v+2}
```

choices.  Summing over `0<=v<=V` and bounding every cofactor term by
`q^{2E+V+2}` gives the displayed estimate.

### Average-Deficit Corollary

Assume now that the sunflower is maximal, so `b<ell`, and work at the L1 lower
cutoff with generated field `q=poly(n)`.  Fix integer constants `E,A >= 0`.  The
number of non-planted listed codewords satisfying

```text
d <= ell+E,        u(P) <= A t(P)
```

is at most

```text
binom(M,2) (sum_{v=0}^{2A} binom(2ell,v)) q^{2E+2A+2}.
```

Indeed, Lemma 4 gives `t(P)>=2` in a maximal sunflower.  Among the `t(P)`
touched petals, the two smallest petal deficits have sum at most
`2u(P)/t(P) <= 2A`.  Lemma B5 with `V=2A` gives the bound.  Since
`M=O(log n)`, `ell<=n`, and `q=poly(n)`, this is polynomial in `n` for fixed
`E,A`.

### Consequences

Lemma B5 sharpens Theorem B2: bounded average deficit is controlled by one
two-petal certificate with total pair deficit at most `2A`, rather than by two
separately `2A`-near-saturated petals.  The residual target is therefore more
focused.  A maximal-sunflower counterexample with bounded cofactor excess must
force the best two-petal combined deficit to grow, unless it escapes through
growing `d-ell`.  This is stronger than the earlier average-deficit residual:
if the best two-petal deficit grows, then `u(P)/t(P)->infinity`, but not
conversely.

The scanner now reports this diagnostic as

```text
best_two_petal_deficit,
two_anchor_exponent = 2(d-ell)+best_two_petal_deficit+2,
```

for sampled sunflower extras with at least two touched petals.

## Lemma B6. Background-Petal Anchor Certificate

Status: PROVED.

Assume the sunflower is maximal, so its unused background has size
`b=|R|<ell`.  Fix integers `E,V >= 0`.  The number of non-planted listed
codewords satisfying

```text
d <= ell+E
```

and having a touched petal `T_i` for which

```text
(ell-|R_P|) + (ell-|S_i|) <= V
```

is at most

```text
M (sum_{w+v<=V} binom(b,ell-w) binom(ell,v)) q^{2E+V+2},
```

with the convention that `binom(b,ell-w)=0` unless `0<=ell-w<=b`.

### Proof

For each codeword in the displayed class, choose the smallest touched-petal
index `i` satisfying the displayed inequality.  Put

```text
R_0=R_P,        r=|R_0|,        w=ell-r,
S_i=A_P(U) cap T_i,        v=ell-|S_i|.
```

Since `W_P` vanishes on `R_0`, there is a polynomial `B` such that

```text
W_P = L_{R_0}B,        deg B <= d-r.
```

Here `B=0` if `d<r`.  By Lemma 2, the chosen petal support satisfies
`|S_i|<=d`, and there is a polynomial `A_i` satisfying

```text
W_P-c_iL_D = L_{S_i}A_i,        deg A_i <= d-|S_i|.
```

The bounds `d<=ell+E`, `r=ell-w`, and `|S_i|=ell-v` give

```text
deg B <= E+w,        deg A_i <= E+v.
```

The certificate

```text
(i, R_0, S_i, B, A_i)
```

determines the missed-core locator by

```text
c_iL_D = L_{R_0}B - L_{S_i}A_i.
```

If the right-hand side does not recover a valid monic locator `L_D` with roots
inside `C`, the certificate is discarded.  Otherwise it determines `D`, then
`W_P=L_{R_0}B`, and finally `P=L_{C\D}W_P`.  Hence the certificate map is
injective.

For fixed `w,v`, there are at most `M` choices of `i`,
`binom(b,ell-w)` choices of `R_0`, and `binom(ell,v)` choices of `S_i`.  The
two cofactors contribute at most

```text
q^{E+w+1} q^{E+v+1} = q^{2E+w+v+2} <= q^{2E+V+2}.
```

Summing over `w+v<=V` proves the estimate.

### Consequences

For fixed `E,V`, this is polynomial at the L1 lower cutoff: `M=O(log n)`,
`b<ell<=n`, and the sum over `w+v<=V` is polynomial because `V` is fixed.
Indeed, when `binom(b,ell-w)` is nonzero, its complementary lower index is
`b-(ell-w) <= w <= V`.
Thus bounded cofactor excess and bounded background-petal combined deficit
cannot produce a super-polynomial maximal-sunflower family.

Together, Lemma B5 and Lemma B6 leave a sharper maximal-sunflower residual.
With bounded `d-ell`, a counterexample must force both diagnostics to grow:

```text
best_two_petal_deficit -> infinity,
best_background_petal_deficit -> infinity.
```

The scanner reports the second diagnostic as

```text
best_background_petal_deficit
  = (ell-background_hits) + (ell-max_petal_hit),
background_petal_exponent
  = 2(d-ell)+best_background_petal_deficit+2.
```

## Theorem B7. Maximal Two-Gate Residual Closure

Status: PROVED.

Assume the sunflower is maximal and work at the L1 lower cutoff with generated
field `q=poly(n)`.  For a non-planted listed codeword, let

```text
v_i = ell-|S_i|
```

on touched petals, and let `v_(1)<=v_(2)` be the two smallest touched-petal
deficits.  Lemma 4 gives at least two touched petals, so these are defined.
Put

```text
G_2(P) = v_(1)+v_(2),
G_R(P) = (ell-|R_P|)+v_(1).
```

Fix integer constants `E,V_2,V_R >= 0`.  The number of non-planted listed
codewords satisfying

```text
d <= ell+E
```

and

```text
G_2(P) <= V_2        or        G_R(P) <= V_R
```

is polynomial in `n`.  More explicitly, it is at most

```text
binom(M,2) (sum_{v=0}^{V_2} binom(2ell,v)) q^{2E+V_2+2}
  + M (sum_{w+v<=V_R} binom(b,ell-w) binom(ell,v)) q^{2E+V_R+2}.
```

Consequently, any super-polynomial maximal-sunflower family at the L1 lower
cutoff with bounded cofactor excess `d-ell` must satisfy

```text
G_2(P) -> infinity        and        G_R(P) -> infinity.
```

### Proof

The first summand is exactly Lemma B5 applied with `V=V_2`.  The second
summand is Lemma B6 applied with `V=V_R`.  Their union contains every codeword
in the displayed class, and both summands are polynomial at the L1 lower
cutoff for fixed `E,V_2,V_R`.

For the final assertion, if a super-polynomial family had bounded `d-ell` and
one of `G_2,G_R` bounded along an infinite subfamily, fixed constants
`E,V_2,V_R` would put that subfamily inside the polynomially bounded union
above, a contradiction.

### Consequences

The current maximal-sunflower residual is now a three-parameter escape:

```text
d-ell,
G_2(P),
G_R(P).
```

Every bounded region in this parameter space is polynomially controlled.  The
remaining mixed-petal amplification problem is therefore not just "diffuse
petals"; it must simultaneously have growing cofactor dimension, or it must
evade both low-dimensional anchor certificates.  The scanner records this
combined gate as

```text
best_anchor_exponent = min(two_anchor_exponent, background_petal_exponent).
```

## Lemma B8. Largest-Petal Width Floor

Status: PROVED.

Assume the sunflower is maximal.  Let `P` be a non-planted listed codeword, and
write the positive petal support sizes in decreasing order

```text
a_1 >= a_2 >= ... >= a_t > 0,
```

where `t=t(P)` is the touched-petal count.  Put `r=|R_P|` and
`d=|C\C_P|`.  Then

```text
t >= ceil((ell+d-r)/a_1).
```

If `t>=2`, then also

```text
t >= 1 + ceil(max(0, ell+d-r-a_1)/a_2).
```

Equivalently, in the two-gate notation of Theorem B7, where
`v_(1)=ell-a_1` and `G_R=(ell-r)+v_(1)`,

```text
t >= 1 + ceil(max(0, d-ell+G_R)/a_2).
```

### Proof

The list condition gives

```text
h = sum_i |S_i| >= ell+d-r.
```

Since every touched petal has size at most `a_1`,

```text
h <= t a_1,
```

which proves the first lower bound.

For the second, separate the largest touched petal.  The remaining `t-1`
touched petals have size at most `a_2`, so

```text
h <= a_1 + (t-1)a_2.
```

Combining this with `h>=ell+d-r` gives the displayed floor.  Finally,

```text
ell+d-r-a_1 = d-ell + ((ell-r)+(ell-a_1)) = d-ell+G_R,
```

which is the equivalent two-gate form.

### Consequences

The two-gate residual cannot stay narrow unless the second-largest petal
support is large relative to the positive part of `d-ell+G_R(P)`.  In
particular, in any near-`ell` defect window `|d-ell|=O(1)`, a family with
`G_R(P)->infinity` and bounded touched-petal count must have `a_2` growing on
the same scale as `G_R(P)`.

The scanner reports both floors as

```text
width_floor_a1,
width_floor_a2.
```

## Corollary B9. Finite-Width Two-Gate Tradeoff

Status: PROVED.

Keep the maximal-sunflower hypotheses and notation of Lemma B8 and Theorem B7.
Then every non-planted listed codeword satisfies

```text
2 max(0,d-ell+G_R(P)) + (t(P)-1)G_2(P) <= 2(t(P)-1)ell.
```

Consequently, for any fixed width bound `T>=2`, every codeword with
`t(P)<=T` satisfies

```text
2 max(0,d-ell+G_R(P)) + (t(P)-1)G_2(P) <= 2(T-1)ell.
```

### Proof

Let `v_(1)<=v_(2)` be the two smallest touched-petal deficits, and put
`a_2=ell-v_(2)`.  Lemma B8 gives

```text
max(0,d-ell+G_R(P)) <= (t(P)-1)a_2.
```

Since

```text
G_2(P)=v_(1)+v_(2) <= 2v_(2),
```

we have

```text
a_2 = ell-v_(2) <= ell-G_2(P)/2.
```

Combining the two displays gives

```text
max(0,d-ell+G_R(P)) <= (t(P)-1)(ell-G_2(P)/2),
```

which is the first displayed inequality after multiplying by `2`.  The
`t(P)<=T` version follows immediately.

### Consequences

This is the finite-width obstruction left by the two gates.  In a bounded
cofactor-excess window, a bounded-width residual cannot make both `G_2` and
`G_R` independently large relative to `ell`; increasing `G_2` consumes the
second-largest petal support available to pay for `G_R`.

The scanner reports the exact nonnegative slack in this inequality as

```text
width_gate_slack
  = 2(t-1)ell
    - ((t-1)best_two_petal_deficit
       + 2 max(0,d-ell+best_background_petal_deficit)).
```

## Corollary B10. Johnson Over-Agreement Gate

Status: PROVED.

Return to the full-list setting of Theorem J.  Let

```text
lambda_J = min { lambda >= 0 : (s+lambda)^2 > n(k-1) }.
```

For any received word `U`, the number of listed codewords with agreement slack
at least `lambda_J`,

```text
|A_P(U)| - s >= lambda_J,
```

is at most

```text
n(n-k+1) / ((s+lambda_J)^2 - n(k-1)).
```

If `2(s+lambda_J)>n+k-1`, this tail has size at most `1`.

In the sunflower notation, the agreement slack is

```text
lambda(P) = |A_P(U)|-s = |R_P| + sum_i |S_i| - (ell+d).
```

Thus every super-polynomial sunflower obstruction outside the ordinary Johnson
region may be assumed to satisfy

```text
lambda(P) < lambda_J.
```

### Proof

The codewords with `|A_P(U)|-s >= lambda_J` are exactly

```text
ImgFib_U(s+lambda_J).
```

The definition of `lambda_J` puts this threshold in the Johnson region, so
Theorem J gives the displayed bound.  The uniqueness assertion is the
unique-decoding part of the same theorem.

For the sunflower identity, Lemma 2 gives

```text
|A_P(U)| = (k-1-d) + |R_P| + sum_i |S_i|,
```

while `s=k+ell-1`; subtracting gives the formula for `lambda(P)`.

### Consequences

The maximal-sunflower residual now has an additional global gate.  The
two-gate and finite-width analysis is only needed for low-overagreement
extras:

```text
lambda(P) < lambda_J.
```

High-overagreement sunflower extras are not a separate obstruction; they are
charged directly to the proved full-list Johnson profile.  The scanner reports
`johnson_slack_needed` and whether each sampled extra is already
`johnson_covered`.

## Theorem B11. Maximal Sunflower Residual Frontier

Status: PROVED.

Assume the sunflower is maximal and work at the L1 lower cutoff with generated
field `q=poly(n)`.  Use the notation of Theorem B7 and Corollary B10.  Fix
integer constants

```text
E,V_2,V_R >= 0.
```

Then the number of non-planted listed codewords satisfying

```text
d <= ell+E
```

and at least one of the three gate conditions

```text
lambda(P) >= lambda_J,
G_2(P) <= V_2,
G_R(P) <= V_R
```

is polynomial in `n`.  More explicitly, it is bounded by

```text
n(n-k+1) / ((s+lambda_J)^2 - n(k-1))
  + binom(M,2) (sum_{v=0}^{V_2} binom(2ell,v)) q^{2E+V_2+2}
  + M (sum_{w+v<=V_R} binom(b,ell-w) binom(ell,v)) q^{2E+V_R+2}.
```

If `2(s+lambda_J)>n+k-1`, the first summand may be replaced by `1`.

Consequently, any super-polynomial maximal-sunflower family at the L1 lower
cutoff must, after passing to an infinite subfamily, satisfy at least one of
the following:

```text
d-ell -> infinity,
```

or

```text
d <= ell+E for some fixed E,        lambda(P) < lambda_J,
G_2(P) -> infinity,        G_R(P) -> infinity.
```

If the second alternative also has bounded touched-petal count, then the
finite-width tradeoff of Corollary B9 is an additional necessary condition:

```text
2 max(0,d-ell+G_R(P)) + (t(P)-1)G_2(P) <= 2(t(P)-1)ell.
```

### Proof

The codewords with `lambda(P)>=lambda_J` are bounded by Corollary B10.  The
codewords with `G_2(P)<=V_2` or `G_R(P)<=V_R`, under `d<=ell+E`, are bounded
by Theorem B7.  Taking the union bound gives the displayed estimate.  Each
summand is polynomial at the lower cutoff for fixed `E,V_2,V_R` and
`q=poly(n)`.

For the residual assertion, suppose a super-polynomial maximal-sunflower
family had bounded cofactor excess, i.e. `d<=ell+E` for some fixed `E`.  If either
`lambda(P)>=lambda_J` occurs on a super-polynomial subfamily, or `G_2` or
`G_R` is bounded on such a subfamily, the polynomial bound above gives a
contradiction.  Hence any bounded-cofactor-excess residual subfamily must lie
below the Johnson gate and must have both gates unbounded.  The finite-width
inequality is exactly Corollary B9.

### Consequences

This theorem is the current maximal-sunflower stopping point for the L1 proof
program.  With bounded cofactor excess, the remaining high-value sunflower
target is no longer the broad mixed-petal family; it is the residual frontier

```text
lambda(P) < lambda_J,        G_2(P)->infinity,        G_R(P)->infinity,
```

or else genuinely growing positive cofactor excess `d-ell`.  A future proof
should attack that frontier directly, while a future counterexample search
should try to populate it.

## Development Ledger

- **Conjecture 1 full-list primitive remainder:** CONJECTURAL.  Main proof
  target for this branch.
- **Sparse-syndrome formulation:** PROVED / AUDIT.  Import from the repaired
  L1 package and scanner.
- **Quotient exact-stabilizer ledger:** PROVED / AUDIT.  Use only as a
  separation ledger, not as an upper bound.
- **High-multiplicity certificate extraction:** PROVED / AUDIT.  Check that
  extracted certificates apply to the full-list object.
- **Quotient and low-defect removal:** PROVED / CONJECTURAL.  Import proved
  defect stripping; formulate the remaining arbitrary-word quotient upper
  budget.
- **Aperiodic extension counting:** CONJECTURAL.  Main quantitative theorem
  needed for Conjecture 1.
- **Sunflower core-defect reduction:** PROVED.  Reduces each non-planted
  mixed-petal extra to a degree-`d` interpolation problem with a per-petal cap.
- **Fixed-defect sunflower layers:** PROVED.  Bounds each fixed missed-core
  layer by `O_{d0}(n^{2d0+1})`.
- **Petal-support tradeoff:** PROVED.  Shows that few-petal non-planted extras
  require large missed-core defect.
- **Background-free two-petal pencil:** PROVED.  Classifies exact two-petal
  extras by a one-parameter locator pencil.
- **Background-free two-petal count:** PROVED.  Bounds the exact two-petal
  family by `binom(M,2)q`.
- **Full-petal CRT compression:** PROVED.  Reduces full-petal multi-petal
  extras to top-coefficient vanishing in a CRT residue.
- **Full-petal rank certificate:** PROVED.  Bounds full-petal extras by the
  kernel dimension of the CRT top-coefficient map.
- **Minimal-defect full-petal count:** PROVED.  Bounds all full-petal extras
  with `d=ell` by `binom(M,2)q`.
- **Bounded-excess full-petal count:** PROVED.  Bounds all full-petal extras
  with `d-ell<=e0` by `O_{e0}(q^{2e0+2}log(n)^2)`.
- **Two-petal syzygy compression:** PROVED.  Reduces partial-petal extras with
  two near-saturated petals to polynomially many syzygy certificates.
- **Background-free residual normal form:** PROVED.  Leaves only
  growing-excess full-petal CRT kernels and diffuse partial-petal patterns.
- **Full-petal high rank below top defect:** PROVED.  Shows the CRT map has
  rank at least `ell` for `t>=3` and `d<(t-1)ell`.
- **Full-petal top-defect rank:** PROVED.  Shows the CRT map is full-rank on
  its top-coefficient target at `d=(t-1)ell`.
- **Uniform full-petal cofactor injection:** PROVED.  Gives the fixed-`I,d`
  bound `q^{d-ell+1}` throughout `ell<=d<=(t-1)ell`.
- **Cofactor-budgeted full-petal layers:** PROVED.  Bounds full-petal layers
  with `d-ell<=E` by `binom(M,2)q + 2^M sum_{e=1}^E q^{e+1}`.
- **Mixed-petal cofactor injection:** PROVED.  For fixed partial-petal support
  pattern, extras inject into a cofactor space of dimension `d-a_*+1`.
- **Bounded-deficit mixed-petal layers:** PROVED.  Bounds all extras with
  `d<=ell+E` and total petal deficit at most `U`.
- **Deficit-average mixed-petal strata:** PROVED.  Bounds fixed `(t,u)` strata
  with cofactor exponent depending on `floor(u/t)`.
- **Bounded-width mixed-petal layers:** PROVED.  Shows bounded excess, bounded
  touched-petal count, and bounded average deficit give only polynomial mass.
- **Background-free bounded-parameter sunflower closure:** PROVED.  Combines
  full-petal and mixed-petal bounds into a single residual theorem.
- **Average-deficit sunflower closure:** PROVED.  Removes bounded-width as a
  residual escape route; bounded excess and bounded average deficit are
  polynomially controlled.
- **Defect-deficit sandwich:** PROVED.  Shows bounded average petal deficit
  forces the core defect to stay within a bounded window below `ell`.
- **Background-aware near-saturated pair count:** PROVED.  Removes the
  background-free hypothesis from the two-near-saturated-petal certificate
  count.
- **Maximal average-deficit closure with background:** PROVED.  Removes the
  background-free hypothesis from the bounded-excess, bounded-average-deficit
  sunflower closure; unused-background agreement is not a separate residual
  escape in maximal sunflowers.
- **Maximal background-anchor injection:** PROVED.  Adds a second fixed-pattern
  injection through the background quotient `W_P/L_{R_P}` and bounds strata by
  `q^max(0,d-max(r,a_*)+1)`.
- **Maximal deficit-background stratum ledger:** PROVED.  Gives an explicit
  `(t,u,r)` ledger balancing petal/background support entropy against the
  joint cofactor exponent.
- **Two-anchor deficit certificate:** PROVED.  Counts maximal-sunflower
  extras with bounded cofactor excess and bounded best two-petal deficit,
  sharpening the average-deficit closure and adding a targeted scanner
  diagnostic.
- **Background-petal anchor certificate:** PROVED.  Counts maximal-sunflower
  extras with bounded cofactor excess and bounded background-petal combined
  deficit, using the background quotient and one petal cofactor without fixing
  all petal supports.
- **Maximal two-gate residual closure:** PROVED.  Combines the two-petal and
  background-petal anchor certificates: bounded cofactor excess is polynomial
  unless both anchor deficits escape every fixed bound.
- **Largest-petal width floor:** PROVED.  Shows the current two-gate residual
  must either spread across many petals or keep the top two petal supports
  large enough to meet the list condition.
- **Finite-width two-gate tradeoff:** PROVED.  Shows bounded-width residuals
  must satisfy an explicit tradeoff between the two-petal and background-petal
  gates.
- **Johnson over-agreement gate:** PROVED.  Removes sunflower extras whose
  agreement slack already puts them in the ordinary Johnson region.
- **Maximal sunflower residual frontier:** PROVED.  Combines the Johnson and
  two-gate controls into the current precise residual target.
- **Mixed-petal sunflower amplification:** CONJECTURAL.  Next focused bound to
  prove or refute in the large-defect regime.
