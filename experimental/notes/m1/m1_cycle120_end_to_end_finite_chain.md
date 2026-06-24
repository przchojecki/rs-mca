# M1 Cycle120 End-To-End Finite Chain

Status: CONDITIONAL / AUDIT / END-TO-END-FINITE-CHAIN.

Date: 2026-06-24.

This note packages the current M1 finite evidence into one reviewer-facing
chain. It does not promote the claim to an official ABF counterexample. Its
purpose is narrower: check that the finite numerator, support threshold, smooth
lift, and Cycle120 density gate now fit together without hidden parameter
changes.

## Chain

The current local chain is:

```text
Cycle84 exact product occupancy
  -> Cycle116 fixed-jet support-wise line/MCA lower bound over F_17^16
  -> Cycle116 external packet source-contract comparison
  -> Cycle116 smooth [512,256] lift over F_17^32
  -> Cycle120 support-wise MCA bridge and ABF-facing density gate.
```

The finite numerator is supplied by

```text
python3 experimental/scripts/verify_m1_cycle84_exact_occupancy_chain.py
```

which composes the color-shell witnesses, projected-log certificate, full
projected-census replay receipt, and kernel-lift filter. It gives

```text
N = 52,747,567,092,
m_max(beta) = 2,
ordered off-diagonal energy = 24,
no fibers of size >= 3.
```

The slot identity replay uses the same normalized table digest

```text
47ae84dc2df0fe0b4b43a7e0543b141fb940061fc48ccb80b40ce4e9483abc01.
```

The Cycle116 fixed-jet bridge gives the native support-wise conclusion

```text
LD_sw(RS[F0,D0,137],143) >= N,
```

where `F0=F_17^16`, `|D0|=256`, the co-support size is `113`, and the common
fixed jet has length `sigma=6`.

The native bad-parameter transfer is checked by

```text
python3 experimental/scripts/verify_m1_cycle116_fixed_jet_transfer.py
```

It verifies the common complement-locator truncation
`W=X^143+X^142+X^141+X^140+X^139+X^138`, the formula
`z_T=W(beta)-V_D(beta)/P_T(beta)`, and the nonzero-denominator conditions
needed for distinct `Phi(T)` values to give distinct bad line parameters.

The co-support size and disjoint slot geometry are checked separately by

```text
python3 experimental/scripts/verify_m1_cycle116_slot_assembly.py
```

It verifies the `D0` decomposition into eight `eta^t H32` cosets, the singleton
in the inactive coset, all `336` active slot blocks, and the all-tuple formula
`|J_T|=1+7*16=113`.

The external Cycle116 packet comparison is checked by

```text
python3 experimental/scripts/verify_m1_cycle116_external_packet_contract.py
```

It verifies that the compact contract extracted from the closed PR #96 packet
uses the same field model, three base exponent sets, seven active slot cosets,
co-support clause

```text
J_T={1} union union_{t=1}^7 eta^t lift(i_t,a_t),
```

native parameters `(n,j,sigma,k,agreement)=(256,113,6,137,143)`, smooth-lift
parameters `(n,j,sigma,k,agreement)=(512,250,6,256,262)`, and Cycle84 finite
values as the local chain.

The smooth padding lift preserves the same set of bad parameters and gives

```text
LD_sw(RS[F_17^32,H,256],262) >= N.
```

The concrete smooth padding is checked by

```text
python3 experimental/scripts/verify_m1_cycle116_smooth_padding_transfer.py
```

It verifies the partition of the odd coset into `A` of size `119` and `R` of
size `137`, checks `P_R(beta)!=0`, and checks the degree inequalities that keep
the same bad parameters after lifting to the `[512,256]` row.

At the Cycle120 row

```text
K = F_17^32,
|H| = 512,
k = 256,
delta = 125/256,
```

the domain-generated field ledger is checked by

```text
python3 experimental/scripts/verify_m1_cycle120_domain_field_ledger.py
```

