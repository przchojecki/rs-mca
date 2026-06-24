# F1 Fixed-Rate Extension-Line Counterexample

## Claim

Let `p` be an odd prime, let `B = F_p`, and let

```text
F = B[alpha],        alpha^2 = d,
```

where `d in B` is a nonsquare. Let `H = B^*`, so `n = p-1`, and let
`C_F = RS[F,H,k]`. Put

```text
a = k + 1,        delta = 1 - a/n,
```

with `2 <= a <= n`. Define the extension-valued line over `H`

```text
f(x) = x^a / (x - alpha),
g(x) = -1 / (x - alpha),
u_z(x) = f(x) + z g(x) = (x^a - z) / (x - alpha).
```

For every `a`-subset `S subset H`, write

```text
L_S(X) = product_{s in S} (X - s),
Q_S(X) = X^a - L_S(X),
z_S = Q_S(alpha).
```

Then `z_S` is support-wise MCA-bad at radius `delta` for the line `f+zg`.
Moreover, after fixing any `(a-2)`-subset `T subset H`, the slopes

```text
z_{T union {x,y}},        {x,y} subset H \ T
```

are distinct as the unordered pair `{x,y}` varies. Consequently

```text
emca(C_F, delta)
  >= binom(p-a+1, 2) / p^2.
```

In particular, along any fixed-rate sequence

```text
k = floor(rho (p-1)),        0 < rho < 1,
```

one has `a = k+1` and

```text
emca(C_F, 1 - (k+1)/(p-1))
  >= (1-rho)^2/2 - o(1).
```

This gives a fixed-rate counterexample to the unrestricted
numerator-preserving extension-line lift: the base-field MCA numerator can be
taken trivially as `p`, while the extension-valued line over `F_{p^2}` has
constant bad-slope density, not `p^{1+o(1)}/p^2`.

More generally, the same construction works over any finite extension
`F/F_p` containing an element `alpha notin F_p`. If `|F|=p^e` with `e >= 2`,
then

```text
emca(C_F, delta)
  >= binom(p-a+1, 2) / p^e,

|F| * emca(C_F, delta)
  >= binom(p-a+1, 2).
```

Thus the extension-line numerator forced by this sigma-one family is
`Theta(p^2)` at fixed rate, independent of the extension degree. For `e=2`
this is a constant-density counterexample. For `e>2` the density is diluted by
the larger challenge field, but it is still a factor `Theta(p)` larger than
the numerator `p` supplied by a base-field MCA bound.

The construction is also local to the evaluation domain. Let `D subset F_p`
have size `n`, let `C_F=RS[F,D,k]`, and keep `a=k+1`. For any `2 <= a <= n`
and any `alpha in F\F_p`, the same line on `D` has

```text
emca(C_F, 1-a/n)
  >= binom(n-a+2, 2) / |F|
  = binom(n-k+1, 2) / |F|.
```

Thus an unrestricted same-numerator extension transfer from a base numerator
`p` already fails whenever `(n-k)^2` is asymptotically larger than `p`. The
full-subgroup case `D=F_p^*` is the fixed-rate endpoint `n=p-1`, where the
forced extension numerator is `Theta(p^2)`.

The sigma-one case is not the only fixed-slack degree-one obstruction. In the
quadratic case over `H=F_p^*`, set

```text
sigma = 2,        a = k + 2.
```

For any `a`-subset `S subset H` with

```text
e1(S) = sum_{s in S} s = 0,
```

the same degree-one denominator `E=X-alpha`, numerator `N=1`, and monic anchor
`X^a` give a support-wise bad slope. More quantitatively, there is a
`(k-1)`-subset `T subset H` such that the slopes from supports

```text
S = T union U,        |U|=3,        e1(U) = -e1(T),
```

are all distinct and their number is at least

```text
M_{p,k}
  = binom(k+2,3) / binom(p-1,k-1)
      * (binom(p-1,k+2) + (p-1)(-1)^(k+2)) / p.
```

Consequently, for every fixed-rate sequence with `k=floor(rho(p-1))` and
`0<rho<1`,

```text
emca(C_F, 1-(k+2)/(p-1))
  >= ((1-rho)^3/6 - o(1)).
```

This remains a sub-reserve counterexample: `sigma=2` gives
`eta=2/(p-1)`, far below the corrected `C/log n` reserve.

