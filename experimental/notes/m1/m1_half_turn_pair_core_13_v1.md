# M1: half-turn pair-core coefficient-window compression v1

Status: PROVED-LOCAL / CONDITIONAL-LEDGER / EXPERIMENTAL-EVIDENCE.

This note proves two narrow M1 row-slice branch statements over honest
`2`-power cyclotomic domains.  The `{1,3}` classification and `{1,4}`
residual-core equation are proved over the honest characteristic-zero model.
Finite-field deployed use requires a separate generated-collision ledger.  The
v3 experiment evidence recorded below is external evidence and is not replayed
by this verifier.

For the `{1,3}` coefficient-window, every survivor is a half-turn pair core
plus at most one residual point.  Thus the support family can be large, but its
finite-slope image is small: one slope when `j` is even, and at most `n` slopes
when `j` is odd.

For the `{1,4}` coefficient-window, paired cores do not multiply slopes.  The
branch is exactly residualized to one core-feasibility equation in the squared
domain, then decomposed into the pair-small, recursive lower-domain, and
half-turn-balance ledgers.  After the latter two ledgers are charged, the
primitive residual image is bounded by `n+1`.

This is not full M1 closure.  Finite-field amplification, arbitrary
nonconsecutive windows, sparse Hankel row-slices, and arbitrary row-slice
inverse theorems remain outside this packet.

## Relation to the v13 M1 wall

The v13 M1 wall is the uniform compression problem for growing split-locator
determinant terms:

```text
CAP25-V13-M1-UNIFORM-SPLIT-LOCATOR-DETERMINANT-COMPRESSION.
```

This packet does not prove the uniform compression theorem.  It localizes a
specific coefficient-shadow subbranch of that wall.  In the half-turn
coefficient windows treated here, the large paired-core support families are
not primitive determinant mass:

- the `{1,3}` branch is slope-small over the honest cyclotomic model;
- the `{1,3}` finite-field failures are exactly generated-collision reductions
  of the residual defect `F_3(R)=e_1(R)e_2(R)-e_3(R)`;
- the `{1,4}` branch is reduced to pair-small slopes, a recursive lower-domain
  coefficient shadow, and a half-turn-balance zero-sum ledger.

Thus the result is a branch-level localization of the M1 wall: it replaces an
unstructured growing support count by named paid ledgers plus a small primitive
remainder in this half-turn window.

## `{1,3}` Statement

Let

```text
D = mu_{2^m} subset Q(zeta_{2^m}),    n = |D| = 2^m,    m >= 2.
```

Let `T subset D` have size `j`, with `3 <= j <= n`, and write its monic
locator as

```text
ell_T(X) = prod_{x in T}(X-x)
         = X^j + c_{j-1}X^{j-1} + ... + c_0.
```

Assume `T` satisfies the `{1,3}` coefficient-window equations: there is a
finite slope `z` such that

```text
c_{j-1} + z c_j = 0,
c_{j-3} + z c_{j-2} = 0.
```

Then the half-turn residual of `T` has size at most `1`.

Equivalently:

- If `j` is even, then `T` is a union of `j/2` antipodal pairs and `z=0`.
  The support count is `binom(n/2,j/2)`, and the slope image has size at most
  `1`.
- If `j` is odd, then `T` is a union of `(j-1)/2` antipodal pairs plus one
  singleton `y`, and `z=y`.  The support count is
  `n*binom(n/2-1,(j-1)/2)`, and the slope image has size at most `n`.

Conversely, every support of these forms satisfies the `{1,3}` equations with
the stated slope.

## Proof

Let the half-turn involution be `x -> -x`.  Every `T subset mu_{2^m}`
decomposes uniquely as

```text
T = C disjoint_union R,
```

where `C` is the union of all complete antipodal pairs contained in `T`, and
`R` contains at most one point from each antipodal pair.

Write

```text
C = {+-a_1, ..., +-a_q},       R = {y_1, ..., y_s},
```

so `j=2q+s`.  The paired-core polynomial is even:

```text
B_C(X) = prod_i (X-a_i)(X+a_i) = prod_i (X^2-a_i^2),
```

and the residual polynomial is

```text
Q_R(X) = prod_{y in R}(X-y).
```

Thus

```text
ell_T(X) = B_C(X) Q_R(X).
```

### The first row

Let `e_r(S)` be the elementary symmetric polynomial of a finite set `S`.  Since

```text
c_{j-1} = -e_1(T),       c_j = 1,
```

the offset-1 row gives

```text
z = e_1(T).
```

