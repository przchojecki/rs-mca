# F3 shift-pair control: h=3 rich-curve bridge guardrails

Status: PROVED local identities and arithmetic compilers, not `H3-ACT`.

This packet vendors three local guardrails from the prize F3 h=3 route.  They
support the primitive shift-pair ledger by pinning the algebraic objects that
future rank-capacity or rich-curve estimates must actually bound.

It does not prove the h=3 activation theorem, the C36/C36' premise, or any
rank-good minor avoidance statement.

## Cubic same-fiber hyperbola

Let

```text
F(T)=T^3+aT^2+bT+c,
G_F(u,v)=(F(u)-F(v))/(u-v)
       =u^2+uv+v^2+a(u+v)+b.
```

Assume a primitive cube root `omega` is available, with
`omega^2+omega+1=0`.  Put

```text
A=u-omega v,
B=u-omega^2 v,
alpha=(1+omega^2)/(omega^2-omega),
beta=1-alpha.
```

Then `alpha A + beta B = u+v` and `A B = u^2+uv+v^2`.  Defining

```text
X=A+a beta,
Y=B+a alpha,
Delta=a^2 alpha beta-b,
```

gives the exact identity

```text
G_F(u,v)=X Y-Delta.                              (HYP)
```

Thus same-fiber pairs of a cubic sit on a multiplicative hyperbola after the
displayed coordinate change.  The toral case `a=b=0` has `Delta=0`, namely
the two rational asymptote lines `u=omega v` and `u=omega^2 v`.

## Base-field degree-2 conic chart

The hyperbola form is useful conceptually, but the h=3 bridge can be expressed
over the actual row field without adjoining `omega`.

Let `K` have characteristic not `3`, and let

```text
G(u,v)=u^2+uv+v^2+a(u+v)+b.
```

Assume `(u0,v0)` lies on `G=0`.  Put

```text
A0=2u0+v0+a,
B0=u0+2v0+a,
Q(t)=t^2+t+1.
```

For `Q(t) != 0`, define

```text
S(t)=-(A0+B0 t)/Q(t),
U(t)=u0+S(t),
V(t)=v0+t S(t),
W(t)=-a-U(t)-V(t).
```

Then

```text
G(U(t),V(t))=0,
U(t)+V(t)+W(t)=-a,
U(t)V(t)+U(t)W(t)+V(t)W(t)=b.                  (CONIC)
```

Therefore `U,V,W` are a same-`(e1,e2)` triple.  After clearing the denominator
`Q(t)`, each membership map has numerator degree at most `2` and denominator
degree `2`.  The missing affine point is the projective `t=infinity` mate

```text
(u0, -a-u0-v0).
```

This is the local geometric reason the rich-curve route may work with
degree-2 rational maps.  The degenerate line cell `a^2=3b` remains separate.

## Chart count to pair count

For each repaired same-`(e1,e2)` chart `z`, let

```text
T_z = finite affine chart count with U_z(t),V_z(t),W_z(t) in H,
epsilon_z in {0,1} = projective/vertical point contribution,
R_z = T_z + epsilon_z = ordered same-fiber triple count.
```

Since ordered triples represent unordered triples with six orderings,

```text
N_z = R_z/6,
P_z = binom(N_z,2) = R_z(R_z-6)/72.             (PAIR)
```

Thus a linear bound on `sum_z T_z` alone is not enough to control activated
pairs.  If a future theorem supplies

```text
T_z <= M       for every z,
sum_z T_z <= S,
number of charts <= Z,
```

then

```text
P_total <= (M+1)(S+Z)/72.                       (MAX)
```

In particular, a normalized chart ledger satisfying `(M+1)(S+Z) <= 1152 n`
would give `P_total <= 16 n`.  The missing global ingredient is exactly a
max-fiber, level-set, or rank-capacity theorem that produces such `M,S,Z`.

## Replay

```bash
python3 experimental/scripts/verify_f3_h3_rich_curve_bridge_guardrails.py
```

Expected digest:

```text
F3_H3_RICH_CURVE_BRIDGE_GUARDRAILS_PASS
```
