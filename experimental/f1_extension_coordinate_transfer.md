# F1 Extension-Coordinate Transfer

## Claim

Let `B subset F` be finite fields with extension degree `e`, let
`D subset B`, and let

```text
C_B = RS[B,D,k],        C_F = RS[F,D,k].
```

Fix a `B`-basis `omega_1,...,omega_e` of `F`. For a word `u:D->F`, write

```text
u(x) = sum_i u_i(x) omega_i,        u_i:D->B,
```

and set

```text
Phi(u) = (u_1,...,u_e) in (B^D)^e.
```

For `z in F`, let `M_z in Mat_e(B)` be the matrix of multiplication by `z`
in this basis, acting pointwise on coordinate words.

Then `Phi` gives an exact support-wise MCA transfer:

```text
Phi(C_F) = C_B^e.
```

For every `f,g in F^D`, every `z in F`, and every support `S subset D`,

```text
(f+zg)|_S in C_F|_S
```

if and only if

```text
(Phi(f) + M_z Phi(g))|_S in (C_B^e)|_S.
```

Moreover, `f` and `g` are simultaneously explained by `C_F` on `S` if and
only if `Phi(f)` and `Phi(g)` are simultaneously explained coordinatewise by
`C_B^e` on `S`.

Consequently, the support-wise MCA-bad slopes of the `F`-line

```text
f + z g,        z in F,
```

are exactly the bad parameters of the multiplication-slice affine family

```text
Phi(f) + M_z Phi(g),        z in F,
```

inside the `e`-interleaved base code `C_B^e`. Thus extension-line MCA is not
scalar base-field MCA; it is a structured matrix-parameter MCA problem over
the base field.

## Status

PROVED.

This is an exact change of coordinates, not a positive local-limit theorem.
It identifies the correct base-field object that would replace the
unrestricted extension-line lift assumption.

## Existing Paper Dependency

This addresses `tex/proximity_blueprint_v3.tex` `prob:F1`, especially the
suggested attack of expressing `C_F` as an extension code of `C_B` and
comparing `F`-lines with interleaved `B`-lines.

It is the MCA-side analogue of the list-side extension identity
`tex/snarks_v4.tex` `eq:extension-list`, but with a crucial difference: the
line parameter `z in F` becomes the multiplication matrix `M_z`, not a scalar
base-field parameter.

## Proof

First prove `Phi(C_F)=C_B^e`. If `P in F[X]` has degree `< k`, write its
coefficients in the chosen basis:

```text
P(X) = sum_i P_i(X) omega_i,        P_i in B[X],        deg P_i < k.
```

Since every evaluation point of `D` lies in `B`, the coordinate expansion of
`P|_D` is exactly `(P_1|_D,...,P_e|_D)`, which lies in `C_B^e`. Conversely,
given any coordinate tuple `(P_1|_D,...,P_e|_D)` with `deg P_i<k`, the
polynomial `sum_i P_i omega_i in F[X]` has degree `< k` and evaluates to the
corresponding `F`-word. This proves the code identity.

The line identity follows from `B`-linearity of coordinate expansion. For each
`x in D`,

```text
Phi(f(x)+z g(x)) = Phi(f(x)) + M_z Phi(g(x)).
```

Thus `f+zg` agrees on `S` with some degree-`<k` polynomial over `F` if and
only if its coordinate tuple agrees on `S` with `e` degree-`<k` polynomials
over `B`, which is precisely membership in `(C_B^e)|_S`.

The simultaneous-explanation statement is the same argument applied to two
words at once. If `A,G in F[X]` of degree `< k` explain `f,g` on `S`, then
their coordinate polynomials explain `Phi(f),Phi(g)` coordinatewise on `S`.
Conversely, coordinatewise explanations assemble to the two polynomials

```text
A = sum_i A_i omega_i,        G = sum_i G_i omega_i
```

of degree `< k` over `F`. Therefore containment and noncontainment are
preserved exactly, and so is the set of support-wise bad slopes.

## Ledger Impact

This theorem gives a precise replacement interface for the failed
same-numerator extension lift. A protocol cannot cite scalar MCA of `C_B` and
then divide by `|F|`; it must either prove an extension-line theorem over `F`
or prove a bound for the multiplication-slice family

```text
Phi(f) + M_z Phi(g),        z in F,
```

inside the `e`-interleaved base code.

The theorem also explains why the extension list ledger and the extension MCA
ledger differ. Lists see the whole product code `C_B^e`; lines see only the
structured `B`-linear subalgebra `{M_z : z in F}` inside `Mat_e(B)`.

## Next Step

For `e=2`, classify rich multiplication-slice supports for the two-dimensional
matrix algebra `{a I + b M_alpha : a,b in B}`. This is the smallest
coordinate form of genuinely extension-valued F1 bad slopes and is the natural
bridge to the balanced residue-cloud problem.
