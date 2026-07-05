# Hankel Termination Assembly

Status: PROVED.

Source DAG node: `f_termination_hankel`.

Depends on:

- `hankel_rank_profile_entropy`;
- `hankel_moment_clean_leaves`.

## Statement

For rate-`1/2` Hankel-kernel instances over `mu_n`, after root-closure
saturation and after routing tangent, common-divisor, quotient, pullback, and
dihedral structure to the paid or reduced ledgers, the number of reachable
unpaid primitive saturated closures is polynomial in `n`. Terminal unpaid
primitive leaves also satisfy the direction-dual moment-count input.

The counted object is the saturated closure state

```text
rcl_P(B union S),
```

not the raw number of support unions. Raw support-union counts can over-count:
the loop-free pair family can have many raw branches while all branches share a
single root-closure state.

## Proof

The conditional implication has two required predicates.

First, `hankel_rank_profile_entropy` gives the state-count bound: unpaid
primitive saturated states are bounded by `n^{O(W^2)}` for fixed cutoff `W`.
This is the family-specific closed-set bound needed after the support-lattice
accounting has reduced descent size to reachable saturated states.

Second, `hankel_moment_clean_leaves` gives the terminal member-count input:
the pinned-value leaf lemma supplies the same moment upper bound as the clean
case, because pinned affine constraints can remove zero assignments but cannot
add members.

Combining these predicates proves the Hankel-family descent termination claim:
there are polynomially many unpaid primitive saturated states, and the terminal
leaves have the member-count control required by the descent accounting.

## Non-Claims

This packet does not count raw support unions, does not produce per-agreement
M3 root tables, and does not close a row-level `F_17^32` safe-side certificate.
It packages the proved saturated-state termination subgraph used by the
aperiodic Hankel program.

## Replay

```bash
python3 experimental/scripts/verify_hankel_termination_assembly.py --emit
python3 experimental/scripts/verify_hankel_termination_assembly.py \
  --check experimental/data/certificates/hankel-termination-assembly/hankel_termination_assembly.json
```
