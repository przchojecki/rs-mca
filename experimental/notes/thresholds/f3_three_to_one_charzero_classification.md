# F3 shift-pair control: three-to-one characteristic-zero classification

Status: PROVED exact characteristic-zero count and large-field transfer.

This packet records a proved branch for the F3/SP three-to-one object
appearing in the C36/C36' h=3 direct-floor route.  It does not close the
official polynomial-field corridor `p >= n^2`; it identifies the complete
characteristic-zero obstruction and gives a clean exponential large-field
transfer.

## Characteristic-zero statement

Let `n=2^s`, `s >= 3`, and let `mu_n` be the complex `n`th roots of unity.
The ordered relations

```text
(1-x)(1-y)(1-z)=1-w,
x,y,z,w in mu_n \ {1},                            (CZ1)
```

are exactly the permutations of

```text
(x,y,z)=(q,-q,-q^2),       w=q^4,                 (CZ2)
```

where `q in mu_n` has order at least `8`.  Consequently

```text
N_3to1^C(mu_n)=3(n-4).                            (CZ3)
```

## Valuation pattern

Put `zeta=zeta_n` and write a nonzero exponent as `a=2^r A`, with `A` odd.
In `Q(zeta)`, the unique prime above `2` satisfies

```text
v(1-zeta^a)=2^r.                                  (CZ4)
```

This is the standard quadratic-tower factorization of `1-zeta^(2^r)`;
multiplication of the exponent by an odd number is a Galois automorphism.

If `(CZ1)` has exponents `a,b,c,d`, equality of valuations says that a sum of
three powers of two is one power of two.  After permuting the inputs, the only
possibility is

```text
v_2(a)=v_2(b)=r,
v_2(c)=r+1,
v_2(d)=r+2.                                      (CZ5)
```

In particular `r <= s-3`.  Put `eta=zeta^(2^r)`, of order
`N=2^(s-r) >= 8`, and write

```text
x=eta^A, y=eta^B, z=eta^(2C), w=eta^(4D),
A,B,C,D odd.                                     (CZ6)
```

## Two quadratic separations

Expand `(CZ1)`.  In the quadratic extension

```text
Q(eta)=Q(eta^2) direct_sum eta*Q(eta^2),
```

the odd-exponent part is

```text
-eta^A-eta^B+eta^(A+2C)+eta^(B+2C)
  =(eta^(2C)-1)(eta^A+eta^B).
```

Since `eta^(2C) != 1`, separation gives

```text
B=A+N/2 (mod N),                 y=-x.           (CZ7)
```

After substituting `(CZ7)`, equation `(CZ1)` becomes, with
`theta=eta^2` of order `M=N/2`,

```text
(1-theta^A)(1-theta^C)=1-theta^(2D).             (CZ8)
```

Separate odd and even powers once more in

```text
Q(theta)=Q(theta^2) direct_sum theta*Q(theta^2).
```

The odd part gives `theta^A+theta^C=0`, and the even part then gives

```text
C=A+M/2 (mod M),
D=A       (mod M/2).                             (CZ9)
```

Equations `(CZ7)` and `(CZ9)` are exactly

```text
y=-x,       z=-x^2,       w=x^4.
```

Conversely `(1-q)(1+q)(1+q^2)=1-q^4`, so every displayed relation is valid.
There are `n-4` choices of `q` having order at least `8`; `q` and `-q` give
the same unordered input triple, and every triple has six orderings, proving
`(CZ3)`.

## Distinct-input norm bound

Suppose `p=1 (mod n)` and `H=mu_n(F_p)`.  Lift a finite-field relation to
the same exponents over `Q(zeta_n)` and put

```text
alpha=(1-zeta^a)(1-zeta^b)(1-zeta^c)-(1-zeta^d).
```

After cancellation of the two constant terms, the eight signed roots are

```text
xy, xz, yz, w, -x, -y, -z, -xyz.                (CZ10)
```

For pairwise distinct inputs, every root in `(CZ10)` has multiplicity at most
`3`.  Folding antipodal pairs and using Parseval over the `phi(n)=n/2` odd
Galois conjugates gives

```text
(2/n) sum_(j odd) |alpha(zeta -> zeta^j)|^2 <= 22.   (CZ11)
```

If the complex relation is false, `alpha` is a nonzero algebraic integer.
The finite relation puts `alpha` in a prime above `p`, hence `p | Norm(alpha)`.
Arithmetic-geometric mean yields

```text
0 < |Norm(alpha)| <= 22^(n/4).                  (CZ12)
```

## Signed-collision payment

The preceding bound improves after paying every equality among the eight
signed roots in `(CZ10)`.  The `binom(8,2)=28` pair labels collapse to `19`
distinct algebraic loci.  The pairs not involving `w` give the twelve
conditions

```text
x=y, x=z, y=z,
x=-1, y=-1, z=-1,
x=-yz, y=-xz, z=-xy,
xy=1, xz=1, yz=1.                               (CZ13)
```

The seven remaining loci are

```text
w=xy, w=xz, w=yz, w=-x, w=-y, w=-z, w=-xyz.     (CZ14)
```

Each locus in `(CZ13)` has at most `(n-1)^2` solutions, after which the main
relation forces `w`.  Six of the seven `w`-loci are also linear after choosing
an input variable not appearing in the paired root.  For the final locus
`w=-xyz`, the relation becomes

```text
(x+y-xy)+z(1-x-y+2xy)=0.                        (CZ15)
```

Unless the coefficient of `z` vanishes, `(x,y)` forces at most one `z`.  If
both the coefficient and constant vanish, then `xy=-1` and `x+y=-1`, giving at
most two ordered `(x,y)` pairs.  Hence the complete signed-root collision
locus has size at most

```text
C_coll <= 19(n-1)^2+2(n-1).                    (CZ16)
```

Off this locus the eight roots in `(CZ10)` are distinct, so the folded
Parseval mass is at most `8`, and a nonzero obstruction has

```text
0 < |Norm(alpha)| <= 8^(n/4).                   (CZ17)
```

Therefore

```text
p > 8^(n/4)
  => N_3to1((1-H)\{0})
       <= 19(n-1)^2+2(n-1)+3(n-4)
       = 19n^2-33n+5.                           (CZ18)
```

The right side satisfies the direct-floor `C36` inequality on every official
order.  Thus this large-field branch closes the h=3 three-to-one route when
`p > 8^(n/4)`, while leaving the hard official corridor `p >= n^2` open.

## Replay

```bash
python3 experimental/scripts/verify_f3_three_to_one_charzero_classification.py
```

Expected digest:

```text
H3_THREE_TO_ONE_CHARZERO_CLASSIFICATION_PASS rows=3 folded=22 collision_free=8 collision_loci=19
```