The paired core has zero first elementary sum, so

```text
e_1(T) = e_1(R),
```

and therefore

```text
z = e_1(R).
```

The paired core cannot change the slope.

### The third row

Write

```text
B_C(X) = sum_{i=0}^q b_i X^{2q-2i},       b_0 = 1,
Q_R(X) = sum_{u=0}^s d_u X^{s-u},         d_u = (-1)^u e_u(R).
```

Since `ell_T=B_CQ_R`, the coefficient at offset `r` from the top is

```text
c_{j-r} = sum_{i>=0} b_i d_{r-2i},
```

where `d_v=0` outside `0 <= v <= s`.

The offset-3 row is

```text
c_{j-3} + z c_{j-2} = 0.
```

Substituting the convolution formula gives

```text
(d_3 + b_1 d_1) + z(d_2 + b_1 d_0) = 0,
```

or

```text
(d_3 + z d_2) + b_1(d_1 + z d_0) = 0.
```

But `d_1=-e_1(R)`, `d_0=1`, and `z=e_1(R)`, so

```text
d_1 + z d_0 = 0.
```

The paired-core term cancels, and the offset-3 equation reduces to the
residual-only equation

```text
d_3 + z d_2 = 0.
```

Equivalently,

```text
e_1(R)e_2(R) - e_3(R) = 0.
```

### Residual rigidity

Let

```text
p_r(R) = sum_{y in R} y^r.
```

Newton's identity gives

```text
p_3(R) = e_1(R)^3 - 3e_1(R)e_2(R) + 3e_3(R).
```

Thus `e_1(R)e_2(R)-e_3(R)=0` is equivalent to

```text
p_3(R) = p_1(R)^3.
```

Cubing is a Galois automorphism of `Q(zeta_{2^m})`, because `gcd(3,2^m)=1`.
Let `sigma_3(zeta)=zeta^3`.  Then

```text
p_3(R) = sigma_3(p_1(R)).
```

So

```text
sigma_3(p_1(R)) = p_1(R)^3.
```

If `L` is the order of `3` modulo `2^m`, iteration gives

```text
p_1(R) = p_1(R)^{3^L}.
```

Hence `p_1(R)=0`, or `p_1(R)` is a root of unity.  The roots of unity in
`Q(zeta_{2^m})` are the `2^m`-th roots of unity, so

```text
p_1(R) in {0} union mu_{2^m}.
```

Now use the half-turn balance lemma:

```text
If sum_{x in mu_{2^m}} a_x x = 0 with a_x >= 0 integers, then a_x=a_{-x}
for every x.
```

Indeed, with `n=2^m` and `N=n/2`, write

```text
A(X)=sum_{i=0}^{n-1} a_i X^i.
```

The relation `A(zeta)=0` implies `Phi_{2^m}(X)=X^N+1` divides `A(X)`.  Since
`deg A < n=2N`, we have `A(X)=(X^N+1)B(X)` with `deg B<N`, so the coefficients
in positions `i` and `i+N` are equal.  These positions represent `x` and `-x`.

If `p_1(R)=0`, half-turn balance forces `R` itself to be balanced under
`x -> -x`.  Since `R` contains at most one point from each antipodal orbit,
this gives `R=empty`.

If `p_1(R)=eta in mu_{2^m}`, then

```text
sum_{y in R} y + (-eta) = 0.
```

By half-turn balance, the multiset `R union {-eta}` is balanced.  Since `R`
has at most one point from each antipodal orbit, this is possible only when
`R={eta}`.

Therefore `|R| <= 1`.

### Counts and converse

Since `j=2q+|R|`, parity gives the two cases.

If `j` is even, `R=empty`, so `T` is a union of `j/2` antipodal pairs and
`z=0`.  There are `binom(n/2,j/2)` supports and at most one slope.

If `j` is odd, `R={y}`.  There are `n` choices for `y`, and then
`n/2-1` antipodal pairs remain available for the paired core.  Thus the support
count is

```text
n*binom(n/2-1,(j-1)/2),
```

and the slope image is contained in `D`, hence has size at most `n`.

Conversely, a union of antipodal pairs has an even locator, so
`c_{j-1}=c_{j-3}=0` and `z=0` satisfies both rows.  A union of antipodal pairs
plus one singleton `y` has `ell_T=B_C(X)(X-y)` with `B_C` even.  The first row
gives `z=y`, and the third row reduces to the singleton residual equation
`e_1({y})e_2({y})-e_3({y})=0`, which is true.

This proves the theorem.

## `{1,3}` finite-field transfer lemma