It verifies `ord_512(17)=32`, equivalently that `theta` is not contained in
any proper subfield of `F_17^32`. Thus the smooth domain generator itself
generates the full field, and this row has

```text
q_gen = q_code = q_line = 17^32.
```

the closed agreement threshold is exactly

```text
(1-delta)|H| = 262.
```

The field-size comparison is also exact:

```text
17^32 =
2367911594760467245844106297320951247361,

floor(17^32 / 2^128) = 6,
N = 52,747,567,092 > 6.
```

Thus, conditional on the source-gate and finite-audit boundaries below, the
composed local chain gives the ABF-facing density comparison

```text
epsilon_mca(RS[F_17^32,H,256],125/256)
  >= N / 17^32
  > 2^-128.
```

The definition-level bridge from `LD_sw(C,262)>=N` to this normalized
`epsilon_mca` lower bound is checked by

```text
python3 experimental/scripts/verify_m1_cycle120_supportwise_mca_bridge.py
```

It verifies that `262=ceil((1-125/256)512)`, that the line-parameter
denominator is the same field `17^32`, and that the numerator is the same
Cycle84 value `N` used by the finite chain.

## What This Resolves Locally

Earlier notes left the M1 Cycle120 candidate as several separately checked
pieces. This note and its verifier check that:

```text
the Cycle84 exact occupancy numerator is the same N used downstream;
the Cycle116 slot assembly has co-support size 113;
the external Cycle116 packet contract uses the same verified co-support and
  finite values;
the fixed-jet bad-parameter map is injective on the counted product values;
the smooth padding uses disjoint A/R odd-coset blocks and preserves the same
  bad parameters;
the domain generator theta generates the full field F_17^32, so
  q_gen=q_code=q_line=17^32 for this row;
the Cycle116 slot replay and Cycle84 certificate use the same slot-table digest;
the native Cycle116 parameters are n=256, k=137, agreement=143;
the smooth lift reaches n=512, k=256, agreement=262 without changing N;
the Cycle120 closed threshold at delta=125/256 is exactly 262;
the support-wise line/MCA count normalizes to
  epsilon_mca(C,125/256) >= N/17^32;
the density numerator N is far above the >2^-128 gate.
```

This is a useful stopping point because the remaining work is no longer a
parameter-alignment question. It is concentrated in the explicit review
boundaries below.

## Remaining Promotion Boundaries

The chain remains conditional on:

1. Official ABF PDF/source verification for the admissible row gates, sampler,
   smoothness condition, same-support MCA predicate, and closed-threshold
   convention.
2. Reviewer acceptance that the Cycle84 generated source contract plus the
   replay algorithm audit is sufficient for promotion beyond audit status.
3. Reviewer acceptance that the compact external Cycle116 contract faithfully
   records the hash-pinned files from PR #96.

The current repository verifiers reduce these boundaries, but they do not
remove them.

## Nonclaims

This note does not claim:

```text
an accepted solution to M1;
independent official ABF source validation;
independent human validation of the generated Cycle84 replay source;
the optional Cycle119 strict-inside-radius strengthening;
an ordinary list-decoding lower bound.
```

It records only the composed finite-chain implication supported by the current
local artifacts.

## Reproducibility

Run:

```sh
python3 experimental/scripts/verify_m1_cycle120_end_to_end_chain.py
python3 experimental/scripts/verify_m1_cycle120_end_to_end_chain.py --json
python3 experimental/scripts/verify_m1_cycle116_external_packet_contract.py
python3 experimental/scripts/verify_m1_cycle116_fixed_jet_transfer.py
python3 experimental/scripts/verify_m1_cycle116_smooth_padding_transfer.py
python3 experimental/scripts/verify_m1_cycle120_domain_field_ledger.py
python3 experimental/scripts/verify_m1_cycle120_supportwise_mca_bridge.py
```

The verifier is nonmutating. It imports and runs the lower M1 verifiers, then
checks the exact cross-artifact equalities used in the chain above.
