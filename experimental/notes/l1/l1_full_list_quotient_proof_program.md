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
- **Mixed-petal sunflower amplification:** CONJECTURAL.  Next focused bound to
  prove or refute in the large-defect regime.
