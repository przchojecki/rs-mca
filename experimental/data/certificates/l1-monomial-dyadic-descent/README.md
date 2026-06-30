# L1 Monomial Dyadic Descent Packet

This directory contains a replayable proof packet for the monomial-prefix
locator classification in
`experimental/notes/l1/l1_monomial_dyadic_descent_survivors.md`.

The packet is for the ambient row

```text
F = F_17[z] / (z^32 - 3),    H=<z>,    |H|=512,
degree bound deg P <= 256.
```

It checks the finite gates behind the classification:

```text
local length-16 imbalance lemma,
binomial basis gate for X^h-3,
dyadic divisibility thresholds,
survivor table,
impossible candidate rows,
structural nonemptiness witnesses.
```

For every admissible survivor row, the verifier also constructs an explicit
quotient-complement witness in exponent coordinates and checks the required
power-sum vanishings `p_1,...,p_d` in the `F_17` basis determined by
`alpha^(N/16)=3`.  It then forms the quotient support `T=G_N\C` and checks
the elementary vanishings `e_1(T),...,e_d(T)=0`, which are the actual
quotient coefficient conditions.  Finally it lifts `T` back to a support
`S subset H` and checks `e_1(S),...,e_(A-257)(S)=0` in `F_17[z]/(z^32-3)`,
which is the direct monomial-admissibility condition for `deg P <= 256`.

Run:

```sh
python3 experimental/scripts/verify_l1_monomial_dyadic_descent_packet.py \
  --check experimental/data/certificates/l1-monomial-dyadic-descent/f17_32_n512_deg256_monomial_dyadic_packet.json

python3 experimental/scripts/verify_l1_monomial_dyadic_descent_local16.py
```

Non-claims: this is not an arbitrary-word L1 local-limit theorem, not the
`k=256` finite-row MCA threshold, and not an MCA, line-decoding,
interleaved-list, or protocol theorem.
