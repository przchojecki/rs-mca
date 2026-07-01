# M3 Low-Rank Affine Spectral Reduction

Status: PROVED / AUDIT.

This note records the structural lemma behind the synthetic low-rank affine
packets in PR #170.  It does not extend the packet to arbitrary M3 row data.
Its role is to replace the opaque statement "selected minors are coprime" by
explicit spectral-disjointness targets for small kernels.

## Setup

Let `F` be a field.  Let

```text
X = (x_0,...,x_{m-1}),    Y = (y_0,...,y_{r-1})
```

with the `x_i` distinct, nonzero, and disjoint from the `y_a`.  Let `L_i(T)`
be the Lagrange basis polynomial for `X`, so `L_i(x_l)=1` if `i=l` and `0`
otherwise.

For `h=0,1`, define the square shifted Hankel moment matrices

```text
H_X^(h)[a,b] = sum_i x_i^(a+b+h),
H_Y^(h)[a,b] = sum_c y_c^(a+b+h),        0 <= a,b < m.
```

The synthetic low-rank pencil is

```text
H_X^(h) + Z H_Y^(h).
```

In the `F_17^32` M3 packet, `m=j+1`, `X` is the first `j+1` descriptor-domain
nodes, and `Y` is the next `rank` descriptor-domain nodes.

## Adjacent-Shift Lemma

Define two `r x r` kernels

```text
K_0[a,b] = sum_i L_i(y_a) L_i(y_b),

K_1[a,b] = y_a * sum_i x_i^(-1) L_i(y_a) L_i(y_b).
```

Then

```text
det(H_X^(0) + Z H_Y^(0))
  = det(V_X)^2 * det(I_r + Z K_0),

det(H_X^(1) + Z H_Y^(1))
  = det(V_X)^2 * (prod_i x_i) * det(I_r + Z K_1),
```

where `V_X[a,i]=x_i^a`.

Proof.  Write

```text
H_X^(0) = V_X V_X^T,
H_Y^(0) = V_Y V_Y^T,
H_X^(1) = V_X D_X V_X^T,
H_Y^(1) = V_Y D_Y V_Y^T,
```

with `D_X=diag(x_i)` and `D_Y=diag(y_a)`.  Since the `x_i` are distinct and
nonzero, both `V_X` and `D_X` are invertible.  The matrix determinant lemma
gives

```text
det(V_X V_X^T + Z V_Y V_Y^T)
  = det(V_X)^2 det(I_r + Z V_Y^T V_X^(-T) V_X^(-1) V_Y),

det(V_X D_X V_X^T + Z V_Y D_Y V_Y^T)
  = det(V_X)^2 det(D_X)
    det(I_r + Z D_Y V_Y^T V_X^(-T) D_X^(-1) V_X^(-1) V_Y).
```

The coordinate vector `V_X^(-1) v(y)` is `(L_i(y))_i`.  Substituting these
coordinates gives the displayed formulas.

## Contiguous-Shift Lemma

More generally, for every integer `h >= 0`, put

```text
H_X^(h)[a,b] = sum_i x_i^(a+b+h),
H_Y^(h)[a,b] = sum_c y_c^(a+b+h),

K_h[a,b] = y_a^h * sum_i x_i^(-h) L_i(y_a)L_i(y_b).
```

Then

```text
det(H_X^(h) + Z H_Y^(h))
  = det(V_X)^2 * (prod_i x_i^h) * det(I_r + Z K_h).
```

Proof.  The same determinant-lemma computation applies with
`D_X^h=diag(x_i^h)` and `D_Y^h=diag(y_a^h)`:

```text
H_X^(h) = V_X D_X^h V_X^T,
H_Y^(h) = V_Y D_Y^h V_Y^T.
```

Since every `x_i` is nonzero, `D_X^h` is invertible.  Therefore

```text
det(V_X D_X^h V_X^T + Z V_Y D_Y^h V_Y^T)
  = det(V_X)^2 det(D_X^h)
    det(I_r + Z D_Y^h V_Y^T V_X^(-T) D_X^(-h) V_X^(-1) V_Y),
```

and substituting the Lagrange coordinates of `V_X^(-1)v(y_a)` gives `K_h`.
The adjacent-shift lemma is the special case `h=0,1`.