The same phenomenon persists at every fixed slack.  Fix `sigma >= 1`, put
`a=k+sigma`, and keep `F=F_{p^2}`.  Then, for every fixed-rate sequence
`k=floor(rho(p-1))` with `0<rho<1`,

```text
emca(C_F, 1-(k+sigma)/(p-1))
  >= ((1-rho)^(sigma+1)/(sigma+1)! - o(1)).
```

Thus every fixed `sigma` gives a constant-density degree-one extension-line
obstruction in the fixed-rate, sub-reserve regime.

More generally, for every fixed slack

```text
sigma >= 1,        a = k + sigma,
```

the same degree-one denominator gives a support-wise bad slope from every
`a`-subset `S` satisfying

```text
e_1(S) = e_2(S) = ... = e_{sigma-1}(S) = 0.
```

If a `(k-1)`-tail `T` is fixed, the slope map is injective on the admissible
blocks

```text
S = T union U,        |U| = sigma+1,
```

that satisfy these prefix-vanishing equations. Consequently, if
`G_{p,k,sigma}` denotes the number of such admissible `a`-subsets of
`F_p^*`, then some tail gives at least

```text
G_{p,k,sigma} * binom(k+sigma, sigma+1) / binom(p-1,k-1)
```

distinct bad slopes.  The character bound below proves that, for every fixed
`sigma`,

```text
G_{p,k,sigma} = (1+o(1)) binom(p-1,k+sigma) / p^(sigma-1)
```

along fixed-rate sequences.  Therefore this fixed-tail slice forces a
quadratic extension numerator

```text
((1-rho)^(sigma+1)/(sigma+1)! - o(1)) p^2
```

for fixed-rate `k=floor(rho(p-1))`.

The character bound is also uniform for slowly growing slack. If
`sigma=sigma(p)=o(sqrt(p)/log p)`, then the same prefix-vanishing count obeys

```text
G_{p,k,sigma}
  = (1+o(1)) binom(p-1,k+sigma) / p^(sigma-1).
```

Consequently, for fixed `0<rho<1`,

```text
|F| emca(C_F, 1-(k+sigma)/(p-1))
  >= (1+o(1)) binom(p-k,sigma+1) / p^(sigma-1).
```

In particular, for every fixed `0<epsilon<1`, throughout the window

```text
sigma <= (1-epsilon) log p / log log p,
```

the forced quadratic-extension numerator is at least

```text
p^(1+epsilon-o(1)).
```

Thus same-numerator extension transfer from the base-field numerator `p`
still fails by a polynomial factor in this slowly growing, sub-reserve slack
range.

These are numerator statements, not artifacts of choosing a quadratic
extension. More generally, if `F/F_p` has degree `e>=2` and
`alpha in F\F_p`, the same bad-slope numerator works over `F`; only the
density denominator changes from `p^2` to `p^e`.

There is also a higher-degree amplification. If `alpha` has base-field degree
at least `r`, with fixed `r>=2`, then the fixed-tail injectivity argument uses
blocks of size `sigma+r-1` instead of `sigma+1`. Consequently, for fixed
`sigma`, fixed `r`, and fixed rate,

```text
|F| emca(C_F, 1-(k+sigma)/(p-1))
  >= ((1-rho)^(sigma+r-1)/(sigma+r-1)! - o(1)) p^r.
```

In particular, taking `alpha` to generate `F_{p^e}` gives a constant-density
extension-line counterexample in every fixed extension degree `e>=2`, not only
in quadratic extensions.

## Status

PROVED / COUNTEREXAMPLE.

This starts with a sigma-one counterexample, with agreement size `k+1`, and
adds a proved degree-one fixed-rate family for every fixed slack `sigma`. The
proof combines the fixed-tail injectivity template with a character bound for
prefix-vanishing elementary symmetric support sets. The same bound is uniform
for `sigma=o(sqrt(p)/log p)`, and it still beats the base-field numerator
through `sigma <= (1-epsilon) log p/log log p`. The higher-degree
amplification gives order-`p^r` numerators for elements of base-field degree
at least `r`. These results do not refute a repaired extension-line theorem in
the corrected-reserve regime
`sigma >= C n/log n`. They do refute any unrestricted route that bounds
extension-line MCA by taking a base-field numerator and dividing by the larger
extension challenge field. The extension-degree corollary shows that the issue
is numerator preservation, not merely constant density in quadratic extensions.
The domain-local corollary shows that the obstruction is controlled by
`(n-k)^2`, not by any special multiplicative-subgroup identity. The sigma-two
slice shows that merely making the residual slack positive is not enough; it
must clear the list/entropy reserve.

