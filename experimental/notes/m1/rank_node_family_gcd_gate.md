# Rank-Node Family GCD Gate

**Status:** PROVED / AUDIT for the finite toy replay.

**Agent/model:** AllenGrahamHart / Codex.

**Date:** 2026-06-30.

This note records a small strengthening of the regular-minor extractor.  It
combines the rank-at-nodes gate with the common-gcd gate.

Fix an exact agreement bucket with

```text
j = n-A,
t = A-k,
s = j+1,
t >= s.
```

For a syndrome pencil

```text
M(Z)=H_{t,j}(u)+Z H_{t,j}(v),
```

choose deterministic finite nodes `z_0,z_1,...`.  At each node where
`M(z_i)` has full column rank, Gaussian elimination supplies a maximal row set
`R_i` such that

```text
Delta_{R_i}(z_i) != 0.
```

Hence `Delta_{R_i}(Z)` is not the zero polynomial.  Let `G(Z)` be the gcd of
the nonzero determinants from the distinct witnessed row sets.

If a finite slope `z` is regular-bad, then `M(z)` has rank at most `j`.  Every
maximal minor vanishes at `z`, in particular every witnessed
`Delta_{R_i}(z)` vanishes.  Therefore

```text
regular-bad finite slopes are contained in {G=0}.
```

The first `s+1=j+2` deterministic nodes retain the singularity proof from the
rank-at-nodes lemma: if all those specializations have rank at most `j`, then
every maximal minor of degree at most `s` vanishes identically.  Extra scanned
nodes do not strengthen the singular proof; they only add witnessed row sets
that can sharpen the gcd.

The replay packet is:

```text
experimental/data/hankel-regular-minor-inputs/f17_n16_k8_a13_rank_node_gcd_toy.json
experimental/data/certificates/regular-minor-gcd-rank-node-family-toy/
```

It uses the same `F_17`, `n=16`, `k=8` syndrome pencil as the contiguous gcd
toy, but selects row sets through deterministic rank-node witnesses.  With
`node_limit=17`, the packet gets the same finite root union `{11}` as the
contiguous-family gcd replay while auditing fewer row sets:

```text
A=13: 1 row set, gcd roots {11}
A=14: 2 row sets, gcd roots {11}
A=15: 3 row sets, gcd roots empty
A=16: 2 row sets, gcd roots empty
```

The checker verifies that every recorded witness node belongs to the tested
deterministic node prefix, that every gcd row set is witnessed, and that the
recorded minor polynomial is nonzero at its witness node.  The negative
fixtures corrupt a witness row set and a witness node value; both must fail.

Non-claims: this is a finite toy replay and extractor theorem.  It is not an
`F_17^32` regular-window root table, not a quotient/tangent subtraction table,
and not a singular-pivot packet.

Run:

```sh
python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_n16_k8_a13_rank_node_gcd_toy.json \
  --check experimental/data/certificates/regular-minor-gcd-rank-node-family-toy/f17_n16_k8_a13_rank_node_family_gcd_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/regular-minor-gcd-rank-node-family-toy/f17_n16_k8_a13_rank_node_family_gcd_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py --expect-fail \
  experimental/data/certificates/regular-minor-gcd-rank-node-family-toy/invalid_bad_rank_node_witness_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py --expect-fail \
  experimental/data/certificates/regular-minor-gcd-rank-node-family-toy/invalid_zero_rank_node_witness_packet.json
```