## Cauchy-Binet Coefficient Formula

The same shifted determinant also has a replacement-subset expansion.  Let
`S` run through the `m`-element subsets of `X union Y`, and put

```text
c_s = 1 if s in X,
c_s = Z if s in Y.
```

Then

```text
det(H_X^(h) + Z H_Y^(h))
  = sum_{|S|=m} det(V_S)^2 * prod_{s in S} s^h c_s.
```

Equivalently, the coefficient of `Z^d` is

```text
sum_{I subset X, J subset Y, |I|=|J|=d}
  det(V_{(X minus I) union J})^2
  * prod_{s in (X minus I) union J} s^h.
```

Proof.  Write the shifted pencil as one weighted Vandermonde Gram matrix over
`X union Y`:

```text
H_X^(h) + Z H_Y^(h)
  = V_{X union Y} diag(s^h c_s) V_{X union Y}^T.
```

Cauchy-Binet gives the displayed sum over `m` chosen columns.  Grouping terms
by the number `d` of chosen elements from `Y` gives the replacement formula.

After dividing by the nonzero base factor `det(V_X)^2 prod_{x in X} x^h`, the
normalized coefficient is

```text
sum_{I,J, |I|=|J|=d}
  (det(V_{(X minus I) union J}) / det(V_X))^2
  * prod_{y in J} y^h / prod_{x in I} x^h.
```

Thus, for consecutive subgroup nodes, the affine spectral-disjointness problem
can be attacked either through the small kernels `K_h` or through explicit
replacement sums over the interval of exponents.  The PR #170 verifier uses the
kernel form; this formula is the coefficient-level proof target for a future
symbolic or q-binomial argument.

## Replacement-Minor Compression

The replacement determinant in the coefficient formula is itself a Lagrange
minor.  Let `I` be a `d`-element subset of the indices of `X`, and let `J` be a
`d`-element subset of `Y`.  Write

```text
L[J,I] = (L_i(y))_{y in J, i in I}.
```

Then

```text
(det(V_{(X minus I) union J}) / det(V_X))^2 = det(L[J,I])^2.
```

The unsquared identity has a sign depending only on the ordering convention for
the replaced columns; the square is canonical.

Proof.  In the column basis `v(x_0),...,v(x_{m-1})` of `V_X`, the column
`v(y)` has coordinate vector `(L_i(y))_i`.  Replacing the columns indexed by
`I` and expanding by multilinearity leaves only the determinant of the
coordinate submatrix on those replaced columns; all terms using a column outside
`I` repeat an existing basis column and vanish.

Consequently the normalized coefficient can be written as

```text
[Z^d] det(I_r+ZK_h)
  = sum_{J subset Y, |J|=d}
      sum_{I subset X, |I|=d}
        det(L[J,I])^2
        * prod_{y in J} y^h / prod_{x_i in I} x_i^h.
```

Equivalently, by Cauchy-Binet applied to

```text
K_h[J,J] = diag(y^h)_{y in J} L[J,X] diag(x_i^(-h)) L[J,X]^T,
```

the same coefficient is the sum of principal minors

```text
[Z^d] det(I_r+ZK_h) = sum_{J subset Y, |J|=d} det(K_h[J,J]).
```

This is the precise bridge between the q-binomial-looking replacement sums and
the rank-size kernels used by the verifier.

## Trace / One-Replacement Coefficient

The first nonconstant coefficient of the normalized shifted determinant is the
trace of the shifted kernel:

```text
[Z] det(I_r+ZK_h)
  = tr(K_h)
  = sum_a y_a^h sum_i x_i^(-h) L_i(y_a)^2.
```

This follows either from the determinant identity
`det(I+ZK_h)=1+Z tr(K_h)+O(Z^2)` or from the `d=1` case of the replacement
formula.

For the normalized consecutive subgroup window

```text
X={1,alpha,...,alpha^(m-1)},
Y={alpha^m,...,alpha^(m+r-1)},
```

this becomes

```text
[Z] det(I_r+ZK_h)
  = sum_{a=0}^{r-1} sum_{i=0}^{m-1}
      L_i(alpha^(m+a))^2 * alpha^(h(m+a-i)).
```

