# F3 shift-pair control: h=3 moment bookkeeping identity

Status: PROVED arithmetic identity, not an activation bound.

This packet isolates an exact h=3 second-moment identity for the primitive
shift-pair ledger.  It is useful as a guardrail: the ordered-triple moment is
not just `72*T_3` plus trivial terms.  A repeat-entry residue remains and must
be bounded or paid separately.

## Identity

Let `H` be a finite subgroup of a field of odd characteristic.  For an ordered
triple `x=(x_1,x_2,x_3) in H^3`, define

```text
sigma(x) = (x_1+x_2+x_3, x_1^2+x_2^2+x_3^2).
```

Since

```text
e_2 = ((sum x)^2 - sum x^2)/2,
```

equality of `sigma` is equivalent to equality of `(e_1,e_2)`.

Let

```text
M = #{(x,y) in H^3 x H^3 : sigma(x)=sigma(y)}.
```

Let `T_3` count unordered pairs `{A,B}` of disjoint three-element subsets of
`H` with equal `(e_1,e_2)`.  Then

```text
M = trivial + 72 T_3 + repeat_residue.           (M3)
```

The trivial term comes from identical multisets:

```text
trivial = 36 * binom(n,3) + 9 * n(n-1) + n.
```

Here `36=6^2` for three distinct entries, `9=3^2` for one repeated pair, and
`1` for a triple repeat.

The factor `72` is exact: a disjoint unordered pair of distinct-entry triples
has two side orderings and six orderings on each side, so it contributes

```text
2 * 6 * 6 = 72
```

ordered pairs to `M`.

The residual term is nonnegative and consists precisely of same-signature
ordered multiset-pairs with different underlying multisets where at least one
multiset has a repeated entry.

## Overlap guardrail

Distinct-entry multisets with equal signature cannot overlap unless they are
equal.  If two such triples share one element, the remaining two entries have
the same sum and product, hence are the same two-element multiset.  Therefore
the off-diagonal distinct-entry part of `M` is exactly the disjoint h=3 trade
count measured by `72*T_3`.

Consequently, any moment-form h=3 proof must either bound or separately pay
`repeat_residue`; it cannot silently identify `M-trivial` with `72*T_3`.

## Replay

```bash
python3 experimental/scripts/verify_f3_h3_moment_bookkeeping_identity.py
```

Expected digest:

```text
H3_MOMENT_BOOKKEEPING_IDENTITY_PASS
```