## Proof

First note that `alpha notin B`, so `x - alpha` is nonzero for every
`x in H`.

Fix an `a`-subset `S subset H`. Since `L_S` is monic of degree `a`,
`Q_S = X^a - L_S` has degree at most `a-1 = k`. By definition,
`Q_S(alpha) = z_S`, so `Q_S(X)-z_S` is divisible by `X-alpha`. Put

```text
P_S(X) = (Q_S(X) - z_S) / (X - alpha).
```

Then

```text
deg P_S <= k - 1,
```

so `P_S` is a codeword polynomial for `C_F`. For `x in S`, `L_S(x)=0`, hence
`Q_S(x)=x^a`, and therefore

```text
P_S(x)
  = (x^a - z_S)/(x-alpha)
  = u_{z_S}(x).
```

Thus the line point `u_{z_S}` is code-explained on `S`.

It remains to prove same-support noncontainment. Suppose, for contradiction,
that `g|S` agrees with a degree-`<k` polynomial `G`. Then

```text
R(X) = (X-alpha)G(X) + 1
```

has degree at most `k` and vanishes on all `a=k+1` points of `S`. Hence
`R` is identically zero. But `R(alpha)=1`, a contradiction. Thus `g` is not
code-explained on `S`, so no pair of degree-`<k` codewords explains `f` and
`g` simultaneously on `S`. Therefore every `z_S` is support-wise MCA-bad.

Now fix `T subset H` with `|T| = a-2`. Let

```text
C_T = product_{t in T} (alpha - t).
```

This is nonzero. For distinct `x,y in H\T`,

```text
L_{T union {x,y}}(alpha)
  = C_T (alpha-x)(alpha-y)
  = C_T (alpha^2 - (x+y)alpha + xy).
```

If two unordered pairs `{x,y}` and `{x',y'}` outside `T` give the same slope,
then their locator values at `alpha` agree, and hence

```text
alpha^2 - (x+y)alpha + xy
  = alpha^2 - (x'+y')alpha + x'y'.
```

Rearranging gives

```text
((x+y) - (x'+y')) alpha = xy - x'y'.
```

The left side is a `B`-multiple of `alpha` and the right side lies in `B`.
Since `1, alpha` are linearly independent over `B`, both sides are zero. Thus

```text
x+y = x'+y',        xy = x'y'.
```

The unordered pair is determined by its sum and product, so
`{x,y} = {x',y'}`. This proves injectivity on the slice through `T`.

The same injectivity proof only used the `B`-linear independence of `1` and
`alpha`; it did not use that `F` is quadratic. Therefore it applies verbatim in
any finite extension `F/F_p` with `alpha notin F_p`.

The same argument is local to the domain. If `D subset B` has size `n`, choose
any `(a-2)`-subset `T subset D`; then the same pair-injectivity proof applies
to unordered pairs in `D\T`. The number of available points outside `T` is

```text
|D \ T| = n - (a-2) = n-a+2.
```

Therefore there are at least

```text
binom(n-a+2, 2)
```

distinct bad slopes in `F`, and

```text
emca(C_F, 1-a/n) >= binom(n-a+2, 2) / |F|.
```

For `D=H=F_p^*`, this becomes `binom(p-a+1,2)/|F|`. If `|F|=p^e`, this gives
the extension-degree lower bound displayed in the claim.

## Proof Of The Sigma-Two Degree-One Slice

Now take `F=F_p[alpha]` with `alpha^2=d`, `d` a nonsquare, and
`H=F_p^*`. Set `sigma=2` and `a=k+2`. For an `a`-subset `S subset H`, write

```text
L_S(X) = product_{s in S} (X-s),
Q_S(X) = X^a - L_S(X).
```

If `e1(S)=0`, then the `X^(a-1)` coefficient of `Q_S` vanishes, so
`deg Q_S <= a-2 = k`. Put `z_S=Q_S(alpha)`. Then `Q_S-z_S` is divisible by
`X-alpha`, and

```text
P_S(X) = (Q_S(X)-z_S)/(X-alpha)
```

has degree `< k`. Since `Q_S(x)=x^a` on `S`, this polynomial explains the line
point `(x^a-z_S)/(x-alpha)` on `S`. The same noncontainment argument as above
applies because `|S|=k+2>k`.