Equivalently,

```text
L_i(alpha^(m+a))
  = prod_{0 <= ell < m, ell != i}
      (alpha^(m+a-ell)-1)/(alpha^(i-ell)-1).
```

All denominators are nonzero because the row domain has order `512` and the
M3 window has `m <= 128`; hence the exponents `i-ell` are nonzero modulo the
domain order.  Thus the trace is a completely explicit subgroup sum.  Any
eventual proof that the adjacent spectra are disjoint must, in particular,
control the two first coefficients

```text
tr(K_0),    tr(K_1).
```

The verifier does not currently use this closed form; it is included to expose
the first algebraic invariant one would attack in a hand proof.

For later symbolic work, the Lagrange value above can be written without a
hidden product over deleted nodes.  Put

```text
P_s = prod_{t=1}^s (1-alpha^t),    P_0=1,
R_i = m-1-i.
```

For `0 <= i < m` and `0 <= a < r`,

```text
L_i(alpha^(m+a))
  = (-1)^R_i alpha^(R_i(R_i+1)/2)
    * P_{a+m} /
      (P_a P_i P_{R_i} (1-alpha^(m+a-i))).
```

Proof.  Starting from

```text
L_i(alpha^(m+a))
  = prod_{ell != i} (alpha^(m+a-ell)-1)/(alpha^(i-ell)-1),
```

the numerator is

```text
(-1)^(m-1) P_{a+m} / (P_a (1-alpha^(m+a-i))).
```

The denominator is

```text
(-1)^i alpha^(-R_i(R_i+1)/2) P_i P_{R_i}.
```

Dividing gives the displayed formula.  In the current M3 window the relevant
exponents are all strictly between `0` and `512`, so the displayed factors are
nonzero in the order-512 subgroup.

## Cauchy Factorization

The closed product form separates the full Lagrange evaluation matrix into
diagonal factors and one geometric Cauchy matrix.  Define

```text
rho_a = P_{a+m}/P_a,
gamma_i =
  (-1)^(m-1-i) alpha^((m-1-i)(m-i)/2) / (P_i P_{m-1-i}),
C[a,i] = 1/(1-alpha^(m+a-i)).
```

Then, for `L[a,i]=L_i(alpha^(m+a))`,

```text
L = diag(rho_a) C diag(gamma_i).
```

This is just the closed product formula with the row factor, Cauchy factor, and
column factor separated.

Therefore every square replacement minor has the closed form

```text
det(L[J,I])^2
  = (prod_{a in J} rho_a^2)
    * (prod_{i in I} gamma_i^2)
    * prod_{a<a' in J} (u_a-u_a')^2
    * prod_{i<i' in I} (v_i-v_i')^2
    / prod_{a in J, i in I} (1-u_a v_i)^2,
```

where `u_a=alpha^(m+a)` and `v_i=alpha^(-i)`.  In particular, every such
minor is nonzero whenever the update window is disjoint from the base window.
The rectangular evaluation matrix `L[Y,X]` is totally nonsingular on these
consecutive subgroup windows.

For the current M3 range, and for the endpoint-capacity ranks targeted by this
low-rank model, the exponents `m+a-i` lie strictly between `0` and `512`, so
the denominators are nonzero in the order-512 subgroup.  Thus the only possible
vanishing in coefficients of `det(I+ZK_h)` comes from cancellation among
explicit nonzero q-Cauchy terms, not from singular replacement minors.

Consequently, with `x_i=alpha^i` and `y_a=alpha^(m+a)`,

```text
K_h
  = diag(y_a^h rho_a) C diag(alpha^(-h*i) gamma_i^2) C^T diag(rho_a).
```

Thus each principal minor of the shifted kernel has an explicit Cauchy-product
expansion.  For a `d`-element subset `J` of update indices,

```text
det(K_h[J,J])
  = (prod_{a in J} alpha^(h(m+a)) rho_a^2)
    * sum_{I subset {0,...,m-1}, |I|=d}
        (prod_{i in I} alpha^(-h*i) gamma_i^2) det(C[J,I])^2.
```