The proof above also gives the exact finite-field transfer obstruction.

Keep the same half-turn decomposition

```text
T = C disjoint_union R,
```

and define the residual defect

```text
F_3(R) := e_1(R)e_2(R) - e_3(R).
```

The coefficient calculation used only polynomial identities with integer
coefficients.  Therefore it remains valid after reducing the `2`-power
cyclotomic model modulo any prime for which the chosen roots are defined.  In
any such finite-field reduction, a `{1,3}` survivor satisfies

```text
z = e_1(R),       F_3(R) = 0
```

in the finite field.

Over the honest characteristic-zero field `Q(zeta_{2^m})`, the rigidity theorem
just proved says

```text
F_3(R)=0  =>  |R|<=1.
```

Consequently, if a finite-field `{1,3}` survivor has `|R|>1`, then the
cyclotomic integer `F_3(R)` is nonzero in `Q(zeta_{2^m})` but reduces to zero
in the finite field.  Such a survivor is precisely a generated-field collision
for the residual defect `F_3(R)`.  Thus the characteristic-zero branch theorem
does not transfer automatically to deployed finite fields, but every failed
transfer is localized to the named generated-collision ledger.

## `{1,4}` Residualization Statement

Let

```text
D = mu_{2^m} subset Q(zeta_{2^m}),    n = |D| = 2^m,    N = n/2,
```

with `m>=2`.  Let `T subset D` have size `j>=4`, and write

```text
ell_T(X) = prod_{x in T}(X-x)
         = X^j + c_{j-1}X^{j-1} + ... + c_0.
```

Assume `T` satisfies the `{1,4}` coefficient-window equations: there is a
finite slope `z` such that

```text
c_{j-1} + z c_j = 0,
c_{j-4} + z c_{j-3} = 0.
```

Decompose `T` under the half-turn involution:

```text
T = C disjoint_union R,
```

where `C` is a union of complete antipodal pairs and `R` contains at most one
point from each antipodal pair.  Write

```text
C = {+-a_1, ..., +-a_q},
U = {a_1^2, ..., a_q^2} subset mu_{2^{m-1}},
R = {y_1, ..., y_s},
j = 2q+s.
```

Then

```text
z = e_1(R).
```

Moreover, the `{1,4}` equations are equivalent to the single residual-core
equation

```text
e_2(U) - alpha_R e_1(U) + beta_R = 0,
```

where

```text
alpha_R = e_2(R) - e_1(R)^2,
beta_R  = e_4(R) - e_1(R)e_3(R).
```

Equivalently, the `{1,4}` slope image at support size `j` is exactly

```text
{
  e_1(R):
  R is half-turn-free,
  s=|R| satisfies s == j mod 2 and 0 <= s <= min(j,n-j),
  and there exists U subset mu_{2^{m-1}} outside R^2 with |U|=(j-s)/2
  such that e_2(U) - alpha_R e_1(U) + beta_R = 0
}.
```

Here `R^2={y^2:y in R}`.  A fixed residual `R` may admit many paired-core
completions `U`, but all such completions have the same slope `e_1(R)`.

## `{1,4}` Proof

Write the paired core as

```text
C = {+-a_1, ..., +-a_q}.
```

Its polynomial is even:

```text
B_C(X) = prod_i (X-a_i)(X+a_i) = prod_i (X^2-a_i^2).
```

Set

```text
U = {u_1, ..., u_q} = {a_1^2, ..., a_q^2} subset mu_{2^{m-1}}.
```

Then

```text
B_C(X) = prod_{u in U}(X^2-u)
       = sum_{i=0}^q b_i X^{2q-2i},
```

with

```text
b_0 = 1,       b_1 = -e_1(U),       b_2 = e_2(U).
```

Write the residual polynomial as

```text
Q_R(X) = prod_{y in R}(X-y)
       = sum_{r=0}^s d_r X^{s-r},
```

where `d_r=(-1)^r e_r(R)` and `d_0=1`.  Since `ell_T=B_CQ_R`, the coefficient
at offset `r` from the top is

```text
c_{j-r} = sum_{i>=0} b_i d_{r-2i},
```

with `d_v=0` outside `0<=v<=s`.

The offset-1 row is the same as before:

```text
c_{j-1}+z c_j=0.
```

It gives

```text
z = e_1(T) = e_1(R),
```

because the paired core has zero first elementary sum.

The offset-4 row is

```text
c_{j-4}+z c_{j-3}=0.
```

Using the convolution formula,

```text
c_{j-4} = d_4 + b_1d_2 + b_2d_0,
c_{j-3} = d_3 + b_1d_1.
```

