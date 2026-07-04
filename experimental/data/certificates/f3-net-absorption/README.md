# F3 Net Absorption Certificate

This certificate supports DAG node `p3_affine_net_richline_residue`.

It replays the P3 affine-net obstruction against the unified pullback strip.
The old tangent/quotient/dihedral strip does not remove the P3 toy net, but
the unified mixed degree-1 pullback strip does: every multi-direction rich
point decomposes into `b=2` affine equality fibers.

Replay:

```bash
python3 experimental/scripts/verify_f3_net_absorption.py
```
