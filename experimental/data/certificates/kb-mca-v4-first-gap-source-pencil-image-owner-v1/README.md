# KoalaBear first-gap source-pencil image owner

This packet adds one pair-global bankable owner after the active six-owner
KoalaBear partition:

```text
ACTIVE_V4_FIRST_GAP_BASE_RATIONAL_SOURCE_PENCIL_IMAGE
```

Every first-gap full-outside coefficient-rank-two selected slope lies in the
finite image of one base-rational projective point of the intrinsic
two-dimensional source pencil. There are at most `p+1` such points, and each
image has size at most `n-2e`, giving the exact cap

```text
(p+1)(n-2e) = 4,180,889,210,446,272.
```

The successor paid subtotal is `4,200,515,150,819,207`; the remaining
unconditional reserve is `270,780,212,960,575,880`. The row remains open
above the first gap and on the Q/balanced-core branches.

Replay:

```bash
python3 experimental/scripts/verify_kb_mca_v4_first_gap_source_pencil_image_owner_v1.py --check
python3 experimental/scripts/verify_kb_mca_v4_first_gap_source_pencil_image_owner_v1.py --tamper-selftest
```

Current emitted bindings:

```text
row payload       dc3d3d9529b925cb11a66a0b21e677a6514391c705f6a816a57f7e97a37b53d9
manifest payload  cf50619eec7af3b39d03ad7deadc64132637055989dcb5db017b6e946c8c33d7
partition digest  7a57fa877417920862ed2fe2e5c569852555f78b73b046d320d5e7a65d98ebaa
```