Therefore

```text
c_{j-4}+z c_{j-3}
  = (d_4+z d_3) + b_1(d_2+z d_1) + b_2.
```

Substituting `z=e_1(R)` gives

```text
d_2+z d_1 = e_2(R)-e_1(R)^2 = alpha_R,
d_4+z d_3 = e_4(R)-e_1(R)e_3(R) = beta_R.
```

Thus the offset-4 equation is

```text
beta_R + b_1 alpha_R + b_2 = 0.
```

Using `b_1=-e_1(U)` and `b_2=e_2(U)`, this is exactly

```text
e_2(U) - alpha_R e_1(U) + beta_R = 0.
```

Conversely, if `R` is half-turn-free, `U subset mu_{2^{m-1}}` is disjoint from
`R^2`, and this equation holds with `|U|=(j-|R|)/2`, then the support formed
from the antipodal pairs over `U` together with `R` satisfies both `{1,4}` rows
with `z=e_1(R)`.  This proves the exact residual-core classification.

## `{1,4}` Residual-Image Bound

Let `R_s` be the set of half-turn-free residuals of size `s`.  Since `D` has
`N=n/2` antipodal orbits,

```text
|R_s| = 2^s binom(N,s).
```

For a `j`-support, the residual size satisfies

```text
s == j mod 2,       0 <= s <= min(j,n-j).
```

The upper bound `s<=n-j` is equivalent to `(j-s)/2+s <= n/2`: the paired-core
orbits and residual orbits must be disjoint.

Therefore the `{1,4}` slope image satisfies

```text
|Slope_{1,4}(j)|
  <= sum_{s == j mod 2, 0 <= s <= min(j,n-j)} 2^s binom(N,s).
```

More sharply, if a branch certificate restricts the residual sizes to a set
`S`, then

```text
|Slope_{1,4}(j;S)| <= sum_{s in S} 2^s binom(N,s).
```

For fixed maximum residual size `s_0`, this is `O(n^{s_0})`.  The important
point is that no factor for the number of paired-core completions appears.  A
fixed residual may admit many core choices, but all of them have the same
slope.

### Core-feasibility forms

Let `q=(j-|R|)/2`.

If `q=0`, then `U=empty`, and feasibility is

```text
beta_R = 0,
```

or `e_4(R)=e_1(R)e_3(R)`.

If `q=1`, say `U={u}`, then feasibility is

```text
-alpha_R u + beta_R = 0.
```

If `alpha_R != 0`, the core square is forced to be

```text
u = beta_R/alpha_R,
```

and it must lie in `mu_{2^{m-1}}` outside `R^2`.  If `alpha_R=0`, feasibility
requires `beta_R=0`; in that degenerate case any allowable `u` works, but the
slope is still only `e_1(R)`.

If `q=2`, say `U={u,v}`, then feasibility is

```text
uv - alpha_R(u+v) + beta_R = 0,
```

equivalently

```text
(u-alpha_R)(v-alpha_R) = alpha_R^2 - beta_R.
```

For general `q`, the core choices lie on the coefficient line

```text
e_2(U) = alpha_R e_1(U) - beta_R
```

inside the split-locator variety on the squared domain `mu_{2^{m-1}}`.  A
large family of cores over one residual is therefore lower-domain fiber mass,
not primitive slope mass.

### `j=5` and `j=6`

For `j=5`, the possible residual sizes are `s=1,3,5`, corresponding to
`q=2,1,0`.  The classifier specializes as follows.

For `s=1`, `R={y}`, so `alpha_R=-y^2` and `beta_R=0`.  With `U={u,v}`, the
condition is

```text
uv + y^2(u+v) = 0,
```

and the slope is `z=y`.

For `s=3`, the one core square is forced to `u=beta_R/alpha_R` when
`alpha_R!=0`, and must lie in `mu_{2^{m-1}}` outside `R^2`.  The slope is
`e_1(R)`.

For `s=5`, there is no paired core, and the residual itself must satisfy
`e_4(R)=e_1(R)e_3(R)`.

For `j=6`, the possible residual sizes are `s=0,2,4,6`.  They give the same
forms with `q=3,2,1,0`.  This explains the experimental phenomenon: `{1,4}`
permits larger residuals than `{1,3}`, but the slope remains residual-only.

## `{1,4}` Lower-Domain And Higher-Pair Ledger Closure

For fixed `j`, let `S_{1,4}(j)` be the set of slopes `e_1(R)` arising from
honest cyclotomic `{1,4}` survivors under the residual-core equation above.
Define:

