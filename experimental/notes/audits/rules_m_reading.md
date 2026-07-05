# Rules M-Reading

- **Status:** PROVED / citation reframe.
- **DAG node:** `rules_m_reading`.
- **Certificate:** `experimental/data/certificates/rules-m-reading/rules_m_reading.json`.
- **Verifier:** `python3 experimental/scripts/verify_rules_m_reading.py --check experimental/data/certificates/rules-m-reading/rules_m_reading.json`.

This packet records the list-side interpretation of the constant interleaving
arity `m`.  The grand list decoding challenge is read as a family of
determinations, one for each fixed constant `m`, not as a single finite
calculation that must cover all constants at once.

## Claim

For each admissible Reed-Solomon code `C` and each declared constant `m`, a
packet may determine the corresponding list threshold for `C^{==m}`.  Such a
per-`m` determination is a valid prize object and a valid partial result.

The full arbitrary-constant-`m` family still requires a uniform-in-`m` theorem
or an equivalent large-`m` route.  This is why `a_regularity_forcing`-type
material remains relevant even when small fixed-`m` cases are closed.

## Citation Pin

The certificate pins the source to ABF26 / IACR ePrint 2026/680, page 5, with
PDF sha256:

```text
426a979c13cc61db0f2cdb909067ef4c9f24438859fe0a7a337d2b19b07fcaa5
```

The decisive page-5 fragments are:

```text
and a constant m
for a code C, an m, and an eps*
```

Together these fix the quantifier shape used by this packet: the object is
indexed by a constant `m` supplied as part of the instance.

## Consequence For The DAG

List-side packets should state their `m` scope explicitly:

```text
fixed-m packet: determines the row for its declared constant m
small-m batch: gives genuine partial coverage for the listed constants
uniform-m packet: required for the full arbitrary-constant family
```

This supports the existing split between small-`m` worst-case routes and
large-`m` regularity routes.

## Non-Claims

- This packet does not prove all constant `m` cases at once.
- This packet does not provide the large-`m` regularity theorem.
- This packet does not change Papers A-D; it is an experimental audit note for
  list-side quantifier bookkeeping.
