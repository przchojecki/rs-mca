# Census Bounded Scales

Status: PROVED.

Source DAG node: `census_bounded_scales`.

## Statement

At an agreement `A`, write `t = A-k` and `j = n-A`. For a rate-preserving
dyadic quotient scale `M | gcd(n,k)`, let `N' = n/M`. A quotient-invariant
co-support of size `j` descends to a quotient co-support of size

```text
l' = j/M = (j/n) N'.
```

Thus the quotient class ratio `l'/N' = j/n` is forced by the row and agreement,
independent of the ambient length `n`. The count at scale `N'` is the exact
binomial

```text
Q(N') = binom(N', l').
```

On the corridor, entropy bounds make `Q(N')` strictly grow with `N'` and create
large dyadic staircase gaps. Therefore at most one admissible dyadic scale can
be the deciding scale near the budget, and the current corridor rows see only
bounded quotient scales. This makes the census symbolic and row-length
uniform.

## Proof

The quotient map from `mu_n` to `mu_{N'}` has fibers of size `M`. A
quotient-invariant co-support `T` of size `j` is a union of these fibers, so its
image has size `l' = j/M`. Since `N' = n/M`, this gives `l'/N' = j/n`.

For fixed ratio `p = j/n`, Stirling's entropy bounds give

```text
log2 binom(N', p N') = N' H(p) + O(log N').
```

In the corridor, `H(p)` is bounded below by an absolute positive constant, and
on the clean rows it is near one. Passing from one admissible dyadic scale to
the next roughly doubles the entropy exponent, creating a large bit gap. Hence
there is at most one scale whose exact binomial count can lie near the budget
within a bounded staircase step.

The verifier checks this mechanism on the recorded clean-rate corridor rows,
including the `n=2^10` versus `n=2^41` invariance examples. The deciding scale,
forced quotient ratio, and exact count are independent of the ambient length in
those paired rows.

## Non-Claims

This packet proves the structural bounded-scale and uniqueness reduction. It
does not by itself decide the pointwise safe or unsafe row inequalities, and it
does not replace exact counting at the deciding scale.

## Replay

```bash
python3 experimental/scripts/verify_census_bounded_scales.py --emit
python3 experimental/scripts/verify_census_bounded_scales.py \
  --check experimental/data/certificates/census-bounded-scales/census_bounded_scales.json
```
