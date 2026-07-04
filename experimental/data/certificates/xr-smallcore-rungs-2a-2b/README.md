# XR small-core rungs 2a/2b certificate

This directory contains the deterministic certificate emitted by
`experimental/scripts/verify_xr_smallcore_rungs_2a_2b.py`.

The certificate supports
`experimental/notes/roadmaps/xr_smallcore_rungs_2a_2b.md`: same-slope exact
supports reduce to the list worst-word object, and distinct-slope partial
cores with `k<r<=A-2` reduce to graded tangent-depth cells.

Regenerate and verify:

```bash
python3 experimental/scripts/verify_xr_smallcore_rungs_2a_2b.py --write-certificate
python3 experimental/scripts/verify_xr_smallcore_rungs_2a_2b.py
```
