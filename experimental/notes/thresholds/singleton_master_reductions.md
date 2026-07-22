# Singleton-MASTER reductions and source route cuts

## Status

```text
PROVED:
  exact insertion-position factorization;
  normalized-monotonicity sufficient criterion;
  exact terminal singleton coordinate;
  scalar upper-cap transfer lemma;
  first-insertion source positivity;
  exact counterexamples to two proposed source-entry facets.

OPEN:
  all-position single-insertion MASTER (SIM).

DOWNSTREAM STATUS:
  PDSP_2 remains open unconditionally.

LIVE K/M/L LEDGER IMPACT:
  zero.

NOT INCLUDED AS PROOF:
  sampled cone feasibility, partial commutator exactification, or finite-depth
  singleton-MASTER scans.
```

The purpose of this audit is to record the exact results obtained while trying
to prove singleton MASTER and to rule out two source-entry architectures that
cannot work. It does not promote the remaining computer searches to a theorem,
move a live KoalaBear or Mersenne-31 integer, or change a manuscript theorem
status.

### Proof authority

The ordinary all-depth MASTER input used in the source-positivity argument is
consumed from

```text
experimental/notes/thresholds/dense_shell_transfer_shape.md
experimental/data/certificates/dense-shell-transfer-shape/consumer_contract.json
```

The consumer contract fixes the transfer envelopes, child-share floor, and
master-margin floor. The older repair-era status prose in
`dense_shell_class_charges.md` is not used as proof authority; that note is
used only for the corrected class-charge interface.

The dependency chain is now:

```text
corrected source envelope (SE)
  + homogeneous preservation under the ordinary transfer T
  => normalized monotonicity for every D_{n,q}
  => all-position single-insertion MASTER (SIM)
  => conditional pair-decorated reduction
  => PDSP_2
  => the |U|=2 dense-shell class-sign law.
```

Only the algebraic reductions surrounding the first two arrows are proved
here.  The all-depth source envelope and homogeneous preservation remain the
next research target; the downstream `SIM => PDSP_2` implication belongs to
the companion pair-reduction packet.

## 1. Transfer operators

Use the flipped shifted-Chebyshev coordinates.  Let

\[
d(t)=a(t)-\frac12=-\frac12\cos(2\pi t),
\qquad
N_t=K+d(t)I,
\]

and define the ordinary transfer

\[
(\mathcal TF)(t)
=N_{t_+}F(t_+)+N_{t_-}F(t_-),
\qquad
t_\pm=\frac{1\pm t}{3}.
\tag{1.1}
\]

The first-insertion source operator is

\[
(\mathcal SF)(t)
=d(t_+)N_{t_+}F(t_+)
 +d(t_-)N_{t_-}F(t_-).
\tag{1.2}
\]

Write

\[
B_n=b(G_n^\varnothing),
\qquad
D_{n,q}=b(G_n^{\{q\}}).
\]

## 2. Exact elimination of the insertion position

### Theorem 2.1

For every `n>=q>=1`,

\[
\boxed{
D_{n,q}=\mathcal T^{q-1}\mathcal S B_{n-q}.
}
\tag{2.1}
\]

### Proof

At the insertion level, the decorated factor is precisely the drift
`d(t_\pm)` multiplying the usual child operator.  This is (1.2), giving
`D_{m+1,1}=\mathcal S B_m`.

Every level above that insertion is undecorated and applies the ordinary
transfer (1.1).  Moving the insertion from position one to position `q`
therefore adds exactly `q-1` ordinary ancestors, proving (2.1).  `QED`

This removes `q` as an independent induction parameter.  A proof may be
split into source inclusion for `\mathcal S B_m` and homogeneous preservation
under `\mathcal T`.

## 3. Normalized-monotonicity criterion

Put

\[
\alpha=\frac{2\pi}{3},
\qquad
\psi(t)=\cos(\alpha t),
\]

and define

\[
J_F=F'+\alpha\tan(\alpha t)F,
\qquad
H_F=F''+\alpha^2F.
\]

On `0<=t<=1/2`, `psi(t)>0`, and direct differentiation gives

\[
\boxed{
\left(\frac{F}{\psi}\right)'=\frac{J_F}{\psi}.
}
\tag{3.1}
\]

Also