This follows by taking determinants of the two outer diagonal factors on the
principal submatrix and applying Cauchy-Binet to the middle product
`C[J,*] diag(alpha^(-h*i) gamma_i^2) C[J,*]^T`.

Finally, if `u_a=alpha^(m+a)` and `v_i=alpha^(-i)`, then the Cauchy determinant
has square

```text
det(C[J,I])^2
  =
  prod_{a<a' in J} (u_a-u_a')^2
  * prod_{i<i' in I} (v_i-v_i')^2
  / prod_{a in J, i in I} (1-u_a v_i)^2.
```

All denominators are nonzero in the current window.  Therefore every
coefficient of `det(I+ZK_h)` is an explicit finite q-Cauchy sum.  This is a
more rigid target than a black-box field gcd: a hand proof of spectral
disjointness can try to compare these q-Cauchy sums across `h=0,1`, while a
future symbolic checker can audit the same formulas without rebuilding the
large Hankel minors.

## Toeplitz-Cauchy Form

The normalized consecutive-window Cauchy matrix has one more useful structure:
it is Toeplitz.  With

```text
tau_s = 1/(1-alpha^(m+s)),
```

the middle Cauchy factor satisfies

```text
C[a,i] = tau_{a-i}.
```

Thus all square replacement minors split as

```text
det(L[J,I])^2
  = (prod_{a in J} rho_a^2)
    * (prod_{i in I} gamma_i^2)
    * det((tau_{a-i})_{a in J, i in I})^2.
```

Equivalently, the shifted kernel can be written from one rectangular
Toeplitz-Cauchy array `T_{m,r}[a,i]=tau_{a-i}` as

```text
K_h = diag(alpha^(h(m+a)) rho_a)
      T_{m,r}
      diag(alpha^(-h*i) gamma_i^2)
      T_{m,r}^T
      diag(rho_a).
```

For the endpoint-capacity target

```text
87 <= m <= 128,    2 <= r <= ceil((m-1)/2),
```

the exponents `m+a-i` appearing in `tau_{a-i}` lie between `1` and `191`, so
none is `0` modulo the subgroup order `512`.  The finite target is therefore a
Toeplitz-Cauchy spectral-disjointness problem with explicit nonzero diagonal
weights.  This is still not a proof of coprimality, but it removes arbitrary
matrix structure from the normalized low-rank branch.

## Rank-One Displacement

The same Toeplitz-Cauchy factor has displacement rank one.  Let

```text
U = diag(alpha^(m+a))_{0 <= a < r},
V = diag(alpha^(-i))_{0 <= i < m},
1_r = column vector of r ones,
1_m = column vector of m ones.
```

Then

```text
T_{m,r} - U T_{m,r} V = 1_r 1_m^T.
```

This is an entrywise identity:

```text
(1-alpha^(m+a-i)) T_{m,r}[a,i] = 1.
```

In the endpoint-capacity range the factors `1-alpha^(m+a-i)` are all nonzero,
so the Sylvester operator

```text
Delta(X) = X - U X V
```

is invertible on `r x m` matrices, with explicit inverse

```text
Delta^(-1)(B)[a,i] = B[a,i]/(1-alpha^(m+a-i)).
```

Thus `T_{m,r}` is the unique solution of a rank-one displacement equation, and
the normalized Lagrange evaluation matrix is

```text
L = diag(rho_a) Delta^(-1)(1_r 1_m^T) diag(gamma_i).
```

The remaining spectral-disjointness target can therefore be viewed as a
weighted Gram problem for a rank-one displacement inverse, not merely as a
family of unrelated small dense matrices.

## Shift-Two Core Displacement

The displacement identity also relates the weighted Gram cores for different
row shifts.  Put

```text
B_h = diag(alpha^(-h*i) gamma_i^2)_{0 <= i < m},
S_h = T_{m,r} B_h T_{m,r}^T.
```

Since `V B_h V = B_{h+2}`, the identity `T-U T V=1_r 1_m^T` gives

```text
S_h - U S_{h+2} U
  = T B_h 1_m 1_r^T
    + 1_r 1_m^T B_h T^T
    - 1_r 1_m^T B_h 1_m 1_r^T.
```

Equivalently, if

