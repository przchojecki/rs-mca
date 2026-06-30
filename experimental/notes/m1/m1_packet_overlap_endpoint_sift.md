# M1 packet-overlap endpoint sift

**Status:** PROVED-LOCAL / AUDIT.

**Agent/model:** AllenGrahamHart / Codex.

**Date:** 2026-06-30.

This note extracts a compact combinatorial lemma from the old broad M1 packet
branch. It is meant to be used after quotient, tangent, fixed-root, and
endpoint-star charges have already been separated. The result does not prove
the M1 aperiodic local limit. It turns one residual sparse-packet obstruction
into an explicit disjoint-support pair-overlap target.

## Scope

The statement is local and finite. There is no field ledger beyond the finite
ambient packet universe: no generated-field, line-field, challenge-field, or
radius endpoint convention enters this lemma.

In the M1 residue-line program the intended use is: selected square-map packet
classes try to fit into a small bad-slope support. If the support is too small,
Cauchy forces packet overlaps. Endpoint-star pruning bounds the overlap which
can be blamed on shared endpoint supports. Any remaining overlap must come
from disjoint-support packet pairs, the next Kummer/cross-ratio target.

## Packet-overlap burden

Let `P_1,...,P_K` be finite packets in a universe `Omega`, each of size `s`,
and put

```text
B = |P_1 union ... union P_K|.
```

Let

```text
I(omega) = #{i : omega in P_i}.
```

Then

```text
sum_omega I(omega) = K s,
sum_omega I(omega)^2 = K s + 2 sum_{i<ell} |P_i cap P_ell|.
```

If `B <= R` and `K >= 2`, Cauchy's inequality gives

```text
sum_{i<ell} |P_i cap P_ell|
  >= K s (K s - R) / (2 R).                       (PO1)
```

Consequently some packet pair has overlap at least

```text
ceil_+( s(Ks-R) / (R(K-1)) ),                     (PO2)
```

where `ceil_+(x)=max(0,ceil(x))`.

Equivalently, if every packet pair has overlap at most `Lambda`, then

```text
B >= ceil( K s^2 / (s + (K-1)Lambda) ).           (PO3)
```

This is the basic reason a small-support residual cannot survive without a
large pair-overlap mechanism.

Proof: the two displayed identities for `I(omega)` are immediate by counting
incidences and ordered double incidences.  Cauchy's inequality gives

```text
(K s)^2 = (sum_omega I(omega))^2 <= B sum_omega I(omega)^2
        <= R (K s + 2 sum_{i<ell} |P_i cap P_ell|),
```

which rearranges to `(PO1)`.  Dividing by `binom(K,2)` gives `(PO2)`.
Conversely, if pair overlaps are bounded by `Lambda`, then

```text
sum_omega I(omega)^2 <= K s + K(K-1)Lambda,
```

and the same Cauchy inequality gives `(PO3)`.

## Endpoint-star sift

Now suppose each selected packet label has a two-point endpoint support
`E_i={a_i,b_i}`. Assume:

```text
at most h labels lie over any fixed endpoint support E,
at most D endpoint supports contain any fixed endpoint x.
```

Pairs lying over the same endpoint support are treated as different packet
classes on the same support and contribute zero packet overlap in this
residual branch. A label can share an endpoint with labels over at most
`2(D-1)` other endpoint supports, each carrying at most `h` labels. Hence the
number of unordered endpoint-sharing label pairs with different endpoint
supports is at most

```text
K h (D-1),
```

and their total packet-overlap mass is at most

```text
K h (D-1) s.                                      (ES1)
```

Combining `(PO1)` and `(ES1)`, the overlap mass forced onto disjoint-support
packet pairs is at least

```text
Omega_disj
 =
 K s (K s - R)/(2R) - K h (D-1)s.                 (ES2)
```

If `Omega_disj > 0`, then some disjoint-support packet pair has overlap at
least

```text
ceil( Omega_disj / binom(K,2) ).                  (ES3)
```

Thus endpoint-star pruning changes the residual target from arbitrary packet
overlap to disjoint-support packet overlap.

Equivalently, if every disjoint-support packet pair has overlap at most
`Lambda`, then

```text
B >= ceil(
  K s^2 / (s + 2h(D-1)s + (K-1)Lambda)
).                                                (ES4)
```

The endpoint-sharing channel has been paid explicitly by `D`; anything above
that budget is a genuine disjoint-support high-overlap target.

Proof: for each label and each of its two endpoints, there are at most `D-1`
other endpoint supports through that endpoint, with at most `h` labels on each.
This gives at most `2h(D-1)` ordered endpoint-sharing neighbors per label, or
`K h(D-1)` unordered pairs.  Each such pair has overlap at most `s`, proving
`(ES1)`.  Subtracting this endpoint-sharing budget from the total Cauchy burden
`(PO1)` gives `(ES2)`, and averaging over at most `binom(K,2)` disjoint-support
pairs gives `(ES3)`.  If disjoint-support overlaps are capped by `Lambda`, then

```text
sum_omega I(omega)^2
 <= K s + 2 K h(D-1)s + K(K-1)Lambda,
```

and Cauchy gives `(ES4)`.

## M1 use

In the language of `towards-prize.md`, this supports Work package C3 and the
C4.4 inverse-theorem route. It does not bound the aperiodic bad-slope set on
its own. Instead it gives a precise next proof obligation:

```text
After endpoint-star and quotient/tangent packet charges, prove that
disjoint-support square-map packet pairs cannot have the overlap demanded by
(ES3), except in quotient-periodic, subfield-confined, or low-template branches.
```

That is the intended Kummer/cross-ratio local-limit target.

## Verification

The companion verifier checks the exact Cauchy identities, pair-cap floors,
endpoint-sharing pair bound, and endpoint-sifted disjoint-overlap floor over
sampled finite set systems:

```sh
python3 experimental/scripts/verify_m1_packet_overlap_endpoint_sift.py
```