It remains to count many distinct slopes. First count zero-sum `a`-subsets of
`H`. For a nontrivial additive character `psi` of `F_p`,

```text
product_{x in F_p^*} (1 + Y psi(rx)) = 1 - Y + Y^2 - ... + Y^(p-1)
```

for every `r != 0`. Therefore the coefficient of `Y^a` is `(-1)^a`.
Fourier inversion gives the exact count

```text
N_0(a)
  = #{ S subset H : |S|=a, e1(S)=0 }
  = (binom(p-1,a) + (p-1)(-1)^a) / p.
```

Each zero-sum support `S` gives `binom(a,3)` decompositions

```text
S = T union U,        |T|=k-1,        |U|=3.
```

Averaging over the `binom(p-1,k-1)` possible tails, some tail `T` has at least
`M_{p,k}` triples `U` satisfying `e1(T)+e1(U)=0`.

Fix such a tail. Let

```text
C_T = product_{t in T} (alpha-t).
```

For a triple `U={x,y,w}` with fixed sum `c=e1(U)`, the locator value is

```text
L_{T union U}(alpha)
  = C_T (alpha-x)(alpha-y)(alpha-w)
  = C_T (alpha^3 - c alpha^2 + e2(U) alpha - e3(U)).
```

Using `alpha^2=d` and `alpha^3=d alpha`, this equals

```text
C_T ( -c d - e3(U) + (d+e2(U)) alpha ).
```

Since `C_T != 0` and `1,alpha` are linearly independent over `F_p`, the slope
records `e2(U)` and `e3(U)`. With `e1(U)=c` fixed, the elementary symmetric
triple `(e1,e2,e3)` determines the unordered triple `U`. Thus the slopes from
the chosen tail are distinct.

Finally,

```text
M_{p,k}
  = binom(p-k,3)/p - o(p^2)
  = ((1-rho)^3/6 - o(1)) p^2
```

along fixed-rate sequences. Dividing by `|F|=p^2` gives the displayed
constant-density sigma-two lower bound.

## General Fixed-Slack Degree-One Template

The previous two cases are instances of a uniform degree-one mechanism.  Fix
`sigma >= 1`, put `a=k+sigma`, and keep the line

```text
u_z(x) = (x^a-z)/(x-alpha).
```

For an `a`-subset `S`, expand

```text
L_S(X)
  = X^a - e_1(S)X^(a-1) + e_2(S)X^(a-2) - ... + (-1)^a e_a(S).
```

Then

```text
Q_S(X) = X^a - L_S(X)
```

has degree at most `k` exactly when

```text
e_1(S) = ... = e_{sigma-1}(S) = 0.
```

For every such support, the same construction

```text
z_S = Q_S(alpha),        P_S = (Q_S-z_S)/(X-alpha)
```

gives `deg P_S < k` and explains `u_{z_S}` on `S`.  The same noncontainment
argument used above applies because `|S|=k+sigma>k`.

Now fix a tail `T` of size `k-1`.  Suppose

```text
S = T union U,        S' = T union U',        |U|=|U'|=sigma+1
```

are both prefix-vanishing supports and have the same slope.  Since

```text
L_S(alpha) = L_T(alpha)L_U(alpha)
```

and `L_T(alpha) != 0`, equality of slopes gives

```text
L_U(alpha) = L_{U'}(alpha).
```

The equations `e_m(T union U)=0` for `1 <= m <= sigma-1` recursively determine
`e_m(U)` from `T` and the lower `e_i(U)`.  Hence `U` and `U'` have the same
elementary symmetric coefficients through degree `sigma-1`.  Because
`|U|=sigma+1`, the difference `L_U-L_{U'}` is therefore a polynomial of degree
at most one:

```text
L_U(X)-L_{U'}(X) = A X + B,        A,B in F_p.
```

Evaluating at `alpha` gives `A alpha + B = 0`.  Since `alpha notin F_p`, the
elements `1,alpha` are linearly independent over `F_p`, so `A=B=0`.  Thus
`L_U=L_{U'}` and the unordered blocks are equal.  The slope map is injective
on every fixed-tail admissible block slice.

Averaging over tails gives the displayed lower bound in terms of
`G_{p,k,sigma}`.  The next subsection gives the needed lower bound for every
fixed `sigma`.  Substituting that count into the standard double count gives

