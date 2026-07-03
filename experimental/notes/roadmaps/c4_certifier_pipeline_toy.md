# C-4 Certifier Pipeline Toy

- **Task:** C-4.
- **DAG nodes:** `QA.16`, `QA.18`, `height_only_impossibility`,
  `weight_graded_mitm`, `certifier_uniformity`.
- **Status:** TOY TOTALITY ANCHOR / direct mod-p MITM.
- **Verifier:** `experimental/scripts/verify_c4_certifier_pipeline_toy.py`.
- **Artifact:** `experimental/data/certificates/c4-certifier-pipeline-toy/c4_certifier_pipeline_toy.json`.

This packet is a toy end-to-end certifier after the height-only and multiplier
routes have been scoped out.  It uses direct modular sparse-sum enumeration
and an exact complete solver mode, as requested by the C-4 revised protocol.

It does not run `N'=128` and does not perform any heavy search.

## Toy Row

The printed certificate uses:

```text
N' = 16
p  = 12289
w <= 6
```

with `zeta` of order `16` in `F_p`.  The verifier certifies all ternary
vectors `v in {-1,0,1}^{16}` of weight at most `6` satisfying

```text
sum_i v_i zeta^i = 0 mod p.
```

The only relations found are the expected antipodal cyclotomic ones generated
by

```text
zeta^i + zeta^{i+8} = 0.
```

Counts:

```text
weight 2:   8
weight 4:  56
weight 6: 224
total:    288
```

The count formula is

```text
sum_{r=1}^{3} binom(8,r) 2^{r-1} = 288,
```

where the global sign is canonicalized.

## Two Independent Modes

The verifier runs both:

```text
1. split meet-in-the-middle over the first/second 8 exponents;
2. complete branch-and-bound depth-first enumeration with weight pruning.
```

They produce the same relation set.  The branch-and-bound mode is the toy
totality anchor: it is a complete finite solver and therefore emits a verdict,
not an unknown.

Recorded run:

```text
MITM left assignments:        5281
MITM right assignments:       5281
MITM residue pair checks:     5601
B&B nodes visited:         1761761
B&B leaves checked:         686401
non-cyclotomic relations:        0
```

## Corrected MITM Cost Scale

For the real `N'=128` row, the packet records the direct mod-p MITM state
count

```text
binom(N', w/2) 2^(w/2).
```

The corrected scale is:

```text
w=12: log2 states = 38.336607
w=14: log2 states = 43.459989
w=16: log2 states = 48.378852
```

So a `2^40` to `2^50` budget buys roughly the `w=12..16` band, consistent
with the C-4 revised tasking.  This table is arithmetic only; the verifier
does not run those large searches.

## Interpretation

This packet demonstrates the intended post-impossibility certifier shape:

```text
height-only gate: scoping theorem, not enough at N'=128;
multiplier route: not used;
direct mod-p MITM: practical band certifier;
exact B&B mode: totality anchor for toy rows and a format exemplar.
```

For Reading B / procedure-as-determination semantics, the important point is
that the complete mode has a finite search tree and independently matches the
MITM relation set on the printed toy row.

## Replay

```bash
python3 experimental/scripts/verify_c4_certifier_pipeline_toy.py --write
python3 experimental/scripts/verify_c4_certifier_pipeline_toy.py --check
python3 -m py_compile experimental/scripts/verify_c4_certifier_pipeline_toy.py
python3 -m json.tool experimental/data/certificates/c4-certifier-pipeline-toy/c4_certifier_pipeline_toy.json >/dev/null
```

## Nonclaims

This packet does not run `N'=128`, does not prove certifier uniformity for
every admissible prime, does not use or repair the multiplier route, and does
not exclude non-cyclotomic sparse relations at `N'=32`.