```text
w_h = T B_h 1_m,
c_h = 1_m^T B_h 1_m,
```

then

```text
S_h - U S_{h+2} U = w_h 1_r^T + 1_r w_h^T - c_h 1_r 1_r^T.
```

The right-hand side has rank at most `2`.  Thus consecutive even shifts of the
core kernel are related by a diagonal rescaling plus a rank-two correction
(and the same statement holds separately for odd shifts).  The original target
only uses `h=0,1`, but this identity is useful for any future pivot packet that
uses more contiguous row shifts: all such cores live in two low-displacement
chains rather than as unrelated dense matrices.

## Weighted-Core Characteristic Polynomial

The actual determinant polynomial `Phi_{m,r,h}(Z)=det(I+ZK_h)` can be written
directly from the core `S_h`.  Let

```text
D_h = diag(alpha^(h(m+a)) rho_a^2)_{0 <= a < r}.
```

Then

```text
Phi_{m,r,h}(Z) = det(I_r + Z D_h S_h).
```

Indeed, from the Toeplitz-Cauchy form,

```text
K_h = diag(alpha^(h(m+a)) rho_a) S_h diag(rho_a).
```

If `A=diag(alpha^(h(m+a)) rho_a) S_h` and `B=diag(rho_a)`, then
`det(I+ZAB)=det(I+ZBA)`.  Since the two diagonal factors commute,
`BA=D_h S_h`.

Thus the endpoint-capacity target is equivalently

```text
gcd(det(I+Z D_0 S_0), det(I+Z D_1 S_1)) = 1
```

for the stated `(m,r)` range.  The shift-two displacement relation acts on
`S_h`, while this identity records exactly how `S_h` feeds the characteristic
polynomials used by the v10 affine gcd ledger.

## Shift-Two Transfer Formula

Combining the preceding two reductions gives a determinant-level transfer
between shifts of the same parity.  Write the rank-two correction as

```text
S_h = U S_{h+2} U + P_h Q_h^T,

P_h = [ w_h, 1_r ],
Q_h = [ 1_r, w_h - c_h 1_r ].
```

For

```text
M_h(Z) = I_r + Z D_h U S_{h+2} U,
```

one has

```text
det M_h(Z) = Phi_{m,r,h+2}(Z),
```

because `det(I+AB)=det(I+BA)` and `U D_h U = D_{h+2}`.  Since `M_h(0)=I`,
`M_h(Z)` is invertible over the rational function field `F(Z)`, and the matrix
determinant lemma gives

```text
Phi_{m,r,h}(Z)
  =
  Phi_{m,r,h+2}(Z)
  * det(I_2 + Z Q_h^T M_h(Z)^(-1) D_h P_h).
```

Thus every two-step shift changes the determinant polynomial by a two-by-two
transfer factor over `F(Z)`.  The displayed identity is not yet a coprimality
proof, but it localizes multi-shift comparisons to rank-two transfer data
instead of full `r x r` determinant recomputation.

## Window Normalization

Two elementary invariances reduce the consecutive-subgroup case to a normalized
window.

First, if `beta` is nonzero and

```text
beta X = (beta x_0,...,beta x_{m-1}),
beta Y = (beta y_0,...,beta y_{r-1}),
```

then

```text
det(H_{beta X}^(h) + Z H_{beta Y}^(h))
  = beta^(hm+m(m-1)) det(H_X^(h) + Z H_Y^(h)).
```

Indeed, with `D_beta=diag(1,beta,...,beta^(m-1))`, the shifted moment matrix
for `beta X` is

```text
H_{beta X}^(h) = beta^h D_beta H_X^(h) D_beta,
```

and the same formula holds for `Y`.  Taking determinants gives the displayed
scalar factor.  Since this factor is nonzero, affine roots and gcds of shifted
minors are unchanged by multiplying the whole window by `beta`.

Second, if all nodes lie in a multiplicative subgroup of order `N`, then

```text
H_X^(h+N) = H_X^(h),     H_Y^(h+N) = H_Y^(h),
```

so the shifted determinants and kernels are periodic in `h` modulo `N`.

For the accepted `F_17^32` row, the domain is the order-512 subgroup