```text
S_le1 = {e_1(R): |R|<=1},

Paid_recursive_lower = {e_1(R): |R|>=2, q>=2, and R is feasible through
                        the lower-domain coefficient-shadow fiber in
                        mu_{2^{m-1}}},

Paid_half_turn_balance = {e_1(R): |R|>=2, q<=1, and the residual equation
                          has a half-turn-balanced zero-sum certificate}.
```

Then

```text
S_{1,4}(j)
  subset S_le1 union Paid_recursive_lower union Paid_half_turn_balance.
```

Consequently, after the recursive lower-domain shadow and higher-pair
half-turn-balanced residual ledgers are charged, the unpaid primitive remainder
satisfies

```text
|S_{1,4}^{prim}(j)| <= |S_le1| <= n+1.
```

This is a ledger decomposition theorem.  It does not prove that
`Paid_recursive_lower` or `Paid_half_turn_balance` are numerically small as
ordinary sets; it proves every such slope carries one of the two explicit
structured ledger certificates.

### Positive zero-sum form

For a residual `R`, set

```text
A_R = e_1(R)^2 - e_2(R),
B_R = e_1(R)e_3(R) - e_4(R).
```

Then `alpha_R=-A_R` and `beta_R=-B_R`.  The `{1,4}` feasibility equation

```text
e_2(U) - alpha_R e_1(U) + beta_R = 0
```

is therefore equivalent to

```text
B_R = e_2(U) + A_R e_1(U).
```

Both `A_R` and `B_R` are positive sums of roots of unity.  More explicitly,
`A_R` is the sum of the multiset

```text
Acal_R = {y^2: y in R} disjoint_union {yy': {y,y'} subset R},
```

so

```text
|Acal_R| = binom(|R|+1,2).
```

Similarly, `B_R` is the sum of the multiset `Bcal_R` containing

```text
x^2yw, xy^2w, xyw^2       for each {x,y,w} subset R,
```

and three copies of `prod_{y in J} y` for each four-subset `J subset R`.
Thus

```text
|Bcal_R| = 3*binom(|R|+1,4).
```

Let

```text
Ccal_U = {uv: {u,v} subset U}.
```

The equality `B_R=e_2(U)+A_R e_1(U)` gives the nonnegative vanishing sum

```text
sum_{xi in Z(R,U)} xi = 0,
```

where

```text
Z(R,U) = Bcal_R disjoint_union (-Ccal_U) disjoint_union (-U*Acal_R).
```

Here `-Ccal_U` means every element is multiplied by `-1`, and similarly for
`-U*Acal_R`.

By the `2`-power half-turn balance lemma used in the `{1,3}` proof, every
honest cyclotomic vanishing sum of `2^m`-th roots with nonnegative
multiplicities is balanced under `x -> -x`.  Hence every honest `{1,4}`
survivor has a half-turn-balanced certificate `Z(R,U)`.

### Case split

If `|R|<=1`, then `z=e_1(R)` gives at most `n+1` slopes: `0` from the empty
residual and at most `n` singleton slopes.

If `|R|>=2` and `q>=2`, the core variable `U` has size at least two and lies on
the lower-domain coefficient-shadow line

```text
e_2(U) + A_R e_1(U) = B_R
```

inside the split-locator variety on `mu_{2^{m-1}}`.

Equivalently, with

```text
P_U(Y) = prod_{u in U}(Y-u) = sum_{i=0}^q p_i Y^i,     p_q=1,
```

we have

```text
p_{q-1} = -e_1(U),       p_{q-2} = e_2(U),
```

and the lower-domain condition is

```text
p_{q-2} - A_R p_{q-1} - B_R p_q = 0.
```

This is an affine coefficient-shadow equation for a split locator in the
smaller domain.  The domain size strictly decreases:

```text
2^m -> 2^{m-1}.
```

Thus the recursive charge cannot cycle.  These slopes are, by definition, paid
by `Paid_recursive_lower`.

If `|R|>=2` and `q<=1`, there is no large moving lower-domain core.  When
`q=0`, feasibility is `B_R=0`, so `Bcal_R` is half-turn-balanced.  When `q=1`,
say `U={u}`, feasibility is `B_R=uA_R`, so

```text
Bcal_R disjoint_union (-u*Acal_R)
```

is half-turn-balanced.  These slopes are paid by `Paid_half_turn_balance`.

This proves the covering

```text
S_{1,4}(j)
  subset S_le1 union Paid_recursive_lower union Paid_half_turn_balance.
```

