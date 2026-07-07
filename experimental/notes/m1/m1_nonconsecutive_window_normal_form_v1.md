# M1 nonconsecutive coefficient-window normal form v1

Status: PROVED / STRUCTURAL NORMAL FORM.

This note proves a structural routing theorem for two-row coefficient windows

```text
W = {1,r},   3 <= r <= j.
```

It does not close the M1 ledger.  It removes these windows from the amorphous
unstructured bucket by routing every survivor to generated-field collision,
honest half-turn, recursive lower-core affine slice, or the named residual
branch

```text
PAIR-DEFICIENT-RESIDUAL-WINDOW.
```

That last branch is necessary and is not paid here.

No deployed budget is deducted by this packet.

The companion verifier is:

```bash
python3 experimental/scripts/verify_m1_nonconsecutive_window_normal_form_v1.py --check
```

## Setup

Let

```text
n = 2^m,
D = mu_n,
K = Q(zeta_n).
```

For a support `T subset D` with `|T|=j`, write

```text
Lambda_T(X)
  = prod_{x in T}(X-x)
  = X^j + C_1(T) X^{j-1} + ... + C_j(T).
```

A `{1,r}` row-slice survivor is a pair `(T,z)` satisfying

```text
C_1(T) + z = 0,
C_r(T) + z C_{r-1}(T) = 0.
```

Decompose `T` under the half-turn involution `x -> -x`:

```text
T = C disjoint-union R,
```

where `C` is a union of complete antipodal pairs and `R` contains at most one
element from each antipodal pair.  Write

```text
C = {+-a_1,...,+-a_q},
U = {a_1^2,...,a_q^2} subset mu_{n/2}.
```

Then

```text
Lambda_C(X) = B_U(X^2),
```

where

```text
B_U(Y) = prod_{u in U}(Y-u)
       = Y^q + b_1 Y^{q-1} + ... + b_q.
```

Also write

```text
Lambda_R(X)
  = X^s + d_1 X^{s-1} + ... + d_s,
```

with `b_0=d_0=1`, and `b_h,d_a` set to zero outside their natural ranges.

## Normal-Form Identity

Since

```text
Lambda_T(X)=B_U(X^2)Lambda_R(X),
```

the coefficient at deficit `a` from the top is

```text
C_a(T) = sum_{h=0}^{floor(a/2)} b_h d_{a-2h}.
```

The first row gives

```text
z = -d_1 = e_1(R).
```

Define

```text
theta_a(R) = d_a + z d_{a-1}.
```

Then

```text
theta_0=1,
theta_1=0.
```

The second row is exactly

```text
sum_{h=0}^{floor(r/2)} b_h theta_{r-2h}(R) = 0.    (*)
```

This is the normal form.

## Routing

### Generated-field finite-only collision

In a finite reduction

```text
red_p : Z[zeta_n] -> F_p,
zeta_n -> omega,
```

define the lifted defect

```text
G_r(T) = sum_h b_h theta_{r-2h}(R).
```

If a finite survivor has

```text
red_p(G_r(T)) = 0
```

but

```text
G_r(T) != 0 in Z[zeta_n],
```

then it is a generated-field collision.  For a printed row packet this is
charged to the existing row-indexed generated-slope cells.  No new deployed
budget is deducted in this note.

### Even windows

Let `r=2kappa`.  Then `(*)` has terminal term

```text
b_kappa theta_0 = b_kappa.
```

If the paired core is deep enough, `q>=kappa`, this solves for `b_kappa` as an
affine function of earlier lower-core coefficients:

```text
b_kappa =
-theta_{2kappa}
- b_1 theta_{2kappa-2}
- ...
- b_{kappa-1} theta_2.
```

So the survivor descends to a codimension-one affine split-locator slice on the
lower squared domain `mu_{n/2}`.

If `q<kappa`, the window is routed to

```text
PAIR-DEFICIENT-RESIDUAL-WINDOW(1,2kappa,q).
```

### Odd windows

Let `r=2kappa+1`.  Then the formal terminal term is

```text
b_kappa theta_1 = 0.
```

The active equation is

```text
theta_{2kappa+1}
+ b_1 theta_{2kappa-1}
+ ...
+ b_{kappa-1} theta_3
= 0.
```

If some exposed active residual coefficient is nonzero, the equation is a
nontrivial affine slice on the lower-core locator coefficients and descends to
the lower squared domain.

If the exposed chain is full and

```text
theta_3 = theta_5 = ... = theta_{2kappa+1} = 0,
```

then `theta_3=0`.  The `{1,3}` half-turn theorem applied to the residual `R`
gives `|R|<=1` over the honest cyclotomic model.  This is the known half-turn
pair-core branch.

If the paired core is too shallow to expose the chain down to `theta_3`, the
window is routed to

```text
PAIR-DEFICIENT-RESIDUAL-WINDOW(1,2kappa+1,q).
```

## Explicit Windows

For `W={1,5}`:

```text
theta_5 + b_1 theta_3 = 0.
```

If `q>=1` and `theta_3 != 0`, this is a lower-rung prefix-one core slice.  If
`theta_3=theta_5=0`, it is the half-turn branch.  If `q=0`, the residual
condition `theta_5=0` is pair-deficient.

For `W={1,6}`:

```text
theta_6 + b_1 theta_4 + b_2 theta_2 + b_3 = 0.
```

If `q>=3`, solve for `b_3`.  If `q<3`, route to pair-deficient residual.

For `W={1,7}`:

```text
theta_7 + b_1 theta_5 + b_2 theta_3 = 0.
```

If `q>=2` and `(theta_5,theta_3)` is nonzero, this is a lower-rung affine slice.
If `theta_3=theta_5=theta_7=0`, this is the half-turn branch.  The shallow cases
`q=0,1` are pair-deficient residual windows.

## Verifier Checks

The verifier checks:

- the symbolic normal-form templates for `r=3,...,10`;
- exact cyclotomic enumerations for small `2`-power domains;
- finite generated-collision splits for `F_17,n=16,j=5,W={1,3}` and `W={1,5}`.

The finite scans record:

```text
W={1,3}: 464 finite survivors = 336 honest lifts + 128 generated collisions.
W={1,5}: 448 finite survivors = 336 honest lifts + 112 generated collisions.
```

## Ledger Interpretation

The row-slice bucket should now be split as:

```text
generated_field_collision:
    PROVED image-cell route, paid only if included in the printed generated
    row packet.

honest_half_turn_odd_shadow:
    PROVED-LOCAL over Q(zeta_n), finite extras routed to generated-field.

recursive_lower_core_affine_slice:
    PROVED DESCENT / CONDITIONAL ON LOWER Q/BC/SP CERTIFICATE.

pair_deficient_residual_window:
    NAMED RESIDUAL / NEW OBSTRUCTION.
```

## Nonclaims

- This note does not pay pair-deficient residual windows.
- This note does not prove lower-rung Q/BC/SP constants.
- This note does not prove primitive Q-fin max-fiber flatness.
- This note does not cover arbitrary sparse Hankel row-slices without printed
  coefficient rows.
- This note does not prove extension-valued split-pencil safety.
