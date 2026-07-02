# M1: displacement-uniform subgroup Hankel identities

- **Status:** PROVED algebra lemma + finite replay.
- **Agent/model:** Codex, acting autonomously for AllenGrahamHart.
- **Date:** 2026-07-02.
- **DAG target:** `displacement_uniform`.
- **Verifier:** `experimental/scripts/verify_m1_displacement_uniform.py`.
- **Artifact:** `experimental/data/certificates/m1-displacement-uniform/m1_displacement_uniform_certificate.json`.

## Statement

Let `H = <alpha>` be a finite multiplicative subgroup of a field `F`, and let
`V_m[x,r]=x^r` for `0<=r<m`.  For any word `w:H->F`, the rectangular syndrome
Hankel block satisfies

```text
H_{t,s}(w) = V_t(H)^T diag(w(x)) V_s(H).
```

In particular, if `X={x_0,...,x_{m-1}}` is a set of distinct nonzero points and

```text
A_h(X) = V_X^T diag(x^h : x in X) V_X,
```

then

```text
det A_h(X) = det(V_X)^2 prod_{x in X} x^h.
```

If `Y={y_0,...,y_{r-1}}` is another point set and

```text
B_h(Y)=V_Y^T diag(y^h : y in Y) V_Y,
```

then the finite-slope determinant polynomial has the rank-`r` reduction

```text
det(A_h(X)+Z B_h(Y))
 =
det(A_h(X)) det(I_r + Z diag(y^h) V_Y A_h(X)^{-1} V_Y^T).
```

This is just the matrix determinant lemma applied after the `V^T D V`
factorization.  Its nonvanishing hypotheses are explicit: the points of `X`
are distinct, nonzero, and `det(V_X) != 0`.

For the contiguous subgroup chart

```text
X_i = alpha^i,        0 <= i < m,
Y_a = alpha^{m+a},    0 <= a < r,
m+r <= ord(alpha),
```

define

```text
C[a,i] = 1 / (1 - alpha^(m+a-i)).
```

Then all Cauchy denominators are nonzero and

```text
C - U C V = 1_r 1_m^T,
U[a,a]=alpha^a,
V[i,i]=alpha^(m-i).
```

Moreover the Lagrange evaluation matrix `V_Y V_X^{-1}` factors as

```text
diag(P_X(Y_a)) C diag(-X_i^{-1}/P_X'(X_i)),
P_X(T)=prod_i (T-X_i).
```

Thus the Toeplitz-Cauchy displacement used in the spectral route is not a
separate assumption; it is the Lagrange interpolation matrix with its row and
column factors printed.

## Replay

The verifier checks the identities over three fields:

```text
F_13 with mu_4,
F_17 with mu_16,
F_49 with mu_16.
```

For each case it verifies:

```text
rectangular Hankel = V^T D V;
det A_h = det(V_X)^2 prod x^h for several shifts h;
det(A_h+zB_h)=det(A_h)det(I+zK_h) for every z in the field;
C-U C V is the all-ones matrix;
the Lagrange matrix factors through C.
```

Run:

```bash
python3 experimental/scripts/verify_m1_displacement_uniform.py --emit
python3 experimental/scripts/verify_m1_displacement_uniform.py
```

## Nonclaims

This packet does not prove spectral disjointness, the XR inverse theorem, Front
alpha, Front beta, or an M1 safe-side threshold.  It only turns the uniform
subgroup Hankel/displacement algebra into a small replayable lemma packet that
later spectral or exchange-rigidity arguments can cite.
