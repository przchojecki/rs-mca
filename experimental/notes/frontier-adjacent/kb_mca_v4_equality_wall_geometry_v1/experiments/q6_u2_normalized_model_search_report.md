# Normalized \(Q=6,s=6,u=2\) Search

## Status

This is a complete search inside one printed synthetic,
unramified normalization. It found no fixture. It is experimental
evidence for the component interpolation target, not a proof over
the deployed KoalaBear labels.

The load-bearing proof reductions are in:

```text
proof/q6_u2_plane_map_reduction.md
```

## Exact model

The search uses the prime field

```text
F_2130706433
```

and the involution \(\lambda\mapsto-\lambda\). The ten common pole
points are

\[
\{\pm1,\pm2,\pm3,\pm4,\pm5\}.
\]

The twelve free pole points are arranged in a six-cycle. Row \(j\)
has the two available free roots

\[
-(6+j),\qquad 6+(j-1\bmod6),
\]

for \(j=0,\ldots,5\). The six source nodes used by the
degree-two weighted-GRS condition are

\[
6^2,7^2,8^2,9^2,10^2,11^2.
\]

Every row locator is a monic split quartic selected from its ten
common and two free roots.

## Exact constraints searched

The program imposes all of the following inside this model:

1. every common pole occurs in exactly two of the six quartics;
2. exactly four free pole edges are selected in total;
3. the six quartics satisfy the common degree-two row-scaling
   weighted-GRS condition;
4. the coefficient span has dimension at most three;
5. both exhaustive zero-edge cases are covered:
   two zero-edge rows with distinct quartics, and two zero-edge rows
   with the same quartic.

For distinct zero-edge quartics, every remaining row is tested in
the span of those two quartics and one common residual direction.
The residual direction is drawn from the union of all six row
option sets. For equal zero-edge quartics, the exact coefficient-map
lemma reduces the six rows to a two-dimensional span.

The optimized weighted-GRS test uses monicity to write the six row
scales as values of one quadratic. This gives a \(12\times3\)
homogeneous system. A direct \(15\times6\) parity-check
implementation was evaluated on the same deterministic 20,000
sample tuples and agreed in every trial.

## Result

```text
status=NO_FIXTURE
field=2130706433
rows=6
common_poles=10
free_edge_poles=12
required_owned_edges=4
common_occurrence=2
grs_crosscheck_trials=20000
identical_zero_edge_branch=NO_FIXTURE
distinct_zero_edge_branch=NO_FIXTURE
distinct_common_pairs=21945
```

The \(21{,}945=\binom{210}{2}\) pair count exhausts all distinct
monic quartics supported on four of the ten common roots.

## Replay

The recorded run used:

```text
g++.exe (Rev8, Built by MSYS2 project) 15.2.0
g++ -O3 -std=c++20 q6_u2_normalized_model_search.cpp -o q6_u2_normalized_model_search.exe
q6_u2_normalized_model_search.exe
```

The search takes several minutes on the review machine. The `--quick`
and `--full` packet replays run the frozen-output integrity and
fail-closed checks without executing the search. The separate
`replay.py --full-search` mode compiles the C++20 source, executes it,
and compares the regenerated output with the committed artifact.

## Guardrail

This search does not prove the deployed theorem. In particular:

* the actual divisor \(\psi^*\mathcal K\) may ramify;
* the actual twelve pole labels and six source labels need not be
  simultaneously equivalent to this normalization;
* a no-fixture result in one finite model is not a uniform
  coefficient-elimination theorem;
* no same-record owner payment is emitted.

The valid conclusion is only:

> Within the printed synthetic unramified model, no \(u=2\)
> rank-three locator tuple satisfies the exact incidence and
> weighted-GRS constraints.
