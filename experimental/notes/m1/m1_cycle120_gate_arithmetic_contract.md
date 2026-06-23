# M1 Cycle120 Gate Arithmetic Contract

Status: CONDITIONAL / AUDIT / SOURCE-CHECK-NEEDED.

Date: 2026-06-23.

This is a compact reviewer contract for the Cycle120 ABF-facing M1 candidate.
It extracts only the gate and arithmetic implications from the longer
integration note
`experimental/notes/m1/m1_cycle120_abf_counterexample_candidate.md`.

The companion source-gate audit is:

```text
experimental/notes/m1/m1_cycle120_abf_source_gate_audit.md
```

That audit independently checks the public Proximity Prize page and the author
page identifying ABF ePrint 2026/680, records that direct ePrint PDF retrieval
is still blocked by Cloudflare from this environment, and classifies
Definitions 2.11, 2.12, and 4.3 as checked only against the PR #96 PDF extract
until a human reviewer fetches the official PDF/source directly.

It does not prove the Cycle84 finite count, the full Cycle116 finite-chain
transfer, or the optional Cycle119 strict-ball transfer. It records exactly
what those imports would imply if they survive independent review.

## Object

Use the row

```text
K = F_17^32
H = <theta> <= K^*
|H| = 512
C = RS[K,H,256]
```

with

```text
n = 512
k = 256
rho = 1/2
delta = 125/256
epsilon* = 2^-128
N = 52,747,567,092
```

The extracted ABF gate used by the longer note is:

```text
RS[F,L,k] may be over an arbitrary finite field F.
Smooth means a multiplicative coset of a subgroup of F^* of power-of-two order.
The grand MCA row set includes rate 1/2.
Definition 4.3 samples gamma uniformly from F.
Definition 4.3 uses the same-support event with |S| >= (1-delta)n.
```

The direct official ABF PDF/source check is still open. The local in-repository
definition in `tex/cs25_cap_v4.tex` has the same support-wise form: maximize
over `f1,f2`, sample `gamma <- F`, require a common support `S`, and test
whether `f1 + gamma f2` is code-explained on `S` while `(f1,f2)` is not
simultaneously code-explained on that same `S`.

## Gate Checks

Assuming the extracted ABF gate is faithful, this row passes the parameter
envelope:

```text
field:       K = F_17^32
field cap:   17^32 < 2^256
domain:      |H| = 512 = 2^9
smoothness:  H is asserted to be a multiplicative subgroup <theta>
rate:        256/512 = 1/2
degree cap:  256 <= 2^40
sampler:     gamma is sampled from K
predicate:   support-wise same-support MCA noncontainment
```

The smoothness and generator assertions for `H=<theta>` should be tied to the
finite certificate/proof source before promotion.

## Exact Arithmetic

At the ABF radius

```text
delta = 125/256,
n = 512,
```

the closed agreement threshold is

```text
(1-delta)n = (131/256)512 = 262.
```

The corresponding Hamming distance radius is

```text
delta n = (125/256)512 = 250.
```

Thus:

```text
Cycle116 agreement 262 meets the printed closed threshold.
Cycle119 agreement 263 gives distance 249 < 250.
```

The denominator comparison is exact:

```text
17^32 =
2367911594760467245844106297320951247361

floor(17^32 / 2^128) = 6
52,747,567,092 > 6
```

Equivalently,

```text
52,747,567,092 / 17^32 > 2^-128.
```

## Conditional Implication

If the Cycle116 transfer proves that one pair `(f1,f2)` has at least `N` bad
values `gamma in K`, each with a common support of size at least `262`, then
the local support-wise MCA definition gives

```text
epsilon_mca(C,125/256)
  >= N / |K|
  = 52,747,567,092 / 17^32
  > 2^-128.
```

Under the usual supremum convention for the safe radius `delta*_C`, this rules
out safety at the endpoint:

```text
delta*_C <= 125/256.
```

If the stronger Cycle119 transfer proves the same numerator with agreement
`263`, then the witness is already inside the strict external radius
`delta=125/256`, and the cleaner closed-threshold statement is

```text
delta*_C <= 249/512 < 125/256.
```

This last implication uses agreement `263 = (1 - 249/512)512`.

## Required Imports Before Promotion

The following inputs remain outside this arithmetic contract:

1. Official ABF PDF/source verification, with page references for the row
   gates, sampler, smoothness condition, support-wise predicate, and closed
   threshold. The source-gate audit above gives public-page confirmation plus
   PDF-extract evidence, but not final independent ePrint retrieval.
2. The finite definition of `K`, `theta`, and `H`, including the proof or
   certificate that `H=<theta>` is the intended power-of-two subgroup.
3. The Cycle84 finite count producing
   `N = 52,747,567,092`.
4. The Cycle116 finite-chain transfer producing agreement `262` in the
   support-wise MCA predicate, including the slot-identity replay, the Cycle84
   occupancy census, and the smooth padding lift.
5. Optionally, the Cycle119 two-ended transfer producing agreement `263`.

## Nonclaims

This note does not claim:

```text
an accepted Proximity Prize solution;
an ordinary list-decoding theorem;
a protocol soundness failure;
an exact value of delta*_C;
independent validation of the ABF PDF wording;
independent validation of the Cycle84/Cycle116/Cycle119 imports.
```

It is only the deterministic gate/arithmetic layer that those imports would
feed.

## Reproducibility

The companion nonmutating verifier is:

```sh
python3 experimental/scripts/verify_m1_cycle120_gate_arithmetic.py
python3 experimental/scripts/verify_m1_cycle120_gate_arithmetic.py --json
```

The verifier checks only integer arithmetic and parameter-envelope predicates.
It does not fetch network sources, write files, run generated archives, or
verify the finite count or transfer proofs.
