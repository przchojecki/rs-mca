# Sparse-direction mean-centered Gram profile

## Status

PROVED, field-general, exact finite arithmetic.

## Theorem

For equal-size `A`-blocks in an `n`-set with intersections at most `c`, put

```text
g=nc-A^2,
T=(n-A)^2-(n-1)g.
```

If `g>=0`, `2A^2>=nc`, and `T>0`, then mean-centering the incidence columns
gives

```text
L <= floor((n-1)n^2(A-c)/(A*T)).
```

The centered Gram matrix is PSD of rank at most `n-1`.  The square on its
off-diagonal interval lies below an endpoint chord with nonpositive slope;
PSD positivity and trace-rank give the formula.

For the sparse-direction deficit profile, use the Johnson cap where its
denominator is positive and the mean-centered cap afterward.  Since raw
caps need not be monotone, replace them by the proved suffix closure

```text
B_h=min_(h<=v<=e) C_v
```

before applying `floor(e/h)` owner weights.

## Exact walls

```text
KoalaBear:   e<=64047, profile 181731868;
Mersenne-31: e<=65454, profile  16101127.
```

The next KoalaBear endpoint has `T=-1499457466`.  The next Mersenne profile
is legal but equals `17120123`, over budget by `342908`.

The full-lift residual intervals become

```text
KoalaBear: 64048<=e<=1044238;
Mersenne:  65455<=e<=1044241.
```

## Audit

`experimental/verify_mca_sparse_direction_mean_centered_gram_profile_v1.py`
checks all 46 newly paid supports, both adjacent records, a finite block
control, and two hostile mutations.

## Nonclaims

No adjacent cell or official row is closed.  A negative denominator or an
over-budget upper bound is not an unsafe certificate.