Adding quotient, common-GCD, contained, and generated-field ledgers only
enlarges the structured side.  Over the honest cyclotomic field the generated
ledger is empty; in finite fields it records reductions where a nonzero
cyclotomic integer vanishes modulo the field characteristic.

### Parity-empty subtheorem

Full emptiness of `Paid_half_turn_balance` is stronger than the ledger theorem.
The ledger theorem only requires that every such point carry an explicit
half-turn-balance certificate.  However, a useful unconditional emptiness
subtheorem follows from parity.

The unqualified statement is false outside the actual `{1,4}` branch range:
for any two-point half-turn-free residual `R={x,y}`, one has
`e_3(R)=e_4(R)=0`, hence `B_R=e_1(R)e_3(R)-e_4(R)=0`.  This does not touch the
`q=0` `{1,4}` case, because then `j=s` and the offset-4 row requires `s>=4`.
The corrected emptiness target must include the valid `q=0, s>=4` range
restriction.

For `q=0`, the half-turn-balance multiset is `Bcal_R`, whose size is

```text
|Bcal_R| = 3*binom(s+1,4).
```

A balanced multiset must have even size.  By Lucas' theorem modulo `2`,
`binom(s+1,4)` is odd exactly when the `4`-bit is present in `s+1`, i.e.

```text
s == 3,4,5,6 mod 8.
```

Thus

```text
q=0 half-turn-balance is empty for s == 3,4,5,6 mod 8.
```

For the actual `{1,4}` window with `q=0`, one also has `j=s>=4`, so the first
relevant exclusions are `s=4,5,6`.

For `q=1`, the zero-sum length is

```text
|Bcal_R| + |Acal_R| = 3*binom(s+1,4) + binom(s+1,2).
```

A direct Lucas check gives odd parity exactly when

```text
s == 1,2,3,4 mod 8.
```

Therefore

```text
q=1 half-turn-balance is empty for s == 1,2,3,4 mod 8.
```

This gives the small-residual exclusions:

```text
q=1: s=2,3,4 are empty,
q=0: s=4,5,6 are empty.
```

For the remaining residue classes,

```text
q=0: s == 0,1,2,7 mod 8,
q=1: s == 0,5,6,7 mod 8,
```

parity alone does not rule out balanced certificates.  The experiments support
full emptiness over the honest cyclotomic model, but that would require a
separate inverse lemma:

```text
No half-turn-free R can make Bcal_R or Bcal_R disjoint_union (-u*Acal_R)
antipodally balanced.
```

This PR does not claim that inverse lemma.

### Imbalance-vector form of half-turn-balance emptiness

For a positive multiset `M` of `2^m`-th roots, define its antipodal imbalance
profile by

```text
Delta_M(xi) = mult_M(xi) - mult_M(-xi).
```

The half-turn balance lemma says:

```text
sum_{xi in M} xi = 0
iff
Delta_M is identically zero.
```

Thus the missing valid-range half-turn-balance emptiness lemma is exactly:

```text
q=0, s>=4:
  Delta_{Bcal_R} is not identically zero
  for every half-turn-free R.

q=1, s>=2, u in mu_{2^{m-1}}\R^2:
  Delta_{Bcal_R disjoint_union (-u*Acal_R)}
  is not identically zero.
```

The parity-empty subtheorem proves this imbalance is nonzero in the mod-8
classes listed above.  The remaining classes are the genuine new inverse
problem:

```text
q=0: s == 0,1,2,7 mod 8,
q=1: s == 0,5,6,7 mod 8.
```

### Finite-field reduction caveat

The theorem above is over the honest cyclotomic field `Q(zeta_{2^m})`.  In a
finite field, an additional generated-field branch appears: a cyclotomic
integer that is nonzero over `Q(zeta_{2^m})` may reduce to zero modulo the
field characteristic.  Such slopes are charged to `Paid_generated`.

Thus the finite-field ledger version is

```text
S_{1,4}(j)
  subset S_le1
       union Paid_recursive_lower
       union Paid_half_turn_balance
       union Paid_generated.
```

After those ledgers are removed, the same primitive bound remains:

```text
|S_{1,4}^{prim}(j)| <= n+1.
```

### Lower-fiber rigidity caveat

The experiments suggest a corrected twofold rigidity statement after fixing
row parity and removing `|R|<=1`.  The unrestricted statement is false.

Take `m>=3` and let `zeta` be a primitive `2^m`-th root.  Let

```text
i = zeta^{2^{m-2}},       y = zeta^{2^{m-3}},
```

