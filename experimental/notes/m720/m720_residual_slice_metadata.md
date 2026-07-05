# M720 Residual Slice Metadata

Status: PROVED.

Source DAG node: `m720_residual_slice_metadata`.

## Statement

Under the Modal count-ceiling window rule, every `h=7..20` residual cell beyond
the WSL-safe complete zero cells is either a `W<n` window slice or one of
exactly two over-ceiling complete-window cells:

```text
n=32, h=16, q_exp=2
n=32, h=16, q_exp=3
```

## Proof

The verifier mechanically replays the Modal window-selection rule over the
configured grid:

```text
h = 7..20
n in {16,32,64,128,256,1024}
q_exp in {2,3}
```

The window rule starts at `W=2h` and then increases `W` while

```text
C(W-1,h-1) + C(W,h) <= 6,000,000.
```

The complete under-ceiling cells are exactly the six cells handled by the
WSL-safe complete zero-certificate packet. The verifier also detects the edge
case where the initializer already has `W=n` but its cost exceeds the ceiling:
this happens exactly at `n=32,h=16`, for both q-exponents. Every other
residual configured cell has `W<n` and is therefore a window slice.

Thus the residual cell set is fully classified into slices plus the two
over-ceiling complete-window obligations.

## Non-Claims

This packet classifies residual cell metadata only. It does not prove zero
unpaid non-toral survivors for any residual cell and does not promote `W<n`
window slices to complete certificates.

## Replay

Regenerate:

```bash
python3 experimental/scripts/verify_m720_residual_slice_metadata.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_m720_residual_slice_metadata.py \
  --check experimental/data/certificates/m720-residual-slice-metadata/m720_residual_slice_metadata.json
```

The verifier checks note anchors and replays the exact window-classification
arithmetic over the configured grid.