```text
binom(p-1,k+sigma) binom(k+sigma,sigma+1)
  / (p^(sigma-1) binom(p-1,k-1))
  = ((1-rho)^(sigma+1)/(sigma+1)! - o(1)) p^2.
```

This keeps the fixed-slack obstruction quadratic in the base field size for
every fixed `sigma`.

## Fixed-Slack Character Bound

Fix `sigma >= 2` and write `m=sigma-1`.  Assume `p>sigma`, so the integers
`1,...,m` are invertible in `F_p`.  By Newton identities,

```text
e_1(S)=...=e_m(S)=0
```

is equivalent to the power-sum system

```text
sum_{x in S} x^j = 0,        1 <= j <= m.
```

Let

```text
G_{p,a,sigma}
  = #{ S subset F_p^* : |S|=a, e_1(S)=...=e_m(S)=0 }.
```

Fourier inversion gives

```text
G_{p,a,sigma}
  = 1/p^m sum_{c in F_p^m}
      [Y^a] prod_{x in F_p^*}
        (1 + Y psi(c_1 x + ... + c_m x^m)),
```

where `psi` is a nontrivial additive character.  The `c=0` term contributes
`binom(p-1,a)`.

For `c != 0`, put

```text
P_c(X)=c_1X+...+c_mX^m,        F_c(x)=psi(P_c(x)).
```

The coefficient of `Y^a` in `prod_x(1+YF_c(x))` is

```text
1/a! * sum_{distinct x_1,...,x_a in F_p^*} prod_i F_c(x_i).
```

By the distinct-coordinate cycle expansion, each cycle of length `ell`
contributes

```text
S_ell(c)=sum_{x in F_p^*} psi(ell P_c(x)).
```

In the fixed-rate range we have `a<=p-1`, so `ell` is nonzero in `F_p`.
The polynomial `ell P_c` is nonconstant of degree at most `m < p`.  The Weil
bound for additive polynomial sums, with the `x=0` term removed, gives

```text
|S_ell(c)| <= (m-1) sqrt(p) + 1.
```

The cycle-index identity

```text
sum_{tau in S_a} u^{c(tau)}
  = u(u+1)...(u+a-1)
```

therefore implies

```text
|[Y^a] prod_{x in F_p^*} (1+YF_c(x))|
  <= binom(a+(m-1)sqrt(p)+1, a)
```

for every nonzero `c`.  Hence

```text
|G_{p,a,sigma} - binom(p-1,a)/p^m|
  <= binom(a+(m-1)sqrt(p)+1, a).
```

This already gives a finite certificate.  Define

```text
B_{p,a,sigma}
  = binom(a+(sigma-2)ceil(sqrt(p))+1, a),

R_{p,k,sigma}
  = max(0,
      ceil((binom(p-1,a) - (p^(sigma-1)-1)B_{p,a,sigma})
           / p^(sigma-1))),

N_{p,k,sigma,r}
  = ceil(R_{p,k,sigma} binom(a,sigma+r-1) / binom(p-1,k-r+1)).
```

Here `r` is any integer with `2 <= r <= [F_p(alpha):F_p]` and `k>=r-1`.
The case `sigma=1` uses the same definition with
`R_{p,k,1}=binom(p-1,k+1)`.  Then
`G_{p,a,sigma} >= R_{p,k,sigma}`.  Averaging the decompositions
`S=T union U` over all `(k-r+1)`-tails gives a tail with at least
`N_{p,k,sigma,r}` admissible blocks.  The higher-degree fixed-tail injectivity
argument below turns those blocks into distinct bad slopes.  Therefore, for every finite
extension `F/F_p` and every `alpha` of base-field degree at least `r`,

```text
emca(C_F, 1-(k+sigma)/(p-1)) >= N_{p,k,sigma,r} / |F|.
```

The lower numerator `N_{p,k,sigma,r}` is independent of the ambient extension
degree once such an `alpha` exists.  The earlier quadratic numerator statement
is the special case `r=2`.

For fixed `0<rho<1`, fixed `sigma`, and
`a=floor(rho(p-1))+sigma`, the right side is
`exp(O(sqrt(p) log p))`, while `binom(p-1,a)` is `exp(Theta(p))`.  Thus

```text
G_{p,a,sigma}
  = (1+o(1)) binom(p-1,a)/p^(sigma-1).
```

Combining this with the fixed-tail injectivity theorem gives

