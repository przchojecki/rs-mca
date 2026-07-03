# Conjecture F Dimension-Two Evidence

- **Status:** EXPERIMENTAL / evidence packet.
- **Agent:** Codex acting autonomously for Allen Graham Hart.
- **Roadmap link:** Fable evidence task `E7` (`conj_f` / `f_primitive_case`).
- **Verifier:** `experimental/scripts/verify_conjecture_f_dim2_evidence.py`.
- **Artifact:** `experimental/data/certificates/conjecture-f-dim2-evidence/conjecture_f_dim2_n16_f17.json`.

This packet is a small, pre-registered evidence run for low-dimensional
Conjecture F geometry.  It does not prove Conjecture F.  In light of the
companion reduction-lemma package in PR #182, fixed projective dimensions are
now theorem-controlled; this packet should be read as calibration and
regression evidence for the first toy dimensions, not as claiming dimension
two is still an open primitive case.

## Object

Let `K = F_17`, let `H = F_17^*`, so `|H| = n = 16`, and let

```text
D_j(H) = { prod_{h in S} (X-h) : S subset H, |S| = j }
```

inside projective locator-coefficient space.  A projective plane `P(W)` is
called common-root paid if all polynomials in `W` vanish at some `h in H`.
The base `j=3` and `j=5` runs have `gcd(n,j)=1`, so there is no proper
quotient-pullback stratum there.  The E10 `j=4` census deliberately does not
have this simplification: quotient orders `2` and `4` are active, so its top
planes should be read as quotient/twin-structured regression data rather than
as a quotient-free primitive residual.

## Pre-Registered Runs

1. Exact projective-plane census at `j=3`.  Here
   `P(K[X]_{<=3}) = P^3`, so projective planes are hyperplanes.  The verifier
   enumerates all `(17^4-1)/(17-1)=5220` hyperplanes, counts their intersections
   with `D_3(H)`, and separates the common-root paid hyperplanes from primitive
   hyperplanes.

2. Deterministic Hankel-kernel sample at `j=5,t=3`.  The verifier samples
   2048 full-rank Hankel row spaces

   ```text
   (s_r, s_{r+1}, ..., s_{r+5}),       r=0,1,2,
   ```

   and counts `D_5(H)` points in the projective kernel plane.  This second run
   is not exhaustive; it is included because it probes the kernel/fiber-plane
   geometry that the proof program actually consumes.

3. E10 exact Grassmannian census at `j=4`.  The companion verifier
   `verify_conjecture_f_dim2_j4_grassmannian.py` enumerates all
   `25,734,890` projective planes in `P(F_17[X]_{<=4})` via the dual
   projective-line Grassmannian.  This is intentionally kept out of the
   base E7 replay because it is much heavier.

## Results

The exact `j=3` census gives:

```text
all projective planes        5220
common-root paid planes        16
common-root hit count         105 = binom(15,2)
primitive planes             5204
max primitive hit count        38
top primitive plane count     240
weighted pair bound floor      60 = floor(binom(16,2)/(3-1))
simple-line bound floor        40 = floor(binom(16,2)/binom(3,2))
```

The paid common-root planes are exactly the expected tangent/common-divisor
shape: fixing one root leaves `binom(15,2)=105` degree-three locators.  After
removing these paid planes, the primitive maximum is only `38`, below even the
simple-line numerical bound `40`.  The top primitive planes have one repeated
evaluation line (`15` distinct evaluation lines, maximum multiplicity `2`), so
the pair-counting explanation should use the weighted form rather than silently
assuming a simple arrangement.

The sampled `j=5,t=3` Hankel-kernel run gives:

```text
accepted full-rank kernel planes     2048
common-root planes seen                 2
max primitive hit count                13
top primitive count in sample           5
weighted pair bound floor              30 = floor(binom(16,2)/(5-1))
simple-line bound floor                12 = floor(binom(16,2)/binom(5,2))
top planes with a twin class          5/5
top planes above simple bound         5/5
```

Most sampled kernel planes have no `D_5(H)` point at all.  No quotient stratum
is present for `j=5`, and no unclassified rich primitive plane appears in this
sample.  The pre-registered QF.4 check is also positive: every sampled top
primitive kernel plane has hit count `13`, just above the simple-line bound
`12`, and every one of these five top planes contains a twin evaluation-line
class.  In fact the recorded profiles all have multiplicity histogram
`1^12 4^1`, so the excess over the simple-line count is explained by repeated
evaluation lines rather than by a new primitive simple-arrangement mechanism.

The E10 `j=4` Grassmannian census gives an exact regression target for the
pair-bound envelope:

```text
all projective planes        25,734,890
common-root paid planes          83,400
primitive planes              25,651,490
primitive max hit count              28
top primitive plane count             9
primitive planes above simple       177
simple-line bound floor              20 = floor(binom(16,2)/binom(4,2))
weighted pair bound floor            40 = floor(binom(16,2)/(4-1))
```

Thus the primitive maximum sits above the simple-line envelope and below the
weighted pair envelope.  All nine top primitive planes have twin evaluation-line
structure, with multiplicity profile `2^8`.  Since `j=4` also has proper
quotient orders, this is evidence for the intended split rather than a
quotient-free theorem: the excess over the simple-line count appears in
structured repeated-line/quotient-compatible planes, not in a recorded
twin-free top plane.

The verifier also replays both runs against the fixed-dimensional/common-root
consumer bound from the Conjecture F reduction lemmas.  For projective
dimension two, every plane with `c` common roots should have at most

```text
binom(16-c,2)
```

hits after common-root accounting.  The exact `j=3` census has zero violations
and the `16` common-root planes are sharp at `binom(15,2)=105`.  The sampled
`j=5` kernel planes also have zero violations; their maximum hit count is far
below the fixed-dimensional bound.

## Interpretation

This moves the E7 prior in the positive direction: the exact toy has only the
expected common-root spike, the kernel-plane sample shows small primitive
intersections, and both are consistent with the fixed-dimensional theorem
consumer.  The evidence also says what to do next.  Future E7 work should not
try to re-prove fixed dimension two; it should either stress-test higher
dimension-growing families, exhaust `n=16,j=4` projective planes as a
regression target with a more efficient Grassmannian enumerator, or replace
random Hankel samples by a structured enumeration of low-complexity syndrome
row spaces.

Non-claims:

- no theorem for arbitrary growing dimension;
- no exhaustive statement for `j=5` kernel planes;
- no M1/MCA threshold or safe-side claim.

## Replay

```bash
python3 experimental/scripts/verify_conjecture_f_dim2_evidence.py
python3 experimental/scripts/verify_conjecture_f_dim2_evidence.py --emit
python3 -m py_compile experimental/scripts/verify_conjecture_f_dim2_evidence.py

# heavier E10 companion replay
python3 experimental/scripts/verify_conjecture_f_dim2_j4_grassmannian.py --emit
python3 experimental/scripts/verify_conjecture_f_dim2_j4_grassmannian.py \
  --check experimental/data/certificates/conjecture-f-dim2-evidence/conjecture_f_dim2_j4_grassmannian.json
```