```text
1, alpha, alpha^2, ..., alpha^511.
```

Therefore a consecutive low-rank window

```text
X = beta {1,alpha,...,alpha^(m-1)},
Y = beta {alpha^m,...,alpha^(m+r-1)}
```

has the same finite affine root data as the normalized window with `beta=1`,
and only `h mod 512` matters.  This is why the synthetic packet can use the
prefix `X={1,alpha,...,alpha^j}` without losing any case that differs only by
a cyclic domain rotation.

## Consequence For The v10 GCD Ledger

The common finite affine roots of the two displayed maximal minors are exactly
the common roots of

```text
det(I_r + Z K_0),    det(I_r + Z K_1).
```

Equivalently, the relevant nonzero reciprocal spectra of `K_0` and `K_1` are
disjoint.  Therefore the finite affine part of the v10 rank-drop ledger is
empty whenever

```text
gcd(det(I_r + Z K_0), det(I_r + Z K_1)) = 1.
```

This is the formal reason the PR #170 affine packet can certify zero finite
affine roots by checking only the prefix and row-shift-1 maximal minors: the
canonical v10 affine rank-drop gcd divides the gcd of any two nonzero maximal
minors.  The contiguous-shift lemma gives the same small-kernel representation
for every contiguous row-set minor `h..h+m-1`; future pivot packets can use
additional shifts by replacing `K_0,K_1` with the corresponding `K_h` family.

## Contiguous All-Shift Target

The two-minor test used by the current packet is sufficient but not necessary
for the v10 regular bucket.  A less overdetermined sufficient test uses every
contiguous maximal minor.  In the exact-agreement row `A`, put

```text
j = n-A,      m = j+1,      t = A-k.
```

The regular Hankel matrix has `t` rows and `m` columns.  Its contiguous maximal
minors start at

```text
h = 0,1,...,t-m.
```

If a finite affine slope is a v10 rank-drop slope for this bucket, then the
full `t x m` Hankel matrix has rank `< m`, so every maximal minor vanishes.  In
particular, all contiguous minors vanish.  After the contiguous-shift reduction,
the canonical finite affine root set is contained in the roots of the
contiguous all-shift gcd

```text
G_{m,r}^{all}(Z)
  =
  gcd(Phi_{m,r,h}(Z) : 0 <= h <= t-m).
```

For the `F_17^32`, `n=512`, `k=256` M3 window, `A=513-m` and hence

```text
t-m+1 = 258-2m.
```

Thus the contiguous all-shift low-rank regular target is

```text
G_{m,r}^{all}(Z) = 1
for every 87 <= m <= 128 and 2 <= r <= ceil((m-1)/2),
```

where the gcd uses `258-2m` shifted polynomials.  The adjacent target

```text
gcd(Phi_{m,r,0}, Phi_{m,r,1}) = 1
```

implies this all-shift target, and coincides with it only at the endpoint
`m=128` where there are exactly two contiguous shifts.  For `m<128`, the
all-shift target is weaker and is the more literal v10 canonical rank-drop
condition among contiguous row-set minors.  It is still only a sufficient test
for the full all-maximal-minor canonical gcd.  The shift-two transfer formula
above gives a structured way to study the even and odd chains inside this
all-shift gcd.

## Rectangular Rank-Drop Nullpolynomial

The contiguous all-shift gcd is still only a root-containment test.  The
underlying v10 regular bucket is rectangular.  Define the full contiguous
`t x m` moment pencil

```text
R_{t,m}(Z)[a,b]
  =
  sum_{x in X} x^(a+b) + Z sum_{y in Y} y^(a+b),
  0 <= a < t, 0 <= b < m.
```

For a finite slope `z`, the matrix `R_{t,m}(z)` has rank `< m` if and only if
there is a nonzero polynomial

```text
P(T) = p_0 + p_1 T + ... + p_{m-1} T^(m-1)
```

such that

```text
sum_{x in X} x^a P(x) + z sum_{y in Y} y^a P(y) = 0
for every 0 <= a < t.
```

Indeed, multiplying `R_{t,m}(z)` by the coefficient vector of `P` gives exactly
these `t` moment equations.  Thus a genuine rectangular rank-drop slope gives
one nullpolynomial satisfying all row moments at once.