so `i^2=-1` and `y^2=i`.  Define

```text
R  = {y},
R' = {1,i}.
```

Both residuals are half-turn-free, but they have different sizes, so
`R'!=R` and `R'!=-R`.  For `R`,

```text
A_R = e_1(R)^2-e_2(R) = y^2 = i,
B_R = e_1(R)e_3(R)-e_4(R) = 0.
```

For `R'={1,i}`,

```text
e_1(R') = 1+i,       e_2(R') = i,
```

and since `(1+i)^2=2i`,

```text
A_R' = (1+i)^2-i = i,
B_R' = 0.
```

Thus

```text
(A_R,B_R) = (A_R',B_R') = (i,0),
```

but `R'` is neither `R` nor `-R`.  Therefore unrestricted twofold lower-fiber
rigidity is not a valid theorem.

A viable corrected target is:

```text
For fixed size, after removing |R|<=1, if |R|=|R'|>=2 and
(A_R,B_R)=(A_R',B_R'), then R'=R or R'=-R.
```

The slightly broader fixed-row-parity version is also experimentally
plausible, but the fixed-size statement is the clean first theorem.  This
sharpened target is not needed for the ledger-payment theorem; it would only
improve recursive accounting.

### Fixed-size rigidity base case: `s=2`

The fixed-size target is already provable for two-point residuals.

Let

```text
R={x,y},       R'={a,b}
```

be half-turn-free two-element residuals.  Then `B_R=B_R'=0`, so equality of
`(A_R,B_R)` is equality of

```text
A_R  = x^2 + xy + y^2,
A_R' = a^2 + ab + b^2.
```

Thus

```text
x^2 + xy + y^2 + (-a^2) + (-ab) + (-b^2) = 0.
```

This is a positive vanishing sum of `2^m`-th roots, so it is antipodally
balanced.

If `(y/x)^2 != -1`, then the three roots `x^2,xy,y^2` contain no internal
antipodal pair.  Each must therefore be balanced by one of
`-a^2,-ab,-b^2`, which gives

```text
{x^2,xy,y^2} = {a^2,ab,b^2}.
```

For `2`-power roots this three-term progression determines the unordered pair
up to simultaneous sign.  Indeed, in `{x^2,xy,y^2}` the middle term `xy` is
the unique element whose square is the product of the other two: if `x^2` were
also a middle term, then `(y/x)^3=1`, impossible in a `2`-power root group
unless `x=y`; similarly for `y^2`.  Thus `ab=xy` and
`{a^2,b^2}={x^2,y^2}`.  Taking square roots gives
`{a,b}={x,y}` or `{a,b}={-x,-y}`.  Hence `R'=R` or `R'=-R`.

If `(y/x)^2=-1`, then `x^2+y^2=0` and `A_R=xy`.  The same balance argument
forces `a^2` and `b^2` to be antipodal, otherwise the three terms
`a^2,ab,b^2` could not balance the single opposite root.  Hence
`A_R'=ab=xy`, and `(b/a)^2=-1`, which again gives `R'=R` or `R'=-R`.

So the first open fixed-size rigidity case is `s>=3`, not `s=2`.

### Imbalance-vector form of fixed-size AB-rigidity

Equality of cyclotomic sums is equality of antipodal imbalance profiles.  Hence

```text
A_R = A_R'
```

is equivalent to

```text
Delta_{Acal_R} = Delta_{Acal_R'}.
```

Similarly,

```text
B_R = B_R'
```

is equivalent to

```text
Delta_{Bcal_R} = Delta_{Bcal_R'}.
```

Therefore the first open fixed-size rigidity theorem is:

```text
For half-turn-free R,R' with |R|=|R'|>=3,
the pair of imbalance profiles

  (Delta_{Acal_R}, Delta_{Bcal_R})

determines R up to the global sign R -> -R.
```

This is the precise inverse theorem supported by the fixed-size AB-fiber
experiments.

## Experiment evidence for the next `{1,4}` targets

The separate exploratory packet `m1_14_ledger_experiments_v3` tested the two
next inverse targets with corrected q1 root-multiplication arithmetic.  These
tests are evidence, not proof.

For half-turn-balance emptiness, no `q=0` or `q=1` hits were found in:

```text
n=32, s=7..10 exhaustive;
n=64, s=4,5 exhaustive;
n=64, s=6..12 prefix-exhaustive.
```