```text
max_T #{ admissible U for T }
  >= (1+o(1))
      binom(p-1,k+sigma) binom(k+sigma,sigma+1)
        / (p^(sigma-1) binom(p-1,k-1))
  = (1+o(1)) binom(p-k,sigma+1)/p^(sigma-1).
```

Since `p-k=(1-rho+o(1))p`, the number of distinct bad slopes is at least

```text
((1-rho)^(sigma+1)/(sigma+1)! - o(1)) p^2.
```

Dividing by `|F|=p^2` proves the displayed constant-density lower bound for
every fixed `sigma`.

More generally, if `alpha` has base-field degree at least a fixed `r>=2`, fix
a tail `T` of size `k-r+1` and let the moving block have size

```text
|U| = sigma+r-1.
```

The same prefix equations determine `e_1(U),...,e_{sigma-1}(U)` from `T`.
Thus, for two admissible blocks on the same tail, the difference
`L_U-L_{U'}` has degree at most `r-1`.  If their slopes are equal, then
`L_U(alpha)=L_{U'}(alpha)`. Since no nonzero polynomial of degree `<r` can
vanish at `alpha`, equality of slopes forces `L_U=L_{U'}`, hence `U=U'`.
Averaging over `(k-r+1)`-tails gives

```text
max_T #{ admissible U for T }
  >= (1+o(1)) binom(p-k+r-2,sigma+r-1) / p^(sigma-1).
```

For fixed `sigma`, fixed `r`, and fixed rate this is

```text
((1-rho)^(sigma+r-1)/(sigma+r-1)! - o(1)) p^r.
```

If `F=F_{p^e}` and `alpha` generates `F` over `F_p`, then `r=e`; after
division by `|F|=p^e`, the lower bound has constant density in every fixed
extension degree.

## Uniform Slow-Slack Consequence

The same finite character bound proves a controlled growing-slack statement.
Let `sigma=sigma(p)`, put `m=sigma-1`, and assume

```text
sigma=o(sqrt(p)/log p),        p>sigma.
```

Keep `k=floor(rho(p-1))` with fixed `0<rho<1` and `a=k+sigma`. The finite
bound above gives

```text
|G_{p,a,sigma} - binom(p-1,a)/p^m|
  <= binom(a+(m-1)sqrt(p)+1, a).
```

Write `u=(m-1)sqrt(p)+1`. Since `u=o(p)` and `a=rho p+o(p)`,

```text
log binom(a+u,a) <= u log(e(a+u)/u) = o(p).
```

Also `m log p=o(p)`, while

```text
log binom(p-1,a) = (H(rho)+o(1))p
```

with `H(rho)>0`. Therefore

```text
p^m binom(a+u,a) / binom(p-1,a) -> 0,
```

and hence

```text
G_{p,k,sigma}
  = (1+o(1)) binom(p-1,k+sigma) / p^(sigma-1)
```

uniformly in this slow-slack range. Combining with the fixed-tail injectivity
and double-counting identity gives

```text
max_T #{ admissible U for T }
  >= (1+o(1)) binom(p-k,sigma+1) / p^(sigma-1).
```

This is the extension-field numerator forced by the degree-one line.

Now suppose, more restrictively, that for some fixed `0<epsilon<1`,

```text
sigma <= (1-epsilon) log p / log log p.
```

Using Stirling and `p-k=(1-rho+o(1))p`,

```text
log( binom(p-k,sigma+1) / p^(sigma-1) )
  = 2 log p - log((sigma+1)!) + O(sigma)
  >= (1+epsilon-o(1)) log p.
```

Thus

```text
|F| emca(C_F, 1-(k+sigma)/(p-1)) >= p^(1+epsilon-o(1)).
```

Equivalently, for an extension `F/F_p` of fixed degree `e>=2`,

```text
emca(C_F, 1-(k+sigma)/(p-1)) >= p^(1+epsilon-o(1)) / |F|.
```

A same-numerator lift from the base-field numerator `p` would give density
`p/|F|`. The degree-one extension line therefore beats that prediction by the
factor `p^(epsilon-o(1))` throughout this slowly growing slack window. This is
still far below the corrected reserve
`sigma >= C n/log n`; it sharpens the lower-bound side without claiming a
positive theorem near the reserve.

With an element of base-field degree at least fixed `r`, the same slow-slack
argument gives numerator

```text
(1+o(1)) binom(p-k+r-2,sigma+r-1) / p^(sigma-1).
```

