# W-A: star-PTE canonical-trade normal form

- **DAG node:** `u1_pte_trade_compression`.
- **Task:** W-A.
- **Status:** PROVED.
- **Provenance:** X-5, restated as an upstream write-up packet.
- **Verifier:** `experimental/scripts/verify_w_a_star_pte_lemma.py`.
- **Certificate:**
  `experimental/data/certificates/w-a-star-pte-lemma/w_a_star_pte_lemma.json`.

## Critical-path role

This is a proof-spine packet for the conditional prize route.  The terminal
post-strip residue is expressed in same-top locator families before it is
charged by the pullback/PTE dictionary.  This lemma proves that those families
have no hidden cancellation: relative to a fixed base, every target support is
a unique common-core extension of a residual PTE trade.

The packet does not prove the bounded pullback compression theorem.  Its role
is to reduce the terminal `active_core_count_bound` / PTE residue to canonical
trade currency, so the later dictionary and compiler packets count the right
object.

## Statement

Let `S0` and `S1` be two locator supports of the same size `A`, and suppose
their locator polynomials have the same top `t` coefficients:

```text
e_r(S0) = e_r(S1),       1 <= r <= t.
```

Write the canonical decomposition

```text
C = S0 cap S1,       Q = S0 \ C,       P = S1 \ C.
```

Then `P` and `Q` are disjoint, have the same size, and form a PTE trade through
level `t`:

```text
e_r(P) = e_r(Q),       1 <= r <= t
```

with the convention that `e_r` is zero above the support size.  Conversely, if
`P` and `Q` are disjoint equal-size supports satisfying those identities, then
`C union P` and `C union Q` have the same top `t` locator coefficients.

Thus every same-top family, viewed from any fixed base locator, decomposes into
canonical star trades `(P,Q)` around the common core `C`.  The decomposition is
unique for each target support because `C`, `P`, and `Q` are set-theoretically
determined by the base and target.

## Proof

Top locator coefficients are elementary symmetric sums, up to the harmless
sign `(-1)^r`, so the hypothesis is

```text
e_r(C union P) = e_r(C union Q),       1 <= r <= t.
```

For every `r`,

```text
e_r(C union P) - e_r(C union Q)
  = sum_{i=0}^r e_i(C) ( e_{r-i}(P) - e_{r-i}(Q) ).
```

Induct on `r`.  The terms with `r-i < r` vanish by the previous induction
steps, and the remaining term has coefficient `e_0(C)=1`, so
`e_r(P)-e_r(Q)=0`.  This proves the forward implication.  The converse is the
same convolution identity in the other direction.

The support bookkeeping is immediate: `P` and `Q` are disjoint, and
`|P|=|Q|` because `|S0|=|S1|` and the same common core `C` was removed from
both.  This is the X-5 "star-PTE" point: no non-PTE cancellation is hiding in a
same-top family.  What remains for U1 is the compression theorem, namely that
the resulting PTE trades are explained by a bounded pullback dictionary rather
than by arbitrary unstructured trades.

## Toy Replay

The verifier enumerates same-top locator families on four small multiplicative
rows and checks the canonical decomposition pair-by-pair:

```text
F17/mu8,   A=4, t=3
F13/mu12,  A=5, t=3
F17/mu16,  A=6, t=3
F97/mu16,  A=8, t=3
```

For every enumerated pair it recomputes:

```text
S0, S1 same top-t
  <=>  (S1 \ (S0 cap S1), S0 \ (S0 cap S1)) is a star-PTE trade
```

and records family sizes and pair counts in the certificate.

## Verification

Run:

```bash
python3 experimental/scripts/verify_w_a_star_pte_lemma.py
```

To refresh the certificate:

```bash
python3 experimental/scripts/verify_w_a_star_pte_lemma.py --write-certificate
```