For fixed-size AB-fiber rigidity, the same rows had maximum residuals per
`(A_R,B_R)` fiber equal to `2`, maximum slopes per fiber equal to `2`, and
every observed twofold fiber was exactly antipodal.  The exact fixed-size rows
now include `n=32, s=2..8` and `n=64, s=4,5`; larger rows were checked by
prefix-exhaustive samples.

The resulting next theorem targets are:

```text
1. Valid-range half-turn-balance emptiness:
   q=0, s>=4, B_R=0 has no honest half-turn-free solution, and
   q=1, s>=2, B_R=uA_R has no honest half-turn-free solution with
   u in mu_{2^{m-1}}\R^2.

2. Fixed-size imbalance-profile rigidity beyond the base case:
   for half-turn-free R,R' with |R|=|R'|>=3,
   (Delta_{Acal_R},Delta_{Bcal_R})
   =
   (Delta_{Acal_R'},Delta_{Bcal_R'})
   implies R'=R or R'=-R.
```

After those two are proved, the `{1,4}` branch is no longer only ledger-paid:
the half-turn-balance ledger is empty over the honest cyclotomic model, and
the recursive lower-domain ledger has only antipodal twofold residual lifts.

### Deployed budget check

For the deployed KoalaBear length `n=2^21`, the primitive `{1,4}` residual
image after charging `Paid_recursive_lower` and `Paid_half_turn_balance` is
bounded by

```text
n+1 = 2097153.
```

The sextic line budget is

```text
B* = floor(((2^31-2^24+1)^6 - 1)/2^128)
   = 274980728111395087.
```

Therefore

```text
n+1 < B*.
```

So the `{1,4}` primitive residual image is budget-safe once the named
recursive lower-domain, higher-pair, and generated-field ledgers are accepted
in the appropriate honest/finite-field setting.

## Deployed KoalaBear parity check

For the deployed KoalaBear length `n=2^21`, the honest characteristic-zero
`{1,3}` branch gives:

```text
A=1116044: j=981108 even, slope image <= 1
A=1116045: j=981107 odd,  slope image <= 2^21
A=1116046: j=981106 even, slope image <= 1
A=1116047: j=981105 odd,  slope image <= 2^21
```

Each characteristic-zero branch bound is far below the sextic line budget
`floor((q_line-1)/2^128)` for `q_line=(2^31-2^24+1)^6`.

These checks are parity and budget arithmetic for the honest branch.  They do
not certify the actual finite-field KoalaBear slope image until the `{1,3}`
generated-collision branch is bounded or ruled out.

## Finite-field transfer guardrail

The honest `{1,3}` theorem does not automatically transfer to finite fields.
For example, over `F_17` with order-16 generator `3`, take support exponents

```text
T = {0,1,3,14}.
```

The support values are `{1,3,10,2}` and the locator coefficients modulo `17`
are

```text
c0..c4 = [9,3,3,1,1].
```

With finite slope `z=-c3=16`, both `{1,3}` rows vanish:

```text
c3 + z c4 = 0 mod 17,
c1 + z c2 = 0 mod 17.
```

But the half-turn residual size is `4`, not `<=1`.  This is exactly the
generated-field collision/amplification branch that must be charged before any
finite-field KoalaBear use of the characteristic-zero theorem: the residual
defect

```text
F_3(R)=e_1(R)e_2(R)-e_3(R)
```

is nonzero in `Q(zeta_16)` but is `0 mod 17` for this support.

## Non-claims

- This does not close M1.
- This does not provide a standalone numerical cost theorem for the recursive
  lower-domain or half-turn-balance ledgers.
- This does not prove full emptiness of the half-turn-balance ledger.
- This does not prove fixed-size AB-fiber rigidity for residual sizes `s>=3`.
- This does not claim unrestricted twofold lower-fiber rigidity.
- This does not classify arbitrary nonconsecutive coefficient windows.
- This does not classify sparse Hankel row-slices.
- This does not charge finite-field generated-collision amplification.
- This does not prove the finite-field `{1,3}` generated-collision branch is
  empty or budget-small.
- This does not certify the deployed KoalaBear finite-field `{1,3}` slope
  image.
- This does not prove the deployed KoalaBear safe-side row.

## Validation

Run from the repository root:

```sh
python3 -m py_compile experimental/scripts/verify_m1_half_turn_pair_core_13_v1.py
python3 experimental/scripts/verify_m1_half_turn_pair_core_13_v1.py --check
python3 experimental/scripts/verify_m1_half_turn_pair_core_13_v1.py --json
python3 -m json.tool experimental/data/certificates/m1-half-turn-pair-core-13-v1/m1_half_turn_pair_core_13_v1.json
git diff --check
```
