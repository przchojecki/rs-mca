# M1: Johnson exchange-mixing lemma for XR

- **Status:** PROVED combinatorial lemma + finite replay.
- **Agent/model:** Codex, acting autonomously for AllenGrahamHart.
- **Date:** 2026-07-02.
- **DAG target:** `averaged_xr`.
- **Verifier:** `experimental/scripts/verify_m1_johnson_exchange_mixing.py`.
- **Artifact:** `experimental/data/certificates/m1-johnson-exchange-mixing/m1_johnson_exchange_mixing_certificate.json`.

## Statement

Let `J(n,j)` be the Johnson graph on `j`-subsets of an `n`-point set.  Its
degree is

```text
d = j(n-j).
```

For a family `A` of vertices, write

```text
delta = |A| / binom(n,j)
```

and let

```text
E_1^J(A) = Pr[T_0 in A and T_1 in A],
```

where `T_0` is uniform on `J(n,j)` and `T_1` is obtained from `T_0` by one
random exchange.

Then

```text
E_1^J(A)
  <=
delta^2 + (1 - n/d) delta(1-delta).
```

Equivalently, conditional on starting inside `A`,

```text
Pr[T_1 in A | T_0 in A]
  <=
delta + (1 - n/d)(1-delta).
```

The point-dictator family

```text
A_x = {T : x in T}
```

attains equality.  In locator language this is the one-fixed-root/common-core
paid shape.

There is also a multi-exchange endpoint form.  Let `T_s` be the result after
`s` random exchanges and put

```text
lambda_* = max_{1 <= i <= min(j,n-j)} |theta_i| / d.
```

Then for every `s >= 0`,

```text
Pr[T_0 in A and T_s in A]
  <=
delta^2 + lambda_*^s delta(1-delta).
```

For the point-dictator family `A_x`, the exact endpoint value is the signed
first-eigenspace formula

```text
Pr[T_0 in A_x and T_s in A_x]
 =
delta^2 + (theta_1/d)^s delta(1-delta),
        delta = j/n.
```

## Proof

Let `P` be the normalized adjacency operator of `J(n,j)` and let `1_A` be the
indicator of `A`, with inner product normalized by the uniform measure on
vertices.  Put

```text
f = 1_A - delta.
```

Then

```text
E_1^J(A) = <1_A, P 1_A> = delta^2 + <f, P f>.
```

The Johnson graph eigenvalues are

```text
theta_i = (j-i)(n-j-i)-i,        0 <= i <= j,
```

with top eigenvalue `theta_0=d`.  Therefore

```text
theta_0 - theta_1 = n,
theta_1 / theta_0 = 1 - n/d.
```

On the mean-zero subspace, `P` has largest eigenvalue `theta_1/theta_0`, so

```text
<f,Pf> <= (theta_1/theta_0) <f,f>
        = (1 - n/d) delta(1-delta).
```

This proves the displayed bound.

For the endpoint form, decompose the same indicator as `1_A=delta+f`.  Since
`P` is self-adjoint and every nonconstant eigenspace has normalized eigenvalue
of absolute value at most `lambda_*`,

```text
Pr[T_0 in A and T_s in A]
 =
<1_A, P^s 1_A>
 =
delta^2 + <f, P^s f>
 <=
delta^2 + lambda_*^s ||f||_2^2
 =
delta^2 + lambda_*^s delta(1-delta).
```

For equality, take `A=A_x`.  Its density is `delta=j/n`.  Starting from a set
containing `x`, a one-exchange move remains in `A_x` exactly when the removed
point is not `x`, which has probability `(j-1)/j`.  Thus

```text
E_1^J(A_x) = (j/n)((j-1)/j) = (j-1)/n,
```

which is exactly the bound above after substituting `delta=j/n` and
`d=j(n-j)`.

The centered indicator `1_{A_x}-j/n` lies in the first nonconstant Johnson
eigenspace, so the signed endpoint formula follows by applying `P^s` on that
eigenspace.

## XR consequence

For the XR route, the aligned-locator set

```text
A_{u,v} = {T : H_u ell_T is parallel to H_v ell_T}
```

lives on the same Johnson graph.  This lemma says that high one-exchange
energy is already constrained by the spectral gap, and the first equality
model is a paid common-root shape.  The inverse theorem remains open: one
still has to classify near-extremal or higher-mode high-energy families after
paid quotient and tangent strata are removed.  The point of this packet is to
make the support-side spectral inequality exact and reusable before attacking
that inverse step.

The endpoint form is the version to use for multi-exchange tests where only
the start and end locators are required to be aligned.  It is deliberately not
an all-intermediate or killed-walk estimate for

```text
Pr[T_0,T_1,...,T_s all lie in A].
```

That stronger survival quantity needs a separate restricted-operator argument.

## Replay

The verifier checks:

```text
theta_0-theta_1=n for small and deployed-shape rows;
all 2^15 families of J(6,2);
endpoint mixing for all J(6,2) families and s=0..4;
point-dictator equality;
point-dictator signed endpoint formula for s=0..5;
fixed two-root core, balanced block-profile, and frozen full-block examples;
48 seeded random families in J(8,3) and J(10,4).
```

Run:

```bash
python3 experimental/scripts/verify_m1_johnson_exchange_mixing.py --emit
python3 experimental/scripts/verify_m1_johnson_exchange_mixing.py
```

## Nonclaims

This does not prove the XR inverse theorem, classify every high-energy family,
bound killed-walk/all-intermediate exchange energy, enumerate Reed-Solomon word
pairs, or prove an M1 safe-side threshold.
