# M1 Cycle120 Finite Obstruction Theorem

Status: CONDITIONAL / AUDIT / CYCLE120-FINITE-OBSTRUCTION-THEOREM.

Date: 2026-06-24.

This note is the reviewer-facing theorem ledger for PR #100. It does not add a
new proof ingredient. It states the finite obstruction now proved by the local
M1 chain, records the exact source condition, and points to the verifiers that
discharge each proof layer.

The companion verifier is:

```text
python3 experimental/scripts/verify_m1_cycle120_obstruction_theorem.py
```

## Source-Conditioned Theorem

Let

```text
K = F_17^32,
H = <theta> <= K^*,
|H| = 512,
C = RS[K,H,256].
```

Assume:

1. The PR #96 ABF PDF extract is faithful to the official ABF ePrint source,
   including the smooth-domain definition, the grand MCA row envelope, the
   uniform `gamma <- F` sampler, the same-support predicate, and the closed
   support threshold.
2. The Cycle84 finite-source closure audit is accepted as a valid exact
   product-occupancy proof.
3. If the external PR #96 packet is cited directly, its provenance is accepted.

Then

```text
epsilon_mca(C,125/256)
  >= 52,747,567,092 / 17^32
  > 2^-128.
```

Equivalently, under those conditions this row is not safe at the printed
closed threshold `delta=125/256`.

The strict-ball addendum is also locally theorem-backed:

```text
LD_sw(RS[F_17^32,H,256],263) >= 52,747,567,092,
```

which gives distance `249 < 250 = (125/256)512`.

## Proof Ledger

The proof is the composition of the following local results.

### Cycle84 finite numerator

```text
python3 experimental/scripts/verify_m1_cycle84_exact_occupancy_chain.py
```

This gives:

```text
N = 52,747,567,092,
m_max = 2,
ordered off-diagonal energy = 24.
```

It composes the color-shell witnesses, projected-log certificate, full
projected-census replay receipt, generated source contract, replay-algorithm
audit, and kernel-lift filtering. Its remaining promotion boundary is reviewer
acceptance of that finite-source closure.

### Native fixed-jet line

```text
python3 experimental/scripts/verify_m1_fixed_jet_ldsw_theorem.py
```

This proves the generic fixed-jet locator theorem and checks the Cycle116
instantiation:

```text
LD_sw(RS[F_17^16,D0,137],143) >= N.
```

### Smooth Cycle120 lift

```text
python3 experimental/scripts/verify_m1_smooth_padding_ldsw_theorem.py
```

This proves the generic `L_A` multiplication/division theorem and checks the
Cycle116-to-Cycle120 instantiation:

```text
143 + 119 = 262,
137 + 119 = 256,
113 + 137 = 250.
```

Therefore

```text
LD_sw(RS[F_17^32,H,256],262) >= N.
```

### Support-wise MCA bridge

```text
python3 experimental/scripts/verify_m1_cycle120_supportwise_mca_bridge.py
```

At `delta=125/256`, the closed support threshold is

```text
ceil((1-delta)512) = 262.
```

The bridge converts the fixed-line support-wise count into the normalized
MCA lower bound

```text
epsilon_mca(C,125/256) >= N/17^32.
```

Since

```text
floor(17^32 / 2^128) = 6
```

and `N` is much larger than `6`, the lower bound is strictly greater than
`2^-128`.

### Strict-ball addendum

```text
python3 experimental/scripts/verify_m1_two_ended_fixed_jet_ldsw_theorem.py
```

This proves the generic two-ended fixed-jet theorem and checks the Cycle119
instantiation:

```text
j = 249,
sigma = 7,
k = 256,
agreement = 263,
distance = 249.
```

This addendum is not needed for the printed closed ABF threshold, but it
addresses stricter open-ball interpretations.

### Source condition

```text
python3 experimental/scripts/verify_m1_cycle120_abf_extract_sources.py
```

This hash-binds the PR #96 ABF PDF extract, text extracts, rendered source
pages 5, 9, and 17, and the Cycle120 ABF packet zip. It does not replace
independent official ePrint retrieval and revision review.

## Nonclaims

This theorem ledger does not claim:

```text
an accepted Proximity Prize solution;
independent official ABF source verification;
independent maintainer acceptance of the Cycle84 finite-source closure;
an ordinary list-decoding lower bound;
a protocol soundness failure;
the exact value of delta*_C.
```

It records the precise source-conditioned finite obstruction supported by the
current local artifacts.

## Reproducibility

Run:

```sh
python3 experimental/scripts/verify_m1_cycle120_obstruction_theorem.py
python3 experimental/scripts/verify_m1_cycle120_obstruction_theorem.py --json
```

The verifier imports the current end-to-end finite chain and ABF extract-source
audit, then checks that the closed-threshold obstruction, strict-ball addendum,
field ledger, proof-theorem layers, density gate, and remaining promotion
boundaries are all recorded consistently.