By contrast, a root of the contiguous all-shift gcd only says that every
sliding `m x m` block is singular:

```text
det(H_X^(h)+zH_Y^(h)) = 0,
0 <= h <= t-m.
```

It may a priori use a different nullpolynomial for each shift `h`.  Therefore
the containments in the synthetic low-rank branch are:

```text
rectangular rank-drop slopes
  subset roots of G_{m,r}^{all}
  subset roots of any selected shifted-minor gcd.
```

The nullpolynomial formulation is the sharper proof target for the actual v10
regular bucket: after quotient and endpoint ledgers are removed, one can try to
prove that no nonzero degree-`<m` polynomial has the displayed `t` vanishing
weighted moments for an unpaid slope `z`.

## Current Certified Instance

The verifier

```text
experimental/scripts/verify_f17_32_m3_low_rank2_12_v10_affine_gcd.py
```

implements this reduction for the accepted `F_17^32`, `n=512`, `k=256` row.
For every `385 <= A <= 426` and every synthetic rank `2..12`, it checks:

```text
deg det(I + Z K_0) = rank,
deg det(I + Z K_1) = rank,
gcd(det(I + Z K_0), det(I + Z K_1)) = 1.
```

Thus the finite affine v10 rank-drop root set is empty for those structured
low-rank branches.

## Next Proof Target

The endpoint side of the same synthetic ladder is now exact for the `c=2`
full-fiber mechanism up to `rank <= 256-floor(A/2)`.  The affine bottleneck can
be attacked through the sufficient adjacent-pair spectral problem:

```text
For the consecutive subgroup nodes X={alpha^0,...,alpha^j}
and Y={alpha^(j+1),...,alpha^(j+r)}, prove that K_0 and K_1 have no common
nonzero reciprocal eigenvalue for the desired rank range.
```

In the `F_17^32`, `n=512`, `k=256` M3 window, `m=j+1=513-A`, so

```text
385 <= A <= 426        <=>        87 <= m <= 128,
rank_capacity(A) = 256-floor(A/2) = ceil((m-1)/2).
```

Using the explicit q-Cauchy coefficients above, define

```text
Phi_{m,r,h}(Z) = det(I_r+ZK_h)
```

for the normalized consecutive subgroup window.  The sufficient adjacent
symbolic target for the endpoint-capacity low-rank model is therefore:

```text
gcd(Phi_{m,r,0}(Z), Phi_{m,r,1}(Z)) = 1
for every 87 <= m <= 128 and 2 <= r <= ceil((m-1)/2).
```

The current verifier proves this adjacent target only for `2 <= r <= 12`.
A proof of the displayed adjacent range would imply the contiguous all-shift
target above.  Alternatively, proving `G_{m,r}^{all}=1` directly would be
enough for this sufficient contiguous-minor v10 regular rank-drop test and may
be easier away from `m=128`, where many more shifted minors are available.  A
still sharper route is to use the rectangular nullpolynomial formulation and
rule out a single nonzero degree-`<m` polynomial satisfying all `t` moment
equations for an unpaid slope.  Together with the endpoint `c=2` capacity
packet, any of these affine exclusions would close the synthetic low-rank
regular projective residual through the endpoint capacity range.  It would
still not be an arbitrary-row M3 theorem; it would be a clean model result
explaining why this low-rank branch has no unpaid regular projective residual.

The script

```text
experimental/scripts/search_f17_32_m3_low_rank_spectral_target.py
```

is a counterexample-first probe for this exact target.  Its default run checks
the first uncertified boundary case `A=426`, `r=13`; larger ranges can be
selected explicitly before promoting any new range into a certificate packet.
The script uses Newton identities below rank `17` and determinant interpolation
from rank `17` upward, so it remains valid across the characteristic-17
threshold where Newton identities would divide by zero.

A stronger pivot-ready form is:

```text
For the same consecutive subgroup nodes, prove that the reciprocal spectra of
the kernels K_h have empty total intersection over the contiguous shifts needed
by the v10 regular gcd.
```

The current PR only uses `h=0,1`; the all-shift formula identifies the exact
small matrices that have to be compared if a later packet needs more shifts.