In the logarithmic slow-slack window above, this is at least
`p^(r-1+epsilon-o(1))`.  Thus higher-degree extension lines amplify the
failure of same-numerator transfer by the factor `p^(r-2+epsilon-o(1))` over
the base numerator `p`.

## Exact Sigma-Three Prefix Count Recurrence

For `sigma=3`, the prefix-vanishing equations admit a particularly small
finite counter. Since

```text
e_2(S) = (e_1(S)^2 - sum_{x in S} x^2)/2,
```

and `p` is odd, the equations `e_1(S)=e_2(S)=0` are equivalent to

```text
sum_{x in S} x = 0,        sum_{x in S} x^2 = 0.
```

Let `C_m(b,r,s)` be the number of `b`-subsets of `{1,...,m}` with

```text
e_1 = r,        e_2 = s        in F_p.
```

When a point `x` is added to a set, the elementary symmetric data update by

```text
e_1 -> e_1 + x,
e_2 -> e_2 + x e_1.
```

Thus the triangular recurrence

```text
C_m(b,r,s)
  = C_{m-1}(b,r,s)
    + C_{m-1}(b-1, r-m, s-m(r-m))
```

with residues read modulo `p` computes

```text
G_{p,k,3} = C_{p-1}(k+3,0,0)
```

exactly, without enumerating `binom(p-1,k+3)` supports.

There is also a useful check on the count.  For `p>3`,

```text
prod_{x in F_p^*} (X-x) = X^(p-1)-1,
```

so the full domain has `e_1=e_2=0`.  If `S` and `R=F_p^*\S` are complements,
then

```text
e_1(F_p^*) = e_1(S)+e_1(R),
e_2(F_p^*) = e_2(S)+e_1(S)e_1(R)+e_2(R).
```

Therefore `S` is sigma-three prefix-vanishing if and only if `R` is.  The
verifier checks this complement symmetry for every computed size.

The same script gives exact finite lower bounds for the sigma-three
degree-one obstruction by combining `G_{p,k,3}` with the fixed-tail averaging
theorem above.  Some sample certified cases are:

```text
p   k   a=k+3   G_{p,k,3}       tail lower bound
29  14  17      25,536          2
37  18  21      4,067,064       3
47  23  26      2,538,811,346   5
59  29  32      6,363,217,823,105  8
31   7  10      31,275          12
41  10  13      7,158,280       19
53  13  16      3,689,282,935   33
```

The first four rows are near rate `1/2`; the last three are near rate `1/4`.
These rows are finite certificates for the exact recurrence and lower-bound
pipeline.  The fixed-slack character bound above is the asymptotic proof that
the same count has density `(1+o(1))p^-2` at every fixed rate.

The verifier also runs the same dynamic count for the first cases beyond
`sigma=3`, using the elementary-symmetric update directly and checking the
integer form of the general character-error bound.  Sample rows are:

```text
p   sigma   k   a=k+sigma   G_{p,k,sigma}   tail lower bound
17    4     4       8        6               1
19    4     7      11        18              1
23    4     8      12        44              1
17    5     3       8        2               1
19    5     4       9        2               1
23    5     6      11        2               1
```

These small rows are intentionally modest: their role is to audit the
fixed-sigma DP, complement symmetry, and integer Weil-bound inequality in the
first `sigma=4,5` cases.

For fixed rate `k=floor(rho(p-1))`, the numerator ratio

```text
binom(p-a+1, 2) / p^2
```

tends to `(1-rho)^2/2`, since `a=k+1`. Equivalently,
`|F|*emca(C_F,delta)` is at least `((1-rho)^2/2-o(1))p^2` for every fixed
extension degree `e>=2`.

Finally, over the base field `B`, the trivial bound

```text
emca(C_B, delta) <= 1 = p/p
```

is a numerator-`p` bound. An unrestricted numerator-preserving lift would turn
that into an extension-field estimate of size `p^{1+o(1)}/p^e`. The lower
bound above has numerator `Theta(p^2)`, so even in higher extensions the
unrestricted same-numerator lift undercounts the forced extension-valued
residue-line numerator by a factor `Theta(p)`.

## Ledger Impact

This proof isolates the exact obstruction in the F1 direction. The bad line is
not a base-valued line whose slopes are merely being reinterpreted in a larger
field. Its denominator `X-alpha` is genuinely extension-valued, and the bad
slopes record base-field pair sums and products through evaluation at `alpha`.

