# Denominator-root puncture trivialization

Status: `PROVED_LOCAL_THEOREM / SELF_CONTAINED_PROOF / INDEPENDENT_REVIEW_REQUESTED`

This note continues the exact common-pole cancellation theorem in
`pole_tolerant_scalar_locator_localization.md`. It resolves the local semantic
gap left when cancellation makes a witness support simultaneously
explainable. It does not pay the denominator-root cell or prove the exception
routing input `(E)`.

## Setup

Use the notation and hypotheses of Theorem 2 in
`pole_tolerant_scalar_locator_localization.md`. Thus every live index has
`c_i != 0`, the common domain-pole set is

```text
P = {x in D : Q(x)=A(x)=B(x)=0},
t = |P|,
```

every exact support `S_i` contains `P`, and division by its squarefree locator
gives

```text
D'        = D \ P,
S_i'      = S_i \ P,
Q' h_i + c_i Lambda_i' = A' + gamma_i B'.            (C')
```

Assume the source degree profile

```text
deg Q <= m-k,  deg A,deg B <= m.
```

The original support `S_i` is support-wise MCA nontrivial.

## Theorem 1: cancellation dichotomy and pole-defect router

The live indices split canonically and disjointly into:

- `N`, where no degree-`<k` pair simultaneously explains `r0,r1` on `S_i'`;
- `T`, where such a pair exists.

Every index in `N` remains a support-wise MCA witness for the reduced
certificate, with its received line and slope unchanged. The cancellation
theorem makes `Q'` nonzero on the reduced coincidence core; it does not say
that `Q'` is root-free on all of `D'`.

For every `i in T`, there is a unique degree-`<k` pair `(p0_i,p1_i)`
simultaneously explaining `r0,r1` on `S_i'`, and

```text
h_i = p0_i + gamma_i p1_i                              (1)
```

as a polynomial identity. On the deleted pole set put

```text
u_i = (r0-p0_i)|_P,
v_i = (r1-p1_i)|_P.
```

Then

```text
u_i + gamma_i v_i = 0,
v_i != 0.                                              (2)
```

Thus the same slope is recovered from any pole coordinate where `v_i` is
nonzero. Distinct slopes have distinct ordered explaining pairs.

### Proof

Since `t<=deg Q<=m-k`,

```text
|S_i'|=m-t>=k.                                        (3)
```

The split is therefore exhaustive and disjoint by definition. The `N`
claim follows directly from (C') and the exact reduced locator supplied by
common-pole cancellation.

Fix `i in T`. Both `h_i` and `p0_i+gamma_i p1_i` agree with
`r0+gamma_i r1` on at least `k` distinct points of `S_i'`. Their difference
has degree less than `k`, proving (1). If a second pair explained `r0,r1` on
`S_i'`, each component difference would have degree less than `k` and at
least `k` roots. Hence the pair is unique.

On `P subset S_i`, equation (1) and the original support agreement give
(2). If `v_i` vanished on `P`, then (2) would make `u_i` vanish there as
well. The pair would simultaneously explain the received pair on
`S_i' union P=S_i`, contradicting original support-wise MCA nontriviality.
Thus `v_i` is nonzero and determines the slope.

If distinct slopes shared one ordered pair, their defect vectors would be
the same. Subtracting their two instances of (2) would force `v_i=0`, the
same contradiction. This proves pair injection.

## Theorem 2: reduced-support shadow packing

For distinct `i,j in T`,

```text
|S_i' intersect S_j'| <= k-1.                         (4)
```

Consequently, with `N=n-t` and `M=m-t`,

```text
|T| binom(M,k) <= binom(N,k),
|T| <= floor(binom(N,k)/binom(M,k)).                  (5)
```

### Proof

If two reduced supports met in at least `k` points, both unique first
components would interpolate `r0` there and hence coincide. The second
components would coincide for the same reason. This contradicts Theorem 1's
pair injection and proves (4). The `k`-shadows of the supports are therefore
disjoint, which proves (5).

## Quantified non-payment fence

The shadow theorem is structural but is not a row payment. Uniformly for
`0<=t<=m-k`,

```text
binom(N,k)/binom(M,k)
  = product_{j=0}^{k-1} (N-j)/(M-j)
  >= (N/M)^k
  >= (n/m)^k
  > (3/2)^k
  > 2^58.
```

The last comparison uses `k=1048576>100` and `3^100>2^158`. At both deployed
rows `n/m>3/2`. The KoalaBear budget is below `2^58`, and the Mersenne-31
budget is below `2^24`. Thus the support-shadow upper bound itself exceeds
both budgets throughout the complete pole-degree range. This does not show
that an over-budget family exists; it shows that support intersection alone
cannot certify `(E)` through this bound.

## Source compiler and remaining wall

Theorem 1 gives a chronology-preserving local subtype after the selected
denominator-root owner: reduced MCA witnesses stay in the reduced
core-regular certificate, while trivialized supports emit

```text
(P, gamma_i, p0_i, p1_i, u_i, v_i),
u_i=-gamma_i v_i,  v_i!=0.
```

No received-line owner or slope is changed. The remaining wall is a
row-sharp image or absorption theorem for these pole-defect records. It must
use the coupled divided identity

```text
Q'(p0_i+gamma_i p1_i)
 +(c0+c1 gamma_i)Lambda_i'
 = A'+gamma_i B'
```

across indices; another support-only packing argument does not address the
quantified gap.

## Nonclaims

- No bound on the actual cardinality of `T` below either deployed budget.
- No absorption into spread routing `(S)` or large-owner payment `(A)`.
- No complete exception routing `(E)`.
- No KoalaBear or Mersenne-31 adjacent-row closure.
- No official score movement.

The universal proof is the argument above. The companion verifier checks
source pins, exact deployed constants, finite-field defect and interpolation
seams, shadow disjointness, the exact non-payment fence, and hostile metadata
mutations.
