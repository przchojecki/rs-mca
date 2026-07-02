# Towards-Prize v2 Residual Reduction Audit

- **Status:** AUDIT / proof-logic review.
- **Source:** `tex/towards-prize.tex` v2, `thm:p2-residual-reduction`,
  `prop:p2-half-sharp`, and `thm:mca-excess-pair-list`.
- **Scope:** Checks the internal proof logic and edge cases.  This note does
  not reprove any external theorem and does not edit the TeX.

## Shortening-Image Reduction

The statement is:

```text
emca(C,delta) <= max( eca(C,delta), (r + R_C(r))/q )
```

where `r=floor(delta n)`.  For Reed-Solomon codes, every nonzero residual
codeword counted by `R_C(r)` lies in a shortening of dimension at most
`max(0,2r-(n-k))`.

The proof splits into the two correct cases.

1. If `(f1,f2)` is `delta`-far from `C^2`, then every MCA-bad slope is CA-bad by
   the chain lemma.  This contributes at most `q*eca(C,delta)` slopes.

2. If `(f1,f2)` is close, choose an explanation `(p1,p2)` with error set
   `E`, `|E|<=r`, and write `e_i=f_i-p_i`.  Tangent slopes satisfy
   `e1(x)+gamma e2(x)=0` for some `x in E`, so there are at most `|E|<=r` finite
   tangent slopes.

For a non-tangent MCA-bad slope with witness `(c,S)`, set `F0=D\S` and
`d=c-(p1+gamma p2)`.  Then `|F0|<=r`, `supp(d) subset E union F0`, and on
`E\F0` one has `d=e1+gamma e2`.  If `d=0`, non-tangency forces `E cap S` to be
empty, so `S subset D\E` and `(p1,p2)` mutually explains the witness, a
contradiction.  Thus every non-tangent bad slope is counted by `R_C(r)`.

For Reed-Solomon codes, the support is contained in a set of size at most
`2r`.  An MDS shortening on a set `W` has dimension `max(0, |W|-(n-k))`, hence
the displayed `max(0,2r-(n-k))` bound follows.  No edge-case discrepancy was
found: when `2r<=n-k`, the shortening dimension is zero and the theorem
recovers the half-distance reduction.

## Sharpness of the Half-Distance Wall

The construction assumes

```text
max(2, ceil(d/2)) <= r <= d-2,
```

with `d=n-k+1`.  Choose disjoint `E,F0` with `|E|=r`, `|F0|=d-r`, and
`W=E union F0`, so `|W|=d`.  For Reed-Solomon codes,

```text
prod_{x in D\W}(X-x)
```

has degree `n-d=k-1` and is nonzero exactly on `W`, so it supplies the required
minimum-support codeword `c`.

Let `S=D\F0`; then `|S|=n-d+r>=n-r` is equivalent to `2r>=d`, which is one of
the hypotheses.  Defining `f1=c` on `E` and zero off `E`, and choosing `f2`
supported on `E` but not scalar-proportional to `c|_E`, gives a pair that is
`r/n`-close to `(0,0)`.  At slope `0`, `f1` agrees with `c` on `S`, but a mutual
explanation would force the second codeword into the one-dimensional shortening
on `W`, contradicting the choice of `f2`.  Since `c` is nonzero on every point
of `E`, the slope is non-tangent relative to `(0,0)`.

No issue was found in the range conditions: `|E|>=2` is exactly what is needed
to choose `f2` not proportional to `c|_E`, and `r<=d-2` leaves `F0` nonempty
without being used in a way that weakens the witness.

## Doubled-Radius Pair-List Reduction

The statement is:

```text
emca(C,delta) <= max( eca(C,delta),
                      (1 + (r+1) L_{2r}^{(2)}(C))/q )
```

Again, the far case reduces to CA-bad slopes.  In the close case, choose one
MCA-bad anchor slope `gamma0`.  For every other bad slope `gamma`, the two
line equations on `S0 cap S_gamma` solve to a pair

```text
p2 = (c_gamma-c0)/(gamma-gamma0),
p1 = (gamma c0 - gamma0 c_gamma)/(gamma-gamma0),
```

which agrees with `(f1,f2)` on at least `n-2r` coordinates.  Hence it lies in
the doubled-radius pair list.

The multiplicity bound for a fixed pair `P=(p1,p2)` is also sound.  Let

```text
E_P={x : (f1(x),f2(x)) != (p1(x),p2(x))},  t=|E_P|<=2r.
```

Inside `E_P`, each finite slope can vanish only on coordinates assigned to that
slope, and distinct slopes have disjoint vanishing coordinate sets.  If `t<=r`,
any non-extending witness must use at least one such coordinate, giving at most
`t<=r` slopes.  If `r<t<=2r`, a witness of size at least `n-r` must use at least
`t-r` coordinates in `E_P`, giving at most `t/(t-r)<=r+1` slopes.  Adding back
the anchor gives the displayed `1+(r+1)L_{2r}^{(2)}` bound.

No logical gap was found in this proof.  The reduction is deliberately a
residual formulation rather than a small bound: its value is that the remaining
mutual-only layer is now an explicit pair-list or shortening-image object.

## Follow-Up

The next useful audit step is not another constants check.  It is to connect
these residual objects to concrete row packets: for a candidate row and radius,
either bound `R_C(r)` / `L_{2r}^{(2)}(C)` or exhibit a minimal residual witness.