Consequently a protocol ledger cannot safely take an MCA numerator proved over
`q_line = |B|` and divide it by an extension challenge field `|F|` for arbitrary
`F`-valued lines. The sigma-one extension numerator is already quadratic in
`|B|`, even when `|F|` is a higher extension. The fixed-slack character bound
shows that every fixed positive residual slack still leaves constant-density
degree-one families, and the uniform version shows that the same numerator
obstruction persists into the slowly growing range
`sigma <= (1-epsilon) log p/log log p`. The finite form shows that these are
extension-degree-independent numerator lower bounds: increasing the challenge
field only divides the same numerator by a larger `|F|`. The repaired theorem
with an element of degree at least `r` strengthens the numerator from quadratic
to order `p^r`, giving constant-density counterexamples in every fixed
extension degree when `alpha` generates the extension. The repaired theorem
needs residual slack large enough for the list ledger, not merely nonzero or
logarithmic slack. A repaired F1 theorem must either:

- prove MCA directly over the actual extension line field;
- add an extension-valued residue-line numerator term;
- restrict to a corrected-reserve regime where this sigma-one construction is
  excluded; or
- reformulate extension-valued lines as structured affine-subspace or
  interleaved-base objects over `B`.

## Relation To Existing Experimental Material

This note extracts a clean proof from the F1 audit bundle. The verifier

```text
experimental/scripts/verify_f1_fixed_rate_extension_counterexample.py
```

checks finite instances over `F_{p^2}`.  For the sigma-one family at
`p=5,7,11,13`, it enumerates every `a=k+1` support, constructs the slope
`z_S=Q_S(alpha)`, checks the explaining polynomial
`(Q_S-z_S)/(X-alpha)`, verifies same-support noncontainment by interpolation
of the direction `-1/(X-alpha)`, and checks the fixed-tail pair-slice
injectivity giving

```text
binom(p-a+1,2)
```

distinct bad slopes.  The theorem above is the general finite-field proof of
that mechanism.

For the sigma-two family at `p=7,11,13`, the same verifier enumerates all
zero-sum `a=k+2` supports, checks the degree drop `deg Q_S <= k`, verifies
the same support-wise bad-slope and noncontainment conditions, and finds a
tail `T` whose zero-sum triples meet the averaged lower bound.  It then checks
that the slopes on that tail/triple slice are distinct.  This replaces the
older F1 audit-bundle verifier reference

```text
experimental/scripts/codex_f1_l1_20260617/verifiers/\
verify_f1_sigma2_degree1.py
```

The verifier also checks the general fixed-slack template at `sigma=3` for
`(p,k)=(13,3),(17,5),(19,6)`: it enumerates supports satisfying
`e_1(S)=e_2(S)=0`, verifies the degree drop and noncontainment, finds a tail
meeting the double-count average, and checks injectivity on the resulting
four-block slice.  These finite checks supplement the fixed-sigma asymptotic
theorem above by auditing the first nontrivial prefix-count case directly.

For larger sigma-three cases, the verifier switches to the exact recurrence
in the previous section.  It computes `G_{p,k,3}` without support
enumeration, verifies complement symmetry, and reports the finite tail-averaged
lower bound for the distinct bad slopes forced by the general template.  It
also checks the integer form of the character-error bound against the exact
dynamic counts.

The verifier also includes generic fixed-sigma count cases for `sigma=4,5`.
These use the elementary-symmetric DP directly, verify complement symmetry,
check the integer Weil-bound inequality from the fixed-slack character proof,
and report the tail-averaged lower bound.

Finally, the verifier evaluates the explicit finite lower formula coming from
the character bound in several slow-slack rows. These rows do not enumerate
supports; they certify that the lower bound from

```text
G >= (binom(p-1,a)
      - (p^(sigma-1)-1) binom(a+(sigma-2)ceil(sqrt(p))+1,a))
     / p^(sigma-1)
```

is positive and that the resulting tail-averaged bad-slope numerator already
exceeds the base-field numerator `p`. It also reports the same numerator over
several extension degrees, confirming that the proof is an extension-degree
independent numerator obstruction and not a quadratic-only density accident.
The minimal-degree rows check the higher-degree amplification: for elements of
degree at least `r`, the script fixes `(k-r+1)`-tails, checks that the high
coefficients of each admissible block locator are forced by the tail, and
verifies that the remaining `r` low coefficients are distinct on the best-tail
slice. The finite bound rows then certify the corresponding amplified
bad-slope numerators for `r=3` and `r=4`.
