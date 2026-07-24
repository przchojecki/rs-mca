# M31 rank-seven combined-domain affine/Johnson endpoint v1

This packet proves one local Mersenne-31 LIST theorem.

After deleting a complete \(E_0\) projective line, every normalized-label
subclass becomes one ordinary rank-at-most-six Reed--Solomon list on

```text
(E0 minus S) disjoint-union Z(P)
```

with length `K+k`, dimension `k`, and agreement at least `k+w`.  Intersecting
the predecessor \(E_0\) cap with the unconditional affine-span cap and active
ordinary Johnson pays the complete cumulative rank-seven head through
`Q=29554`:

```text
head = 15,775,891
target = 15,775,932
margin = 41
```

The first unclosed head is exact:

```text
Q = 29,555
head = 15,776,139
excess = 207
surviving k = 4,981,...,4,986
```

A uniform combined-domain subclass cap `14,115,290` closes that next head;
`14,115,291` does not.  The generic affine-span cap is `14,115,528`, so the
localized missing improvement is `238`.

The packet does not:

- close global rank seven or treat rank at least eight;
- assign a v4 LIST atom or pay the signed `Xi_46` gate;
- prove the missing `14,115,290` source-incidence bound;
- assume aligned quotient supports;
- use a no-common-zero recurrence;
- move an official endpoint or close the row.

Replay:

```text
python3 experimental/scripts/verify_m31_rank7_combined_domain_affine_johnson_endpoint_v1.py --check
python3 -O experimental/scripts/verify_m31_rank7_combined_domain_affine_johnson_endpoint_v1.py --check
python3 experimental/scripts/verify_m31_rank7_combined_domain_affine_johnson_endpoint_v1.py --tamper-selftest
python3 -O experimental/scripts/verify_m31_rank7_combined_domain_affine_johnson_endpoint_v1.py --tamper-selftest
python3 experimental/scripts/verify_m31_rank7_combined_domain_affine_johnson_endpoint_v1_independent.py
/usr/local/bin/sage experimental/scripts/verify_m31_rank7_combined_domain_affine_johnson_endpoint_v1.sage
```

The primary verifier is fail-closed: strict JSON, a closed schema, canonical
payload sealing, source hashes, predecessor payload pins, exact array hashes,
hostile mutations, and the current Grande Finale provenance migration are all
checked.  The independent Python and Sage programs derive the endpoint
arithmetic without importing the primary verifier.