\[
\boxed{J_F'=H_F+\alpha\tan(\alpha t)J_F.}
\tag{3.2}
\]

For an even profile, `J_F(0)=0`.  Hence the scalar integrating-factor
formula applied coordinatewise gives

\[
H_F\succeq0\Longrightarrow J_F\succeq0.
\tag{3.3}
\]

Now set

\[
t_{\rm out}=\frac5{12}+\frac\varepsilon3,
\qquad
t_{\rm in}=\frac14-\frac\varepsilon3,
\]

and

\[
\nu(\varepsilon)=
\frac{\sin(2\pi\varepsilon/3)}
     {\sin(\pi/3+2\pi\varepsilon/3)}.
\]

The exact scalar comparison is

\[
\frac{\psi(t_{\rm out})}{\psi(t_{\rm in})}
\ge\nu(\varepsilon),
\qquad 0\le\varepsilon\le\frac14.
\tag{3.4}
\]

This comparison has a short exact proof.  Put

\[
x=\frac{2\pi\varepsilon}{9}\in\left[0,\frac\pi{18}\right].
\]

Both denominators are positive, and the cross-product difference is

\[
\begin{aligned}
M(x)={}&
\cos\left(\frac{5\pi}{18}+x\right)
\sin\left(\frac\pi3+3x\right)
-
\cos\left(\frac\pi6-x\right)\sin(3x)\\
={}&
\sin\left(\frac{7\pi}{18}\right)
\cos\left(\frac{2\pi}{9}+4x\right)
-
\sin\left(\frac\pi{18}\right)
\cos\left(\frac\pi9+2x\right),
\end{aligned}
\tag{3.5}
\]

where the second line is product-to-sum.  On the stated interval,

\[
\cos\left(\frac{2\pi}{9}+4x\right)
\ge \cos\left(\frac{4\pi}{9}\right)
=\sin\left(\frac\pi{18}\right)
\]

and

\[
\cos\left(\frac\pi9+2x\right)\le\cos\left(\frac\pi9\right)
=\sin\left(\frac{7\pi}{18}\right).
\]

Thus \(M(x)\ge0\), proving (3.4).  The verifier independently checks the
literal parameter and endpoint conventions as a regression.

Combining (3.1) and (3.4) gives the exact sufficient chain

\[
\boxed{
H_F\succeq0
\Longrightarrow
J_F\succeq0
\Longrightarrow
F(t_{\rm out})\succeq\nu(\varepsilon)F(t_{\rm in}).
}
\tag{3.6}
\]

Thus singleton MASTER follows from an invariant Helmholtz or normalized
derivative cone, but this note does not prove that cone for all `D_{n,q}`.

## 4. Exact terminal singleton coordinate

Define

\[
\kappa_q=-\prod_{\ell=1}^q
\cos\left(\frac{2\pi}{3^\ell}\right)>0.
\]

### Theorem 4.1

For every `n>=q>=1`,

\[
\boxed{
(D_{n,q}(t))_n
=2^{-n}\kappa_q
\cos\left(\frac{2\pi t}{3^q}\right).
}
\tag{4.1}
\]

### Proof

Write `b_{m,m}(t)=(B_m(t))_m`. Only the raising part of `N_t` reaches a
new top coordinate. The exceptional raise from coordinate zero has coefficient
`1/2`, whereas every raise from a positive coordinate has coefficient `1/4`.
The ordinary top coordinate therefore satisfies

\[
b_{0,0}=1,
\qquad
b_{1,1}=\frac12b_{0,0}(t_+)+\frac12b_{0,0}(t_-)=1,
\]

and, for `m>=1`,

\[
b_{m+1,m+1}(t)
=\frac14b_{m,m}(t_+)+\frac14b_{m,m}(t_-).
\]

Induction gives the exact constant formula

\[
b_{m,m}=2^{1-m}\quad(m>=1).
\tag{4.2}
\]

There are now three cases.

For `n=q=1`, the source recurrence and the exceptional raise give

\[
\begin{aligned}
(D_{1,1}(t))_1
&=\frac12\bigl(d(t_+)+d(t_-)\bigr)\\
&=\frac12\kappa_1\cos\left(\frac{2\pi t}{3}\right)
=2^{-1}\kappa_1\cos\left(\frac{2\pi t}{3}\right),
\end{aligned}
\tag{4.3}
\]

where product-to-sum gives

\[
d(t_+)+d(t_-)
=-\cos\left(\frac{2\pi}{3}\right)
 \cos\left(\frac{2\pi t}{3}\right)
=\kappa_1\cos\left(\frac{2\pi t}{3}\right).
\]

For `n>1` and `q=1`, the source acts on `B_{n-1}` at a positive top
coordinate. Using the `1/4` raise and (4.2),

\[
\begin{aligned}
(D_{n,1}(t))_n
&=\frac14\,2^{2-n}\bigl(d(t_+)+d(t_-)\bigr)\\
&=2^{-n}\kappa_1\cos\left(\frac{2\pi t}{3}\right).
\end{aligned}
\tag{4.4}
\]

Finally let `q>1`. The exact recurrence is

\[
D_{n,q}(t)
=N_{t_+}D_{n-1,q-1}(t_+)
 +N_{t_-}D_{n-1,q-1}(t_-).
\]

The child top coordinate is positive-indexed, so the new top coordinate uses
the `1/4` raise. Applying the induction hypothesis and product-to-sum,

\[
\begin{aligned}
(D_{n,q}(t))_n
&=\frac14\,2^{-(n-1)}\kappa_{q-1}
\left[
\cos\left(\frac{2\pi t_+}{3^{q-1}}\right)
+\cos\left(\frac{2\pi t_-}{3^{q-1}}\right)
\right]\\
&=2^{-n}\kappa_{q-1}
\cos\left(\frac{2\pi}{3^q}\right)
\cos\left(\frac{2\pi t}{3^q}\right)\\
&=2^{-n}\kappa_q
\cos\left(\frac{2\pi t}{3^q}\right).
\end{aligned}
\tag{4.5}
\]

Here the last identity uses

\[
\kappa_q=\kappa_{q-1}\cos\left(\frac{2\pi}{3^q}\right)
\qquad(q>1).
\]

This proves (4.1), including the exceptional first raise. `QED`

In particular, the finite worst-case endpoint at `q=1` has exact ratio

\[
\frac{\cos(\pi/3)}{\cos(\pi/9)}
>\frac12.
\]

## 5. Scalar upper-cap transfer lemma

The following analytic lemma is independent of the coefficient coordinate.

Let

\[
p=\frac{1+t}{3},\qquad m=\frac{1-t}{3},
\]

\[
(Lf)(t)=f(p)+f(m),
\qquad
(Rf)(t)=d(p)f(p)+d(m)f(m),
\]

and `\mathcal H=\partial_t^2+\alpha^2`.

### Theorem 5.1

Suppose `f in C^2([0,1/2])`, `f'(0)=0`, and

\[
f\ge0,
\qquad
0\le\mathcal Hf\le6f.
\tag{5.1}
\]

Then

\[
\boxed{
6Rf-\mathcal H(Rf)
+\frac13\bigl(6Lf-\mathcal H(Lf)\bigr)\ge0.
}
\tag{5.2}
\]

### Proof

Put

\[
\kappa^2=6-\alpha^2.
\]

The upper and lower inequalities in (5.1), together with `f'(0)=0`, give

\[
f'(u)\le\kappa\tanh(\kappa u)f(u),
\tag{5.3}
\]

and, for `0<=u<=v<=1/2`,

\[
f(v)\ge
\frac{\cos(\alpha v)}{\cos(\alpha u)}f(u).
\tag{5.4}
\]

Equation (5.3) follows by differentiating

\[
f'\cosh(\kappa u)-\kappa f\sinh(\kappa u),
\]

and (5.4) follows by differentiating `f/\cos(\alpha u)`.

Let `h=6f-\mathcal Hf>=0`.  The contribution of a child `u` to the
left side of (5.2) is

\[
\begin{aligned}
&\left[
\frac{16}{9}-\frac{8\alpha^2}{27}
+\left(\frac{16}{3}+\frac{\alpha^2}{9}\right)d(u)
\right]f(u)\\
&\qquad
-\frac29d'(u)f'(u)
+\frac{1+3d(u)}{27}h(u).
\end{aligned}
\tag{5.5}
\]

On the child interval `[1/6,1/2]`, the final coefficient is at least
`1/108`.  Discard it and use (5.3).  The resulting lower bound is

\[
\Phi(p)f(p)+\Phi(m)f(m),
\tag{5.6}
\]

where

\[
\Phi(u)=a-b\cos(2\pi u)
-c\sin(2\pi u)\tanh(\kappa u),
\]

\[
a=\frac{16}{9}-\frac{32\pi^2}{243},
\qquad
b=\frac83+\frac{2\pi^2}{81},
\qquad
c=\frac{2\pi\kappa}{9}.
\]

Differentiation gives

\[
\begin{aligned}
\Phi'(u)
={}&\sin(2\pi u)
\left[2\pi b-c\kappa\operatorname{sech}^2(\kappa u)\right]\\
&-2\pi c\cos(2\pi u)\tanh(\kappa u).
\end{aligned}
\]

Using

\[
2\pi b-c\kappa
=\pi\left(4+\frac{\alpha^2}{3}\right)>0
\]

is not by itself enough to cover the whole interval; the signs must be split.
On `[1/4,1/2]`,

\[
\sin(2\pi u)\ge0,
\qquad
\cos(2\pi u)\le0,
\]

so both terms in `Phi'(u)` are nonnegative. On `[1/6,1/4]`,

\[
\sin(2\pi u)\ge\frac{\sqrt3}{2},
\quad
0\le\cos(2\pi u)\le\frac12,
\quad
\tanh(\kappa u)\le\kappa u\le\frac\kappa4.
\]

Therefore

\[
\begin{aligned}
\Phi'(u)
&\ge
\frac{\sqrt3\pi}{2}
\left(4+\frac{\alpha^2}{3}\right)
-\frac{\pi^2\kappa^2}{18}\\
&>10-\frac{10}{9}
=\frac{80}{9}>0,
\end{aligned}
\tag{5.7}
\]

where the last line uses

\[
\sqrt3>\frac53,
\quad
\pi>3,
\quad
\pi^2<10,
\quad
\kappa^2<2.
\]

Thus `Phi` is increasing on `[1/6,1/2]`.

For completeness, the endpoint margins follow from the same elementary
bounds

\[
3<\pi<\frac{22}{7},
\qquad
9<\pi^2<10,
\qquad
\frac53<\sqrt3<\frac74
\]

which imply

\[
0<\kappa^2<2,
\qquad
a>\frac{112}{243},
\qquad
b<\frac{236}{81}.
\tag{5.8}
\]

At `u=1/4`, `tanh x<x` gives

\[
\begin{aligned}
\Phi\left(\frac14\right)
&=a-c\tanh\left(\frac\kappa4\right)\\
&>a-\frac{c\kappa}{4}
=a-\frac{\pi\kappa^2}{18}\\
&>\frac{112}{243}-\frac{22}{63}
=\frac{190}{1701}>0.
\end{aligned}
\tag{5.9}
\]

At the coupled endpoints,

\[
\begin{aligned}
\Phi\left(\frac16\right)
&=a-\frac b2
-\frac{\sqrt3c}{2}\tanh\left(\frac\kappa6\right),\\
\Phi\left(\frac5{12}\right)
&=a+\frac{\sqrt3b}{2}
-\frac c2\tanh\left(\frac{5\kappa}{12}\right).
\end{aligned}
\]

Using `tanh x<x`,

\[
\begin{aligned}
\Phi\left(\frac16\right)
+\frac12\Phi\left(\frac5{12}\right)
>{}&\frac32a
+b\left(\frac{\sqrt3}{4}-\frac12\right)\\
&-\pi\kappa^2
\left(\frac{\sqrt3}{54}+\frac5{216}\right).
\end{aligned}
\tag{5.10}
\]

The rational estimates above give

\[
\frac32a>\frac{56}{81},
\qquad
b\left(\frac{\sqrt3}{4}-\frac12\right)>-\frac{59}{243},
\]

and

\[
\pi\kappa^2
\left(\frac{\sqrt3}{54}+\frac5{216}\right)<\frac{22}{63}.
\]

Hence

\[
\begin{aligned}
\Phi\left(\frac16\right)
+\frac12\Phi\left(\frac5{12}\right)
&>\frac{56}{81}-\frac{59}{243}-\frac{22}{63}\\
&=\frac{169}{1701}>0.
\end{aligned}
\tag{5.11}
\]

If `t<=1/4`, both children are at least `1/4`, so (5.9) and monotonicity
pay both terms in (5.6).  If `t>=1/4`, then `m>=1/6`, `p>=5/12`, and
(5.4) gives `f(p)>=f(m)/2`.  Equation (5.11) then pays (5.6).  This proves
(5.2).  `QED`

This is a preservation lemma.  Section 6 shows why it cannot be applied to
the singleton source at its creation level.

## 6. Exact source-entry counterexamples

Let

\[
U_m=\mathcal S B_m.
\]

For `m=0`, put `c=\cos(\alpha t)`.  Since `B_0=e_0`, direct evaluation gives

\[
\boxed{
U_0(t)=\frac{3-2c^2}{8}e_0+\frac c4e_1.
}
\tag{6.1}
\]

### 6.1 The cap-six source facet is false

At `t=0`,

\[
(U_0)_0=\frac18,
\qquad
(\mathcal HU_0)_0=\frac{5\pi^2}{18}.
\]

Therefore

\[
\left(6U_0-\mathcal HU_0\right)_0(0)
=\frac34-\frac{5\pi^2}{18}<0.
\tag{6.2}
\]

Thus `\mathcal HU_m<=6U_m` is not a valid uniform source-entry premise.

### 6.2 The shifted-Jacobi source facet is false

At `t=1/2`,

\[
U_0=\frac5{16}e_0+\frac18e_1,
\qquad
(KU_0)_0=\frac1{32}.
\]

Hence for `\lambda=241/500`,

\[
\left((K-\lambda I)U_0\right)_0
=-\frac{191}{1600}<0.
\tag{6.3}
\]

Indeed, `KU_0>=lambda U_0` fails for every `lambda>1/10`.

These are source counterexamples, not counterexamples to singleton MASTER.

## 7. First-insertion source positivity

Although the stronger source facets fail, positivity at the first insertion is
valid. This is not an invariant source-cone theorem.

### Theorem 7.1

For every `m>=0` and `0<=t<=1/2`,

\[
\boxed{U_m(t)=\mathcal S B_m(t)\succeq0.}
\tag{7.1}
\]

The low active coordinates are strict.

### Proof

Write

\[
p=\frac{1+t}{3},\qquad r=\frac{1-t}{3},
\qquad X=B_m(p),\quad Y=B_m(r).
\]

Then

\[
U_m=d(p)N_pX+d(r)N_rY.
\tag{7.2}
\]

For `t<=1/4`, both drifts and both child operators are nonnegative, so
(7.1) follows from ordinary cascade positivity.

For `t>1/4`, write `t=1/4+epsilon`.  The exact atom identity and ordinary
MASTER give

\[
d(r)=-\nu d(p),
\qquad
X\succeq\nu Y.
\]

Consequently

\[
\boxed{
U_m
=d(p)N_p(X-\nu Y)
 +\nu(1+\nu)d(p)^2Y
\succeq0.
}
\tag{7.3}
\]

Ordinary strict positivity gives the low-coordinate statement.  `QED`

## 8. Correct remaining source target

Define

\[
Y_m(u)=N_uB_m(u),
\]

\[
G_m(t)=Y_m(p)+Y_m(r)=B_{m+1}(t),
\qquad
C_m(t)=Y_m(p)-Y_m(r).
\]

With `c=cos(alpha t)` and `s=sin(alpha t)`, one has

\[
4U_m=cG_m+\sqrt3\,sC_m.
\tag{8.1}
\]

Writing `E_{m+1}=-G_m'`, exact differentiation gives

\[
4J_{U_m}
=-cE_{m+1}
 +\sqrt3\,sC_m'
 +\frac{\sqrt3\alpha}{c}C_m.
\tag{8.2}
\]

A sufficient source theorem is therefore

\[
\boxed{
C_m'\succeq\frac13Q_{m+1},
\qquad Q_{m+1}=-G_m''.
}
\tag{SE}
\]

It is equivalent to

\[
\left(Y_m''+9Y_m'\right)(p)
+\left(Y_m''+9Y_m'\right)(r)
\succeq0.
\tag{8.3}
\]

The attempts do not prove `(SE)` at every depth.  The displayed statement is
recorded as the corrected source target, not as a theorem.

## 9. Exact current boundary

By (2.1), proving `(SIM)` still requires:

1. a source-specific proof of normalized monotonicity for `\mathcal S B_m`;
2. a homogeneous invariant or finite-step recovery theorem under
   `\mathcal T`;
3. coverage of the full parameter continuum and every coefficient stencil.

The conditional interior commutator exactification and sampled cone searches
are useful discovery evidence, but they are deliberately excluded from this
proved packet.

## 10. Nonclaims

- This note does not prove `(SIM)` or unconditional `PDSP_2`.
- It does not prove `(SE)`.
- It does not prove invariance of a reflected state.
- It does not promote finite-depth or sampled Farkas checks to all-depth
  theorems.
- It does not prove positivity for three or more decorations, product-profile
  admission, a Sidon payment, or a lower-reserve payment.
